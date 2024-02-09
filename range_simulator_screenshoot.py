from os import scandir, rename
from os.path import exists, join, splitext
from shutil import move
import os

import logging

# ! FILL IN BELOW
source_dir = "../Desktop"
dest_dir_sfx = "../Music"
dest_dir_music = "../Music/Music"
dest_dir_video = "../Movies"
dest_dir_image = "../Pictures"
dest_dir_documents = ""

# ? supported image types
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
# ? supported Video types
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
# ? supported Audio types
audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]

# ? supported Document types
document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

# ios simulator start character
character_ios = "Simulator Screenshot"


def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)

def on_cleaner():
    with scandir(source_dir) as entries:
        for entry in entries:
            name = entry.name
            check_audio_files(entry, name)
            check_video_files(entry, name)
            check_image_files(entry, name)
            check_document_files(entry, name)

def check_audio_files(entry, name):  # * Checks all Audio Files
    for audio_extension in audio_extensions:
        if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
            if entry.stat().st_size < 10_000_000 or "SFX" in name:  # ? 10Megabytes
                dest = dest_dir_sfx
            else:
                dest = dest_dir_music
            move_file(dest, entry, name)
            logging.info(f"Moved audio file: {name}")

def check_video_files(entry, name):  # * Checks all Video Files
    for video_extension in video_extensions:
        if name.endswith(video_extension) or name.endswith(video_extension.upper()):
            move_file(dest_dir_video, entry, name)
            logging.info(f"Moved video file: {name}")

def check_image_files(entry, name):  # * Checks all Image Files
    for image_extension in image_extensions:
        if name.endswith(image_extension) or name.endswith(image_extension.upper()):
            if name.find(character_ios) != -1:
                # Split the file name using the hyphen " - " to get all the element of the screenshoot file name
                split_result_name_file = name.split(' - ')
                
                # Get the string time element to range by date folder 
                date_element = split_result_name_file[-1].strip()
                
                # Get the simulator screen type
                simulator_element = split_result_name_file[1].strip()
                
                # Split the file date using the hyphen " at " to get all the day of screenshoot created
                split_day_folder = date_element.split(' at ')
                
                # Get the simulator screen type
                day_element = split_day_folder[0].strip()
                
                # Move the screenshoot to the day file
                file_destination = dest_dir_image + "/" + simulator_element + "/" + day_element

                # Check whether the specified path exists or not
                isExist = os.path.exists(file_destination)
                if not isExist:

                    # Create a new directory because it does not exist
                    os.makedirs(file_destination)
                    print("The new directory is created!")
                move_file(file_destination , entry, name)
                logging.info(f"Moved image file: {name}")
                
            else:
                move_file(dest_dir_image, entry, name)
                logging.info(f"Moved image file: {name}")
                print("Dans le else")
                
            

def check_document_files(entry, name):  # * Checks all Document Files
    for documents_extension in document_extensions:
        if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
            move_file(dest_dir_documents, entry, name)
            logging.info(f"Moved document file: {name}")
            
on_cleaner()