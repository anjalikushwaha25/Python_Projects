import datetime
import json
import os
import sqlite3
import hashlib

# ==================== DATABASE ====================

connection = sqlite3.connect("smartdesk.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'customer',
    created_at TEXT NOT NULL
    )
    """)
connection.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id TEXT UNIQUE NOT NULL,
    customer TEXT NOT NULL,
    issue TEXT NOT NULL,
    priority TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
)
""")

connection.commit()

def hash_password(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()

def register_user():
    print("\n" + "=" * 50)
    print("CREATE NEW ACCOUNT")
    print("=" * 50)

    username = input("Enter username:").strip()

    while not username:
        print("username cannot be empty")
        username = input("Enter username:").strip()

    password = input("Enter password:").strip()

    while not password:
        print("password cannot be empty")
        password = input("Enter password:").strip()

    confirm_password = input("Confirm password:").strip()

    if password != confirm_password:
        print("Passwords don't match")
        return False

    hashed_password = hash_password(password)

    created_at = datetime.datetime.now().strftime( "%Y-%m-%d %H:%M:%S"
    )

    try:
        cursor.execute("""
        INSERT INTO users(
        username, password, role, created_at)
        VALUES (?,?,?,?)
        """,(
            username, hashed_password, "customer", created_at
        ))

        connection.commit()
        print("\n✅ Account created successfully!")
        print(f"Username: {username}")

        return True

    except sqlite3.IntegrityError:

        print("\n❌ Username already exists.")
        return False

# ============================================================
# LOGIN USER
# ============================================================

def login_user():

    print("\n" + "=" * 50)
    print("SMARTDESK LOGIN")
    print("=" * 50)

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    hashed_password = hash_password(password)

    cursor.execute("""
        SELECT username, role
        FROM users
        WHERE username = ? AND password = ?
    """, (
        username,
        hashed_password
    ))

    user = cursor.fetchone()

    if user is None:

        print("\n❌ Invalid username or password.")
        return None

    print("\n✅ Login successful!")
    print(f"Welcome, {user[0]}!")

    return {
        "username": user[0],
        "role": user[1]
    }

# ============================================================
# AUTHENTICATION MENU
# ============================================================

def authentication():

    while True:

        print("\n" + "=" * 50)
        print("WELCOME TO SMARTDESK")
        print("=" * 50)

        print("""
1. Login
2. Register
3. Exit
""")

        choice = input("Choose an option: ").strip()

        if choice == "1":

            user = login_user()

            if user is not None:
                return user

        elif choice == "2":

            register_user()

        elif choice == "3":

            print("Goodbye! 👋")
            connection.close()
            exit()

        else:

            print("❌ Invalid choice. Please select 1, 2 or 3.")


#Greeting

current_user = authentication()

name = current_user["username"]
user_role = current_user["role"]


present_hour = datetime.datetime.now().hour

if 5 <= present_hour < 12:
    print(f"Good Morning, {name}!")
elif 12 <= present_hour < 17:
    print(f"Good Afternoon, {name}!")
elif 17 <= present_hour < 21:
    print(f"Good Evening, {name}!")
else:
    print(f"Good Night, {name}!")

print("-"*40)
print("Namaste!!\n Welcome to SmartDesk — Python AI-Style Customer Support Chatbot")
print("-"*40)

print("""
You can ask me basic questions.

Commands.
. view tickets
. serach ticket
. update ticket
. update priority
. delete ticket
. bye/exit/quit
""")

#Bot Responses
intents = {

    "greeting": {
        "keywords": ["hello", "hi", "hey"],
        "response": "Hi! 👋 Welcome to SmartDesk. How can I help you today?"
    },

    "working_hours": {
        "keywords": ["working hours", "office hours", "support hours"],
        "response": "Our support team is available from 9 AM to 6 PM, Monday to Saturday."
    },

    "password": {
        "keywords": ["password", "forgot password", "reset password"],
        "response": "You can reset your password using the 'Forgot Password' option on the login page."
    },

    "agent": {
        "keywords": ["agent", "customer service", "representative"],
        "response": "Sure! I'll create a support request for you."
    },

    "wellbeing": {
        "keywords": ["how are you", "how are you doing"],
        "response": "I am doing very well. Thank you for asking!"
    },

    "identity": {
        "keywords": ["who are you", "what are you"],
        "response": "I am SmartDesk, a Python-based customer support chatbot."
    },

    "motivation": {
        "keywords": ["motivate", "motivation", "give me motivation"],
        "response": "Keep going! 🚀 Every small step takes you closer to your goal."
    },

    "happiness": {
        "keywords": ["happy", "excited", "great"],
        "response": "That's great to hear! 😊"
    }
}

chat_history = []
history_file = "chat_history.json"

if os.path.exists(history_file):
    try:
        with open(history_file,"r")as file:
            chat_history = json.load(file)

    except json.JSONDecodeError:
        print("Chat history file is empty")
        chat_history = []

"""if os.path.exists(ticket_file):
    try:
        with open(ticket_file,"r")as file:
            tickets = json.load(file)

    except json.JSONDecodeError:
        print("Ticket file is empty/corrupted")
        tickets=[] """

def view_tickets():

    print("\n" + "=" * 50)
    print("ALL SUPPORT TICKETS")
    print("=" * 50)

    cursor.execute("""
    SELECT ticket_id, customer,issue,priority, status, created_at
    FROM tickets
    ORDER BY id DESC
    """)

    tickets = cursor.fetchall()

    if not tickets:
        print("No tickets found.")
        return

    for ticket in tickets:

        ticket_id, customer, issue, priority, status, created_at = ticket

        print(f"\nTicket ID : {ticket_id}")
        print(f"Customer  : {customer}")
        print(f"Issue     : {issue}")
        print(f"Priority  : {priority}")
        print(f"Status    : {status}")
        print(f"Created At: {created_at}")
        print("-" * 50)

def search_ticket():

    print("\n" + "=" * 50)
    print("SEARCH SUPPORT TICKET")
    print("=" * 50)

    ticket_id = input("Enter Ticket ID: ").strip().upper()

    cursor.execute("""
    SELECT ticket_id, customer, issue, priority, status, created_at
    FROM tickets
    WHERE ticket_id = ?
    """, (ticket_id,))

    ticket = cursor.fetchone()

    if ticket is None:
        print("❌ Ticket not found.")
        return
    ticket_id, customer, issue, priority, status, created_at = ticket

    print("\nTicket Found! ✅")
    print("-" * 40)
    print(f"Ticket ID : {ticket_id}")
    print(f"Customer  : {customer}")
    print(f"Issue     : {issue}")
    print(f"Priority  : {priority}")
    print(f"Status    : {status}")
    print(f"Created At: {created_at}")
    print("-" * 40)

def create_ticket():
    print("\n"+"="*40)
    print("CREATE SUPPORT TICKET")
    print("="*40)

    issue = input("Describe your issue: ").strip()

    while not issue:
        print("Issue cannot be empty.")
        issue = input("Describe your issue: ").strip()

    priority = input("Select priority(low/medium/high):").lower().strip()

    while priority not in ["low","medium","high"]:
        print("Please select: low,medium,high")
        priority = input("Select priority(low/medium/high):").lower().strip()

    cursor.execute("Select MAX(id) FROM tickets")
    result = cursor.fetchone()[0]

    if result is None:
        next_number = 1001
    else:
        next_number = 1001 + result

    ticket_id = f'INC{next_number}'
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO tickets
    (ticket_id, customer,issue,priority,status,created_at)
    VALUES(?,?,?,?,?,?)
    """,(
        ticket_id, name, issue, priority,"open",created_at
    ))

    connection.commit()

    print("\n🎫 Ticket created successfully!")
    print(f"Ticket ID : {ticket_id}")
    print(f"Customer  : {name}")
    print(f"Priority  : {priority}")
    print("Status    : open")
    print(f"Created At: {created_at}")

def update_ticket_status():

    print("\n" + "=" * 50)
    print("UPDATE TICKET STATUS")
    print("=" * 50)

    ticket_id = input("Enter Ticket ID: ").strip().upper()

    cursor.execute("""
    SELECT status
    FROM tickets
    WHERE ticket_id = ?
    """, (ticket_id,))

    ticket = cursor.fetchone()

    if ticket is None:
        print("Ticket not found.")
        return

    print(f"\nCurrent Status: {ticket[0]}")

    print("""
    Available status:
    1. In progress
    2. Resolved
    3. Closed
    """)

    choice = input("Choose status(1-3)").strip()
    status_options = {
        "1": "in progress",
        "2": "resolved",
        "3": "closed"
    }

    if choice not in status_options:

        print("❌ Invalid choice.")
        return

    new_status = status_options[choice]

    cursor.execute("""
        UPDATE tickets
        SET status = ?
        WHERE ticket_id = ?
    """, (new_status, ticket_id))

    connection.commit()

    print("\n✅ Ticket status updated successfully!")
    print(f"Ticket ID : {ticket_id}")
    print(f"New Status: {new_status}")

def delete_ticket():

    print("\n" + "=" * 50)
    print("DELETE SUPPORT TICKET")
    print("=" * 50)

    ticket_id = input("Enter Ticket ID to delete: ").strip().upper()

    cursor.execute("""
    SELECT ticket_id, customer, issue, priority, status
    FROM tickets
    WHERE ticket_id = ?
    """, (ticket_id,))

    ticket = cursor.fetchone()
    if ticket is None:
        print("❌ Ticket not found.")
        return

    print("\nTicket Found!")
    print(f"Ticket ID : {ticket[0]}")
    print(f"Customer  : {ticket[1]}")
    print(f"Issue     : {ticket[2]}")
    print(f"Priority  : {ticket[3]}")
    print(f"Status    : {ticket[4]}")

    confirmation = input(
        "\nAre you sure you want to delete this ticket? (yes/no): "
    ).lower().strip()

    if confirmation != "yes":

        print("Deletion cancelled.")
        return

    cursor.execute("""
        DELETE FROM tickets
        WHERE ticket_id = ?
    """, (ticket_id,))

    connection.commit()

    print("\n🗑️ Ticket deleted successfully!")


def update_ticket_priority():

    print("\n" + "=" * 50)
    print("UPDATE TICKET PRIORITY")
    print("=" * 50)

    ticket_id = input("Enter Ticket ID:").strip().upper()

    cursor.execute("""
    SELECT priority
    FROM tickets
    WHERE ticket_id = ?
    """,(ticket_id,))

    ticket = cursor.fetchone()

    if ticket is None:
        print("No tickets available.")
        return

    print(f"\nCurrent Priority: {ticket[0]}")

    print("""
    Available Priorities:
    1. Low
    2. MEdium
    3. High
    """)
    choice = input("Choose priority (1-3): ").strip()

    priority_options = {
        "1": "low",
        "2": "medium",
        "3": "high"
    }

    if choice not in priority_options:

        print("❌ Invalid choice.")
        return

    new_priority = priority_options[choice]

    cursor.execute("""
        UPDATE tickets
        SET priority = ?
        WHERE ticket_id = ?
    """, (new_priority, ticket_id))

    connection.commit()

    print("\n✅ Ticket priority updated successfully!")
    print(f"Ticket ID   : {ticket_id}")
    print(f"New Priority: {new_priority}")


def get_Response_of_Bot(userQuestion):
    userQuestion = userQuestion.lower().strip()

    best_intent = None
    highest_score = 0

    for intent in intents:
        score = 0
        keywords = intents[intent]["keywords"]

        for keyword in keywords:

            if keyword in userQuestion:
                if len(keyword.split())>1:
                    score+=2
                else:
                    score+=1
                
        if score>highest_score:
            highest_score = score
            best_intent = intent

    print(f"Detected intent:{best_intent}")
    print(f"Confidence intent:{highest_score}")

    if best_intent is not None:
        response = intents[best_intent]["response"]

        return ( response,
                best_intent,
                highest_score)

    return ("I'm sorry, I don't understand that yet. I'm still learning.", None, 0)

#chat loop 
while True:
    userInput = input("You: ").strip()

    # Exit
    if userInput.lower() in ["bye", "exit", "quit"]:
        print("Bot: Thank you for chatting with SmartDesk! 👋")
        break

    # View all tickets
    if userInput.lower() == "view tickets":
        view_tickets()
        continue

    # Search ticket
    if userInput.lower() == "search ticket":
        search_ticket()
        continue

    if userInput.lower() == "update ticket":
        update_ticket_status()
        continue

    if userInput.lower() == "update priority":
        update_ticket_priority()
        continue

    if userInput.lower() == "delete ticket":
        delete_ticket()
        continue

    reply, detected_intent, confidence_score  = get_Response_of_Bot(userInput)

    print("Bot:", reply)

    if detected_intent == "agent":

        create_ticket()

        # Save conversation
    chat_history.append({
        "user": userInput,
        "bot": reply,
        "intent": detected_intent,
        "confidence_score": confidence_score
    })
    

with open(history_file,"w") as file:
        json.dump(
        chat_history,
        file,
        indent = 4
    )

connection.close()

print("\nChat history saved successfully")
print("Database connection closed.")





