import time
import schedule
from datetime import datetime, timedelta
from reminder import Reminder
from notifier import Notifier
from email_fetcher import EmailFetcher


# Initialize Notifier globally
notifier = Notifier()


# ======================================
# Voice Confirmation Helper
# ======================================
def voice_confirm(message):
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(message)
        engine.runAndWait()
    except Exception as e:
        print("[Voice Error]", e)


# ======================================
# Check Task Deadlines
# ======================================
def check_deadlines(reminder):
    print("[Checking deadlines...]")
    now = datetime.now()
    due_tasks = reminder.get_all_tasks()

    for task in due_tasks:
        task_id, title, desc, deadline_str, priority, status = task
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")

        if status.lower() == "completed":
            continue

        # 1️⃣ Alert one day before deadline
        if now >= (deadline - timedelta(days=1)) and now < deadline:
            notifier.send_notification(
                f"Upcoming Task Tomorrow: {title}",
                f"The task '{title}' is due on {deadline_str}. Finish it soon!"
            )
            voice_confirm(f"Reminder! The task {title} is due tomorrow.")
            notifier.start_repeating_alert(
                f"Reminder! The task {title} is due tomorrow. Please complete it before the deadline.",
                repeat_seconds=600  # Every 10 minutes
            )

        # 2️⃣ Alert exactly at or after deadline
        elif now >= deadline:
            notifier.send_notification(
                f"Deadline Reached: {title}",
                f"Task '{title}' deadline has passed! Deadline: {deadline_str}"
            )
            voice_confirm(f"Urgent! The task {title} deadline has passed.")
            notifier.start_repeating_alert(
                f"URGENT! Task {title} deadline has passed! Please complete it immediately!",
                repeat_seconds=300  # Every 5 minutes
            )
            reminder.mark_completed(task_id)


# ======================================
# Check Gmail for New Deadlines / Jobs
# ======================================
def check_email_deadlines():
    print("[Checking Gmail for deadlines...]")
    fetcher = EmailFetcher(
        email_user="akshithaakki2704@gmail.com",   # ⚠️ Replace with your Gmail
        email_pass="ayovwstgscsgynun"      # ⚠️ Replace with your App Password
    )
    reminder = Reminder()
    emails = fetcher.get_deadline_emails()

    for e in emails:
        title = e["subject"]
        desc = f"From: {e['sender']} | {e['body']}"
        deadline = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d %H:%M")  # Default +2 days
        reminder.add_task(title, desc, deadline)

        notifier.send_notification("New Email Deadline", f"{title}")
        voice_confirm(f"New email detected about {title}. Task added successfully.")
        notifier.start_repeating_alert(
            f"New email related to deadline found: {title}. Check your inbox soon.",
            repeat_seconds=600
        )


# ======================================
# Main Menu
# ======================================
def main_menu():
    reminder = Reminder()

    while True:
        print("\n============================")
        print("📅 SMART DEADLINE TRACKER")
        print("============================")
        print("1️⃣  Add New Task")
        print("2️⃣  View All Tasks")
        print("3️⃣  Mark Task as Completed")
        print("4️⃣  Delete a Task")
        print("5️⃣  Start Auto Reminder Service")
        print("6️⃣  Stop Voice Alerts")
        print("7️⃣  Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            title = input("Enter Task Title: ")
            desc = input("Enter Description: ")
            deadline = input("Enter Deadline (YYYY-MM-DD HH:MM): ")
            priority = input("Enter Priority (High/Medium/Low): ") or "Medium"

            reminder.add_task(title, desc, deadline, priority)
            notifier.send_notification("New Task Added", f"{title} due at {deadline}")
            voice_confirm(f"Task {title} has been added successfully and will remind you before the deadline.")

            notifier.start_repeating_alert(
                f"Reminder! Task {title} is pending. Please complete it before {deadline}.",
                repeat_seconds=900  # Every 15 minutes
            )

        elif choice == "2":
            reminder.show_tasks()

        elif choice == "3":
            task_id = input("Enter Task ID to mark as completed: ")
            reminder.mark_completed(task_id)
            notifier.stop_alert()
            voice_confirm("Task marked as completed.")

        elif choice == "4":
            task_id = input("Enter Task ID to delete: ")
            reminder.delete_task(task_id)
            voice_confirm("Task deleted successfully.")

        elif choice == "5":
            print("\n[Auto Reminder Service Started...]")
            schedule.every(1).minutes.do(check_deadlines, reminder)
            schedule.every(10).minutes.do(check_email_deadlines)

            try:
                while True:
                    schedule.run_pending()
                    time.sleep(5)
            except KeyboardInterrupt:
                print("\n[Service stopped by user]")
                voice_confirm("Service stopped.")

        elif choice == "6":
            notifier.stop_alert()
            voice_confirm("Voice alerts stopped.")

        elif choice == "7":
            notifier.stop_alert()
            print("Goodbye 👋")
            voice_confirm("Exiting Smart Deadline Tracker. Goodbye!")
            break

        else:
            print("❌ Invalid choice! Please try again.")


# ======================================
# Run Program
# ======================================
if __name__ == "__main__":
    main_menu()
