# Ksense Assessment

A demo project for Ksense for an API integration project. Works with a simple API to pull patient data, perform calculations, and output results that are to be submitted in a specific format. 


## Dependencies

- [python poetry](https://python-poetry.org/)
- python v3.10+


## Run project

First, setup the `.env` file in the root of the project directory. Follow the `.env.example` file for guidance. Then, after installing the dependencies, run this from the project root directory:

```
poetry install
poetry run python -m src.main
```


## Description

This project is a demo project for a Ksense coding assessment. It demonstrates working with their API for basic patient data.

Follows the 12 factor app approach and uses a `.env` file for secrets and parameters around the API, which is hosted by Ksense. Values such as the API key, base url and api path are considered secrets and written into the `.env` file. See the `.env.example` file for an example.

Built into the project code is handling server errors and rate limit errors (429 and 5xx codes) using retries with the requests library. 

There are also possible issues with the data such as required fields being missing or having invalid values. This is handled by first modeling patient data in a Domain model class "Patient" and then mapping all invalid values to `None` and all valid values to their respective int, float or string value. This allows for both easily checking for required values being missing or invalid and calculating risk scores since we'll know that any `None` value in a Patient field represents a missing or invalid value even if that invalid value is itself not a NoneType. We offload much of the scoring and calculations work to the domain model since that's the purpose of domain models, handling business logic related to data.

This project finalizes its pipeline by using stdout to print out the formatted data expected for the submission, which looks like this:

```
output_data: Dict = {
    "high_risk_patients": high_risk_patient_ids,
    "fever_patients": fever_patient_ids,
    "data_quality_issues": data_quality_issue_ids
}
print(output_data)
```
