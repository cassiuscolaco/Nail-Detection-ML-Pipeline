# estimate_nail_height.py

# Settings: image size used during YOLO detection
img_width, img_height = 640, 640

# Scale factor: how many pixels per 1 mm of real nail length
# Adjust this value based on your camera setup or synthetic data scale!
pixels_per_mm = 10  # e.g., 10 pixels = 1 mm
grams_per_mm = 0.1  # e.g., 1 mm of nail length weighs 0.1 grams

# Step 1: Read YOLO label file
with open("yolov5/runs/detect/exp2/labels/real_image2.txt") as f:
    lines = f.readlines()

# Step 2: Process each detected nail
for line in lines:
    # Parse normalized YOLO box values
    class_id, x_center, y_center, width, height = map(float, line.strip().split())

    # Convert normalized coordinates to pixel positions
    x_center *= img_width
    y_center *= img_height
    width *= img_width
    height *= img_height

    # Convert to bounding box pixel corners
    x_min = int(x_center - width / 2)
    y_min = int(y_center - height / 2)
    x_max = int(x_center + width / 2)
    y_max = int(y_center + height / 2)

    # Compute height in pixels
    box_height_pixels = y_max - y_min

    # Estimate height in millimeters
    height_mm = box_height_pixels / pixels_per_mm
  # Estimate weight in grams
    weight_g = height_mm * grams_per_mm

    # Output results
    print(f"Bounding box (pixels): [{x_min}, {y_min}, {x_max}, {y_max}]")
    print(f"Estimated height: {box_height_pixels} pixels ≈ {height_mm:.2f} mm")
    print(f"Estimated weight: {weight_g:.2f} grams\n")
