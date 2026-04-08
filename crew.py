from crewai import Agent, Task, Crew
from crewai import LLM
from dotenv import load_dotenv
import os


# 1. LLM CONFIGURATION
def get_llm(temp):
    """Returns a configured LLM instance based on required temperature."""
    return LLM(
        model="llama-3.3-70b-versatile",
        temperature=temp,
        api_key=os.getenv("GROQ_API_KEY"),
        api_base="https://api.groq.com/openai/v1"
    )

def run_tone_crew(topic: str):
    # 2. AGENTS
    researcher = Agent(
        role="Fact-Based Researcher",
        goal=f"Provide a neutral, high-quality core explanation of {topic}.",
        backstory="You are a data-driven analyst. You provide raw, factual s" \
        "ummaries without any stylistic flair.",
        llm=get_llm(0.2),
        verbose=True
    )

    academic_writer = Agent(
        role="Academic Specialist",
        goal="Transform facts into scholarly, rigorous prose in academic tone.",
        backstory="Expert in peer-reviewed journals. You use complex vocabulary and formal structures.",
        llm=get_llm(0.1),
        verbose=True
    )

    conversational_writer = Agent(
        role="Friendly Explainer",
        goal="Transform facts into an engaging, warm, and simple narrative in a conversational tone.",
        backstory="You are a popular blogger. You use 'you' and 'we', analogies, and a lighthearted tone.",
        llm=get_llm(0.8),
        verbose=True
    )

    corporate_writer = Agent(
        role="Executive Communications Lead",
        goal="Transform facts into a concise, high-impact business briefing in corporate tone.",
        backstory="You write for CEOs. You focus on efficiency, professional jargon, and clarity.",
        llm=get_llm(0.3),
        verbose=True
    )

    # 3. TASKS
    # Each writing task uses 'context' to build upon the researcher's work
    research_task = Task(
        description=f"Research and summarize 5 core factual points about: {topic}.",
        expected_output="A list of 5 key factual points.",
        agent=researcher
    )

    academic_task = Task(
        description="Rewrite the research into formal academic paragraphs using scholarly language. Tone: Academic",
        expected_output="A scholarly analysis paragraph.",
        agent=academic_writer,
        context=[research_task]
    )

    conv_task = Task(
        description="Rewrite the research into a friendly, conversational explanation for a general audience. Tone: Conversational",
        expected_output="A warm and approachable explanation.",
        agent=conversational_writer,
        context=[research_task]
    )

    corp_task = Task(
        description="Rewrite the research into a professional, high-impact corporate briefing for executives. Tone: Corporate",
        expected_output="A polished business executive summary.",
        agent=corporate_writer,
        context=[research_task]
    )

    # 4. CREW EXECUTION
    crew = Crew(
        agents=[researcher, academic_writer, conversational_writer, corporate_writer],
        tasks=[research_task, academic_task, conv_task, corp_task],
        verbose=True
    )

    # Kickoff the process
    crew.kickoff()

    # 5. DATA EXTRACTION
    # Pulling the raw string from each specific task output to populate our tabs
    return {
        "academic": academic_task.output.raw,
        "conversational": conv_task.output.raw,
        "corporate": corp_task.output.raw
    }