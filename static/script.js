const form = document.getElementById('create-task-form');
const taskList = document.getElementById('task-list');

form.addEventListener('submit', (e) => {
    e.preventDefault();
    const input = form.querySelector('input[name="title"]');
    const title = input.value;
    if (title.trim() !== '') {
        createTask(title);
        input.value = '';
    }
});

function createTask(title) {
    fetch('/tasks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            title
        })
    })
    .then(response => response.json())
    .then(task => {
        renderTask(task);
    });
}

function updateTask(taskId, title, completed) {
    fetch(`/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            title,
            completed
        })
    })
    .then(response => response.json())
    .then(task => {
        const taskElement = document.getElementById(`task-${taskId}`);
        if (taskElement) {
            taskElement.querySelector('.task-title').textContent = task.title;
            taskElement.classList.toggle('completed', task.completed);
        }
    });
}

function deleteTask(taskId) {
    fetch(`/tasks/${taskId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        const taskElement = document.getElementById(`task-${taskId}`);
        if (taskElement) {
            taskElement.remove();
        }
    });
}

function renderTask(task) {
    const taskElement = document.createElement('li');
    taskElement.id = `task-${task.id}`;
    taskElement.className = task.completed ? 'completed' : '';

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.checked = task.completed;
    checkbox.addEventListener('change', (e) => {
        updateTask(task.id, task.title, e.target.checked);
    });
    taskElement.appendChild(checkbox);

    const titleElement = document.createElement('span');
    titleElement.className = 'task-title';
    titleElement.textContent = task.title;
    taskElement.appendChild(titleElement);

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Delete';
    deleteButton.addEventListener('click', () => {
        deleteTask(task.id);
    });
    taskElement.appendChild(deleteButton);

    taskList.appendChild(taskElement);
}

function renderTasks(tasks) {
    taskList.innerHTML = '';
    for (const task of tasks) {
        renderTask(task);
    }
}

