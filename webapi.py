from lib2to3.pgen2 import token
from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
from flask_restful import Resource, Api
import socket
import subprocess

app = Flask(__name__) 
api = Api(app) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tokens.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app) 
ma = Marshmallow(app)

class TwoFAToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    secretKey = db.Column(db.String(256))
    digitCount = db.Column(db.Integer)

    def __init__(self, name, secretKey, digitCount):
        self.name = name
        self.secretKey = secretKey
        self.digitCount = digitCount

class TwoFATokenSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'secretKey', 'digitCount')

token_schema = TwoFATokenSchema() 
tokens_schema = TwoFATokenSchema(many=True)

class TwoFATokenManager(Resource): 
    @staticmethod
    def get():
        try: id = request.args['id']
        except Exception as _: id = None

        if not id:
            tokens = TwoFAToken.query.all()
            return jsonify(tokens_schema.dump(tokens))
        token = TwoFAToken.query.get(id)
        return jsonify(token_schema.dump(token))

    @staticmethod
    def post():
        secretKey = request.json['name']
        name = request.json['secretKey']
        digitCount = request.json['digitCount']

        token = TwoFAToken(secretKey, name, digitCount)
        db.session.add(token)
        db.session.commit()

        return jsonify({
        'Message': f'Token {name} successfully inserted.'
    })

    @staticmethod
    def put():
        try: id = request.args['id']
        except Exception as _: id = None

        if not id:
            return jsonify({ 'Message': 'Must provide the token ID' })

        name = request.json['name']
        secretKey = request.json['secretKey']
        digitCount = request.json['digitCount']

        token.secretKey = secretKey
        token.name = name
        token.digitCount = digitCount

        db.session.commit()
        return jsonify({
            'Message': f'Token {name} updated!'
    })

    @staticmethod
    def delete():
        try: id = request.args['id']
        except Exception as _: id = None

        if not id:
            return jsonify({ 'Message': 'Must provide the token ID' })

        token = TwoFAToken.query.get(id)
        db.session.delete(token)
        db.session.commit()

        return jsonify({
        'Message': f'Token {str(id)} deleted successfully.'
    })

api.add_resource(TwoFATokenManager, '/api/tokens')

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
        