# Automatically drafting emails

This is a sample multi-agent application that uses Google ADK and Zapier's MCP server to automatically draft email responses based on incoming emails in Gmail.

![Architecture Diagram](diagram.jpeg)

## Setup

Start by initializing a new Google ADK project and adding the necessary dependencies:

```bash
$ uv init
$ uv add google-adk google-genai python-dotenv
```

## Running the application

To run the application, you'll need to set up a few environment variables. Create a `.env` file in the root of the project and add the following:

```bash
GOOGLE_ADK_API_KEY=<your-api-key>
GOOGLE_GENAI_USE_VERTEXAI=0
ZAPIER_MCP=<your-zapier-mcp-url>
```

Then, run the application:

```bash
$ uv run adk run
```