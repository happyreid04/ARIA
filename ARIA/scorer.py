"""Python implementation of the scorer module (replaces scorer.pyd)"""
import math

def scoreSource(wordCount: int, snippetLen: int, titleLen: int) -> float:
    """Score a single source based on content metrics."""
    # Word count scoring
    if wordCount == 0:
        wordScore = 0.0
    elif wordCount < 100:
        wordScore = 0.2
    elif wordCount < 300:
        wordScore = 0.5
    elif wordCount <= 1000:
        wordScore = 1.0
    else:
        wordScore = 0.8  # too long = might be noise heavy
    
    # Snippet length scoring (normalized to max 1.0)
    snippetScore = min(float(snippetLen) / 200.0, 1.0)
    
    # Title length scoring
    if titleLen < 10:
        titleScore = 0.3
    elif titleLen < 60:
        titleScore = 1.0
    else:
        titleScore = 0.6
    
    # Weighted combination
    result = (wordScore * 0.6) + (snippetScore * 0.3) + (titleScore * 0.1)
    return result

def rankSources(wordCounts: list, snippetLens: list, titleLens: list) -> list:
    """Rank multiple sources and return their scores."""
    result = []
    for i in range(len(wordCounts)):
        score = scoreSource(wordCounts[i], snippetLens[i], titleLens[i])
        result.append(score)
    return result
