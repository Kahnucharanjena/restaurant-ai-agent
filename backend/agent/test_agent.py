from backend.agent.agent import execute_tool, get_agent_info


print("================================")
print("AGENT INFORMATION")
print("================================")

print(get_agent_info())


print("\n================================")
print("TESTING ORDER STATUS TOOL")
print("================================")

result = execute_tool(
    "get_order_status",
    {
        "order_id": "ORD-1005"
    }
)

print(result)


print("\n================================")
print("TESTING ORDER DETAILS TOOL")
print("================================")

result = execute_tool(
    "get_order_details",
    {
        "order_id": "ORD-1005"
    }
)

print(result)


print("\n================================")
print("TESTING INVALID TOOL")
print("================================")

result = execute_tool(
    "delete_customer_data",
    {
        "customer_id": "CUS-001"
    }
)

print(result)


print("\n================================")
print("TESTING KNOWLEDGE BASE TOOL")
print("================================")

result = execute_tool(
    "search_knowledge_base",
    {
        "query": "Can I cancel my order?"
    }
)

print(result)