from Build_Task_List import *
from main import Task

if __name__ == '__main__':
    tasks = []
    read_labor_tasks(tasks,"tasks.csv")
    read_acquisition_tasks(tasks,"tasks.csv")
    total_cost = sum(list(map(lambda t : t.get_total_cost(),tasks)))
    print("total cost: ",total_cost)

