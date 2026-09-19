# android-amazon-photos

An attempt to selectively get Photos from an Android phone to Amazon Photos, by using an intermediary Macbook or Windows PC.

# Why?
Amazon Photos Android App doesn't let you select a range of photos, upload them, and remove them from local storage

# Thought process
- Move a years worth of Photos to a temporary Macbook or Windows PC folder, making sure file modification times are preserved
  - Android SDK?
- Potentially edit the files (use Mac Photos)
- Use Mac Amazon Photos app to upload local folder

File [android_pictures.py](./android_pictures.py) is a working prototype

# Requirements
Install [Android SDK Platform Tools](https://developer.android.com/tools/releases/platform-tools) (provides `adb`)

The script looks for `adb` in these locations, in order:
- macOS: `~/Library/Android/sdk/platform-tools/adb` (Android Studio install)
- Windows: `~/Downloads/platform-tools/adb.exe` (unzip `platform-tools-latest-windows.zip` into your Downloads folder)
- Otherwise, `adb` on your `PATH`

# Setup
Enable Developer Options
- About phone: Open your phone's Settings, scroll to the bottom, and tap About phone.
- Software information: Tap on Software information.
- Build number: Tap the Build number item 7 times rapidly until you see a message saying "Developer mode has been turned on".2.

Enable USB Debugging and File Transfer
- Developer options: Go back to your main Settings menu and tap the new Developer options menu at the very bottom.
- USB debugging: Scroll down and toggle on USB debugging. Confirm the prompt by tapping Allow or OK.
- Default USB configuration: Still inside Developer Options, look for Default USB configuration (or Select USB configuration) and change it to Transferring files or MTP (Media Transfer Protocol).
- Manual override: If your phone is already plugged in, swipe down your notification shade, tap the Android system notification regarding USB, and select Transferring files / MTP.

Debug: `adb devices`
