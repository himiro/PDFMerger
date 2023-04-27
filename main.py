import fileinput
import os
import sys
from PIL import Image

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']


def merge_images(folder_path, images, pdf_name):
    pdf_path = (folder_path if folder_path[-1] == '/' else folder_path + '/') + pdf_name

    converted_images = []
    for path in images:
        im = Image.open(path)
        im = im.convert('RGB')
        converted_images.append(im)

    if len(converted_images) > 0:
        converted_images[0].save(
            pdf_path, "PDF", resolution=100.0, save_all=True, append_images=converted_images[1:]
        )
        print("########################################")
        print("###### PDF MERGED SUCCESSFULLY ! #######")
        print("########################################")
    else:
        print("#################################")
        print("###### NO IMAGES TO MERGE #######")
        print("#################################")


def order_images(images):
    order_indexes = []
    for image in images:
        print('Please specify the order of this image : ', image)
        for line in sys.stdin:
            line = line.strip()
            if line.isdigit():
                order_indexes.append(int(line))
                break
            else:
                print('Wrong order, the value must be an int')
                continue

    return [images[i] for i in order_indexes]


def get_images(path, pdf_name):
    print('Wait a second while I\'m getting the images in the folder ', path)
    files = os.listdir(path)
    images = [path + '/' + f for f in files if f.split('.')[-1] in ALLOWED_EXTENSIONS]
    print('The following files will be merged in this order : ', images)
    print('Are you sure you want to ? [y]/n')
    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0 or line.lower() == 'y' or line.lower() == 'yes':
            merge_images(path, images, pdf_name)
            return True
        elif line.lower() == 'n' or line.lower() == 'no' or line.lower() == 'exit':
            print('Please reorder the images with indices from 0 to ', len(images)-1)
            reordered_images = order_images(images)
            merge_images(path, reordered_images, pdf_name)
            return True
        else:
            continue


def select_directory(directory, pdf_name):
    directory = directory.strip()
    if os.path.isdir(directory):
        get_images(directory, pdf_name)
    else:
        print(os.path.isdir(directory))
        print('The directory path you specify is not a directory')


def print_help():
    print("USAGE : ./main.py -f FOLDER_PATH")
    print("-h | --help : print this help")
    print("-d | --directory : Specify the folder path where the images are. Default current directory")
    # print("--pdf-folder : Specify the folder path in which the merged pdf will be saved. Default in the same "
    #      "directory as the images")
    print("--pdf-name : Specify the name of the merged pdf file. Default name 'merged_pdf.pdf'")


def parse_arguments():
    args = sys.argv
    directory = './'
    pdf_name = 'merged_pdf.pdf'
    i = 1
    while i < len(sys.argv):
        if args[i] == '-h' or args[i] == '--help':
            print_help()
            return True
        elif args[i] == '-d' or args[i] == '--directory':
            if i == len(args) - 1 or not args[i + 1]:
                print("Directory not specified. Default current directory")
            else:
                i += 1
                directory = args[i]
                print('DIRECTORY SET : ', directory)
        elif args[i] == '--pdf-name':
            if i == len(args) - 1 or not args[i + 1]:
                print("Name not specified. Default name 'merged_pdf.pdf'")
            else:
                i += 1
                pdf_name = args[i] if args[i].rfind('.pdf') > 0 else args[i] + '.pdf'
                print('PDF NAME SET : ', pdf_name)
        else:
            print('Unknown command. ./main.py --help for more information')
            return True
        i += 1
    select_directory(directory, pdf_name)


"""
TODO : 
    - Check if the ordering is OK. Else change it by hand
    - Check if pdf_file already exist and ask to replace if needed
    - Turn images when portrait
    - Can autocomplete path in stdin ?
    - Write README
    - Create an executable
"""
if __name__ == '__main__':
    parse_arguments()
