from insight_researcher.config import Config
from insight_researcher.llm import LLM
from insight_researcher.memory import Memory
from insight_researcher.tools import Tool
from markdown_to_json import dictify
from collections import OrderedDict
from insight_researcher import log, cur_timestamp, write_report_to_file


class Agent:
    """
    Insight Researcher
    """

    def __init__(self, query, report_type="full_report"):
        self.task_id = cur_timestamp
        self.query = query
        self.report_type = report_type
        self.agent = None
        self.role = None
        self.cfg = Config()
        self.memory = Memory(self.cfg, self.task_id)
        self.tool = Tool(self.cfg, self.memory)
        self.llm = LLM(self.cfg, self.memory)

    def run(self):
        """
        Runs the Insight Researcher
        Returns:
            Report
        """
        if self.report_type not in ['outline_report', 'full_report']:
            raise ValueError(
                f"unsupported report_type: {self.report_type}, report_type must be one of ['outline_report', 'full_report']")

        task_id = cur_timestamp
        log.info(f"🔎 Running research for '{self.query}'...")
        # Generate Agent
        self.agent, self.role = self.llm.choose_agent(self.query)
        log.info(f'{self.agent}\n{self.role}')

        outline = self.generate_outline()
        log.debug(f"Finished writing outline...\n{outline}")
        if self.report_type == "outline_report":
            write_report_to_file(self.task_id, outline)
            return outline
        report = self.generate_report(outline)
        log.debug(f"Finished writing full report...\n{report}")
        write_report_to_file(self.task_id, report)
        return report

    def generate_outline(self):
        """
        generate outline
        Returns: outline
        """
        # Generate Sub-Queries including original query
        sub_queries = self.llm.get_sub_queries(self.query, self.role) + [self.query]
        log.info(f"🧠 I will conduct my research based on the following queries: {sub_queries}...")
        context = []
        # Run Sub-Queries
        for sub_query in sub_queries:
            log.info(f"🔎 Running research for '{sub_query}'...")
            scraped_sites = self.tool.scrape_sites_by_query(sub_query)
            similar_contents = self.memory.get_similar_content_by_query(sub_query, scraped_sites)
            context.append(similar_contents)
        log.info(f"✍️ Writing report for research task: {self.query}...")
        outline = self.llm.generate_outline(query=self.query, agent_role_prompt=self.role, context="\n".join(context))
        log.warning(f"Total running cost for outline: ${self.llm.get_total_cost():.3f}")
        return outline

    def generate_report(self, outline):
        """
        generate full report based on the outline
        Args:
            outline: Markdown formatted outline generated before

        Returns: full long report
        """
        leaf_chapters = self._get_outline_leaves(outline)
        report = outline
        for chapter, query in leaf_chapters.items():
            log.info(f"🔎 Running research for '{chapter}\n{query}'...")
            self.tool.scrape_sites_by_query(query)
            context = self.memory.retrieve_memory(query)
            log.info(f"✍️ Writing content for chapter: {chapter}\n{query}...")
            chapter_content = self.llm.generate_chapter(chapter=chapter, query=query, agent_role_prompt=self.role,
                                                        context=context)
            report = report.replace(query, chapter_content)
        log.warning(f"Total running cost for full report: ${self.llm.get_total_cost():.3f}")
        return report

    def _get_leaf_key_values(self, json_obj, current_path='', result=None):
        if result is None:
            result = OrderedDict()

        if isinstance(json_obj, dict):
            for key, value in json_obj.items():
                new_path = f"{current_path} - {key}" if current_path else key
                self._get_leaf_key_values(value, new_path, result)
        elif isinstance(json_obj, list):
            for index, item in enumerate(json_obj):
                new_path = f"{current_path}[{index}]"
                self._get_leaf_key_values(item, new_path, result)
        else:
            # 当前节点既不是字典也不是列表，因此是叶子节点
            result[current_path] = json_obj

        return result

    def _get_outline_leaves(self, markdown_outline):
        outline_dict = dictify(markdown_outline)
        return self._get_leaf_key_values(outline_dict)
