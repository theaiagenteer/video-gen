from agency_swarm import Agent, ModelSettings
from agency_swarm.tools import ImageGenerationTool
from openai.types.shared import Reasoning

assets_generator = Agent(
    name="Assets Generator",
    description="Produces voiceovers, code snapshots, and images.",
    instructions="./instructions.md",

    tools_folder="./tools",
    tools=[
        ImageGenerationTool(
            tool_config={
                "model": "gpt-image-1",
            }
        ),
    ],
    model="gpt-5.2",
    model_settings=ModelSettings(
        reasoning=Reasoning(effort="medium", summary="auto"),
    ),
)
