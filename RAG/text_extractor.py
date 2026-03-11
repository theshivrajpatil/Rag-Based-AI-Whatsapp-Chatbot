import os
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path):

    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def extract_all_pdfs(input_folder, output_folder):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file in os.listdir(input_folder):

        if file.endswith(".pdf"):

            pdf_path = os.path.join(input_folder, file)

            text = extract_text_from_pdf(pdf_path)

            output_file = file.replace(".pdf", ".txt")
            output_path = os.path.join(output_folder, output_file)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"Extracted text from {file}")