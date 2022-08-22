

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from  flask_marshmallow import Marshmallow
from flask_cors import CORS
from config import config

app = Flask(__name__)
CORS(app) 

app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://jbatistav:Hardware100.@34.75.68.76/jbatistav'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db =SQLAlchemy(app)
ma =  Marshmallow(app)


#tabla banco ################### MODELO BANCO
class Banks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(), nullable=False, default=db.func.current_timestamp())
    

    def __init__(self,name):
        self.name = name



#esquema bancos
class BankSchema(ma.Schema):
    class Meta:
        fields =('id','name')
        
#UNA SOLA RESPUESTA      
bank_schema = BankSchema()

#MUCHAS RESPUESTAS
banks_schema = BankSchema(many=True)

#MODELO TIPO_CUENTAS
class AccountTypes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(), nullable=False, default=db.func.current_timestamp())
    
    #contructor modelo tipo cuentas
    def __init__(self,description):
        self.description = description
        
#esquema tipo cuentas
class TypeCountSchema(ma.Schema):
    class Meta:
        fields =('id','description')
        
#UNA SOLA RESPUESTA      
type_count_schema = TypeCountSchema()

#MUCHAS RESPUESTAS
type_counts_schema = TypeCountSchema(many=True)

db.create_all()
    
#leer los bancos de la bd
@app.route('/get_bank', methods = ['GET'])
def get_banks():
    all_bank=Banks.query.all()
    result =banks_schema.dump(all_bank)
    return jsonify(result)

#leer un solo banco GET * ID #######
@app.route('/get_bank/<id>',methods = ['GET'])
def get_bank_x_id(id):
    one_bank = Banks.query.get(id)
    return bank_schema.jsonify(one_bank)
    

#ingresar un nuevo banco### POST
@app.route('/insert_bank', methods = ['POST'])
def add_bank():  
    name =request.json['name']
    bank = Banks(name)
    db.session.add(bank)
    db.session.commit()
    return bank_schema.jsonify(bank)


#put ######
@app.route('/update_banck/<id>', methods=['PUT'])
def update_bank(id):
    upd_banck = Banks.query.get(id)
    name = request.json['name']
    upd_banck.name = name
    db.session.commit()
    return bank_schema.jsonify(upd_banck)

#delete
@app.route('/delete_bank/<id>', methods=['DELETE'])
def delete_bank(id):
    del_bank = Banks.query.get(id)
    db.session.delete(del_bank)
    db.session.commit()
    return jsonify({'mensaje':"Banco Eliminado"})


## metodos model count type
#leer los type_count de la bd
@app.route('/get_type_count', methods = ['GET'])
def get_type_count():
    all_type_count=AccountTypes.query.all()
    result =type_counts_schema.dump(all_type_count)
    return jsonify(result)


#leer un solo type_count GET * ID #######
@app.route('/get_type_count/<id>',methods = ['GET'])
def get_type_count_x_id(id):
    one_type_count = AccountTypes.query.get(id)
    return type_count_schema.jsonify(one_type_count)

#ingresar un nuevo banco### POST
@app.route('/insert_type_count', methods = ['POST'])
def add_type_count():  
    description =request.json['description']
    type_count = AccountTypes(description)
    db.session.add(type_count)
    db.session.commit()
    return type_count_schema.jsonify(type_count)

#update tipo cuenta
@app.route('/update_type_count/<id>', methods=['PUT'])
def update_type_count(id):
    upd_type_count = AccountTypes.query.get(id)
    description = request.json['description']
    upd_type_count.description = description
    db.session.commit()
    return bank_schema.jsonify(upd_type_count)

#delete
@app.route('/delete_type_count/<id>', methods=['DELETE'])
def delete_type_count(id):
    del_type_count = AccountTypes.query.get(id)
    db.session.delete(del_type_count)
    db.session.commit()
    return jsonify({'mensaje':"Tipo Cuenta Eliminado"})

    

if __name__== "__main__":
    app.run(debug=True)