#important and working
#function generating the images
import requests, base64
from PIL import Image
from io import BytesIO
import re
import google.generativeai as genai
import os

YOUR_API_KEY=os.environ.get('YOUR_API_KEY')
# Story Segment: [Relevant dialogue/action for this page]


def prompt_gen(prompt_text,system_instruction,YOUR_API_KEY):
    """
    Generates content using a Gemini model with a system instruction.
    """
    # Check if the prompt is empty
    if not prompt_text.strip():
        raise ValueError("Prompt cannot be empty.")

    try:
        # Get API key from environment variables for security
        # Or, replace with your actual API key
        api_key = YOUR_API_KEY
        genai.configure(api_key=YOUR_API_KEY)

        if not api_key:
            raise ValueError("API key not found. Please set the GOOGLE_API_KEY environment variable.")

        # Correctly pass the API key and system instruction to the model
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash-latest',
            system_instruction=system_instruction,

        )

        # Generate content with the user's prompt
        response = model.generate_content(prompt_text)

        # Check for a valid response
        if response.text:
            return response.text.strip()
        else:
            # The model might return a block reason, which is an error in generation
            raise Exception("The model did not return a script. Block reason: " + str(response.prompt_feedback))

    except Exception as e:
        print(f"An error occurred: {e}")
        raise



def gen_image(prompt,image_num,API_KEY):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-preview-image-generation:generateContent?key={API_KEY}"

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"]
        }
    }

    print("🔄 Sending request to Gemini API...")
    response = requests.post(url, json=payload)

    if response.ok:
        result = response.json()
        # 4. Extract image base64
        candidates = result.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            for part in parts:
                if "inlineData" in part:
                    img_data = base64.b64decode(part["inlineData"]["data"])
                    img = Image.open(BytesIO(img_data))
                    img.save(f"image-api//{image_num}.png")
                    print(f"✅ Image saved at {image_num}.png")
                    break
            else:
                print("❌ No image data found in response")
                result = response.json()
                # 4. Extract image base64
                candidates = result.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    for part in parts:
                        if "inlineData" in part:
                            img_data = base64.b64decode(part["inlineData"]["data"])
                            img = Image.open(BytesIO(img_data))
                            img.save(f"image-api//{image_num}.png")
                            print(f"✅ Image saved at /image-api/{image_num}.png")
                            break
                else:
                  print("❌ Tried again")
        else:
            print("❌ No candidates in API response")
    else:
        print("❌ API call failed:", response.status_code, response.text)

def visual_image():
    # 🔑 Your Gemini API key
    API_KEY = os.environ.get('YOUR_API_KEY')
# delta prompt generation
    with open("prompt//auto_generated_prompt.txt", "r", encoding="utf-8") as f:
        auto_generated_prompt = f.read()
    
    with open("prompt//dialogue.txt", "r",encoding="utf-8",errors="replace") as f:
        dialogue = f.read()
    print("after it..................................")   
    # gamma prompt genreation
    delta_prompt=auto_generated_prompt+dialogue+"""You are a Storybook Visualizer. Your task is to generate a series of detailed illustration prompts. Each prompt should be suitable for an image generation agent like IllustratorSingleCall and maintain a consistent visual style throughout the story.
    
    For each distinct scene or 'page' in the dialogue, create a separate illustration prompt using the following format:
    
    Illustration Prompt for Page X:
    Style: [Consistent style for the entire story - e.g., 'A whimsical digital painting with a bright, cheerful palette, soft lighting, and clean linework, creating an optimistic storybook feel.']
    Scene: [Detailed description of the setting for this specific page/scene, including perspective and key environmental elements.]
    Subjects: [Detailed description of characters and objects present in this scene, maintaining consistent appearance for main characters as described in the premise. Include their actions and expressions.]
    Mood/Emotion: [The prevailing feeling or emotion of this specific scene.]
    
    Story Premise and Characters:
    take it from the above
    
    Hindi Dialogue Script (for scene breakdown):
    take it from the above"""
    
    system_instruction="Important instruction: 1.do complete it maximum 10 pages 2.do copy the style segement in each page rather then typing same as page 1 3.do show all the pages rather then showing Continue this format "
    illustration=prompt_gen(delta_prompt,system_instruction,API_KEY)
    # print(illustration_prompts)
    
    #do not add the Page 1
    # executing the image generation function
    pages = illustration.split("Illustration Prompt for Page")
    # print(pages)
    common = """**Consistent Visual Style for all Illustrations:**
    A whimsical digital painting with a bright, cheerful palette, soft, magical lighting, and clean, expressive linework. The overall feel should be optimistic and enchanting, reminiscent of classic storybook illustrations, with attention to detail in textures (like lint and fabric).
    """
    
    # print(pages[0])
    # print(pages)
    for i in range(1,len(pages)):
        # if pages[1] or pages[2]:
        # print(common+pages[i]+"""Important Instruction:
    # Do not include any text, letters, numbers, or writing inside the image. Only visual storytelling.""")
        gen_image(common+pages[i]+"""Important Instruction:
    # Do not include any text, letters, numbers, or writing inside the image. Only visual storytelling.""",i,API_KEY)

    # this is for thumbnail generation
    intial_thumb_prompt="""Create a vibrant, cinematic YouTube thumbnail in 16:9 ratio, HD quality (1920x1080). Do add the title of the story book. Take the elements from the below:"""
    # auto_generated_prompt=auto_generated_prompt.split("Premise:")[1]
    # auto_generated_prompt=auto_generated_prompt.split("Premise:")[1]
    thumbnail_prompt=intial_thumb_prompt+auto_generated_prompt
    # print(thumbnail_prompt)
    system_instruction="Help me to edit this prompt and generate and return the required prompt only other data should not be returned"
    thumb_gen_auto=prompt_gen(thumbnail_prompt,system_instruction,API_KEY)
    # print(thumb_gen_auto)
    gen_image(thumb_gen_auto,"thumbnail",API_KEY)
