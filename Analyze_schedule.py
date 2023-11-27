from Build_Task_List import *
from Analyze_cost import import_tasks
from main import Task
import plotly.express as px
import datetime

# function that takes a task list, which has a tree structure
# encoded into its dependencies, and returns the time to completion
# of the task at the target index.
# This is a recursive function that calls itself on the dependents of the task.
# The base case is when the task is a leaf node, i.e. it has no dependents; in
# this case the function just returns the duration of the task.  If the task
# dependencies, the time to completion is the duration of the task plus the
# maximum of the time to completion of each of the dependents.
# The function should also check for cycles in the dependencies, and raise an
# error if one is found.  The function should also check that the target index
# is valid, and raise an error if it is not.
def compute_time_to_completion(tasks: list[Task], target_index: int) -> float:
    # check that target index is valid
    if target_index >= len(tasks):
        raise ValueError("target index is not valid")
    # check for cycles
    #if check_for_cycles(tasks):
    #    raise ValueError("cycles detected")
    # check for leaf node
    if tasks[target_index].dependencies == []:
        return tasks[target_index].duration
    # compute time to completion by first getting the list of indices of the dependents,
    # then mapping the compute_time_to_completion function to the list of indices, then
    # taking the max of the list of times to completion, and finally adding the duration
    # of the task
    else:
        list_of_dependents_indices = list(map(lambda x : find_task_index_by_name(x,tasks), tasks[target_index].dependencies))
        # check if any of the dependencies are invalid
        if None in list_of_dependents_indices:
            print("list of dependents indices: ",list_of_dependents_indices)
            print("target dependents: ",tasks[target_index].dependencies)
            raise ValueError("dependency is not valid")
        dependents_time_to_completion = list(map(lambda x : compute_time_to_completion(tasks,x), list_of_dependents_indices))
        return tasks[target_index].duration + max(dependents_time_to_completion)


if __name__ == '__main__':
    tasks = []
    mapping = {"name": 0, "description": 1, "total_cost": 2, "duration": 3, "is_milestone": 4, "is_deliverable": 5,
               "parent": 6, "is_acquisition": 7, "unit_price": 8, "quantity": 9, "percent_spares": 10, "rate": 11,
               "hours": 12, "dependencies": 13}
    import_tasks(tasks, mapping, "data/tasks.csv")

    import pandas as pd

    df = pd.DataFrame()
    start_date = datetime.datetime(2025, 1, 1)
    data=[]
    for i,task in enumerate(tasks):
        time_to_completion = compute_time_to_completion(tasks,i)
        dt = datetime.timedelta(weeks = time_to_completion)
        task_end_date = start_date + dt
        dt = datetime.timedelta(weeks = task.duration)
        task_start_date = task_end_date - dt
        data.append(dict(Task=task.name+": "+task.description, Finish = '{0}-{1}-{2}'.format(task_end_date.year,task_end_date.month,task_end_date.day), Start = '{0}-{1}-{2}'.format(task_start_date.year,task_start_date.month,task_start_date.day)))

    df = pd.DataFrame(data)
    df.sort_values("Start", inplace=True)
    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task")

    fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up
    fig.show()
    fig.write_image("images/DAC_timeline.png")

    # compute time to completion for each task
    times = list(map(lambda x : (tasks[x].name,compute_time_to_completion(tasks,x)), range(len(tasks))))
    print("Total time to completion: :",max(list(map(lambda x : x[1],times))))
    total_cost = sum(list(map(lambda t: t.get_total_cost(), tasks)))
    print("total cost: ", total_cost)