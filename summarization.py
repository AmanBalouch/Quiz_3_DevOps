"""
Simple extractive summarization - no heavy dependencies
"""

def summarize_text(text, num_sentences=3):
    """
    Summarize text by extracting important sentences
    """
    if not text or len(text.strip()) < 50:
        return text
    
    # Split into sentences
    sentences = text.replace('!', '.').replace('?', '.').split('.')
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
    
    if len(sentences) <= num_sentences:
        return text
    
    # Score sentences by word frequency
    words = text.lower().split()
    word_freq = {}
    
    for word in words:
        if len(word) > 3 and word not in ['the', 'that', 'this', 'with', 'from', 'have']:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Score each sentence
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        score = 0
        for word in sentence.lower().split():
            if word in word_freq:
                score += word_freq[word]
        sentence_scores[i] = score
    
    # Get top sentences
    top_indices = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
    top_indices = sorted([idx for idx, _ in top_indices])
    
    summary = '. '.join([sentences[i] for i in top_indices]) + '.'
    
    return summary
