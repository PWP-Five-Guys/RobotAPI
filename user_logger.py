import datetime

user_log = "login_record.log"
current_user = None

def update_record(line):
    with open(user_log, "a") as f:
        f.write(f"{str(datetime.datetime.now())[:-4]} - {line}\n")

def update_login(username, action):
    match action:
        case "login":
            update_record(f"LOGIN - user '{username}' logged in")
            global current_user
            current_user = username
        case "register":
            update_record(f"LOGIN - user '{username}' created account")
        case "delete":
            update_record(f"LOGIN - user '{username}' deleted account")

def update_api(command):
    update_record(f"API - '{current_user}' sent a command: {str(command)}")