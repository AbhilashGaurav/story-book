import os
import re
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import google.generativeai as genai

# =====================================
# 1. Gemini: Generate YouTube Metadata
# =====================================
API_KEY = "YOUR_GEMINI_API_KEY"  # Replace with your Gemini API Key

def generate_youtube_metadata(content):
    genai.configure(api_key=API_KEY)

    system_instruction = """You are a YouTube SEO expert.  
From the given content (script, transcript, or summary), generate:

1. Title: A catchy, engaging, SEO-friendly YouTube video title (under 100 characters).  
2. Description: A well-structured video description (3–5 sentences). Summarize the video, use natural keywords, and encourage engagement (like/share/subscribe).  
3. Keywords: 10–15 high-ranking keywords relevant to the content.  
4. Tags: A comma-separated list of optimized YouTube tags.

Return the answer in this exact format:
Title: ...
Description: ...
Keywords: ...
Tags: ...
"""

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-preview-05-20",
        system_instruction=system_instruction
    )

    response = model.generate_content(content)
    if response.text:
        return response.text.strip()
    else:
        raise Exception("Gemini did not return metadata.")


# =====================================
# 2. YouTube Upload Functions
# =====================================
scopes = ["https://www.googleapis.com/auth/youtube.upload"]

def upload_video(file, title, description, tags, category="22", privacy="public"):
    # OAuth flow
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", scopes)
    credentials = flow.run_local_server(port=0)

    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials
    )

    # Upload video
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": category,
                "title": title,
                "description": description,
                "tags": tags
            },
            "status": {
                "privacyStatus": privacy
            }
        },
        media_body=file
    )
    response = request.execute()
    video_id = response["id"]

    print("✅ Upload successful! Video ID:", video_id)
    return youtube, video_id


def set_thumbnail(youtube, video_id, thumbnail_file):
    request = youtube.thumbnails().set(
        videoId=video_id,
        media_body=thumbnail_file
    )
    response = request.execute()
    print("✅ Thumbnail uploaded!")
    return response


# =====================================
# 3. Run the End-to-End Workflow
# =====================================
if __name__ == "__main__":
    # Load your script/summary
    with open("prompt//auto_generated_prompt.txt", "r", encoding="utf-8", errors="replace") as f:
        video_content = f.read()

    # Step 1: Get SEO metadata from Gemini
    metadata = generate_youtube_metadata(video_content)
    metadata.replace("*","")
    print("\n--- Generated Metadata ---\n", metadata, "\n")

    # Parse the response
    title = re.search(r"Title:\s*(.*)", metadata).group(1)
    description = re.search(r"Description:\s*(.*?)(?:Keywords:|Tags:)", metadata, re.S).group(1).strip()
    tags_line = re.search(r"Tags:\s*(.*)", metadata, re.S).group(1)
    tags = [tag.strip() for tag in tags_line.split(",")]

    # Step 2: Upload video
    youtube, video_id = upload_video(
        file="final_story_book.mp4",
        title=title,
        description=description,
        tags=tags,
        category="22",
        privacy="public"
    )

    # Step 3: Upload thumbnail
    set_thumbnail(youtube, video_id, "image-api//thumbnail.png")
