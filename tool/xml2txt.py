import os
import xml.etree.ElementTree as ET


# 根据 xml 文件中的 name 选择生成的 txt 文件中的 id
def select_id(name):
    if name == "car":
        id = 0
    elif name == "truck":
        id = 1
    elif name == "bus":
        id = 2
    elif name == "van":
        id = 3
    elif name == "feright_car":
        id = 4

    return id


# YOLO 数据处理
def data_transform(height, width, xmin, ymin, xmax, ymax):
    # 中心点坐标 x_c,y_c
    x_c = (xmin + xmax) / 2
    y_c = (ymin + ymax) / 2

    # 中心横坐标与图像宽度比值 x_，中心纵坐标与图像高度比值 y_，bbox 宽度与图像宽度比值 w_，bbox 高度与图像高度比值 h_
    x_ = x_c / width
    y_ = y_c / height
    w_ = (xmax - xmin) / width
    h_ = (ymax - ymin) / height

    return x_, y_, w_, h_


def update_xml(input_xml_path, output_txt_path, crop_coords):
    # 解析XML文件
    tree = ET.parse(input_xml_path)
    root = tree.getroot()

    y0, y1, x0, x1 = crop_coords
    img_width, img_height = x1 - x0, y1 - y0

    # 更新图像大小信息
    size = root.find('size')
    if size is not None:
        if size.find('width') is not None:
            size.find('width').text = str(img_width)
        if size.find('height') is not None:
            size.find('height').text = str(img_height)
    else:
        print(f"Warning: 'size' element not found in {input_xml_path}")
        return  # 如果没有'size'节点，跳过该文件
    # 更新每个边界框的坐标
    # 生成对应的 txt 文件
    with open(output_txt_path, "w+", encoding='UTF-8') as out_file:
        for obj in root.findall('object'):
            name = obj.find('name').text
            if name == 'feright car':
                name = 'feright_car'
            elif name == 'feright':
                name = 'feright_car'
            elif name == '*':
                name = 'feright_car'
            else:
                name = name

            if obj.find('polygon'):

                bbox = obj.find('polygon')

                # 获取四个角点的坐标
                x1, y1 = int(bbox.find('x1').text), int(bbox.find('y1').text)
                x2, y2 = int(bbox.find('x2').text), int(bbox.find('y2').text)
                x3, y3 = int(bbox.find('x3').text), int(bbox.find('y3').text)
                x4, y4 = int(bbox.find('x4').text), int(bbox.find('y4').text)

                # 计算最小和最大边界值
                # min(x1, x2, x3, x4) - x0 计算出目标框左边界在裁剪区域中的新位置；同理，max(x1, x2, x3, x4) - x0 是右边界在裁剪区域的 x 坐标
                xmin, xmax = max(min(x1, x2, x3, x4) - x0, 0), min(max(x1, x2, x3, x4) - x0, img_width)
                ymin, ymax = max(min(y1, y2, y3, y4) - y0, 0), min(max(y1, y2, y3, y4) - y0, img_height)

                # 如果边界框在裁剪后的图像外，则删除此对象
                if xmin >= xmax or ymin >= ymax:
                    root.remove(obj)
                else:
                    x1 = x1-x0
                    y1 = y1-y0
                    x2 = x2-x0
                    y2 = y2-y0
                    x3 = x3-x0
                    y3 = y3-y0
                    x4 = x4-x0
                    y4 = y4-y0

                xmin1, xmax1, ymin1, ymax1 = [], [], [], []

                for i in [x1, x2, x3, x4]:
                    xmin1.append(i)
                    xmax1.append(i)
                for j in [y1, y2, y3, y4]:
                    ymin1.append(j)
                    ymax1.append(j)
                # 使用 min()、max() 方法获取最大值，最小值
                xmin1 = min(xmin1)
                xmax1 = max(xmax1)
                ymin1 = min(ymin1)
                ymax1 = max(ymax1)
                # yolo 格式转换
                result = data_transform(img_height, img_width, xmin1, ymin1, xmax1, ymax1)
                # id 选择
                result_id = select_id(name)


            elif obj.find('bndbox'):
                bbox = obj.find('bndbox')
                # 使用 .find() 方法获取对应 xml 文件中键的键值
                xmin = max(int(bbox.find('xmin').text) - x0, 0)
                ymin = max(int(bbox.find('ymin').text) - y0, 0)
                xmax = min(int(bbox.find('xmax').text) - x0, img_width)
                ymax = min(int(bbox.find('ymax').text) - y0, img_height)

                # 如果边界框在裁剪后的图像外，则删除此对象
                if xmin >= xmax or ymin >= ymax:
                    root.remove(obj)
                else:
                    # 更新边界框坐标
                    if bbox.find('xmin') is not None:
                        bbox.find('xmin').text = str(xmin)
                    if bbox.find('ymin') is not None:
                        bbox.find('ymin').text = str(ymin)
                    if bbox.find('xmax') is not None:
                        bbox.find('xmax').text = str(xmax)
                    if bbox.find('ymax') is not None:
                        bbox.find('ymax').text = str(ymax)

                xmin = bbox.find('xmin').text
                ymin = bbox.find('ymin').text
                xmax = bbox.find('xmax').text
                ymax = bbox.find('ymax').text
                x1 = int(xmin)
                y1 = int(ymin)
                x3 = int(xmax)
                y3 = int(ymax)
                # yolo 格式转换
                result = data_transform(img_height, img_width, x1, y1, x3, y3)
                # id 选择
                result_id = select_id(name)

            # 创建 txt 文件中的数据
            data = str(result[0]) + " " + str(result[1]) + " " + str(result[2]) + " " + str(result[3]) + '\n'
            data = str(result_id) + " " + data
            out_file.write(data)

if __name__ == "__main__":
    # 文件路径
    data_dir_xml = ''
    output_dir_txt = ''
    os.makedirs(output_dir_txt, exist_ok=True)

    # 裁剪坐标
    crop_coords = (100, 612, 100, 740)

    # 处理XML文件
    for xml_file in os.listdir(data_dir_xml):
        input_xml_path = os.path.join(data_dir_xml, xml_file)
        txt_file = xml_file[:-4] + '.txt'
        output_txt_path = os.path.join(output_dir_txt, txt_file)
        update_xml(input_xml_path, output_txt_path, crop_coords)

    print("XML标签更新完成。")

