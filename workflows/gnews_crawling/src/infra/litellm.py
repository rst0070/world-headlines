from typing import Optional
from litellm.router import Router
import litellm


def _get_model_list(
    gemini_api_key: Optional[str] = None,
    vllm_api_base: Optional[str] = None,
    openrouter_api_key: Optional[str] = None
) -> list[dict]:
    extra_headers = {}
    model_list = []

    if gemini_api_key:
        # For using google ai studio, only need to set gemini_api_key
        model_list.extend(
            [
                {
                    "model_name": "gemini-2.0-flash-lite",
                    "litellm_params": {
                        "model": "gemini/gemini-2.0-flash-lite-preview-02-05",
                        "api_key": gemini_api_key,
                        "timeout": 300,
                        "extra_headers": extra_headers,
                    },
                },
                {
                    "model_name": "gemini-2.0-flash",
                    "litellm_params": {
                        "model": "gemini/gemini-2.0-flash",
                        "api_key": gemini_api_key,
                        "timeout": 300,
                        "extra_headers": extra_headers,
                    },
                },
                {
                    "model_name": "gemini-2.5-flash",
                    "litellm_params": {
                        "model": "gemini/gemini-2.5-flash-preview-04-17",
                        "api_key": gemini_api_key,
                        "timeout": 300,
                        "extra_headers": extra_headers,
                    },
                },
            ]
        )

    if vllm_api_base:
        model_list.extend(
            [
                {
                    "model_name": "gemma-3-4b-it",
                    "litellm_params": {
                        "model": "hosted_vllm/google/gemma-3-4b-it",
                        "api_base": vllm_api_base,
                    }
                },
            ]
        )
    
    if openrouter_api_key:
        model_list.extend(
            [
                {
                    "model_name": "deepseek-r1-0528",
                    "litellm_params": {
                        "model": "openrouter/deepseek/deepseek-r1-0528",
                        "api_key": openrouter_api_key,
                        "api_base": "https://openrouter.ai/api/v1",
                    }
                }
            ]
        )

    return model_list


def get_litellm_router(
    gemini_api_key: Optional[str] = None,
    vllm_api_base: Optional[str] = None,
    openrouter_api_key: Optional[str] = None,
    redis_host: Optional[str] = None,
    redis_port: Optional[int] = None,
) -> Router:
    model_list = _get_model_list(
        gemini_api_key=gemini_api_key,
        vllm_api_base=vllm_api_base,
        openrouter_api_key=openrouter_api_key,
    )
    litellm.suppress_debug_info = True
    return Router(
        model_list=model_list,
        debug_level="DEBUG",
        redis_host=redis_host,
        redis_port=redis_port,
    )
