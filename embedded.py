import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
import mintotp

cred = credentials.Certificate("/home/sacit/Desktop/Senior/physicalauth-firebase-adminsdk-s61k3-c4e4f495e5.json")
firebase_admin = firebase_admin.initialize_app(cred, {'databaseURL': 'https://physicalauth-default-rtdb.europe-west1.firebasedatabase.app/'})

ref = db.reference("/")

with open("secretkeys.json", "r") as f:
	file_contents = json.load(f)

#for key, value in file_contents.items():
#	ref.push().set(value)

ref = db.reference("/-MyYPhG4bM44YXuSMkfl/Secret%20Key")
print(ref.get())

print(mintotp.totp(ref.get()))