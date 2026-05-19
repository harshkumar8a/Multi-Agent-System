from langchain_core.prompts import ChatPromptTemplate

critic_prompt = ChatPromptTemplate.from_messages([

    (
        "system",
        """
        You are an expert research evaluator.

        Evaluate the report concisely and objectively.

        Keep the response under 150 words.
        """
    ),

    (
        "human",
        """
        Evaluate the following report.

        REPORT:
        {report}

        Return ONLY in this format:

        Score: <1-10>

        Strengths:
        - point 1
        - point 2

        Weaknesses:
        - point 1
        - point 2

        Verdict:
        <short final verdict>
        """
    )
])