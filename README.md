# Description
* Project name: Invoice Parser using built-in model from Azure Form Recofgnizer
* Objective: To automate the filling process of Finance Department in terms of parsing the information from documents (invoice) 
* Document format: PDF

# Pre-requisite 
1. Install all the requirement from `requirements.txt` by `pip install -r requirements.txt`
2. Create your own `.env` file and store the `endpoint` and `key` you got from Azure Form Recognition into the project directory. 
3. `cd` into `main_project` and run the following command on CLI:
```
$ python3 main.py
```

# Unit-testing
1. To run unit test, make sure you are on `form_recognizer` dir. 
2. Run the following command on CLI;
```
$ python -m pytest unit_test/test_fr.py
```
