from fpdf import FPDF
import os
import re
import json
import pandas as pd
from pptx import Presentation

def generate_pdf_report(session, filename="summary.pdf"):
    pdf = FPDF()
    pdf.add_page()

    font_path = os.path.join("assets", "fonts", "DejaVuSans.ttf")
    pdf.add_font('DejaVu', '', font_path, uni=True)
    pdf.set_font('DejaVu', '', 14)

    pdf.cell(0, 10, f"Dataset: {session.get('name', 'Unnamed Dataset')}", ln=True)

    pdf.cell(0, 10, "Insights:", ln=True)
    for insight in session.get('insights', []):
        pdf.multi_cell(0, 10, f"{insight['question']}\n{insight['result']}\n")

    pdf.cell(0, 10, "Chat History:", ln=True)
    for chat in session.get('chat_history', []):
        pdf.multi_cell(0, 10, f" {chat['user']}\n🤖 {chat['assistant'].get('response', '')}\n")

    output_path = os.path.join("exports", filename)
    pdf.output(output_path)
    return output_path


from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

def generate_pdf_report(session, filename="summary.pdf"):
    pdf = FPDF()
    pdf.add_page()

    font_path = os.path.join("assets", "fonts", "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "", font_path)
    pdf.set_font("DejaVu", "", 14)

    pdf.cell(0, 10, f"Dataset: {session.get('name', 'Unnamed Dataset')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.cell(0, 10, "Insights:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    insight_list = session.get("insights") or session.get("selected_insight_results", [])
    for insight in insight_list:
        pdf.multi_cell(0, 10, f"Question: {insight['question']}\nAnswer: {insight['result']}\n")

    pdf.cell(0, 10, "Chat History:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    for chat in session.get('chat_history', []):
        user_msg = chat.get('user', '')
        assistant_msg = chat.get('assistant', {}).get('response', '')
        pdf.multi_cell(0, 10, f"User: {user_msg}\nBot: {assistant_msg}\n")

    os.makedirs("exports", exist_ok=True)
    output_path = os.path.join("exports", filename)
    pdf.output(output_path)
    return output_path

def export_to_pptx(session, filename="summary.pptx"):
    prs = Presentation()

    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = f"Dataset: {session.get('name', 'Unnamed Dataset')}"
    insight_list = session.get("insights") or session.get("selected_insight_results", [])
    for insight in insight_list:
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = f"{insight['question']}"
        slide.shapes.placeholders[1].text = insight['result']

    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Chat History"
    chat_text = ""
    for chat in session.get('chat_history', []):
        chat_text += f"{chat['user']}\n {chat['assistant'].get('response', '')}\n\n"

    slide.shapes.placeholders[1].text = chat_text

    output_path = os.path.join("exports", filename)
    prs.save(output_path)
    return output_path



