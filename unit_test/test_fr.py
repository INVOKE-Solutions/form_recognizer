from main_project.utils import configure
from main_project.form_recog import analyze_document, \
                                    ParseResult

def analyze_doc():
    url_pdf = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/sample-invoice.pdf"
    configure()
    print("Recognition started...")
    document_result = analyze_document(
        doc_is_url=True, 
        docURL=url_pdf, 
        prebuilt_model="prebuilt-invoice", 
        )
    return document_result

parse_result = ParseResult(analyze_doc())
def test_basic_info():
    
    basic_information = parse_result.display_basic_info()
    
    assert len(basic_information["Attribute"]) == \
                len(basic_information["Value"]) == \
                    len(basic_information["Conf"]), "Len list is not same"

def test_desc_info():
    document_result = analyze_doc()
    desc_information = parse_result.display_item_description()
    
    assert len(desc_information["Attribute"]) == \
                len(desc_information["Value"]) == \
                    len(desc_information["Conf"]), "Len list is not same"

    
