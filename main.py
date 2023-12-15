from insight_researcher import Agent


def main():
    # Query
    query = "大语言模型技术进展报告"

    # Report Type
    # report_type = "outline_report"

    # Run Research
    agent = Agent(query=query)
    report = agent.run()
    print(report)


if __name__ == "__main__":
    main()
