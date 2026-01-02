from agency_swarm import Agent, ModelSettings
from agency_swarm.tools import IPythonInterpreter
from openai.types.shared import Reasoning

video_editor = Agent(
    name="Video Editor",
    description="Edits and renders videos via shell commands (ffmpeg workflow) with persistence across commands.",
    instructions="./instructions.md",
    files_folder=None,
    tools_folder=None,
    tools=[
        IPythonInterpreter
    ],
    model="gpt-5.2",
    model_settings=ModelSettings(
        reasoning=Reasoning(effort="medium", summary="auto"),
    ),
)
