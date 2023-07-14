from models import *

if __name__ == '__main__':
    # creating objects
    admin_id = db.User.add(name='Admin', age=26)
    basket_id = db.Basket.add(items=[])
    item1_id = db.Item.add(name='item1', price=200)
    item2_id = db.Item.add(name='item2', price=500)
    item3_id = db.Item.add(name='item3', price=100)

    # getting objects
    admin = db.User[admin_id]
    basket = db.Basket[basket_id]

    # updating objects
    admin.basket_id = basket_id
    admin.commit()

    # searching
    basket.items = basket.items + [item._id for item in db.Item.find(price=lambda price: price < 400)]
    basket.commit()

    # all objects have their own methods for printing
    # by default
    print(admin)
    print(basket)
    for item_id in basket.items:
        print(db.Item[item_id])
