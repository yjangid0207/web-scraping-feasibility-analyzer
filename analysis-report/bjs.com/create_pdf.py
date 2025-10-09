#!/usr/bin/env python3
"""
Convert the technical analysis markdown to PDF format with proper styling.
"""

import os
from pathlib import Path

def create_pdf():
    """Create PDF from the technical analysis markdown file."""
    
    current_dir = Path(__file__).parent
    md_file = current_dir / "technical-analysis.md"
    pdf_file = current_dir / "technical-analysis.pdf"
    
    # Check if we have pandoc available
    pandoc_cmd = f'''pandoc "{md_file}" -o "{pdf_file}" \
        --from markdown \
        --to pdf \
        --pdf-engine=wkhtmltopdf \
        --margin-top=1in \
        --margin-bottom=1in \
        --margin-left=1in \
        --margin-right=1in \
        --page-size=Letter \
        --encoding=UTF-8 \
        --disable-smart \
        --standalone'''
    
    print(f"Converting {md_file} to PDF...")
    
    try:
        result = os.system(pandoc_cmd)
        if result == 0:
            print(f"✅ Successfully created: {pdf_file}")
        else:
            print("❌ PDF conversion failed with pandoc. Trying alternative approach...")
            
            # Fallback: try with weasyprint if available
            try:
                import weasyprint
                
                # Convert markdown to HTML first
                html_content = f'''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>BJ's Wholesale Club - Web Scraping Feasibility Analysis</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
                        h2 {{ color: #34495e; margin-top: 30px; }}
                        h3 {{ color: #7f8c8d; }}
                        .code {{ background: #f4f4f4; padding: 10px; font-family: monospace; }}
                        table {{ border-collapse: collapse; width: 100%; }}
                        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                        th {{ background-color: #f2f2f2; }}
                    </style>
                </head>
                <body>
                '''
                
                with open(md_file, 'r', encoding='utf-8') as f:
                    md_content = f.read()
                
                # Simple markdown to HTML conversion
                import re
                html_content += md_content.replace('\n', '<br>')
                html_content += '</body></html>'
                
                # Convert HTML to PDF
                weasyprint.HTML(string=html_content).write_pdf(pdf_file)
                print(f"✅ Successfully created PDF using WeasyPrint: {pdf_file}")
                
            except ImportError:
                print("❌ Neither pandoc nor weasyprint available. Cannot create PDF.")
                print("To install dependencies:")
                print("  - For pandoc: brew install pandoc wkhtmltopdf (macOS)")
                print("  - For weasyprint: pip install weasyprint")
                
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")

if __name__ == "__main__":
    create_pdf()