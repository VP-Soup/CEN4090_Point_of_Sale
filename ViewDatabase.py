import sqlite3
 
conn = sqlite3.connect('BakeryDatabase.db')
cur = conn.cursor()

print("\nEmployee Table:")
for row in cur.execute("SELECT * FROM Employee"):
    print(row)

print("\nProduct Table:")
for row in cur.execute("SELECT * FROM Product"):
    print(row)

print("\nTransactions Table:")
for row in cur.execute("SELECT * FROM Transactions"):
    print(row)

print("\nTransactions_Item Table:")
for row in cur.execute("SELECT * FROM Transactions_Item"):
    print(row)
