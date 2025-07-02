import asyncio
from dotenv import load_dotenv
import os

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage


load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
stdio_server_params = StdioServerParameters(
    command="python",
    args=[
        "/Users/robertowalter/Documents/code/mcp-crash-course/langchain-mcp-adapters/servers/math_server.py"
    ],
)


async def main():
    # This communicate the Client with the Server
    async with stdio_client(stdio_server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Session initialized")
            tools = await load_mcp_tools(session)
            # print(tools)

            agent = create_react_agent(llm, tools)

            result = await agent.ainvoke(
                {"messages": [HumanMessage(content="What is 54 + 2 * 3?")]}
            )
            print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
