from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
import src.agents.researcher as researcher
from src.prompts import AGENT_ORCHESTRATOR
from dotenv import load_dotenv

load_dotenv()

agent_orchestrator = create_agent( # Thought -> Action -> Observation and iterates
    model=ChatOpenAI(model="gpt-4o-mini", temperature=0),
    tools=[researcher.invoke_researcher_tool],
    system_prompt=AGENT_ORCHESTRATOR
)