from google.adk.agents import Agent

github_card_agent = Agent(
    name="github_card_agent",
    model="gemini-1.5-flash",
    description="GitHub Developer Card Generator",
    instruction="""
    You analyze GitHub developer profiles and generate developer summaries.
    """
)