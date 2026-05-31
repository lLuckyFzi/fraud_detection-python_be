import enum

# Define enumerations for various fields
class RiskProfile(enum.Enum):
    Low = 'Low'
    Medium = 'Medium'
    High = 'High'

class AccountType(enum.Enum):
    Savings = 'Savings'
    Checking = 'Checking'
    Business = 'Business'

class AccountStatus(enum.Enum):
    Active = 'Active'
    Frozen = 'Frozen'
    Suspended = 'Suspended'

class TransactionType(enum.Enum):
    Transfer = 'Transfer'
    Withdrawal = 'Withdrawal'
    Online_Purchase = 'Online_Purchase'

class TransactionStatus(enum.Enum):
    Success = "Success"
    Failed = "Failed"
    Blocked = "Blocked"

class AlertStatus(enum.Enum):
    Open = "Open"
    Under_Review = "Under_Review"
    Resolved_Fraud = "Resolved_Fraud"
    Resolved_False_Positive = "Resolved_False_Positive"