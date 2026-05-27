import nimpy
import std/math
import std/strutils
proc scoreSource(
    wordCount: int,
    snippetLen: int,
    titleLen: int
): float {.exportpy.} = 
 let wordScore = 
  if wordCount == 0: 0.0
  elif wordCount < 100: 0.2
  elif wordCount < 300: 0.5
  elif wordCount <= 1000: 1.0
  else: 0.8 # too long = might be noise heavy
 let snippetScore = min(float(snippetLen) / 200.0, 1.0)
 let titleScore =
  if titleLen < 10: 0.3
  elif titleLen < 60: 1.0
  else: 0.6
 result = (wordScore * 0.6) + (snippetScore * 0.3) + (titleScore * 0.1)
proc rankSources(
    wordCounts: seq[int],
    snippetLens: seq[int],
    titleLens: seq[int]
): seq[float] {.exportpy.} =
 result = @[]
 for i in 0 ..< wordCounts.len:
    let score = scoreSource(wordCounts[i], snippetLens[i], titleLens[i])
    result.add(score)