import os
import asyncio
import aiohttp
from tqdm import tqdm
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import hashlib
import requests

BASE_URL = "https://api.socialverseapp.com/posts"
FLIC_TOKEN = "flic_6b25205dfef7040558016798f182528669495d995a4669a82ae3ab1c10c1af3b" 
HEADERS = {
    "Flic-Token": FLIC_TOKEN,
    "Content-Type": "application/json"
}
VIDEOS_DIR = "videos"

class VideoHandler(FileSystemEventHandler):
    """Handles new video file events."""
    def __init__(self, loop):
        self.loop = loop

    def on_created(self, event):
        if event.src_path.endswith(".mp4"):
            self.loop.create_task(process_video(event.src_path))

async def get_upload_url():
    """Get pre-signed upload URL."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/generate-upload-url", headers=HEADERS) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception("Failed to get upload URL.")

async def upload_video(file_path, upload_url):
    """Upload video to the pre-signed URL."""
    with open(file_path, "rb") as file:
        file_size = os.path.getsize(file_path)
        with tqdm(total=file_size, unit="B", unit_scale=True, desc="Uploading") as progress:
            async with aiohttp.ClientSession() as session:
                async with session.put(upload_url, data=file) as response:
                    if response.status == 200:
                        progress.update(file_size)
                        return True
                    else:
                        raise Exception("Failed to upload video.")

async def create_post(title, video_hash, category_id=1):
    """Create a new post."""
    payload = {
        "title": title,
        "hash": video_hash,
        "is_available_in_public_feed": False,
        "category_id": category_id
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(BASE_URL, headers=HEADERS, json=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception("Failed to create post.")

async def process_video(file_path):
    """Process video: upload and create post."""
    try:
        upload_data = await get_upload_url()
        upload_url = upload_data["url"]
        video_hash = upload_data["hash"]

        await upload_video(file_path, upload_url)

        title = os.path.basename(file_path)
        await create_post(title, video_hash)

        os.remove(file_path)
        print(f"Processed and deleted {file_path}")
    except Exception as e:
        print(f"Error processing video {file_path}: {e}")

async def monitor_directory():
    """Monitor directory for new video files."""
    loop = asyncio.get_event_loop()
    event_handler = VideoHandler(loop)
    observer = Observer()
    observer.schedule(event_handler, path=VIDEOS_DIR, recursive=False)
    observer.start()
    print(f"Monitoring {VIDEOS_DIR} for new .mp4 files.")
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    if not os.path.exists(VIDEOS_DIR):
        os.makedirs(VIDEOS_DIR)
    asyncio.run(monitor_directory())
