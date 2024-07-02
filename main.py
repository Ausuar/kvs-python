from fastapi import FastAPI,HTTPException #载入FastAPI,HTTPException模块
from pydantic import BaseModel#载入BaseModel模块
from fastapi.testclient import TestClient#载入TestClient模块用于测试
import json

app = FastAPI()#创造一个fastapi实例
DB = {}#创建一个空字典
db_filename = "db.json"

def load_db():
    try:
        with open(db_filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_db(data):
    with open(db_filename, "w") as f:
        json.dump(data, f, indent=4)

DB = load_db()
class DictItem(BaseModel):#创建一个DicIetm类，key和value元素为字符串类型
    key: str
    value: str

@app.get("/items", response_model=DictItem)#创建一个路径为/items的get方法
def get_key(key: str):
    value = DB.get(key)#获取key对应的value
    if value is None:#如果key不在就返回404，并报key is not found
        raise HTTPException(status_code=404,detail="key is not found") 
    return DictItem(key=key, value=value)#返回一个dictitem


@app.post("/items",response_model=DictItem)
def set_key(body: DictItem):
   DB[body.key]=body.value#添加一个键为body.key 值为body.value的元素
   save_db(DB)
   return DictItem(key=body.key,value=body.value)#返回一个dictitem

@app.delete("/items", response_model=DictItem)
def delete_key(key):
    if key in DB:#如果key在DB里就删掉key
        value=DB.pop(key)
        save_db(DB)
    else:#如果key不在，返回404并说明key is not found
        raise HTTPException(status_code=404,detail= "key is not found")
    return DictItem(key=key, value=value)#返回一个Dictitem

def test_item():
    client = TestClient(app)
    #获取空表
    response = client.get("/items",params={"key":"foo"})#从get中获取信息
    assert response.status_code == 404#状态码404说明没找到
    #添加字符串
    response = client.post("items",json={"key":"foo","value":"bar"})#从post中获取信息
    assert response.status_code == 200#状态码200说明成功添加字符串
    assert response.json()=={"key":"foo","value":"bar"}#确保返回的值符合结构
    #判断是否添加成功
    response = client.get("/items",params={"key":"foo"})#从get中获取信息
    assert response.status_code==200#状态码200说明成功获取添加的字符串
    assert DictItem(**response.json())==DictItem(key="foo",value="bar")#确保返回的值符合Dicitem的结构
    #删除key
    response = client.delete("/items",params={"key":"foo"})#从delet中获取信息
    assert response.status_code==200#状态码200说明运行成功
    #判断是否删除成功
    response=client.get("/items",params={"key":"foo"})#从get里获取信息
    assert response.status_code== 404#判断404没找到说明删除成功
if __name__ == "__main__":
    DB = load_db()
    client = TestClient(app)
    test_item()
    
    
