
class MockLLM:
    def __int__(self, cfg=None, mock=False):
        self.cfg = cfg

    def choose_agent(self, query=None):
        return "📊 Market Research Agent", "作为一名专业的市场研究分析师AI助手，你的主要任务是根据提供的数据、行业趋势、技术发展和市场需求，撰写全面、深入、公正且系统化的行业分析报告。报告应专注于'AI Agent'赛道，包括但不限于市场规模、增长潜力、竞争格局、技术创新、主要参与者以及投资风险与机会。"

    def get_sub_queries(self, query=None, agent_role_prompt=None):
        return ["AI Agent industry market size and growth forecast",
                "investment risks and challenges in AI Agent industry",
                "emerging technologies and research of AI Agent"]

    def generate_outline(self, query=None, agent_role_prompt=None, websocket=None):
        return """# AI Agent行业分析报告：投资者视角

## 1. 市场概述
### 1.1 市场规模与增长预测
AI Agent industry market size and growth forecast
### 1.2 市场趋势分析
AI Agent industry market trends analysis
### 1.3 需求驱动因素
demand drivers in AI Agent industry

## 2. 竞争格局
### 2.1 主要参与者与市场份额
major players and market share in AI Agent industry
### 2.2 竞争策略与差异化
competitive strategies and differentiation in AI Agent industry
### 2.3 新进入者与退出壁垒
barriers to entry and exit for new players in AI Agent industry

## 3. 技术景观
### 3.1 新兴技术与研究
emerging technologies and research of AI Agent
### 3.2 知识产权格局
intellectual property landscape of AI Agent
### 3.3 技术创新与应用案例
technology innovation and use cases in AI Agent industry

"""