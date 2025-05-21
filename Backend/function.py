from json import *
import json
from groq import Groq
import datetime


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
        data = json.load(file)

    # Check if phantom code already exists for another user
    for user in data['users']:
        if user.get('phantom_code') == code and user.get('username') != username:
            print("Phantom code already used by another user.")
            return False

    # Update the current user's data
    for user in data['users']:
        if user['username'] == username:
            user['phantom_code'] = code
            user['system_prompt'] = sys
            break

    # Save updated data
    with open('Data/id_pass.json', 'w') as file:
        json.dump(data, file, indent=4)

    print("System prompt and phantom code updated successfully.")
    return True

def get_user_data(username):
    with open('Data/id_pass.json', 'r') as file:
        data = load(file)

        for user in data["users"]:
            if user["username"] == username:
                return {
                    "system_prompt": user["system_prompt"],
                    "phantom_code": user["phantom_code"]
                }

        # Log if the username was not found
        print(f"User '{username}' not found in the data.")
        return None

def Ai(query, username):
    import datetime
    from groq import Groq
    import json

    client = Groq(api_key="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") # Store your API key securely as an environment variable

    def RealtimeInformation():
        now = datetime.datetime.now()
        return (
            f"Please use this real-time information if needed:\n"
            f"Day: {now.strftime('%A')}\n"
            f"Date: {now.strftime('%d')}\n"
            f"Month: {now.strftime('%B')}\n"
            f"Year: {now.strftime('%Y')}\n"
            f"Time: {now.strftime('%H')} hours : {now.strftime('%M')} minutes : {now.strftime('%S')} seconds.\n"
        )

    def AnswerModifier(answer):
        return '\n'.join([line for line in answer.split('\n') if line.strip()])

    try:
        with open("Data/id_pass.json", "r") as f:
            data = json.load(f)
    except Exception as e:
        print("❌ Failed to load user data:", e)
        return "Error: Could not load user data."

    # Identify user and load prompt + chat history
    user_found = False
    for user in data["users"]:
        if user.get("username", "") == username:
            system_prompt = user.get("system_prompt", "You are a helpful assistant.")
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "system", "content": RealtimeInformation()}
            ]
            for chat in user.get("chats", []):
                messages.append({"role": "user", "content": chat.get("question", "")})
                messages.append({"role": "assistant", "content": chat.get("answer", "")})
            user_found = True
            break

    if not user_found:
        print("❌ Username not found.")
        return "Error: Invalid username."

    messages.append({"role": "user", "content": query})

    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages,
            stream=True,
            max_tokens=1024,
            temperature=0.7,
            top_p=1
        )

        answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content

        answer = answer.replace("</s>", "")
        clean_answer = AnswerModifier(answer)

        # Save new chat
        for user in data["users"]:
            if user.get("username", "") == username:
                if "chats" not in user:
                    user["chats"] = []
                user["chats"].append({"question": query, "answer": clean_answer})
                break

        with open("Data/id_pass.json", "w") as f:
            json.dump(data, f, indent=4)

        return clean_answer

    except Exception as e:
        print("❌ AI service error:", str(e))
        return "Error: AI service failed."

def get_chat_history(username):
    try:
        with open("Data/id_pass.json", "r") as f:
            data = json.load(f)
    except Exception as e:
        print("❌ Failed to load user data:", e)
        return "Error: Could not load user data."

    # Find the user and retrieve their chat history
    user_found = False
    for user in data["users"]:
        if user.get("username", "") == username:
            user_found = True
            chat_history = user.get("chats", [])
            break

    if not user_found:
        print("❌ Username not found.")
        return "Error: Invalid username."

    # Format chat history for display
    if chat_history:
        history = []
        for chat in chat_history:
            history.append(f"Q: {chat.get('question', '')}\nA: {chat.get('answer', '')}\n")
        return "\n".join(history)
    else:
        return "No chat history found for this user."