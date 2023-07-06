from typing import Union
from fastapi import FastAPI, Request, Depends, Body
from fastapi.openapi.utils import get_openapi
from starlette.requests import Request
import requests
import sqlite3
import hashlib

from .model import UserSchema, UserLoginSchema
from auth_handler import signJWT
from auth_bearer import JWTBearer
from genqrcode import generate_qrcode

users = []

app = FastAPI()

# The id starts by 7
URL = "https://615f5fb4f7254d0017068109.mockapi.io/api/v1/"
headers = {'Accept': 'application/json'}

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

def hash(password):
    password = password.encode("utf-8")  # Convert the password to bytes
    # Hash the password using SHA-256 algorithm
    hashed_password = hashlib.sha256(password).hexdigest()
    return hashed_password


@app.get("/home", tags=["home"])
async def get_posts():
    return { "data": "Welcome to PayTonKawa" }


@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    user.password = hash(user.password)
    user.id = 7 + len(users)
    users.append(user)
    return signJWT(user.email)

@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    user.password = hash(user.password)
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }

@app.post("/user/login/qrcode", tags=["user"])
async def user_login_qrcode(user: UserLoginSchema = Body(...)):
    user.password = hash(user.password)
    if check_user(user):
        token = signJWT(user.email)
        return generate_qrcode(user.email, token)
    return {
        "error": "Wrong login details!"
    }
#================================================================================

@app.get("/customers", dependencies=[Depends(JWTBearer())], tags=["customers"])
async def get_costumers():
    url = f"{URL}customers"
    resp = requests.get(url, headers=headers)
    return resp.json()

@app.get("/customers/{customer_id}", dependencies=[Depends(JWTBearer())], tags=["customers"])
async def get_costumer(customer_id: int, request: Request):
    url = f"{URL}customers/{customer_id}"
    resp = requests.get(url, headers=headers)
    return resp.json()


@app.get("/customers/{customer_id}/orders", dependencies=[Depends(JWTBearer())], tags=["customers"])
async def get_costumer_orders(customer_id: int, request: Request):
    url = f"{URL}customers/{customer_id}/orders"
    resp = requests.get(url, headers=headers)
    return resp.json()

@app.get("/customers/{customer_id}/orders/{order_id}/products", dependencies=[Depends(JWTBearer())], tags=["customers"])
async def get_costumer_products(customer_id: int, order_id: int, request: Request):
    url = f"{URL}customers/{customer_id}/orders/{order_id}/products"
    resp = requests.get(url, headers=headers)
    return resp.json()


#@app.put("/items/{item_id}")
#def update_item(item_id: int, item: int):
#    return {"item_name": item.name, "item_id": item_id}
    

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="PayeTonKawa",
        version="1.0",
        description="REST APIs for PayeTonKawa Revendeurs",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)