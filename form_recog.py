import os
import numpy as np
import pandas as pd
from typing import Dict

import azure
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

def format_polygon(polygon):
    if not polygon:
        return "N/A"
    return ", ".join("[{}, {}]".format(p.x, p.y) for p in polygon)


def format_bounding_region(bounding_region):
    """
    Return bounding box region recognize within the pdf file. 
    """
    if not bounding_region:
        return "N/A"
    return ", ".join("Page #{}: {}".format(
                    region.page_number, format_polygon(region.polygon)
                    )for region in bounding_region
                    )

def analyze_document(doc_is_url=False,
                    docURL:str=False, 
                    docPath:str=False, 
                    prebuilt_model:str="prebuilt-document"):
    
    """
    Return azure.ai.formrecognizer._models.AnalyzedDocument 

    *Args
        doc_is_url: True if document is from URL (ie Github link)
        docURL    : Document URL link if doc_is_url is True
        docPath   : Document path in local (doc_is_url either False or no args)
        prebuilt_model: Pre-built model from Form Recognizer (default is prebuild-document; 
                        alternative; invoice-document)
    """

    doc_analysis_client = DocumentAnalysisClient(
                            endpoint=os.getenv("endpoint"),
                            credential=AzureKeyCredential(os.getenv("key")))
    # DOCS IN URL 
    if doc_is_url:
        poller = doc_analysis_client.begin_analyze_document_from_url(
            prebuilt_model, docURL)
    else:
        with open(docPath, "rb") as f:
            poller = doc_analysis_client.begin_analyze_document(
                prebuilt_model, 
                document=f)

    result = poller.result()
    return result

def key_val_extraction(result:azure.ai.formrecognizer._models.AnalyzeResult)->Dict:
    """
    Return raw parsed information without classification from the document
    
    """

    information = {
                "key-content":[],
                "key-bbox":[], 
                "value-content":[], 
                "value-bbox":[]
            }
    
    for kv_pair in result.key_value_pairs:
        if kv_pair.key:
            # LOGGER
            # print(
            #     "Key '{}' found within '{}' bounding region".format(
            #             kv_pair.key.content, 
            #             format_bounding_region(kv_pair.key.bounding_regions)
            #     )
            # )
            information["key-content"].append(kv_pair.key.content)
            information["key-bbox"].append(kv_pair.key.bounding_regions)
        
        else: 
            information["key-content"].append(np.NAN)
            information["key-bbox"].append(np.NAN)


        if kv_pair.value:
            # LOGGER
            # print(
            #     "Value '{}' found within '{}' bounding region".format(
            #             kv_pair.value.content, 
            #             format_bounding_region(kv_pair.value.bounding_regions)
            #     )
            # )
            information["value-content"].append(kv_pair.value.content)
            information["value-bbox"].append(kv_pair.value.bounding_regions)
        else:
            information["value-content"].append(np.NAN)
            information["value-bbox"].append(np.NAN)

    # return pd.DataFrame(information).head(5)
    return information

def get_basic_info(invoice:azure.ai.formrecognizer._models.AnalyzedDocument, 
                    infoToget:str):
    
    """
    Return basic information from the document
    """
    
    getInfo = invoice.fields.get(infoToget)

    if getInfo:
        if infoToget == "CustomerAddress" or \
            infoToget == "ShippingAddress" or \
                infoToget == "VendorAddress" :
            # print(f"{infoToget}: {getInfo.value.city} | {infoToget} confidence: {getInfo.confidence}")
            return (str(getInfo.value.city), str(getInfo.confidence))
        else:
            # print(f"{infoToget}: {getInfo.value} | {infoToget} confidence: {getInfo.confidence}")
            return (str(getInfo.value), str(getInfo.confidence))

def display_basic_info(invoice_result:azure.ai.formrecognizer._models.AnalyzeResult):

    """
    Return dictionary that has key-value of attribute-value from the docs 

    """

    for idx, invoice_result in enumerate(invoice_result.documents):
        print(f"----- Invoice # {idx+1}")

        get_this = [
            "VendorName", 
            "VendorAddress"
            "VendorAddressRecipient", 
            "CustomerName", 
            "CustomerId", 
            "CustomerAddress", 
            "CustomerAddressRecipient", 
            "InvoiceId", 
            "InvoiceDate", 
            "InvoiceTotal", 
            "DueDate", 
            "PurchaseOrder", 
            "BillingAddress"
            "BillingAddressRecipient", 
            "ShippingAddress", 
            "ShippingAddressRecipient", 
        ]
        infoDict = {"Attribute":[], "Value":[], "Conf":[]}

        for content in get_this:
            info = get_basic_info(invoice_result, content)
            if info == None:
                    infoDict["Attribute"].append(np.NAN)
                    infoDict["Value"].append(np.NAN)
                    infoDict["Conf"].append(np.NAN)
            else:
                val = get_basic_info(invoice=invoice_result, infoToget=content)[0]
                conf = get_basic_info(invoice=invoice_result, infoToget=content)[1]
                infoDict["Attribute"].append(content)
                infoDict["Value"].append(val)
                infoDict["Conf"].append(conf)

        return infoDict
