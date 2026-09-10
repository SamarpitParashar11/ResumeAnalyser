import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from prompts.prompt_reader import get_format_prompt
from dotenv import load_dotenv

load_dotenv()


def get_formatter_llm():
    model_name = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
    return ChatGoogleGenerativeAI(model=model_name, temperature=0)


def format_resume_chain(resume, llm=None):
    system_prompt = get_format_prompt()
    resume_json = resume.model_dump_json(indent=2)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Generate the HTML resume for the following data:\n\n{resume_json}"),
    ]
    active_llm = llm if llm is not None else get_formatter_llm()
    response = active_llm.invoke(messages)
    html_output = response.content

    if not isinstance(html_output, str):
        html_output = str(html_output)

    if "<!DOCTYPE html>" in html_output:
        html_output = html_output[html_output.index("<!DOCTYPE html>"):]

    return html_output