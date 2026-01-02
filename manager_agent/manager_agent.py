from agency_swarm import Agent, ModelSettings
from openai.types.shared import Reasoning

manager_agent = Agent(
    name="Manager Agent",
    description="Owns intake, task routing, QA, and delivery for research and media asset generation.",
    instructions="./instructions.md",
    files_folder=None,
    tools_folder=None,
    model="gpt-5.2",
    model_settings=ModelSettings(
        reasoning=Reasoning(effort="medium", summary="auto"),
    ),
)
