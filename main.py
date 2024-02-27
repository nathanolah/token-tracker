##
#
import requests

from observer import observer
from singleton import DatabaseConnection


print("\n")
print("Token-Tracker")
print("********************")

#Login/Signup
#
db = DatabaseConnection()
conn = db.connect()
mycursor = conn.cursor()





db.close()


# cmd = input("Would you like to observe list of tokens y/n: ")
# if (cmd == 'y'):
#     observer()

print('goodbye')

