from DataAccess import * 

print("Display all tables")
print(listTables())

'''
print("Test Employee DAL")
print("\nTest retrieving single employee from table")
emp1 = getEmployeeNameFromID(3)
print(emp1)
print("First Name: " + emp1[0])
print("Last Name: " + emp1[1])

print("\nTest Retrieving Table As List")
employees = listAllEmployees()
print (employees)
print(employees[0][1] + "'s security level: " + employees[0][3])

'''
'''
print("\nTest login\n")

print("Valid login Test:")
if (validateLoginCredentials("user1", "123")):
    print('logged in')
else:
    print('invalid username/password')

print("\nInvalid Username Test:")
if (validateLoginCredentials("Boop", "123")):
    print('logged in')
else:
    print('invalid username/password')

print("\nInvalid Password Test:")
if (validateLoginCredentials("user1", "Beep")):
    print('logged in')
else:
    print('invalid username/password')

print("\nInvalid Username and Password Test:")
if (validateLoginCredentials("Boop", "Beep")):
    print('logged in')
else:
    print('invalid username/password')
'''

'''
print("\nGet Employee from Username and Password")
emp = getEmployeeFromLogin("user2", "123")
print(f"ID: {emp[0]}")
print(f"Name: {emp[1]} {emp[2]}")
'''

print("Test Product Table")
viewProductTable()

print("\nList Format")
print(listAllProducts())

print("\nSingle item select query")
print(getProductFromID(100)) #Prints Array of Queried Row
print(f"Name: {getProductFromID(100)[1]}") 
print("Selling Cost: ${:0.2f}".format(getProductFromID(100)[3]))

print()
print(f"Name: {getProductNameFromID(301)}")
print(f"Quantity: {getProductQuantityFromID(301)}")
print("Selling Price: ${:0.2f}".format(getProductSellingPriceFromID(301)))
print("Cost: ${:0.2f}".format(getProductCostFromID(301)))
print(f"Category: {getProductCategoryFromID(301)}")