import os
import cv2
from ultralytics import YOLO
import torch
torch.cuda.empty_cache()
# Initialize YOLO model
model = YOLO("yolov8m.pt")


# Function to crop and save image
def crop_and_save_image(image_path, bounding_box, save_path):
    image = cv2.imread(image_path)
    x_min, y_min, x_max, y_max = map(int, bounding_box)
    cropped_image = image[y_min:y_max, x_min:x_max]
    cv2.imwrite(save_path, cropped_image)


# Path to the birds folder
birds_folder = "test_images"
errors = []
# Loop through each bird species folder
for bird_species in os.listdir(birds_folder):
    bird_species_folder = os.path.join(birds_folder, bird_species)
    if os.path.isdir(bird_species_folder):
        # Loop through each image in the bird species folder
        for image_name in os.listdir(bird_species_folder):
            try:
                image_path = os.path.join(bird_species_folder, image_name)

                prediction = model.predict(image_path)
                result = prediction[0]
                for box in result.boxes:
                    print(box)
                boxes = result.boxes[1]

                bounding_box = boxes.xyxy[0].tolist()

                save_name = f"cropped_{image_name}"
                save_path = os.path.join(bird_species_folder, save_name)

                crop_and_save_image(image_path, bounding_box, save_path)
            except:
                errors.append(save_path)


print("ERROR IMAGES WERE: ", errors)
print("Images cropped and saved successfully.")
