from PIL import Image, ImageDraw, ImageFont
import textwrap
import separate_dialogue
import math

def generate_text_image(
    text,
    output_file="story_text.png",
    image_size=(960, 1080),
    margin=50,
    min_font_size=20,
    max_font_size=120
):
    img = Image.new("RGB", image_size, "#E8DFC5")
    draw = ImageDraw.Draw(img)

    max_width = image_size[0] - 2 * margin
    max_height = image_size[1] - 2 * margin

    def wrap_text(font):
        lines = []
        for paragraph in text.split("\n"):
            if not paragraph.strip():
                lines.append("")
                continue
            words = paragraph.split(" ")
            line = ""
            for word in words:
                test_line = line + word + " "
                if font.getlength(test_line) <= max_width:
                    line = test_line
                else:
                    lines.append(line.strip())
                    line = word + " "
            if line:
                lines.append(line.strip())
        return lines

    def measure_height(font, lines):
        line_height = font.getbbox("अ")[3] + 10
        return len(lines) * line_height, line_height

    # Start from a middle size and adjust
    font_size = min_font_size
    best_size = font_size

    for size in range(min_font_size, max_font_size + 1, 2):
        font_regular = ImageFont.truetype("ttf_file/NotoSansDevanagari-Regular.ttf", size)
        lines = wrap_text(font_regular)
        total_height, _ = measure_height(font_regular, lines)

        if total_height <= max_height:
            best_size = size  # safe size
        else:
            break  # too big, stop

    # Use the best size found
    font_size = best_size
    font_regular = ImageFont.truetype("ttf_file/NotoSansDevanagari-Regular.ttf", font_size)
    font_bold = ImageFont.truetype("ttf_file/NotoSansDevanagari-Bold.ttf", font_size)

    # Final wrap
    lines = wrap_text(font_regular)
    total_height, line_height = measure_height(font_regular, lines)

    # Center vertically
    y = margin + (max_height - total_height) // 2
    for line in lines:
        if ":" in line:
            speaker, dialogue = line.split(":", 1)
            draw.text((margin, y), speaker + ":", font=font_bold, fill=(0, 0, 0))
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
    