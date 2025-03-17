import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
import random
import os
import time
from dotenv import load_dotenv
load_dotenv()


# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/debasmitroy/Desktop/programming/gemini-agent-assist/key.json"
os.environ["GOOGLE_CLOUD_PROJECT"] = "hackathon0-project"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"

class ImageGenerator:
    def __init__(self):
        vertexai.init(project=os.environ["GOOGLE_CLOUD_PROJECT"], location=os.environ["GOOGLE_CLOUD_LOCATION"])
        self.model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")

    def _generate(self,script_result, flag, randomly_genrated_local_bucket_id):
        for i,script in enumerate(script_result[flag][:2]):
            prompt = f"""You are image genrator AI Assistant. You are assigned to generate an image for a advertisement company.
            Here is the ad details:
            Title: {script['title']}
            Body: {script['body']}
            Month: {script['month']}
            Age Group: {script['age_group']}
            Region: {script['region']}

            Now, generate an image for the advertisement post. The image should be relevant to the product and the target demographics.
            """
            images = self.model.generate_images(
                prompt=prompt,
                # Optional parameters
                number_of_images=1,
                language="auto",
                # You can't use a seed value and watermark at the same time.
                # add_watermark=False,
                # seed=100,
                aspect_ratio="1:1",
                safety_filter_level="block_some",
                person_generation="allow_adult",
            )

            image_name = f"{script['month']}_{script['age_group']}_{script['region']}_{flag}_{i}.png"
            image_path = f"assets/{randomly_genrated_local_bucket_id}/{flag}/{image_name}"

            try:
                images[0].save(image_path)

                print(f"Image generated for {image_name}. Now delaying for 30 sec to avoid rate limit.")
                time.sleep(30)
            except Exception as e:
                print(f"Error while saving image: {e} for {image_name}")

    def run(self,script_result):
        randomly_genrated_local_bucket_id = str(random.randint(1000,9999))
        os.makedirs(f"assets/{randomly_genrated_local_bucket_id}/top", exist_ok=True)
        os.makedirs(f"assets/{randomly_genrated_local_bucket_id}/bottom", exist_ok=True)

        self._generate(script_result, "top", randomly_genrated_local_bucket_id)
        self._generate(script_result, "bottom", randomly_genrated_local_bucket_id)

        script_result["bucket_id"] = randomly_genrated_local_bucket_id
        return script_result
    


IMAGE_GENERATOR_AGENT = ImageGenerator()