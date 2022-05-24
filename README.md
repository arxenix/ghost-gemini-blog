# ghost-gemini-blog
serve ghost blog over gemini

attempts to convert blog html contents -> markdown -> gemini using existing python packages, works decently as long as post contents are not complex


```bash
GHOST_CONTENT_API_KEY=REDACTED GHOST_CONTENT_API_URL=REDACTED python3 server.py --ip 0.0.0.0
```
