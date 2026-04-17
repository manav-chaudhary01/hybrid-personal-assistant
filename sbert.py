# sbert.py

import os
from sentence_transformers import SentenceTransformer, util



class SBERTIntentDetector:
    """
    SBERT-based intent detector.
    Loads the model once and precomputes embeddings for all intents.
    """

    def __init__(self, model_path = "sentence-transformers/all-MiniLM-L6-v2"):
        print("Loading SBERT model...")
        self.model = SentenceTransformer(model_path)

        self.stopwords = ["is", "a", "the", "an", "and", "or", "in", "of", "to", "for", "on", "with"]

        self.intents = {
            "date_query": [
                "what is the date", "date today", "tell me today's date", "what date is it"
            ],
            "time_query": [
                "what the time", "tell me the time", "current time", "what's the time now"
            ],
            "temperature_query": [
                "tell the temperature", "current temperature", "how's the weather",
                "what the temperature outside"
            ],
            "web_search": [
                "search", "search on browser", "search this", "search on google",
                "google this", "look up this topic", "search for information"
            ],
            "casual_conversation": [
                "hello", "hi", "how are you", "what's up", "how's your day",
                "good morning", "good evening"
            ],
            "information_query": [
                "what", "how", "why happening", "explain this concept", "what does this mean"
            ],
            "file_search_open": [
                "file", "find file", "search file", "locate the file", "document"
            ],
            "app_open": [
                "open", "app", "start app", "launch notepad", "open application"
            ],
            "exit_program": [
                "exit", "sleep", "terminate", "close", "bye"
            ]
        }

        self.intent_embeddings = {
            intent: self.model.encode(examples, convert_to_tensor=True)
            for intent, examples in self.intents.items()
        }

    def remove_stopwords(self, text):
        """
        Remove stopwords from a query.
        """
        words = text.lower().split()
        filtered = [w for w in words if w not in self.stopwords]
        return " ".join(filtered)

    def detect_intent(self, query):
        """
        Detect intent of a given query using SBERT embeddings.
        Returns the intent string or "no_intent" if confidence is low.
        """
        if len(query.split()) == 1 and len(query) <= 3:
            return "no_intent"

        clean_query = self.remove_stopwords(query)
        query_emb = self.model.encode(clean_query, convert_to_tensor=True)

        best_intent = None
        best_score = -1

        for intent, emb_list in self.intent_embeddings.items():
            score = util.cos_sim(query_emb, emb_list).max().item()
            if score > best_score:
                best_score = score
                best_intent = intent

        if best_score < 0.23:
            return "no_intent"

        return best_intent