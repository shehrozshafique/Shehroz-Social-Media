"""Turn vo.json word timings into caption chunks (max 4 words, split on punctuation) -> captions.js"""
import json, re
segs = json.load(open("audio/vo.json"))
chunks = []
for s in segs:
    toks = s["text"].split()
    assert len(toks) == len(s["words"]), (s["name"], len(toks), len(s["words"]))
    cur = []
    for tok, w in zip(toks, s["words"]):
        txt = tok.replace("n-eight-n", "n8n").rstrip(".,")
        cur.append({"w": txt, "s": round(s["start"] + w["s"], 3), "e": round(s["start"] + w["e"], 3)})
        if len(cur) == 4 or re.search(r"[.,?!]$", tok):
            chunks.append(cur); cur = []
    if cur: chunks.append(cur)
for i, c in enumerate(chunks):  # each chunk stays up until the next one starts (max +0.6s)
    nxt = chunks[i + 1][0]["s"] if i + 1 < len(chunks) else 33
    c[-1]["hold"] = round(min(nxt, c[-1]["e"] + 0.6), 3)
open("captions.js", "w").write("const CAPTIONS=" + json.dumps(chunks) + ";\n")
print(len(chunks), "chunks")
