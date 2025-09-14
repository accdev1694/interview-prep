import crewai
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Test that we can access our API key (without printing it)
api_key = os.getenv("OPENAI_API_KEY")


print("✅ CrewAI imported successfully")
print("✅ OpenAI imported successfully") 
print("✅ Environment variables loaded")
print(f"✅ Api key loaded: {'YES' if api_key else 'NO'}")
print(f"✅ Api key format looks correct: {'YES' if api_key and api_key.startswith('sk-') else 'NO'}")

print("\n🎉 Setup complete! Ready to build your interview prep app!")