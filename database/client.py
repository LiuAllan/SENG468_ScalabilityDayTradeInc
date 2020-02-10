from database import Database
db = Database()
print(db.changeUsers("lsls", 99))
print(db.selectUsers("lsls"))