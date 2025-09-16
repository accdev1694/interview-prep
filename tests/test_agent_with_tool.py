from src.agents.research_agent import research_agent

print(f"Agent has {len(research_agent.tools)} tool(s)")
print(f"Tool name: {research_agent.tools[0].name}")
print("✅ Agent and tool connected successfully!")