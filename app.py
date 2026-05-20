import streamlit as st

from model import generate_cover_letter


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
        cover_letter = generate_cover_letter(details, tone)

        st.subheader("Generated Cover Letter")

        lines = cover_letter.count('\n') + 10
        dynamic_height = max(200, lines * 30)
        st.text_area("Cover Letter", cover_letter, height=dynamic_height)
        st.success("Cover letter generated! Copy it from the box above.")
        st.balloons()