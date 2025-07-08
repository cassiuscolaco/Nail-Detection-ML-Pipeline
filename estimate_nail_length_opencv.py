import cv2

# Settings
pixels_per_mm = 5  # example: 10 pixels = 1 mm
grams_per_mm = 0.1  # e.g., each mm of nail weighs 0.1 grams

image_path = "yolov5/runs/detect/exp22/real_image.png"  # path to your detected image
# Example bounding box coordinates from YOLO detection (replace with actual values!)
x_min, y_min, x_max, y_max = 100, 150, 200, 350  

# Step 1: Load the full image
image = cv2.imread(image_path)
if image is None:
    raise FileNotFoundError(f"could not read: {image_path}")

# Step 2: Crop the bounding box area
crop = image[y_min:y_max, x_min:x_max]
cv2.imshow("Cropped nail", crop)
cv2.waitKey(0)

# Step 3: Convert crop to grayscale
gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

# Step 4: Threshold to separate nail from background
_, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
cv2.imshow("Thresholded", binary)
cv2.waitKey(0)

# Step 5: Find contours
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if contours:
    # Step 6: Get largest contour
    largest = max(contours, key=cv2.contourArea)

    # Step 7: Fit rotated rectangle to largest contour
    rect = cv2.minAreaRect(largest)
    (center_x, center_y), (width, height), angle = rect

    # Step 8: Estimate nail length using the longer rectangle side
    nail_length_pixels = max(width, height)
    nail_length_mm = nail_length_pixels / pixels_per_mm
    nail_weight_g = nail_length_mm * grams_per_mm
    


    print(f"Estimated nail length: {nail_length_pixels:.1f} pixels ≈ {nail_length_mm:.2f} mm")
    print(f"Estimated nail weight: {nail_weight_g:.2f} grams")

    # Draw the rectangle on the crop for visualization
    box = cv2.boxPoints(rect)
    box = box.astype(int)
    cv2.drawContours(crop, [box], 0, (0, 255, 0), 2)
    cv2.imshow("Estimated nail", crop)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No contour found — cannot estimate nail length.")
