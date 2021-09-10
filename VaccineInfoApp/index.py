################## imports ##########################################
from fastapi import FastAPI
from pydantic import BaseModel
# from .config.database import connection
# from routes.index import user
import mysql.connector

################# models ###########################################

class VaccineInfo(BaseModel):
    doseDate : str
    vaccineName : str
    lotNumber : str
    # def __init__(self, doseDate:str , vaccineName:str, lotNumber:str):
    #     self.doseDate = doseDate
    #     self.vaccineName = vaccineName
    #     self.lotNumber = lotNumber

class CitizenVaccineDetails(BaseModel):
    citizenId :str
    firstName : str
    lastName : str
    phoneNumber : str
    emailId : str
    vaccineInfo1 : VaccineInfo
    vaccineInfo2 : VaccineInfo

    # def __init__(self, citizenId, firstName, lastName,phoneNumber,emailId):
    #     self.citizenId = citizenId
    #     self.firstName =  firstName
    #     self.lastName = lastName
    #     self.phoneNumber = phoneNumber
    #     self.emailId = emailId
        # self.vaccineInfo = vaccineInfo


#################### objects ########################################
app =  FastAPI()
#############################################################################################
#                                    REQUIREMENT                                            #
# create entry in tbcitizen [citizenId, firstName, lastName, PhoneNumber, emailId]          #
# create entry in tbvaccinationinfo [citizenId, VaccineName, LotNumber, doseDate]       #
# "vaccineInfo": -- array
#     [{"doseDate": 1,
#     "VaccineName": "DoseName",
#     "LotNumber": "LLL98"},
#      {"doseDate": 1,
#     "VaccineName": "DoseName",
#     "LotNumber": "LLL98"}
#    ]
# take vaccineInfo object from CitizenVaccineDetails.                                       #
# create json string of attributes in VaccineInfo                                           #
#                                                                                           #
#############################################################################################
################### routing methods ###################################
@app.post('/createTbCitizenEntry')
def createNewCitizenAndVaccineInfo(citizenInfoRequest : CitizenVaccineDetails):
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                             database='citizenschema',
                                             user='root',
                                             password='India@123') #move this to constants file.
        cursor = connection.cursor()
        first_insert_query = """INSERT INTO `tbcitizen` (`citizenId`, `firstName`, `lastName`, `phoneNumber`, `emailId`) VALUES (%s, %s, %s, %s,%s);"""
        record = (citizenInfoRequest.citizenId, citizenInfoRequest.firstName, citizenInfoRequest.lastName, citizenInfoRequest.phoneNumber, citizenInfoRequest.emailId)
        cursor.execute(first_insert_query, record)
        connection.commit()
        print("Record inserted successfully into tbcitizen table")
        firstVaccineInfo= citizenInfoRequest.vaccineInfo1
        secondVaccineInfo = citizenInfoRequest.vaccineInfo2
        second_insert_query = """INSERT INTO `tbvaccineinfo` (`citizenId`, `doseDate`,`vaccineName`,`lotNumber`) 
        VALUES (%s, %s, %s, %s);"""
        anotherRecord = (citizenInfoRequest.citizenId, firstVaccineInfo.doseDate, firstVaccineInfo.vaccineName, firstVaccineInfo.lotNumber)
        cursor.execute(second_insert_query, anotherRecord)
        
        second_insert_query = """INSERT INTO `tbvaccineinfo` (`citizenId`, `doseDate`,`vaccineName`,`lotNumber`) 
        VALUES (%s, %s, %s, %s);"""
        anotherRecord = (citizenInfoRequest.citizenId, secondVaccineInfo.doseDate, secondVaccineInfo.vaccineName, secondVaccineInfo.lotNumber)
        cursor.execute(second_insert_query, anotherRecord)
        connection.commit()
        print("Record inserted successfully into tbvaccineinfo table")
        
        
        # for vaccineInfoObj in vaccineInfoList:
        #     second_insert_query = """INSERT INTO `tbvaccineinfo` (`citizenId`, `doseDate`,`vaccineName`,`lotNumber`) 
        #     VALUES (%s, %s, %s, %s);"""
        #     anotherRecord = (citizenInfoRequest.citizenId, vaccineInfoObj.doseDate, vaccineInfoObj.vaccineNumber, vaccineInfoObj.lotNumber)
        #     cursor.execute(second_insert_query, anotherRecord)
        #     connection.commit()
        #     print("Record inserted successfully into tbvaccineinfo table")
        
        cursor.close()
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return citizenInfoRequest
 
@app.get("/fetchVaccineInfoByCitizenId/{id}")
def retrieveDbRecordsById(id : int):
    connection = mysql.connector.connect(host='127.0.0.1',
                                             database='citizenschema',
                                             user='root',
                                             password='India@123') #move this to constants file.
    cursor = connection.cursor()
    queryStatement = (
        "select A.*, B.doseDate, B.vaccineName, B.lotNumber "
        "from tbcitizen A, tbvaccineinfo B "
        "where A.citizenId = %s"
    )
    cursor.execute(queryStatement, id)
    for (cititzenId, firstName, lastName, phoneNumber,emailId,doseDate,VaccineName,lotNumber) in cursor:
        print("{}, {} was vaccinated on {} {:%d %b %Y}".format(firstName, lastName, doseDate))

    cursor.close()
    connection.close()
################################################################

############################################################
