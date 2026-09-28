from backend.agent.tool_schemas import TOOL_SCHEMAS


print("========================================")
print("AI AGENT TOOL SCHEMAS")
print("========================================")

for tool in TOOL_SCHEMAS:

    print("\nTool:", tool["name"])
    print("Description:", tool["description"])
    print("Required:", tool["parameters"]["required"])