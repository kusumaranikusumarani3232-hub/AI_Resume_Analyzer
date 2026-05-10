import streamlit as st
import pdfplumber
from groq import Groq

# -----------------------------
# GROQ API
# -----------------------------
import os

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
)

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

st.title("📄 AI Resume Analyzer")

st.write(
    "Upload your resume and get AI-powered analysis."
)

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

# -----------------------------
# PDF TEXT EXTRACTION
# -----------------------------
if uploaded_file is not None:

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted

    st.success("✅ Resume uploaded successfully!")

    # -----------------------------
    # ANALYZE BUTTON
    # -----------------------------
    if st.button("Analyze Resume"):

        with st.spinner("Analyzing Resume..."):

            prompt = f"""
            Analyze the following resume and provide:

            1. Professional Summary
            2. Technical Skills
            3. Missing Skills
            4. Resume Improvements
            5. Suitable Job Roles
            6. ATS Score out of 100
            7. Career Recommendations

            Resume:
            {text}
            """

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            result = response.choices[0].message.content

        st.balloons()

        st.subheader("📊 AI Resume Analysis")

        st.write(result)