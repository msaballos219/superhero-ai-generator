import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Example: Load API key into a global variable
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
