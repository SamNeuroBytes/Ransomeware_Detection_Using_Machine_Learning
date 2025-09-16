import psutil
import time
import joblib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# === Load your trained model ===
model = joblib.load("random_forest_ransomware.pkl")  # Replace with your trained model path

# === File system activity handler ===
class FileActivityHandler(FileSystemEventHandler):
    def __init__(self):
        self.reset()

    def reset(self):
        self.created = 0
        self.deleted = 0
        self.renamed = 0

    def on_created(self, event):
        if not event.is_directory:
            self.created += 1

    def on_deleted(self, event):
        if not event.is_directory:
            self.deleted += 1

    def on_moved(self, event):
        if not event.is_directory:
            self.renamed += 1

# === Set up file observer ===
file_handler = FileActivityHandler()
observer = Observer()
observer.schedule(file_handler, path="C:\\", recursive=True)  # Change path for Linux/macOS
observer.start()

# === Monitor and predict ===
def monitor(interval=60):
    print(f"🔍 Monitoring every {interval} seconds for ransomware behavior...\n")

    try:
        while True:
            # Initial disk and network stats
            disk1 = psutil.disk_io_counters()
            net1 = psutil.net_io_counters()
            time.sleep(interval)

            # Read feature values
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory().used / (1024 * 1024)
            disk2 = psutil.disk_io_counters()
            net2 = psutil.net_io_counters()

            # Compute deltas
            disk_mb_s = round((disk2.read_bytes - disk1.read_bytes +
                               disk2.write_bytes - disk1.write_bytes) / (1024 * 1024 * interval), 2)
            net_mbps = round((net2.bytes_sent - net1.bytes_sent +
                              net2.bytes_recv - net1.bytes_recv) * 8 / (1024 * 1024 * interval), 2)

            # Feature vector for prediction
            row = [
                round(cpu, 2),
                round(memory, 2),
                disk_mb_s,
                net_mbps,
                file_handler.created,
                file_handler.deleted,
                file_handler.renamed
            ]

            # ML model prediction
            prediction = model.predict([row])[0]
            label = "⚠️ RANSOMWARE DETECTED!" if prediction == 1 else "✅ Normal Behavior"

            # Display result
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {label}")
            print(f" Features → CPU: {row[0]}%, Mem: {row[1]}MB, Disk: {row[2]}MB/s, Net: {row[3]}Mbps, "
                  f"Files C/D/R: {row[4]}/{row[5]}/{row[6]}")
            print("-" * 60)

            # Reset file counters
            file_handler.reset()

    except KeyboardInterrupt:
        print("⏹️ Monitoring stopped by user.")
        observer.stop()
    observer.join()

# === Start Monitoring ===
monitor(interval=60)
