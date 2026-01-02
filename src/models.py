from typing import List

# {
#     "patient_id": "DEMO001",
#     "name": "TestPatient, John",
#     "age": 45,
#     "gender": "M",
#     "blood_pressure": "120/80",
#     "temperature": 98.6,
#     "visit_date": "2024-01-15",
#     "diagnosis": "Sample_Hypertension",
#     "medications": "DemoMed_A 10mg, TestDrug_B 500mg"
# },

class Patient:
    patient_id: str
    name: str
    age: int
    blood_pressure: str
    temperature: float
