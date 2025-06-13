from fpdf import FPDF
import json

def clean_text(text):
    replacements = {
        '\u2019': "'",   # right single quote → apostrophe
        '\u2018': "'",   # left single quote → apostrophe
        '\u201c': '"',   # left double quote → quote
        '\u201d': '"',   # right double quote → quote
        '\u2014': '-',   # em dash → hyphen
        '\u2022': '-',   # bullet → hyphen
        '\u00a0': ' ',   # non-breaking space
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    return text

class PDF(FPDF):
    def __init__(self, person_name=None):
        super().__init__()
        self.person_name = person_name

    def header(self):
        self.set_font("Helvetica", "B", 16)
        title = "Resume Analysis Report"
        if self.person_name:
            title += f" - {clean_text(self.person_name)}"
        self.cell(0, 10, title, ln=True, align="C")
        self.ln(5)

    def section_title(self, title):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(30, 30, 30)
        self.cell(0, 8, clean_text(title), ln=True)
        self.set_text_color(0, 0, 0)

    def section_body(self, text):
        self.set_font("Helvetica", "", 11)
        self.multi_cell(0, 6, clean_text(text))
        self.ln(2)

    def bullet_list(self, items):
        self.set_font("Helvetica", "", 11)
        for item in items:
            self.cell(5)
            self.multi_cell(0, 6, f"- {clean_text(item)}")
        self.ln(2)

def generate_pdf_report(json_path, output_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    analysis = {k: v for k, v in data.items() if k not in ["resume_data", "score_breakdown"]}
    resume = data.get("resume_data", {})
    score = data.get("score_breakdown", {})

    person_name = resume.get("personal_info", {}).get("name", None)
    pdf = PDF(person_name)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Score summary
    pdf.section_title("Score Breakdown")
    for k, v in score.items():
        label = k.replace("_", " ").capitalize()
        pdf.section_body(f"{label}: {v}/100" if k == "total_score" else f"{label}: {v}")

    # Strengths and suggestions
    pdf.section_title("Well-Written Sections")
    pdf.bullet_list(analysis.get("well_written_sections", []))

    pdf.section_title("Improvement Suggestions")
    pdf.bullet_list(analysis.get("improvement_suggestions", []))

    pdf.section_title("Skills Sentiment Summary")
    pdf.section_body(analysis.get("skills_sentiment_summary", "N/A"))

    # Resume data
    pdf.section_title("Resume Summary")

    personal_info = resume.get("personal_info", {})
    pdf.section_body(f"Name: {personal_info.get('name', 'N/A')}")
    pdf.section_body(f"Email: {personal_info.get('email', 'N/A')}")
    if "mobile" in personal_info:
        pdf.section_body(f"Mobile: {personal_info.get('mobile')}")
    if "location" in personal_info:
        pdf.section_body(f"Location: {personal_info.get('location')}")

    pdf.section_title("Education")
    for edu in resume.get("education", []):
        line = f"{edu.get('degree', '')}, {edu.get('institution', '')} ({edu.get('year', '')})"
        pdf.section_body(line)

    pdf.section_title("Experience")
    for exp in resume.get("experience", []):
        title = exp.get("title", "")
        company = exp.get("company", "")
        duration = exp.get("duration", "")
        details = exp.get("details", "")
        pdf.section_body(f"{title} at {company} ({duration})")
        pdf.section_body(f"- {details}")

    pdf.section_title("Projects")
    for proj in resume.get("projects", []):
        pdf.section_body(f"{proj.get('title', '')}: {proj.get('description', '')}")

    pdf.section_title("Skills")
    pdf.bullet_list(resume.get("skills", []))

    # Save to file
    pdf.output(output_path)
    print(f"PDF report generated at: {output_path}")