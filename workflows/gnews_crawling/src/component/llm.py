import json
from typing import Dict, List, Optional
from litellm import Router


class LLMClient:
    def __init__(
        self,
        litellm_router: Router,
        model_name: str,
    ):
        self.litellm_router = litellm_router
        self.model_name = model_name
        self.config = {
            "model": model_name,
            "temperature": 0.5,
            "max_tokens": 1000,
            "top_p": 1,
        }

    def _parse_response(self, response, tools):
        """
        Process the response based on whether tools are used or not.

        Args:
            response: The raw response from API.
            tools: The list of tools provided in the request.

        Returns:
            str or dict: The processed response.
        """
        if tools:
            processed_response = {
                "content": response.choices[0].message.content,
                "tool_calls": [],
            }

            if response.choices[0].message.tool_calls:
                for tool_call in response.choices[0].message.tool_calls:
                    processed_response["tool_calls"].append(
                        {
                            "name": tool_call.function.name,
                            "arguments": json.loads(tool_call.function.arguments),
                        }
                    )

            return processed_response
        else:
            return response.choices[0].message.content

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        response_format=None,
        tools: Optional[List[Dict]] = None,
        tool_choice: str = "auto",
    ):

        params = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.config["temperature"],
            "max_tokens": self.config["max_tokens"],
            "top_p": self.config["top_p"],
        }
        if response_format:
            params["response_format"] = response_format
        if (
            tools
        ):  # TODO: Remove tools if no issues found with new memory addition logic
            params["tools"] = tools
            params["tool_choice"] = tool_choice

        response = await self.litellm_router.acompletion(**params)
        return self._parse_response(response, tools)
