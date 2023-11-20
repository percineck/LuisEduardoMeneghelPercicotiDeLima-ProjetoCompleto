from flask import Flask, jsonify,request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def get_db():
    # Substitua 'agenda.db' pelo nome do seu banco de dados SQLite
    db = sqlite3.connect('agenda.db')
    return db
@app.route('/')
def criarBanco():
    try:
        
    
            db = get_db()
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
            db.commit()
        

            db.close()

            return jsonify("banco de dados criado com sucesso"), 201  # Código 201 indica "Created"
    

    except Exception as error:
        print(f"Erro: {error}")
        return jsonify({"error": str(error)}), 400
    

def criar_contato(data):
    try:
        if data and 'id_group' in data and 'name' in data and 'phone' in data:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO contacts (id_group, name, phone) VALUES (?, ?, ?)",
                        (data['id_group'], data['name'], data['phone']))
            db.commit()

            # Recupera o ID do contato recém-criado
            novo_id = cursor.lastrowid

            # Obtém as informações completas do novo contato
            cursor.execute("SELECT * FROM contacts WHERE id = ?", (novo_id,))
            contact = cursor.fetchone()
            db.close()

            if contact:
                formatted_contact = {
                    "id": contact[0],
                    "id_group": contact[1],
                    "name": contact[2],
                    "phone": contact[3]
                }
                return jsonify(formatted_contact)
            else:
                return jsonify({"error": "Contato não encontrado"}), 404
        else:
            return jsonify({"error": "Dados inválidos"}), 400

    except Exception as error:
        print(f"Erro: {error}")
        return jsonify({"error": str(error)}), 400

@app.route('/contact')
def listar_contatos():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT distinct c.id, c.id_group, c.name, c.phone, g.name as group_name FROM contacts c left join groups_contacts g on(g.id=c.id_group) order by c.id desc")
        contacts = cursor.fetchall()
        db.close()

        formatted_contacts = []
        for contact in contacts:
            formatted_contact = {
                "id": contact[0],
                "id_group": contact[1],
                "name": contact[2],
                "phone": contact[3]
            }
            formatted_contacts.append(formatted_contact)

        return jsonify(formatted_contacts)
    except Exception as error:
        print(f"Erro: {error}")
        return jsonify({"error": str(error)}), 400
    

@app.route('/contact', methods=['GET', 'POST'])
def buscar_criar_contato():
    try:
        if request.method == 'POST':
            data = request.get_json()
            return criar_contato(data)  # Adicionei o retorno aqui
        elif request.method == 'GET':
            return listar_contatos()  # Adicionei o retorno aqui
    except Exception as error:
        print(f"Erro: {error}")
        return jsonify({"error": str(error)}), 400
     
def listar_contatosPorId(id):    
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT distinct c.id, c.id_group, c.name, c.phone, g.name as group_name FROM contacts c left join groups_contacts g on(g.id=c.id_group) WHERE c.id = ? order by c.id desc", (id,))
        contact = cursor.fetchone()
        db.close()

        if contact:
            formatted_contact = {
                "id": contact[0],
                "id_group": contact[1],
                "name": contact[2],
                "phone": contact[3]
            }
            return jsonify(formatted_contact)
        else:
            return jsonify({"error": "Contato não encontrado"}), 404
    except Exception as error:
        print(f"Erro: {error}")
        return jsonify({"error": str(error)}), 400

def atualizar_contato(id,data):
    try:
        if data and 'id_group' in data and 'name' in data and 'phone' in data:
            db = get_db()
            cursor = db.cursor()

            # Atualiza as informações do contato
            cursor.execute("UPDATE contacts SET id_group=?, name=?, phone=? WHERE id=?",
                        (data['id_group'], data['name'], data['phone'], id))
            db.commit()

            cursor.execute("SELECT * FROM contacts WHERE id = ?", (id,))
            contact = cursor.fetchone()
            db.close()

            if contact:
                formatted_contact = {
                    "id": contact[0],
                    "id_group": contact[1],
                    "name": contact[2],
                    "phone": contact[3]
                }
                return jsonify(formatted_contact)
            else:
                return jsonify({"error": "Contato não encontrado"}), 404
        
        else:
            return jsonify({"error": "Dados inválidos"}), 400

    except Exception as error:
        print(f"Erro: {error}")
        return jsonify({"error": str(error)}), 400


def deletar_contato(id):
    try:
        db = get_db()
        cursor = db.cursor()

        # Verifica se o contato existe antes de excluí-lo
        cursor.execute("SELECT * FROM contacts WHERE id = ?", (id,))
        contato_existente = cursor.fetchone()

        if contato_existente:
            # Exclui o contato
            cursor.execute("DELETE FROM contacts WHERE id = ?", (id,))
            db.commit()

            db.close()

            return jsonify(contato_existente), 200  # Código 200 indica "OK"
        else:
            return jsonify({"error": "Contato não encontrado"}), 404  # Código 404 indica "Not Found"

    except Exception as error:
        print(f"Erro: {error}")
        return jsonify({"error": str(error)}), 400

