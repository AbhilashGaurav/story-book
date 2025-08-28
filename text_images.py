from PIL import Image, ImageDraw, ImageFont
import textwrap
import separate_dialogue
def generate_text_image(text, output_file="story_text.png", image_size=(960, 1080), margin=50, font_size=52):
    # Create blank white image
    img = Image.new("RGB", image_size, "#E8DFC5")
    draw = ImageDraw.Draw(img)

    # Load fonts
    try:
        font_regular = ImageFont.truetype("ttf_file//NotoSansDevanagari-Regular.ttf", font_size)
        font_bold = ImageFont.truetype("ttf_file//NotoSansDevanagari-Bold.ttf", font_size)
    except:
        font_regular = ImageFont.load_default()
        font_bold = font_regular

    max_width = image_size[0] - 2 * margin

    # Wrap text dynamically
    lines = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        words = paragraph.split(" ")
        line = ""
        for word in words:
            test_line = line + word + " "
            if font_regular.getlength(test_line) <= max_width:
                line = test_line
            else:
                lines.append(line.strip())
                line = word + " "
        if line:
            lines.append(line.strip())

    # Draw text
    y = margin
    line_height = font_regular.getbbox("अ")[3] + 10

    for line in lines:
        if ":" in line:  # Has a speaker name
            speaker, dialogue = line.split(":", 1)
            # Draw speaker in bold
            draw.text((margin, y), speaker + ":", font=font_bold, fill=(0, 0, 0))
            # Draw dialogue right after speaker
            speaker_width = font_bold.getlength(speaker + ": ")
            draw.text((margin + speaker_width, y), dialogue.strip(), font=font_regular, fill=(0, 0, 0))
        else:
            draw.text((margin, y), line, font=font_regular, fill=(0, 0, 0))

        y += line_height

    img.save(output_file)
    return output_file

def text_images():
    dialogue = separate_dialogue.separate_dialogue()
    # this is text_image per page text used
    text_image=dialogue[1]
    for i in range(len(text_image)):
      ans=[]
      # ans.append(text_image[i].strip(character_names[0]))
      ans=text_image[i].split("%%")
      # for j in
      ans=ans[1:]
      story_Segment=""
      for j in ans:
        # print(j)
        story_Segment+=j+"\n"
    
      generate_text_image(story_Segment, f"image-api//story_with_text{i}.png")
    