from exiftool import ExifToolHelper
import PySimpleGUIQt as sg
import os, shutil
from pathlib import Path

def rename_files_in_folder(folder_path: str):
    with ExifToolHelper() as et:
        for file in sorted(os.listdir(folder_path)):
            print(file, end=": ")
            file_tags = et.get_tags(Path(folder_path, file), ["Comment", "FileModifyDate"])
            if "QuickTime:Comment" in file_tags[0]:
                # insta 360 exported video
                date = file_tags[0]["QuickTime:Comment"][:19]
                new_file_name = date.replace(":", ".")
                new_file_name += file[-4:].lower()
                print(new_file_name)
                shutil.move(Path(folder_path, file), Path(folder_path, new_file_name))
            else:
                # video recorded from iphone camera
                date = file_tags[0]["File:FileModifyDate"][:19]
                new_file_name = date[:11].replace(":", "-")
                new_file_name += date[11:].replace(":", ".")
                new_file_name += "." + file.split(".")[-1].lower()
                print(new_file_name)
                shutil.move(Path(folder_path, file), Path(folder_path, new_file_name))

def main():
    layout = [
        [sg.Text("Footage folder:")],
        [sg.Input(key="-INPUT-"), sg.FolderBrowse(size=(10, .8))],
        [sg.Button("Run")]
    ]

    window = sg.Window("insta360-clip-renamer", layout)

    while True:
        event, values = window.read()
        
        if event in (None, sg.WIN_CLOSED):
            break

        print(event)

        if event == "Run":
            rename_files_in_folder(values["-INPUT-"])

    window.close()

if __name__ == "__main__":
    main()