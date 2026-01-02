from agency_swarm import Agent, ModelSettings
from agency_swarm.tools import WebSearchTool
from openai.types.shared import Reasoning

research_agent = Agent(
    name="Research Agent",
    description="Performs targeted web research and returns cited summaries and action-ready talking points.",
    instructions="./instructions.md",
    files_folder=None,
    tools_folder=None,
    tools=[WebSearchTool()],
    model="gpt-5.2",
    model_settings=ModelSettings(
        reasoning=Reasoning(effort="medium", summary="auto"),
    ),
)
