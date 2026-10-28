from scheduler.fcfs_scheduler import schedule_fcfs

def test_fcfs_orders_by_arrival():
    tasks = [
        {"task_id":1,"task_name":"A","category":"Other","arrival_time":2,"burst_time":2,"priority":"Low"},
        {"task_id":2,"task_name":"B","category":"Other","arrival_time":0,"burst_time":3,"priority":"High"},
    ]
    rows = schedule_fcfs(tasks)
    assert [r["task_id"] for r in rows] == [2,1]
    assert rows[1]["start_time"] == 3 and rows[1]["waiting_time"] == 1

def test_empty_fcfs():
    assert schedule_fcfs([]) == []
