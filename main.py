import sqlite3
import datetime
import logging
import sys
import os
from flask import Flask, jsonify
from flask import request


class Tasks():
    def check_table(self):
        filename = "example.txt"
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                pass
        connection = sqlite3.connect('tasks.db')
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='list_tasks'")
        result = cursor.fetchall()
        if result:
             return
        cursor.execute("CREATE TABLE list_tasks(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT, status TEXT, created_at TEXT, updated_at TEXT)")
        connection.commit()
        connection.close()
        return
    
    def get_tasks(self):
        connection = sqlite3.connect('tasks.db')
        cursor = connection.cursor()
        cursor.execute("SELECT id, title, description, status, created_at, updated_at FROM list_tasks")
        result = cursor.fetchall()
        mas = []
        vr_sl = {}
        for cor in result:
            vr_sl["id"] = cor[0]
            vr_sl["title"] = cor[1]
            vr_sl["description"] = cor[2]
            vr_sl["status"] = cor[3]
            vr_sl["created_at"] = cor[4]
            vr_sl["updated_at"] = cor[5]
            mas.append(vr_sl)
            vr_sl = {}
        connection.commit()
        connection.close()
        return mas

    def get_task(self, id):
        connection = sqlite3.connect('tasks.db')
        cursor = connection.cursor()
        cursor.execute("SELECT id, title, description, status, created_at, updated_at FROM list_tasks WHERE id=?", (id,))
        result = cursor.fetchall()
        mas = []
        vr_sl = {}
        for cor in result:
            vr_sl["id"] = cor[0]
            vr_sl["title"] = cor[1]
            vr_sl["description"] = cor[2]
            vr_sl["status"] = cor[3]
            vr_sl["created_at"] = cor[4]
            vr_sl["updated_at"] = cor[5]
            mas.append(vr_sl)
            vr_sl = {}
        connection.commit()
        connection.close()
        return mas

    def create_task(self, title, description, status):
        connection = sqlite3.connect('tasks.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO list_tasks (title, description, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)", (title, description, status, datetime.date.today(), datetime.date.today()))
        connection.commit()
        connection.close()
        return 

    def edit_task(self, id, rest):
        connection = sqlite3.connect('tasks.db')
        cursor = connection.cursor()
        for name in rest:
            cursor.execute(f"UPDATE list_tasks SET {name} = ? WHERE id = ?", (rest[name], id))
        cursor.execute("UPDATE list_tasks SET updated_at = ? WHERE id = ?", (datetime.date.today(), id))
        connection.commit()
        connection.close()
        return

    def delete_task(self, id):
        connection = sqlite3.connect('tasks.db')
        cursor = connection.cursor() 
        cursor.execute("DELETE FROM list_tasks WHERE id=?", (id,))
        connection.commit()
        connection.close()
        return

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[ logging.FileHandler("TODO_log.log", encoding="utf-8"), logging.StreamHandler()]
)

@app.errorhandler(Exception)
def handle_flask_exception(e):
    logging.exception("Ошибка")
    return jsonify({'error': 'Ошибка'}), 500

@app.route('/tasks', methods=['GET']) # Получение всех заданий
def return_tasks():
    task = Tasks()
    result = task.get_tasks()
    print(result)
    return jsonify({'message': result}), 200

@app.route('/tasks/<int:task_id>', methods=['GET']) # Получение определённого задания
def return_task(task_id):
    task = Tasks()
    result = task.get_task(task_id)
    return jsonify({'message': result}), 200

@app.route('/tasks', methods=['POST']) # Создание нового задания
def create_tasks():
    if not request.json: # Проверка на пустой запрос
        return jsonify({'error': "Пустой запрос"}), 400
    
    if "title" not in request.json: # Проверка title
        return jsonify({'error': "Пустой заголовок задачи"}), 400
    elif len(request.json["title"]) == 0:
        return jsonify({'error': "Пустой заголовок задачи"}), 400
    
    if "description" not in request.json: # Проверка description
        return jsonify({'error': "Пустое описание задачи"}), 400
    elif len(request.json["description"]) == 0:
        return jsonify({'error': "Пустое описание задачи"}), 400
    
    if "status" not in request.json: # Проверка status
        task = Tasks()
        sl = request.json
        status = "pending"
        task.create_task(sl["title"], sl["description"], status)
        return jsonify({'message': "Задание создано"}), 201
    elif request.json["status"] not in ["pending", "in_progress", "completed"]:
        return jsonify({'error': "Не допустимый статус задачи"}), 400
    
    task = Tasks()
    sl = request.json
    task.create_task(sl["title"], sl["description"], sl["status"])
    return jsonify({'message': "Задание создано"}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT']) # Изменение определённого задания
def edit_task(task_id):
    task = Tasks()
    name_list = ["title", "description", "status"]
    sl = {}
    for name in name_list:
        if name in request.json: # Получение данных из запроса
            sl[name] = request.json[name]

        if name == "title" and "title" in request.json and len(request.json["title"]) == 0: # Проверка title
            return jsonify({'error': "Пустой заголовок задачи"}), 400

        if name == "description" and "description" in request.json and len(request.json["description"]) == 0: # Проверка description
            return jsonify({'error': "Пустое описание задачи"}), 400

        if name == "status" and "status" in request.json and request.json["status"] not in ["pending", "in_progress", "completed"]: # Проверка status
            return jsonify({'error': "Не допустимый статус задачи"}), 400
    
    task.edit_task(task_id, sl)
    return jsonify({'message': "Задание изменино"}), 200
 
@app.route('/tasks/<int:task_id>', methods=['DELETE']) # Удаление определённого задания
def delete_task(task_id):
    task = Tasks()
    task.delete_task(task_id)
    return jsonify({'message': "Задание удалено"}), 200

if __name__ == '__main__':
    task = Tasks()
    task.check_table()
    app.run(debug=True)