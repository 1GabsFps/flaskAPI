from flask import Flask, jsonify, request
import os
import csv

app = Flask(__name__)

arquivo_csv = "./dados.csv"

if not os.path.isfile(arquivo_csv):
    with open(arquivo_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Nome", "idade", "Cidade"])

def escrever_csv():
    with open(arquivo_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Nome", "idade", "Cidade"])
        for user in userList:
            writer.writerow([user["ID"], user["Nome"], user["idade"], user["Cidade"]])

def ler_csv():
    with open(arquivo_csv, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader) 
        userList = []
        for row in reader:
            if len(row) >= 4:  
                userList.append({
                    "ID": int(row[0]),
                    "Nome": row[1],
                    "idade": row[2],
                    "Cidade": row[3]
                })
    return userList

userList = ler_csv()


@app.route('/', methods=['GET'])
def index():
    ler_csv()
    return userList

@app.route('/user', methods=['POST'])
def login():
    item = request.json
    userList.append(item)
    escrever_csv()
    return userList

@app.route('/update/<int:key_update>', methods=['PUT'])
def update_user(key_update):
    users = userList
    ler_csv()
    for user in users:
        if user["ID"] == key_update:
            user_data = request.get_json()
            user.update(user_data)
            escrever_csv()
            return jsonify(user), 200  
    return jsonify({"erro": "Usuario Não encontrado"}), 404

@app.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    ler_csv()
    users = userList
    for i, user in enumerate(users):
        if user["ID"] == user_id:
            users.pop(i)
            escrever_csv()
            return jsonify({"sucesso": "Usuario deletado"}), 200
    return jsonify({"erro": "Usuario Não encontrado"}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)