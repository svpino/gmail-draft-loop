import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent, LoopAgent, SequentialAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.tools.tool_context import ToolContext

from gmail.prompts import (
    CRITIQUING_INSTRUCTIONS,
    DRAFTING_INSTRUCTIONS,
    EMAIL_FINDER_INSTRUCTIONS,
    REPLYING_INSTRUCTIONS,
)

load_dotenv()


def exit_loop(tool_context: ToolContext):
    tool_context.actions.escalate = True
    return {}


email_finder_agent = LlmAgent(
    name="EmailFinderAgent",
    model="gemini-2.5-flash",
    description="An assistant to automatically find emails.",
    instruction=EMAIL_FINDER_INSTRUCTIONS,
    tools=[
        McpToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=os.getenv("ZAPIER_MCP"),
            ),
        )
    ],
    output_key="current_email",
)

critiquing_agent = LlmAgent(
    name="CritiquingAgent",
    model="gemini-2.5-flash",
    include_contents="none",
    instruction=CRITIQUING_INSTRUCTIONS,
    description="Reviews the current draft, providing critique if clear improvements are needed, otherwise signals completion.",
    output_key="criticism",
)

drafting_agent = LlmAgent(
    name="DraftingAgent",
    model="gemini-2.5-flash",
    include_contents="none",
    instruction=DRAFTING_INSTRUCTIONS,
    description="Drafts the email based on critique, or calls exit_loop if critique indicates completion.",
    tools=[exit_loop],
    output_key="current_email",
)

refinement_loop = LoopAgent(
    name="RefinementLoop",
    sub_agents=[
        critiquing_agent,
        drafting_agent,
    ],
    max_iterations=3,
)


replying_agent = LlmAgent(
    name="ReplyingAgent",
    model="gemini-2.5-flash",
    description="An assistant to automatically creates draft replies.",
    instruction=REPLYING_INSTRUCTIONS,
    tools=[
        McpToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=os.getenv("ZAPIER_MCP"),
            ),
        )
    ],
)

root_agent = SequentialAgent(
    name="EmailAutoResponder",
    description="Finds relevant emails and iteratively drafts replies.",
    sub_agents=[email_finder_agent, refinement_loop, replying_agent],
)
