from scheduler.metrics import calculate_metrics

def test_metrics():
    rows = [{"arrival_time":0,"completion_time":5,"waiting_time":0,"turnaround_time":5,"response_time":0,"status":"Completed"},
            {"arrival_time":1,"completion_time":7,"waiting_time":2,"turnaround_time":6,"response_time":2,"status":"Completed"}]
    m = calculate_metrics(rows)
    assert m["total_tasks"] == 2
    assert m["average_waiting_time"] == 1
    assert m["average_turnaround_time"] == 5.5
    assert m["average_response_time"] == 1
    assert m["makespan"] == 7

def test_empty_metrics():
    assert calculate_metrics([])["total_tasks"] == 0
