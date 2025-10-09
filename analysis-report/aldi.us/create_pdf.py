#!/usr/bin/env python3
"""Create PDF version of technical analysis using reportlab"""

import sys
import os
from pathlib import Path

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
    from reportlab.pdfgen import canvas
    reportlab_available = True
except ImportError:
    reportlab_available = False

def create_pdf_from_markdown(md_file_path: str, pdf_file_path: str):
    """Create PDF from markdown content using reportlab"""
    
    if not reportlab_available:
        print("❌ ReportLab not available. Install with: pip install reportlab")
        return False
        
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        pdf_file_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.darkblue
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',  
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=10,
        spaceBefore=15,
        textColor=colors.darkred
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_JUSTIFY
    )
    
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Code'],
        fontSize=9,
        fontName='Courier',
        leftIndent=20,
        backgroundColor=colors.lightgrey,
        spaceBefore=10,
        spaceAfter=10
    )
    
    # Build document content
    story = []
    lines = content.split('\n')
    
    in_code_block = False
    code_content = []
    
    for line in lines:
        line = line.strip()
        
        # Handle code blocks
        if line.startswith('```'):
            if in_code_block:
                # End of code block
                if code_content:
                    code_text = '\n'.join(code_content)
                    story.append(Paragraph(code_text, code_style))
                    story.append(Spacer(1, 12))
                code_content = []
                in_code_block = False
            else:
                # Start of code block
                in_code_block = True
            continue
            
        if in_code_block:
            code_content.append(line)
            continue
            
        if not line:
            story.append(Spacer(1, 12))
            continue
            
        # Handle different markdown elements
        if line.startswith('# '):
            # Main title
            title_text = line[2:].replace('*', '').replace('_', '')
            story.append(Paragraph(title_text, title_style))
            story.append(Spacer(1, 20))
            
        elif line.startswith('## '):
            # Section heading
            heading_text = line[3:].replace('*', '').replace('_', '')
            story.append(Paragraph(heading_text, heading_style))
            story.append(Spacer(1, 10))
            
        elif line.startswith('### '):
            # Subsection heading
            subheading_text = line[4:].replace('*', '').replace('_', '')
            story.append(Paragraph(subheading_text, subheading_style))
            story.append(Spacer(1, 8))
            
        elif line.startswith('**') and line.endswith('**'):
            # Bold paragraph
            bold_text = f"<b>{line[2:-2]}</b>"
            story.append(Paragraph(bold_text, normal_style))
            
        elif line.startswith('- ') or line.startswith('* '):
            # Bullet point
            bullet_text = f"• {line[2:]}"
            story.append(Paragraph(bullet_text, normal_style))
            
        elif line.startswith('| '):
            # Table row (simple handling)
            table_text = line.replace('|', ' | ')
            story.append(Paragraph(table_text, code_style))
            
        else:
            # Regular paragraph
            if line:
                # Clean up markdown formatting
                clean_text = line.replace('**', '').replace('*', '')
                clean_text = clean_text.replace('`', '')
                # Handle links - extract just the text part
                import re
                clean_text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean_text)
                
                if clean_text:
                    story.append(Paragraph(clean_text, normal_style))
    
    # Build PDF
    try:
        doc.build(story)
        print(f"✅ PDF created: {pdf_file_path}")
        return True
    except Exception as e:
        print(f"❌ PDF creation failed: {str(e)}")
        return False

if __name__ == "__main__":
    md_file = "technical-analysis.md"
    pdf_file = "technical-analysis.pdf"
    
    if os.path.exists(md_file):
        success = create_pdf_from_markdown(md_file, pdf_file)
        if success:
            print(f"PDF report generated successfully: {pdf_file}")
        else:
            print("Failed to generate PDF report")
    else:
        print(f"Markdown file not found: {md_file}")