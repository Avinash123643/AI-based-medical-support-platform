def allocate_resources(tasks, resource_pool):
    """Illustrative resource check; does not allocate real OS resources."""
    rows = []
    for task in tasks:
        category = str(task.get("category", "")).lower()
        if "image" in category:
            req = {"CPU": 2, "Memory": 6, "I/O": 1}
        elif "report" in category or "result" in category:
            req = {"CPU": 1, "Memory": 3, "I/O": 1}
        else:
            req = {"CPU": 1, "Memory": 2, "I/O": 1}
        fits = all(int(resource_pool.get(k, 0)) >= v for k, v in req.items())
        rows.append({"Task ID": task["task_id"], "Task Name": task["task_name"],
                     "Requirements": ", ".join(f"{k}: {v}" for k, v in req.items()),
                     "Configured Pool": ", ".join(f"{k}: {int(resource_pool.get(k, 0))}" for k in req),
                     "Status": "Requirements fit configured pool" if fits else "Insufficient configured resource units",
                     "Note": "Illustrative simulation only"})
    return rows
