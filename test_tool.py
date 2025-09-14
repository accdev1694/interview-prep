from src.tools.web_search_tool import search_company_info

print("✅ Tool created successfully!")
print(f"✅ Tool name: {search_company_info.name}")
print(f"✅ Tool description available: {'Search for basic information' in search_company_info.description}")
print("\n🎉 Tool is ready to be used by CrewAI agents!")