from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser

class CoverLetter(BaseModel):
    cover_letter: str


def get_model() -> ChatGroq:
    """Initialize and return the Groq LLM model."""
    return ChatGroq(model="llama-3.3-70b-versatile")


def get_template() -> ChatPromptTemplate:
    """Return the cover letter prompt template."""
    return ChatPromptTemplate.from_messages([
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


def get_parser() -> PydanticOutputParser:
    """Return the output parser for CoverLetter model."""
    return PydanticOutputParser(pydantic_object=CoverLetter)


def generate_cover_letter(details: str, tone: str) -> str:
    """Generate a cover letter based on candidate details and desired tone.

    Args:
        details: Candidate's details (JD, skills, experience, etc.)
        tone: Desired tone - one of "formal", "friendly", or "confident"

    Returns:
        The generated cover letter text.
    """
    model = get_model()
    template = get_template()
    parser = get_parser()

    final_prompt = template.invoke({
        "tone": tone,
        "details": details,
        "format_instructions": parser.get_format_instructions()
    })

    response = model.invoke(final_prompt)
    parsed_output = parser.parse(response.content)

    return parsed_output.cover_letter


def main():
    """CLI entry point for generating a cover letter."""
    details = input("Enter your details (JD, skills, experience): ")
    tone = input("What type of tone do you want (formal/friendly/confident)? : ")

    cover_letter = generate_cover_letter(details, tone)
    print(cover_letter)


if __name__ == "__main__":
    main()
