from backend.tools.authorization import (
    check_customer_authorization
)


print("========================================")
print("AUTHORIZATION TEST")
print("========================================")


# -----------------------------------------
# Authorized request
# -----------------------------------------

print("\n1. Authorized request:")

result = check_customer_authorization(
    "CUS-001",
    "ORD-1005"
)

print(result)


# -----------------------------------------
# Unauthorized request
# -----------------------------------------

print("\n2. Unauthorized request:")

result = check_customer_authorization(
    "CUS-002",
    "ORD-1005"
)

print(result)


# -----------------------------------------
# Unknown order
# -----------------------------------------

print("\n3. Unknown order:")

result = check_customer_authorization(
    "CUS-001",
    "ORD-9999"
)

print(result)