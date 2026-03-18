import cv2
import os
import time
from cap_from_youtube import cap_from_youtube

ASCII_CHARS = "@%#*+=-:. "

def frame_to_ascii(frame, cols=100):
    height, width = frame.shape[:2]
    aspect_ratio = height / width
    new_height = int(cols * aspect_ratio * 0.55)
    
    resized_frame = cv2.resize(frame, (cols, new_height))
    gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

    ascii_str = ""
    for row in gray_frame:
        for pixel in row:
            ascii_str += ASCII_CHARS[int(pixel / 256 * len(ASCII_CHARS))]
        ascii_str += "\n"
    return ascii_str

def main():
    url = input("Enter YouTube URL: ")
    cap = cap_from_youtube(url, '480p')
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            ascii_frame = frame_to_ascii(frame, cols=os.get_terminal_size().columns)
            print("\033[H" + ascii_frame, end="") 
            time.sleep(0.03)
            
    except KeyboardInterrupt:
        print("\nPlayback stopped.")
    finally:
        cap.release()

main()
