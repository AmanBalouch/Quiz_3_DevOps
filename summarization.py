"""
Summarization module for extracting key information from articles
Uses a simple extractive summarization approach
"""

def summarize_text(text, num_sentences=3):
    """
    Summarize text by extracting the most important sentences
    
    Args:
        text (str): The text to summarize
        num_sentences (int): Number of sentences to include in summary
    
    Returns:
        str: Summarized text
    """
    
    if not text or len(text.strip()) < 50:
        return text
    
    try:
        # Try to use transformers for better summarization
        from transformers import pipeline
        
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        
        # Limit text length for the model (max 1024 tokens)
        text_limited = text[:1000]
        
        if len(text_limited.split()) < 50:
            return text
        
        summary = summarizer(text_limited, max_length=150, min_length=50, do_sample=False)
        return summary[0]['summary_text']
        
    except Exception as e:
        print(f"Transformer summarization failed: {e}, using fallback method")
        return extractive_summarize(text, num_sentences)

def extractive_summarize(text, num_sentences=3):
    """
    Fallback summarization using sentence extraction
    
    Args:
        text (str): The text to summarize
        num_sentences (int): Number of sentences to include
    
    Returns:
        str: Summarized text
    """
    
    # Split into sentences
    sentences = text.split('.')
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) <= num_sentences:
        return text
    
    # Score sentences based on word frequency
    words = text.lower().split()
    word_freq = {}
    
    for word in words:
        if len(word) > 3:  # Only consider words longer than 3 characters
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Score sentences
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        for word in sentence.lower().split():
            if word in word_freq:
                sentence_scores[i] = sentence_scores.get(i, 0) + word_freq[word]
    
    # Get top sentences
    top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
    top_sentences = sorted(top_sentences, key=lambda x: x[0])  # Sort by original order
    
    summary = '. '.join([sentences[idx] for idx, _ in top_sentences]) + '.'
    
    return summary
