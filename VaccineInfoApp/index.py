################## imports ##########################################
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import MetaData

# from routes.index import user

################# models ###########################################

class VaccineInfo(BaseModel):

    citizenId : str
    doseCount : int
    vaccineSupplier : str
    vaccineLotNumber : str
    # nextAppointmentStartDate : datetime.date
    

class CitizenVaccineDetails(BaseModel):

    citizenId :str
    firstName : str
    lastName : str
    phoneNumber : str
    emailId : str
    vaccineInfo : VaccineInfo


#################### objects ########################################
app =  FastAPI()
metadata = MetaData()
################### routing methods ###################################
@app.post('/createTbCitizenEntry')
def createNewCitizenAndVaccineInfo():
    
    #create entry in tbcitizen [citizenId, firstName, lastName, PhoneNumber, emailId]
    #create entry in tbvaccinationinfo [citizenId, vaccineInfoJson]
        # take vaccineInfo object from CitizenVaccineDetails.
        # create json string of attributes in VaccineInfo
    return 'new data index'

@app.get('/fetchVaccineInfoByCitizenId')
def retrieveDbRecordsById():
    pass   
################################################################

############################################################
############################################################
# app = FastAPI()
# app.include_router(user)