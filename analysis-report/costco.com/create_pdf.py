#!/usr/bin/env python3
"""
Create PDF version of technical analysis for Costco web scraping feasibility.
"""

import os
from pathlib import Path

def markdown_to_pdf():
    """Convert technical analysis markdown to PDF."""
    
    md_file = Path(__file__).parent / "technical-analysis.md"
    pdf_file = Path(__file__).parent / "technical-analysis.pdf"
    
    if not md_file.exists():
        print(f"Error: {md_file} not found")
        return False
    
    try:
        # Try using pandoc first
        import subprocess
        result = subprocess.run([
            'pandoc', 
            str(md_file), 
            '-o', str(pdf_file),
            '--pdf-engine=wkhtmltopdf',
            '--margin-top=1in',
            '--margin-bottom=1in',
            '--margin-left=1in', 
            '--margin-right=1in'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ PDF created successfully: {pdf_file}")
            return True
        else:
            print(f"Pandoc failed: {result.stderr}")
            
    except FileNotFoundError:
        print("Pandoc not found, trying alternative methods...")
    
    # Try using weasyprint
    try:
        import weasyprint
        import markdown
        
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        html_content = markdown.markdown(md_content)
        
        # Add basic styling
        styled_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 1in; line-height: 1.6; }}
                h1 {{ color: #d32f2f; border-bottom: 2px solid #d32f2f; padding-bottom: 10px; }}
                h2 {{ color: #1976d2; margin-top: 30px; }}
                h3 {{ color: #388e3c; margin-top: 25px; }}
                code {{ background: #f5f5f5; padding: 2px 4px; border-radius: 3px; }}
                pre {{ background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        weasyprint.HTML(string=styled_html).write_pdf(str(pdf_file))
        print(f"✅ PDF created successfully with WeasyPrint: {pdf_file}")
        return True
        
    except ImportError:
        print("WeasyPrint not available, trying reportlab...")
    
    # Fallback: create basic text-based PDF with reportlab
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        doc = SimpleDocTemplate(str(pdf_file), pagesize=letter, 
                              topMargin=1*inch, bottomMargin=1*inch,
                              leftMargin=1*inch, rightMargin=1*inch)
        
        styles = getSampleStyleSheet()
        story = []
        
        # Add title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='#d32f2f',
            spaceAfter=30
        )
        story.append(Paragraph("Costco Web Scraping Feasibility Analysis", title_style))
        story.append(Spacer(1, 20))
        
        # Process content line by line
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                story.append(Spacer(1, 12))
                continue
                
            if line.startswith('# '):
                story.append(Paragraph(line[2:], styles['Heading1']))
            elif line.startswith('## '):
                story.append(Paragraph(line[3:], styles['Heading2']))
            elif line.startswith('### '):
                story.append(Paragraph(line[4:], styles['Heading3']))
            elif line.startswith('- ') or line.startswith('* '):
                story.append(Paragraph("• " + line[2:], styles['Normal']))
            else:
                # Clean up markdown formatting
                import re
                line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
                line = re.sub(r'`(.*?)`', r'<i>\1</i>', line)
                line = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', line)
                
                if line:
                    story.append(Paragraph(line, styles['Normal']))
        
        doc.build(story)
        print(f"✅ Basic PDF created with ReportLab: {pdf_file}")
        return True
        
    except ImportError:
        print("❌ No PDF generation library available. Install pandoc, weasyprint, or reportlab.")
        return False

if __name__ == "__main__":
    markdown_to_pdf()