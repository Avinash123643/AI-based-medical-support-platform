import pandas as pd
import streamlit as st
from scheduler.fcfs_scheduler import schedule_fcfs
from scheduler.priority_scheduler import schedule_priority
from scheduler.resource_manager import allocate_resources
from scheduler.sample_data import SAMPLE_TASKS
from scheduler.validation import validate_tasks
from scheduler.metrics import calculate_metrics

st.set_page_config(page_title="AI-Based Medical Decision Support Platform", page_icon="🏥", layout="wide")
st.title("AI-Based Medical Decision Support Platform")
st.caption("Operating Systems PBL • Group 5 • Educational scheduling simulation")

if "tasks" not in st.session_state:
    st.session_state.tasks = [dict(t) for t in SAMPLE_TASKS]
if "priority_results" not in st.session_state:
    st.session_state.priority_results = []
if "fcfs_results" not in st.session_state:
    st.session_state.fcfs_results = []

with st.sidebar:
    st.header("Navigation")
    page = st.radio("Choose a module", ["Dashboard", "Task Management", "Priority Scheduling", "Resource Management", "Performance Analysis", "About Project"])
    st.divider()
    st.caption("Synthetic tasks only. Not a clinical diagnosis system.")

def result_df(results):
    cols = ["task_id", "task_name", "category", "priority", "arrival_time", "burst_time", "start_time", "completion_time", "waiting_time", "turnaround_time", "response_time", "status"]
    if not results:
        return pd.DataFrame(columns=cols)
    df = pd.DataFrame(results)[cols]
    return df.rename(columns={"task_id":"Task ID", "task_name":"Task Name", "category":"Category", "priority":"Priority", "arrival_time":"Arrival Time", "burst_time":"Burst Time", "start_time":"Start Time", "completion_time":"Completion Time", "waiting_time":"Waiting Time", "turnaround_time":"Turnaround Time", "response_time":"Response Time", "status":"Status"})

def run_schedulers():
    validate_tasks(st.session_state.tasks)
    st.session_state.priority_results = schedule_priority(st.session_state.tasks)
    st.session_state.fcfs_results = schedule_fcfs(st.session_state.tasks)

def show_metrics(results):
    if not results:
        st.info("Run scheduling to calculate performance metrics.")
        return
    m = calculate_metrics(results)
    cols = st.columns(5)
    cols[0].metric("Total Tasks", m["total_tasks"])
    cols[1].metric("Completed", m["completed_tasks"])
    cols[2].metric("Avg Waiting", f'{m["average_waiting_time"]:.2f}')
    cols[3].metric("Avg Turnaround", f'{m["average_turnaround_time"]:.2f}')
    cols[4].metric("Avg Response", f'{m["average_response_time"]:.2f}')
    st.caption(f'Makespan: {m["makespan"]:.2f} simulated time units.')

def show_timeline(results):
    if not results:
        return
    st.subheader("Execution Timeline")
    chart = pd.DataFrame([{"Task": r["task_name"], "Start": r["start_time"], "Duration": r["burst_time"]} for r in results])
    st.bar_chart(chart.set_index("Task"))
    st.caption("The table below shows exact start and completion times; the chart is a simple duration view, not a time-scaled Gantt chart.")

if page == "Dashboard":
    st.subheader("Project Dashboard")
    st.write("Manage synthetic medical-related computational tasks, simulate priority scheduling, and review OS scheduling metrics.")
    a, b = st.columns(2)
    if a.button("Load Sample Tasks", use_container_width=True):
        st.session_state.tasks = [dict(t) for t in SAMPLE_TASKS]
        st.session_state.priority_results, st.session_state.fcfs_results = [], []
        st.rerun()
    if b.button("Run Scheduling", type="primary", use_container_width=True):
        try:
            run_schedulers(); st.success("Scheduling completed.")
        except ValueError as e:
            st.error(str(e))
    st.subheader("Current Tasks")
    st.dataframe(pd.DataFrame(st.session_state.tasks), use_container_width=True, hide_index=True)
    show_metrics(st.session_state.priority_results)
    if st.session_state.priority_results:
        st.subheader("Priority Scheduling Results")
        st.dataframe(result_df(st.session_state.priority_results), use_container_width=True, hide_index=True)
        show_timeline(st.session_state.priority_results)

