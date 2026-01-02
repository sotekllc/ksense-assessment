import json
import os
import requests
from requests.adapters import HTTPAdapter
from typing import Dict, List
from urllib3.util.retry import Retry

from dotenv import load_dotenv

from .models import HIGH_RISK_THRESHOLD
from .models import Patient

load_dotenv()  # reads variables from a .env file and sets them in os.environ

# Implement a session with builtin retries for server errors.
# Default to 10 retries with a backoff for server errors and rate-limit errors.
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
def fetch_all_patients() -> List[Patient]: 
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
            patients.extend(payload["data"])

            pagination = payload["pagination"]
            total_pages = pagination['totalPages']

            page_num += 1

        return [Patient(data) for data in patients]
    
    except requests.HTTPError as e:
        print(f"HTTPError fetching patients: {e}")

# Application entrypoint.
def main() -> None:
    # Fetch all patients
    all_patients: List[Patient] = fetch_all_patients()

    # Find all patients with a fever
    fever_patients: List[Patient] = [p for p in all_patients if p.has_fever()]

    # Find all patients missing "required" data
    data_quality_issue_patients: List[Patient] = [p for p in all_patients if p.missing_required_fields()]

    # Map results to output requirements:
    #   high_risk_patients, fever_patients, data_quality_issues
    high_risk_patient_ids: List[str] = [p.patient_id for p in all_patients if p.risk_score >= HIGH_RISK_THRESHOLD]
    fever_patient_ids: List[str] = [p.patient_id for p in fever_patients]
    data_quality_issue_ids: List[str] = [p.patient_id for p in data_quality_issue_patients]

    output_data: Dict = {
        "high_risk_patients": high_risk_patient_ids,
        "fever_patients": fever_patient_ids,
        "data_quality_issues": data_quality_issue_ids
    }
    print(output_data)

if __name__ == "__main__":
    main()
