#!/usr/bin/env python
# encoding: utf-8


"""

This version is depreciated because of problems with sqlite. Instead this new source is available at webapi.py file.



import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn

def create_db_table():
    try:
        conn = connect_to_db()
        conn.execute('''DROP TABLE keys''')
        conn.execute('''
            CREATE TABLE keys (
                key_id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                secretkey TEXT NOT NULL,
                digitcount INTEGER NOT NULL
            );
        ''')

        conn.commit()
        print("Keys table created successfully")
    except:
        print("Keys table creation failed")
    finally:
        conn.close()

def insert_user(keys):
    inserted_key = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO keys (name, secretkey, digitcount) VALUES (?, ?, ?)", (keys['name'], keys['secretkey'], keys['digitcount']) )
        conn.commit()
        inserted_key = get_key_by_id(cur.lastrowid)
    except:
        conn().rollback()

    finally:
        conn.close()

    return inserted_key

def get_keys():
    keys = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM keys")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            key = {}
            key["key_id"] = i["key_id"]
            key["name"] = i["name"]
            key["secretkey"] = i["secretkey"]
            key["digitcount"] = i["digitcount"]
            keys.append(key)

    except:
        keys = []

    return keys


def get_key_by_id(key_id):
    key = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM keys WHERE key_id = ?", (key_id,))
        row = cur.fetchone()

        # convert row object to dictionary
        key["key_id"] = row["key_id"]
        key["name"] = row["name"]
        key["secretkey"] = row["secretkey"]
        key["digitcount"] = row["digitcount"]
    except:
        user = {}

    return user

create_db_table()

keys = []
key0 = {
    "name": "Test",
    "secretkey": "JBSWY3DPEHPK3PXP",
    "digitcount": "6",
}

keys.append(key0)

for i in keys:
    print(insert_user(i))

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/keys', methods=['GET'])
def api_get_users():
    return jsonify(get_keys())

@app.route('/api/keys/<key_id>', methods=['GET'])
def api_get_user(user_id):
    return jsonify(get_key_by_id(user_id))
app.run(host='0.0.0.0')
"""
