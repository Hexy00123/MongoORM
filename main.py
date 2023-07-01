from models import db

user = db.User.find()[0]
user.email = 'smt@mail.ru'
user.username = 'hexy'
user.commit()
