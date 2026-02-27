import cv2
import os
import sys
import time
from pytube import YouTube

# --- 1. DOWNLOAD SECTION ---
def download_video(url):
    print("Checking URL...")
    yt = YouTube(url)
    print(f"Downloading: {yt.title}")
    
    # Get the lowest resolution to save processing power
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').first()
    stream.download(output_path=".", filename="video.mp4")
    return "video.mp4"

# --- 2. RENDERING SECTION ---
def render_to_terminal(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Get terminal size
    cols, rows = os.get_terminal_size()
    
    # Adjust height because terminal characters are taller than they are wide
    # Use a 0.5 multiplier to fix the "stretched" look
    target_width = cols
    target_height = int(rows * 0.9) # Leave a little room at the bottom

    print("\033[2J") # Clear screen once at start

    try:
        while cap.isOpened():
            start_time = time.time()
            ret, frame = cap.read()
            if not ret:
                break

            # Resize frame for terminal
            resized_frame = cv2.resize(frame, (target_width, target_height))
            
            # Build the frame string
            output = "\033[H" # Move cursor to top-left (no flicker)
            for row in resized_frame:
                line = ""
                for pixel in row:
                    b, g, r = pixel
                    # \033[48;2;R;G;Bm is for background color
                    # Use a space ' ' with a colored background for "pixels"
                    line += f"\033[48;2;{r};{g};{b}m "
                output += line + "\033[0m\n" # Reset color at end of line
            
            sys.stdout.write(output)
            sys.stdout.flush()

            # Maintain original video FPS
            elapsed = time.time() - start_time
            if elapsed < 1/fps:
                time.sleep((1/fps) - elapsed)

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        print("\033[0m") # Final reset

# --- 3. EXECUTION ---
if __name__ == "__main__":
    video_url = input("Enter YouTube URL: ")
    path = download_video(video_url)
    render_to_terminal(path)
