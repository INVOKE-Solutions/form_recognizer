from form_recog import analyze_document
from utils import configure
from pathlib import Path

test_pdf_path = Path('/home/ammar/INVOKE/invoice_parser/venvParser/project/pdf_test')
def main():
    configure()
    document_result = analyze_document(
        docPath=test_pdf_path/"test_pdf_1.pdf"
        )

    print("HEALTH TEST")
    return document_result


if __name__ == "__main__":
    main()