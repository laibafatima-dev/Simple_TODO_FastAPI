from enum import Enum

class TaskStatus(str, Enum):
    pending = "Pending"
    in_progress = "In-progress"
    completed = "Completed"