@app.route('/contact/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def listar_atualizar_excluir(id):   
    try:
        if request.method == 'GET':
            return listar_contatosPorId(id)  # Adicionei o retorno aqui
        elif request.method == 'PUT':
            data = request.get_json()
            return atualizar_contato(id,data)  # Adicionei o retorno aqui
        elif request.method == 'DELETE':
            data = request.get_json()
            return deletar_contato(id)  # Adicionei o retorno aqui
    except Exception as error:
        print(f"Erro: {error}")
        return jsonify({"error": str(error)}), 400

#-------------------------------------------------------------------------------------------------------------
#######################################   GROUP ##############################################  
def criar_grupo(data):
    try:
        if data and 'name' in data:
            db = get_db()
            cursor = db.cursor()

            # Insere o novo grupo no banco de dados
            cursor.execute("INSERT INTO groups_contacts (name) VALUES (?)", (data['name'],))
            db.commit()

            # Recupera o ID do grupo recém-criado
            novo_id = cursor.lastrowid

            # Obtém as informações completas do novo grupo
            cursor.execute("SELECT * FROM groups_contacts WHERE id = ?", (novo_id,))
            group = cursor.fetchone()
            db.close()

            if group:
                formatted_group = {"id": group[0], "name": group[1]}
                return jsonify(formatted_group)
            else:
                return jsonify({"error": "Grupo não encontrado"}), 404
        else:
            return jsonify({"error": "Dados inválidos"}), 400

    except Exception as error:
        print(f"Erro: {error}")
        return jsonify({"error": str(error)}), 400

def listar_group():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM groups_contacts")
        groups = cursor.fetchall()
        db.close()
        formatted_groups = [{"id": row[0], "name": row[1]} for row in groups]
        return jsonify(formatted_groups)

    except Exception as error:
        print(f"Erro: {error}")
        return jsonify({"error": str(error)}), 400

@app.route('/group', methods=['GET', 'POST'])
def buscar_criar_grupo():
    try:
        if request.method == 'POST':
            data = request.get_json()
            return criar_grupo(data)  # Adicionei o retorno aqui
        elif request.method == 'GET':
            return listar_group()  # Adicionei o retorno aqui
    except Exception as error:
        print(f"Erro: {error}")
        return jsonify({"error": str(error)}), 400
    
def listar_groupPorId(id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM groups_contacts WHERE id = ?", (id,))
        group = cursor.fetchone()
        db.close()
        if group:
            formatted_group = {"id": group[0], "name": group[1]}
            return jsonify(formatted_group)
        else:
            return jsonify({"error": "Grupo não encontrado"}), 404
    except Exception as error:
        print(f"Erro: {error}")
        return jsonify({"error": str(error)}), 400

def atualizar_grupo(id,data):
    try:
        data = request.get_json()
        if data and 'name' in data:
            db = get_db()
            cursor = db.cursor()

            # Verifica se o grupo com o ID fornecido existe
            cursor.execute("SELECT * FROM groups_contacts WHERE id = ?", (id,))
            grupo_existente = cursor.fetchone()

            if not grupo_existente:
                db.close()
                return jsonify({"error": "Grupo não encontrado"}), 404

            # Atualiza o nome do grupo
            cursor.execute("UPDATE groups_contacts SET name = ? WHERE id = ?", (data['name'], id))
            db.commit()

            cursor.execute("SELECT * FROM groups_contacts WHERE id = ?", (id,))
            group = cursor.fetchone()
            db.close()

            if group:
                formatted_group = {"id": group[0], "name": group[1]}
                return jsonify(formatted_group)
            else:
                return jsonify({"error": "Grupo não encontrado"}), 404
        else:
            return jsonify({"error": "Dados inválidos"}), 400

    except Exception as error:
        print(f"Erro: {error}")
        return jsonify({"error": str(error)}), 400

def excluir_grupo(id):
    try:
        db = get_db()
        cursor = db.cursor()

        # Verifica se o grupo com o ID fornecido existe
        cursor.execute("SELECT * FROM groups_contacts WHERE id = ?", (id,))
        grupo_existente = cursor.fetchone()

        if not grupo_existente:
            db.close()
            return jsonify({"error": "Grupo não encontrado"}), 404

        # Verifica se o grupo possui contatos antes de excluir
        cursor.execute("SELECT COUNT(*) FROM contacts WHERE id_group = ?", (id,))
        numero_contatos = cursor.fetchone()[0]

        if numero_contatos > 0:
            db.close()
            return jsonify({"error": "Não é possível excluir o grupo, pois ele possui contatos associados"}), 400

        # Exclui o grupo
        cursor.execute("DELETE FROM groups_contacts WHERE id = ?", (id,))
        db.commit()

        db.close()

        return jsonify({"success": "Grupo excluído com sucesso"})

    except Exception as error:
        print(f"Erro: {error}")
        return jsonify({"error": str(error)}), 400

@app.route('/group/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def listar_atualizar_excluir_group(id):   
    try:
        if request.method == 'GET':
            return listar_groupPorId(id)  # Adicionei o retorno aqui
        elif request.method == 'PUT':
            data = request.get_json()
            return atualizar_grupo(id,data)  # Adicionei o retorno aqui
        elif request.method == 'DELETE':
            data = request.get_json()
            return excluir_grupo(id)  # Adicionei o retorno aqui
    except Exception as error:
        print(f"Erro: {error}")
        return jsonify({"error": str(error)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
