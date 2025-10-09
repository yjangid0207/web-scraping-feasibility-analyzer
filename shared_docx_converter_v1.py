import pypandoc
import sys
import os

def md_to_docx(md_file_path, output_dir=None):
    """
    Converts a Markdown (.md) file to a Word (.docx) file using pypandoc.

    Args:
        md_file_path (str): Path to the .md file.
        output_dir (str, optional): Directory where the .docx file will be saved.
                                    Defaults to same directory as input file.

    Returns:
        str: Path to the generated .docx file.
    """
    if not os.path.exists(md_file_path):
        raise FileNotFoundError(f"Markdown file not found: {md_file_path}")

    if output_dir is None:
        output_dir = os.path.dirname(md_file_path)

    base_name = os.path.splitext(os.path.basename(md_file_path))[0]
    output_path = os.path.join(output_dir, f"{base_name}.docx")

    print(f"Converting '{md_file_path}' → '{output_path}' ...")
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    pypandoc.convert_text(
        md_content,
        'docx',
        format='md',
        outputfile=output_path,
        extra_args=['--standalone']
    )
    print("✅ Conversion complete.")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python md_to_docx.py <input_file.md> [output_dir]")
        sys.exit(1)

    md_file = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else None
    md_to_docx(md_file, out_dir)
