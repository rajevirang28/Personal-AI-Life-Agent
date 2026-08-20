def format_tool_result(
    tool_name: str,
    result
):

    if tool_name in [
        "get_pending_tasks",
        "get_today_priorities"
    ]:

        if not result:
            return "No tasks found."

        lines = []

        for task in result:

            lines.append(
                f"- {task.title} | "
                f"priority={task.priority} | "
                f"status={task.status} | "
                f"due={task.due_date}"
            )

        return "\n".join(lines)

    if tool_name == "search_memories":

        if not result:
            return "No matching memories found."

        lines = []

        for memory in result:

            lines.append(
                f"- [{memory.memory_type}] "
                f"{memory.title}: "
                f"{memory.content}"
            )

        return "\n".join(lines)
    
    if tool_name == "get_task_statistics":

        return (
            f"Total tasks: {result['total']}\n"
            f"Completed: {result['completed']}\n"
            f"Pending: {result['pending']}\n"
            f"In progress: {result['in_progress']}"
        )
    
    if tool_name in [
        "search_memories",
        "get_goals"
    ]:

        if not result:
            return "No memories found."

        lines = []

        for memory in result:

            lines.append(
                f"- [{memory.memory_type}] "
                f"{memory.title}: "
                f"{memory.content}"
            )

        return "\n".join(lines)

    return str(result)