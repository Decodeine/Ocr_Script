import cv2
import os
from PIL import Image
import pytesseract
import subprocess

def extract_frames(video_path, output_folder, interval=1):
    os.makedirs(output_folder, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    success, frame = cap.read()
    count = 0
    while success:
        if count % int(frame_rate * interval) == 0:
            frame_name = os.path.join(output_folder, f"frame{count}.jpg")
            cv2.imwrite(frame_name, frame)
        success, frame = cap.read()
        count += 1
    cap.release()

def ocr_from_frames(folder_path):
    frame_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.jpg')]
    ocr_results = []
    for frame_file in frame_files:
        image = Image.open(frame_file)
        text = pytesseract.image_to_string(image)
        ocr_results.append((frame_file, text))
    return ocr_results

def extract_audio_segment(video_path, start_time, duration, output_path):
    command = [
        'ffmpeg', '-i', video_path, '-ss', str(start_time), '-t', str(duration),
        '-q:a', '0', '-map', 'a', output_path
    ]
    subprocess.run(command)

def main(video_path, output_folder, interval=1):
    extract_frames(video_path, output_folder, interval)
    ocr_results = ocr_from_frames(output_folder)
    for frame_file, text in ocr_results:
        print(f"Text from {frame_file}:\n{text}\n")
        if text.strip():
            frame_number = int(os.path.basename(frame_file).split("frame")[1].split(".jpg")[0])
            start_time = frame_number
            duration = 1
            audio_output_folder = "extracted_audio"
            os.makedirs(audio_output_folder, exist_ok=True)
            audio_output_path = os.path.join(audio_output_folder, f"audio_{frame_number}.mp3")
            extract_audio_segment(video_path, start_time, duration, audio_output_path)

if __name__ == "__main__":
    video_path = r"C:\Users\HP\Downloads\How Valorant is putting women at the forefront of esports [TubeRipper.com].mp4"
    output_folder = "extracted_frames"
    main(video_path, output_folder, interval=1)
