import os
from dotenv import load_dotenv
import crewai
import openai

# Load environment variables
load_dotenv()

# Test that we can access our API key (without printing it)
api_key = os.getenv("GOOGLE_API_KEY")


print("✅ CrewAI imported successfully")
print("✅ OpenAI imported successfully") 
print("✅ Environment variables loaded")
print(f"✅ Google API key loaded: {'YES' if api_key else 'NO'}")

print("\n🎉 Setup complete! Ready to build your interview prep app!")