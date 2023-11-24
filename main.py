

# class that describes a task
class Task:
    def __init__(self, name, description):
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

    def __str__(self):
        return f"{self.name}"

    def to_csv(self):
        if self.dependencies == []: dependencies = ""
        else: dependencies = self.dependencies[0]+":".join(self.dependencies[1:])
        return f"{self.name},{self.description},{self.total_cost},{self.duration},{self.is_milestone},{self.is_deliverable},{dependencies},{self.parent}"

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

# create a class, Acquisition, that inherits from Task
class Acquisition(Task):
    def __init__(self, name, description):
        super().__init__(name, description)
        # an acquisition should have a unit price, a quantity, percent spares
        self.unit_price = 0
        self.quantity = 0
        self.percent_spares = 0

    def to_csv(self):
        return f"{super().to_csv()},{self.unit_price},{self.quantity},{self.percent_spares}"

    def __str__(self):
        return f"Acquisition Task[{self.name}: {self.description}]"

    def print(self):
        print("Acquisition Task ----------")
        super().print()
        print("unit price: ",self.unit_price)
        print("quantity: ",self.quantity)
        print("percent spares: ",self.percent_spares)

# create a class, Labor, that inherits from Task
class Labor(Task):
    def __init__(self, name, description):
        super().__init__(name, description)
        # a labor should have a rate, and a number of hours
        self.rate = 0
        self.hours = 0

    def to_csv(self):
        return f"{super().to_csv()},,{self.rate},{self.hours}"

    def __str__(self):
        return f"Labor Task[{self.name}: {self.description}]"

    def print(self):
        print("Labor Task ----------------")
        super().print()
        print("rate: ",self.rate)
        print("hours: ",self.hours)

if __name__ == '__main__':
    t1 = Task("task1","description1");
    t1.duration = 10;
    t1.total_cost = 100;
    t1.is_milestone = True;
    t1.is_deliverable = False;
    t2 = Acquisition("task2","description2");
    t2.duration = 5;
    t2.total_cost = 50;
    t2.is_milestone = False;
    t2.is_deliverable = False;
    t2.parent = t1;
    t2.unit_price = 1;
    t2.quantity = 10;
    t2.percent_spares = 0.1;

    t3 = Labor("task3","description3");
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