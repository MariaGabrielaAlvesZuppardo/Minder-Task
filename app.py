from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
tasks = []
task_id_counter = 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    new_task = {
        'id': task_id_counter,
        'title': request.form['title'],
        'completed': False
    }
    tasks.append(new_task)
    task_id_counter += 1
    return jsonify(new_task)

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['title'] = request.form['title']
            task['completed'] = request.form.get('completed', False)
            return jsonify(task)
    return jsonify({'error': 'Task not found'})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            return jsonify({'message': 'Task deleted'})
    return jsonify({'error': 'Task not found'})

@app.route('/tasks/all', methods=['DELETE'])
def delete_all_tasks():
    global tasks
    tasks = []
    return jsonify({'message': 'All tasks deleted'})

if __name__ == '__main__':
    app.run()
