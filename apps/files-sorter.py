import os
import shutil

# Ask the user to enter the source directory path
source_dir = input("Enter the source directory path: ")

# Ask the user to enter the destination directory path
destination_dir = input("Enter the destination directory path: ")

# Ensure that the source and destination directory paths are valid
if not os.path.isdir(source_dir):
    print("Invalid source directory path.")
    exit()

if not os.path.isdir(destination_dir):
    print("Invalid destination directory path.")
    exit()

# List of extensions (You can add more if you want)
extensions = {
    "Images": [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".bmp", ".dib", ".svg", ".svgz", ".ico", ".ief", ".pnm", ".pbm", ".pgm", ".ppm", ".rgb", ".rgba", ".xbm", ".xpm", ".xwd"],
    "Videos": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".m4p", ".m4v", ".mpg", ".mpeg", ".mpe", ".mpv", ".mp2", ".mpeg2", ".m2v", ".svi", ".3gp", ".3g2", ".mxf", ".roq", ".nsv", ".flv", ".f4v", ".f4p", ".f4a", ".f4b", ".mkv", ".webm"],
    "Musics": [".3gp", ".aa", ".aac", ".aax", ".act", ".aiff", ".amr", ".ape", ".au", ".awb", ".dct", ".dss", ".dvf", ".flac", ".gsm", ".iklax", ".ivs", ".m4a", ".m4b", ".m4p", ".mmf", ".mp3", ".mpc", ".msv", ".nmf", ".nsf", ".ogg", ".oga", ".mogg", ".opus", ".ra", ".rm", ".raw", ".sln", ".tta", ".vox", ".wav", ".wma", ".wv", ".webm", ".8svx"],
    "Zip": [".zip", ".tar", ".tar.gz", ".tgz", ".tar.bz2", ".tbz2", ".tbz", ".txz", ".tar.xz", ".gz", ".bz2", ".rar", ".7z", ".xz", ".lz", ".lzma", ".z", ".Z"],
    "Documents": [".doc", ".docx", ".dot", ".dotx", ".docm", ".dotm", ".rtf", ".txt", ".pdf", ".odt", ".ott", ".fodt", ".sxw", ".stw", ".sxg", ".odf", ".uot", ".uof", ".csv", ".tsv", ".xls", ".xlsx", ".xlt", ".xltx", ".xlsm", ".xltm", ".xlsb", ".ods", ".ots", ".fods", ".sxc", ".stc", ".sxd", ".std", ".sxi", ".sti", ".pot", ".potx", ".ppt", ".pptx", ".pps", ".ppsx", ".odp", ".otp", ".fodp", ".sxi"],
    "Setup": [".exe", ".msi", ".bat", ".cmd", ".com", ".jar", ".scr"],
    "Programs": [".py", ".pyc", ".pyo", ".pyd", ".ipynb", ".c", ".cpp", ".h", ".hpp", ".cs", ".java", ".php", ".pl", ".pm", ".rb", ".sh", ".swift", ".vb", ".vbs", ".asm", ".pas", ".f90", ".f", ".for", ".lisp", ".scm", ".lua", ".tcl", ".awk", ".d", ".dart", ".go", ".hs", ".kt", ".rs", ".scala", ".vala", ".groovy"],
    "Design": [".ai", ".eps", ".ps", ".psd", ".svg", ".pdf", ".indd", ".cdr", ".dwg", ".dxf", ".skp", ".sketch", ".3dm", ".3ds", ".max", ".obj", ".blend", ".bvh", ".c4d", ".fbx", ".ma", ".mb", ".blend", ".dae", ".stl"]
}

# Create destination directories if they don't exist
for category in extensions.keys():
    category_dir = os.path.join(destination_dir, category.capitalize())  # Capitalize the category name
    os.makedirs(category_dir, exist_ok=True)

# Iterate over files in the source directory
for file in os.listdir(source_dir):
    # Get the file extension
    _, extension = os.path.splitext(file)
    extension = extension.lower()  # Ensure lowercase for consistent comparison

    # Find the category corresponding to the file extension
    category = None
    for cat, ext_list in extensions.items():
        if extension in ext_list:
            category = cat
            break

    if category:
        # Construct the destination path
        destination_path = os.path.join(destination_dir, category.capitalize(), file)
        source_path = os.path.join(source_dir, file)

        # Move the file to the destination directory
        try:
            shutil.move(source_path, destination_path)
        except Exception as e:
            print(f"Error moving {file}: {e}")
    else:
        # If category is not found, move the file to "others" directory
        destination_path = os.path.join(destination_dir, "Others", file)
        source_path = os.path.join(source_dir, file)

        try:
            shutil.move(source_path, destination_path)
        except Exception as e:
            print(f"Error moving {file}: {e}")
