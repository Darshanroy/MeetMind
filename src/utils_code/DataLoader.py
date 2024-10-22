from langchain_community.document_loaders import YoutubeLoader



def get_word_count_and_docs_from_youtube_url(yt_link):
    """Calculates the word count from a YouTube video link and returns the documents.

    Args:
        yt_link (str): The URL of the YouTube video.

    Returns:
        tuple: A tuple containing the number of words and the documents.
    """

    try:
        loader = YoutubeLoader.from_youtube_url(yt_link)
        docs = loader.load()
        word_count = len(docs[0].page_content.split())
        return word_count, docs
    except Exception as e:
        print(f"Error loading YouTube video: {e}")
        return 0, None
    
    
# word_count, docs = get_word_count_from_youtube_url(Credentials.yt_link)
# print(f"Number of words: {word_count}")