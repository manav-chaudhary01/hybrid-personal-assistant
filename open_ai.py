import os
from dotenv import load_dotenv
from groq import Groq
from local_llm import run_local_llm
from tts import speak

load_dotenv()

def ask_groq(prompt: str, model: str = "llama-3.3-70b-versatile") -> str:
    original_prompt = prompt
    prompt = prompt + ". Explain in 1 - 2 lines."

    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )

        answer = response.choices[0].message.content

        txt = answer.split()
        speak(answer, len(txt) - 1)

        return answer

    except Exception as e:
        print("Groq API error:", e)
        return run_local_llm(original_prompt)
    