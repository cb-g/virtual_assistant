import os, sys, json
from datetime import date, datetime, timedelta
from pprint import pprint

class schedule:
    def __init__(self, 
                 path_directory: str = "src/RAS/data/", 
                 filename_template: str = "template.json", 
                 filename_data: str = "data.json", 
                 filename_history: str = "history.json",
                 exclude: bool = False,
                 to_be_excluded: list = [
                     "activity C",
                     "activity H",
                     ],
                 ):
        self.p_d = path_directory
        self.f_t = filename_template
        self.f_d = filename_data
        self.f_h = filename_history
        self.exclude = exclude
        self.to_be_excluded = to_be_excluded

        with open(self.p_d + self.f_t, "r") as f: 
            self.template = json.load(f) 

        self.subdictionary_keys = [] 
        for value in self.template.values(): 
            if isinstance(value, dict): 
                self.subdictionary_keys.extend(value.keys())
                break
            
        for n in self.subdictionary_keys: 
            vars = n.replace(":", "").replace(" ", "_") 
            setattr(self, vars, n) 

    def json_exists(self, file) -> bool:
        path = os.path.join(self.p_d, file)
        return os.path.exists(path)
    
    def keys_and_values(self):
        vars = []
        s = []
        for n, v in self.template.items():
            u = n.replace(" ", "_").replace("-", "_") 
            setattr(self, u, v) 
            vars.append(u) 
            s.append(n)
            
        return vars, s
    
    def read_history(self, dict):
        if not self.json_exists(self.f_h):
            empty_history = {}
            with open(self.p_d + self.f_h, 'w') as file:
                json.dump(empty_history, file)

        if self.json_exists(self.f_h):
            with open(self.p_d + self.f_h, "r") as f:
                self.history = json.load(f)
            
            _, s = self.keys_and_values()

            for n in s:
                try:
                    if self.history[n][self.last_date] != "":
                        dict[n][self.last_date] = self.history[n][self.last_date]
                except KeyError:
                    pass

    def create_json(self):
        self.read_history(dict = self.template)

        with open(self.p_d + self.f_d, "w") as f:
            json.dump(self.template, f)

    def str_to_date(self, s):
        return datetime.strptime(s, '%Y-%m-%d').date()
    
    def date_to_string(self, d):
        return d.strftime('%Y-%m-%d')
    
    def update_json(self):
        with open(self.p_d + self.f_d, "r") as f:
            self.data = json.load(f)

        self.read_history(dict = self.data)

        _, tasks = self.keys_and_values()
        if self.exclude == True:
            tasks = [x for x in tasks if x not in self.to_be_excluded]

        my_list = []
        string_dict = {}
        while True:
            for i, tsk in enumerate(tasks):
                print(f"{i+1}: {tsk}")
                string_dict[i+1] = tsk
            print('\n(Enter "p" to proceed)')
            print("___________________________")
            user_input = input("\nWhich one did you do today? Enter number:\n\n")

            if user_input.lower() == "p":
                print("\n")
                break

            selected_string = string_dict.get(int(user_input))
            my_list.append(selected_string)

            print("\n")

        for element in my_list: 
            try:
                self.data[element][self.last_date] = self.date_to_string(date.today())
            except KeyError:
                user_input = input("A key couldn't be found. Overwrite history.json before deleting data.json? (y/n): ")

                if user_input.lower() == "y":
                    with open(self.p_d + self.f_h, "w") as f:
                        json.dump(self.data, f)
                    print("\n")

                    os.remove(self.p_d + self.f_d)

                    with open(self.p_d + self.f_t, "r") as f:
                        self.data = json.load(f)
                    
                    self.read_history(dict = self.data)
                
                else:
                    sys.exit()

        subset = {key: value for key, value in self.data.items() if key in tasks}

        for tsk in subset.keys():
            if subset[tsk][self.last_date] != "":
                subset[tsk][self.min_date] = self.date_to_string(self.str_to_date(subset[tsk][self.last_date]) + timedelta(days=subset[tsk][self.min_int]))
                subset[tsk][self.max_date] = self.date_to_string(self.str_to_date(subset[tsk][self.last_date]) + timedelta(days=subset[tsk][self.max_int]))
                subset[tsk][self.due_date] = self.date_to_string(self.str_to_date(subset[tsk][self.min_date]) + (self.str_to_date(subset[tsk][self.max_date]) - self.str_to_date(subset[tsk][self.min_date]))/2)
                subset[tsk][self.due_int] = (self.str_to_date(subset[tsk][self.due_date]) - date.today()).days
                subset[tsk][self.last_int] = (date.today() - self.str_to_date(subset[tsk][self.last_date])).days
                subset[tsk][self.rest_date] = self.date_to_string(self.str_to_date(subset[tsk][self.min_date]) - timedelta(days=1))
                subset[tsk][self.rest_int] = (self.str_to_date(subset[tsk][self.rest_date]) - date.today()).days
                subset[tsk][self.overdue_date] = subset[tsk][self.max_date]
                subset[tsk][self.overdue_int] = (date.today() - self.str_to_date(subset[tsk][self.overdue_date])).days

        with open(self.p_d + self.f_d, "w") as f:
            json.dump(subset, f)

    def save_data(self):
        if not self.json_exists(self.f_d):
            self.create_json()

        self.update_json()

    def sort_tasks(self, tasks, category, reverse=True):
        tasks_dict = {}
        for tsk in tasks:
            if self.data[tsk][category] != "":
                tasks_dict[tsk] = self.data[tsk][category]
        return sorted(tasks_dict, key=lambda x: tasks_dict[x], reverse=reverse)
    
    def schedule(self):
        if not self.json_exists(self.f_d): 
            return
        
        with open(self.p_d + self.f_d, "r") as f:
            self.data = json.load(f)

        _, tasks = self.keys_and_values()
        if self.exclude == True:
            tasks = [x for x in tasks if x not in self.to_be_excluded]

        print("REST FOR:")
        for tsk in self.sort_tasks(tasks, self.rest_int, True): 
            if self.data[tsk][self.rest_int] != "":
                if int(self.data[tsk][self.rest_int]) > 1:
                    print(f"{self.data[tsk][self.rest_int]} more days: {tsk}")
                elif int(self.data[tsk][self.rest_int]) == 1:
                    print(f"{self.data[tsk][self.rest_int]} more day: {tsk}")
        print("\n")

        print("DUE IN:")
        for tsk in self.sort_tasks(tasks, self.due_int, True):  
            if self.data[tsk][self.due_int] != "":
                if int(self.data[tsk][self.due_int]) > 1:
                    print(f"{self.data[tsk][self.due_int]} days: {tsk}")
                elif int(self.data[tsk][self.due_int]) == 1:
                    print(f"{self.data[tsk][self.due_int]} day: {tsk}")
        print("\n")

        print("DUE TODAY:")
        for tsk in tasks:
            if self.data[tsk][self.due_int] != "":
                if int(self.data[tsk][self.due_int]) == 0 & int(self.data[tsk][self.overdue_int]) <= 0:
                    print(f"{tsk}")
        print("\n")

        print("OVERDUE SINCE:")
        for tsk in self.sort_tasks(tasks, self.overdue_int, False):
            if self.data[tsk][self.overdue_int] != "":
                if int(self.data[tsk][self.overdue_int]) > 1:
                    print(f"{int(self.data[tsk][self.overdue_int])} days: {tsk}")
                elif int(self.data[tsk][self.overdue_int]) == 1:
                    print(f"{int(self.data[tsk][self.overdue_int])} day: {tsk}")

        if self.exclude == True:
            with open(self.p_d + self.f_h, "r") as f:
                unabridged_dict = json.load(f)
            for key in unabridged_dict.keys():
                if key not in self.data:
                    self.data[key] = unabridged_dict[key]
            with open(self.p_d + self.f_d, "w") as f:
                json.dump(self.data, f) 
        if self.exclude == False:
            with open(self.p_d + self.f_d, "w") as f:
                json.dump(self.data, f) 
        
        print("\n")

    def save_history(self):
        user_input = input("Overwrite history.json? (y/n): ")

        if self.exclude == False:
            if user_input.lower() == "y":
                with open(self.p_d + self.f_h, "w") as f:
                    json.dump(self.data, f)
            print("\n")

        if self.exclude == True:
            if user_input.lower() == "y":
                with open(self.p_d + self.f_h, "r") as f:
                    unabridged_dict = json.load(f)
                for key in unabridged_dict.keys():
                    if key not in self.data:
                        self.data[key] = unabridged_dict[key]
                with open(self.p_d + self.f_h, "w") as f:
                    json.dump(self.data, f)
            print("\n")
