from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import os

from dotenv import load_dotenv
from typing import Tuple
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from agents.linkedin_lookup import lookup
from output_parser import summary_parser, Summary
from third_parties.scrap_linkedin_profile import scrap_linkedin_profile

def make_coffee_with(name, socketio) -> Tuple[Summary, str]:
    load_dotenv()

    linkedin_url = lookup(name=name, socketio=socketio)
    print(linkedin_url)

    linkedin_data = scrap_linkedin_profile(linkedin_profile_url=linkedin_url, mock=True)

    summary_template = """
    give the LinkedIn information {information} about a person from I want you to create:
    1. a short summary
    2. three coffee chat questions to ask this person based on their background and experience
    \n{format_instructions}
    """

    summary_promt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-4o-mini",
    )
    chain = summary_promt_template | llm | summary_parser

    res = chain.invoke(input={"information": linkedin_data})

    return res, linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    make_coffee_with("licheng Wang")
