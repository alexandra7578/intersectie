from ultralytics import YOLO
import os
import shutil
import random

# Setările directoarelor
base_dir = 'D:/Work/intersectie'
image_dir = os.path.join(base_dir, 'images')
label_dir = os.path.join(base_dir, 'labels')
train_dir = os.path.join(image_dir, 'train')
val_dir = os.path.join(image_dir, 'val')
test_dir = os.path.join(image_dir, 'test')
train_label_dir = os.path.join(label_dir, 'train')
val_label_dir = os.path.join(label_dir, 'val')
test_label_dir = os.path.join(label_dir, 'test')

# Creează directoarele dacă nu există
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)
os.makedirs(train_label_dir, exist_ok=True)
os.makedirs(val_label_dir, exist_ok=True)
os.makedirs(test_label_dir, exist_ok=True)

# Obține toate imaginile și sortează-le
images = sorted([f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])

# Shuffle pentru a le amesteca
random.shuffle(images)

# Split datele în proporțiile dorite
train_split = int(0.8 * len(images))
val_split = int(0.1 * len(images))

train_images = images[:train_split]
val_images = images[train_split:train_split + val_split]
test_images = images[train_split + val_split:]

def move_files(image_list, dest_image_dir, dest_label_dir):
    for image in image_list:
        base_name = os.path.splitext(image)[0]
        image_path = os.path.join(image_dir, image)
        label_path = os.path.join(label_dir, f"{base_name}.txt")

        if os.path.exists(label_path):
            shutil.move(image_path, os.path.join(dest_image_dir, image))
            shutil.move(label_path, os.path.join(dest_label_dir, f"{base_name}.txt"))
        else:
            print(f"Eticheta pentru {image} nu a fost găsită.")

# Mută fișierele în directoarele corespunzătoare
move_files(train_images, train_dir, train_label_dir)
move_files(val_images, val_dir, val_label_dir)
move_files(test_images, test_dir, test_label_dir)

# Încarcă modelul pre-antrenat (poți alege un alt model din familia YOLOv8)
model = YOLO('yolov8n.pt')

# Antrenează modelul pe datele tale
model.train(data='D:\Work\intersectie\data.yaml', epochs=50, imgsz=640)

# Evaluează modelul pe setul de validare
metrics = model.val()

# Afișează metricile de evaluare
print("Precision: ", metrics['precision'])
print("Recall: ", metrics['recall'])
print("mAP@0.5: ", metrics['map50'])
print("mAP@0.5:0.95: ", metrics['map'])

# Calcularea și afișarea acurateței
accuracy = metrics['map50']  # mAP@0.5 poate fi considerată o aproximare a acurateței
print("Acuratețe (mAP@0.5): ", accuracy)

# Realizează inferențe pe o imagine nouă
results = model('D:\Work\intersectie\Poze_Nord')
results.show()
