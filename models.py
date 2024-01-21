from typing import List, Dict, Optional
from openai import OpenAI
import instructor
from pydantic import BaseModel
import together
import os

## Model definitions.
together_model_data = together.Models.list()
together_model_list = [
    m["name"].lower() for m in together_model_data if m.get("display_type", "") == "chat" if m.get("instances", []) != []
]

local_model_list = [
    "phi-2",
    "una-cybertron-7b-v2-bf16",
    "openhermes-2.5-neural-chat-7b-v3-1-7b",
]
openai_model_list = ["gpt-3.5-turbo-1106", "gpt-4-1106-preview"]

model_sizes = {m["name"].split("/")[-1].lower(): int(m.get("num_parameters", 0))/1e9 for m in together_model_data}
model_sizes.update({"gpt-3.5-turbo-1106": 170, "gpt-4-1106-preview": 400, "una-cybertron-7b-v2-bf16": 7})

## Map service names to model lists.
model_map = {
    "openai": openai_model_list,
    "together": together_model_list,
    "local": local_model_list,
}
service_map = {
    model: service for service, model_list in model_map.items() for model in model_list
}
model_list = list(set(service_map.keys()))


def get_client(service_name: str):
    """Get the client for the specified service."""
    if service_name == "openai":
        client = OpenAI()
    elif service_name == "together":
        client = OpenAI(
            base_url="https://api.together.xyz",
            api_key=os.environ.get("TOGETHER_API_KEY"),
        )
    elif service_name == "local":
        client = OpenAI(base_url="http://localhost:1234/v1")
    else:
        raise ValueError("Invalid service name.")
    return instructor.patch(client)


def query_model(
    model_name: str,
    messages: List[Dict[str, str]],
    temperature: float = 0.0,
    max_tokens: int = 2000,
    response_model: Optional[object] = None,
    stop: Optional[List[str]] = None,
):
    """Send prompt to LLM and get back a response message."""
    client = get_client(service_map[model_name])
    response = client.chat.completions.create(
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        stop=stop,
        response_model=response_model,
        messages=messages,
    )
    if response_model is None:
        message = response.choices[0].message.content
    else:
        message = response
    return message
