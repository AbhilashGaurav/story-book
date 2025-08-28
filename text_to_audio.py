# To run this code you need to install the following dependencies:
# pip install google-genai
import base64
import mimetypes
import os
import re
import struct
from google import genai
from google.genai import types
from api import YOUR_API_KEY
#save the binary data while converting the text to speech
def save_binary_file(file_name, data):
    f = open(file_name, "wb")
    f.write(data)
    f.close()
    print(f"File saved to to: {file_name}")

# generate function CHOOSE 1.model 2.speaker
def generate(speakerData,modelName="gemini-2.5-pro-preview-tts",voice1="Gacrux",voice2="Puck"):
    client = genai.Client(
        api_key=YOUR_API_KEY,
    )
#gemini-2.5-flash-preview-tts
#gemini-2.5-pro-preview-tts
    model = modelName
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"""like we are reading a story book, in a pleasent voice
{speakerData}
"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        response_modalities=[
            "audio",
        ],
        speech_config=types.SpeechConfig(
            multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                speaker_voice_configs=[
                    types.SpeakerVoiceConfig(
                        speaker="Speaker 1",
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=voice1
                            )
                        ),
                    ),
                    types.SpeakerVoiceConfig(
                        speaker="Speaker 2",
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=voice2
                            )
                        ),
                    ),
                ]
            ),
        ),
    )

    file_index = 0
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if (
            chunk.candidates is None
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None
        ):
            continue
        if chunk.candidates[0].content.parts[0].inline_data and chunk.candidates[0].content.parts[0].inline_data.data:
            file_name = f"ty"
            file_index += 1
            inline_data = chunk.candidates[0].content.parts[0].inline_data
            data_buffer = inline_data.data
            file_extension = mimetypes.guess_extension(inline_data.mime_type)
            if file_extension is None:
                file_extension = ".wav"
                data_buffer = convert_to_wav(inline_data.data, inline_data.mime_type)
            save_binary_file(f"{file_name}{file_extension}", data_buffer)
        else:
            print(chunk.text)

def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:

    parameters = parse_audio_mime_type(mime_type)
    bits_per_sample = parameters["bits_per_sample"]
    sample_rate = parameters["rate"]
    num_channels = 1
    data_size = len(audio_data)
    print(data_size)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size  # 36 bytes for header fields before data chunk size

    duration_sec = len(audio_data) / (sample_rate * num_channels * bytes_per_sample)
    print(f"Duration ≈ {duration_sec:.2f} sec")
    # http://soundfile.sapp.org/doc/WaveFormat/

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",          # ChunkID
        chunk_size,       # ChunkSize (total file size - 8 bytes)
        b"WAVE",          # Format
        b"fmt ",          # Subchunk1ID
        16,               # Subchunk1Size (16 for PCM)
        1,                # AudioFormat (1 for PCM)
        num_channels,     # NumChannels
        sample_rate,      # SampleRate
        byte_rate,        # ByteRate
        block_align,      # BlockAlign
        bits_per_sample,  # BitsPerSample
        b"data",          # Subchunk2ID
        data_size         # Subchunk2Size (size of audio data)
    )
    return header + audio_data

def parse_audio_mime_type(mime_type: str) -> dict[str, int | None]:

    bits_per_sample = 16
    rate = 24000

    # Extract rate from parameters
    parts = mime_type.split(";")
    for param in parts: # Skip the main type part
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate_str = param.split("=", 1)[1]
                rate = int(rate_str)
            except (ValueError, IndexError):
                # Handle cases like "rate=" with no value or non-integer value
                pass # Keep rate as default
        elif param.startswith("audio/L"):
            try:
                bits_per_sample = int(param.split("L", 1)[1])
            except (ValueError, IndexError):
                pass # Keep bits_per_sample as default if conversion fails

    return {"bits_per_sample": bits_per_sample, "rate": rate}

def text_to_audio():
    #gemini-2.5-flash-preview-tts
    #gemini-2.5-pro-preview-tts
    modelName="gemini-2.5-flash-preview-tts"
    # this below will be the dialogue
    with open("prompt//dialogue.txt", "r",encoding="utf-8",errors="replace") as f:
        dialogue = f.read()
    
    print(dialogue)
    speakerData=dialogue

    femaleVoices = [
    "Aoede",
    "Autonoe",
    "Callirrhoe",
    "Despina",
    "Enceladus",
    "Erinome",
    "Kore",
    "Laomedeia",
    "Leda",
    "Pulcherrima",
    "Sadachbia",
    "Schedar",
    "Sulafat",
    "Vindemiatrix",
    "Zubenelgenubi"
    ];

    maleVoices = [
    "Gacrux",
    "Puck",
    "Achernar",
    "Achird",
    "Algenib",
    "Algieba",
    "Alnilam",
    "Charon",
    "Fenrir",
    "Iapetus",
    "Orus",
    "Rasalgethi",
    "Sadaltager",
    "Umbriel",
    "Zephyr"
  ];

    generate(speakerData,modelName,maleVoices[6],femaleVoices[5])
