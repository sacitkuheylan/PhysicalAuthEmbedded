import pyotp
import sqlalchemy as db
from sqlalchemy import inspect

engine = db.create_engine('sqlite:///tokens.db')

"""
inspector = inspect(engine)
print(inspector.get_table_names())
for table_name in inspector.get_table_names():
   for column in inspector.get_columns(table_name):
       print("Column: %s" % column['name'])
"""

connection = engine.connect()
metadata = db.MetaData()
TwoFAToken = db.Table('two_fa_token', metadata, autoload=True, autoload_with=engine)
query = db.select([TwoFAToken.columns.secretKey]).where(TwoFAToken.columns.id == 2)
query2 = db.select([TwoFAToken.columns.secretKey])
data = connection.execute(query).scalar()

ResultProxy = connection.execute(query2)
ResultSet = ResultProxy.fetchall()

print(data)
print(ResultSet[:2])

calculatedToken = pyotp.TOTP(data)


