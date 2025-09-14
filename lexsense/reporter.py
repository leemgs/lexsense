"""LLM Reporter – GPT-4 (optional) or HuggingFace summarizer; simple fallback otherwise."""
import os
try:
    import openai
except ImportError:
    openai = None
try:
    from transformers import pipeline
except ImportError:
    pipeline = None

class Reporter:
    def __init__(self) -> None:
        self.testing = os.getenv("TESTING") == "1"
        self.use_openai = False
        key = os.getenv("OPENAI_API_KEY")
        if key and openai is not None:
            openai.api_key = key
            self.use_openai = True
            self.summarizer = None
        else:
            self.summarizer = None
            if not self.testing and pipeline is not None:
                try:
                    self.summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-6-6")
                except Exception as e:
                    print(f"[Reporter] HF summarizer init failed: {e}")
                    self.summarizer = None

    def summarize(self, text: str, max_length: int = 130) -> str:
        if self.testing or (not self.use_openai and self.summarizer is None):
            parts = text.split('.')
            if len(parts) > 1:
                out = '.'.join(parts[:2]).strip()
                if not out.endswith('.'):
                    out += '.'
                return out
            return (text[:200] + ("..." if len(text) > 200 else "")).strip()
        if self.use_openai and openai is not None:
            try:
                resp = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": f"Summarize concisely:\n\"\"\"\n{text}\n\"\"\""}]
                )
                return resp['choices'][0]['message']['content'].strip()
            except Exception as e:
                print(f"[Reporter] OpenAI call failed: {e}")
                if self.summarizer:
                    try:
                        s = self.summarizer(text, max_length=max_length, truncation=True)
                        return s[0]['summary_text'].strip()
                    except Exception as e2:
                        print(f"[Reporter] HF summarization failed: {e2}")
                        return text[:200] + ("..." if len(text) > 200 else "")
                return text[:200] + ("..." if len(text) > 200 else "")
        if self.summarizer:
            try:
                s = self.summarizer(text, max_length=max_length, truncation=True)
                return s[0]['summary_text'].strip()
            except Exception as e:
                print(f"[Reporter] HF summarization failed: {e}")
                return text[:200] + ("..." if len(text) > 200 else "")
        return ""
