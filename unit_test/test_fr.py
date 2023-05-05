from main_project.utils import configure
from main_project.form_recog import analyze_document, \
                                        display_basic_info

def test_basic_info():
    url_pdf = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/sample-invoice.pdf"
    configure()
    print("Recognition started...")
    document_result = analyze_document(
        doc_is_url=False, 
        docURL=url_pdf, 
        prebuilt_model="prebuilt-invoice", 
        )
    
    basic_information = display_basic_info(document_result)
    
    assert len(basic_information["Attribute"]) == \
                len(basic_information["Value"]) == \
                    len(basic_information["Conf"]), "Len list is not same"

    
