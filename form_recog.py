import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

def format_polygon(polygon):
    if not polygon:
        return "N/A"
    return ", ".join("[{}, {}]".format(p.x, p.y) for p in polygon)


def format_bounding_region(bounding_region):
    if not bounding_region:
        return "N/A"
    return ", ".join("Page #{}: {}".format(
                    region.page_number, format_polygon(region.polygon)
                    )for region in bounding_region
                    )

def analyze_document(docURL:str=False, docPath:str=False, prebuilt_model:str="prebuilt-document"):

    doc_analysis_client = DocumentAnalysisClient(endpoint="https://formrecognizerinvoiceparser.cognitiveservices.azure.com/",
                                                credential=AzureKeyCredential(os.getenv("key")))
    # IF DOCS IN URL 
    # poller = doc_analysis_client.begin_analyze_document_from_url(
    #     prebuilt_model, docURL
    # )

    # LOCAL PDF
    poller = doc_analysis_client.begin_analyze_document(
        prebuilt_model, docPath
    )
    result = poller.result()
    return result