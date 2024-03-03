from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler

# Change paths below. Source to track is the downloads folder.
# ---------------------------------------------
# Windows: C:\Users\Username\Downloads
# Mac: /Users/Username/Downloads
# Linux (Debian-based): /usr/Username/Downloads
# ---------------------------------------------
source_dir = "/Users/sc/Downloads"
dest_rand = "/Users/sc/Desktop/Tech"
dest_audio = "/Users/sc/Music"
dest_images = "/Users/sc/Pictures"
dest_video = "/Users/sc/Videos"
dest_docs = "/Users/sc/Desktop/ASSETS"
dest_installers = "/Users/sc/Desktop"
dest_other = "/Users/sc/Desktop/Random Media"

now = time.time()


# Audio file types
audio_extensions = [".m4a", ".mp3", ".flac", ".wav", ".wma", ".aac"]

# Image file types
image_extensions = [".jpg", ".jpeg", ".gif", ".png", ".jpe", ".heic", ".heif", ".jfif", ".bmp", ".ico", ".tiff", ".apng", ".jif", ".jfi", ".webp", ".tif", ".psd",
                    ".raw", ".arw", ".cr2", ".nrw", ".k25", ".dib", ".ind", ".indd", ".indt", ".jp2", ".jpk", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".avif"]

# Video file types
video_extensions = [".webm", "mpg", ".mp4", ".mp2", ".mpeg", ".mpe", ".mpv",
                    ".ogg", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]

# Document file types
doc_extensions = [".doc", ".docx", ".pdf",
                  ".ppt", ".pptx", ".xls", ".xlsx", ".odt"]

# Installer file types
inst_extensions = [".exe", ".dmg", ".deb", ".msi"]

# Other misc file types
other_extensions = [".csv", ".htm", ".html", ".txt", ".sys", ".rtf"
                    ".zip", ".7z", ".dat", ".drv", ".bin", ".sh", ".cmd"]


def create_unique(dest, name):
    filename, extension = splitext(name)
    # Will append a file with 1 if it already exists and is a duplicate.
    counter = 1
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

        return name


def move_files(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = create_unique(dest, name)
        oldname = join(dest, name)
        newname = join(dest, unique_name)
        rename(oldname, newname)
    move(entry, dest)


class MoverHandler(FileSystemEventHandler):
    # Function will run whenever there is a change in the source directory you specify. Downloads is the default directory.
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_image_files(entry, name)
                self.check_video_files(entry, name)
                self.check_doc_files(entry, name)
                self.check_other_files(entry, name)

    # Audio file check
    def check_audio_files(self, entry, name):
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                if entry.stat().st_size < 10_000_000 or "SFX" in name:
                    dest = dest_other
                else:
                    dest = dest_audio
                    move_files(dest, entry, name)
                    logging.info(f"Moved audio file: {name}")

    # Image file check
    def check_image_files(self, entry, name):
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_files(dest_images, entry, name)
                logging.info(f"Moved image file: {name}")

    # Video file check
    def check_video_files(self, entry, name):
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_files(dest_video, entry, name)
                logging.info(f"Moved video file: {name}")

    # Document file check
    def check_doc_files(self, entry, name):
        for doc_extension in doc_extensions:
            if name.endswith(doc_extension) or name.endswith(doc_extension.upper()):
                move_files(dest_docs, entry, name)
                logging.info(f"Moved document file: {name}")

    # Other file check
    def check_other_files(self, entry, name):
        for other_extension in other_extensions:
            if name.endswith(other_extension) or name.endswith(other_extension.upper()):
                move_files(dest_other, entry, name)
                logging.info(f"Moved {other_extension} file: {name}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%m-%d-%Y %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
