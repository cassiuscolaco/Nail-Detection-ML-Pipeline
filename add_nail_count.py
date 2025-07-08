import os
import cv2

# Automatically find the latest exp folder
detect_root = 'yolov5/runs/detect'
exp_folders = [d for d in os.listdir(detect_root) if d.startswith('exp')]
if not exp_folders:
    raise FileNotFoundError(f"No exp folders found in {detect_root}")

# Sort by exp number (exp, exp1, exp2, ...)
exp_folders.sort(key=lambda x: int(x[3:]) if x != 'exp' else -1)
latest_exp = exp_folders[-1]
exp_dir = os.path.join(detect_root, latest_exp)

print(f"🔎 Using latest YOLO detection folder: {exp_dir}")

images_dir = exp_dir
labels_dir = os.path.join(exp_dir, 'labels')

# Iterate over each image file
for image_file in os.listdir(images_dir):
    if not image_file.lower().endswith(('.jpg', '.png')):
        continue  # skip non-image files

    image_path = os.path.join(images_dir, image_file)
    label_path = os.path.join(labels_dir, image_file.replace('.jpg', '.txt').replace('.png', '.txt'))

    # Count nails
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            nail_count = len(f.readlines())
    else:
        nail_count = 0

    # Load image
    img = cv2.imread(image_path)

    # Overlay nail count as text
    text = f"Nails detected: {nail_count}"
    cv2.putText(img, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    # Save updated image (overwrite original)
    cv2.imwrite(image_path, img)

    print(f"✅ Updated {image_file} with nail count: {nail_count}")
