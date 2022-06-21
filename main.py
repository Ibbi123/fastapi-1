# from fastapi import Depends, FastAPI
# from fastapi.security import OAuth2PasswordBearer
# from fastapi import FastAPI
from fastapi import FastAPI, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

api_keys = [
    "akljnv13bvi2vfo0b0bw"
]  # This is encrypted in the database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # use token authentication

# headers = {
#   'Content-Type': 'application/json',
#   'Authorization': 'akljnv13bvi2vfo0b0bw'
# }

def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    if api_key not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )

app = FastAPI()


fake_db = []                   

@app.get("/items/",)
async def read_items(token: str = Depends(api_key_auth,)):
    return {"token": token}

@app.get("/")
def root():
    return {"message": "Hello World"}
 
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}

@app.post("/items/")
def create_item(item: dict):

    fake_db.append(item)
    return item

@app.get("/items/")
def read_items():
    return fake_db

@app.put("/items/{item_id}")
def update_item(item_id: int, item: dict):
    for i in range(len(fake_db)):
        if fake_db[i]["item_id"] == item_id:
            fake_db[i] = item
            return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for i in range(len(fake_db)):
        if fake_db[i]["item_id"] == item_id:
            del fake_db[i]
            return {"message": "Item deleted"}