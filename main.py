from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class TODO(BaseModel):
    id : int
    task : str
    status : bool

TODO_list : List[TODO] = []

@app.get("/")
def welcome():
    return {"message": "Welcome to my todo list"}

@app.post("/add")
def add_item(item : TODO):
    TODO_list.append(item)
    return {"message": "Item Added successfully"}

@app.put("/add/{item_id}")
def update_item(item_id : int, updated_item : TODO):
    for indeii, id in enumerate(TODO_list):
        if id == item_id:
            TODO_list[indeii] = update_item
            return {"message": "Item updated successfully"}
    else:
        return {"message": "item not found"}
    
@app.delete("/delete/{item_id}")
def delete_item(item_id : int):
    for index, id in TODO_list:
        if id == item_id:
            TODO_list.pop[index]
            return {"message": "item deleted successfully"}
    return {"error": "item not found"}

