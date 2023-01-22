import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

class Task:
    def __init__(self, task_number = None, username = None, title = None, description = None, due_date = None, assigned_date = None, completed = False): #Add number variable 
        '''
        Inputs:
        username: String
        title: String
        description: String
        due_date: DateTime
        assigned_date: DateTime
        completed: Boolean
        '''
        #number variable needs adding
        self.task_number = task_number
        self.username = username
        self.title = title
        self.description = description
        self.due_date = due_date
        self.assigned_date = assigned_date
        self.completed = completed

    def from_string(self, task_str):
        '''
        Convert from string in tasks.txt to object
        '''
        tasks = task_str.split(";")
        #add number variable
        task_number = tasks[0]
        username = tasks[1]
        title = tasks[2]
        description = tasks[3]
        due_date = datetime.strptime(tasks[4], DATETIME_STRING_FORMAT)
        assigned_date = datetime.strptime(tasks[5], DATETIME_STRING_FORMAT)
        completed = True if tasks[6] == "Yes" else False
        self.__init__(task_number, username, title, description, due_date, assigned_date, completed) #add number variable


    def to_string(self):
        '''
        Convert to string for storage in tasks.txt
        '''
        str_attrs = [
            #add number variable
            self.task_number,
            self.username,
            self.title,
            self.description,
            self.due_date.strftime(DATETIME_STRING_FORMAT),
            self.assigned_date.strftime(DATETIME_STRING_FORMAT),
            "Yes" if self.completed else "No"
        ]
        return ";".join(str_attrs)

    def display(self):
        '''
        Display object in readable format
        '''
       #add number variable
        disp_str = f"Task Number: \t {self.task_number}\n"
        disp_str = f"Task: \t\t {self.title}\n"
        disp_str += f"Assigned to: \t {self.username}\n"
        disp_str += f"Date Assigned: \t {self.assigned_date.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {self.due_date.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \t{self.description}\n"
        return disp_str
        


# Read and parse tasks.txt
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

#Read from tasks.txt
with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]
    

task_list = []
for t_str in task_data:
    curr_t = Task()
    curr_t.from_string(t_str)
    task_list.append(curr_t)

# Read and parse user.txt

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

# Keep trying until a successful login
logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

#Validate strings
def validate_string(input_str):
    '''
    Function for ensuring that string is safe to store
    '''
    if ";" in input_str:
        print("Your input cannot contain a ';' character")
        return False
    return True

#Check username and passwords
def check_username_and_password(username, password):
    '''
    Ensures that usernames and passwords can't break the system
    '''
    # ';' character cannot be in the username or password
    if ";" in username or ";" in password:
        print("Username or password cannot contain ';'.")
        return False
    return True

#Write usernames to text file
def write_usernames_to_file(username_dict):
    '''
    Function to write username to file

    Input: dictionary of username-password key-value pairs
    '''
    with open("user.txt", "a") as out_file:
        user_data = []
        for k in username_dict:
            user_data.append(f"{k};{username_dict[k]}")
        out_file.write("\n".join(user_data))

#function to add current user        
def reg_user(curr_user):
    # Request input of a new username
    if curr_user != 'admin':
        print("Registering new users requires admin privileges")
    
    #Request user enter username and check if username already exists
    new_username = input("New Username: ")
    while new_username in username_password:
        print("User already registered")
        new_username = input("New Username: ") #If username already exists, program will ask for a new username
        
    # Request input of a new password
    new_password = input("New Password: ")

    #if not check_username_and_password(new_username, new_password):
    #   Username or password is not safe for storage continue
    
    # Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # If they are the same, add them to the user.txt file,
        print("New user added")

        # Add to dictionary and write to file
        username_password[new_username] = new_password
        write_usernames_to_file(username_password)

    # Otherwise you present a relevant message.
    else:
            print("Passwords do no match")

#function to add a task
def add_task():
    # Prompt a user for the following: 
    #     A number to be added to the task
    #     A username of the person whom the task is assigned to,
    #     A title of a task,
    #     A description of the task and 
    #     the due date of the task.

   
    # Ask for username
    task_username = input("Name of person assigned to task: ")
    while task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")

    #Add a number for the task  
    last_number = [line for line in task_data if 'Title' in line]
    number = str(len(last_number)+1)
    print(f"Task Number: {number}")
    # Get title of task and ensure safe for storage
    while True:
        task_title = input("Title of Task: ")
        if validate_string(task_title):
            break

    # Get description of task and ensure safe for storage
    while True:
        task_description = input("Description of Task: ")
        if validate_string(task_description):
            break

    # Obtain and parse due date
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Obtain and parse current date
    curr_date = date.today()
    
    #number variable to add 1    
    # Create a new Task object and append to list of tasks
    new_task = Task(number, task_username, task_title, task_description, due_date_time,curr_date, False) #add number variable
    task_list.append(new_task)

    
    # Write to tasks.txt
    with open("tasks.txt", "a") as task_file:
       
        task_file.write("\n".join([t.to_string() for t in task_list]))
    print("Task successfully added.")    

