import os
import shutil
import subprocess
import re
import sys
#import shlex  # fix filenames with parens

# Set the target year
TARGET_YEAR = 2023
LOCAL_SAVE_DIR = "./files"
delete_files = False
# Enable compression for ADB
set_compress = False
android_dir = "/sdcard/DCIM/Camera" # "/storage/*/DCIM/Camera/"
file_ext = "jpg"  # "mp4"

# Locate adb: macOS Android Studio SDK, or platform-tools unzipped into Downloads on Windows,
# falling back to whatever "adb" is on PATH
if sys.platform == "win32":
    ADB_PATH = os.path.expanduser("~/Downloads/platform-tools/adb.exe")
else:
    ADB_PATH = os.path.expanduser("~/Library/Android/sdk/platform-tools/adb")
if not os.path.isfile(ADB_PATH):
    ADB_PATH = shutil.which("adb")
if ADB_PATH is None:
    sys.exit("adb not found: install platform-tools (see README) or add adb to PATH")
# Ensure local directory exists
os.makedirs(LOCAL_SAVE_DIR, exist_ok=True)
""" Uses ADB to list all image files on the Android device's DCIM and Pictures folders. """
#result = subprocess.run([f"{ADB_PATH}", "shell", "find /sdcard/DCIM /sdcard/Pictures -type f -name '*.jpg' -o -name '*.png'"],
#result = subprocess.run([f"{ADB_PATH}", "shell", "find /sdcard/DCIM -type f -name '*.mp4'"],
#result = subprocess.run([f"{ADB_PATH}", "shell", f"find /sdcard/DCIM/Camera -type f -name '{TARGET_YEAR}*.mp4'"],
result = subprocess.run([f"{ADB_PATH}", "shell", f"find {android_dir} -type f -name '{TARGET_YEAR}*.{file_ext}'"],
                        capture_output=True, text=True)

files = result.stdout.strip().split("\n")

if set_compress:
    subprocess.run([f"{ADB_PATH}", "shell", "setprop service.adb.compress 1"], capture_output=True)

good_files = []
for file in files:
    if not file.strip():
        continue
    try:
        filename = os.path.basename(file)
        if filename.startswith(f"{TARGET_YEAR}"):
            good_files.append(file)
    except Exception as e:
        print(f"Error extracting date for {file}: {e}")

good_len = len(good_files)
dl_count = 0
failed_files = []
downloaded_files = []
for good_file in good_files:
    #good_file = shlex.quote(good_file)  # Fixes filenames with parens
    try:
        # Fallback: check file modified date (no reason to do this extra call, lets just use filename)
        #stat_result = subprocess.run([f"{ADB_PATH}", "shell", f"stat -c %y {file}"], capture_output=True, text=True)
        #match = re.search(r"(\d{4})-(\d{2})-(\d{2})", stat_result.stdout)
        #if match:
        #    #print('oh yeah')
        #    year = int(match.group(1))
        dl_count += 1
        print(f"Downloading {good_file} File {dl_count} of {good_len}")
        good_file_result = subprocess.run([ADB_PATH, "pull", "-a", good_file, LOCAL_SAVE_DIR], capture_output=True, text=True)
        if good_file_result.returncode == 0:
            downloaded_files.append(good_file)
        else:
            failed_files.append(good_file)
            print(f"  FAILED: {good_file_result.stderr.strip()}")
    except Exception as e:
        print(f"Error downloading {good_file}: {e}")
        failed_files.append(good_file)

if failed_files:
    print(f"\n{len(failed_files)} file(s) failed to download:")
    for f in failed_files:
        print(f"  {f}")

if set_compress:
    subprocess.run([ADB_PATH, "shell", "setprop service.adb.compress 0"], capture_output=True)

# TODO: Possibly implement a tar then pull like:
#adb shell "tar cf /cache/temp.tar /sdcard/DCIM/Camera/2021*.jpeg" && adb pull /cache/temp.tar && tar xf temp.tar && rm temp.tar
if delete_files:
    del_count = 0
    for del_file in downloaded_files:
        del_count += 1
        try:
            #del_count += 1
            print(f"Deleting {del_file} File {del_count} of {good_len}")
            #subprocess.run([ADB_PATH, "shell", "rm", "", del_file, LOCAL_SAVE_DIR], capture_output=True)
            subprocess.run([ADB_PATH, "shell", "rm", "", del_file], capture_output=True)
        except Exception as e:
            print(f"Error deleting {del_file}: {e}")
