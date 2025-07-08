import cv2
import os
import glob
import csv

# Settings
pixels_per_mm = 5
grams_per_mm = 0.5
img_width, img_height = 640, 640  # YOLO detection image size

# Paths
detect_runs = glob.glob("yolov5/runs/detect/exp*")
if not detect_runs:
    raise FileNotFoundError("No YOLO runs found in yolov5/runs/detect/")
detect_dir = max(detect_runs, key=os.path.getmtime)
print(f"[INFO] Using latest YOLO run: {detect_dir}")
labels_dir = os.path.join(detect_dir, "labels")
images_dir = detect_dir
results_dir = "results"
os.makedirs(results_dir, exist_ok=True)

# Open CSV file for writing measurements
with open("nail_measurements.csv", mode="w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Image", "NailNumber", "Length_mm", "Weight_g"])

    # Loop over each YOLO label file
    label_files = glob.glob(os.path.join(labels_dir, "*.txt"))
    for label_path in label_files:
        base_name = os.path.splitext(os.path.basename(label_path))[0]
        image_path = next((p for p in [f"{os.path.join(images_dir, base_name)}.jpg", f"{os.path.join(images_dir, base_name)}.png"] if os.path.exists(p)), None)
        if image_path is None:
            print(f"[{base_name}] Annotated image not found (.jpg or .png), skipping.")
            continue

        image = cv2.imread(image_path)
        if image is None:
            print(f"[{base_name}] Failed to read image, skipping.")
            continue

        with open(label_path) as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            class_id, x_center, y_center, width, height = map(float, line.strip().split())

            # Convert YOLO normalized box to pixel coordinates
            x_center *= img_width
            y_center *= img_height
            width *= img_width
            height *= img_height
            x_min = int(max(x_center - width / 2, 0))
            y_min = int(max(y_center - height / 2, 0))
            x_max = int(min(x_center + width / 2, img_width - 1))
            y_max = int(min(y_center + height / 2, img_height - 1))

            # Check for invalid box dimensions
            if x_min >= x_max or y_min >= y_max:
                print(f"[{base_name}] Nail {i+1}: Invalid crop coordinates, skipping.")
                continue

            # Crop the bounding box region
            crop = image[y_min:y_max, x_min:x_max]
            if crop is None or crop.size == 0:
                print(f"[{base_name}] Nail {i+1}: Empty crop, skipping.")
                continue

            # Convert crop to grayscale & threshold
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)

            # Find contours
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                largest = max(contours, key=cv2.contourArea)
                rect = cv2.minAreaRect(largest)
                (center_x, center_y), (w, h), angle = rect

                # Estimate nail length & weight
                nail_length_pixels = max(w, h)
                nail_length_mm = nail_length_pixels / pixels_per_mm
                nail_weight_g = nail_length_mm * grams_per_mm

                print(f"[{base_name}] Nail {i+1}: {nail_length_mm:.2f} mm, {nail_weight_g:.2f} g")

                # Write measurements to CSV
                writer.writerow([base_name, i + 1, f"{nail_length_mm:.2f}", f"{nail_weight_g:.2f}"])

                # Draw the rotated rectangle on the crop
                box = cv2.boxPoints(rect).astype(int)
                cv2.drawContours(crop, [box], 0, (0, 255, 0), 2)

                # Save the annotated crop
                save_path = os.path.join(results_dir, f"{base_name}_nail_{i+1}.jpg")
                cv2.imwrite(save_path, crop)
            else:
                print(f"[{base_name}] Nail {i+1}: No contour found, skipping.")
