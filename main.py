import fileinput
import os
from PIL import Image

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']


def merge_images(folder_path, images):
    pdf_path = (folder_path if folder_path[-1] == '/' else folder_path + '/') + 'merged_pdf.pdf'
    print(pdf_path)
    images = [
        Image.open(path)
        for path in images
    ]
    images[0].save(
        pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
    )
    exit()


def get_images(path):
    print('Wait a second while I\'m getting the images in the folder ', path)
    files = os.listdir(path)
    print('The files are : ', files)
    images = [path + '/' + f for f in files if f.split('.')[-1] in ALLOWED_EXTENSIONS]
    print('The following files will be merged : ', images)
    merge_images(path, images)


def prompt():
    print("Specify a folder path")

    for line in fileinput.input():
        line = line.strip()
        if line == 'exit':
            return True
        if os.path.isdir(line):
            get_images(line)
        else:
            print(os.path.isdir(line))
            print('You must specify a folder path')


"""
TODO : 
    - ADD HELP COMMAND
    - Pass folder path in second argument
    - Check if the ordering is OK. Else change it by hand
    - Add pdf file renaming
    - Check if pdf_file already exist and ask to replace if needed
    - Turn images when portrait
    - Can autocomplete path in stdin ?
"""
if __name__ == '__main__':
    prompt()
