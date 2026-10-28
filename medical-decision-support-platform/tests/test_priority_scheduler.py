import pytest
from scheduler.priority_scheduler import schedule_priority

def task(i, arrival, burst, priority):
    return {"task_id":i, "task_name":f"Task {i}", "category":"Other", "arrival_time":arrival, "burst_time":burst, "priority":priority}

def test_priority_among_eligible_tasks():
    rows = schedule_priority([task(1,0,5,"Medium"), task(2,1,3,"High"), task(3,2,4,"Low")])
    assert [r["task_id"] for r in rows] == [1,2,3]  # non-preemptive first task continues

def test_priority_tie_uses_arrival_then_input_order():
    rows = schedule_priority([task(1,1,2,"High"), task(2,0,1,"High"), task(3,0,2,"High")])
    assert [r["task_id"] for r in rows] == [2,3,1]

def test_idle_until_arrival():
    row = schedule_priority([task(1,5,2,"High")])[0]
    assert row["start_time"] == 5 and row["completion_time"] == 7

def test_metrics_formulas():
    row = schedule_priority([task(1,2,3,"High")])[0]
    assert (row["waiting_time"], row["turnaround_time"], row["response_time"]) == (0,3,0)

def test_empty_tasks():
    assert schedule_priority([]) == []

def test_invalid_burst():
    with pytest.raises(ValueError):
        schedule_priority([task(1,0,0,"High")])

def test_duplicate_ids():
    with pytest.raises(ValueError):
        schedule_priority([task(1,0,1,"High"), task(1,1,1,"Low")])

def test_input_unchanged():
    original = task(1,0,2,"High")
    schedule_priority([original])
    assert "start_time" not in original
