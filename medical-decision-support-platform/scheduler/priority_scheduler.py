from scheduler.validation import VALID_PRIORITIES, validate_tasks

def schedule_priority(tasks):
    """Run non-preemptive priority scheduling; ties use arrival time then input order."""
    validate_tasks(tasks)
    pending = [(i, dict(task)) for i, task in enumerate(tasks)]
    results, clock = [], 0.0
    while pending:
        eligible = [item for item in pending if float(item[1]["arrival_time"]) <= clock]
        if not eligible:
            clock = min(float(item[1]["arrival_time"]) for item in pending)
            eligible = [item for item in pending if float(item[1]["arrival_time"]) <= clock]
        selected = min(eligible, key=lambda item: (VALID_PRIORITIES[item[1]["priority"]], float(item[1]["arrival_time"]), item[0]))
        _, task = selected
        pending.remove(selected)
        arrival, burst = float(task["arrival_time"]), float(task["burst_time"])
        start = max(clock, arrival)
        completion = start + burst
        result = dict(task)
        result.update(start_time=start, completion_time=completion, waiting_time=start-arrival,
                      turnaround_time=completion-arrival, response_time=start-arrival,
                      status="Completed", execution_order=len(results)+1)
        results.append(result)
        clock = completion
    return results
