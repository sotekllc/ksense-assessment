import json
import os
import requests
from requests.adapters import HTTPAdapter
from typing import List, Tuple
from urllib3.util.retry import Retry

from dotenv import load_dotenv

load_dotenv()  # reads variables from a .env file and sets them in os.environ

# Implement a session with builtin retries for server errors.
# Default to 5 retries with a backoff for server errors.
def create_session_with_retries(
    retries: int = 10,
    backoff_factor: float = 0.5,
    status_forcelist: tuple[int, ...] = (429, 500, 502, 503, 504),
) -> requests.Session:
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods={"GET"},
        raise_on_status=False,
    )

    adapter = HTTPAdapter(max_retries=retry)

    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session

# Fetch all pages of patients' data.
def fetch_all_patients(): 
    base_url: str = os.environ.get('API_BASE_URL')
    path: str = os.environ.get('API_PATIENT_PATH')

    page_num: int = 1
    total_pages: int = 10   # default value, to be updated after first response
    limit: int = 10

    headers = {
        "Content-Type": "application/json",
        "x-api-key": os.environ.get('X_API_KEY')
    }

    patients: List = []

    try:
        session = create_session_with_retries()

        while page_num <= total_pages:
            response: requests.Response = session.get(
                f"{base_url}/{path}?page={page_num}&limit={limit}",
                headers=headers
            )

            # Expicitly throw exception for error statuses
            response.raise_for_status()

            payload = response.json()

            # print(payload)

            patients.extend(payload["data"])

            pagination = payload["pagination"]
            total_pages = pagination['totalPages']

            page_num += 1

        return patients
    
    except requests.HTTPError as e:
        print(f"HTTPError fetching patients: {e}")


def calculate_patient_risk_scores() -> Tuple:
    pass
    # return (scores, patients_missing_data)


def main() -> None:
    # Fetch all patients
    all_patients = fetch_all_patients()

    # DEBUG
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(all_patients, f)

    # Find all patients with a fever

    # Find all patients missing "required" data

    # Calculate risk scores for each patient (if possible)
    #   Also determine which patients are missing required data

    # Map results to output requirements:
    #   high_risk_patients, fever_patients, data_quality_issues
    pass


if __name__ == "__main__":
    main()
