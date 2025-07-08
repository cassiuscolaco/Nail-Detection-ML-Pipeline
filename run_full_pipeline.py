import glob
import os
import subprocess

# 1️⃣ Detect the latest YOLO run folder
detect_runs = glob.glob("yolov5/runs/detect/exp*")
if not detect_runs:
    raise FileNotFoundError("No YOLO runs found in yolov5/runs/detect/")
latest_run = max(detect_runs, key=os.path.getmtime)
print(f"[INFO] Latest YOLO run detected: {latest_run}")

# 2️⃣ Count nails by reading YOLO label files
labels_dir = os.path.join(latest_run, "labels")
total_nails = 0
for label_file in glob.glob(os.path.join(labels_dir, "*.txt")):
    with open(label_file) as f:
        lines = f.readlines()
        total_nails += len(lines)
print(f"[INFO] Total nails detected: {total_nails}")

# 3️⃣ Run nail measurement script
os.environ["YOLO_RUN_PATH"] = latest_run
print("[INFO] Running nail height & weight estimation...")
result = subprocess.run(["python", "automate_nail_estimation.py"], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
result.check_returncode()

# 4️⃣ Run grouping script
print("[INFO] Grouping nails with similar physical properties...")
result = subprocess.run(["python", "group_similar_nails.py"], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
result.check_returncode()

print("[INFO] Counting, measurement, and grouping completed successfully!")
