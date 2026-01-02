from dotenv import load_dotenv
from agency_swarm import Agency

from manager_agent import manager_agent
from research_agent import research_agent
from assets_generator import assets_generator
from video_editor import video_editor

load_dotenv()


# do not remove this method, it is used in the main.py file to deploy the agency (it has to be a method)
def create_agency(load_threads_callback=None):
    # Avoid ingesting stale or incompatible stored threads by default
    load_cb = load_threads_callback or (lambda: [])
    agency = Agency(
        manager_agent,
        communication_flows=[
            (manager_agent, research_agent),
            (research_agent, manager_agent),
            (manager_agent, assets_generator),
            (assets_generator, manager_agent),
            (manager_agent, video_editor),
            (video_editor, manager_agent),
        ],
        name="VideoGenAgency",
        shared_instructions="shared_instructions.md",
        load_threads_callback=load_cb,
    )

    return agency


if __name__ == "__main__":
    agency = create_agency()
    agency.terminal_demo()
