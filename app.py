import base64
import streamlit as st
import io
import fitz  # PyMuPDF

import google.generativeai as genai

GOOGLE_API_KEY = st.secrets["KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

def get_gemini_response(pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the PDF file
        pdf_data = uploaded_file.read()
        
        # Open the PDF using PyMuPDF
        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
        
        # Extract images from the first page
        first_page = pdf_document.load_page(0)
        images = first_page.get_pixmap()
        
        # Convert image data to bytes
        img_byte_arr = images.tobytes()
        
        # Encode to base64
        img_base64 = base64.b64encode(img_byte_arr).decode()
        
        pdf_parts = [{
            "mime_type": "image/jpeg",
            "data": img_base64
        }]
        
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
job_description = st.text_area("Job Description: ", key="job_description")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage match")

input_prompt1 = """
As an experienced Technical Human Resource Manager, your task is to review the provided resume and provide a comprehensive analysis of the candidate's qualifications and experiences.
Please ensure that your analysis focuses exclusively on the content of the resume without incorporating any details from the job description.
Highlight specific skills, experiences, and achievements showcased in the resume, and identify any areas where the candidate's qualifications may require further development or clarification.
Your evaluation should be strictly confined to the information provided in the resume, excluding any references to the job description.
"""


input_prompt3 = """
You are an advanced ATS (Applicant Tracking System) scanner designed for precise evaluation of resumes against job descriptions. Your task is to conduct a rigorous analysis and provide actionable insights.

**1. Percentage Match (Strict):**
Calculate the percentage match between the resume and the job description by considering only exact matches of keywords and criteria from both the job description and the resume content.
Disregard any partial matches or variations in spelling or wording.
Utilize advanced algorithms to ensure strict alignment of candidate's skills and qualifications with the job requirements based on both the job description and the resume content.
Emphasize exact skill set match and keyword accuracy to provide a stringent evaluation.

**2. Missing Keywords and Skill Match (Strict):**
Identify the main keywords from the job description that are essential for the role.
Then, strictly compare these keywords with the candidate's skills and qualifications listed in the resume content.
Highlight any missing keywords or skills from the resume that are crucial for the job, ensuring precision in evaluation.
Prioritize candidates with a precise match of skills and qualifications to the job requirements based on both the job description and the resume content.

**3. Recommendations for Improvement (Strict):**
Offer precise recommendations and optimization strategies to enhance the alignment between the resume and the job description.
Provide specific advice for the candidate to address any gaps or deficiencies in their qualifications based on both the job description and the resume content.
Focus on strict adherence to the job requirements and emphasize the importance of accuracy and relevance in resume optimization.

**Desired Output Structure:**
- **Percentage Match**: [Percentage]
- **Missing Keywords and Skill Match**:
  - [Missing Keyword/Skill 1]
  - [Missing Keyword/Skill 2]
  - ...
- **Recommendations for Improvement**:
  - [Recommendation 1]
  - [Recommendation 2]
  - [Recommendation 3]
  - [Recommendation 4]
  - ...
  provide in detail
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(pdf_content, input_prompt1)
        st.subheader("The Response is")
        st.markdown(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(pdf_content, job_description + input_prompt3)
        st.subheader("The Response is")
        st.markdown(response)
    else:
        st.write("Please upload the resume")
hide_streamlit_style = """
            <style>
            [data-testid="stToolbar"] {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
