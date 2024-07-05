from fastapi.testclient import TestClient
from main import app, load_db, DB,DictItem 

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
