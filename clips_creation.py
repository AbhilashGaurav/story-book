from moviepy.editor import ImageClip

from separate_dialogue import separate_dialogue

def clips_creation():
  chunk_duration=separate_dialogue()[0]
  for i in range(0,10):
  # Load image
    clip = ImageClip(f"image-api//combined_horizontal{i}.jpg", duration=chunk_duration[i])  # 10 seconds

    # Write video
    clip.write_videofile(f"clips_video//output{i}.mp4", fps=24)
  
  #clips creation for thumbnail
  thumb_clip = ImageClip(f"image-api//thumbnail.jpg", duration=3)  # 10 seconds
  thumb_clip.write_videofile(f"clips_video//thumbnail.mp4", fps=24)

