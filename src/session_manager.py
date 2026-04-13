from uuid import uuid4

def new_thread_id(prefix: str = "session") -> str:
    return f"{prefix}-{uuid4().hex[:8]}"
