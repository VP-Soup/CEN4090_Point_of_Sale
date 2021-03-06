import sqlite3
import bcrypt

conn = sqlite3.connect('BakeryDatabase.db')
cur = conn.cursor()
cur.execute('''PRAGMA foreign_keys = ON''')


# Returns a list of all table names in the DB
def listTables():
    # Note: sqlite_sequence is a table automatically created when Auto Increment is used for a primary key in the
    # database
    arr = list()
    for row in cur.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name!='sqlite_sequence'"""):
        arr.append(row[0])
    return arr


#################################### Employee ####################################
# # Prints every row in the employee table
# def viewEmployeeTable():
#     print('\nEmployee Table:')
#     for x in cur.execute('''SELECT * FROM Employee'''):
#         print(x)


# Prints every row in the employee table
# Rob- changed return for the database window
def viewEmployeeTable():
    # print('\nEmployee Table:')
    # for x in cur.execute('''SELECT * FROM Employee'''):
    #     print(x)
    data = cur.execute('''SELECT * FROM Employee''')
    return (cur, *data)


# Returns list of entire employee table
def listAllEmployee():
    cur.execute('''SELECT * FROM Employee''')
    return cur.fetchall()


# Returns array containing an Employee's first name and last name
def getEmployeeNameFromID(empID):
    cur.execute('''SELECT FirstName, LastName FROM Employee WHERE EmployeeID =?''', (empID,))
    return cur.fetchone()


# Returns True/False if user/pass do/don't match, or -1 if user was not found in db
def validateLoginCredentials(user, password):
    try:
        key = cur.execute("SELECT Password FROM Employee WHERE Username = ?", (user,)).fetchone()[0]
    except TypeError:
        return -1   # user not found in db

    password_bytes = bytes(password, encoding='utf-8')
    key_bytes = bytes(key, encoding='utf-8')

    if bcrypt.checkpw(password_bytes, key_bytes):
        return getEmployeeIDFromLogin(user, key)[0]
    else:
        return 0

# Returns array containing an Employee's attributes from login credentials
def getEmployeeIDFromLogin(user, pas):
    cur.execute('''SELECT * FROM Employee WHERE Username =? AND Password=?''', (user, pas,))
    return cur.fetchone()


# Returns array containing an Employee's attributes from login credentials
def getEmployeeFromLogin(user, pas):
    cur.execute('''SELECT * FROM Employee WHERE Username =? AND Password=?''', (user, pas,))
    return cur.fetchone()


# Inserts a new Employee record into the Employee table
def insertEmployee(firstName='', lastName='', username='', password=''):
    password_bytes = bytes(password, encoding='utf-8')              # encode password
    key = bcrypt.hashpw(password_bytes, bcrypt.gensalt())           # encrypt password

    param_pass = key.decode('utf-8')

    cur.execute('''INSERT INTO Employee (FirstName, LastName, Username, Password) VALUES (?, ?, ?, ?)''',
                       (firstName, lastName, username, param_pass))
    conn.commit()
    return "Employee Inserted"


# Update Employee with ID 
def updateEmployee(empID, firstName='', lastName='', username='', password=''):
    if firstName: 
        cur.execute('''UPDATE Employee SET FirstName = ? WHERE EmployeeID = ?''', (firstName, empID, ))
    if lastName: 
        cur.execute('''UPDATE Employee SET LastName = ? WHERE EmployeeID = ?''', (lastName, empID, ))
    if username: 
        cur.execute('''UPDATE Employee SET Username = ? WHERE EmployeeID = ?''', (username, empID, ))
    if password: 
        cur.execute('''UPDATE Employee SET password = ? WHERE EmployeeID = ?''', (password, empID, ))
    conn.commit()
    return "Employee updated"


# Delete row from Employee table using ID 
def deleteEmployee(empID):
    sql = "DELETE FROM Employee WHERE EmployeeID = ?"
    cur.execute(sql, (empID,))
    conn.commit()
    return "Employee Deleted"


#################################### Product ####################################
# Prints every row in the product table
# def viewProductTable():
#     print('\nProduct Table:')
#     for x in cur.execute('''SELECT * FROM Product'''):
#         print(x)


# Rob- changed to get all the columns and data
# Returned the cursor data
def viewProductTable():
    data=cur.execute('''SELECT * FROM Product''')
    cur.fetchall()
    return (cur,*data)

# Returns a List of all rows in the table
def listAllProduct():
    cur.execute('''SELECT * FROM Product''')
    return cur.fetchall()


# Return Array of all product attributes from ID
# Rob added the [0] to the return
def getProductFromID(prodID):
    cur.execute('''SELECT * FROM Product where ProductID=?''', (prodID,))
    return cur.fetchone()[0]


# Returns Product Name
def getProductNameFromID(prodID):
    cur.execute('''SELECT Name FROM Product where ProductID=?''', (prodID,))
    return cur.fetchone()[0]


# Returns Product Quantity
def getProductQuantityFromID(prodID):
    cur.execute('''SELECT Quantity FROM Product where ProductID=?''', (prodID,))
    return cur.fetchone()[0]


# Returns Product Selling Price
def getProductSellingPriceFromID(prodID):
    cur.execute('''SELECT SellingPrice FROM Product where ProductID=?''', (prodID,))
    return cur.fetchone()[0]


# Returns Product Cost
def getProductCostFromID(prodID):
    cur.execute('''SELECT Cost FROM Product where ProductID=?''', (prodID,))
    return cur.fetchone()[0]


# Returns Product Category
def getProductCategoryFromID(prodID):
    cur.execute('''SELECT Category FROM Product where ProductID=?''', (prodID,))
    return cur.fetchone()[0]


# Returns All Product Category
# Rob-added this to get all the categories
def getProductCategory():
    data=cur.execute('''SELECT Category FROM Product''')
    return data


# Inserts a new Product record into the Product table
def insertProduct(prodID, name = "", quantity= 0, sellP=0, cost=0, category=""):
    cur.execute('''INSERT INTO Product (Name, Quantity, SellingPrice, Cost, Category) VALUES (?, ?, ?, ?, ?)''',
                       (name, quantity, sellP, cost, category))
    conn.commit()
    return "Product Inserted"


# Update Product with ID 
def updateProduct(prodID, name='', quantity=-111, sellingP=-111, cost=-111, category=''):
    if name: 
        cur.execute('''UPDATE Product SET Name = ? WHERE ProductID = ?''', (name, prodID, ))
    if quantity !=-111: 
        cur.execute('''UPDATE Product SET Quantity = ? WHERE ProductID = ?''', (quantity, prodID, ))
    if sellingP !=-111: 
        cur.execute('''UPDATE Product SET SellingPrice = ? WHERE ProductID = ?''', (sellingP, prodID, ))
    if cost !=-111: 
        cur.execute('''UPDATE Product SET Cost = ? WHERE ProductID = ?''', (cost, prodID, ))
    if category: 
        cur.execute('''UPDATE Product SET Category = ? WHERE ProductID = ?''', (category, prodID, ))
    conn.commit()
    return "Product updated"


# Remove Product from table using ID 
def deleteProduct(prodID):
    sql = "DELETE FROM Product WHERE ProductID = ?"
    cur.execute(sql, (prodID,))
    conn.commit()
    return "Product Deleted"


#################################### Transactions ####################################
# # Prints every row in the Transactions table
# def viewTransactionTable():
#     print('\nTransactions Table:')
#     for x in cur.execute('''SELECT * FROM Transactions'''):
#         print(x)


# Prints every row in the Transactions table
# Rob changed teh return type
def viewTransactionsTable():
    data=cur.execute('''SELECT * FROM Transactions''')
    return (cur,*data)


# Returns a List of all rows in the table
def listAllTransactions():
    cur.execute('''SELECT * FROM Transactions''')
    return cur.fetchall()


# Returns row of Transaction from ID 
def getTransactionFromID(tranID):
    cur.execute('''SELECT * FROM Transactions where TransactionID=?''', (tranID,))
    return cur.fetchone()


# Get ID of the employee who completed the transaction 
def getEmployeeIDFromTransactionID(tranID):
    cur.execute('''SELECT EmployeeID FROM Transactions where TransactionID=?''', (tranID,))
    return cur.fetchone()[0]


# Get Total Cost of transaction from the ID 
def getTransactionTotalCostFromID(tranID):
    cur.execute('''SELECT TotalCost from Transactions where TransactionID=?''', (tranID,))
    return cur.fetchone()[0]


# Get the Date of the transaction from the ID 
def getTransactionDateFromID(tranID):
    cur.execute('''SELECT Date from Transactions where TransactionID=?''', (tranID,))
    return cur.fetchone()[0]


# Get the payment type of the transaction from the ID 
def getTransactionPaymentTypeFromID(tranID):
    cur.execute('''SELECT PaymentType from Transactions where TransactionID=?''', (tranID,))
    return cur.fetchone()[0]


# Insert transaction into table and return transaction ID 
def insertTransactions(employeeID="", totalCost=0.0, date="0000-00-00", paymentType="", transactionID=None):
    val = '''NULL''' if transactionID is None else '''?'''

    sql = '''INSERT INTO Transactions (TransactionID, EmployeeID, TotalCost, Date, PaymentType) VALUES (
    ''' + val + ''', ?, ?, ?, ?) ON CONFLICT(TransactionID) DO UPDATE SET EmployeeID = ?, TotalCost = ?, Date = ?, 
    PaymentType = ? '''
    parameters = (employeeID, totalCost, date, paymentType, employeeID, totalCost, date, paymentType,)

    if transactionID is not None:
        parameters = (transactionID,) + parameters

    cur.execute(sql, parameters)
    cur.execute('''SELECT last_insert_rowid() AS new_id''')

    conn.commit()

    return cur.fetchone()[0]


# Update Transaction with ID 
def updateTransactions(tranID, empID=-111, totalCost=-111, date='', paymentType=''):
    if empID !=-111: 
        cur.execute('''UPDATE Transactions SET EmployeeID = ? WHERE TransactionID = ?''', (empID, tranID, ))
    if totalCost !=-111: 
        cur.execute('''UPDATE Transactions SET TotalCost = ? WHERE TransactionID = ?''', (totalCost, tranID, ))
    if date: 
        cur.execute('''UPDATE Transactions SET Date = ? WHERE TransactionID = ?''', (date, tranID, ))
    if paymentType: 
        cur.execute('''UPDATE Transactions SET PaymentType = ? WHERE TransactionID = ?''', (paymentType, tranID, ))
    conn.commit()
    return "Transaction updated"


# Remove transaction from table using ID 
def deleteTransactions(tranID):
    sql = "DELETE FROM Transactions WHERE TransactionID = ?"
    cur.execute(sql, (tranID,))
    conn.commit()
    return "Transaction Deleted"


#################################### Transactions_Item ####################################
# Prints every row in the Transactions_Item table
# def viewTran_ItemTable():
#     print('\nTransactions_Item Table:')
#     for x in cur.execute('''SELECT * FROM Transactions_Item'''):
#         print(x)


# Prints every row in the Transactions_Item table
# Rob-changed to get data for database view
def viewTransactions_ItemTable():
    data=cur.execute('''SELECT * FROM Transactions_Item''')
    return(cur,*data)


# Returns a List of all rows in the table
def listAllTran_Item():
    cur.execute('''SELECT * FROM Transactions_Item''')
    return cur.fetchall()

# Returns a List of all rows in the table
# Rob-changed to make the 'tran' to 'transactions' like the others
def listAllTransactions_Item():
    cur.execute('''SELECT * FROM Transactions_Item''')
    return cur.fetchall()


# return row of Transactions_item table using TrasactionID and ProductID 
def getTran_ItemFromTranIDProdID(tranID, prodID):
    cur.execute('''SELECT * FROM Transactions_Item WHERE TransactionID=? AND ProductID=?''', (tranID, prodID,))
    return cur.fetchone()


# Get the Quantity of the Transactions_item using 2 IDs
def getTran_ItemQuantityFromTranIdProdID(tranID, prodID):
    cur.execute('''SELECT Quantity FROM Transactions_Item WHERE TransactionID=? AND ProductID=?''', (tranID, prodID,))
    return cur.fetchone()[0]


# Get the Cost of the Transactions_item using 2 IDs
def getTran_ItemCostFromTranIdProdID(tranID, prodID):
    cur.execute('''SELECT Cost FROM Transactions_Item WHERE TransactionID=? AND ProductID=?''', (tranID, prodID,))
    return cur.fetchone()[0]


# Inserts a new Transaction_Item record into the Transaction_Item table
def insertTransactions_Item(transactionID, productID, quantity=0, cost=0.00):
    try: 
        cur.execute('''INSERT INTO Transactions_Item (TransactionID, ProductID, Quantity, Cost) VALUES (?, ?, ?, ?)''',
                        (transactionID, productID, quantity, cost))
        conn.commit()
        return "Transaction Item Inserted"
    except sqlite3.IntegrityError:
        return "Invalid Transaction/Product ID"


# Update Transaction_Item with IDs
def updateTransactions_Item(tranID, prodID, quantity=-111, cost=-111):
    if quantity !=-111: 
        cur.execute('''UPDATE Transactions_Item SET Quantity = ? WHERE TransactionID = ? AND ProductID = ?''',
         (quantity, tranID, prodID, ))
    if cost !=-111: 
        cur.execute('''UPDATE Transactions_Item SET Cost = ? WHERE TransactionID = ? AND ProductID = ?''',
         (cost, tranID, prodID, ))
    conn.commit()
    return "Transaction_Item updated"


# Remove transaction from table using ID 
def deleteTransactions_Item(tranID, prodID):
    sql = "DELETE FROM Transactions_Item WHERE TransactionID = ? AND ProductID = ?"
    cur.execute(sql, (tranID, prodID,))
    conn.commit()
    return "Transactions_Item Deleted"