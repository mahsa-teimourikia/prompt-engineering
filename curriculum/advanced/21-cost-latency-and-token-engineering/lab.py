"""Simple Pareto comparison for Course 21."""
OPTIONS=({"name":"full","quality":.92,"cost":.04,"latency":900},{"name":"pruned","quality":.90,"cost":.02,"latency":500},{"name":"cheap","quality":.70,"cost":.005,"latency":200})
def acceptable(x): return x["quality"]>=.85
