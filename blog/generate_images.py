import os, json, base64, sys, urllib.request, concurrent.futures as cf, pathlib
SP = pathlib.Path(__file__).parent
KEY = os.environ["OPENAI_API_KEY"]
STYLE = ("Photorealistic editorial outdoor photography, natural light, shallow depth of field, "
         "Southern California offshore sportfishing setting. No text, no logos, no watermarks, no people's faces in focus. "
         "Tasteful: no gore, minimal blood.")
JOBS = {
 "bleed-hero": "On the white fiberglass deck of a Southern California sportfishing boat at golden hour, a freshly caught yellowfin tuna rests beside a large white cooler filled with ice slurry (crushed ice and seawater). An angler's gloved hands are about to lift the tuna into the slurry. On the deck in the foreground lies a tuna spike: a perfectly STRAIGHT, pointed stainless steel rod about 5 inches long (like an ice pick, no hook, no curve) set into a short cord-wrapped bamboo handle. Calm blue Pacific ocean in the background.",
 "bleed-slurry": "Close-up of a white marine cooler filled with ice slurry, crushed ice and seawater, with two clean, bright yellowtail fish fully submerged and chilled, water droplets and frost, on a boat deck in bright morning light. Clean, appetizing, fresh catch.",
 "priest-hero": "A traditional hardwood fisherman's priest (a short, heavy wooden club about 10 inches long with a lanyard hole and a worn grip) lying on a wet, weathered teak boat deck next to a freshly caught rockfish, coiled rope and a cord-wrapped bamboo gaff handle in the soft-focus background, overcast coastal light.",
 "priest-tools": "Flat lay on weathered wooden planks of three fish-handling tools arranged side by side: a traditional wooden fish priest club, a stainless steel tuna spike with a cord-wrapped bamboo handle, and the end of a cord-wrapped bamboo fishing gaff with a stainless hook. Clean composition, top-down view, soft natural light, a little seawater spray on the wood.",
}
def gen(name):
    body = json.dumps({"model": "gpt-image-2", "prompt": JOBS[name] + " " + STYLE, "size": "1536x1024",
                       "quality": "medium", "output_format": "jpeg", "output_compression": 82, "n": 1}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=body,
                                 headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        d = json.load(r)
    (SP / "img" / f"{name}.jpg").write_bytes(base64.b64decode(d["data"][0]["b64_json"]))
    return name
names = sys.argv[1:] or list(JOBS)
with cf.ThreadPoolExecutor(4) as ex:
    for f in cf.as_completed([ex.submit(gen, n) for n in names]):
        try: print("ok", f.result())
        except Exception as e: print("ERR", getattr(e, "read", lambda: b"")()[:400] or e)
