from google import genai
from dotenv import load_dotenv
import os
import time

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_answer(question, context, answer_type):

    if answer_type == "2 Marks":

        prompt = f"""
Answer in 2 marks format.

Context:
{context}

Question:
{question}

Rules:
- Definition
- 2 points only
- Maximum 80 words
"""

    elif answer_type == "5 Marks":

        prompt = f"""
Answer in 5 marks format.

Context:
{context}

Question:
{question}

Rules:
- Definition
- Explanation
- Important Points
- Around 200 words
"""

    elif answer_type == "10 Marks":

        prompt = f"""
Answer in 10 marks format.

Context:
{context}

Question:
{question}

Rules:
- Definition
- Detailed Explanation
- Advantages
- Disadvantages
- Conclusion
"""

    else:

        prompt = f"""
You are an experienced SPPU examiner.

Study Material:
{context}

Generate TOP 15 most important exam questions.

Rules:
- Only questions
- No answers
- Group by Unit
- Use proper numbering
"""

    models = [
        "gemini-2.0-flash",
        "gemini-2.5-flash-lite"
    ]

    for model_name in models:

        for attempt in range(3):

            try:

                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )

                return response.text

            except Exception:

                if attempt < 2:
                    time.sleep(3)
                    continue

                break

    return """
All AI models are currently busy.

Please try again later.
"""