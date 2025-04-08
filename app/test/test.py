# old test code
import os

from dotenv import load_dotenv

from utils.utils import generate_backstory

load_dotenv()  # Load environment variables from .env file
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")



# Test the function
name = "Cosmic Voyager"
powers = ["Teleportation", "Energy Manipulation", "Cosmic Awareness"]
backstory = generate_backstory(name, powers)
print(f"Backstory for {name}:")
print(backstory)