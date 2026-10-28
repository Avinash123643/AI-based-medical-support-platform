VALID_PRIORITIES = {"High": 1, "Medium": 2, "Low": 3}

def validate_tasks(tasks):
    seen = set()
    required = {"task_id", "task_name", "arrival_time", "burst_time", "priority"}
    for i, task in enumerate(tasks):
        missing = required - set(task)
        if missing:
            raise ValueError(f"Task {i + 1} is missing: {', '.join(sorted(missing))}")
        if not str(task["task_name"]).strip():
            raise ValueError(f"Task {task['task_id']} has an empty name.")
        if isinstance(task["arrival_time"], bool) or not isinstance(task["arrival_time"], (int, float)) or task["arrival_time"] < 0:
            raise ValueError(f"Task {task['task_id']} arrival time must be a non-negative number.")
        if isinstance(task["burst_time"], bool) or not isinstance(task["burst_time"], (int, float)) or task["burst_time"] <= 0:
            raise ValueError(f"Task {task['task_id']} burst time must be a positive number.")
        if task["priority"] not in VALID_PRIORITIES:
            raise ValueError(f"Task {task['task_id']} priority must be High, Medium, or Low.")
        if task["task_id"] in seen:
            raise ValueError(f"Duplicate task ID: {task['task_id']}.")
        seen.add(task["task_id"])
