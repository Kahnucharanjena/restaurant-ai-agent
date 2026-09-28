from backend.agent.memory import (
    get_session,
    add_message,
    get_memory_info
)


session_id = "demo-session"


add_message(
    session_id,
    "user",
    "Where is my order?"
)

add_message(
    session_id,
    "assistant",
    "Your order is out for delivery."
)


print("========================================")
print("CONVERSATION MEMORY TEST")
print("========================================")

print(get_session(session_id))

print("\nMemory information:")
print(get_memory_info(session_id))