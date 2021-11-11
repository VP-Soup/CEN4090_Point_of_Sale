# IMPORTANT!
# run CreateDB.py first!

import DataAccess

DataAccess.viewEmployeeTable()

username = "admin"
password = "123"

if DataAccess.validateLoginCredentials(username, password):
    print("Test passed: Login credentials passed for user " + username + " with password " + password)
else:
    print("Test failed: Incorrect login credentials for user " + username + " with password " + password)

username = "admin"
password = "not123"

if not DataAccess.validateLoginCredentials(username, password):
    print("Test passed: Incorrect login credentials for user " + username + " with password " + password)
else:
    print("Test failed: Login credentials passed for user " + username + " with password " + password)

username = "notadmin"
password = "123"

if DataAccess.validateLoginCredentials(username, password) == - 1:
    print("Test passed: User not found for username " + username + " with password " + password)
else:
    print("Test failed: Test failed for invalid user " + username + " with password " + password)

username = "ben"
password = "mypass"
DataAccess.insertEmployee("Ben", "Affleck", username, password)

if DataAccess.validateLoginCredentials(username, password):
    print("Test passed: Login credentials passed for user " + username + " with password " + password)
else:
    print("Test failed: Incorrect login credentials for user " + username + " with password " + password)