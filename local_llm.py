import os, sys
from llama_cpp import Llama
import time
from tts import speak

def run_local_llm(
        prompt: str,
        model_path: str = "qwen.gguf",
        max_tokens: int = 200,
        temperature: float = 0.7,
        n_ctx: int = 2048,
        n_threads: int = 4
) -> str:
    
    try:
        print("Local LLM got your query")

        system_prompt = (
            "You are a concise assistant. "
            "Answer in 1-2 short sentences only. "
            "Do not repeat the question, "
            "do not explain extra details, "
            "and do not add examples."
            "If the question is not complete, then respond accordingly."
        )

        final_prompt = f"{system_prompt}\nUser: {prompt}\nAssistant:"

        os.environ["GGML_METAL_LOG_LEVEL"] = "1"
        sys.stderr = open(os.devnull, "w")

        llm = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_threads=n_threads,
            verbose=False
        )

        response = llm(
            final_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        text = response["choices"][0]["text"].strip()

        for w in ["User:", "Assistant:", "Answer:", "Question:"]:
            text = text.replace(w, "")

        sentences = text.split(".")
        text = ".".join(sentences[:2]).strip()

        if not text.endswith("."):
            text += "."


        txt = text.split()
        len_txt = len(txt)-1
        speak(text,len_txt)
        return text

    except Exception as e:
        err = f"Local LLM Error: {e}"
        print(err)
        speak(err)
        return err