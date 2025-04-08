import os
import subprocess
import re
#import shlex  # fix filenames with parens

# Set the target year
TARGET_YEAR = 2023
LOCAL_SAVE_DIR = "./files"

ADB_PATH = os.path.expanduser("~/Library/Android/sdk/platform-tools/adb")
# Ensure local directory exists
os.makedirs(LOCAL_SAVE_DIR, exist_ok=True)
""" Uses ADB to list all image files on the Android device's DCIM and Pictures folders. """
#result = subprocess.run([f"{ADB_PATH}", "shell", "find /sdcard/DCIM /sdcard/Pictures -type f -name '*.jpg' -o -name '*.png'"],
#result = subprocess.run([f"{ADB_PATH}", "shell", "find /sdcard/DCIM -type f -name '*.jpg'"],
#result = subprocess.run([f"{ADB_PATH}", "shell", "find /sdcard/DCIM -type f -name '*.mp4'"],
#result = subprocess.run([f"{ADB_PATH}", "shell", f"find /sdcard/DCIM/Camera -type f -name '{TARGET_YEAR}*.mp4'"],
result = subprocess.run([f"{ADB_PATH}", "shell", f"find /sdcard/DCIM/Camera -type f -name '{TARGET_YEAR}*.jpg'"],
                        capture_output=True, text=True)

photos = result.stdout.strip().split("\n")

# Enable compression for ADB
subprocess.run([f"{ADB_PATH}", "shell", "setprop service.adb.compress 1"], capture_output=True)

good_photos = []
for photo in photos:
    if not photo.strip():
        continue
    try:
        filename = os.path.basename(photo)
        if filename.startswith(f"{TARGET_YEAR}"):
            good_photos.append(photo)
    except Exception as e:
        print(f"Error extracting date for {photo}: {e}")

good_len = len(good_photos)
dl_count = 0
for good_photo in good_photos:
    #good_photo = shlex.quote(good_photo)  # Fixes filenames with parens
    try:
        # Fallback: check file modified date (no reason to do this extra call, lets just use filename)
        #stat_result = subprocess.run([f"{ADB_PATH}", "shell", f"stat -c %y {photo}"], capture_output=True, text=True)
        #match = re.search(r"(\d{4})-(\d{2})-(\d{2})", stat_result.stdout)
        #if match:
        #    #print('oh yeah')
        #    year = int(match.group(1))
        dl_count += 1
        print(f"Downloading {good_photo} File {dl_count} of {good_len}")
        subprocess.run([ADB_PATH, "pull", "-a", good_photo, LOCAL_SAVE_DIR], capture_output=True)
    except Exception as e:
        print(f"Error extracting date for {good_photo}: {e}")
    #finally:
    #    if os.path.exists(temp_file):
    #        os.remove(temp_file)

# Disable compression after transfer
subprocess.run([ADB_PATH, "shell", "setprop service.adb.compress 0"], capture_output=True)

# TODO: Possibly implement a tar then pull like:
#adb shell "tar cf /cache/temp.tar /sdcard/DCIM/Camera/2021*.jpeg" && adb pull /cache/temp.tar && tar xf temp.tar && rm temp.tar
delete_files = False
del_count = 0
if delete_files:
    for del_photo in good_photos:
        del_count += 1
        try:
            #del_count += 1
            print(f"Deleting {del_photo} File {del_count} of {good_len}")
            subprocess.run([ADB_PATH, "shell", "rm", "", del_photo, LOCAL_SAVE_DIR], capture_output=True)
        except Exception as e:
            print(f"Error extracting date for {del_photo}: {e}")
