import hashlib
import os
import sqlite3
 
conn = sqlite3.connect('BakeryDatabase.db')
cur = conn.cursor()

######### Create Database #########

## Drop tables ##
try: 
    conn.execute('''DROP TABLE Employee''')
    conn.commit()
    print("Employee table dropped.")
except: 
    print("Employee table doesn't exist.")

try: 
    conn.execute('''DROP TABLE Product''')
    conn.commit()
    print("Product table dropped.")
except: 
    print("Product table doesn't exist.")

try: 
    conn.execute('''DROP TABLE Transactions''')
    conn.commit()
    print("Transactions table dropped")
except: 
    print("Transactions table doesn't exist")

try: 
    conn.execute('''DROP TABLE Transactions_Item''')
    conn.commit()
    print("Transactions_Item table dropped")
except: 
    print("Transactions_Item table doesn't exist")


## Create tables ##
print("\nCreate Tables in DB")

# Employee
cur.execute('''CREATE TABLE Employee(
EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT, 
FirstName TEXT NOT NULL,
LastName TEXT NOT NULL,
Username TEXT NOT NULL, 
Password TEXT NOT NULL,
PasswordSalt TEXT NOT NULL
);''')
print('Employee Table created successfully.')

# Product
cur.execute('''CREATE TABLE Product(
ProductID INTEGER PRIMARY KEY AUTOINCREMENT, 
Name TEXT, 
Quantity INTEGER, 
SellingPrice REAL,
Cost REAL, 
Category TEXT 
);''')
print('Product Table created successfully.')

# Transactions
cur.execute('''CREATE TABLE Transactions(
TransactionID INTEGER PRIMARY KEY AUTOINCREMENT, 
EmployeeID INTEGER NOT NULL,
TotalCost REAL,
Date TEXT,
PaymentType TEXT
);''')
print('Transactions Table created successfully.')

# Transactions_Item
cur.execute('''CREATE TABLE Transactions_Item(
TransactionID INTEGER NOT NULL REFERENCES Transactions(TransactionID)
    ON DELETE CASCADE,
ProductID INTEGER NOT NULL REFERENCES Product(ProductID),
Quantity INTEGER,
Cost REAL
 
);''')
print('Transactions_Item Table created successfully.')

conn.commit()

## Populate tables ##

# Employees
# emp = [["Sally", "Smith", "admin", "123"], ["John", "Doe", "user1", "123"], ["Heather", "Robbins", "user2", "123"]]
# for x in emp:
#     salt = os.urandom(64)   # generate a random password salt
#     key = hashlib.pbkdf2_hmac('sha256', x[3].encode('utf-8'), salt, 100000)     # hash password
#     x[3] = str(key)         # replace plain-text password with hashed password
#     x.append(str(salt))     # save password salt
#     cur.execute('''INSERT INTO Employee(FirstName, LastName, Username, Password, PasswordSalt) VALUES(?,?,?,?,?)''', x)

# Products 
prod = [["Chocolate Chip Cookie", 48, 1.50, .25, "Cookie"], ["Sugar Cookie", 24, 1.50, .15, "Cookie"], 
        ["Plain Bagel", 10, 3.00, .50, "Bread"], ["Biscuit", 12, 2.00, .30, "Bread"],
        ["Birthday Cake", 5, 15.00, 5.00, "Cake"], ["Vanilla Cupcake", 24, 3.00, .50, "Cake"]]
for x in prod: 
    cur.execute('''INSERT INTO Product(Name, Quantity, SellingPrice, Cost, Category) VALUES(?,?,?,?,?)''', x)

# Transaction
tran = [[1, 22.47, "10/19/21", "cash"],
        [2, 5.50, "1/10/20", "cash"]]
for x in tran:
    cur.execute('''INSERT INTO Transactions(EmployeeID, TotalCost, Date, PaymentType) VALUES(?,?,?,?)''', x)

# Transaction Items
tran_it = [[1, 5, 1, 15.00], 
           [1, 6, 2, 6.00]]
for x in tran_it:
    cur.execute('''INSERT INTO Transactions_Item(TransactionID, ProductID, Quantity, Cost) VALUES(?,?,?,?)''', x)

conn.commit()
conn.close()
