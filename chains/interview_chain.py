from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List
from enum import Enum

from prompts.prompt_reader import get_interview_prompt

class Difficulty(str, Enum):
    HARD = "HARD"
    MEDIUM = "MEDIUM"
    EASY = "EASY"


class InterviewQuestion(BaseModel):
    question: str
    difficulty: Difficulty

def create_context(name, role, skills, previous_questions):
    return f"""
    System Prompt : {get_interview_prompt()}
    Name : {name}
    Role : {role}
    Skills : {skills}
    Previous Questions : {previous_questions}
    """

def generate_question_chain(name, role, skills, previous_questions, llm):
    context = create_context(name, role, skills, previous_questions)
    prompt = ChatPromptTemplate.from_messages([("human", context)])
    structured_llm = llm.with_structured_output(InterviewQuestion)
    chain = prompt | structured_llm

    return chain