import image_upscale as iu
import csv


def csv_creator(pixels_data, labels_data):
    new_data_filename = r"..\data\new_data.csv"
    data = []

    for i in range(len(pixels_data)):
        image = iu.pic_upscale(pixels_data[i])
        image.append(labels_data[i])
        data.append(image)

    with open(new_data_filename, 'w') as f:
        writer = csv.writer(f, delimiter=';', lineterminator='\n')
        writer.writerows(data)
