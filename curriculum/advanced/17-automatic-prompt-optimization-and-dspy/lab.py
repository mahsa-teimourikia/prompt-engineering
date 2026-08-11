"""Offline optimizer-overfitting demonstration for Course 17."""
def score(prompt, split):
    scores={("manual","dev"):.70,("optimized","dev"):.92,("manual","heldout"):.72,("optimized","heldout"):.65}
    return scores[prompt,split]
