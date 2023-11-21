from enum import Enum


class TransactionStatus(str, Enum):
    in_progress = "in_progress"
    pending = "pending"
    completed = "completed"
    faulted = "faulted"


class NotificationType(str, Enum):
    new_operator_invited = "new_operator_invited"
    friendly_reminder = "friendly_reminder"
