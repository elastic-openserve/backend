import json
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

def get_audio_duration(audio_path):
    """Get audio duration using ffprobe"""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration", "-of",
         "default=noprint_wrappers=1:nokey=1", audio_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return float(result.stdout.decode().strip())

def generate_video(base_number):
    json_path = f'assets/{base_number}/audio_script_result.json'
    
    # Extract bucket_id
    with open(json_path, 'r') as f:
        data = json.load(f)
    bucket_id = data.get("bucket_id", base_number)
    base_path = f'assets/{bucket_id}'

    for section in ['top', 'bottom']:
        for idx, item in enumerate(data[section]):
            try:
                # Build common prefix
                prefix = f"{item['month']}_{item['age_group']}_{item['region']}_{section}_{idx}"
                
                image_path = f"{base_path}/{section}/{prefix}.png"
                audio_path = f"{base_path}/{section}/{prefix}.wav"

                # Open image & create canvas
                img = Image.open(image_path).convert('RGB')
                draw = ImageDraw.Draw(img)
                w, h = img.size

                # Fonts
                try:
                    font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 60)
                    font_body = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 30)
                    font_hashtags = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 40)
                except:
                    font_title = ImageFont.load_default()
                    font_body = ImageFont.load_default()
                    font_hashtags = ImageFont.load_default()

                # Draw Title
                draw.text((50, 50), item['title'], font=font_title, fill='white')

                # Draw Body
                draw.text((50, 200), item['body'], font=font_body, fill='white')

                # Draw Hashtags (blue)
                hashtags_text = " ".join(item['hashtags'])
                draw.text((50, h - 120), hashtags_text, font=font_hashtags, fill='blue')

                # Save edited image
                edited_image_path = f"{base_path}/{section}/{prefix}_edited.png"
                img.save(edited_image_path)

                # Get audio duration with ffprobe
                duration_sec = get_audio_duration(audio_path)

                # Output video name using the SAME prefix
                output_video = f"{base_path}/{section}/{prefix}.mp4"

                # ffmpeg command to create video
                cmd = [
                    "ffmpeg",
                    "-y",
                    "-loop", "1",
                    "-i", edited_image_path,
                    "-i", audio_path,
                    "-c:v", "libx264",
                    "-tune", "stillimage",
                    "-c:a", "aac",
                    "-b:a", "192k",
                    "-pix_fmt", "yuv420p",
                    "-shortest",
                    "-t", str(duration_sec),
                    output_video
                ]
                subprocess.run(cmd, check=True)
                print(f"✅ Video created: {output_video}")
            except Exception as e:
                print(f"❌ Error creating video: {e}")
                continue

    print("🎉 All videos created successfully!")


class VideoAgent:
    def __init__(self):
        pass

    def run(self, base_number):
        generate_video(base_number)
        return {"message": "Videos generated successfully!"}
    


VIDEO_AGENT = VideoAgent()
