# To-Do CLI

A simple, local command-line ToDo app written in Python using only the standard library.

This tool is not very useful (yet), but it's part of an ongoing effort to build better CLI tools, practice clean Python structure, and learn Git/GitHub workflows.

---

## ✅ Current Features

- Add new todos via the command line
- List all active todos
- Mark todos as complete (and remove them)
- Saves data to a local `todos.json` file
- Runs entirely with built-in Python modules (`sys`, `uuid`, `json`, `datetime`)

---

## 🚧 Limitations / TODO

- No date validation for due dates (they're stored as strings)
- No filtering or sorting
- Requires typing/pasting a long UUID (for now)
- No error handling for malformed JSON or invalid input
- Only usable from the command line

---

## 🚀 Getting Started

Make sure you have Python 3 installed.

```bash
# Clone the repo
git clone https://github.com/tylartylartylar/To-Do-CLI.git
cd To-Do-CLI/project\ files/

# Run a command
python main.py add
python main.py list
python main.py complete
