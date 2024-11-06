import json
import os

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def __repr__(self):
        return f'User({self.username})'

class Task:
    def __init__(self, title, description, completed=False):
        self.title = title
        self.description = description
        self.completed = completed

    def mark_completed(self):
        self.completed = True

    def __repr__(self):
        return f'Task({self.title}, Completed: {self.completed})'

class TaskManager:
    def __init__(self):
        self.users = {}
        self.load_users()

    def load_users(self):
        if os.path.exists('users.json'):
            with open('users.json', 'r') as file:
                self.users = json.load(file)
                for username, user_data in self.users.items():
                    user = User(username, user_data['password'])
                    user.tasks = [Task(**task) for task in user_data['tasks']]
                    self.users[username] = user

    def save_users(self):
        with open('users.json', 'w') as file:
            json.dump({username: {'password': user.password, 'tasks': [task.__dict__ for task in user.tasks]}
                        for username, user in self.users.items()}, file)

    def register_user(self, username, password):
        if username in self.users:
            raise Exception("Username already exists.")
        self.users[username] = User(username, password)
        self.save_users()

    def authenticate_user(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            return user
        raise Exception("Invalid username or password.")

def main():
    manager = TaskManager()

    while True:
        action = input("Do you want to (register/login)? ").strip().lower()
        
        if action == 'register':
            username = input("Enter username: ")
            password = input("Enter password: ")
            try:
                manager.register_user(username, password)
                print("User registered successfully.")
            except Exception as e:
                print(e)
        
        elif action == 'login':
            username = input("Enter username: ")
            password = input("Enter password: ")
            try:
                user = manager.authenticate_user(username, password)
                print(f"Welcome {user.username}!")
                
                while True:
                    task_action = input("Do you want to (add/remove/view/quit)? ").strip().lower()
                    
                    if task_action == 'add':
                        title = input("Enter task title: ")
                        description = input("Enter task description: ")
                        user.add_task(Task(title, description))
                        manager.save_users()
                        print("Task added.")
                    
                    elif task_action == 'remove':
                        title = input("Enter task title to remove: ")
                        task_to_remove = next((task for task in user.tasks if task.title == title), None)
                        if task_to_remove:
                            user.remove_task(task_to_remove)
                            manager.save_users()
                            print("Task removed.")
                        else:
                            print("Task not found.")
                    
                    elif task_action == 'view':
                        if user.tasks:
                            for task in user.tasks:
                                print(task)
                        else:
                            print("No tasks available.")
                    
                    elif task_action == 'quit':
                        break
                    else:
                        print("Invalid action.")
        
        else:
            print("Invalid action.")

if __name__ == '__main__':
    main()
