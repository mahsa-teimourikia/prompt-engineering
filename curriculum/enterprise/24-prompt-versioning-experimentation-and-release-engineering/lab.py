"""Release promotion decision for Course 24."""
def promote(eval_passes, canary_error_rate): return eval_passes and canary_error_rate<.02
