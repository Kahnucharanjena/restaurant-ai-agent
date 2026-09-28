from datetime import datetime
from pathlib import Path

from backend.tools.order_status import get_order_status
from backend.tools.order_details import get_order_details
from backend.tools.support_ticket import create_support_ticket
from backend.tools.knowledge_base import search_kb


# ==========================================
# AVAILABLE AGENT TOOLS
# ==========================================

TOOLS = {
    "get_order_status": get_order_status,
    "get_order_details": get_order_details,
    "create_support_ticket": create_support_ticket,
    "search_knowledge_base": search_kb,
}
def log_tool_call(tool_name: str, success: bool):
    """
    Record tool execution for observability.
    """

    log_file = (
        Path(__file__).resolve().parent.parent
        / "logs"
        / "tool_calls.log"
    )

    timestamp = datetime.now().isoformat()

    status = "SUCCESS" if success else "FAILED"

    with open(log_file, "a", encoding="utf-8") as file:
        file.write(
            f"{timestamp} | {tool_name} | {status}\n"
        )
# ==========================================
# TOOL EXECUTION
# ==========================================

def execute_tool(tool_name: str, arguments: dict):
    """
    Execute an approved tool with validated arguments.
    """

    if tool_name not in TOOLS:
        return {
            "success": False,
            "error": "UNKNOWN_TOOL",
            "message": f"Tool '{tool_name}' is not available."
        }

    try:
        tool_function = TOOLS[tool_name]

        result = tool_function(**arguments)

        log_tool_call(
            tool_name,
            result.get("success", False)
        )

        return result

    except TypeError as e:
        return {
            "success": False,
            "error": "INVALID_TOOL_ARGUMENTS",
            "message": str(e)
        }

    except Exception:
        return {
            "success": False,
            "error": "TOOL_EXECUTION_ERROR",
            "message": "The requested tool could not be executed."
        }


# ==========================================
# AGENT HEALTH CHECK
# ==========================================

def get_agent_info():
    return {
        "agent": "Restaurant AI Support Agent",
        "status": "ready",
        "tools": list(TOOLS.keys())
    }


# ==========================================
# AGENT STATUS
# ==========================================

def get_agent_status():
    return {
        "name": "Restaurant AI Support Agent",
        "status": "ready",
        "tool_count": len(TOOLS),
        "tools": list(TOOLS.keys())
    }