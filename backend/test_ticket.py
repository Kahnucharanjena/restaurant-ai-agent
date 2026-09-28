
from tools.support_ticket import create_support_ticket


result = create_support_ticket(
    customer_id="CUS-001",
    category="Payment",
    priority="High",
    description="Payment was deducted but the order failed."
)

print(result)