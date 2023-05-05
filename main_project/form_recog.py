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

def get_item_info(item, itemToget:str):
    itemInfo = item.value.get(itemToget)
    if itemInfo:
        #print(f"{itemToget}: {itemInfo.value} | {itemToget} confidence: {itemInfo.confidence}")
        return (str(itemInfo.value), str(itemInfo.confidence))
    
class ParseResult:
    def __init__(self, result:azure.ai.formrecognizer._models.AnalyzeResult):
        self.result = result
        self.information = {"key-content":[],"key-bbox":[], "value-content":[], "value-bbox":[]}
        self.infoDict_basic = {"Attribute":[], "Value":[], "Conf":[]}
        self.infoDict_desc = {"Attribute":[], "Value":[], "Conf":[]}   


    def key_val_extraction(self)->Dict:
        """
        Return raw parsed information without classification from the document
        """
        for kv_pair in self.result.key_value_pairs:
            if kv_pair.key:
                self.information["key-content"].append(kv_pair.key.content)
                self.information["key-bbox"].append(kv_pair.key.bounding_regions)
            else: 
                self.information["key-content"].append(np.NAN)
                self.information["key-bbox"].append(np.NAN)
            if kv_pair.value:
                self.information["value-content"].append(kv_pair.value.content)
                self.information["value-bbox"].append(kv_pair.value.bounding_regions)
            else:
                self.information["value-content"].append(np.NAN)
                self.information["value-bbox"].append(np.NAN)

        # return pd.DataFrame(information).head(5)
        return self.information
    
    def display_basic_info(self)->Dict:
        """
        Return dictionary that has key-value of attribute-value from the docs 

        """
        for idx, invoice_result in enumerate(self.result.documents):
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

            for content in get_this:
                info = get_basic_info(invoice_result, content)
                if info == None:
                    self.infoDict_basic["Attribute"].append(np.NAN)
                    self.infoDict_basic["Value"].append(np.NAN)
                    self.infoDict_basic["Conf"].append(np.NAN)
                else:
                    val = get_basic_info(invoice=invoice_result, infoToget=content)[0]
                    conf = get_basic_info(invoice=invoice_result, infoToget=content)[1]
                    self.infoDict_basic["Attribute"].append(content)
                    self.infoDict_basic["Value"].append(val)
                    self.infoDict_basic["Conf"].append(conf)
                    
        return self.infoDict_basic

    def display_item_description(self)->Dict:
    
        for idx_1, invoice in enumerate(self.result.documents):
            print(f"----- Invoice # {idx_1+1}")
            for idx_2, item in enumerate(invoice.fields.get("Items").value):
                print(f"----- Table {idx_2+1} Invoice # {idx_1+1}")
                item_description = [
                    "Description", 
                    "Quantity", 
                    "Unit", 
                    "UnitPrice", 
                    "ProductCode"
                    "Date", 
                    "Tax", 
                    "Amount", 
                    "SubTotal", 
                    "TotalTax", 
                    "PreviousUnpaidBalance", 
                    "AmountDue", 
                    "ServiceStartDate",
                    "ServiceEndDate", 
                    "ServiceAddress", 
                    "ServiceAddressRecipient", 
                    "RemittanceAddressRecipient", 
                    ]
                for description in item_description:
                    info = get_item_info(item=item, itemToget=description)
                    if info == None:
                        self.infoDict_desc["Attribute"].append(np.NAN)
                        self.infoDict_desc["Value"].append(np.NAN)
                        self.infoDict_desc["Conf"].append(np.NAN)
                        pass
                    else:
                        val = get_item_info(item=item, itemToget=description)[0]
                        conf = get_item_info(item=item, itemToget=description)[1]
                        self.infoDict_desc["Attribute"].append(description)
                        self.infoDict_desc["Value"].append(val)
                        self.infoDict_desc["Conf"].append(conf)

        return self.infoDict_desc