from Build_Task_List import *
from main import Task

def import_tasks(tasks=[], mapping={}, filename="data/tasks.csv"):
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
        if task[mapping['description']] == "":
            continue
        if "204.03.02" in task[mapping['name']]:
            task_key = "204.03.02"
            temp = Task("204.03.02.{0}".format(int(len(tasks_dict["204.03.02"]) + 1)), task[mapping['description']], True)
            tasks_dict["204.03.02"].append(temp)
        elif "204.03.03" in task[mapping['name']]:
            task_key = "204.03.03"
            temp = Task("204.03.03.{0}".format(int(len(tasks_dict["204.03.03"]) + 1)), task[mapping['description']], True)
            tasks_dict["204.03.03"].append(temp)
        else:
            print("error, task code not recognized")
            print(" ".join(task))
            continue

        tasks_dict[task_key][-1].quantity = float(task[mapping['quantity']])
        tasks_dict[task_key][-1].unit_price = float(task[mapping['unit_price']])
        tasks_dict[task_key][-1].percent_spares = float(task[mapping['percent_spares']])
        tasks_dict[task_key][-1].total_cost = float(task[mapping['total_cost']])
        tasks_dict[task_key][-1].duration = float(task[mapping['duration']])
        tasks_dict[task_key][-1].is_milestone = bool(task[mapping['is_milestone']])
        tasks_dict[task_key][-1].is_deliverable = bool(task[mapping['is_deliverable']])
        tasks_dict[task_key][-1].parent = task[mapping['parent']]
        tasks_dict[task_key][-1].is_acquisition = bool(task[mapping['is_acquisition']])
        tasks_dict[task_key][-1].rate = float(task[mapping['rate']])
        tasks_dict[task_key][-1].hours = float(task[mapping['hours']])
        tasks_dict[task_key][-1].dependencies.extend(task[mapping['dependencies']].split(";"))
        #remove empty strings from dependencies
        tasks_dict[task_key][-1].dependencies = list(filter(lambda x : x != "",tasks_dict[task_key][-1].dependencies))

        tasks.append(tasks_dict[task_key][-1])
        print(tasks[-1])

if __name__ == '__main__':
    tasks = []
    mapping = {"name": 0, "description": 1, "total_cost": 2, "duration": 3, "is_milestone": 4, "is_deliverable": 5,
                    "parent": 6, "is_acquisition": 7, "unit_price": 8, "quantity": 9, "percent_spares": 10, "rate": 11,
                    "hours": 12, "dependencies": 13}
    import_tasks(tasks, mapping, "data/tasks.csv")
    total_cost = sum(list(map(lambda t : t.get_total_cost(),tasks)))
    print("total cost: ",total_cost)

