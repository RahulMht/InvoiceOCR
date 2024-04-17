import os

def rename_images(folder_path):
  """Renames image files in a folder serially with leading zeros.

  Args:
    folder_path: The path to the folder containing the images.
  """
  file_count = 1
  for filename in os.listdir(folder_path):
    # Check if file is an image (adjust extensions as needed)
    if os.path.splitext(filename)[1].lower() in (".jpg", ".jpeg", ".png"):
      # Generate new filename with leading zeros
      new_filename = f"{folder_path}/{file_count:03d}.{os.path.splitext(filename)[1]}"
      # Rename the file using os.rename
      os.rename(os.path.join(folder_path, filename), new_filename)
      file_count += 1

# Specify your folder path here
folder_path = r"C:\Users\DELL\Desktop\Fuseentrance"


# Call the function to start renaming
rename_images(folder_path)

print("Images renamed successfully!")
