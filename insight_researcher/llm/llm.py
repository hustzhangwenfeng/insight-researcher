from .prompts import *
import json
from insight_researcher import log
from colorama import Fore, Style
from .mock_provider import MockLLM
from .openai_provider import OpenAIGPTAPI


class LLM:
    def __init__(self, cfg, memory):
        self.cfg = cfg
        self.mock_llm = MockLLM()
        self.openai_llm = OpenAIGPTAPI(memory)
        self.memory = memory

    def choose_agent(self, query):
        """
        Chooses the agent automatically
        Args:
            query: original query

        Returns:
            agent: Agent name
            agent_role_prompt: Agent role prompt
        """
        if self.cfg.mock_llm:
            return self.mock_llm.choose_agent(query)
        try:
            response = self.openai_llm.send_chat_completion_request(
                model=self.cfg.smart_llm_model,
                messages=[
                    {"role": "system", "content": f"{auto_agent_instructions()}"},
                    {"role": "user", "content": f"task: {query}"}],
                temperature=0,
                llm_provider=self.cfg.llm_provider
            )
            agent_dict = json.loads(response)
            return agent_dict["server"], agent_dict["agent_role_prompt"]
        except Exception as e:
            log.error(f"Error in choose_agent: {e}")
            return "Default Agent", "You are an AI critical thinker research assistant. Your sole purpose is to write well written, critically acclaimed, objective and structured reports on given text."

    def get_sub_queries(self, query, agent_role_prompt):
        if self.cfg.mock_llm:
            return self.mock_llm.get_sub_queries(query, agent_role_prompt)
        log.info(f"ask llm to get_sub_queries for '{query}'")
        max_research_iterations = self.cfg.max_iterations if self.cfg.max_iterations else 1
        prompt = generate_search_queries_prompt(query, max_iterations=max_research_iterations)
        response = self.openai_llm.send_chat_completion_request(
            model=self.cfg.smart_llm_model,
            messages=[
                {"role": "system", "content": f"{agent_role_prompt}"},
                {"role": "user", "content": f"{prompt}"}],
            temperature=0,
            llm_provider=self.cfg.llm_provider
        )
        sub_queries = json.loads(response)
        return sub_queries

    def generate_report(self, query, context, agent_role_prompt, report_type, websocket=None):
        generate_prompt = get_report_by_type(report_type)
        report = ""
        try:
            log.info(f"ask llm to generate_report for '{query}'")
            report = self.openai_llm.send_chat_completion_request(
                model=self.cfg.smart_llm_model,
                messages=[
                    {"role": "system", "content": f"{agent_role_prompt}"},
                    {"role": "user", "content": f"{generate_prompt(query, context, self.cfg.report_format, self.cfg.total_words)}"}],
                temperature=0,
                llm_provider=self.cfg.llm_provider,
                stream=True,
                websocket=websocket,
                max_tokens=self.cfg.smart_token_limit
            )
        except Exception as e:
            print(f"{Fore.RED}Error in generate_report: {e}{Style.RESET_ALL}")

        return report

    def generate_outline(self, query, agent_role_prompt, context="", websocket=None):
        if self.cfg.mock_llm:
            return self.mock_llm.generate_outline(query, agent_role_prompt)
        outline = ""
        try:
            outline_prompt = generate_outline_prompt(query, context)
            log.info(f"ask llm to generate_outline for '{query}'")
            outline = self.openai_llm.send_chat_completion_request(
                model=self.cfg.smart_llm_model,
                messages=[
                    {"role": "system", "content": f"{agent_role_prompt}"},
                    {"role": "user", "content": f"{outline_prompt}"}],
                temperature=0,
                llm_provider=self.cfg.llm_provider,
                stream=True,
                websocket=websocket,
                max_tokens=self.cfg.smart_token_limit
            )
        except Exception as e:
            log.error(f"Error in generate_report: {e}")

        return outline

    def generate_chapter(self, chapter, query, agent_role_prompt, context="", websocket=None):
        content = ""
        try:
            log.info(f"ask llm to generate_chapter for '{chapter}'")
            chapter_prompt = generate_chapter_prompt(chapter, query, context, self.cfg.total_words)
            content = self.openai_llm.send_chat_completion_request(
                model=self.cfg.fast_llm_model,
                messages=[
                    {"role": "system", "content": f"{agent_role_prompt}"},
                    {"role": "user", "content": f"{chapter_prompt}"}],
                temperature=0,
                llm_provider=self.cfg.llm_provider,
                stream=True,
                websocket=websocket,
                max_tokens=self.cfg.smart_token_limit
            )
        except Exception as e:
            log.error(f"Error in generate_chapter: {e}")

        return content

    def get_total_cost(self):
        return self.openai_llm.get_total_cost()
