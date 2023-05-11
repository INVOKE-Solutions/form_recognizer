__appname__ = "iParser"
__version__ = "0.1.0"

(
    SUCCESS, 
    INFERENCE_ERROR, 
    DOCUMENT_ERROR, 
) = range(3)

ERRORS ={
    INFERENCE_ERROR: "Model failed to infer the document.", 
    DOCUMENT_ERROR: "Document is not invoice"
}