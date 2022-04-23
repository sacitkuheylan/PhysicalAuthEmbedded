import pyotp
from sqlalchemy import true

while true:
    print(pyotp.TOTP("JBSWY3DPEHPK3PXP").now())