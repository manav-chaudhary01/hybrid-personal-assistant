import os
from sentence_transformers import SentenceTransformer, util



class SBERTIntentDetector:
    """
    SBERT-based intent detector.
    Loads the model once and precomputes embeddings for all intents.
    """

    def __init__(self, model_path = "models/all-MiniLM-L6-v2"):
        print("Loading SBERT model...")
        self.model = SentenceTransformer(model_path, local_files_only=True)

        self.stopwords = ["is", "a", "the", "an", "and", "or", "in", "of", "to", "for", "on", "with"]

        self.intents = {

            "date_query": [
                "what is today's date",
                "tell me the date",
                "what date is it",
                "current date",
                "today's date please",
                "which day is today",
                "what day is it today"
            ],

            "time_query": [
                "what is the current time",
                "tell me the time",
                "what time is it",
                "current time now",
                "can you tell me the time",
                "time right now"
            ],

            "temperature_query": [
                "what is the temperature",
                "tell me the weather",
                "how is the weather outside",
                "current temperature",
                "what's the weather like",
                "temperature outside now"
            ],

            "web_search": [
                "search this on google",
                "search for this",
                "look this up online",
                "google this",
                "find this on the internet",
                "search the web for this",
                "open browser and search"
            ],

            "casual_conversation": [
                "hello",
                "hi",
                "hey",
                "how are you",
                "what's up",
                "how is your day",
                "good morning",
                "good evening",
                "good afternoon",
                "nice to meet you"
            ],

            "information_query": [
                "what is this",
                "what does this mean",
                "explain this",
                "explain this concept",
                "tell me about this",
                "give me information about this",
                "how does this work",
                "why does this happen",
                "explain something",
                "tell me something about a topic",
                "help me understand this",
                "what is machine learning",
                "what is artificial intelligence",
                "explain any topic",
                "what are data structures",
                "explain data structures",
                "what is programming",
                "tell me about algorithms",
                "how does computer work",
                "what is a database",
                "explain networking",
                "what is cloud computing"
            ],

            "file_search_open": [
                "find a file",
                "search for a file",
                "open a file",
                "locate a document",
                "find my document",
                "search my files",
                "open document",
                "look for a file", 
                "look for a file",
                "look up a file",
                "find something",
                "search my computer",
                "find this file",
                "open this file",
                "look for document",
                "search for document",
            ],

            "app_open": [
                "open an app",
                "open chrome",
                "launch spotify",
                "start application",
                "open vscode",
                "open calculator",
                "run an app",
                "launch a program"
            ],

            "exit_program": [
                "exit",
                "quit",
                "close the program",
                "terminate program",
                "shutdown assistant",
                "stop the assistant",
                "bye",
                "goodbye"
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
        if len(query.strip()) == 0:
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

        print(f"Intent: {best_intent} | Score: {best_score:.3f}")

        if best_intent in ["app_open", "exit_program"]:
            threshold = 0.35

        elif best_intent in ["web_search", "temperature_query", "time_query", "date_query"]:
            threshold = 0.30

        else:  # information_query, casual_conversation, file_search_open
            threshold = 0.22


        if best_score < threshold:
            return "no_intent"


        
        return best_intent