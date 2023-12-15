from langchain.adapters import openai as lc_openai
from colorama import Fore, Style
from openai import APIConnectionError
from tenacity import (
    after_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)
from insight_researcher import log
from .token_counter import (
    TOKEN_COSTS,
    count_message_tokens,
    count_string_tokens,
)


class OpenAIGPTAPI:
    def __init__(self, memory):
        self._cost_manager = CostManager()
        self.memory = memory

    @retry(
        wait=wait_random_exponential(min=1, max=60),
        stop=stop_after_attempt(6),
        after=after_log(log, log.level("WARNING").name),
        retry=retry_if_exception_type(APIConnectionError),
    )
    def send_chat_completion_request(self, messages, model, temperature=1.0, max_tokens=None, stream=False,
                                           llm_provider=None, websocket=None):
        log.debug(self.format_messages(messages))
        # validate input
        if model is None:
            raise ValueError("Model cannot be None")
        if max_tokens is not None and max_tokens > 8001:
            raise ValueError(f"Max tokens cannot be more than 8001, but got {max_tokens}")
        if not stream:
            result = lc_openai.ChatCompletion.create(
                model=model,  # Change model here to use different models
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                provider=llm_provider,  # Change provider here to use a different API
            )
            response = result["choices"][0]["message"]["content"]
            self._calc_and_update_costs(messages, response, model)
            msg = {"role": "assistant", "model": model, "content": response}
            log.debug(self.format_messages(msg))
            messages.append(msg)
            self.memory.add_messages(messages)
            return response
        else:
            paragraph = ""
            response = ""

            for chunk in lc_openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    provider=llm_provider,
                    stream=True,
            ):
                content = chunk["choices"][0].get("delta", {}).get("content")
                if content is not None:
                    response += content
                    paragraph += content
                    if "\n" in paragraph:
                        if websocket is not None:
                            websocket.send_json({"type": "report", "output": paragraph})
                        else:
                            print(f"{Fore.GREEN}{paragraph}{Style.RESET_ALL}")
                        paragraph = ""
            self._calc_and_update_costs(messages, response, model)
            msg = {"role": "assistant", "model": model, "content": response}
            log.debug(self.format_messages(msg))
            messages.append(msg)
            self.memory.add_messages(messages)
            return response

    def format_messages(self, messages):
        if isinstance(messages, list):
            return '\n' + '\n'.join(f'{msg["role"]}:\n{msg["content"]}' for msg in messages)
        elif isinstance(messages, dict):
            return '\n' + f'{messages["role"]}:\n{messages["content"]}'
        else:
            return '\n' + f'{messages}'

    def _update_costs(self, usage: dict, model):
        try:
            prompt_tokens = int(usage["prompt_tokens"])
            completion_tokens = int(usage["completion_tokens"])
            self._cost_manager.update_cost(prompt_tokens, completion_tokens, model)
        except Exception as e:
            log.error("updating costs failed!", e)

    def _calc_and_update_costs(self, messages: list[dict], rsp: str, model: str) -> dict:
        usage = {}
        try:
            prompt_tokens = count_message_tokens(messages, model)
            completion_tokens = count_string_tokens(rsp, model)
            usage["prompt_tokens"] = prompt_tokens
            usage["completion_tokens"] = completion_tokens
            self._update_costs(usage, model)
        except Exception as e:
            log.error("usage calculation failed!", e)

    def get_total_cost(self):
        return self._cost_manager.total_cost


class CostManager:
    """计算使用接口的开销"""

    def __init__(self):
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_cost = 0
        self.total_budget = 0

    def update_cost(self, prompt_tokens, completion_tokens, model):
        """
        Update the total cost, prompt tokens, and completion tokens.

        Args:
        prompt_tokens (int): The number of tokens used in the prompt.
        completion_tokens (int): The number of tokens used in the completion.
        model (str): The model used for the API call.
        """
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        cost = ((prompt_tokens * TOKEN_COSTS[model]["prompt"] + completion_tokens * TOKEN_COSTS[model]["completion"])
                / 1000)
        self.total_cost += cost
        log.warning(
            f"Total running cost: ${self.total_cost:.3f} | "
            f"Current cost: ${cost:.3f}, prompt_tokens: {prompt_tokens}, completion_tokens: {completion_tokens}"
        )
