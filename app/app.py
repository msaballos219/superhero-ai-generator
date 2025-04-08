from flask import Flask, request, render_template
import requests
from dotenv import load_dotenv
import os
import re

app = Flask(__name__)
load_dotenv()

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        description = request.form.get("description")

        api_url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "sonar",
            "messages": [
                {
                    "role": "system",
                    "content": "You're a creative AI who generates superhero names and rich backstories."
                },
                {
                    "role": "user",
                    "content": f"Generate a superhero based on the following description clearly. Format clearly as:\n\nName: <hero_name>\nBackstory: <hero_backstory>\n\nDescription: {description}"
                }
            ]
        }

        # Send API Request explicitly
        response = requests.post(api_url, headers=headers, json=payload)
        print("Status Code clearly:", response.status_code)
        print("Response Body explicitly:", response.text)


        if response.status_code == 200:
            api_result = response.json()
            # Extract the text message clearly from response
            generated_text = api_result["choices"][0]["message"]["content"]

            # Parse text explicitly and clearly to get Hero Name and Backstory
            name_match = re.search(r"Name:\s*(.+)", generated_text)
            backstory_match = re.search(r"Backstory:\s*(.+)", generated_text, re.DOTALL)

            hero_name = name_match.group(1).strip() if name_match else "Unknown Hero"
            hero_backstory = backstory_match.group(1).strip() if backstory_match else "No backstory provided."

            return render_template("index.html",
                                   description=description,
                                   hero_name=hero_name,
                                   hero_backstory=hero_backstory)
        else:
            error_message = "Something went wrong with the API call. Try again later!"
            return render_template("index.html",
                                   description=description,
                                   error=error_message)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)