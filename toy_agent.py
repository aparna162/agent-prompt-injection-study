
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  

api_key = os.environ.get("GROQ_API_KEY")


client = Groq(api_key=api_key)
MODEL_NAME = "openai/gpt-oss-20b"  


def summarize_document(document_text):
    
    prompt = f"""You are a helpful assistant that summarizes web content.

Summarize the following document in one sentence:

{document_text}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    
    test_doc = """
    Scientists at a European research institute have developed a new method
    for detecting weak cryptographic keys in TLS certificates. The technique
    analyzes key generation patterns and can flag suspicious certificates
    automatically. Researchers say this could help prevent incidents similar
    to recent certificate authority compromises.
    """

    print("Testing with a normal document...")
    result = summarize_document(test_doc)
    print(f"\nAgent's summary:\n{result}")