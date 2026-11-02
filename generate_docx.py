import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_report_docx():
    doc = docx.Document()

    # Set page margins
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    # Title section
    p_tag = doc.add_paragraph()
    r_tag = p_tag.add_run("NPC CAPSTONE PROJECT ASSIGNMENT (UNIT 1)")
    r_tag.font.name = "Arial"
    r_tag.font.size = Pt(13)
    r_tag.font.bold = True
    r_tag.font.color.rgb = RGBColor(43, 108, 176)
    p_tag.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_title = doc.add_paragraph()
    r_title = p_title.add_run("MALWARE ANALYSIS SANDBOX USING VIRTUALBOX OR VMWARE")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(15, 37, 55)
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run("Comprehensive Design, Empirical Network Containment, Process Triage, Static Cryptographic Identification, and Snapshot Forensic Recovery")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(10.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(74, 85, 104)
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph()

    # Student metadata table
    info = [
        ("Submitted By:", "Aditya Arun Shelke"),
        ("PRN Number:", "2125UCSM1052"),
        ("Program / Degree:", "Bachelor of Technology (B.Tech)"),
        ("Department:", "Computer Science Engineering"),
        ("Specialization:", "Cyber Security"),
        ("University:", "Sanjivani University, Kopargaon"),
        ("Academic Year:", "2026–2027"),
        ("Subject:", "NPC - Unit 1 (Network Programming & Cyber Security)"),
        ("Project Type:", "Capstone Project Submission"),
        ("Repository:", "https://github.com/AdityaShelke2209/NPC-CAPSTONE-Activity-52-.git")
    ]

    table = doc.add_table(rows=len(info), cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    for idx, (k, v) in enumerate(info):
        row = table.rows[idx]
        c0 = row.cells[0]
        c1 = row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.5)

        p0 = c0.paragraphs[0]
        r0 = p0.add_run(k)
        r0.font.bold = True
        r0.font.size = Pt(9.5)
        r0.font.name = "Arial"

        p1 = c1.paragraphs[0]
        r1 = p1.add_run(v)
        r1.font.size = Pt(9.5)
        r1.font.name = "Arial"
        if k in ["Submitted By:", "PRN Number:"]:
            r1.font.bold = True

        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F1F5F9"/>')
        c0._tc.get_or_add_tcPr().append(shd)

    doc.add_paragraph()
    doc.add_page_break()

    # Read and parse report_source.md
    with open("report/report_source.md", "r", encoding="utf-8") as f:
        text = f.read()

    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("# NPC CAPSTONE") or line.startswith("# MALWARE") or "Student Identification" in line:
            while i < len(lines) and not lines[i].startswith("## Abstract"):
                i += 1
            continue

        if line.startswith("## "):
            heading = doc.add_heading(line.replace("## ", "").strip(), level=1)
            heading.paragraph_format.space_before = Pt(14)
            heading.paragraph_format.space_after = Pt(6)
        elif line.startswith("### "):
            heading = doc.add_heading(line.replace("### ", "").strip(), level=2)
            heading.paragraph_format.space_before = Pt(10)
            heading.paragraph_format.space_after = Pt(4)
        elif line.startswith("#### "):
            heading = doc.add_heading(line.replace("#### ", "").strip(), level=3)
            heading.paragraph_format.space_before = Pt(8)
            heading.paragraph_format.space_after = Pt(2)
        elif line.startswith("```"):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            code_p = doc.add_paragraph()
            code_p.paragraph_format.space_before = Pt(4)
            code_p.paragraph_format.space_after = Pt(4)
            code_run = code_p.add_run("\n".join(code_lines))
            code_run.font.name = "Consolas"
            code_run.font.size = Pt(8.5)
            code_run.font.color.rgb = RGBColor(30, 41, 59)
        elif line.startswith("- ") or line.startswith("* "):
            doc.add_paragraph(line[2:], style="List Bullet")
        elif len(line) > 3 and line[0].isdigit() and line[1:3] == ". ":
            doc.add_paragraph(line[3:], style="List Number")
        elif line.strip() == "---":
            pass
        elif line.strip():
            p = doc.add_paragraph(line.strip())
            p.paragraph_format.space_after = Pt(5)
        i += 1

    doc.save("Report.docx")
    doc.save("report/Report.docx")
    print("Report.docx generated successfully!")

if __name__ == "__main__":
    create_report_docx()
