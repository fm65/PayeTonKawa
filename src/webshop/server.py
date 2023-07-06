from typing import Union
from fastapi import FastAPI, Request, Depends, Body, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.utils import get_openapi
from starlette.requests import Request
import jwt
import requests
import sqlite3
import hashlib

from .model import UserSchema, UserLoginSchema
from auth_handler import signJWT, decodeJWT
from auth_bearer import JWTBearer
from genqrcode import generate_qrcode

users = []

app = FastAPI()
security = HTTPBearer()

# The id starts by 7
URL = "https://615f5fb4f7254d0017068109.mockapi.io/api/v1/"
headers = {'Accept': 'application/json'}


# Function to get the current user from the token
def get_current_user(token):
    try:
        decoded_token = decodeJWT(token)
        current_user = decoded_token.get("email")  # Replace with the key that holds the username in the token
        return current_user
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

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

@app.get("/customer/info", tags=["customer"])
async def get_costumer(dependencies=Depends(JWTBearer())):
    customer_id = get_current_user(dependencies)
    print(customer_id)
    customer_id=7
    url = f"{URL}customers/{customer_id}"
    resp = requests.get(url, headers=headers)
    return resp.json()


@app.get("/customer/orders", tags=["customer"])
async def get_costumer_orders(dependencies=Depends(JWTBearer())):
    customer_id = 7
    url = f"{URL}customers/{customer_id}/orders"
    resp = requests.get(url, headers=headers)
    return resp.json()

@app.get("/customer/orders/{order_id}/products", tags=["customer"])
async def get_costumer_products(order_id: int, dependencies=Depends(JWTBearer())):
    customer_id = 7
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
        description="REST APIs for PayeTonKawa Webshop",
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