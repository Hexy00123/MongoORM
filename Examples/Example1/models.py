from DataBase import *
from config import CONNECTION_STRING

db = DataBase('Example1', CONNECTION_STRING)


class User:
    name: str
    age: int
    basket_id: str


class Basket:
    items: list[str]


class Item:
    name: str
    price: float


db.add_collection(User)
db.add_collection(Basket)
db.add_collection(Item)
db.build()
