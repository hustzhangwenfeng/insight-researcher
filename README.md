# insight-researcher
基于GPT4的自主AI Agent，可以使用联网搜索、本地知识库查询等工具，根据指定的研究问题写报告，例如写行业分析报告、科研综述报告。

---

基于AI Agent实现了一个自主科研的小工具🌿insight-researcher🌿，可根据用户的研究任务，一键生成万字长文报告，并且报告中引用的数据实时、可溯源，适合写行业研究报告、科研综述等。项目的总体架构如下：
![ebf5abb86b2e39c0f833ed29da0e1b1d](https://github.com/hustzhangwenfeng/insight-researcher/assets/18573957/1ca02ab5-5d3a-43fe-8822-a9a3507fd49e)

<br />

代码实现思路是，用agent来协调llm、memory和tools等模块，串起整个业务流程。具体实现流程如下：
![image](https://github.com/hustzhangwenfeng/insight-researcher/assets/18573957/7c397da7-2299-451d-8a29-51301d9eaa84)


## 解决了当前研究的如下几个痛点问题
- 人工主导的研究形成客观结论可能需要很长的时间才能找到相关的支撑数据和素材；
- 基于大模型辅助的方法受限于LLM的知识幻觉，输出的观点不可信、不可靠、不实时；
- 基于LLM + Web插件的方法，也无法输出超长（万字以上甚至几万字）全面而有深度的内容；
- 大部分的智能辅助手段都是HITL形式，需要复杂的交互和多轮的修改。

## 快速开始
> **步骤 0** - 安装 Python 3.11 或更高版本。[参见此处](https://www.tutorialsteacher.com/python/install-python) 获取详细指南。

<br />

> **步骤 1** - 下载项目：

```bash
$ git clone https://github.com/hustzhangwenfeng/insight-researcher
$ cd insight-researcher
```

<br />

> **步骤2** -安装依赖项：

```bash
$ pip install -r requirements.txt
```

<br />

> **第 3 步** - 配置环境变量：

使用 OpenAI 密钥和 Tavily API 密钥创建 .env 文件，将秘钥等相关配置写入：

```commandline
OPENAI_API_KEY=Your OpenAI API Key here
TAVILY_API_KEY=Your Tavily API Key here
```

或者直接export这些配置变量：

```bash
$ export OPENAI_API_KEY={Your OpenAI API Key here}
$ export TAVILY_API_KEY={Your Tavily API Key here}
```

- **LLM，目前仅支持 [OpenAI GPT](https://platform.openai.com/docs/guides/gpt)**。
- **对于搜索引擎，推荐使用 [Tavily Search API](https://app.tavily.com)（已针对 LLM 进行优化）**，但您也可以选择其他搜索引擎，只需将 config/config.py 中的搜索提供程序更改为 "duckduckgo"、"googleAPI"、"googleSerp "或 "searx "即可。然后在 config.py 文件中添加相应的 env API 密钥。

<br />

> **第 4 步** - 运行 main.py ：

```bash
$ python main.py
```
每次运行都会用当前时间戳生成一个 task_id，运行过程中的日志记录在 logs 目录下，最终的报告在 outputs 目录下。
<br />

## 🛡 免责声明
- 本项目是一个实验性应用程序，按 "现状 "提供，不做任何明示或暗示的保证。我们根据 MIT 许可分享用于学术目的的代码。
- **请注意，使用 GPT-4 语言模型可能会因使用token而产生高昂费用**。使用本项目即表示您承认有责任监控和管理自己的令牌使用情况及相关费用。强烈建议您定期检查 OpenAI API 的使用情况，并设置任何必要的限制或警报，以防止发生意外费用。
- 如使用本项目及其修改版本提供服务产生误导性或有害性言论，造成不良影响，由服务提供方负责，与本项目无关。

## ❤️ 致谢
- [gpt-researcher](https://github.com/assafelovic/gpt-researcher)：搜索引擎工具和大纲报告生成流程引用了gpt-researcher的相关成果。
- [MetaGPT](https://arxiv.org/abs/2308.00352)：OpenAI模型使用的费用计算逻辑和FaissStorage模块参考了MetaGPT的相关思路。
- [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)：角色选择和工具使用规划参考了AutoGPT的规划思路。
- [Generative Agents](https://arxiv.org/abs/2304.03442)：斯坦福AI小镇项目提供基于message和context的反思机制思路。

