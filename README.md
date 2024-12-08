# Video Bot

# Overview

Video Bot is an automated solution to monitor a directory for new `.mp4` files, upload them to a specified platform using API endpoints, and create posts with the uploaded videos. It simplifies the process of video uploads and post creation with asynchronous operations for maximum efficiency.

# Features

- Search and download videos (future scope)
- Upload videos via API endpoints
- Auto-delete local files after successful upload
- Monitor `/videos` directory for new `.mp4` files
- Asynchronous operations for concurrent uploads
- Progress bars for uploads using `tqdm`
- Error handling for robust operation

# Project Structure
video-bot/
├── main.py                # Main script
├── requirements.txt       # Dependencies
├── README.md              # Documentation


# Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

# Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd video-bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Flic-Token**:
   - Open `main.py`.
   - Replace `<YOUR_TOKEN>` in the `FLIC_TOKEN` variable with your actual token.

4. **Create the videos directory**:
   ```bash
   mkdir videos
   ```

## Usage

1. **Run the script**:
   ```bash
   python main.py
   ```

   The script will start monitoring the `/videos` directory for new `.mp4` files.

2. **Add a video file**:
   - Place any `.mp4` file in the `/videos` directory.
   - The script will:
     - Automatically detect the new file.
     - Upload it to the platform via the API.
     - Create a post with the uploaded video.
     - Delete the file after successful processing.

3. **Check progress**:
   - During uploads, a progress bar will display the upload status.
   - On successful completion, you’ll see a success message in the terminal.

## API Integration

### 1. Get Upload URL

- **Endpoint**: `https://api.socialverseapp.com/posts/generate-upload-url`
- **Method**: `GET`
- **Headers**:
  ```json
  {
    "Flic-Token": "<YOUR_TOKEN>",
    "Content-Type": "application/json"
  }
  ```

### 2. Upload Video

- **Method**: `PUT`
- **Pre-signed URL**: Obtained from Step 1.

### 3. Create Post

- **Endpoint**: `https://api.socialverseapp.com/posts`
- **Method**: `POST`
- **Headers**:
  ```json
  {
    "Flic-Token": "<YOUR_TOKEN>",
    "Content-Type": "application/json"
  }
  ```
- **Body**:
  ```json
  {
    "title": "<video title>",
    "hash": "<hash from Step 1>",
    "is_available_in_public_feed": false,
    "category_id": <category_id>
  }
  ```

## Example Output

- On starting the script:
  ```
  Monitoring ./videos for new .mp4 files.
  ```

- On detecting a new file:
  ```
  Processing video: example.mp4
  Uploading: 100%|███████████████████████████████████████████████| 50.0M/50.0M [00:15<00:00, 3.25MB/s]
  Successfully uploaded and created post for example.mp4
  ```

## Error Handling

- If an error occurs during any step, it will be logged in the console with details:
  ```
  Error processing video example.mp4: <Error description>
  ```

## Contribution

Feel free to open issues or submit pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

This `README.md` provides all essential details for understanding, setting up, and using the project. You can modify it further based on any additional features or specific instructions.
