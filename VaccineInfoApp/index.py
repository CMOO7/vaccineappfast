################## imports ##########################################
from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
import mysql.connector
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .config.database import fake_users_db
from .schemas.VaccineSchemas import CitizenVaccineDetails,VaccineInfo
from .models.userModels import User, UserInDB
from .db.dbConnection import connection

#################### objects ########################################
app =  FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

################### routing methods ###################################
@app.post('/createTbCitizenEntry')
def createNewCitizenAndVaccineInfo(citizenInfoRequest : CitizenVaccineDetails, token: str = Depends(oauth2_scheme)):
    try:
        cursor = connection.cursor()
        first_insert_query = """INSERT INTO `tbcitizen` (`citizenId`, `firstName`, `lastName`, `phoneNumber`, `emailId`) VALUES (%s, %s, %s, %s,%s);"""
        record = (citizenInfoRequest.citizenId, citizenInfoRequest.firstName, citizenInfoRequest.lastName, citizenInfoRequest.phoneNumber, citizenInfoRequest.emailId)
        cursor.execute(first_insert_query, record)
        connection.commit()
        print("Record inserted successfully into tbcitizen table")
        for vaccineInfo in citizenInfoRequest.vaccineInfo:
            second_insert_query = """INSERT INTO `tbvaccineinfo` (`citizenId`, `doseDate`,`vaccineName`,`lotNumber`) 
            VALUES (%s, %s, %s, %s);"""
            anotherRecord = (citizenInfoRequest.citizenId, vaccineInfo.doseDate, vaccineInfo.vaccineName, vaccineInfo.lotNumber)
            cursor.execute(second_insert_query, anotherRecord)
        connection.commit()
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

def processTbCitizenRecords(row):   
    newObjToBeReturned = CitizenVaccineDetails
    newObjToBeReturned.citizenId = row[0]
    newObjToBeReturned.firstName = row[1]
    newObjToBeReturned.lastName = row[2]
    newObjToBeReturned.phoneNumber = row[3]
    newObjToBeReturned.emailId = row[4]
    return newObjToBeReturned

def processTbVaccineInfoRecords(row):
    vaccineInfoObj = VaccineInfo
    vaccineInfoObj.doseDate = row[2]
    vaccineInfoObj.vaccineName = row[3]
    vaccineInfoObj.lotNumber = row[4]
    return vaccineInfoObj

@app.get("/fetchVaccineInfoByCitizenId/{id}")
def retrieveDbRecordsById(id : int):
    """
    input : iD (citizen Id)
    output : return all the details of citizen including vaccine details taken.
    fetches data from tables : TBCITIZEN, TBVACCINEINFO.
    """
    try:
        cursor = connection.cursor()
        queryStatement = ("""select * from tbcitizen where citizenId = %s""")
        cursor.execute(queryStatement, (id,))
        record = cursor.fetchall()
        for row in record:
            returnObj = processTbCitizenRecords(row)
        anotherQueryStatement = ("""select * from tbvaccineinfo where citizenId = %s""")
        cursor.execute(anotherQueryStatement, (id,))
        record = cursor.fetchall()
        lst = []
        for row in record:
            retVaccineInfo = processTbVaccineInfoRecords(row)
            lst.append(retVaccineInfo)
        returnObj.vaccineInfo = lst

    except mysql.connector.Error as error:
        print("Failed to get record from MySQL table: {}".format(error))
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
   
    return returnObj


###############################AUTHENTICA########################################

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

#####################################################################################################
