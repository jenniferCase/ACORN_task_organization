from main import Task
import csv

# function that finds the index of a task in a list of tasks
def find_task_index_by_name(name: str, tasks) -> int:
    for i in range(len(tasks)):
        if name == tasks[i].name:
            return i
    return -1


# function that find reference to task from list by name
def find_task_by_name(name: str, tasks) -> Task:
    for task in tasks:
        if task.name == name:
            return task
    return None

def export_tasks_to_csv(tasks = [],outputfile = "data/tasks.csv"):
    with open(outputfile, "w") as f:
        f.write("name,description,total_cost,duration,is_milestone,is_deliverable,parent,is_acquisition,unit_price,quantity,percent_spares,rate,hours,dependencies\n")
        for task in tasks:
            f.write(task.to_csv() + "\n")
    for task in tasks:
        print(task.to_csv())

    f.close()

# function that finds the index of a task in a list of tasks
def find_dependencies(in_partial_descriptions, in_task_list):
    dependencies = []
    for i in range(len(in_task_list)):
        for partial_description in in_partial_descriptions:
            if partial_description in in_task_list[i].description:
                dependencies.append(in_task_list[i].name)
    return dependencies

# function that builds tasks for developing specifications
def build_distribution_tasks(in_distribution_list, in_cnt):
    distribution_tasks = []
    for signal in in_distribution_list:
        in_cnt += 1
        temp_name = "204.03.02." + str(in_cnt)
        temp_description = f"Develop specification for MCH/AMC {signal} distribution"
        specification_task = Task(temp_name, temp_description, False)
        distribution_tasks.append(specification_task)

        in_cnt += 1
        temp_name = "204.03.02." + str(in_cnt)
        temp_description = f"Develop firmware for MCH/AMC {signal} distribution"
        firmware_task = Task(temp_name, temp_description, False, [specification_task.name])
        distribution_tasks.append(firmware_task)
    return [distribution_tasks, in_cnt]

def build_general_AMC_tasks(in_cnt):
    amc_tasks = []
    in_cnt += 1
    temp_name = "204.03.02." + str(in_cnt)
    temp_description = f"Develop specifications for controlling AMCs"
    specification_task = Task(temp_name, temp_description, False)
    amc_tasks.append(specification_task)

    in_cnt += 1
    temp_name = "204.03.02." + str(in_cnt)
    temp_description = f"Develop software for controlling AMCs"
    software_task = Task(temp_name, temp_description, False, [specification_task.name])
    amc_tasks.append(software_task)
    return [amc_tasks, in_cnt]

def build_MCH_integration_tasks(in_cnt, in_task_list):
    mch_tasks = []
    in_cnt += 1
    temp_name = "204.03.02." + str(in_cnt)
    temp_description = f"Integrate MCH and AMC firmware"
    temp_dependencies = find_dependencies(['Develop firmware for MCH/AMC', 'Develop software for controlling AMCs', 'Develop specifications for RTM/AMC interface'], in_task_list)
    integration_task = Task(temp_name, temp_description, False, temp_dependencies)
    mch_tasks.append(integration_task)

    in_cnt += 1
    temp_name = "204.03.02." + str(in_cnt)
    temp_description = f"Test control interfaces betweeen the MCH and AMCs"
    test_task = Task(temp_name, temp_description, False, [integration_task.name])
    mch_tasks.append(test_task)
    return [mch_tasks, in_cnt]

def build_function_specific_firmware(in_types, in_cnt, in_task_list):
    firmware_tasks = []
    for function_type in in_types:
        in_cnt += 1
        temp_name = "204.03.03." + str(in_cnt)
        temp_description = f"Develop specification for {function_type} AMC"
        temp_dependencies = find_dependencies(['Develop specification for MCH/AMC', 'Develop specifications for controlling AMCs', 'Develop specifications for RTM/AMC interface'], in_task_list)
        specification_task = Task(temp_name, temp_description, False, temp_dependencies)
        firmware_tasks.append(specification_task)

        in_cnt += 1
        temp_name = "204.03.03." + str(in_cnt)
        temp_description = f"Develop firmware for {function_type} AMC"
        firmware_task = Task(temp_name, temp_description, False, [specification_task.name])
        firmware_tasks.append(firmware_task)

        in_cnt += 1
        temp_name = "204.03.03." + str(in_cnt)
        temp_description = f"Procure COTS AMC for {function_type} AMC"
        firmware_task = Task(temp_name, temp_description, True, [firmware_task.name])
        firmware_tasks.append(firmware_task)

    return [firmware_tasks, in_cnt]

