"""Provides a graphical simulation of four scheduling algorithms
First in first out
Shortest job first
Shortest time to completion
Round Robin
"""

__author__ = "Elijah Kwaku Adutwum Boateng"
__version__ = "1.0.1"
__email__ = "elijah.boateng@ashesi.edu.gh"
__supervisors__ = "Dennis Owusu Asamoah & Ian Akotey"

import pandas as pd
import streamlit as st
import plotly.express as px
from schedulers import Schedulers
from random import randint

st.set_page_config(page_title='Scheduling Algorithms Simulations', layout="wide")


# visualizer (wow factor 1.0)
def viz(data):
    fig = px.timeline(data, x_start="Start", x_end="Finish", y="Task", color="Start")
    fig.update_yaxes(autorange="reversed")
    fig.layout.xaxis.type = 'linear'
    duration = []
    for x in data:
        duration.append(x['Finish'] - x['Start'])
    fig.data[0].x = duration
    return fig


# calculating response time (wow factor 2.1)
def response(res):
    _procs = dict()
    total_response = 0

    for proc in res:

        curr_proc = proc['Task']
        curr_resp = proc['Start']  # first run
        arrival = proc['Arrival']

        if curr_proc not in _procs:
            _procs[curr_proc] = (curr_resp - arrival)
        else:
            pass

    for p in _procs:
        total_response += _procs[p]

    return [total_response, round(total_response / len(_procs), 1)]


# calculating turn around time (wow factor 2.2)
def turn_around(res):
    _procs = dict()
    turn_ard = 0

    for proc in res:

        curr_proc = proc['Task']
        curr_turn = proc['Finish']
        arrival = proc['Arrival']

        if curr_proc not in _procs:
            _procs[curr_proc] = (curr_turn - arrival)
        else:
            _procs[curr_proc] = (curr_turn - arrival)

    for p in _procs:
        turn_ard += _procs[p]

    return [turn_ard, round(turn_ard / len(_procs), 1)]


# organizing the 4 metrics (turn around and response times with their avgs)
def metrics(data):
    turn_around_vals = turn_around(data)
    total_turnaround = turn_around_vals[0]
    avg_turnaround = turn_around_vals[1]

    response_vals = response(data)
    total_response = response_vals[0]
    avg_response = response_vals[1]

    return [total_turnaround, avg_turnaround, total_response, avg_response]


# heading
st.markdown("<h1 style='text-align: center;'>CPU SCHEDULING ALGORITHMS</h1>", unsafe_allow_html=True)

# spacing
st.markdown("\n\n")

# spacing
st.markdown("\n\n\n\n")

# process input setup
with st.expander("Set Parameters"):
    st.header("Customize your processes 👨🏽‍💻")
    st.write("------------------------------")
    num_procs = st.number_input("Number of Processes", min_value=1, max_value=10, value=1, step=1)

    try:
        columns = st.columns(num_procs)
    except:
        columns = st.columns(1)

    proc_struct = dict()
    a = 0
    for i, j in enumerate(columns):
        a+=30
        with j:
            st.markdown('\n\n\n')
            st.markdown(f"<h5 style='text-align: center;'>Process {chr(i + 65)}</h5>", unsafe_allow_html=True)
            arr_time = st.number_input(f"Arrival time (ms)", min_value=0, max_value=10, step=1, key=randint(a,a*10))
            time = st.number_input(f"Runtime time (ms)", min_value=1, max_value=200, step=1, key=randint(a+20,a*10))
        proc_struct[f'Process {chr(i + 65)}'] = [arr_time, time]
    time_slice = st.number_input(f"Time slice(ms)", min_value=1, max_value=10, step=3, value=3,
                                 help="For Round Robin Scheduler")

# spacing with button
st.markdown('\n\n\n\n\n\n\n\n\n')

run = st.button("Run Scheduler 🏃🏽‍♀️💨")

st.markdown('\n\n\n\n\n\n\n\n\n')

# when button is clicked
if run:
    # tabs for each process
    fifo, sjf, stc, rr = st.tabs(
        ["First In First Out", "Shortest Job First", "Shortest Time to Completion", "Round Robin"])

    with fifo:
        data_fifo = Schedulers.FirstInFirstOut(proc_struct)
        st.markdown(f"<h2 style='text-align: center;'>First In First Out Scheduling</h2>", unsafe_allow_html=True)
        values = metrics(data_fifo)
        st.plotly_chart(viz(data_fifo), use_container_width=True)
        l, lc, rc, r = st.columns(4)
        l.metric('Total turn around time', f'{values[0]} ms')
        lc.metric('Average turn around time', f'{values[1]} ms')
        rc.metric('Total response time', f'{values[2]} ms')
        r.metric('Average response time', f'{values[3]} ms')
        with st.expander("Running Sequence Data"):
            df = pd.DataFrame.from_dict(data_fifo)
            st.write(df)

    with sjf:
        data_sjf = Schedulers.ShortestJobFirst(proc_struct)
        st.markdown(f"<h2 style='text-align: center;'>Shortest Job First Scheduling</h2>", unsafe_allow_html=True)
        values = metrics(data_sjf)
        st.plotly_chart(viz(data_sjf), use_container_width=True)
        l, lc, rc, r = st.columns(4)
        l.metric('Total turn around time', f'{values[0]} ms')
        lc.metric('Average turn around time', f'{values[1]} ms')
        rc.metric('Total response time', f'{values[2]} ms')
        r.metric('Average response time', f'{values[3]} ms')
        with st.expander("Running Sequence Data"):
            df = pd.DataFrame.from_dict(data_sjf)
            st.write(df)

    with stc:
        data_stc = Schedulers.ShortestTimeToCompletion(proc_struct)
        st.markdown(f"<h2 style='text-align: center;'>Shortest Time to Completion Scheduling</h2>",
                    unsafe_allow_html=True)
        values = metrics(data_stc)
        st.plotly_chart(viz(data_stc), use_container_width=True)
        l, lc, rc, r = st.columns(4)
        l.metric('Total turn around time', f'{values[0]} ms')
        lc.metric('Average turn around time', f'{values[1]} ms')
        rc.metric('Total response time', f'{values[2]} ms')
        r.metric('Average response time', f'{values[3]} ms')
        with st.expander("Running Sequence Data"):
            df = pd.DataFrame.from_dict(data_stc)
            st.write(df)

    with rr:
        data_rr = Schedulers.RoundRobin(proc_struct, time_slice)
        st.markdown(f"<h2 style='text-align: center;'>Round Robin Scheduling</h2>", unsafe_allow_html=True)
        values = metrics(data_rr)
        st.plotly_chart(viz(data_rr), use_container_width=True)
        l, lc, rc, r = st.columns(4)
        l.metric('Total turn around time', f'{values[0]} ms')
        lc.metric('Average turn around time', f'{values[1]} ms')
        rc.metric('Total response time', f'{values[2]} ms')
        r.metric('Average response time', f'{values[3]} ms')
        with st.expander("Running Sequence Data"):
            df = pd.DataFrame.from_dict(data_rr)
            st.write(df)
