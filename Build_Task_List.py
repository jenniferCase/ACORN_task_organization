from main import Task, Acquisition, Labor
import csv

## function that reads a csv file and a list of tasks that are each a list of strings,
## one corresonding to each column in the csv file
def read_tasks(filename="ACORN_DAC_costing_Labor_costs.csv"):
    tasks = []
    # read csv file
    with open(filename, "r") as f:
        reader = csv.reader(f)
        task_list = list(reader)
    #print(task_list)
    return task_list[1:]

## function that reads a csv file and appends a tasks with Labor tasks
def read_labor_tasks(tasks=[], filename="ACORN_DAC_costing_Labor_costs.csv"):
    tasks_dict = {}
    task_list = read_tasks(filename)

    # create a list of tasks
    first = True
    for task in task_list:
        if task[1] == "": continue
        if task[0] in tasks_dict:
            tasks_dict[task[0]].append(Labor(task[0] + ".{0}".format(int(len(tasks_dict[task[0]]) + 1)), task[1]+"; "+task[2]))
        else:
            tasks_dict[task[0]] = [Labor(task[0] + ".{0}".format(1), task[1]+task[2])]

        #tasks.append(Labor(task[0] + ".{0}".format(int(len(tasks) + 1)), task[1]))
        tasks_dict[task[0]][-1].rate = float(task[5])
        tasks_dict[task[0]][-1].hours = float(task[3])
        tasks_dict[task[0]][-1].total_cost = float(task[5]) * float(task[3])
        tasks_dict[task[0]][-1].duration = float(task[4])
        tasks_dict[task[0]][-1].dependencies.extend(task[8].split(","))
        print(tasks_dict[task[0]][-1])
        tasks.append(tasks_dict[task[0]][-1])

# function that read a csv file and appends tasks with Acquisition tasks
def read_acquisition_tasks(tasks=[], filename="ACORN_DAC_costing_MandS_costs.csv"):
    tasks_dict = {}
    task_list = read_tasks(filename)

    # create a list of tasks
    first = True
    for task in task_list:
        if task[1] == "": continue
        if task[0] in tasks_dict:
            tasks_dict[task[0]].append(Labor(task[0] + ".{0}".format(int(len(tasks_dict[task[0]]) + 1)), task[1]+"; "+task[2]))
        else:
            tasks_dict[task[0]] = [Labor(task[0] + ".{0}".format(1), task[1]+task[2])]

        #tasks.append(Acquisition(task[0] + ".{0}".format(int(len(tasks) + 1)), task[1]))
        tasks_dict[task[0]][-1].quantity = float(task[3])
        tasks_dict[task[0]][-1].unit_price = float(task[6])
        tasks_dict[task[0]][-1].percent_spares = float(task[4])
        tasks_dict[task[0]][-1].total_cost = float(task[6]) * float(task[3]) * (1 + float(task[4])/100)
        tasks_dict[task[0]][-1].duration = float(task[8])
        tasks_dict[task[0]][-1].dependencies.extend(task[9].split(","))
        tasks_dict[task[0]][-1].dependencies.extend(task[10].split(","))

        print(tasks_dict[task[0]][-1])
        tasks.append(tasks_dict[task[0]][-1])

# function that writes a list of tasks to a csv file
# each line is a unieque task; columns are formatted
# according to the to_csv() method of the object
def export_tasks_to_csv(tasks=[]):
    with open("tasks.csv","w") as f:
        f.write("name,description,duration,total_cost,is_milestone,is_deliverable,unit_price,quantity,percent_spares,rate,hours,dependencies,parent,children\n")
        for task in tasks:
            f.write(task.to_csv() + "\n")
    for task in tasks :
        print(task.to_csv())

if __name__ == '__main__':
    tasks = []
    read_labor_tasks(tasks)
    read_acquisition_tasks(tasks)

    ## set up dependencies between tasks
    #  dependencies are based on references to base classes; one shortcoming of this
    #  is that one will lose the ability to know where the task is a Labor or Acquisition
    #  task, and some information may be lost
    # for task in tasks:
    #     for dependency in task.dependencies:
    #         for task2 in tasks:
    #             if task2.name == dependency:
    #                 task.children.append(task2)
    #                 task2.parent = task

    export_tasks_to_csv(tasks)