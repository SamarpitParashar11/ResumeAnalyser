import os

PROMPT_DIR = os.path.dirname(os.path.abspath(__file__))

def _read_prompt(filename: str) -> str:
    with open(os.path.join(PROMPT_DIR, filename), "r", encoding="utf-8") as file:
        return file.read()

def get_ats_prompt() -> str:
    return _read_prompt("ats_prompt.md")

def get_skills_prompt() -> str:
    return _read_prompt("skills_prompt.md")

def get_interview_prompt() -> str:
    return _read_prompt("interview_prompt.md")

def get_evaluation_prompt() -> str:
    return _read_prompt("evaluation_prompt.md")

def get_rewrite_prompt() -> str:
    return _read_prompt("rewrite_prompt.md")

def get_format_prompt() -> str:
    return _read_prompt("format_prompt.md")