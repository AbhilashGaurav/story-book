import story_text
import text_to_audio
import text_images
import visual_image
import combine_images
import clips_creation
import os

YOUR_API_KEY =os.environ.get('YOUR_API_KEY')
#1 run the below one time as the story will be changed as each time new story will be generated
story_text.story_text()
print("done story text")
# #2 audio bulk will be generated
text_to_audio.text_to_audio()
print("done audio")
#3 text_images will be generated
text_images.text_images()
print("done text images")
#4 visual images will be generated
visual_image.visual_image()
print("done visual images")
#5 combine the image(visual+text)
combine_images.combine_images()
print("done combine images")
#6 clips creation
clips_creation.clips_creation()
print("done clips creation") 

