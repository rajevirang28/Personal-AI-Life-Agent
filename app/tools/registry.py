from app.tools.task_tools import (
    get_pending_tasks,
    get_today_priorities,
    get_task_statistics
)

from app.tools.memory_tools import (
    search_memories,
    get_goals
)


TOOLS = {
    "get_pending_tasks":
        get_pending_tasks,

    "get_today_priorities":
        get_today_priorities,

    "get_task_statistics":
        get_task_statistics,

    "search_memories":
        search_memories,

    "get_goals":
        get_goals
}