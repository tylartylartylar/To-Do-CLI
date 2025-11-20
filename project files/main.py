from todos import ToDo
from datetime import datetime
import json
import sys


# -----------------------------
# 🔁 Utility Functions
# -----------------------------

def todo_to_dict(todo):
    """
    Converts a ToDo object into a plain dictionary.
    This is used before serializing the data to JSON.
    """
    return {
        "id": todo.id,
        "name": todo.name,
        "description": todo.description,
        "complete": todo.complete,
        "dueDate": todo.dueDate
    }

def convertToJSON(todoDict):
    """
    Converts the entire todo dictionary into a JSON-formatted string.
    Assumes all ToDos have been converted to dictionaries.
    """
    converted = {
        str(id): todo_to_dict(todoDict[id])
        for id in todoDict
    }
    return json.dumps(converted, indent=2)

def save_todos(todoDict):
    """
    Saves the current state of the todo list to a JSON file.
    """
    json_string = convertToJSON(todoDict)
    with open("todos.json", "w") as f:
        f.write(json_string)

def load_todos():
    """
    Loads the todos from the JSON file and returns them as raw data.
    Will raise FileNotFoundError if the file does not exist.
    """
    with open("todos.json", "r") as f:
        data = json.load(f)
    return data


# -----------------------------
# 📋 Core ToDo Functionality
# -----------------------------

def add_todo(todoList):
    """
    Prompts the user to add a new todo.
    Creates a new ToDo object and saves the updated list.
    """
    name = input("Please enter the name of your ToDo: ")
    desc = input("Give your todo a description: ")
    dueDate = input("Please enter a due date with the following format: YYYY-MM-DD: ")

    new_todo = ToDo(name, desc, False, dueDate)
    todoList[new_todo.id] = new_todo

    save_todos(todoList)

    print(f"\nNew entry added!\n\nName: {new_todo.name}\nDescription: {new_todo.description}\nDue Date: {new_todo.dueDate}")
    return todoList

def list_todos(todoList):
    """
    Displays all todos in the list with their UUID, name, due date, and completion status.
    """
    print("\nToDo List:")
    for id, todo in todoList.items():
        print(f"[{id}] {todo.name} - Description: {todo.description}\nDue: {todo.dueDate} - Completed: {todo.complete}")

def complete_todo(todoList):
    """
    Prompts the user to complete a todo by UUID.
    Marks it complete and removes it from the list.
    """
    list_todos(todoList)
    completedToDo = input("\nPlease enter the UUID of the ToDo you would like to complete: ")

    if completedToDo in todoList:
        todoList[completedToDo].complete = True
        del todoList[completedToDo]
        save_todos(todoList)

        print("\nToDo marked as complete and removed.")
        list_todos(todoList)
    else:
        print("\nInvalid UUID entered. No changes made.")

    return todoList


# -----------------------------
# 🚀 Entry Point
# -----------------------------

def main():
    """
    Loads existing todos from file (if any).
    If no file exists, starts with an empty list.
    Calls the desired function from args using sys.argv.
    """
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        print("Usage: python3 main.py <action> \'add\', \'complete\', \'list\' can be used.")
        sys.exit(1)
    
    try:
        raw_data = load_todos()
        todoList = {
            id: ToDo(
                todo_data["name"],
                todo_data["description"],
                todo_data["complete"],
                todo_data["dueDate"]
            )
            for id, todo_data in raw_data.items()
        }
    except FileNotFoundError:
        todoList = {}

    command = sys.argv[1]

    if command == "add":
        add_todo(todoList)
        sys.exit(0)
    
    elif command == "list":
        list_todos(todoList)
        sys.exit(0)

    elif command == "complete":
        complete_todo(todoList)
        sys.exit(0)
    else:
        print(f"unknown command: {command}")

if __name__ == '__main__':
    main()
