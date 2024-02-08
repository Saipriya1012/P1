from fastapi import FastAPI, HTTPException, APIRouter
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel
from typing import Dict,Optional

app = FastAPI()

class Blog(BaseModel):
    name: str
    desc:str
    data: Dict  

class MongoDB:
    def __init__(self, database_name, collection_name):
        self.client = MongoClient('mongodb+srv://Saipriya:Priya2002@cluster0.voqtxao.mongodb.net/')
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
        self.router = APIRouter()

        @self.router.post("/")
        def create(blog: Blog):
            return {"id": self.create_document(blog.dict())}

        @self.router.get("/")
        def read(id: str):
            return self.read_document(id)

        @self.router.put("/")
        def update(id:str,key:str, value:str, blog: Blog):
            return {"result": self.update_document(id,key,value,blog.dict())}

        @self.router.delete("/")
        def delete(key: str, value: str):
            return {"result": self.delete_document(key, value)}

    def create_document(self, document: dict):
        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    def read_document(self, id):
        result = self.collection.find_one({"_id": ObjectId(id)})
        return str(result)

    def update_document(self, id:str,key:str, value: str,data: dict):
        query = {key:value}
        result = self.collection.update_one(query,{"_id":ObjectId(id)},{'$set':data})
        if result.modified_count > 0:
            return "Document updated successfully."
        else:
            return "No document found."

    def delete_document(self, key: str, value: str):
        query = {key: value}
        result = self.collection.delete_one(query)
        if result.deleted_count > 0:
            return "Document deleted successfully."
        else:
            return "No document found."

mongo_db = MongoDB(database_name='blogs', collection_name='test1')
app.include_router(mongo_db.router)
