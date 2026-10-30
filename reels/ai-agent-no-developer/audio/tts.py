"""Generate voiceover segments + word timings with edge-tts."""
import certifi
certifi.where = lambda: "/root/.ccr/ca-bundle.crt"
import asyncio, json, os, edge_tts

VOICE = "en-US-AndrewMultilingualNeural"
SEGMENTS = [
    ("hook",  0.15, "Your first AI agent doesn't need a developer."),
    ("pain",  3.15, "Copying emails into spreadsheets. Answering the same questions. Building the same report, every single week. That's hours gone on work a machine could do."),
    ("step1", 12.2, "Step one. Pick one repetitive task. Just one, like sorting new leads."),
    ("step2", 18.2, "Step two. Define your inputs and outputs. What comes in, and what should come out?"),
    ("step3", 24.2, "Step three. Build and test it in n-eight-n. Trigger, AI, action. Done."),
    ("cta",   30.1, "Comment AGENT for the course list."),
]

async def gen(name, text):
    c = edge_tts.Communicate(text, VOICE, rate="+8%", boundary="WordBoundary",
                             proxy=os.environ.get("HTTPS_PROXY"))
    words = []
    with open(f"audio/{name}.mp3", "wb") as f:
        async for ch in c.stream():
            if ch["type"] == "audio":
                f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                words.append({"w": ch["text"], "s": ch["offset"] / 1e7, "e": (ch["offset"] + ch["duration"]) / 1e7})
    return words

async def main():
    out = []
    for name, start, text in SEGMENTS:
        print(name, flush=True)
        out.append({"name": name, "start": start, "text": text, "words": await gen(name, text)})
    json.dump(out, open("audio/vo.json", "w"), indent=1)

asyncio.run(main())
