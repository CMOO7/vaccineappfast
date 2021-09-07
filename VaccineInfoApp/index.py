################## imports ##########################################
from fastapi import FastAPI
from pydantic import BaseModel
# from .config.database import connection
# from routes.index import user
import mysql.connector

################# models ###########################################

class VaccineInfo(BaseModel):

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

################### routing methods ###################################
@app.post('/createTbCitizenEntry')
def createNewCitizenAndVaccineInfo(citizenInfoRequest : CitizenVaccineDetails):
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                             database='citizenschema',
                                             user='root',
                                             password='India@123')
        cursor = connection.cursor()
        first_insert_query = """INSERT INTO `tbcitizen` (`citizenId`, `firstName`, `lastName`, `phoneNumber`, `emailId`) VALUES (%s, %s, %s, %s,%s);"""
        record = (citizenInfoRequest.citizenId, citizenInfoRequest.firstName, citizenInfoRequest.lastName, citizenInfoRequest.phoneNumber, citizenInfoRequest.emailId)
        cursor.execute(first_insert_query, record)
        connection.commit()
        print("Record inserted successfully into tbcitizen table")
        vaccineInfoObj = citizenInfoRequest.vaccineInfo
        vaccineInfoJson :str 
        vaccineInfoJson = 'concatenate all fields in to jsonstring'
        second_insert_query = """INSERT INTO `tbvaccineinfo` (`citizenId`, `vaccineInfoJson`) 
        VALUES (%s, %s);"""
        anotherRecord = (citizenInfoRequest.citizenId, vaccineInfoJson)
        cursor.execute(second_insert_query, anotherRecord)
        connection.commit()
        #create entry in tbcitizen [citizenId, firstName, lastName, PhoneNumber, emailId]
        #create entry in tbvaccinationinfo [citizenId, vaccineInfoJson]
            # take vaccineInfo object from CitizenVaccineDetails.
            # create json string of attributes in VaccineInfo
        print("Record inserted successfully into tbvaccineinfo table")
        cursor.close()
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return citizenInfoRequest
 
@app.get('/fetchVaccineInfoByCitizenId')
def retrieveDbRecordsById():
    pass   
################################################################

############################################################
############################################################
# app = FastAPI()
# app.include_router(user)