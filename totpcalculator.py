import pyotp
import sqlalchemy as db
from sqlalchemy import inspect
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess

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

RST = None   
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = -2
top = padding
bottom = height-padding
x = 0

font = ImageFont.load_default()

while True:
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    #draw.text((x+30, top),       "Github",  font=font, fill=255)
    draw.text((x+50, top+10), pyotp.TOTP(getSecretKey(1).now(), font=font, fill=255)
    #draw.text((x+30, top+20),   "Remaining Time: 30",  font=font, fill=255)
    disp.image(image)
    disp.display()
    time.sleep(.1)



