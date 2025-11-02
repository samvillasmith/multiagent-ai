from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.config.settings import settings

def get_response_from_ai_agents(llm_id, query, allow_search, system_prompt):
    llm = ChatGroq(model=llm_id)
    tools = [TavilySearchResults(max_results=2)] if allow_search else []

    agent = create_react_agent(
        model=llm,
        tools=tools
        # Remove state_modifier - it doesn't exist!
    )

    # Build messages: Start with system prompt, then user messages
    messages = [SystemMessage(content=system_prompt)]
    messages.extend([HumanMessage(content=msg) for msg in query])
    
    state = {"messages": messages}
    response = agent.invoke(state)

    response_messages = response.get("messages")

    ai_messages = [message.content for message in response_messages if isinstance(message, AIMessage)] 

    return ai_messages[-1] if ai_messages else "No response generated"