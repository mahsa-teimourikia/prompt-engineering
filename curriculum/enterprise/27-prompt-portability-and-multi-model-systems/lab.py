"""Offline model-migration regression check for Course 27."""
def migrate(old,new): return {"old":old,"new":new,"schema_valid":old["schema"]==new["schema"],"regression":old["quality"]>new["quality"]}
