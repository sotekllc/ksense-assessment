from typing import Dict, Optional

"""
Domain model class representing a Patient.
"""
class Patient:
    patient_id: str
    name: str
    age: int
    blood_pressure: str
    temperature: float

    risk_score: Optional[int] = None

    def __init__(self, data: Dict) -> None:
        self.patient_id = data.get('patient_id', None)
        self.name = data.get('name', None)
        self.age = self.parse_int(data.get('age', None))
        self.blood_pressure = self.parse_blood_pressure(data.get('blood_pressure', None))
        self.temperature = self.parse_float(data.get('temperature', None))

        self.calculate_risk_score()

    def missing_required_fields(self) -> bool:
        return self.patient_id is None or self.age is None or self.blood_pressure is None or self.temperature is None

    def has_fever(self) -> bool:
        return self.temperature is not None and self.temperature >= 99.6
    
    # Parse the value for a valid integer value.
    #   Return None otherwise.
    def parse_int(self, value) -> int:
        try:
            val: int = int(value)
            return val
        except (TypeError, ValueError):
            return None
    
    # Parse the value for a valid float value.
    #   Return None otherwise.
    def parse_float(self, value) -> float:
        try:
            val: float = float(value)
            return val
        except (TypeError, ValueError):
            return None
    
    # Parse the value for possibly being a valid blood_pressure reading, 
    #   as determined by there being two integers separated by a
    #   forward slash. Return None in all other cases.
    # This way, we either return a valid blood_pressure string or None
    #   and all missing and malformed values will be represented by a
    #   None value.
    def parse_blood_pressure(self, value) -> str:
        try:
            # Check for two numbers separated by a forward slash
            if value is not None and isinstance(value, str) and "/" in value:
                bp_parts = value.split("/")

                if len(bp_parts) == 2:
                    systolic: int = int(bp_parts[0])
                    diastolic: int = int(bp_parts[1])

                    return value
        except (TypeError, ValueError):
            return None

    def calculate_blood_pressure_score(self) -> int:
        bp_score: int = 0   # default to 0, missing or invalid values get a 0 score
        if self.blood_pressure is not None:
            bp_parts = self.blood_pressure.split("/")

            try: 
                systolic: int = int(bp_parts[0])
                diastolic: int = int(bp_parts[1])

                if systolic >= 140 or diastolic >= 90:
                    bp_score = 3
                elif (systolic >= 130 and systolic <= 139) or (diastolic >= 80 and diastolic <= 89):
                    bp_score = 2
                elif systolic >= 120 and systolic <= 129 and diastolic < 80:
                    bp_score = 1
                elif systolic < 120 and diastolic < 80:
                    bp_score = 0

            except (ValueError, TypeError):
                bp_score = 0

        return bp_score
    
    def calculate_temperature_score(self) -> int:
        temp_score: int = 0 # default to 0, missing or invalid values get a 0 score

        if self.temperature is not None:
            if self.temperature <= 99.5:
                temp_score = 0
            elif self.temperature >= 99.6 and self.temperature <= 100.9:
                temp_score = 1
            elif self.temperature >= 101.0:
                temp_score = 2
        
        return temp_score
    
    def calculate_age_score(self) -> int:
        age_score: int = 0  # default to 0, missing or invalid values get a 0 score

        if self.age is not None:
            if self.age < 40:
                age_score = 0
            elif self.age >= 40 and self.age <= 65:
                age_score = 1
            elif self.age > 65:
                age_score = 2
        
        return age_score

    def calculate_risk_score(self) -> int:
        # Calculate blood_pressure risk score
        bp_score: int = self.calculate_blood_pressure_score()

        # Calculate temperature risk score
        temp_score: int = self.calculate_temperature_score()

        # Calculate age risk score
        age_score: int = self.calculate_age_score()

        self.risk_score = bp_score + temp_score + age_score
        return self.risk_score

    def to_json(self) -> Dict:
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "age": self.age,
            "blood_pressure": self.blood_pressure,
            "temperature": self.temperature,
            "risk_score": self.risk_score
        }
