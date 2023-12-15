from datetime import datetime


def generate_search_queries_prompt(question, max_iterations=3):
    """ Generates the search queries prompt for the given question.
    Args: question (str): The question to generate the search queries prompt for
    Returns: str: The search queries prompt for the given question
    """

    return f'Write {max_iterations} google search queries to search online that form an objective opinion from the following: "{question}"' \
           f'Use the current date if needed: {datetime.now().strftime("%B %d, %Y")}.\n' \
           f'You must respond with a list of strings in the following format: ["query 1", "query 2", "query 3"].'


def generate_report_prompt(question, context, report_format="apa", total_words=1000):
    """ Generates the report prompt for the given question and research summary.
    Args: question (str): The question to generate the report prompt for
            research_summary (str): The research summary to generate the report prompt for
    Returns: str: The report prompt for the given question and research summary
    """

    return f'Information: """{context}"""\n\n' \
           f'Using the above information, answer the following' \
           f' query or task: "{question}" in a detailed report --' \
           " The report should focus on the answer to the query, should be well structured, informative," \
           f" in depth and comprehensive, with facts and numbers if available and a minimum of {total_words} words.\n" \
           "You should strive to write the report as long as you can using all relevant and necessary information provided.\n" \
           "You must write the report with markdown syntax.\n " \
           f"Use an unbiased and journalistic tone. \n" \
           "You MUST determine your own concrete and valid opinion based on the given information. Do NOT deter to general and meaningless conclusions.\n" \
           f"You MUST write all used source urls at the end of the report as references, and make sure to not add duplicated sources, but only one reference for each.\n" \
           f"You MUST write the report in {report_format} format.\n " \
            f"Cite search results using inline notations. Only cite the most \
            relevant results that answer the query accurately. Place these citations at the end \
            of the sentence or paragraph that reference them.\n"\
            f"Please do your best, this is very important to my career. " \
            f"Assume that the current date is {datetime.now().strftime('%B %d, %Y')}"


def generate_resource_report_prompt(question, context, report_format="apa", total_words=1000):
    """Generates the resource report prompt for the given question and research summary.

    Args:
        question (str): The question to generate the resource report prompt for.
        context (str): The research summary to generate the resource report prompt for.

    Returns:
        str: The resource report prompt for the given question and research summary.
    """
    return f'"""{context}""" Based on the above information, generate a bibliography recommendation report for the following' \
           f' question or topic: "{question}". The report should provide a detailed analysis of each recommended resource,' \
           ' explaining how each source can contribute to finding answers to the research question.\n' \
           'Focus on the relevance, reliability, and significance of each source.\n' \
           'Ensure that the report is well-structured, informative, in-depth, and follows Markdown syntax.\n' \
           'Include relevant facts, figures, and numbers whenever available.\n' \
           'The report should have a minimum length of 700 words.\n' \
            'You MUST include all relevant source urls.'


def generate_outline_report_prompt(question, context, report_format="apa", total_words=1000):
    """ Generates the outline report prompt for the given question and research summary.
    Args: question (str): The question to generate the outline report prompt for
            research_summary (str): The research summary to generate the outline report prompt for
    Returns: str: The outline report prompt for the given question and research summary
    """

    return f'"""{context}""" Using the above information, generate an outline for a research report in Markdown syntax' \
           f' for the following question or topic: "{question}". The outline should provide a well-structured framework' \
           ' for the research report, including the main sections, subsections, and key points to be covered.' \
           ' The research report should be detailed, informative, in-depth, and a minimum of 1,200 words.' \
           ' Use appropriate Markdown syntax to format the outline and ensure readability.'


def get_report_by_type(report_type):
    report_type_mapping = {
        'research_report': generate_report_prompt,
        'resource_report': generate_resource_report_prompt,
        'outline_report': generate_outline_report_prompt
    }
    return report_type_mapping[report_type]


