import sqlite3
 
conn = sqlite3.connect('BakeryDatabase.db')
cur = conn.cursor()

# Returns a list of all table names in the DB 
def listTables():
    # Note: sqlite_sequence is a table automatically created when Auto Increment is used for a primary key in the database 
    cur.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name!='sqlite_sequence'""")
    return cur.fetchall()

#################################### Employee ####################################
# Prints every row in the employee table 
def viewEmployeeTable():
    print('\nEmployee Table:')
    for  x in cur.execute('''SELECT * FROM Employee'''):
        print (x)

# Returns list of entire employee table
def listAllEmployees():
    cur.execute('''SELECT * FROM Employee''')
    return cur.fetchall()

# Returns array containing an Employee's firstname and last name 
def getEmployeeNameFromID(empID):
    cur.execute('''SELECT FirstName, LastName FROM Employee WHERE EmployeeID =?''', (empID, ))
    return cur.fetchone()

# Returns True if username and password is valid / False otherwise 
def validateLoginCredentials(user, pas):
    # If Username exists, check password 
    if (cur.execute("""SELECT Username FROM Employee WHERE Username = ?""", (user,)).fetchone()):
        # If Password exists, return true 
        if((cur.execute("""SELECT Password FROM Employee WHERE Password = ?""", (pas,)).fetchone())):
            return True
        else: 
            return False  # Password invalid 
    else:   
        return False      # Username invalid 

# Returns array containing an Employee's attributes from login credentials 
def getEmployeeFromLogin(user, pas):
    cur.execute('''SELECT * FROM Employee WHERE Username =? AND Password=?''', (user, pas, ))
    return cur.fetchone()


#################################### Product ####################################
# Prints every row in the product table 
def viewProductTable():
    print('\nProduct Table:')
    for  x in cur.execute('''SELECT * FROM Product'''):
        print (x)

# Returns a List of all rows in the table 
def listAllProducts():
    cur.execute('''SELECT * FROM Product''')
    return cur.fetchall()

# Return Array of all product attributes from ID
def getProductFromID(prodID):
    cur.execute('''SELECT * FROM Product where ProductID=?''', (prodID, ))
    return cur.fetchone()

# Returns Product Name 
def getProductNameFromID(prodID):
    cur.execute('''SELECT Name FROM Product where ProductID=?''', (prodID, ))
    return cur.fetchone()[0]

# Returns Product Quantity
def getProductQuantityFromID(prodID):
    cur.execute('''SELECT Quantity FROM Product where ProductID=?''', (prodID, ))
    return cur.fetchone()[0]

# Returns Product Selling Price
def getProductSellingPriceFromID(prodID):
    cur.execute('''SELECT SellingPrice FROM Product where ProductID=?''', (prodID, ))
    return cur.fetchone()[0]

# Returns Product Cost
def getProductCostFromID(prodID):
    cur.execute('''SELECT Cost FROM Product where ProductID=?''', (prodID, ))
    return cur.fetchone()[0]

# Returns Product Category 
def getProductCategoryFromID(prodID):
    cur.execute('''SELECT Category FROM Product where ProductID=?''', (prodID, ))
    return cur.fetchone()[0]


#################################### Transactions ####################################
# Prints every row in the Transactions table 
def viewTransactionsTable():
    print('\nTransactions Table:')
    for  x in cur.execute('''SELECT * FROM Transactions'''):
        print (x)


#################################### Transactions_Item ####################################
# Prints every row in the Transactions_Item table 
def viewTransactions_ItemTable():
    print('\nTransactions_Item Table:')
    for  x in cur.execute('''SELECT * FROM Transactions_Item'''):
        print (x)

