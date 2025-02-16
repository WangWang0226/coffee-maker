import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from agents.callbacks import AgentCallbackHandler

from langchain import hub

from tools.tools import get_profile_url_tavily

react_prompt = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}
"""

def lookup(name: str, socketio) -> str:
    load_dotenv()

    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-4o-mini",
        callbacks=[AgentCallbackHandler(socketio)],
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google for LinkedIn profile page",
            func=get_profile_url_tavily,
            description="useful for when you need to get the LinkedIn page URL",
        )
    ]

    prompt = PromptTemplate(
        template=react_prompt,
        input_variables=["input", "tools", "tool_names", "agent_scratchpad"],
    )

    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=prompt)

    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools_for_agent,
        verbose=True,
        handle_parsing_errors=True,
    )

    result = agent_executor.invoke(
        {"input": f"find me the LinkedIn profile URL for {name}"}
    )
    return result["output"]


if __name__ == "__main__":
    linkedin_url = lookup(name="Licheng Wang")
    print(linkedin_url)
