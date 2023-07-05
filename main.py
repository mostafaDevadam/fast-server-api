from fastapi import FastAPI, Body
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from pymongo import MongoClient
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
import json
from app.routers import basic, customer, order, iQL
#from app.routers import customer
from starlette.graphql import GraphQLApp
import graphene
#
from dotenv import load_dotenv
import os
#
load_dotenv()

#


# db connection
client = MongoClient("mongodb://127.0.0.1:27017/")
# define db_name as "fastapiDB"
db = client["fastapiDB"]
# define table_name as "user"
collection = db["user"]

#
app = FastAPI()
#

# class and Enum
class ModelName(str, Enum): 
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


     

# class
class Item(BaseModel):
    name: str 
    price: float 
    is_offer: Optional[bool] = None


# class Item
class ItemV(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# class User
class User(BaseModel): 
    username: str 
    full_name: Optional[str] = None

# class UserIn
class UserIn(BaseModel):
    username: str
    password: str 
    email: EmailStr
    full_name: Optional[str] = None


# class UserOut
class UserOut(BaseModel):
    _id: Optional[ObjectId]
    username: str
    email: EmailStr
    full_name: Optional[str] = None





# add routes from customer file
app.include_router(customer.router)
# add routes from order file
app.include_router(order.router)
# add GraphQL route from iQL file
app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=iQL.Query, mutation= iQL.MyMutations)))




# GraphQL
class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_hello(self, info, name):
        return "Hello " + name
    
#app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query)))    

# routes
@app.post("/user/add/", response_model=UserOut)
async def create_user(user: UserIn): 
    print("user: ", user)
    # insert into mongodb
    res = collection.insert_one({"username": user.username, "email": user.email, "full_name": user.full_name})
     #tb = jsonable_encoder(user)
    #res = collection.insert_one(tb)
    #
    print("user is created with id is ", res.inserted_id)
    # get new user by id
    res2 = collection.find_one({"_id": ObjectId(res.inserted_id)})
    print("get new user by id: ", res2)
    
    user = res2
    return user




# update product
@app.put("/product/{product_id}")
async def update_product(product_id: int, item: Item = Body(..., embed=True)):
    result = {"product_id": product_id, "item": item}
    return result




# update thing
@app.put("/things/{thing_id}")
async def update_thing(thing_id: int, item: ItemV, user: User): 
    results = {"thing_id": thing_id, "item":item, "user": user}
    #
    print("results: ", results)
    #
    return results


# get
@app.get('/')
async def index():
    basic.display()
    return {"message":"Hello world from fast-api"}

# get by id
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id":item_id, "q":q}

# update by item_id
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item): 
    return { "item_name": item.name, "item_id": item_id}

# get
@app.get("/user/{_id}")
def get_user_by_id(_id: int):
    return {"user": {"_id": _id}} 

#
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName): 
    if model_name == ModelName.alexnet: 
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    
    if model_name.value == "lenet":
        return { "model_name": model_name, "message": "LeCNN all the images"}
    
    return {"model_name": model_name, "message":"Have some residuals"}