from main_project.form_recog import analyze_document, \
                        key_val_extraction, \
                        display_basic_info, \
                        display_item_description
from main_project.utils import configure
from pathlib import Path


local_pdf_path = Path('/home/ammar/INVOKE/invoice_parser/venvParser/project/pdf_test')
url_pdf = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/sample-invoice.pdf"
def recognize_this(
        doc_is_url:bool,
        doc_url=False,
        doc_path=False,
    ):
    configure()
    print("Recognition started...")
    document_result = analyze_document(
        doc_is_url=doc_is_url, 
        docURL=doc_url, 
        prebuilt_model="prebuilt-invoice", 
        docPath=doc_path,
        )
    print("Recognition completed.")
    print("Parsing and return json format...")

    # TEST
    # parsed_Dict = key_val_extraction(document_result)
    # print(parsed_Dict)

    basic_information = display_basic_info(document_result)
    desc_information = display_item_description(document_result)
    print("BASIC INFORMATION: \n", basic_information)
    print("DESCRIPTION: \n", desc_information)

    return (basic_information, desc_information)
    # return basic_information


# if __name__ == "__main__":
#     main() 