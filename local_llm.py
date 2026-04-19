import os, sys
from llama_cpp import Llama
import time
from tts import speak

print("Loading Local LLM...")

llm = Llama(
    model_path="models/qwen.gguf",
    n_ctx=1024,
    n_threads=8,
    verbose=False
)

print("Local LLM Loaded!")

def run_local_llm(
        prompt: str,
        max_tokens: int = 80,
        temperature: float = 0.6
) -> str:

    try:
        print("Local LLM processing...")

        system_prompt = (
            "You are a concise assistant. "
            "Answer in 1-2 short sentences only. "
            "No extra explanation."
        )

        final_prompt = f"{system_prompt}\nUser: {prompt}\nAssistant:"

        response = llm(
            final_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        text = response["choices"][0]["text"].strip()

        # cleanup
        for w in ["User:", "Assistant:", "Answer:", "Question:"]:
            text = text.replace(w, "")

        text = text.split(".")
        text = ".".join(text[:2]).strip()

        if not text.endswith("."):
            text += "."

        speak(text, len(text.split()) - 1)

        return text

    except Exception as e:
        err = f"Local LLM Error: {e}"
        print(err)
        speak(err)
        return err