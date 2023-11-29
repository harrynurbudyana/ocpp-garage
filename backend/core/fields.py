from enum import Enum


class TransactionStatus(str, Enum):
    in_progress = "in_progress"
    pending = "pending"
    completed = "completed"
    faulted = "faulted"


class NotificationType(str, Enum):
    new_user_invited = "new_user_invited"
    friendly_reminder = "friendly_reminder"


class Role(str, Enum):
    resident = "resident"
    employee = "employee"
