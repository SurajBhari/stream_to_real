# Stream To Real

A small Flask web tool that converts between **stream time** and **real (wall-clock) time** for YouTube livestreams — in both directions.

- **Stream → Real:** given a stream URL with a timestamp (e.g. `?t=1280s`), find the actual date/time that moment happened.
- **Real → Stream:** given a wall-clock time, find the offset into the stream where it occurred.

You can paste **multiple links at once** (one per line) and convert them in a single batch. It works out the stream's start time using [`chat_downloader`](https://github.com/xenova/chat-downloader), then offsets from there.

## Run locally

```bash
pip install -r requirements.txt
python main.py
```

Then open the local site. Use the **right** panel for Stream → Real and the **left** panel for Real → Stream.

## Test case

Paste these into the right-side (Stream → Real) box:

```text
https://youtu.be/live/aRHcStRteQE
https://youtu.be/live/T7zPNkKL0pQ
https://youtu.be/live/s46VJxqiHCk
```

All three resolve to just after **21:20**. Reversing the operation (left side) with `2024-01-26 21:20:00` returns the corresponding stream offsets.
