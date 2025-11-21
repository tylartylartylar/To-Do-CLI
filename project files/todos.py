from datetime import datetime
import uuid
class ToDo:
    def __init__(self, name, description, complete, dueDate,completedDate=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.complete = complete
        self.dueDate = dueDate
        self.completedDate = completedDate
    