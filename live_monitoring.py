import psutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

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

# === Set up observer ===
file_handler = FileActivityHandler()
observer = Observer()
observer.schedule(file_handler, path="C:\\", recursive=True)  # Change this for non-Windows systems
observer.start()

# === Monitor and display values only ===
def monitor(interval=60):
    print(f"🟢 Monitoring system activity every {interval} seconds...\n")

    try:
        while True:
            disk1 = psutil.disk_io_counters()
            net1 = psutil.net_io_counters()
            time.sleep(interval)

            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory().used / (1024 * 1024)  # In MB
            disk2 = psutil.disk_io_counters()
            net2 = psutil.net_io_counters()

            disk_mb_s = round((disk2.read_bytes - disk1.read_bytes +
                               disk2.write_bytes - disk1.write_bytes) / (1024 * 1024 * interval), 2)
            net_mbps = round((net2.bytes_sent - net1.bytes_sent +
                              net2.bytes_recv - net1.bytes_recv) * 8 / (1024 * 1024 * interval), 2)

            # Output system activity values
            print(f"[{datetime.now().strftime('%H:%M:%S')}]")
            print(f"🔹 CPU Usage: {round(cpu, 2)}%")
            print(f"🔹 Memory Used: {round(memory, 2)} MB")
            print(f"🔹 Disk Activity: {disk_mb_s} MB/s")
            print(f"🔹 Network Activity: {net_mbps} Mbps")
            print(f"🔹 Files → Created: {file_handler.created}, Deleted: {file_handler.deleted}, Renamed: {file_handler.renamed}")
            print("-" * 60)

            file_handler.reset()

    except KeyboardInterrupt:
        print("🛑 Monitoring stopped by user.")
        observer.stop()
    observer.join()

# === Start the trial ===
monitor(interval=60)
