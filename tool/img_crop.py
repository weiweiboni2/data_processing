# Description: This script is used to crop the images in the dataset.
import cv2
import os
from tqdm import tqdm


def create_file(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f'Created folder:({output_dir})')


def update(input_img_path, output_img_path):
    image = cv2.imread(input_img_path)
    cropped = image[100:612, 100:740]  # 裁剪坐标为[y0:y1, x0:x1]
    cv2.imwrite(output_img_path, cropped)


dataset_dir_vi = r'E:\python_pj\yolov8\YOLOv8-main\data\DroneVehicle_det\images\testimgr'
output_dir = r'E:\python_pj\yolov8\YOLOv8-main\data\DroneVehicle_det\images\test'
# dataset_dir_ir = r'E:\python_pj\yolov8\YOLOv8-main\data\DroneVehicle_det\images\val'
# output_dir_ir = r'E:\python_pj\yolov8\YOLOv8-main\data\DroneVehicle_det\img\val'

# 检查文件夹是否存在，如果不存在则创建
create_file(output_dir)
# 获得需要转化的图片路径并生成目标路径
image_filenames_vi = [(os.path.join(dataset_dir_vi, x), os.path.join(output_dir, x))
                      for x in os.listdir(dataset_dir_vi)]

# image_filenames_ir = [(os.path.join(dataset_dir_ir, x), os.path.join(output_dir_ir, x))
#                       for x in os.listdir(dataset_dir_ir)]
# 转化所有图片
print('Start transforming vision images...')

for path in tqdm(image_filenames_vi):
    update(path[0], path[1])

