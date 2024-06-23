from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()
DB = {}

class DictItem(BaseModel):
    key: str
    value: str
    lkl: str | None


@app.get("/items", response_model=DictItem)
def get_key(key: str):
    value = DB.get(key,'') 
    return DictItem(key=key, value=value)



@app.post("/items",response_model=DictItem)
def set_key(body: DictItem):
   DB[body.key]=body.value
   return DictItem(key=body.key,value=body.value)

