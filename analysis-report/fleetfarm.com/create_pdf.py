#!/usr/bin/env python3
"""
PDF creation script for Fleet Farm web scraping analysis report.
"""

import os
from pathlib import Path

def create_pdf_from_html():
    """Convert HTML to PDF using available methods."""
    html_file = "technical-analysis.html"
    pdf_file = "technical-analysis.pdf"
    
    if not os.path.exists(html_file):
        print(f"❌ HTML file not found: {html_file}")
        return False
    
    # Try weasyprint first (best quality)
    try:
        import weasyprint
        weasyprint.HTML(filename=html_file).write_pdf(pdf_file)
        print(f"✅ PDF created using weasyprint: {pdf_file}")
        return True
    except ImportError:
        pass
    except Exception as e:
        print(f"⚠️ weasyprint failed: {e}")
    
    # Try pdfkit (requires wkhtmltopdf)
    try:
        import pdfkit
        pdfkit.from_file(html_file, pdf_file)
        print(f"✅ PDF created using pdfkit: {pdf_file}")
        return True
    except ImportError:
        pass
    except Exception as e:
        print(f"⚠️ pdfkit failed: {e}")
    
    # Try pypandoc as fallback
    try:
        import pypandoc
        # Read the HTML content
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Convert to PDF
        pypandoc.convert_text(html_content, 'pdf', format='html', 
                            outputfile=pdf_file, 
                            extra_args=['--pdf-engine=pdflatex'])
        print(f"✅ PDF created using pypandoc: {pdf_file}")
        return True
    except ImportError:
        pass
    except Exception as e:
        print(f"⚠️ pypandoc failed: {e}")
    
    # If all else fails, create a simple text-based PDF
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.units import inch
        
        # Read markdown content as fallback
        md_file = "technical-analysis.md"
        if os.path.exists(md_file):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            doc = SimpleDocTemplate(pdf_file, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Split content into lines and create paragraphs
            for line in content.split('\n'):
                if line.strip():
                    if line.startswith('#'):
                        # Headers
                        level = len(line) - len(line.lstrip('#'))
                        text = line.lstrip('# ')
                        if level == 1:
                            story.append(Paragraph(text, styles['Title']))
                        elif level == 2:
                            story.append(Paragraph(text, styles['Heading1']))
                        else:
                            story.append(Paragraph(text, styles['Heading2']))
                    else:
                        # Regular text
                        clean_text = line.replace('**', '').replace('*', '').replace('`', '')
                        story.append(Paragraph(clean_text, styles['Normal']))
                else:
                    story.append(Spacer(1, 0.1*inch))
            
            doc.build(story)
            print(f"✅ PDF created using reportlab: {pdf_file}")
            return True
            
    except ImportError:
        pass
    except Exception as e:
        print(f"⚠️ reportlab failed: {e}")
    
    print("❌ All PDF conversion methods failed. Please install weasyprint, pdfkit, pypandoc, or reportlab.")
    print("   pip install weasyprint")
    print("   pip install pdfkit")  
    print("   pip install pypandoc")
    print("   pip install reportlab")
    return False

if __name__ == "__main__":
    create_pdf_from_html()