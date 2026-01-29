import gradio as gr
import os
from groq import Groq
from PyPDF2 import PdfReader
from docx import Document

# 1. SETUP CLIENT & MODEL
api_key = os.environ.get("GROQ_API_KEY")
# Note: On local, you might need python-dotenv to load this. 
# For this archive file, it's fine as is.

if api_key:
    client = Groq(api_key=api_key)
else:
    client = None # Handle missing key gracefully for archive

# UPDATED MODEL: Using the powerful Llama 3.3 70B for best reasoning
MODEL_ID = "llama-3.3-70b-versatile" 

# 2. IMPROVED CSS - High Contrast for Dark Mode
CSS = """
/* 1. Fix the 'Duplicate' button if it appears */
.duplicate-button { 
    margin: auto !important; 
    color: white !important; 
    background: black !important; 
    border-radius: 100vh !important;
}

/* 2. Global Text Styling for Dark Theme */
h3, p, h1 { 
    text-align: center; 
    color: white !important; /* Force all text to be white */
}

/* 3. FIX: Custom Footer (SIC Team 013) */
footer { 
    text-align: center; 
    padding: 10px; 
    width: 100%; 
    background-color: #000000 !important; /* Black background */
    z-index: 1000; 
    position: relative; 
    margin-top: 10px; 
    color: white !important; /* White text */
    border-top: 1px solid #333;
}

/* 4. FIX: Standard Gradio Footer (Use via API) */
.gradio-container .footer a, .gradio-container .footer {
    color: #aaaaaa !important; 
    display: none !important; 
}
"""

TITLE = "<h1>📄 Intelligent Resume Screener (SIC Team 013) 📄</h1>"

# 3. HELPER FUNCTIONS
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def process_upload(file):
    if file is not None:
        file_type = file.name.split('.')[-1].lower()
        if file_type == 'pdf':
            return extract_text_from_pdf(file.name)
        elif file_type == 'docx':
            return extract_text_from_docx(file.name)
    return ""

def generate_llm_response(system_prompt, user_prompt, temperature=0.5):
    if not client:
        return "Error: GROQ_API_KEY not found. Please set it in Settings."
        
    try:
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=1024,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {str(e)}"

# 4. CORE LOGIC FUNCTIONS
def analyze_resume(resume_text, job_description, use_jd, temp):
    if use_jd:
        prompt = f"""
        Analyze this resume against the Job Description. 
        STRICT OUTPUT FORMAT REQUIRED:
        1. Match Score: [0-100]%
        2. Missing Keywords: [List]
        3. Analysis: (3 lines summary)
        4. Recommendations: (3 specific bullet points)

        Job Description: {job_description}
        Resume: {resume_text}
        """
        sys_prompt = "You are a strict ATS Scanner. Be critical and objective."
    else:
        prompt = f"""
        Analyze this resume for general quality.
        1. Score: [0-10]/10
        2. Strengths: Impact, Brevity, Style.
        3. Weaknesses: Formatting, Passive Voice, Vague terms.
        4. Improvements: 3 specific actionable tips.
        
        Resume: {resume_text}
        """
        sys_prompt = "You are a Professional Career Coach."
        
    return generate_llm_response(sys_prompt, prompt, temp)

def write_cover_letter(resume_text, job_description, temp):
    prompt = f"""
    Write a professional cover letter based on this resume and job description.
    Tone: Professional, enthusiastic, and tailored.
    Length: 250-300 words.
    
    Resume: {resume_text}
    Job Description: {job_description}
    """
    return generate_llm_response("You are an expert Copywriter for HR.", prompt, temp)

def generate_questions(job_description, temp):
    prompt = f"""
    Generate 10 interview questions based on this job description.
    Include: 3 Technical, 3 Behavioral, 2 Situational, 2 Cultural fit.
    
    Job Description: {job_description}
    """
    return generate_llm_response("You are a Senior Hiring Manager.", prompt, temp)

# 5. GRADIO INTERFACE CONSTRUCTION
with gr.Blocks(css=CSS, theme="Nymbo/Nymbo_Theme") as demo:
    gr.HTML(TITLE)
    
    with gr.Tab("🚀 Resume Analyzer"):
        gr.Markdown("### Upload Resume & Compare with Job Description")
        with gr.Row():
            with gr.Column():
                resume_file = gr.File(label="Upload Resume (PDF/DOCX)")
                use_jd = gr.Checkbox(label="Analyze with Job Description", value=True)
                job_desc_input = gr.Textbox(label="Job Description", lines=5, placeholder="Paste JD here...")
                
            with gr.Column():
                resume_text_display = gr.Textbox(label="Parsed Resume Content", lines=10, interactive=False)
        
        analyze_btn = gr.Button("🔍 Analyze Resume", variant="primary")
        analysis_output = gr.Markdown(label="Analysis Results")

    with gr.Tab("✍️ Cover Letter"):
        gr.Markdown("### Generate a Tailored Cover Letter")
        create_cl_btn = gr.Button("Generate Cover Letter", variant="primary")
        cl_output = gr.Markdown()

    with gr.Tab("❓ Interview Prep"):
        gr.Markdown("### Predict Interview Questions")
        iq_jd_input = gr.Textbox(label="Job Description (for Questions)", lines=3)
        create_iq_btn = gr.Button("Generate Questions", variant="primary")
        iq_output = gr.Markdown()

    with gr.Accordion("⚙️ Advanced Settings", open=False):
        temp_slider = gr.Slider(0, 1, value=0.5, label="Creativity (Temperature)")

    # -- EVENT LISTENERS --
    resume_file.upload(process_upload, inputs=[resume_file], outputs=[resume_text_display])
    
    analyze_btn.click(
        analyze_resume, 
        inputs=[resume_text_display, job_desc_input, use_jd, temp_slider], 
        outputs=[analysis_output]
    )
    
    create_cl_btn.click(
        write_cover_letter,
        inputs=[resume_text_display, job_desc_input, temp_slider],
        outputs=[cl_output]
    )
    
    create_iq_btn.click(
        generate_questions,
        inputs=[iq_jd_input, temp_slider],
        outputs=[iq_output]
    )

    gr.HTML("<footer><p>SIC Team 013 - Phase 0 Module</p></footer>")

if __name__ == "__main__":
    demo.launch()