from app.tools.task_tools import (
    get_pending_tasks,
    get_today_priorities
)

from app.tools.memory_tools import (
    search_memories
)

TOOLS = {
    "get_pending_tasks": get_pending_tasks,
    "get_today_priorities": get_today_priorities,
    "search_memories": search_memories
}