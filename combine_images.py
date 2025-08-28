#combine images
from PIL import Image
def combine_images():
  
  for i in range(0,10):

    # Open your two images
    img1 = Image.open(f"image-api\\{i+1}.png")
    img2 = Image.open(f"image-api\\story_with_text{i}.png")

    # Resize both to half width (960x1080 each)
    img1 = img1.resize((960, 1080))
    img2 = img2.resize((960, 1080))

    # Create a blank canvas
    final_img = Image.new("RGB", (1920, 1080))

    # Paste images
    final_img.paste(img1, (0, 0))         # left
    final_img.paste(img2, (960, 0))       # right

    # Save
    final_img.save(f"image-api//combined_horizontal{i}.jpg")
  return True