from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

from app.services.document_loader import load_single_pdf

WATCH_FOLDER = "app/knowledge"


class PDFHandler(FileSystemEventHandler):

    def on_created(self, event):
        if event.is_directory:
            return

        if not event.src_path.endswith(".pdf"):
            return

        print(f"[NEW PDF DETECTED] {event.src_path}")

        # 🔥 WAIT FOR FILE TO BE FULLY WRITTEN
        max_attempts = 10

        for i in range(max_attempts):

            if os.path.exists(event.src_path):

                try:
                    # check file is not locked
                    with open(event.src_path, "rb") as f:
                        f.read(10)

                    break  # file is ready

                except Exception:
                    time.sleep(1)

            else:
                time.sleep(1)

        # Now safely ingest
        load_single_pdf(event.src_path)


def start_watcher():
    event_handler = PDFHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()

    print("[WATCHER STARTED] Monitoring PDFs...")

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()