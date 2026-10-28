from scheduler.validation import validate_tasks

def schedule_fcfs(tasks):
    """Run non-preemptive FCFS scheduling using arrival time and input order."""
    validate_tasks(tasks)
    pending = [(i, dict(t)) for i, t in enumerate(tasks)]
    pending.sort(key=lambda item: (float(item[1]["arrival_time"]), item[0]))
    results, clock = [], 0.0
    for _, task in pending:
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
