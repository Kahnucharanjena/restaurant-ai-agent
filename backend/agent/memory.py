# ==========================================
# SIMPLE CONVERSATION MEMORY
# ==========================================

sessions = {}


def get_session(session_id: str):
    """
    Get conversation history for a session.
    Creates a new session if it does not exist.
    """

    if session_id not in sessions:
        sessions[session_id] = []

    return sessions[session_id]


def add_message(session_id: str, role: str, content: str):
    """
    Add a message to the conversation history.
    """

    history = get_session(session_id)

    history.append({
        "role": role,
        "content": content
    })


def clear_session(session_id: str):
    """
    Clear conversation history.
    """

    sessions.pop(session_id, None)


def get_memory_info(session_id: str):
    """
    Return basic session information.
    """

    history = get_session(session_id)

    return {
        "session_id": session_id,
        "message_count": len(history)
    }