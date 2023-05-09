import streamlit as st

from main_project.form_recog import analyze_document, \
                        key_val_extraction, \
                        display_basic_info, \
                        display_item_description
from main_project.utils import configure

@st.cache_data(ttl=60*60)
def recognize_this( doc_is_url:bool,
                    doc_url=False,
                    doc_path=False,
                    ):
    """
    Return Tuple[Dict[str, str]] or Dict[str, int]
    Args*:
        doc_is_url=False :True if URL link, False if from path
        doc_url=False (default): Document URL string
        doc_path=False (default): Document path
    """
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

    try:
        basic_information = display_basic_info(document_result)
        desc_information = display_item_description(document_result)
        print("BASIC INFORMATION: \n", basic_information)
        print("DESCRIPTION: \n", desc_information)
        return (basic_information, desc_information)
    except Exception as e1:
        print("ERROR recognize_this():\n", e1)
        print("No information detected")        


# if __name__ == "__main__":
#     main() 