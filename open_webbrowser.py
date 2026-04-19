import webbrowser

def clean_query(query):
    remove_words = [
        "search",
        "search on browser",
        "search this",
        "search on google",
        "google this",
        "look up this topic",
        "search on",
        "search for information"
    ]
    
    query_lower = query.lower()
    for word in remove_words:
        query_lower = query_lower.replace(word, "")

    return query_lower.strip()

def search_web(query):
    query = clean_query(query)
    url = "https://www.google.com/search?q=" + query.replace(" ", "+")
    webbrowser.open(url)
