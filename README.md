# Welcome to PhysicalAuth Embedded Software Repo!
<p align="center">
  <img width="250" height="250" src="https://i.ibb.co/3zzNH99/Physical-Auth-Logo50.png"  title="PhysicalAuth Logo">
</p>


Hi! :wave: Thank you for your interest in **PhysicalAuth**. This page contains information about how to set up Embedded Software and Hardware part of Physical Auth. 

:hourglass:Expected Setup Time :  **30 Minutes**


:warning:**Disclaimer**: This project is still in development and in alpha phase, not all features are available at the moment. General information about **PhysicalAuth** project is available at [PhysicalAuth Main Repository](https://www.github.com/sacitkuheylan/PhysicalAuth)
**Expected beta relase date: :date: 20.05.2022**

# Table of Contents

 - [About Embedded Software and Hardware](#about-embedded-software-and-hardware)
	 - [Files](#files)
	 - [Libraries Used](#libraries-used)
	 - [Setting Up Enviroment](#setting-up-enviroment)
 - [Requirements](#requirements)
	 - [Hardware Requirements](#hardware-requirements)
	 - [Software Requirements](#software-requirements)
 - [Wiring Up Hardware](#wiring-up-hardware)
 - [Database Structure](#database-structure)
 - [Gallery](#gallery)
 - [Contribution](#contribution)
 - [LICENSE](#license)



# About Embedded Software and Hardware
#### Files
This repo contains software that you are going to deploy on your embedded device. This project has two different python projects. They are;

 - webapi.py
	 - This is te **REST API** developed using **Flask**. This is required to run in order to communicate with mobile application. When application starts, it writes Local IP address to LCD Screen. That IP address is going to be used for connecting from mobile device.
 - tokengenerator.py
	 - This is the token calculator application. It communicates with local database that is developed using SQLite and it calculates 6 digit **TOTP** (Time-Based One Time Password) from secret keys that are stored in database.

**Next Milestone:** There is a plan to migrate those two project into one single executeable file. With this way resource consumption will be decreased.

#### Libraries Used

    time
    Adafruit_GPIO
    Adafruit_SSD1306
    PIL
    subprocess
    lib2to3.pgen2
    flask 
    flask_sqlalchemy 
    flask_marshmallow
    flask_restful
    socket
    pyotp
    sqlalchemy

# Requirements
Hardware and Software Requirements are as following. I am still developing and testing with the hardware and software configuration below. There is no guarantee that PhysicalAuth will work on different hardware or software combinations.

 - #### Hardware Requirements 
 	 - A **Wi-Fi Capable** Development Board runs **Linux** (I have used **Raspberry Pi Model 3B+**)
	 - An OLED Screen (I have used 0.91" **SSD1306**)
	 - A Real Time Clock Module (I have used **PCF8523**)
	 - Some Jumper Wires
	 - A Push Button
 - #### Software Requirements
	 - A Linux Distrubution capable to run Python
	 - Required Python Packages are listed at [Libraries Used](#libraries-used) and installation guide is at [Setting Up Enviroment](#setting-up-enviroment)


   

# Getting Ready
In this section there are 2 different guides needed to follow. First one is setting the **Software Enviroment** and the second one is **Wiring Up Hardware**.

## Hardware

### Wiring Up Hardware


With help of a breadborad, we connect our OLED Screen and RTC Module using I2C (Inter-Interconnected Circuit) Interface. Also we need a push button for changing selected token.

<p align="center" href="https://ibb.co/GcPF4y0"><img src="https://i.ibb.co/Tmhrx6k/Screenshot-1.png" alt="Screenshot-1" border="0"></p>

This table below shows pinout diagram of a Raspberry Pi Model 3B+
<p align="center" href="https://imgbb.com/"><img src="https://i.ibb.co/7pQJHCN/Screenshot-2.png" alt="Screenshot-2" border="0"></p>

### Enabling I2C Interfaces

To enable I2C Interfaces, you need to set it up via Raspberry Pi Configuration Tool. To run this tool, open a terminal window and type

    sudo raspi-config

After that you will see screen below. Select 5th option (Interfacing Options)
<p align="center" href="https://imgbb.com/"><img src="https://www.mathworks.com/help/supportpkg/raspberrypiio/ref/raspberrypi_kernel_i2c.png" alt="Screenshot-2" border="0"></p>
When prompted select yes to enable I2C Interface
<p align="center" href="https://imgbb.com/"><img src="https://www.mathworks.com/help/supportpkg/raspberrypiio/ref/raspberrypi_kernel_i2c_enable_disable_option.png" alt="Screenshot-2" border="0"></p>

Now, your I2C Interface is enabled and your external hardware is ready to use.

## Software

#### Setting Up Enviroment
This project requires Python 3 installed to your system in order to run correctly.

Navigate your terminal to project directory and type command

    pip3 install -r requirements.txt 

This operation will iterate recursively through packages listed in **requirements.txt** file and download them.

Contents of requirements.txt is avaliable at [Libraries Used](#libraries-used)

After gathering libraries, you are ready to start your webapi.py and totpcalculator.py source files.
To do that open a terminal window and type

    python3 webapi.py
    python3 totpcalculator.py


# Database Structure
<p align="center" href="https://imgbb.com/"><img src="https://i.ibb.co/J2FSYWN/Screenshot-48.png" alt="Screenshot-48" border="0"></p>

PhysicalAuth uses **SQLite** in the background to store entries. There is one table and this table contains four different attributes they are:

 - id: Unique identifier for every entry.
 - name: This name is given by user and it is used to identify token.
 - secretKey: This is the secret key given from application.
 - digitCount: This is the digit count of token that is going to be generated. It is usally 6.

# Gallery

<p align="center" href="https://ibb.co/7zRfhM8"><img src="https://i.ibb.co/H2xSZw1/Whats-App-Image-2022-05-08-at-22-10-30.jpg" alt="Whats-App-Image-2022-05-08-at-22-10-30" border="0"></p>

> I know it doesn't looks much appetizing for now :smiley: but it will look better I promise

<p align="center" href="https://imgbb.com/"><img src="https://i.ibb.co/HT15QbW/Screenshot-3.png" alt="Screenshot-3" border="0"></p>

# Contribution
Everybody who is passionate about developing information security and also software is welcome to make contributions. You can open a pull request and write a summary about your contribution.

# LICENSE
[Embedded Software MIT License](https://github.com/sacitkuheylan/PhysicalAuthEmbedded/blob/master/LICENSE)
