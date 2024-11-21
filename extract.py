import fitz
def pdf_to_text(pdf_path, txt_path):
	pdf_document = fitz.open(pdf_path)
	with open(txt_path, "w", encoding="utf-8") as text_file:
		for page_number in range(len(pdf_document)):
			page = pdf_document.load_page(page_number)
			text = page.get_text()
			text_file.write(text)
		pdf_document.close()
# Example usage
pdf_path = "amusing.pdf"
txt_path = "extracted_text.txt"
pdf_to_text(pdf_path, txt_path)