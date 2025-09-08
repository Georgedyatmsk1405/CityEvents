"""Place Search Agent

Streams Yandex MCP-powered search results for leisure places in Moscow using
pydantic-ai.

Configuration sources:
- llm_settings: OpenAI credentials and base URL (from .env)
- agents_settings: agent parameters like model_name, temperature (from config.yaml)
- agents_prompts: system prompt for SEARCH_AGENT (from prompts.yaml)
- search_settings: Yandex MCP settings (SEARCH_API_KEY, YANDEX_SEARCH_MCP_URL from .env)

Usage:
    agent = PlaceSearchAgent()
    nodes = await agent.iter_search("Найди бары в Москве в азиатском стиле")
    # or
    text = await agent.run("Найди бары в Москве в азиатском стиле")
"""

from typing import AsyncIterator, Optional

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerSSE
from app.agent.llm_factory import get_openai_chat_model

from app.setting import agents_settings, agents_prompts, search_settings


class PlaceSearchAgent:
    """Search agent with streaming support.

    - Builds model via shared factory using llm_settings and agents_settings.
    - Loads system prompt from agents_prompts["SEARCH_AGENT"]["SYSTEM_PROMPT"].
    - Connects to MCP server using search_settings (headers and SSE URL).

    Methods:
      - iter_search(query) -> list: collects streamed nodes and returns list
      - run(query) -> str: single-shot run that returns final text
    """

    def __init__(self) -> None:
        agent_cfg = agents_settings.get("agents", {})
        search_cfg = search_settings

        model_name = agent_cfg.get("model_name", "gpt-4o-mini")
        temperature = agent_cfg.get("temperature", 0.7)
        max_tokens = agent_cfg.get("max_tokens", 10000)
        top_p = agent_cfg.get("top_p", 0.95)

        model = get_openai_chat_model(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
        )

        system_prompt = (
            (
                (agents_prompts.get("SEARCH_AGENT", {}) or {}).get("SYSTEM_PROMPT")
                if isinstance(agents_prompts, dict)
                else None
            )
            or "Ты помощник по поиску мест для досуга в Москве. Отвечай структурировано."
        )

        mcp_api_key = search_cfg.search_api_key
        mcp_url = search_cfg.search_mcp_url
        mcp_headers = {"ApiKey": mcp_api_key} if mcp_api_key else {}
        mcp_client = MCPServerSSE(url=mcp_url, headers=mcp_headers)

        self._agent = Agent(
            name="place_search_agent",
            model=model,
            system_prompt=system_prompt,
            toolsets=[mcp_client],
        )

    async def iter_search(self, query: str) -> list:
        """Execute streaming run and return a list of streamed nodes.

        Note: For printing on the fly, iterate over agent.iter() yourself.
        This helper collects nodes to a list for convenience.
        """
        nodes = []
        async with self._agent.iter(query) as agent_run:
            async for node in agent_run:
                nodes.append(node)
        return nodes

    async def run(self, query: str) -> str:
        """Execute a non-streaming run and return the final text output."""
        result = await self._agent.run(query)
        return result.output
