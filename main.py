

# class that describes a task
class Task:
    def __init__(self, name, description, is_acquisition=False):
        self.name = name
        self.description = description
        # a task should have a name, a total_cost, a duration, can be a mileston or not,
        # can be a deliverable or not, has a list of dependencies, and a parent task
        self.total_cost = 0
        self.duration = 0
        self.is_milestone = False
        self.is_deliverable = False
        self.dependencies = []
        self.parent = None
        self.children = []
        self.is_acquisition = is_acquisition
        # an acquisition task should have a unit price, a quantity, percent spares
        self.unit_price = 0
        self.quantity = 0
        self.percent_spares = 0
        # a labor task should have a rate, and a number of hours
        self.rate = 0
        self.hours = 0
        # a mapping of the csv file columns to the object attributes
        # below are the mapping used by this class for exporting to CSV
        self.mapping = {"name":0,"description":1,"total_cost":2,"duration":3,"is_milestone":4,"is_deliverable":5,"parent":6,"is_acquisition":7,"unit_price":8,"quantity":9,"percent_spares":10,"rate":11,"hours":12,"dependencies":13}

    def __str__(self):
        return f"{self.name}:{self.description}"

    def to_csv(self):
        if self.dependencies == []: dependencies = ""
        else: dependencies = self.dependencies[0]+";".join(self.dependencies[1:])
        return f"{self.name},{self.description},{self.total_cost},{self.duration},{self.is_milestone},{self.is_deliverable},{self.parent},{self.is_acquisition},{self.unit_price},{self.quantity},{self.percent_spares},{self.rate},{self.hours},{dependencies}"

    def print(self):
        print("--------------------")
        print(self.name,": ",self.description)
        print("total cost: ",self.total_cost)
        print("duration: ",self.duration)
        print("milestone: ",self.is_milestone)
        print("deliverable: ",self.is_deliverable)
        print("dependencies: ","".join(list(map(str,self.dependencies))))
        print("parent: ",self.parent)
        print("children: ","".join(list(map(str,self.children))))
        print("is acquisition: ",self.is_acquisition)
        print("--------------------")
        print("unit price: ", self.unit_price)
        print("quantity: ", self.quantity)
        print("percent spares: ", self.percent_spares)
        print("--------------------")
        print("rate: ", self.rate)
        print("hours: ", self.hours)

    def get_total_cost(self):
        return self.total_cost

if __name__ == '__main__':
    t1 = Task("task1","description1");
    t1.duration = 10;
    t1.total_cost = 100;
    t1.is_milestone = True;
    t1.is_deliverable = False;
    t2 = Task("task2","description2");
    t2.is_acquisition=True;
    t2.duration = 5;
    t2.total_cost = 50;
    t2.is_milestone = False;
    t2.is_deliverable = False;
    t2.parent = t1;
    t2.unit_price = 1;
    t2.quantity = 10;
    t2.percent_spares = 0.1;

    t3 = Task("task3","description3",False);
    t3.duration = 5;
    t3.total_cost = 50;
    t3.is_milestone = False;
    t3.is_deliverable = False;
    t3.parent = t1;
    t3.rate = 10;
    t3.hours = 5;

    t1.print();

    t2.print();

    t3.print();