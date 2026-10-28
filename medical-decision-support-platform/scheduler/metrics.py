def calculate_metrics(results):
    if not results:
        return {"total_tasks": 0, "completed_tasks": 0, "average_waiting_time": 0.0,
                "average_turnaround_time": 0.0, "average_response_time": 0.0, "makespan": 0.0}
    n = len(results)
    return {
        "total_tasks": n,
        "completed_tasks": sum(r.get("status") == "Completed" for r in results),
        "average_waiting_time": sum(float(r["waiting_time"]) for r in results)/n,
        "average_turnaround_time": sum(float(r["turnaround_time"]) for r in results)/n,
        "average_response_time": sum(float(r["response_time"]) for r in results)/n,
        "makespan": max(float(r["completion_time"]) for r in results)-min(float(r["arrival_time"]) for r in results),
    }
