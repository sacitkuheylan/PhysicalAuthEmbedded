import pyotp
import sqlalchemy as db
from sqlalchemy import inspect

engine = db.create_engine('sqlite:///tokens.db')
connection = engine.connect()
metadata = db.MetaData()
TwoFAToken = db.Table('two_fa_token', metadata, autoload=True, autoload_with=engine)

def getIDList():
    query = db.select([TwoFAToken.columns.id]) 
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    print(ResultSet)


def getSecretKey(id):
    query = db.select([TwoFAToken.columns.secretKey]).where(TwoFAToken.columns.id == id)
    query1 = db.select([TwoFAToken.columns.name]).where(TwoFAToken.columns.id == id)
    query2 = db.select([TwoFAToken.columns.digitCount]).where(TwoFAToken.columns.id == id)
    data = connection.execute(query).scalar()
    data1 = connection.execute(query1).scalar()
    data2 = connection.execute(query2).scalar()
    print("***Key Details***")
    print("Name: " + data1)
    print("Secret Key: " + data)
    print("Digit Count: " + str(data2))
    return data

#TODO: Make calling secretKey details more generic. This or ordered call system won't work when token deletion occurs
for i in range(1,4):
    calculatedToken = pyotp.TOTP(getSecretKey(i))
    print("Calculated Token: " + str(calculatedToken.now()))



