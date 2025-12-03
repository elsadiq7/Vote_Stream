from app.main import app
from app import schemas
from .database import client,session
import pytest



def test_root(client):
    res=client.get("/")
    assert res.json().get("message")=="Welcome to the FastAPI Posts API"
    assert res.status_code==200

@pytest.fixture
def test_user(client):
    user_data={
        "email":"test@gmail.com",
        "password":"test123"
    }
    res=client.post("/users/",json=user_data)
    new_user=res.json()
    new_user["password"]=user_data["password"]
    return new_user

# def test_create_user(client):
#     res=client.post("/users/",json={"email":"test@gmail.com","password":"test123"})
#     new_user=schemas.UserOut(**res.json())
#     assert new_user.email=="test@gmail.com"

#     assert res.status_code==201   
    
def test_login_user(test_user,client):
    
    res=client.post("/login",data={"username":test_user['email'],"password":test_user['password']})
    login_res=schemas.Token(**res.json())
    assert login_res.token_type=="bearer"
    assert res.status_code==200