from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List

from prompts.prompt_reader import get_ats_prompt

class ATSResponse(BaseModel):
    ats_score: int
    strengths: List[str]
    weaknesses: List[str]
    missing_keywords: List[str]
    improvements: List[str]
    summary: str


def create_context(resume):
    return f"""
    System Prompt : {get_ats_prompt()}
    Resume : {resume}
    """

def analyze_resume_chain(resume_text: str, llm):
    context = create_context(resume_text)
    prompt = ChatPromptTemplate.from_messages([("human", context)])
    structured_llm = llm.with_structured_output(ATSResponse)
    chain = prompt | structured_llm

    return chain