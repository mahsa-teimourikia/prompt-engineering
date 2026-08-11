"""Offline judge-agreement and order-bias checks for Course 15."""
def agreement(human, judge): return sum(a==b for a,b in zip(human,judge))/len(human)
def pairwise(first, second): return {"first_wins":first>second,"second_wins":second>first}
HUMAN=(1,0,1,0); JUDGE=(1,1,1,0)
