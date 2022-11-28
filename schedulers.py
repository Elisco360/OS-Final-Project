
class Schedulers:
    def __init__(self):
        pass

    @staticmethod
    def __check_arrivals(p1, p2):
        """Check if any two processes have the same arrival time"""
        if p1 == p2:
            return True
        else:
            return False

    @staticmethod
    def __merge(dict1, dict2):
        """Merges any two dictionaries"""
        for i in dict2.keys():
            dict1[i] = dict2[i]
        return dict1

    @staticmethod
    def __sort_procs(procs: list, processes: dict):
        """Sorts processes by arrival time and runtime altogether."""
        proc_list = {}

        i = 0
        while i < len(procs):
            temp = {}
            if i + 1 < len(procs):
                if processes[procs[i]][0] < processes[procs[i + 1]][0]:
                    proc_list[procs[i]] = processes[procs[i]]
                    i += 1
                elif processes[procs[i]][0] == processes[procs[i + 1]][0]:
                    counter = 0
                    while i + counter < len(procs):
                        if Schedulers.__check_arrivals(processes[procs[i]][0], processes[procs[i + counter]][0]):
                            counter += 1
                        else:
                            break
                    for k in procs[i:i + counter]:
                        temp[k] = processes[k]
                    temp = dict(sorted(temp.items(), key=lambda item: item[1][1]))
                    proc_list = Schedulers.__merge(proc_list, temp)
                    i += counter
            else:
                proc_list[procs[-1]] = processes[procs[-1]]
                break
        return proc_list

    @staticmethod
    def __update_procs(procs, finish):
        """updates the arrival times of processes to allow re-ordering"""
        new_procs = {}
        for i in procs:
            if procs[i][0] <= finish:
                new_procs[i] = [finish, procs[i][1]]
            else:
                new_procs[i] = [procs[i][0], procs[i][1]]
        return new_procs

    @staticmethod
    def FirstInFirstOut(processes: dict):
        # sort processes by their arrival times given the structure -> {<process_name>:[<arrival_time>:<runtime>]}
        processes = dict(sorted(processes.items(), key=lambda item: item[1][0]))

        # initialize a queue to keep running/ready jobs and a resultant array of the running sequence
        active_queue = dict()
        res = []

        # putting all processes and their runtimes in the queue given the structure -> {<process_name>:<current_runtime>}
        for proc in processes:
            active_queue[proc] = processes[proc][1]
        procs = list(active_queue)

        # ------------------ Go through the loop until the queue is empty: thus all runtimes are zero ----------------#

        # initialize finish time to the arrival time of the first process
        finish = processes[procs[0]][0]

        # ---------------------------- Emptying the queue ---------------------------#
        while len(active_queue) != 0:
            # select a process and store its attributes
            curr_proc = list(active_queue)[0]
            original_runtime = active_queue[curr_proc]
            arrival = processes[curr_proc][0]

            # set start time to finish time after every new process is selected
            start = finish

            for i in range(int(original_runtime)):
                finish += 1
                active_queue[curr_proc] -= 1
                curr_runtime = active_queue[curr_proc]
                n_curr_proc = curr_proc

                if curr_runtime == 0:
                    del active_queue[curr_proc]
                    break
                else:
                    del active_queue[curr_proc]
                    active_queue[curr_proc] = curr_runtime

            if start >= arrival:
                res.append(dict(Task=curr_proc, Start=start, Finish=finish, Runtime=finish - start, Arrival=arrival))
            else:
                start = arrival
                finish = start + processes[curr_proc][1]
                res.append(dict(Task=curr_proc, Start=arrival, Finish=finish, Runtime=finish - start, Arrival=arrival))

        return res

    @staticmethod
    def ShortestJobFirst(processes):
        # same as FIFO but processes are now sorted by arrival time and runtime altogether.
        processes = dict(sorted(processes.items(), key=lambda item: item[1][0]))
        processes = Schedulers.__sort_procs(list(processes), processes)
        active_queue = dict()
        res = []

        for proc in processes:
            active_queue[proc] = processes[proc][1]
        procs = list(active_queue)

        finish = processes[procs[0]][0]

        while len(active_queue) != 0:
            curr_proc = list(active_queue)[0]
            original_runtime = active_queue[curr_proc]

            start = finish
            arrival = processes[curr_proc][0]
            nxt_curr_proc = curr_proc
            for i in range(int(original_runtime)):
                finish += 1
                active_queue[curr_proc] -= 1
                curr_runtime = active_queue[curr_proc]

                if curr_runtime == 0:
                    del active_queue[curr_proc]
                    break
                else:
                    del active_queue[curr_proc]
                    active_queue[curr_proc] = curr_runtime
                    active_queue = dict(sorted(active_queue.items(), key=lambda item: item[1]))

                    if active_queue[list(active_queue)[0]] <= curr_runtime and processes[list(active_queue)[0]][0] == finish:
                        nxt_curr_proc = list(active_queue)[0]

            if start >= arrival:
                res.append(dict(Task=curr_proc, Start=start, Finish=finish, Runtime=finish - start, Arrival=arrival))
                curr_proc = nxt_curr_proc
            else:
                start = arrival
                finish = start + processes[curr_proc][1]
                res.append(dict(Task=curr_proc, Start=arrival, Finish=finish, Runtime=finish - start, Arrival=arrival))

        return res

    @staticmethod
    def RoundRobin(processes, time_slice=3):
        # sort by arrival time and initialize queue and resultant array
        processes = dict(sorted(processes.items(), key=lambda item: item[1][0]))
        active_queue = dict()
        res = []

        # put all processes with their runtime in a queue
        for proc in processes:
            active_queue[proc] = processes[proc][1]
        procs = list(active_queue)

        # ------------------ Go through the loop until the queue is empty: thus all runtimes are zero ----------------#

        # initialize finish to the arrival time of the first process
        finish = processes[procs[0]][0]

        # initialized time_tracked to zero
        timer = 0

        # initialize a flag to false
        flag = False

        # initialize the timer_flag to False
        timer_flag = False

        # ---------------------------- Emptying the queue ---------------------------#
        while len(active_queue) != 0:
            # select a process and loop through for the time slice's number of times
            curr_proc = list(active_queue)[0]
            curr_runtime = active_queue[curr_proc]
            arrival = processes[curr_proc][0]

            # set the start time to the finish time
            start = finish

            # for every iteration
            for i in range(int(time_slice)):

                # -> check if the arrival time within (<=) the time_tracked
                if arrival <= timer:
                    # set flag to true
                    flag = True

                    # --Y--> add one to the finish time
                    finish += 1
                    # update the runtime of the process by subtracting one
                    active_queue[curr_proc] -= 1
                    curr_runtime = active_queue[curr_proc]
                    # add one to time_tracked
                    # timer += 1

                    # check if the process is done
                    if curr_runtime == 0:

                        # --Y--> remove the process from the queue
                        del active_queue[curr_proc]
                        # set the timer flag to True
                        timer_flag = True
                        # break out of the loop
                        break
                    # --N--> remove the process and add to the queue again with the new runtime and set timer_flag to false
                    else:
                        del active_queue[curr_proc]
                        active_queue[curr_proc] = curr_runtime
                        timer_flag = False

                # --N--> add it to the back of the queue
                else:
                    del active_queue[curr_proc]
                    active_queue[curr_proc] = curr_runtime
                    # set flag to False and break out of the loop
                    flag = False

            # if timer_flag is True: add one to timer and set finish to timer
            if timer_flag:
                timer += 1
                finish = timer

            # set timer to finish
            timer = finish

            # update resultant array if flag is true
            if flag:
                res.append(dict(Task=curr_proc, Start=start, Finish=finish, Runtime=finish - start, Arrival=arrival))

        return res

    @staticmethod
    def ShortestTimeToCompletion(processes):
        processes = dict(sorted(processes.items(), key=lambda item: item[1][0]))
        processes = Schedulers.__sort_procs(list(processes), processes)
        active_queue = dict()
        res = []

        for proc in processes:
            active_queue[proc] = [processes[proc][0], processes[proc][1]]
        procs = list(active_queue)

        finish = processes[procs[0]][0]

        while len(active_queue) != 0:
            curr_proc = list(active_queue)[0]
            curr_runtime = active_queue[curr_proc][1]

            start = finish
            arrival = processes[curr_proc][0]

            for i in range(curr_runtime):
                # run(curr_proc)
                finish += 1
                active_queue[curr_proc][1] -= 1
                curr_runtime = active_queue[curr_proc][1]
                curr_arrival = active_queue[curr_proc][0]

                # check if the process is done
                if curr_runtime == 0:

                    # --Y--> remove from the array
                    del active_queue[curr_proc]
                    break
                # --N-->
                else:
                    # update procs with arrivals such that
                    active_queue = Schedulers.__update_procs(active_queue, finish)

                    # sort procs and choose the 0th index
                    active_queue = dict(sorted(active_queue.items(), key=lambda item: item[1][0]))
                    active_queue = Schedulers.__sort_procs(list(active_queue), active_queue)

                    # --------------------- check if there's a shorter process ----------------------------- #
                    if active_queue[list(active_queue)[0]][1] < curr_runtime and active_queue[list(active_queue)[0]][0] == finish:
                        n_proc = list(active_queue)[0]
                        break
                    # --N--> keep running curr_procs
                    else:
                        del active_queue[curr_proc]
                        active_queue[curr_proc] = [curr_arrival, curr_runtime]

            # add to resultant array
            if start >= arrival:
                res.append(dict(Task=curr_proc, Start=start, Finish=finish, Runtime=finish - start, Arrival=arrival))
            else:
                start = arrival
                finish = start + processes[curr_proc][1]
                res.append(dict(Task=curr_proc, Start=arrival, Finish=finish, Runtime=finish - start, Arrival=arrival))

        return res

