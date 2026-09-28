from backend.automation.complaint import process_complaint


print("========================================")
print("COMPLAINT AUTOMATION TEST")
print("========================================")


message = (
    "My payment was deducted but my order failed. "
    "Please help me immediately."
)


result = process_complaint(
    customer_id="CUS-001",
    message=message
)


print("\nCustomer complaint:")
print(message)

print("\nAutomation result:")
print(result)