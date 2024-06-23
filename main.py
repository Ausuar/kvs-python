from fastapi import FastAPI,HTTPException

from pydantic import BaseModel

app = FastAPI()
DB = {}

class DictItem(BaseModel):
    key: str
    value: str


@app.get("/items", response_model=DictItem)
def get_key(key: str):
    value = DB.get(key)
    if value is None:
        raise HTTPException(status_code=404) 
    return DictItem(key=key, value=value)



@app.post("/items",response_model=DictItem)
def set_key(body: DictItem):
   DB[body.key]=body.value
   return DictItem(key=body.key,value=body.value)

@app.delete("/itmes/{key}", response_model=DictItem)
def delete_key(key):
    if key in DB:
        value=DB.pop(key)
    else:
        raise HTTPException(status_code=404,detail="key is not found")
    return DictItem(key=key, value=value)