import os
from dotenv import load_dotenv
from google import genai
from vector_store import retrieve_chunks
from prompt import create_prompt

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(
    api_key=GEMINI_API_KEY
)

def generate_answer(
    description,
    chunks,
    top_k=3
):

    retrieved_results = retrieve_chunks(
        chunks,
        description,
        top_k=top_k
    )

    if not retrieved_results:

        return (
            "No relevant resume sections were found.",
            []
        )
    context=""
    for result in retrieved_results:
        context += f"""
        Source:{result['source']}, Page: {result['page']}
        {result['chunk']}
        """
 

    prompt = create_prompt(
        context,
        description
    )

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    answer = response.text

    return answer, retrieved_results

