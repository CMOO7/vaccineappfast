################## imports ##########################################
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from .config.database import fake_users_db
# from routes.index import user
import mysql.connector
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
################# models ###########################################

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
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
def createNewCitizenAndVaccineInfo(citizenInfoRequest : CitizenVaccineDetails, token: str = Depends(oauth2_scheme)):
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
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                                database='citizenschema',
                                                user='root',
                                                password='India@123') #move this to constants file.
        cursor = connection.cursor()
        queryStatement = ("""select * from tbcitizen where citizenId = %s""")
        cursor.execute(queryStatement, (id,))
        record = cursor.fetchall()
        # global returnObj : CitizenVaccineDetails
        
        for row in record:
            print("Id = ", row[0], )
            print("FirstName = ", row[1])
            print("Last name = ", row[2])
            print("phone Number = ", row[3])
            print("email Id  = ", row[4], "\n")
            returnObj.citizenId = row[0]
            returnObj.firstName = row[1]
            returnObj.lastName = row[2]
            returnObj.phoneNumber = row[3]
            returnObj.emailId = row[4]
        
        anotherQueryStatement = ("""select * from tbvaccineinfo where citizenId = %s""")
        cursor.execute(anotherQueryStatement, (id,))
        record = cursor.fetchall()
        # global returnObj : CitizenVaccineDetails
        
        for row in record:
            print("Citizen Id = ", row[1], )
            print("doseDate = ", row[2])
            print("vaccineName = ", row[3])
            print("lotNumber  = ", row[4])

    except mysql.connector.Error as error:
        print("Failed to get record from MySQL table: {}".format(error))
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    # return returnObj

@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
################################################################

def fake_hash_password(password: str):
    return "fakehashed" + password

def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

############################################################
