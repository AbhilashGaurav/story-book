# story and auto prompt generation
import google.generativeai as genai
import os
import re
from api import YOUR_API_KEY
# Your API key. Leave this as an empty string; the environment will provide it at runtime.
# If you want to use models other than gemini-2.5-flash-preview-05-20, provide an API key here.
API_KEY = YOUR_API_KEY

def generate_creative_prompt(topic: str = "A mundane everyday event.") -> str:

    try:
        # Configure the Generative AI client with the API key.
        genai.configure(api_key=API_KEY)

        # System instructions are now passed to the GenerativeModel constructor
        system_instruction = (
            """Generate a completely unique and imaginative children’s story concept (not the full story) that has never been done before. Follow the structure below exactly:

1. Title: Give the story a short, catchy, original title.

2. Main Characters: Only Names without any other data

3. Premise: In 2–3 paragraphs, outline the main adventure, mystery, or challenge the children face, including emotional stakes, wonder, and engaging twists. Ensure the narrative naturally incorporates and showcases the following human values through the characters’ actions, dialogue, and decisions: Integrity, Honesty, Justice, Fairness, Responsibility, Accountability, Courage, Empathy, Compassion, Kindness, Forgiveness, Patience, Humility, Gratitude, Curiosity, Creativity, Critical Thinking, Wisdom, Self-discipline, Perseverance, Adaptability, Respect, Cooperation, Tolerance, Altruism, Loyalty, Solidarity, Self-awareness, Purpose, Hope, Faith, Belief, Connection to Nature, Transcendence, Punctuality, Cleanliness, Diligence, Generosity, Simplicity.

4. Tone: Keep it inspiring, age-appropriate, and designed to spark imagination. Teach values subtly through story elements, not by direct preaching.

Do not write the full story — only the scene setup and premise as described above."""
        )
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash-preview-05-20',
            system_instruction=system_instruction
        )

        response = model.generate_content(
            contents=[
                {"role": "user", "parts": [{"text": f"Generate a prompt based on this topic: {topic}"}]}
            ]
        )

        if response.text:
            print("Generated prompt:", response.text.strip())
            return response.text.strip()
        else:
            raise Exception("The model did not return a prompt.")

    except Exception as e:
        print(f"An error occurred during prompt generation: {e}")
        raise


def generate_hindi_dialogue_script(prompt: str) -> str:
    if not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    try:
        # Configure the Generative AI client with the API key.
        genai.configure(api_key=API_KEY)

        # System instructions are now passed to the GenerativeModel constructor
        system_instruction = (
          """You are a creative Hindi story generator. Use the following story concept as the basis for your work:

[INSERT STORY CONCEPT FROM PART A HERE]

Follow these rules strictly:
1. The story must be between 500–800 words.
2. Write entirely in Hindi.
3. The story must be told only through dialogues between two characters.
4. Clearly label dialogues as either "speaker 1: " or "speaker 2: ".
5. Every single line must start with either "speaker 1: " or "speaker 2: ".
6. Do not include narration, titles, scene descriptions, or explanations — only dialogue.
"""
        )
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash-preview-05-20',
            system_instruction=system_instruction
        )

        # Combine the user's prompt and the system instruction
        response = model.generate_content(
            contents=[
                {"role": "user", "parts": [{"text": prompt}]}
            ]
        )

        # Check for a valid response
        if response.text:
            return response.text.strip()
        else:
            raise Exception("The model did not return a script. Please try a different prompt.")

    except Exception as e:
        print(f"An error occurred: {e}")
        raise

def characters_name(text):
    character_names = []

    # Case 1: Multiline format (names listed line by line after "Main Characters:")
    match_block = re.search(r"Main Characters:\s*((?:.*\n)+?)(?=\d+\.|\Z)", text)
    if match_block:
        block = match_block.group(1)
        for line in block.splitlines():
            line = line.strip()
            if line and not line.lower().startswith("main characters"):
                character_names.append(line)

    # Case 2: Inline format (names after "Main Characters:" on same line)
    if not character_names:
        match_inline = re.search(r"Main Characters:\s*([^\n]+)", text)
        if match_inline:
            character_names = [name.strip() for name in match_inline.group(1).split(",")]
    if len(character_names)<2:
        if (len(character_names)==0:
            character_names.append("Speaker 1")
            character_names.append("Speaker 2")
        elif (len(character_names)==1:
            character_names.append("Speaker 2")
    return character_names
def story_text():
    # Example usage: The prompt is now generated automatically.
    try:
        # Generate a creative prompt first. You can provide a topic here or leave it empty.
        auto_generated_prompt = generate_creative_prompt()
        
        
        with open("prompt//auto_generated_prompt.txt", "w", encoding="utf-8") as f:
            f.write(auto_generated_prompt)
        
        # Now, use the generated prompt to create the Hindi dialogue
        dialogue = generate_hindi_dialogue_script(auto_generated_prompt)
        # print("\nGenerated Hindi Dialogue Script:")
        # print(dialogue)
        
        #save the dialogue to a text file
        with open("prompt//dialogue.txt", "w", encoding="utf-8") as f:
            f.write(dialogue)
        
###############################################################################
        #getting the characters name from the prompt

        # character_names=characters_name(auto_generated_prompt)
        # print(character_names)
        
        #save the character names to a text file


    except Exception as e:
        print(f"Failed to generate dialogue: {e}")


