from todos import ToDo
from datetime import datetime
import json
import sys


# ===========================
# Utility Functions
# ===========================

def serialize_todo(todo):
    """Convert a ToDo object to a dictionary for JSON serialization."""
    return {
        "id": todo.id,
        "name": todo.name,
        "description": todo.description,
        "complete": todo.complete,
        "dueDate": todo.dueDate.isoformat(),
        "completedDate": todo.completedDate.isoformat() if todo.completedDate else None
    }


def todos_to_json(todos):
    """Convert todos dictionary to JSON string."""
    serialized = {
        todo_id: serialize_todo(todo)
        for todo_id, todo in todos.items()
    }
    return json.dumps(serialized, indent=2)


def save_todos(todos):
    """Save todos to JSON file."""
    json_string = todos_to_json(todos)
    with open("todos.json", "w") as f:
        f.write(json_string)


def load_todos():
    """Load todos from JSON file. Raises FileNotFoundError if file doesn't exist."""
    with open("todos.json", "r") as f:
        return json.load(f)


def deserialize_todos(raw_data):
    """Convert raw JSON data back into ToDo objects."""
    return {
        todo_id: ToDo(
            todo_data["name"],
            todo_data["description"],
            todo_data["complete"],
            datetime.fromisoformat(todo_data["dueDate"]),
            datetime.fromisoformat(todo_data.get("completedDate")) if todo_data.get("completedDate") else None
        )
        for todo_id, todo_data in raw_data.items()
    }


# ===========================
# Core ToDo Operations
# ===========================

def add_todo(todos):
    """Prompt user to create and add a new todo."""
    name = input("Enter todo name: ")
    description = input("Enter todo description: ")

    due_date = None
    while due_date is None:
        date_input = input("Enter due date (YYYY-MM-DD): ")
        try:
            due_date = datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError as e:
            print(f"Invalid date format. Example: 2025-12-27\n")

    new_todo = ToDo(name, description, False, due_date)
    todos[new_todo.id] = new_todo
    save_todos(todos)

    print(f"\n✓ Todo added!")
    print(f"  Name: {new_todo.name}")
    print(f"  Description: {new_todo.description}")
    print(f"  Due: {new_todo.dueDate.strftime('%Y-%m-%d')}\n")

def list_todos(todos):
    """Display all todos."""
    if not todos:
        print("\nNo todos found.\n")
        return

    print("\n" + "=" * 60)
    print("Todo List")
    print("=" * 60)
    for todo_id, todo in todos.items():
        status = "✓ Done" if todo.complete else "○ Pending"
        print(f"\n[{todo_id}]")
        print(f"  {todo.name}")
        print(f"  Description: {todo.description}")
        print(f"  Due: {todo.dueDate.strftime('%Y-%m-%d')}")
        print(f"  Status: {status}")
        if todo.completedDate:
            print(f"  Date Completed: {todo.completedDate.strftime('%Y-%m-%d')}")
            
    print("\n" + "=" * 60 + "\n")

def list_completed_todos(todos):
    """Display only completed todos."""
    completed = 0

    if not todos:
        print("\nNo todos found.\n")
        return
    
    print("\n" + "=" * 60)
    print("Completed Todos")
    print("=" * 60)
    for todo_id, todo in todos.items():
        if todo.complete:
                status = "✓ Done" if todo.complete else "○ Pending"
                print(f"\n[{todo_id}]")
                print(f"  {todo.name}")
                print(f"  Description: {todo.description}")
                print(f"  Due: {todo.dueDate.strftime('%Y-%m-%d')}")
                print(f"  Status: {status}")
                print(f"  Date Completed: {todo.completedDate.strftime('%Y-%m-%d')}")
                completed += 1
    if completed == 0:
        print("0 Completed ToDos")
    
    print("\n" + "=" * 60 + "\n")

def list_incomplete_todos(todos):
    """Display only incomplete todos."""

    incomplete = 0

    if not todos:
        print("\nNo todos found.\n")
        return
    
    print("\n" + "=" * 60)
    print("Completed Todos")
    print("=" * 60)
    for todo_id, todo in todos.items():
        if todo.complete == False:
                status = "○ Pending"
                print(f"\n[{todo_id}]")
                print(f"  {todo.name}")
                print(f"  Description: {todo.description}")
                print(f"  Due: {todo.dueDate.strftime('%Y-%m-%d')}")
                print(f"  Status: {status}")
                incomplete += 1
    if incomplete == 0:
        print("0 ToDos")
    
    print("\n" + "=" * 60 + "\n")

def complete_todo(todos):
    """Mark a todo as complete and remove it from the list."""
    list_todos(todos)
    todo_id = input("Enter the ID of the todo to complete: ")

    if todo_id in todos:
        todos[todo_id].complete = True
        todos[todo_id].completedDate = datetime.now()
        save_todos(todos)
        print("✓ Todo marked complete\n")
    else:
        print("Invalid ID. No changes made.\n")


# ===========================
# Main Entry Point
# ===========================

def main():
    """Load todos and execute the requested command."""
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <command>")
        print("Commands: add, list, complete")
        sys.exit(1)

    # Load existing todos or start with empty list
    try:
        raw_data = load_todos()
        todos = deserialize_todos(raw_data)
    except FileNotFoundError:
        todos = {}

    command = sys.argv[1]

    if command == "add":
        add_todo(todos)
    elif command == "list":
        list_todos(todos)
    elif command == "show_completed":
        list_completed_todos(todos)
    elif command == "show_incomplete":
        list_incomplete_todos(todos)
    elif command == "complete":
        complete_todo(todos)
    else:
        print(f"Unknown command: '{command}'")
        print("Available commands: add, list, complete")
        sys.exit(1)


if __name__ == '__main__':
    main()