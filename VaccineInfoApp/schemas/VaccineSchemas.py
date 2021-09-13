from pydantic import BaseModel
from typing import List

class VaccineInfo(BaseModel):
    doseDate : str
    vaccineName : str
    lotNumber : str

class CitizenVaccineDetails(BaseModel):
    citizenId :str
    firstName : str
    lastName : str
    phoneNumber : str
    emailId : str
    vaccineInfo : List[VaccineInfo]