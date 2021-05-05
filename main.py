from fastapi import FastAPI, HTTPException, File, UploadFile, Request, Header
import databases
import sqlalchemy
import schemasClass
from scheme import Schemas
import token2
import shutil

DATABASE_URL = 'postgres://postgres:MasterBase!@localhost:5432/postgres?sslmode=prefer'

metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(DATABASE_URL)

app = FastAPI()
database = databases.Database(DATABASE_URL)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/')
async def index():
    return {'Connect': 'OK'}


@app.post('/adduser')
async def index(user: schemasClass.User):
    hash_password = token2.get_password_hash(user.password)

    query = Schemas.userTable.insert().values(email=user.email, password=str(hash_password))
    last_record_id = await database.execute(query)
    access_token = token2.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, 'id': last_record_id, "email": user.email}


@app.post('/getuser')
async def index(user: schemasClass.User):
    query = "SELECT password FROM users where email= :email"

    result = await database.execute(query, values={"email": user.email})

    if not result:
        raise HTTPException(status_code=404, detail="Item not found")

    hash_from_base = ""

    for item in range(2, len(result) - 1):
        hash_from_base += result[item]

    end_hash = bytes(hash_from_base, 'utf8')

    try:
        is_checked = token2.get_password_check(user.password, end_hash)
        if is_checked is False:
            raise HTTPException(status_code=404, detail="Item not found")
    except:
        raise HTTPException(status_code=404, detail="Item not found")

    query3 = "SELECT id FROM users where email= :email"
    id = await database.execute(query3, values={"email": user.email})
    access_token = token2.create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "id": id, "email": user.email}


@app.post("/getjson/1")
async def index(request: schemasClass.TechnologyTreatments, id_user: int = Header(None), x_token: str = Header(None)):
    access = await validating(token2.decode_token(x_token)["sub"])

    if access is False:
        raise HTTPException(status_code=404, detail="Item not found")

    query2 = "SELECT id FROM zabiegi_agrotechniczne ORDER BY id DESC"
    id = await database.execute(query2)

    if id is None:
        query = Schemas.zabiegi_agrotechniczne.insert().values(id=1, userid=id_user, date=request.date[0],
                                                               action=request.action[0], data1=request.data1[0],
                                                               data2=request.data2[0])
        await database.execute(query)
        for i in range(1, len(request.date)):
            await database.execute(queryFunction2(i, id, request, id_user))
            id = await database.execute(query2)

    elif id is not None:
        for i in range(0, len(request.date)):
            await database.execute(queryFunction2(i, id, request, id_user))
            id = await database.execute(query2)

    return id


@app.post("/getjson/2")
async def index(request: schemasClass.CurrentCondition, id_user: int = Header(None), x_token: str = Header(None)):
    access = await validating(token2.decode_token(x_token)["sub"])

    if access is False:
        raise HTTPException(status_code=404, detail="Item not found")

    query2 = "SELECT id FROM warunki_biezace ORDER BY 1 DESC"
    id = await database.execute(query2)
    if id is None:
        query = Schemas.warunki_biezace.insert().values(id=1, userid=id_user, plant=request.plant,
                                                        term=request.term, condition=request.condition)
    else:
        query = Schemas.warunki_biezace.insert().values(id=(id + 1), userid=id_user, plant=request.plant,
                                                        term=request.term, condition=request.condition)

    await database.execute(query)
    return id


@app.post("/getjson/3")
async def index(request: schemasClass.ActionDiary, id_user: int = Header(None), x_token: str = Header(None)):
    access = await validating(token2.decode_token(x_token)["sub"])

    if access is False:
        raise HTTPException(status_code=404, detail="Item not found")

    query2 = "SELECT id FROM dziennik_zdarzen ORDER BY id DESC"
    id = await database.execute(query2)

    if id is None:
        query = Schemas.dziennik_zdarzen.insert().values(id=1, userid=id_user, datatime=request.datatime[0],
                                                         incident=request.incident[0], loss=request.loss[0])
        await database.execute(query)
        for i in range(1, len(request.datatime)):
            await database.execute(queryFunction(i, id, request, id_user))
            id = await database.execute(query2)

    elif id is not None:
        for i in range(0, len(request.datatime)):
            await database.execute(queryFunction(i, id, request, id_user))
            id = await database.execute(query2)

    return id


@app.post("/upload-file")
async def create_upload_file(uploaded_file: UploadFile = File(...)):
    file_location = f"storage/{uploaded_file.filename}"
    with open("storage/" + uploaded_file.filename, "wb+") as file_object:
        shutil.copyfileobj(uploaded_file.file, file_object)
    return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}


@app.post("/upload")
async def create_upload_file(file: bytes = File(...)):
    allowedFiles = {"image/jpeg", "image/png", "image/gif", "image/tiff", "image/bmp", "video/webm"}
    if file.content_type in allowedFiles:
        with open("uploaded_images" + file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print({"filename": file.filename})
    else:
        print("deny")


@app.get("/statistic")
async def getStatistic(id_user: int = Header(None)):
    query1 = "SELECT * FROM dziennik_zdarzen where userid= :userid"
    query2 = "SELECT * FROM warunki_biezace where userid= :userid"
    query3 = "SELECT * FROM zabiegi_agrotechniczne where userid= :userid"
    data1 = await database.fetch_all(query3, values={"userid": id_user})
    data2 = await database.fetch_all(query2, values={"userid": id_user})
    data3 = await database.fetch_all(query1, values={"userid": id_user})

    return data1, data2, data3


def queryFunction(index, id, request, id_user):
    query = Schemas.dziennik_zdarzen.insert().values(id=(id + 1), userid=id_user,
                                                     datatime=request.datatime[index],
                                                     incident=request.incident[index],
                                                     loss=request.loss[index])
    return query


def queryFunction2(index, id, request, id_user):
    query = Schemas.zabiegi_agrotechniczne.insert().values(id=(id + 1), userid=id_user, date=request.date[index],
                                                           action=request.action[index], data1=request.data1[index],
                                                           data2=request.data2[index])
    return query


async def validating(email):
    query = "SELECT * FROM users where email= :email"
    data = await database.execute(query, values={"email": email})
    if data is None:
        return False
    else:
        return True
