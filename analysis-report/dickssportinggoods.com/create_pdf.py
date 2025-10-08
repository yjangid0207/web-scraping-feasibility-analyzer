#!/usr/bin/env python3
"""
Create PDF version of the technical analysis using available libraries.
"""

import os
import sys
from pathlib import Path

# Try weasyprint first, then reportlab as fallback
try:
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
    USE_WEASYPRINT = True
except ImportError:
    USE_WEASYPRINT = False

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    USE_REPORTLAB = True
except ImportError:
    USE_REPORTLAB = False

def create_pdf_from_html(html_file: str, pdf_file: str) -> None:
    """Create PDF from HTML file using WeasyPrint."""
    
    # Custom CSS for better PDF formatting
    css_content = """
        @page {
            size: A4;
            margin: 1in;
        }
        body {
            font-family: 'DejaVu Sans', sans-serif;
            font-size: 11pt;
            line-height: 1.4;
        }
        .header {
            background: linear-gradient(135deg, #2c5f2d, #97bf47);
            color: white;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
        }
        .difficulty-hard {
            background: #dc3545;
            color: white;
            padding: 8px 16px;
            border-radius: 15px;
            display: inline-block;
            font-weight: bold;
        }
        h1, h2, h3 { 
            color: #2c5f2d; 
            page-break-after: avoid;
        }
        .metric-box, .warning-box, .success-box, .danger-box {
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
            page-break-inside: avoid;
        }
        .warning-box { border-left: 4px solid #f39c12; background: #fff8e1; }
        .success-box { border-left: 4px solid #28a745; background: #e8f5e9; }
        .danger-box { border-left: 4px solid #dc3545; background: #ffeaea; }
        table { 
            width: 100%; 
            border-collapse: collapse; 
            margin: 10px 0;
            font-size: 10pt;
        }
        th, td { 
            border: 1px solid #ddd; 
            padding: 8px; 
            text-align: left; 
        }
        th { background-color: #f2f2f2; font-weight: bold; }
        .code-block {
            background: #f5f5f5;
            border: 1px solid #ddd;
            padding: 10px;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            margin: 10px 0;
        }
        .toc {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }
        .toc ul { list-style-type: none; padding-left: 15px; }
        .highlight { background-color: #fff3cd; padding: 2px 4px; border-radius: 3px; }
    """
    
    font_config = FontConfiguration()
    
    html_doc = HTML(filename=html_file)
    css_doc = CSS(string=css_content, font_config=font_config)
    
    html_doc.write_pdf(pdf_file, stylesheets=[css_doc], font_config=font_config)

def create_pdf_from_markdown(md_file: str, pdf_file: str) -> None:
    """Create PDF from markdown using ReportLab as fallback."""
    
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    doc = SimpleDocTemplate(pdf_file, pagesize=A4, topMargin=1*inch)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=colors.HexColor('#2c5f2d'),
        spaceAfter=30
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#2c5f2d'),
        spaceBefore=20,
        spaceAfter=10
    )
    
    story = []
    lines = md_content.split('\n')
    
    story.append(Paragraph("DICK'S Sporting Goods - Web Scraping Feasibility Analysis", title_style))
    story.append(Spacer(1, 20))
    
    for line in lines[:100]:  # Limit to first 100 lines for basic PDF
        line = line.strip()
        
        if not line:
            story.append(Spacer(1, 6))
            continue
        
        if line.startswith('# '):
            story.append(Paragraph(line[2:], heading_style))
        elif line.startswith('## '):
            story.append(Paragraph(line[3:], styles['Heading2']))
        elif line.startswith('### '):
            story.append(Paragraph(line[4:], styles['Heading3']))
        elif line.startswith('- ') or line.startswith('* '):
            story.append(Paragraph(line[2:], styles['Bullet']))
        else:
            # Clean up markdown formatting
            import re
            clean_line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
            clean_line = re.sub(r'`(.*?)`', r'<i>\1</i>', clean_line)
            clean_line = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean_line)
            
            if clean_line and not clean_line.startswith('---'):
                story.append(Paragraph(clean_line, styles['Normal']))
    
    doc.build(story)

def main():
    """Main function to create PDF from available files."""
    
    base_dir = Path(__file__).parent
    html_file = base_dir / "technical-analysis.html"
    md_file = base_dir / "technical-analysis.md"
    pdf_file = base_dir / "technical-analysis.pdf"
    
    print("Creating PDF version of technical analysis...")
    
    try:
        if USE_WEASYPRINT and html_file.exists():
            print("Using WeasyPrint with HTML source...")
            create_pdf_from_html(str(html_file), str(pdf_file))
            print("✅ PDF created successfully using WeasyPrint")
            
        elif USE_REPORTLAB and md_file.exists():
            print("Using ReportLab with Markdown source...")
            create_pdf_from_markdown(str(md_file), str(pdf_file))
            print("✅ PDF created successfully using ReportLab")
            
        else:
            print("❌ No suitable PDF creation library available.")
            print("   Install weasyprint or reportlab: pip install weasyprint reportlab")
            return False
            
    except Exception as e:
        print(f"❌ PDF creation failed: {str(e)}")
        
        # Try alternative approach
        if USE_REPORTLAB and md_file.exists():
            print("Attempting fallback with ReportLab...")
            try:
                create_pdf_from_markdown(str(md_file), str(pdf_file))
                print("✅ PDF created successfully using fallback method")
            except Exception as e2:
                print(f"❌ Fallback also failed: {str(e2)}")
                return False
        else:
            return False
    
    return True

if __name__ == "__main__":
    main()