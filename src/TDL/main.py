import json
import os

class Task:
    def __init__(self, description, deadline):
        self.description = description
        self.deadline = deadline

def print_tasks(tasks):
    print("tasks:")
    for index, task in enumerate(tasks, start=1):
        print("\n")
        print(f"{index}. {task.description} (deadline: {task.deadline})")

def add_task(tasks, new_task):

    if tasks:
        print("select a task before/after which to insert the new task:")
    
    if not tasks:
        # print("No tasks found. The new task will be added as the first task.")
        tasks.append(new_task)
        print("task added successfully!")
        return

    print_tasks(tasks)
    try:
        position = int(input("\n\nenter the task number before/after which to insert the new task: ")) - 1
        choice = input("\ndo you want to add the task before or after the selected task? (b/a): ").lower()
        
        if 0 <= position < len(tasks):
            if choice == "b":
                tasks.insert(position, new_task)
            elif choice == "a":
                tasks.insert(position + 1, new_task)
            else:
                print("\ninvalid choice. task not added.")
                return
            print("\ntask added successfully!")
        else:
            print("\ninvalid task number. task not added.")
    except (ValueError, IndexError):
        print("\ninvalid input. task not added.")

def delete_task(tasks):
    print("\nselect a task to delete:")
    print_tasks(tasks)
    try:
        position = int(input("\nenter the task number: ")) - 1
        if 0 <= position < len(tasks):
            removed_task = tasks.pop(position)
            print(f"task '{removed_task.description}' deleted.")
        else:
            print("\ninvalid task number.")
    except ValueError:
        print("\ninvalid input. task not deleted.")

def save_tasks(tasks, filename):
    with open(filename, "w") as file:
        json.dump([task.__dict__ for task in tasks], file)

def load_tasks(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            tasks = [Task(task["description"], task["deadline"]) for task in data]
            return tasks
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def modify_task(tasks):
    print("\nselect a task to modify:")
    print_tasks(tasks)
    try:
        position = int(input("\n\nenter the number of the task to be modified: ")) - 1
        if 0 <= position < len(tasks):
            task_to_modify = tasks[position]
            print(f"\nselected task: {task_to_modify.description} (deadline: {task_to_modify.deadline})")
            
            new_description = input("\nenter new task description (leave empty aka just hit enter to keep current): ")
            new_deadline = input("\nenter new task deadline (leave empty aka just hit enter to keep current): ")
            
            if new_description:
                task_to_modify.description = new_description
            if new_deadline:
                task_to_modify.deadline = new_deadline
                
            print("\ntask modified successfully!")
        else:
            print("\ninvalid task number.")
    except ValueError:
        print("\ninvalid input. task not modified.")

def clear_terminal():
    os.system("clear")

def main():
    filename = "src/TDL/data/tasks.json"
    tasks = load_tasks(filename)

    while True:
        print("\n\noptions:\n")
        print("1. just show tasks and don't quit")
        print("2. add task")
        print("3. delete task")
        print("4. modify task")
        print("5. show tasks, save and quit")
        print("6. quit without saving changes")

        choice = input("\nenter your choice: ")

        if choice == "1":
            clear_terminal()
            print_tasks(tasks)
        elif choice == "2":
            clear_terminal()
            description = input("\nenter task description: ")
            deadline = input("\nenter task deadline: ")
            new_task = Task(description, deadline)
            add_task(tasks, new_task)
            clear_terminal()
        elif choice == "3":
            clear_terminal()
            delete_task(tasks)
        elif choice == "4": 
            clear_terminal()
            modify_task(tasks)
        elif choice == "5": 
            clear_terminal()
            save_tasks(tasks, filename)
            print("\n")
            print_tasks(tasks)
            print("\n\ntasks saved.\n\n")
            break
        elif choice == "6":
            clear_terminal()
            print("\n")
            print_tasks(tasks)
            print("\n\nexited without saving changes.\n\n")
            break
        else:
            print("\ninvalid choice. please select a valid option.")

if __name__ == "__main__":
    main()