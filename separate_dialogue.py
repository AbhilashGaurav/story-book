import numpy as np
from pydub import AudioSegment
import re
from story_text import characters_name # for characters name

# to divide into proper chunks and to calculate the duration of chunks

# reading the dialogue file 
def separate_dialogue():
    with open("prompt//dialogue.txt", "r",encoding="utf-8",errors="replace") as f:
        dialogue = f.read()
        
    list1=dialogue
    page_division=list1.count("speaker") # total number of speakers
    
    chunk = page_division //10 # proper chunks
    chunk_list=[chunk]*10
    
    for i in range (page_division%10):
      chunk_list[i]+=1

    # now breaking the data into chunks
    # sentence = list1

    # Split into speakers
    parts = re.split(r"(speaker)", list1)
    speakers = [parts[i].strip() + " " + parts[i+1].strip() for i in range(1, len(parts), 2)]

    chunk_data = []
    idx = 0

    for size in chunk_list:
        chunk_data.append(speakers[idx:idx+size])
        idx += size
    chunk_data = [list(chunk) for chunk in chunk_data]  # convert numpy arrays to lists
    # print(chunk_data)
    #########################################
    merged_sentences = [" ".join(inner) for inner in chunk_data]
    
    # from here the chunk data is separted into two parts 1: for audio_duration
    # 2: part for dialouge in a image

    #part 1 for text inside the image part
    text_image=merged_sentences.copy()
    
    # part 2 for audio duration
    audio_text=merged_sentences.copy()


    # fetching the character names from the prompt file
    with open("prompt//auto_generated_prompt.txt", "r", encoding="utf-8") as f:
        auto_generated_prompt = f.read()

    character_names=characters_name(auto_generated_prompt)
    print(character_names)
    total_count=0
    chunk_list=[]
    for i in range(0,len(audio_text)):
      audio_text[i]=audio_text[i].replace("speaker 1: ","").replace("speaker 2: ", "").replace("\n","")
      if len(character_names)>=2:
          text_image[i]=text_image[i].replace("speaker 1: ","%%"+character_names[0] + ": ").replace("speaker 2: ", "%%"+character_names[1] + ": ").replace("\n","")
      else:
          text_image[i]=text_image[i].replace("speaker 1: ","%%"+"speaker 1" + ": ").replace("speaker 2: ", "%%"+"speaker 2" + ": ").replace("\n","")
      # print(text_image[i])
      
      # if i==0:
        # print(merged_sentences[0])
      chunk_list.append(len(audio_text[i]))
      total_count+=len(audio_text[i])
      
    # print(text_image)

    #############################################

    # Load full audio (generated in one go)
    audio = AudioSegment.from_file("ty.wav")
    total_duration = len(audio)  # in ms

    # Total parts = sum of chunk lengths
    total_parts = sum(chunk_list)

    # Calculate per-chunk duration
    chunk_durations = []
    current_time = 0

    for size in chunk_list:
        # proportional duration
        duration_part = int((size / total_parts) * total_duration)
        chunk_durations.append(duration_part / 1000)  # in seconds

        # optional: slice & save
        # chunk_audio = audio[current_time:current_time + duration_part]
        # chunk_audio.export(f"chunk_{len(chunk_durations)}.wav", format="wav")

        current_time += duration_part
    # print("Chunk Durations (sec):", chunk_durations)
    return chunk_durations,text_image
    
    
    

  