complete = []

#function for marking complete
def mark_as_complete():
    complete = True
    return complete

#function to view all the tasks
def view_all():
    print("-----------------------------------")

    if len(task_list) == 0:
        print("There are no tasks.")
        print("-----------------------------------")
    else:
        task_number_selection = input("Please select a task number: ")
        for t in task_list:
            print(t.display())
            print("-----------------------------------")
            task_completion_option = input("Would you like to mark this task as complete? Y/N: ")
            if task_completion_option.lower() == "y":
                completion = mark_as_complete()
                return completion
            else:
                continue

#function to view tasks of the current user
def view_mine():
    print("-----------------------------------")
    has_task = False
    for t in task_list:
        if t.username == curr_user:
            has_task = True
            print(t.display())
            print("-----------------------------------")

    if not has_task:
        print("You have no tasks.")
        print("-----------------------------------")


#function to generate 2 reports in txt files
def generate_report():
#First report is task_view.txt
    num_users = len(username_password.keys())
    num_tasks = len(task_list)
    task_complete = complete.count("yes")
    task_not_complete = complete.count("no")
    complete_overdue = complete.count("Yes") 
    percentage_incomplete = (num_tasks - task_complete) * 100  
    percentage_overdue = (num_tasks - complete_overdue) * 100
    with open('task_overview.txt', 'w') as task_overview:
        task_overview.writelines("The total number of tasks generated is: " + str(num_tasks) + "\n")
        task_overview.writelines("The total number of tasks completed is: " + str(task_complete) + "\n")
        task_overview.writelines("The total task not completed is: " + str(task_not_complete) +"\n")
        task_overview.writelines("The total number of tasks complete but overdue is: " + str(complete_overdue) + "\n")
        task_overview.writelines("The percentage of tasks incomplete is: " + str(percentage_incomplete) + "% \n")
        task_overview.writelines("The percentage of tasks overdue is: " + str(percentage_overdue) + "% \n")

 #second report is user_overview.txt
    user_tasks = 0
    for user in task_data:
      if curr_user in task_list:
        user_tasks = (user_tasks + 1) * 100
    user_percent = (num_tasks - user_tasks) * 100
    user_complete = 0
    for user in task_data:
        if curr_user == complete:
            user_complete = (user_complete + 1) * 100
    user_not_complete = 0
    for user in task_data:
        if curr_user != complete:
            user_not_complete = (user_not_complete + 1) * 100 
    user_remaining = (user_tasks - user_complete) * 100
    with open('user_overview.txt', 'w') as user_overview:
        user_overview.write("Total numbers of users are: " + str(num_users) + "\n")
        user_overview.write("Total number of tasks tracked is: " + str(num_tasks) + "\n")
        user_overview.write(f"Total number of tasks assigned to {curr_user} is {user_tasks} \n")
        user_overview.write("Percentage of tasks assinged to user: " + str(user_percent) + "% \n")
        user_overview.write("Percentage of tasks complete by user: " + str(user_complete) + "% \n")
        user_overview.write("Percentage of tasks not complete by user: " + str(user_not_complete) + "% \n")
        user_overview.write("Percentage of tasks outstanding and overdue is: " + str(user_remaining) + "% \n")


 
 
#########################
# Main Program
######################### 

while True:
    # Get input from user
    print()
    if curr_user == 'admin':
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - view my task
    gr - generate reports
    ds - display statistics
    e - Exit
    : ''').lower()
    else:
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - view my task
    e - Exit
    : ''').lower()

    if menu == 'r': # Register new user (if admin)
        x = reg_user(curr_user)

    elif menu == 'a': # Add a new task
        x = add_task()

    elif menu == 'va': # View all tasks
        x = view_all()

    elif menu == 'vm': # View my tasks
        vm_user = int(input("Please select task number or -1 to return to menu: "))
        if vm_user == int(-1):
            continue
        else:
            x = view_mine()

    elif menu == 'gr': #Generate reports
        x = generate_report()

    elif menu == 'ds' and curr_user == 'admin': # If admin, display statistics
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")

        #call generate report
        x = generate_report()

        #read and print both reports
        with open('user_overview.txt','r') as user_report:
            users = user_report.readlines()
            for line in users:
                print(line)
        print("-----------------------------------")
        
        with open('task_overview.txt', 'r') as task_report:
            tasks = task_report.readlines()
            for line in tasks:
                print(line)
        print("-----------------------------------")


    elif menu == 'e': # Exit program
        print('Goodbye!!!')
        exit()

    else: # Default case
        print("You have made a wrong choice, Please Try again")
    
