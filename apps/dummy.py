import os

# List of extensions (You can add more if you want)
extensions = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Videos": [".mp4", ".mkv"],
    "Musics": [".mp3", ".wav"],
    "Zip": [".zip", ".tgz", ".rar", ".tar"],
    "Documents": [".pdf", ".docx", ".csv", ".xlsx", ".pptx", ".doc", ".ppt", ".xls"],
    "Setup": [".msi", ".exe"],
    "Programs": [".py", ".c", ".cpp", ".php", ".C", ".CPP"],
    "Design": [".xd", ".psd"]
}

# Create dummy files
for category, ext_list in extensions.items():
    for ext in ext_list:
        filename = f"{category.lower()}{ext}"
        with open(filename, "w") as f:
            f.write("This is a dummy file.")