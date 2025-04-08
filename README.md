# android-amazon-photos

An attempt to selectively get Photos from an Android phone to Amazon Photos, by using an intermediary Macbook.

# Why?
Amazon Photos Android App doesn't let you select a range of photos, upload them, and remove them from local storage

# Thought process
- Move a years worth of Photos to a temporary Macbook folder, making sure file modification times are preserved
  - Android SDK?
- Potentially edit the files (use Mac Photos)
- Use Mac Amazon Photos app to upload local folder

File [android_pictures.py](./android_pictures.py) is a working prototype
