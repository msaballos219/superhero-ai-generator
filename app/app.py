from flask import Flask, render_template, request
from utils.clean_text import clean_generated_text
import requests
from openai import OpenAI
from dotenv import load_dotenv
import os
import re

app = Flask(__name__)
load_dotenv()

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY")

nebius_client = OpenAI(
    base_url="https://api.studio.nebius.com/v1/",
    api_key=NEBIUS_API_KEY
)

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        description = request.form.get("description")
        image_theme = request.form.get("image_theme")

        if not image_theme:
            image_theme = "Comicbook"

        # --- Text generation (Perplexity AI) ---
        pplx_url = "https://api.perplexity.ai/chat/completions"
        pplx_payload = {
            "model": "sonar",
            "messages": [
                {
                    "role": "system",
                    "content": "You generate superhero names and backstories."
                },
                {
                    "role": "user",
                    "content": f"Generate a superhero with a theme of {image_theme} based on: {description}. Do not add anything else. Do not use markdown for bolding or italics. Format explicitly as:\n\nName: <hero_name>\nBackstory: <hero_backstory>"
                }
            ]
        }
        pplx_headers = {
            "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }

        pplx_response = requests.post(pplx_url, headers=pplx_headers, json=pplx_payload)

        hero_name = clean_generated_text("Unknown Hero")
        hero_backstory = clean_generated_text("No backstory provided.")

        if pplx_response.status_code == 200:
            generated_text = pplx_response.json()["choices"][0]["message"]["content"]
            name_match = re.search(r"Name:\s*(.+)", generated_text)
            story_match = re.search(r"Backstory:\s*(.+)", generated_text, re.DOTALL)

            hero_name = name_match.group(1).strip() if name_match else hero_name
            hero_backstory = story_match.group(1).strip() if story_match else hero_backstory
        else:
            app.logger.error(f"Perplexity API Error: {pplx_response.status_code} - {pplx_response.text}")

        # --- Image generation clearly using NEBIUS API ---
        hero_image_url = None


        image_prompt = (f"A detailed, anatomically correct and vibrant {image_theme}-style portrait of superhero {hero_name},"
                f" depicted in a realistic heroic pose with accurate musculature, proportional limbs,"
                f" clear anatomy, correct joint articulation, highly detailed artwork, high resolution,"
                f" professional comic book illustration. Based on: {description}.")

        try:
            image_response = nebius_client.images.generate(
                model="black-forest-labs/flux-schnell",
                response_format="url",
                prompt=image_prompt,
                extra_body={
                "response_extension": "webp",
                "width": 1024,
                "height": 1024,
                "num_inference_steps": 5,  # Slightly increased explicitly for quality
                "negative_prompt": (
                    "bad anatomy, bad proportions, blurry, cloned face, cropped, deformed, dehydrated, disfigured, duplicate, error, extra arms, "
                    "extra fingers, extra legs, extra limbs, fused fingers, gross proportions, jpeg artifacts, long neck, low quality, lowres, malformed limbs, "
                    "missing arms, missing legs, morbid, mutated hands, mutation, mutilated, out of frame, poorly drawn face, poorly drawn hands, signature, text, "
                    "too many fingers, ugly, username, watermark, worst quality, "
                    "asymmetric eyes, misshapen muscles, twisted limbs, irregular joints, distorted face, incorrect bone structure, exaggerated proportions"),
                "seed": -1  # Explicitly non-random seed for consistency and repeatability of results
                }
            )
            hero_image_url = image_response.data[0].url
        except Exception as e:
            app.logger.error(f"Nebius API Exception: {str(e)}")

        return render_template("index.html",
                               hero_name=hero_name,
                               hero_backstory=hero_backstory,
                               hero_image_url=hero_image_url,
                               description=description)

    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)