elif page == "Task Management":
    st.subheader("Task Management")
    with st.form("add_task", clear_on_submit=True):
        name = st.text_input("Task name")
        category = st.selectbox("Task category", ["Lab Report Processing", "Medical Image Review", "Test Result Analysis", "Doctor Request", "Other"])
        arrival = st.number_input("Arrival time", min_value=0, value=0, step=1)
        burst = st.number_input("Burst time (processing units)", min_value=1, value=3, step=1)
        priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        submitted = st.form_submit_button("Add Task", type="primary")
    if submitted:
        if not name.strip():
            st.error("Task name cannot be empty.")
        else:
            new_id = max([int(t["task_id"]) for t in st.session_state.tasks] or [0]) + 1
            st.session_state.tasks.append({"task_id":new_id, "task_name":name.strip(), "category":category, "arrival_time":int(arrival), "burst_time":int(burst), "priority":priority, "status":"New"})
            st.session_state.priority_results, st.session_state.fcfs_results = [], []
            st.success(f"Task {new_id} added.")
    x, y = st.columns(2)
    if x.button("Load Sample Tasks"):
        st.session_state.tasks = [dict(t) for t in SAMPLE_TASKS]
        st.session_state.priority_results, st.session_state.fcfs_results = [], []
        st.rerun()
    if y.button("Clear All Tasks"):
        st.session_state.tasks = []
        st.session_state.priority_results, st.session_state.fcfs_results = [], []
        st.rerun()
    st.dataframe(pd.DataFrame(st.session_state.tasks), use_container_width=True, hide_index=True)
    if st.session_state.tasks:
        delete_id = st.selectbox("Task ID to delete", [t["task_id"] for t in st.session_state.tasks])
        if st.button("Delete Selected Task"):
            st.session_state.tasks = [t for t in st.session_state.tasks if t["task_id"] != delete_id]
            st.session_state.priority_results, st.session_state.fcfs_results = [], []
            st.rerun()

elif page == "Priority Scheduling":
    st.subheader("Custom Non-Preemptive Priority Scheduling")
    st.markdown("**Priority values:** High = 1, Medium = 2, Low = 3. Lower value means higher priority. Ties use arrival time, then input order. A running task is not interrupted.")
    if st.button("Run Priority Scheduler", type="primary"):
        try:
            run_schedulers(); st.success("Priority scheduler completed.")
        except ValueError as e:
            st.error(str(e))
    if st.session_state.priority_results:
        st.dataframe(result_df(st.session_state.priority_results), use_container_width=True, hide_index=True)
        show_timeline(st.session_state.priority_results)
        st.download_button("Download Results CSV", result_df(st.session_state.priority_results).to_csv(index=False).encode("utf-8"), "priority_scheduling_results.csv", "text/csv")

elif page == "Resource Management":
    st.subheader("Resource Management Simulation")
    st.caption("These are illustrative resource units, not actual CPU or memory allocation.")
    cpu = st.number_input("Configured CPU units", min_value=1, max_value=100, value=4)
    memory = st.number_input("Configured memory units", min_value=1, max_value=1000, value=16)
    io_units = st.number_input("Configured I/O units", min_value=1, max_value=100, value=2)
    if st.button("Simulate Resource Check", type="primary"):
        st.session_state.resource_results = allocate_resources(st.session_state.tasks, {"CPU":int(cpu), "Memory":int(memory), "I/O":int(io_units)})
    if "resource_results" in st.session_state:
        st.dataframe(pd.DataFrame(st.session_state.resource_results), use_container_width=True, hide_index=True)

elif page == "Performance Analysis":
    st.subheader("Performance Analysis")
    if st.button("Calculate / Refresh Results", type="primary"):
        try:
            run_schedulers()
        except ValueError as e:
            st.error(str(e))
    p, f = st.session_state.priority_results, st.session_state.fcfs_results
    if p and f:
        pm, fm = calculate_metrics(p), calculate_metrics(f)
        comparison = pd.DataFrame([
            {"Algorithm":"Priority Scheduling", "Average Waiting Time":pm["average_waiting_time"], "Average Turnaround Time":pm["average_turnaround_time"], "Average Response Time":pm["average_response_time"], "Makespan":pm["makespan"]},
            {"Algorithm":"FCFS", "Average Waiting Time":fm["average_waiting_time"], "Average Turnaround Time":fm["average_turnaround_time"], "Average Response Time":fm["average_response_time"], "Makespan":fm["makespan"]},
        ])
        st.dataframe(comparison.round(2), use_container_width=True, hide_index=True)
        st.bar_chart(comparison.set_index("Algorithm")[["Average Waiting Time", "Average Turnaround Time", "Average Response Time"]])
        st.caption("Results depend on task arrival times, burst times, and assigned priorities. Priority scheduling is not always better for every metric.")
    else:
        st.info("Run scheduling to compare both algorithms.")

else:
    st.subheader("About Project")
    st.markdown("""
**Project:** AI-Based Medical Decision Support Platform  
**Subject:** Operating Systems (CCSE0303A)  
**Team:** Group 5  
**Team Leader:** Avinash Kumar  
**Faculty Guide:** Mr. Manish Chaudhary

**OS concepts demonstrated:** Process/task management, CPU scheduling simulation, priority management, task queues, resource requirement simulation, and performance monitoring.

**Limitations:** This is an educational prototype. It does not diagnose patients or recommend treatment. It uses synthetic data, does not modify the Windows kernel scheduler, and does not include a trained or clinically validated AI model.
""")
