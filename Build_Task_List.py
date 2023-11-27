from main import Task
import csv


# function that finds the index of a task in a list of tasks
def find_task_index_by_name(name:str, tasks:list(Task))->int:
    for i in range(len(tasks)):
        if name == tasks[i].name:
            return i
    return None

# function that find reference to task from list by name
def find_task_by_name(name:str, tasks:list(Task))->Task:
    for task in tasks:
        if task.name == name:
            return task
    return None


# function that reads a csv file and a list of tasks that are each a list of strings,
# one corresponding to each column in the csv file
def read_tasks(filename="data/ACORN_DAC_costing_Labor_costs.csv":str)->list(list(str)):
    # read csv file
    with open(filename, "r") as f:
        reader = csv.reader(f)
        task_list = list(reader)
    return task_list[1:]


# function that reads a csv file and appends a tasks with Labor tasks
def read_labor_tasks(tasks=[]:list(Task), mapping={}:dict, filename="data/ACORN_DAC_costing_Labor_costs.csv":str):
    tasks_dict = {"204.03.02":[],
                  "204.03.03":[]}
    for task in tasks:
        if "204.03.02" in task.name :
            tasks_dict["204.03.02"].append(task)
        elif "204.03.03" in task.name:
            tasks_dict["204.03.03"].append(task)
        else:
            print("error, task code not recognized")

    task_list = read_tasks(filename)

    # create a list of tasks
    for task in task_list:
        if task[1] == "":
            continue
        task_key = ""
        if "204.03.02" in task[0]:
            task_key = "204.03.02"
            temp = Task("204.03.02.{0}".format(int(len(tasks_dict["204.03.02"]) + 1)), task[1]+"; "+task[2], False)
            tasks_dict["204.03.02"].append(temp)
        elif "204.03.03" in task[0]:
            task_key = "204.03.03"
            temp = Task("204.03.03.{0}".format(int(len(tasks_dict["204.03.03"]) + 1)), task[1]+task[2], False)
            tasks_dict["204.03.03"].append(temp)
        else:
            print("error, task code not recognized")
            print(" ".join(task))
            continue

        tasks_dict[task_key][-1].rate = float(task[mapping['rate']])
        tasks_dict[task_key][-1].hours = float(task[mapping['hours']])
        tasks_dict[task_key][-1].total_cost = float(task[mapping['rate']]) * float(task[mapping['hours']])
        tasks_dict[task_key][-1].duration = float(task[mapping['duration']])
        tasks_dict[task_key][-1].dependencies.extend(task[mapping['dependencies']].split(";"))
        tasks.append(tasks_dict[task_key][-1])
        print(tasks[-1])


# function that read a csv file and appends tasks with Acquisition tasks
def read_acquisition_tasks(tasks=[]: list(Task), mapping={}:dict, filename="data/ACORN_DAC_costing_MandS_costs.csv":str):
    tasks_dict = {"204.03.02":[],
                  "204.03.03":[]}
    for task in tasks:
        if "204.03.02" in task.name :
            tasks_dict["204.03.02"].append(task)
        elif "204.03.03" in task.name:
            tasks_dict["204.03.03"].append(task)
        else:
            print("error, task code not recognized")
    task_list = read_tasks(filename)

    # create a list of tasks
    for task in task_list:
        task_key = ""
        if task[1] == "":
            continue
        if "204.03.02" in task[0]:
            task_key = "204.03.02"
            temp = Task("204.03.02.{0}".format(int(len(tasks_dict["204.03.02"]) + 1)), task[1]+"; "+task[2], True)
            tasks_dict["204.03.02"].append(temp)
        elif "204.03.03" in task[0]:
            task_key = "204.03.03"
            temp = Task("204.03.03.{0}".format(int(len(tasks_dict["204.03.03"]) + 1)), task[1]+task[2], True)
            tasks_dict["204.03.03"].append(temp)
        else:
            print("error, task code not recognized")
            print(" ".join(task))
            continue

        tasks_dict[task_key][-1].quantity = float(task[mapping['quantity']])
        tasks_dict[task_key][-1].unit_price = float(task[mapping['unit_price']])
        tasks_dict[task_key][-1].percent_spares = float(task[mapping['percent_spares']])
        tasks_dict[task_key][-1].total_cost = float(task[mapping['unit_price']]) * float(task[mapping['quantity']]) * (1 + float(task[mapping['percent_spares']])/100)
        tasks_dict[task_key][-1].duration = float(task[mapping['duration']])
        tasks_dict[task_key][-1].dependencies.extend(task[mapping['dependencies']].split(";"))
        tasks_dict[task_key][-1].dependencies.extend(task[mapping['dependencies']+1].split(";"))

        tasks.append(tasks_dict[task_key][-1])
        print(tasks[-1])


# function that writes a list of tasks to a csv file
# each line is a unique task; columns are formatted
# according to the to_csv() method of the object
def export_tasks_to_csv(tasks=[]:List(Task)):
    with open("data/tasks.csv", "w") as f:
        f.write("name,description,total_cost,duration,is_milestone,is_deliverable,parent,is_acquisition,unit_price,quantity,percent_spares,rate,hours,dependencies\n")
        for task in tasks:
            f.write(task.to_csv() + "\n")
    for task in tasks:
        print(task.to_csv())

    f.close()


if __name__ == '__main__':
    # set CVS mapping for inputs from Excel
    labor_mapping = {"name": 0, "description": 1, "hours": 2, "duration": 3, "rate": 4, "total_cost": 5,
                     "contingency": 6, "dependencies": 7}
    acquisition_mapping = {"name": 0, "description": 1, "quantity": 2, "percent_spares": 3, "total_number": 4,
                           "unit_price": 5, "total_cost": 6, "duration": 7,
                           "dependencies": 8, "contingency": 10}
    tasks = []
    read_labor_tasks(tasks)
    read_acquisition_tasks(tasks)
    export_tasks_to_csv(tasks)
