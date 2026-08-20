from google.adk.agents import Agent

from .tools import (
    calculate_average,
    create_file,
    generate_linkedin_post,
    push_to_github
)

root_agent = Agent(
    name="student_assistant",
    model="gemini-3.6-flash",
    description="A student assistant that can answer questions using study documents and manage code repository pushes.",
    instruction="""
    You are a helpful student assistant.

    Help students with questions about their studies.


    When the user asks you to calculate an average,
    use the calculate_average tool.

    When the user asks to create a file, use the create_file tool.

    When the user asks for content for a linkedin post, use the generate_linkedin_post tool.

    When the user asks to push the agent or codebase to GitHub, use the push_to_github tool.

    Answer clearly and concisely.
    """,
    tools=[
        calculate_average,
        create_file,
        generate_linkedin_post,
        push_to_github
    ],
)