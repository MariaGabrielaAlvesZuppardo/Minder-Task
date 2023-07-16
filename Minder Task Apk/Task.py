from plyer import notification
from datetime import datetime

# Nó da lista encadeada
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.top = None

    def is_empty(self):
        return self.top is None

    def push(self, data):
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.is_empty():
            raise Exception("A pilha está vazia.")
        data = self.top.data
        self.top = self.top.next
        return data

# Representação de uma pilha
class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    # Verificando se a pilha está vazia
    def is_empty(self):
        return self.front is None

    def enqueue(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.front = new_node
        else:
            self.rear.next = new_node
        self.rear = new_node

    def dequeue(self):
        if self.is_empty():
            raise Exception("A fila está vazia.")
        data = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        return data

class Task:
    def __init__(self, title, description, creation_date, priority):
        self.title = title
        self.description = description
        self.creation_date = creation_date
        self.priority = priority
        self.next = None

    # Para adicionar uma atividade
    def add_task(self, head, undo_stack, redo_stack):
        title = input("Digite o título da tarefa: ")
        description = input("Digite a descrição da tarefa: ")
        creation_date = input("Digite a data de criação da tarefa: ")
        priority = input("Digite a prioridade da tarefa: ")

        new_task = Task(title, description, creation_date, priority)

        if head is None:
            head = new_task
        else:
            current_task = head
            while current_task.next is not None:
                current_task = current_task.next
            current_task.next = new_task

        choice = input("Deseja adicionar uma notificação para essa tarefa? (S/N): ")

        if choice.lower() == "s":
            notification_date = input("Digite a data da notificação (formato: DD/MM/AAAA): ")
            notification_time = input("Digite a hora da notificação (formato: HH:MM): ")
            notification_datetime = f"{notification_date} {notification_time}"
            self.add_notification(new_task, notification_datetime)

        undo_stack.push(("add", new_task))
        redo_stack = Stack()

        print("Tarefa adicionada com sucesso!")

        return head
    
    # Função para remover tarefa
    def remove_task(self, head, title, undo_stack, redo_stack):
        if head is None:
            print("Lista de tarefas vazia.")
            return head

        if head.title == title:
            removed_task = head
            head = head.next
            removed_task.next = None

            undo_stack.push(("remove", removed_task))
            redo_stack = Stack()

            print("Tarefa removida com sucesso.")
            return head

        current_task = head
        previous_task = None

        while current_task is not None:
            if current_task.title == title:
                removed_task = current_task
                previous_task.next = current_task.next
                removed_task.next = None

                undo_stack.push(("remove", removed_task))
                redo_stack = Stack()

                print("Tarefa removida com sucesso.")
                return head

            previous_task = current_task
            current_task = current_task.next

        print("Tarefa não encontrada.")
        return head
    
    # Função para atualizar tarefa
    def update_task(self, head, title, undo_stack, redo_stack):
        if head is None:
            print("Lista de tarefas vazia.")
            return head

        current_task = head

        while current_task is not None:
            if current_task.title == title:
                print("Escolha quais informações deseja atualizar:")
                print("1. Título")
                print("2. Descrição")
                print("3. Data de Criação")
                print("4. Prioridade")
                print("5. Todas as informações")

                choice = input("Escolha uma opção: ")

                if choice == "1":
                    new_title = input("Digite o novo título da tarefa: ")
                    undo_stack.push(("update", current_task.title, current_task.title))
                    current_task.title = new_title
                elif choice == "2":
                    new_description = input("Digite a nova descrição da tarefa: ")
                    undo_stack.push(("update", current_task.title, current_task.description))
                    current_task.description = new_description
                elif choice == "3":
                    new_creation_date = input("Digite a nova data de criação da tarefa: ")
                    undo_stack.push(("update", current_task.title, current_task.creation_date))
                    current_task.creation_date = new_creation_date
                elif choice == "4":
                    new_priority = input("Digite a nova prioridade da tarefa: ")
                    undo_stack.push(("update", current_task.title, current_task.priority))
                    current_task.priority = new_priority
                elif choice == "5":
                    new_title = input("Digite o novo título da tarefa: ")
                    new_description = input("Digite a nova descrição da tarefa: ")
                    new_creation_date = input("Digite a nova data de criação da tarefa: ")
                    new_priority = input("Digite a nova prioridade da tarefa: ")
                    undo_stack.push(("update", current_task.title, (current_task.title, current_task.description, current_task.creation_date, current_task.priority)))
                    current_task.title = new_title
                    current_task.description = new_description
                    current_task.creation_date = new_creation_date
                    current_task.priority = new_priority
                else:
                    print("Opção inválida. Nenhuma informação será atualizada.")

                redo_stack = Stack()

                print("Tarefa atualizada com sucesso.")
                return head

            current_task = current_task.next

        print("Tarefa não encontrada.")
        return head

    def undo_action(self, head, undo_stack, redo_stack):
        if undo_stack.is_empty():
            print("Não há ações para desfazer.")
            return head

        last_action = undo_stack.pop()

        if last_action[0] == "add":
            task = last_action[1]
            if head == task:
                head = head.next
            else:
                current_task = head
                previous_task = None
                while current_task is not None:
                    if current_task == task:
                        previous_task.next = current_task.next
                        current_task.next = None
                        break
                    previous_task = current_task
                    current_task = current_task.next

        elif last_action[0] == "remove":
            task = last_action[1]
            if head is None:
                head = task
            else:
                current_task = head
                while current_task.next is not None:
                    current_task = current_task.next
                current_task.next = task

        elif last_action[0] == "update":
            title = last_action[1]
            previous_value = last_action[2]
            current_task = head
            while current_task is not None:
                if current_task.title == title:
                    if isinstance(previous_value, tuple):
                        current_task.title = previous_value[0]
                        current_task.description = previous_value[1]
                        current_task.creation_date = previous_value[2]
                        current_task.priority = previous_value[3]
                    else:
                        if previous_value == current_task.title:
                            current_task.title = title
                        elif previous_value == current_task.description:
                            current_task.description = title
                        elif previous_value == current_task.creation_date:
                            current_task.creation_date = title
                        elif previous_value == current_task.priority:
                            current_task.priority = title
                    break
                current_task = current_task.next

        redo_stack.push(last_action)
        print("Ação desfeita com sucesso.")

        return head

    def redo_action(self, head, undo_stack, redo_stack):
        if redo_stack.is_empty():
            print("Não há ações para refazer.")
            return head

        last_action = redo_stack.pop()

        if last_action[0] == "add":
            task = last_action[1]
            if head is None:
                head = task
            else:
                current_task = head
                while current_task.next is not None:
                    current_task = current_task.next
                current_task.next = task

        elif last_action[0] == "remove":
            task = last_action[1]
            if head == task:
                head = head.next
            else:
                current_task = head
                previous_task = None
                while current_task is not None:
                    if current_task == task:
                        previous_task.next = current_task.next
                        current_task.next = None
                        break
                    previous_task = current_task
                    current_task = current_task.next

        elif last_action[0] == "update":
            title = last_action[1]
            new_value = last_action[2]
            current_task = head
            while current_task is not None:
                if current_task.title == title:
                    if isinstance(new_value, tuple):
                        current_task.title = new_value[0]
                        current_task.description = new_value[1]
                        current_task.creation_date = new_value[2]
                        current_task.priority = new_value[3]
                    else:
                        if new_value == current_task.title:
                            current_task.title = title
                        elif new_value == current_task.description:
                            current_task.description = title
                        elif new_value == current_task.creation_date:
                            current_task.creation_date = title
                        elif new_value == current_task.priority:
                            current_task.priority = title
                    break
                current_task = current_task.next

        undo_stack.push(last_action)
        print("Ação refazida com sucesso.")

        return head

    def add_notification(self, task, notification_datetime):
        notification_queue.enqueue((task, notification_datetime))
        print("Notificação adicionada com sucesso.")

    def check_notifications(self):
        current_datetime = datetime.now()
        while not notification_queue.is_empty():
            task, notification_datetime = notification_queue.front.data
            if datetime.strptime(notification_datetime, "%d/%m/%Y %H:%M") <= current_datetime:
                self.notify_task(task)
                notification_queue.dequeue()
            else:
                break

    def notify_task(self, task):
        notification_title = "Lembrete de Tarefa"
        notification_message = f"Tarefa: {task.title}\nDescrição: {task.description}"
        notification.notify(title=notification_title, message=notification_message, timeout=10)

    def view_tasks(self, head):
        if head is None:
            print("Lista de tarefas vazia.")
            return

        current_task = head
        count = 1

        print("Tarefas cadastradas:")
        while current_task is not None:
            print(f"Tarefa {count}:")
            print(f"Título: {current_task.title}")
            print(f"Descrição: {current_task.description}")
            print(f"Data de Criação: {current_task.creation_date}")
            print(f"Prioridade: {current_task.priority}")
            print()
            current_task = current_task.next
            count += 1

    def search_task(self, head, title):
        current_task = head

        while current_task is not None:
            if current_task.title == title:
                return current_task
            current_task = current_task.next

        return None

    def sort_tasks(self, head):
        task_list = []
        current_task = head

        while current_task is not None:
            task_list.append(current_task)
            current_task = current_task.next

        sorted_task_list = sorted(task_list, key=lambda x: x.priority)

        new_head = None
        current_task = None

        for task in sorted_task_list:
            if new_head is None:
                new_head = task
                current_task = task
            else:
                current_task.next = task
                current_task = task

        if current_task is not None:
            current_task.next = None

        return new_head

head = None
undo_stack = Stack()
redo_stack = Stack()
notification_queue = Queue()

task_manager = Task(None, None, None, None)

while True:
    print("1. Adicionar tarefa")
    print("2. Remover tarefa")
    print("3. Atualizar tarefa")
    print("4. Desfazer ação")
    print("5. Refazer ação")
    print("6. Visualizar tarefas cadastradas")
    print("7. Sair")

    choice = input("Escolha uma opção: ")

    if choice == "1":
        head = task_manager.add_task(head, undo_stack, redo_stack)
    elif choice == "2":
        title = input("Digite o título da tarefa a ser removida: ")
        head = task_manager.remove_task(head, title, undo_stack, redo_stack)
    elif choice == "3":
        title = input("Digite o título da tarefa a ser atualizada: ")
        head = task_manager.update_task(head, title, undo_stack, redo_stack)
    elif choice == "4":
        head = task_manager.undo_action(head, undo_stack, redo_stack)
    elif choice == "5":
        head = task_manager.redo_action(head, undo_stack, redo_stack)
    elif choice == "6":
        task_manager.view_tasks(head)
    elif choice == "7":
        break
    else:
        print("Opção inválida. Tente novamente.")

    if head is None:
        print("A lista de tarefas está vazia. Por favor, adicione uma tarefa.")
        head = task_manager.add_task(head, undo_stack, redo_stack)
