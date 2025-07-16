import os
import requests
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

io_intelligence_api_key = os.getenv("IOINTELLIGENCE_API_KEY", "default_api_key")

print(io_intelligence_api_key)

from pc_agent_remote.llm.base import BaseService

class IOIntelligenceService(BaseService):
    """
    Custom LLM service using IO Intelligence API.
    """

    def __init__(self, config: Dict[str, Any], agent_type: str):
        self.config_llm = config[agent_type]
        self.config = config
        self.max_retry = config.get("MAX_RETRY", 3)
        self.timeout = config.get("TIMEOUT", 30)

        self.api_key = self.config_llm["API_KEY"]
        self.model = self.config_llm.get("API_MODEL", "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8")
        self.base_url = self.config_llm.get(
            "API_BASE", "https://api.intelligence.io.solutions/api/v1"
        )

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        n: int = 1,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs: Any,
    ):
        
        print(f"Bearer ${io_intelligence_api_key} " )
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {io_intelligence_api_key} "        }


        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "n": n,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens,
            "reasoning_content": True,
            **kwargs
        }

        payload = {k: v for k, v in payload.items() if v is not None}

        for attempt in range(self.max_retry):
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
                response.raise_for_status()
                result = response.json()
                completions = [c["message"]["content"] for c in result.get("choices", [])]
                return completions, None
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retry - 1:
                    raise Exception(f"IOIntelligence API call failed after {self.max_retry} attempts: {e}")
        return completions, 0.0
