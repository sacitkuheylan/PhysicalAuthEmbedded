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
import RPi.GPIO as GPIO
import datetime
import socket

engine = db.create_engine('sqlite:///tokens.db')
connection = engine.connect()
metadata = db.MetaData()
TwoFAToken = db.Table('two_fa_token', metadata, autoload=True, autoload_with=engine)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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

#for i in range(1,4):
#    data = getSecretKey(i)
#    secretKeyList.append(data)
#    calculatedToken = pyotp.TOTP(data)
#    print("Calculated Token: " + str(calculatedToken.now()))
secretKeyList = []
nameList = []

def getSecretKeyAsList():
   for row in connection.execute(db.select(TwoFAToken.columns.secretKey)):
       print(row)
       secretKeyList.append("".join(filter(str.isalnum, row)))
   for row in connection.execute(db.select(TwoFAToken.columns.name)):
       print(row)
       nameList.append("".join(filter(str.isalnum, row)))

getSecretKeyAsList()

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
buttonCounter = 0
ipShownFlag = False

def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP

while True:
    
    if GPIO.input(15) == GPIO.HIGH:
        ipShownFlag = True
    
    if ipShownFlag == True:
        if buttonCounter < len(secretKeyList)-1:
            if GPIO.input(15) == GPIO.HIGH:
                buttonCounter = buttonCounter + 1
                time.sleep(0.8)
        elif buttonCounter == len(secretKeyList)-1:
            if GPIO.input(15) == GPIO.HIGH:
                buttonCounter = 0
                secretKeyList = []
                nameList = []
                getSecretKeyAsList()
                
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x+40, top), str(nameList[buttonCounter]),  font=font, fill=255)
        draw.text((x+50, top+10), str(pyotp.TOTP(secretKeyList[buttonCounter]).now()), font=font, fill=255)
        now = datetime.datetime.now()
        draw.text((x+60, top+20),   now.strftime("%S"),  font=font, fill=255)
        disp.image(image)
        disp.display()
    else:
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x+30, top+10), extract_ip(), font=font, fill=255)
        draw.text((x+30, top+20),   "IP ADDRESS",  font=font, fill=255)
        disp.image(image)
        disp.display()
        
    
    



