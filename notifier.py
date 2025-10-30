import threading
import time
import winsound
from plyer import notification
import pyttsx3

class Notifier:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.alert_running = False
        self.thread = None

    # ---------------------------
    # Text-to-speech voice alert
    # ---------------------------
    def voice_alert(self, message):
        try:
            self.engine.say(message)
            self.engine.runAndWait()
        except Exception as e:
            print("[Voice Error]", e)

    # ---------------------------
    # Single notification + voice + beep
    # ---------------------------
    def send_notification(self, title, message):
        try:
            notification.notify(
                title=title,
                message=message,
                timeout=10
            )
            winsound.Beep(1000, 800)
            print(f"[Notification] {title}: {message}")
            self.voice_alert(message)
        except Exception as e:
            print("[Notify Error]", e)

    # ---------------------------
    # Repeating alert (continuous reminder)
    # ---------------------------
    def start_repeating_alert(self, message, repeat_seconds=120):
        if self.alert_running:
            print("[Alert] Already running.")
            return

        self.alert_running = True

        def repeat():
            while self.alert_running:
                print("[Voice Alert Loop] Speaking reminder...")
                self.voice_alert(message)
                winsound.Beep(1200, 500)
                time.sleep(repeat_seconds)

        self.thread = threading.Thread(target=repeat, daemon=True)
        self.thread.start()
        print("[+] Continuous alert started.")

    # ---------------------------
    # Stop continuous voice alert
    # ---------------------------
    def stop_alert(self):
        if self.alert_running:
            self.alert_running = False
            print("[+] Voice alert stopped.")
        else:
            print("[Info] No voice alert is running currently.")
