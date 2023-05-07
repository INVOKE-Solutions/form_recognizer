# Description
* Project name: Invoice Parser using built-in model from Azure Form Recofgnizer
* Objective: To automate the filling process of Finance Department in terms of parsing the information from documents (invoice) 
* Document format: PDF
* Service provider: Azure Form Recognizer

# Pre-requisite 
1. Install all the requirement from `requirements.txt` by `pip install -r requirements.txt`
2. Prepare your own `.env` file that store the `endpoint` and `key` you got from Azure Form Recognition into the `form_recognizer` directory. 
3. To execute the parser, `cd` into `main_project` and run the following command on CLI:
```
$ python3 main.py
```
4. Output should return a `Dict[List]` that contains the contents of the document.

# Unit-testing
1. To run unit test, make sure you are on `form_recognizer` dir. 
2. Run the following command on CLI;
```
$ python -m pytest unit_test/test_fr.py
```
4. Testing should be succeed.

# Development

## Next sprint
* Building CLI 

## Source 
* [concept-model-overview](https://learn.microsoft.com/en-us/azure/applied-ai-services/form-recognizer/concept-model-overview?view=form-recog-3.0.0)
* [/use-sdk-rest-api](https://learn.microsoft.com/en-us/azure/applied-ai-services/form-recognizer/how-to-guides/use-sdk-rest-api?view=form-recog-3.0.0&pivots=programming-language-python&tabs=linux)
* [concept-invoice](https://learn.microsoft.com/en-us/azure/applied-ai-services/form-recognizer/concept-invoice?view=form-recog-3.0.0)
* [azure.ai.formrecognizer.documentanalysisclient](https://learn.microsoft.com/en-us/python/api/azure-ai-formrecognizer/azure.ai.formrecognizer.documentanalysisclient?view=azure-python)
