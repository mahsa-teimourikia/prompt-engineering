```python
from pathlib import Path
from northstar.runtime import get_client, PromptRequest, Message
client = get_client(Path("fixtures/replays.json"))  # NORTHSTAR_MODE=replay|live|record
```

Replay mode uses recorded fixtures and does not call a live model. Set
`NORTHSTAR_MODE=live` to call Gemini explicitly when `GEMINI_API_KEY` is
available, or use `NORTHSTAR_MODE=record` to save live responses for a
replay fixture.
