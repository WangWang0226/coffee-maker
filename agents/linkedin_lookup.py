import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from agents.callbacks import AgentCallbackHandler

from langchain import hub

from tools.tools import get_profile_url_tavily


def lookup(name: str, socketio) -> str:
    load_dotenv()

    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-4o-mini",
        callbacks=[AgentCallbackHandler(socketio)],
    )

    template = """given the full name {name_of_person} I want you to get it me a link to their linkedin profile page. 
        your answer should only conatin a URL"""

    prompt_template = PromptTemplate(template=template, input_variables=["name_of_person"])

    tools_for_agent = [
        Tool(
            name="Crawl Goolge for LinkedIn profile page",
            func=get_profile_url_tavily,
            description="useful for when you need to get the LinkedIn page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input= {"input": prompt_template.format_prompt(name_of_person=name)}
    )

    url = result["output"]
    return url


if __name__ == "__main__":
    linkedin_url = lookup(name="Licheng Wang")
    print(linkedin_url)
