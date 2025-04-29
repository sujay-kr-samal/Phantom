from json import *

def login(username, password):
    with open('Data/id_pass.json', 'r') as file:
        data = load(file)
        for user in data['users']:
            if user['username'] == username and user['password'] == password:
                return True  # The function exits here if the user is found
    return False

def signup(username, password):
    # Load the existing data from the JSON file
    with open('Data/id_pass.json', 'r') as file:
        data = load(file)

    # Check if the username already exists
    for user in data['users']:
        if user['username'] == username:
            return False  # Prevent adding duplicate usernames

    # If the username does not exist, append the new user to the list
    new_user = {'username': username, 'password': password}
    data['users'].append(new_user)

    # Write the updated data back to the JSON file
    with open('Data/id_pass.json', 'w') as file:
        dump(data, file, indent=4)

    print("Signup successful!")
    return True  # The function exits here if the signup is successful

def sysprompt(username, sys, code):
    with open('Data/id_pass.json', 'r') as file:
        data = load(file)

    # First, check if the phantom code is already used by someone else
    for user in data['users']:
        if user.get('phantom_code') == code and user.get('username') != username:
            print("Phantom code already used by another user.")
            return False

    # Find the user and update their fields
    for user in data['users']:
        if user['username'] == username:
            # Clear previous data
            user['phantom_code'] = None
            user['system_prompt'] = None
            # Assign new data
            user['phantom_code'] = code
            user['system_prompt'] = sys
            break

    # Save changes
    with open('Data/id_pass.json', 'w') as file:
        dump(data, file, indent=4)

    print("System prompt and phantom code updated successfully.")
    return True