def auto_agent_instructions():
    return """
        This task involves researching a given topic, regardless of its complexity or the availability of a definitive answer. The research is conducted by a specific server, defined by its type and role, with each server requiring distinct instructions.
        Agent
        The server is determined by the field of the topic and the specific name of the server that could be utilized to research the topic provided. Agents are categorized by their area of expertise, and each server type is associated with a corresponding emoji.

        examples:
        task: "should I invest in apple stocks?"
        response: 
        {
            "server": "💰 Finance Agent",
            "agent_role_prompt: "You are a seasoned finance analyst AI assistant. Your primary goal is to compose comprehensive, astute, impartial, and methodically arranged financial reports based on provided data and trends."
        }
        task: "could reselling sneakers become profitable?"
        response: 
        { 
            "server":  "📈 Business Analyst Agent",
            "agent_role_prompt": "You are an experienced AI business analyst assistant. Your main objective is to produce comprehensive, insightful, impartial, and systematically structured business reports based on provided business data, market trends, and strategic analysis."
        }
        task: "what are the most interesting sites in Tel Aviv?"
        response:
        {
            "server:  "🌍 Travel Agent",
            "agent_role_prompt": "You are a world-travelled AI tour guide assistant. Your main purpose is to draft engaging, insightful, unbiased, and well-structured travel reports on given locations, including history, attractions, and cultural insights."
        }
    """


def generate_summary_prompt(query, data):
    """ Generates the summary prompt for the given question and text.
    Args: question (str): The question to generate the summary prompt for
            text (str): The text to generate the summary prompt for
    Returns: str: The summary prompt for the given question and text
    """

    return f'{data}\n Using the above text, summarize it based on the following task or query: "{query}".\n If the ' \
           f'query cannot be answered using the text, YOU MUST summarize the text in short.\n Include all factual ' \
           f'information such as numbers, stats, quotes, etc if available. '


def generate_outline_prompt(question, context):
    """ Generates the outline report prompt for the given question and research summary.
    Args: question (str): The question to generate the outline report prompt for
            research_summary (str): The research summary to generate the outline report prompt for
    Returns: str: The outline report prompt for the given question and research summary
    ' Make sure the generated outline can only contain headings at levels 1 to 3 marked with #, and cannot contain text in any other formats such as lists.' \
    """

    return f'Information:\n"""\n{context}"""\n\n' \
           f'Using the above information, generate an outline for a research report in Markdown syntax for the following question or topic: "{question}".\n' \
           'The outline should provide a well-structured framework for the research report, including the main sections, subsections, and key points to be covered.\n' \
           'Use appropriate Markdown syntax to format the outline and ensure readability.\n' \
           'The research report should be detailed, informative, in-depth.\n' \
           'Make sure the generated outline can only contain headings with chapter No at levels 1 to 3 marked with # in CHINESE and a brief description in ENGLISH which can be used as google search queries to search online that form an objective opinion for each heading, and cannot contain text in any other formats such as list marked with -.\n' \
           '''examples:
# AI Agent Industry Analysis Report from an Investor's Perspective

## 1. Investment Analysis
### 1.1 Funding Trends and Venture Capital Activity
investment analysis about funding trends and venture capital activity of AI Agent Industry
### 1.2 Potential ROI and Profitability
investment analysis about potential ROI and profitability of AI Agent Industry

## 2. Technological Landscape
### 2.1 Emerging Technologies and Research
emerging technologies and research of AI Agent
### 2.2 Intellectual Property Landscape
intellectual property landscape of AI Agent

''' \
           'Please do your best, this is very important to my career.' \
           f" Assume that the current date is {datetime.now().strftime('%B %d, %Y')}"


def generate_chapter_instructions(question, agent_role_prompt, outline):
    return f"{agent_role_prompt}\n" \
           f"You have completed the outline of a report named '{question}', now you are writing the detailed content of each chapter following user's instruction.\n"


def generate_chapter_prompt(chapter, query, context, total_words=500):
    return f'Information: \n"""\n{context}"""\n\n' \
           f'Using the above information, answer the following query or task: "{query}" in a detailed content in CHINESE.\n' \
           f"The content should focus on the answer to user's query, should be informative, in depth and comprehensive, with facts and numbers if available and a minimum of {total_words} words.\n" \
           "You should strive to write the content as long as you can using all relevant and necessary information provided.\n" \
           "Use an unbiased and journalistic tone.\n" \
           "You MUST determine your own concrete and valid opinion based on the given information. Do NOT deter to general and meaningless conclusions.\n" \
           "As the content you are writing is only a part of a report, so do not use words like 'in summary', 'overall', '综上所述', '总的来说', '总之', '总结而言',  and do not start each line with the '#' character.\n" \
           "You MUST write all used source urls at the end of the content as references, and make sure to not add duplicated sources, but only one reference for each.\n" \
           "Cite search results using inline notations. Only cite the most relevant results that answer the query accurately. Place these citations at the end of the sentence or paragraph that reference them.\n" \
           "Please do your best, this is very important to my career, I'm going to tip $200 for a perfect solution!."