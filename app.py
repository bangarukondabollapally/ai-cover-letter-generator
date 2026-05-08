import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser


# Schema
class CoverLetter(BaseModel):
    cover_letter: str


# Model
model = ChatGroq(model="llama-3.3-70b-versatile")


# Prompt Template
template = ChatPromptTemplate.from_messages([
    ("system", """You are a professional cover letter writer.
Generate a cover letter for someone APPLYING to a new company.

Candidate level detection:
- If experience mentions only personal projects, college work or 
  self-built projects → treat as FRESHER
  Use words like: "aspiring", "passionate", "eager to learn", 
  "hands-on project experience"
  Avoid: "seasoned", "accomplished", "veteran", "experienced professional"
- Never use the word "basic" to describe 
  candidate's skills, use "working knowledge" 
  or "proficiency" instead

- If experience mentions actual job roles, internships at companies,
  or years of work experience → treat as EXPERIENCED
  Use words like: "proven track record", "demonstrated expertise",
  "professional experience"

Instructions:
- If company name is mentioned, use it. If not, use "your organization"
- If JD is vague or minimal, focus more on skills and experience
- Always write as if candidate is APPLYING, not already working there
- Keep it between 3-4 paragraphs
- Avoid buzzwords like "drive innovation", "esteemed organization"
- Always end with "Sincerely, [Your Name]"
- Mirror JD keywords if provided, otherwise highlight skills strongly
- Always capitalize tool/technology names properly
- Capitalize only the first letter of technology 
  names, never use ALL CAPS
  Example: Python, Docker, DBMS — not PYTHON, DOCKER
- Exception: Acronyms like DBMS, OOP, API are fine in caps
- Do not mention "I have attached my resume as this is a standalone cover letter
Tone guidelines:
- formal: professional language, no contractions
- friendly: warm, conversational  
- confident: bold, achievement-focused

Tone should be {tone}.
{format_instructions}"""),

    ("human", "Here are my details:\n{details}")
])


# Parser
parser = PydanticOutputParser(pydantic_object=CoverLetter)


# Streamlit UI
st.title("AI Cover Letter Generator")

details = st.text_area(
    "Enter your details (JD, skills, experience):",
    placeholder="Example: Applying for AI intern role. Skills: Python, LangChain. Experience: Built 2 Gen AI projects"
)

tone_descriptions = {
    "formal": "📋 Best for corporate companies, banks, large enterprises",
    "friendly": "😊 Best for startups, creative agencies, small teams",
    "confident": "💪 Best for tech companies, competitive roles, internships"
}

tone = st.selectbox("Select Tone", list(tone_descriptions.keys()))

# Show guide below selectbox
st.caption(tone_descriptions[tone])


if st.button("Generate Cover Letter"):

    if not details:
        st.error("Please enter your details.")
    else:

        final_prompt = template.invoke(
            {
                "tone": tone,
                "details": details,
                "format_instructions": parser.get_format_instructions()
            }
        )

        response = model.invoke(final_prompt)

        parsed_output = parser.parse(response.content)

        st.subheader("Generated Cover Letter")

        lines = parsed_output.cover_letter.count('\n') + 10
        dynamic_height = max(200, lines * 30)
        st.text_area("Cover Letter", parsed_output.cover_letter, height=dynamic_height)
        st.success("Cover letter generated! Copy it from the box above.")
        st.balloons()