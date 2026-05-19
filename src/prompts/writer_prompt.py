from langchain_core.prompts import ChatPromptTemplate

writer_prompt = ChatPromptTemplate.from_messages([

    (
        "system",
        """
        You are an expert research writer.
        Write clear, detailed, factual reports.
        """
    ),

    (
        "human",
        """
        Topic:
        {topic}

        Research:
        {research}

        Structure:
        - Introduction
        - Key Findings
        - Conclusion
        - Sources
        """
    )
])