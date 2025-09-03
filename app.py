from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

todos = [
   
]

@app.route('/')
def home():
    return jsonify({'message': 'Todo Backend Server is running!', 'task_count': len(todos)})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(todos)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    text = data.get('text', '').strip()
    
    if not text:
        return jsonify({'error': 'Task text is required'}), 400
    
    current_time = datetime.utcnow().isoformat() + 'Z'
    
    new_todo = {
        'id': str(uuid.uuid4()),
        'text': text,
        'created_at': current_time,
        'updated_at': current_time
    }
    
    todos.append(new_todo)
    return jsonify(new_todo), 201

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    for i, todo in enumerate(todos):
        if todo['id'] == task_id:
            del todos[i]
            return '', 204
    
    return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    text = data.get('text', '').strip()
    
    if not text:
        return jsonify({'error': 'Task text is required'}), 400
    
    for todo in todos:
        if todo['id'] == task_id:
            todo['text'] = text
            todo['updated_at'] = datetime.utcnow().isoformat() + 'Z'
            return jsonify(todo)
    
    return jsonify({'error': 'Task not found'}), 404

@app.route('/health')
def health():
    return jsonify({'status': 'OK', 'message': 'Todo backend is running', 'task_count': len(todos)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=True) 