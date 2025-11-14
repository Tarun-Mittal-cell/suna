from .api import agents, threads
from .agent import ChromaFlowAgent
from .thread import ChromaFlowThread
from .tools import AgentPressTools, MCPTools


class ChromaFlow:
    def __init__(self, api_key: str, api_url="https://suna.so/api"):
        self._agents_client = agents.create_agents_client(api_url, api_key)
        self._threads_client = threads.create_threads_client(api_url, api_key)

        self.Agent = ChromaFlowAgent(self._agents_client)
        self.Thread = ChromaFlowThread(self._threads_client)
