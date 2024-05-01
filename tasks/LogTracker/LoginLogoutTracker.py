import sqlite3
import datetime
from openpyxl import Workbook

# Function to create the user_sessions table if it doesn't exist
def create_table():
    conn = sqlite3.connect('user_sessions.db')
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS user_sessions''')  # Drop the existing table if it exists
    c.execute('''CREATE TABLE user_sessions
                 (username TEXT, login_date TEXT, login_time TEXT, logout_date TEXT, logout_time TEXT)''')  # Recreate the table with updated schema
    conn.commit()
    conn.close()

def login(username):
    conn = sqlite3.connect('user_sessions.db')
    c = conn.cursor()
    login_time = datetime.datetime.now()
    login_date = login_time.strftime("%Y-%m-%d")
    login_time = login_time.strftime("%H:%M:%S")
    c.execute("INSERT INTO user_sessions (username, login_date, login_time) VALUES (?, ?, ?)", (username, login_date, login_time))
    conn.commit()
    conn.close()
    print("User '{}' logged in at {} {}".format(username, login_date, login_time))

def logout(username):
    conn = sqlite3.connect('user_sessions.db')
    c = conn.cursor()
    logout_time = datetime.datetime.now()
    logout_date = logout_time.strftime("%Y-%m-%d")
    logout_time = logout_time.strftime("%H:%M:%S")
    c.execute("UPDATE user_sessions SET logout_date = ?, logout_time = ? WHERE username = ? AND logout_date IS NULL", (logout_date, logout_time, username))
    conn.commit()
    conn.close()
    print("User '{}' logged out at {} {}".format(username, logout_date, logout_time))

def display_sessions():
    conn = sqlite3.connect('user_sessions.db')
    c = conn.cursor()
    c.execute("SELECT * FROM user_sessions")
    rows = c.fetchall()
    conn.close()

    print("\nUser sessions:")
    for row in rows:
        username, login_date, login_time, logout_date, logout_time = row
        logout_date = logout_date if logout_date else "N/A"
        logout_time = logout_time if logout_time else "N/A"
        print("User '{}': Login Date - {}, Login Time - {}, Logout Date - {}, Logout Time - {}".format(username, login_date, login_time, logout_date, logout_time))

def generate_report():
    conn = sqlite3.connect('user_sessions.db')
    c = conn.cursor()
    c.execute("SELECT * FROM user_sessions")
    rows = c.fetchall()
    conn.close()

    wb = Workbook()
    ws = wb.active
    ws.append(["Username", "Login Date", "Login Time", "Logout Date", "Logout Time"])

    for row in rows:
        username, login_date, login_time, logout_date, logout_time = row
        logout_date = logout_date if logout_date else "N/A"
        logout_time = logout_time if logout_time else "N/A"
        ws.append([username, login_date, login_time, logout_date, logout_time])

    report_filename = "user_sessions_report.xlsx"
    wb.save(report_filename)
    print(f"Report generated and saved to {report_filename}")

# Create the user_sessions table
create_table()

# Main program loop
while True:
    print("\n1. Login")
    print("2. Logout")
    print("3. Display User Sessions")
    print("4. Generate Report and Export to Excel")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        username = input("Enter username to login: ")
        login(username)
    elif choice == '2':
        username = input("Enter username to logout: ")
        logout(username)
    elif choice == '3':
        display_sessions()
    elif choice == '4':
        generate_report()
    elif choice == '5':
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please enter a valid option.")
