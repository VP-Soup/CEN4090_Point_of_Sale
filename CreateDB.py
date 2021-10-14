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
Password TEXT NOT NULL
);''')
print('Employee Table created successfully.')

# Product
cur.execute('''CREATE TABLE Product(
ProductID INTEGER PRIMARY KEY, 
Name TEXT, 
Quantity INTEGER, 
Cost REAL,
Price REAL, 
Category TEXT 
);''')
print('Transactions Table created successfully.')

# Transactions
cur.execute('''CREATE TABLE Transactions(
TransactionID INTEGER PRIMARY KEY AUTOINCREMENT , 
EmployeeID INTEGER NOT NULL,
TotalCost REAL,
Date TEXT,
PaymentType TEXT
);''')
print('Transactions Table created successfully.')

# Transactions_Item
cur.execute('''CREATE TABLE Transactions_Item(
TransactionID INTEGER PRIMARY KEY NOT NULL, 
ProductID INTEGER NOT NULL,
Quantity INTEGER,
Cost REAL
);''')
print('Transactions_Item Table created successfully.')

conn.commit()

## Populate tables ##

# Employees
emp = [["Sally", "Smith", "admin", "123"], ["John", "Doe", "user1", "123"], ["Heather", "Robbins", "user2", "123"]]
for x in emp: 
    cur.execute('''INSERT INTO Employee(FirstName, LastName, Username, Password) VALUES(?,?,?,?)''', x)

# Products 
prod = [[100, "Chocolate Chip Cookie", 48, 1.50, .25, "Cookie"], [101, "Sugar Cookie", 24, 1.50, .15, "Cookie"], 
        [200, "Plain Bagel", 10, 3.00, .50, "Bread"], [201, "Biscuit", 12, 2.00, .30, "Bread"],
        [300, "Birthday Cake", 5, 15.00, 5.00, "Cake"], [301, "Vanilla Cupcake", 24, 3.00, .50, "Cake"]]
for x in prod: 
    cur.execute('''INSERT INTO Product(ProductID, Name, Quantity, Cost, Price, Category) VALUES(?,?,?,?,?,?)''', x)


conn.commit()
conn.close()
