Smart Reminder & Deadline Tracker
Overview
The **Smart Reminder & Deadline Tracker** is an Object-Oriented Python project that helps students and professionals manage **assignments, exams, project submissions, and job application deadlines** efficiently.

It automatically tracks important dates, sends **desktop notifications, voice alerts**, and even fetches **deadline-related emails** from Gmail. The goal is to ensure you never miss a deadline again!

---

## 🎯 Features

 **Task Management System**
- Add, view, delete, and mark tasks as completed.
- Tasks include title, description, deadline, and priority (High/Medium/Low).

 **Automatic Deadline Alerts**
- Sends notifications **1 day before** and **at the deadline**.
- Plays **beep + voice alerts** continuously until you stop it.

 **Email Integration**
- Connects to Gmail using IMAP.
- Auto-detects emails containing words like **“deadline”**, **“job application”**, **“apply by”**.
- Adds them automatically to your task list.

 **Voice Notifications**
- Uses `pyttsx3` for real-time voice alerts.
- Alerts repeat at intervals (5 or 10 minutes) until the task is completed.

 **Persistent Database**
- All tasks are stored in a local SQLite database (`reminder.db`).
- Even after restarting, your tasks remain saved.


---

## 🛠️ Tech Stack

| Component | Technology Used |
|------------|----------------|
| Programming Language | Python |
| Database | SQL |
| Notification | plyer |
| Voice Engine | pyttsx3 |
| Scheduling | schedule |
| Email Fetch | imaplib, email |
| Object-Oriented Design | Classes: `Reminder`, `Task`, `Notifier`, `EmailFetcher` |

---

Project Structure

Smart-Reminder/

├── main.py ( Main program entry point)

├── reminder.py (Handles database & task operations)

├── notifier.py (Handles voice + popup notifications)

├── email_fetcher.py (Fetches emails with deadlines)

├── reminder.db (SQL database (auto-created))

└── README.md (Project documentation)

