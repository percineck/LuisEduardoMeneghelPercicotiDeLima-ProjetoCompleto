from flask import Flask,request,render_template,jsonify,session#biblioteca flash
from flask_cors import CORS#liberar acesso as requisições por metodos put post get e delete
import json#manipulação de formato json
import random#reliza sorteios de números
#import mysql.connector#conecta ao banco de dados
import sqlite3

app = Flask(__name__)#criar o objeto da aplicação Flask


CORS(app)#libera acesso as requisições por metodos put post get e delete


db = sqlite3.connect('agenda.db')
cursor = db.cursor()            
cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups_contacts (
            id INTEGER PRIMARY KEY,
            name VARCHAR(50)
        );

''')
cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY,
            id_group INTEGER,
            name VARCHAR(50),
            phone VARCHAR(13),
            FOREIGN KEY (id_group) REFERENCES groups_contacts(id)
        );
''')

# Commit para salvar as alterações
db.commit()#é o classe responsavel por manipular os dados 
#em SQL


@app.route('/contact')
def listar():
    try:
        global cursor#variavel global do cursor
        cursor.execute("SELECT * FROM contacts order by id desc")# seleção de todos os dados
        contacts = cursor.fetchall()#listagem dos dados
        return jsonify(contacts)#resposta dos dados
    except Exception as error:
        return jsonify({"error":  type(error).__name__}), 400

@app.route('/contact/<int:id>')
def listarPorId(id):
    try:
        global cursor
        cursor.execute("SELECT * FROM contacts ORDER BY id DESC LIMIT 1")#seleção de apenas um contact
        contact = cursor.fetchone()
        return jsonify(contact)
    except Exception as error:
        return jsonify({"error":  type(error).__name__}), 400

    

@app.route('/contact',methods=['POST'])
def criar():
    try:
        global db, cursor
        data = request.get_json()
        if data:
            cursor.execute("INSERT INTO contacts (id_group,name, phone) VALUES (%s, %s, %s)", (data.get('id_group'),data.get('name'), data.get('phone')))
            #cria um novo contact
            db.commit()
            cursor.execute("SELECT * FROM contacts  WHERE id = %s", (id,))#seleção de apenas um contact
            contact = cursor.fetchone()
            return jsonify(contact)
        else:
            return jsonify({"error": "Dados inválidos"}), 400
    except Exception as error:
        return jsonify({"error":  type(error).__name__}), 400
    
    
@app.route('/contacts/<int:id>',methods=['PUT'])
def alterar(id):
    try:
        global db, cursor
        data = request.get_json()
        if data:
            cursor.execute("UPDATE contacts SET id_group=%s,name=%s, phone=%s WHERE id=%s", (data.get('id_group'),data.get('name'), data.get('phone'), id))
            #atualizar um novo contact
            db.commit()
            cursor.execute("SELECT * FROM contacts  WHERE id = %s", (id,))#seleção de apenas um contact
            contact = cursor.fetchone()
            return jsonify(contact)
        else:
            return jsonify({"error": "Dados inválidos"}), 400
    except Exception as error:
        return jsonify({"error":  type(error).__name__}), 400



@app.route('/contact/<int:id>',methods=['DELETE'])
def deletar(id):
    try:
        global db, cursor
        cursor.execute("DELETE FROM contacts WHERE id = %s", (id,))
        #excluir um novo contact
        db.commit()
        cursor.execute("SELECT * FROM contacts  WHERE id = %s", (id,))#seleção de apenas um contact
        contact = cursor.fetchone()
        return jsonify(contact)
    except Exception as error:
        return jsonify({"error":  type(error).__name__}), 400

#backend groups
#backend
@app.route('/group')
def listar_group():
    try:
        global cursor#variavel global do cursor
        cursor.execute("SELECT * FROM groups_contacts ")# seleção de todos os dados
        groups = cursor.fetchall()#listagem dos dados
        return jsonify("oi")#resposta dos dados
    except Exception as error:
        print(f"Erro: {error}")
        return jsonify({"error":  type(error).__name__}), 400
    
@app.route('/group/<int:id>')
def listar_groupPorId(id):
    try:
        global cursor
        cursor.execute("SELECT id, name FROM groups_contacts WHERE id = %s", (id,))#seleção de apenas um contact
        group = cursor.fetchone()
        return jsonify(group)
    except Exception as error:
        return jsonify({"error":  type(error).__name__}), 400

@app.route('/group',methods=['POST'])
def criar_group():
    try:
        global db, cursor
        data = request.get_json()
        if data:
            cursor.execute("INSERT INTO groups_contacts (name) VALUES (%s)", (data.get('name'),))
            #cria um novo contact
            db.commit()
            cursor.execute("SELECT * FROM groups_contacts ORDER BY id DESC LIMIT 1")
            group = cursor.fetchone()
            return jsonify(group)
        else:
            return jsonify({"error": "Dados inválidos"}), 400
    except Exception as error:
        return jsonify({"error":  type(error).__name__}), 400
    
@app.route('/group/<int:id>',methods=['PUT'])
def alterar_group(id):
    try:
        global db, cursor
        data = request.get_json()
        if data:
            cursor.execute("UPDATE groups_contacts SET name=%s WHERE id=%s", (data.get('name'), id))
            #atualizar um novo contact
            db.commit()
            cursor.execute("SELECT * FROM groups_contacts WHERE id = %s", (id,))#seleção de apenas um contact
            group = cursor.fetchone()
            return jsonify(group)
        else:
            return jsonify({"error": "Dados inválidos"}), 400
    except Exception as error:
        return jsonify({"error":  type(error).__name__}), 400

def count_contacts_group(id_group):
    try:
        global cursor  # variavel global do cursor
        cursor.execute("SELECT g.id, g.name, (SELECT COUNT(c.id) FROM contacts c WHERE c.id_group=g.id) AS filhos FROM groups_contacts g WHERE g.id = %s", (id_group,))
        group = cursor.fetchone()
        return group["filhos"]
    except Exception as error:
        return jsonify({"error":  type(error).__name__}), 400

@app.route('/group/<int:id>',methods=['DELETE'])
def deletar_group(id):
    try:
        global db, cursor
        if(count_contacts_group(id)==0):
            cursor.execute("DELETE FROM groups_contacts WHERE id = %s", (id,))
            #excluir um novo contact
            db.commit()
            cursor.execute("SELECT * FROM groups_contacts WHERE id = %s", (id,))#seleção de apenas um contact
            group = cursor.fetchone()
            return jsonify(group)
        else:
            return jsonify({"success": "Grupo não pode excluído por que possui contacts"})
    except Exception as error:
        return jsonify({"error":  type(error).__name__}), 400

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)