def build_generic_hardware_tasks(in_part_name, in_cnt, in_task_list):
    hardware_tasks = []
    in_cnt += 1
    temp_name = "204.03.03." + str(in_cnt)
    temp_description = f"Develop specification for {in_part_name}"
    temp_dependencies = find_dependencies(['Develop specifications for RTM/AMC interface'], in_task_list)
    specification_task = Task(temp_name, temp_description, False, temp_dependencies)
    hardware_tasks.append(specification_task)

    in_cnt += 1
    temp_name = "204.03.03." + str(in_cnt)
    temp_description = f"Design schematic for {in_part_name}"
    schematic_task = Task(temp_name, temp_description, False, [specification_task.name])
    hardware_tasks.append(schematic_task)

    in_cnt += 1
    temp_name = "204.03.03." + str(in_cnt)
    temp_description = f"Design board layout for {in_part_name}"
    layout_task = Task(temp_name, temp_description, False, [schematic_task.name])
    hardware_tasks.append(layout_task)

    in_cnt += 1
    temp_name = "204.03.03." + str(in_cnt)
    temp_description = f"Procure {in_part_name}"
    procure_task = Task(temp_name, temp_description, False, [layout_task.name])
    hardware_tasks.append(procure_task)

    in_cnt += 1
    temp_name = "204.03.03." + str(in_cnt)
    temp_description = f"Test {in_part_name}"
    test_task = Task(temp_name, temp_description, False, [procure_task.name])
    hardware_tasks.append(test_task)
    return [hardware_tasks, in_cnt]

def build_hardware_tasks(in_RTM_types, in_connector_types, in_versions, in_cnt02, in_cnt03, in_task_list):
    hardware_tasks = []
    for version in in_versions:
        total_tasks = in_task_list
        if in_RTM_types:
            for rtm_type in in_RTM_types:
                part_name = f'{version} {rtm_type} RTM'
                [temp_tasks, in_cnt03] = build_generic_hardware_tasks(part_name, in_cnt03, in_task_list)
                hardware_tasks.extend(temp_tasks)

        if in_connector_types:
            for connector_type in in_connector_types:
                part_name = f'{version} {connector_type} Connector Daughterboard'
                [temp_tasks, in_cnt03] = build_generic_hardware_tasks(part_name, in_cnt03, in_task_list)
                hardware_tasks.extend(temp_tasks)

        # TODO: AMC Y fab & assembly - must be more than a purchase?

        in_cnt02 += 1
        temp_name = "204.03.02." + str(in_cnt02)
        temp_description = f"Test integration with {version} hardware"
        total_tasks.extend(hardware_tasks)
        temp_dependencies = find_dependencies([f'Test {version}', 'Procure COTS AMC'], total_tasks)
        test_task = Task(temp_name, temp_description, False, temp_dependencies)
        hardware_tasks.append(test_task)
        # NOTE: dependencies between versions need to be added after the fact
    return [hardware_tasks, in_cnt02, in_cnt03]

# declare variables
cnt2040302 = 0
cnt2040303 = 0
task_list = []

# make the task list
# add distribution related tasks
[distribution_tasks, cnt2040302] = build_distribution_tasks(['ACLK','BSCLK','MPS/Beam Permit/Abort','data transmission'], cnt2040302)
task_list.extend(distribution_tasks)

# add general AMC software tasks
[amc_tasks, cnt2040302] = build_general_AMC_tasks(cnt2040302)
task_list.extend(amc_tasks)

# add RTM/AMC interface task
cnt2040303 += 1
temp_name = "204.03.03." + str(cnt2040303)
temp_description = f"Develop specifications for RTM/AMC interface"
specification_task = Task(temp_name, temp_description, False)
task_list.append(specification_task)

# add MCH/AMC integration and testing tasks
[mch_tasks, cnt2040302] = build_MCH_integration_tasks(cnt2040302, task_list)
task_list.extend(mch_tasks)

# add tasks related to vacuum
#TBD

# add firmware tasks for P3 & MTA cards
[firmware_tasks, cnt2040302] = build_function_specific_firmware(['Ramping Power Supply Controller', 'Timing Delays', 'Voltage Readback'], cnt2040302, task_list)
task_list.extend(firmware_tasks)

# add hardware iterations
[hardware_list, cnt2040302, cnt2040303] = build_hardware_tasks(['Ramping Power Supply Controller 12V', 'Digital I/O 5V Fast', 'Voltage ADC'], ['Viking'], ['Prototype', 'Pre-production', 'Production'], cnt2040302, cnt2040303, task_list)
task_list.extend(hardware_list)

for task in task_list:
    print(f'{task.name}\t{task.description}\t{task.dependencies}')

export_tasks_to_csv(task_list,"data/JC_incomplete_test_tasks.csv")