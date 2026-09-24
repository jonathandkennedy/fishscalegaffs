"""Generate product descriptions + SEO title/description for the Fishscale Gaff Co. catalog.

Output: seo/product_copy.json  -> [{id, handle, title, descriptionHtml, seo: {title, description}}]
Facts come from the store's variants/options and the /pages/faq copy.
"""
import json
from pathlib import Path

LEAD = ("<p><strong>Made to order.</strong> Standard items ship in about 5–7 business days, and custom orders take "
        "8–12 business days because the wrap graphics are printed for your build. Need it sooner? Call "
        "<a href=\"tel:+18189188374\">(818) 918-8374</a> to ask what's ready to ship.</p>")

COLORWAYS = {
    "SHAKA STICK": ("Shaka Stick", "Teal, black and white with a laid-back, hang-loose island feel."),
    "NIHO MANO": ("Niho Mano", "Niho mano is Hawaiian for \"shark's tooth\". The earthy brown, tan and white wrap nods to the classic Polynesian pattern."),
    "VAYA CON DIOS": ("Vaya Con Dios", "\"Go with God\": a clean black, grey and white wrap, and a proper send-off for the fish at the rail."),
    "LOCAL LEGEND": ("Local Legend", "A timeless tan-and-white wrap for the angler everybody at the landing already knows."),
    "LA BRUJA DEL MAR": ("La Bruja Del Mar", "\"The Sea Witch\": aqua, green and purple that look like they were pulled straight out of a kelp bed."),
    "HIGH SEAS DRIFTER": ("High Seas Drifter", "Aqua, blue and black: deep-water colors for anglers who follow the fish offshore."),
    "FISH MACHINE": ("Fish Machine", "High-visibility orange and black that's easy to find on a busy deck."),
    "PATRIOT": ("Patriot", "Red, white and blue, for anglers who like to fly the flag on every trip."),
    "SLOB STICK": ("Slob Stick", "Neon green and purple, built for the slobs: the fish you'll be talking about for years."),
    "OFFSHORE ORIGINAL": ("Offshore Original", "The classic tan-and-black look of traditional offshore gear."),
    "MEXICUTIONER": ("Mexicutioner", "Green, white and red, made for Baja runs and trips south of the border."),
    "GANJA GAFF": ("Ganja", "Rasta green, gold, red and black for a laid-back look with a serious hook."),
    "GANJA": ("Ganja", "Rasta green, gold, red and black for a laid-back look with a serious point."),
    "PINEAPPLE CYCO": ("Pineapple Cyco", "Tropical gold, yellow and green that looks as good on the wall as it does on deck."),
    "THE WHITE": ("The White", "A clean grey-and-white wrap that pairs with any boat and any rod setup."),
    "DEATH STICK": ("Death Stick", "Blacked out from end to end: a stealthy, all-business wrap."),
    "BLODFEST": ("Blodfest", "Red, burgundy, black and white, made for the bloody-deck days you remember most."),
}

WHY_CALCUTTA = ("<li><strong>Floats:</strong> Calcutta bamboo is naturally buoyant, so a dropped tool can be recovered instead of lost.</li>"
                "<li><strong>Flexes:</strong> the cane bends like a fishing rod and soaks up head shakes instead of fighting them.</li>"
                "<li><strong>Light and grippy:</strong> the cord wrap gives a sure hold with wet, slimy hands.</li>"
                "<li><strong>Easy on your boat:</strong> no metal shaft to gouge gelcoat or rails.</li>")


GAFF_CW = {"Pineapple Cyco","Ganja","The White","Shaka Stick","Local Legend","Offshore Original","Slob Stick","Death Stick","Patriot","Mexicutioner","Fish Machine","Blodfest","La Bruja Del Mar","Niho Mano"}
SPIKE_CW = {"Shaka Stick","Niho Mano","Vaya Con Dios","Local Legend","La Bruja Del Mar","High Seas Drifter","Fish Machine","Patriot","Slob Stick","Offshore Original","Mexicutioner","Ganja"}
BRUSH_CW = {"Pineapple Cyco","Shaka Stick","Local Legend","Blodfest","Ganja","Fish Machine","Vaya Con Dios","Slob Stick","Offshore Original","Death Stick","The White"}


def matching(name, exclude):
    links = []
    if exclude != "gaff" and name in GAFF_CW:
        links.append(f'<a href="/collections/traditional-gaffs">{name} Calcutta gaff</a>')
    if exclude != "spike" and name in SPIKE_CW:
        links.append(f'<a href="/collections/fish-spikes">{name} tuna spike</a>')
    if exclude != "brush" and name in BRUSH_CW:
        links.append(f'<a href="/collections/deck-brushes">{name} deck brush</a>')
    return " and ".join(links)


def colorway(title, marker):
    head = title.split(marker)[0].strip()
    colors = title.split(marker)[-1].strip()
    name, blurb = COLORWAYS.get(head, (head.title(), ""))
    return name, colors, blurb


def gaff(p):
    name, colors, blurb = colorway(p["title"], "CALCUTTA GAFF")
    finish, ti = p["finish"], p["ti"]
    html = f"""<p>The <strong>{name} Calcutta Gaff</strong> is a handmade Calcutta bamboo fishing gaff in the {name} colorway ({colors}). {blurb} Each gaff is built one at a time and set up the way you fish: you choose the length, the action and the hook.</p>
<h3>Why a Calcutta bamboo gaff?</h3>
<ul>{WHY_CALCUTTA}</ul>
<h3>Build options</h3>
<ul>
<li><strong>Length:</strong> 3 ft, 4 ft, 5 ft or 6 ft. Choose it based on your freeboard, the height from the waterline to your deck. A 3–4 ft gaff suits kayaks, skiffs and bay boats; 5–6 ft reaches past higher gunwales on sportfishers.</li>
<li><strong>Action:</strong> Light/Medium, Medium/Heavy or Heavy. A lighter action flexes more; a heavier action gives a stiffer, more direct stick on big fish.</li>
<li><strong>Hook:</strong> Mustad 2/0–5/0 gaff hooks with a {finish} ceramic coating for extra corrosion protection, marine-grade 316 stainless steel (3" or 4" gap), or {ti} (3" or 4" gap). Titanium is the lightest option and won't corrode.</li>
</ul>
<h3>Which hook gap do I need?</h3>
<ul>
<li><strong>2.50":</strong> calico bass, barracuda, smaller dorado, halibut, sheepshead, bluefish.</li>
<li><strong>2.75":</strong> white seabass, lingcod, yellowtail, dorado, striped bass, snapper.</li>
<li><strong>3.00":</strong> tuna, yellowtail, white seabass, cobia, wahoo, grouper.</li>
<li><strong>3.25":</strong> tuna, king mackerel, amberjack, larger halibut, smaller sharks.</li>
<li><strong>4.00":</strong> big tuna, swordfish, marlin, mako, thresher, Pacific halibut.</li>
</ul>
<p>Not sure? See our <a href="/blogs/news/how-to-choose-gaff-size">gaff size guide</a> or <a href="/blogs/news/how-much-does-a-bamboo-fishing-gaff-cost">what goes into bamboo gaff pricing</a>.</p>
<h3>Care</h3>
<p>Rinse with fresh water after every trip, let it dry and store it out of direct sun. Touch up the hook point with a file as needed. More in our <a href="/blogs/news/how-to-care-for-bamboo-gaff">bamboo gaff care guide</a>.</p>
{LEAD}
<p>{('Complete the set with the matching ' + matching(name, 'gaff') + ', or design') if matching(name, 'gaff') else 'Want something different? Design'} your own with the <a href="/products/custom-gaff-builder">Custom Gaff Builder</a>.</p>"""
    seo_t = f"{name} Calcutta Bamboo Fishing Gaff – {colors}"
    seo_d = f"Handmade {name} Calcutta bamboo fishing gaff in {colors}. Floats and flexes. 3–6 ft, 3 actions, Mustad, stainless or titanium hook. From ${p['min']}."
    return html, seo_t, seo_d


def spike(p):
    name, colors, blurb = colorway(p["title"], "TUNA SPIKE")
    html = f"""<p>The <strong>{name} Tuna Spike</strong> is a handmade ike jime brain spike with a Calcutta bamboo handle in the {name} colorway ({colors}). {blurb}</p>
<p>A quick, accurate spike to the brain stops a tuna from thrashing on deck. That means less bruising, less lactic acid build-up and better-tasting fish. It's the first step of the Japanese <em>ike jime</em> method, and one of the easiest ways to improve the quality of your catch. Learn more in <a href="/blogs/news/what-is-a-tuna-spike">what is a tuna spike and when to use it</a>.</p>
<h3>Features</h3>
<ul>
<li><strong>316 stainless steel spike</strong>, marine-grade and built for saltwater.</li>
<li><strong>Calcutta bamboo handle</strong> that's light, grippy when wet and naturally buoyant.</li>
<li><strong>Optional screw-on sheath</strong> to protect the point (and you) when it's riding in a bag or on a belt.</li>
</ul>
<h3>Choose your spike size</h3>
<ul>
<li><strong>1/4" diameter × 4" length:</strong> yellowtail, bonito, dorado and school-size tuna.</li>
<li><strong>5/16" diameter × 4.5" length:</strong> the all-around size for yellowfin and bluefin.</li>
<li><strong>3/8" diameter × 5" length:</strong> larger tuna and other big, thick-skulled fish.</li>
</ul>
{LEAD}
<p>{('Pair it with the matching ' + matching(name, 'spike') + ', or build') if matching(name, 'spike') else 'Or build'} a one-off with the <a href="/products/custom-bait-net-builder-copy">Custom Tuna Spike Builder</a>.</p>"""
    seo_t = f"{name} Tuna Spike – Calcutta Bamboo Ike Jime Brain Spike"
    seo_d = f"Handmade {name} tuna spike ({colors}): 316 stainless ike jime brain spike with a Calcutta bamboo handle. 3 sizes, optional sheath. From ${p['min']}."
    return html, seo_t, seo_d


def brush(p):
    name, colors, blurb = colorway(p["title"], "CALCUTTA DECK BRUSH")
    html = f"""<p>The <strong>{name} Calcutta Deck Brush</strong> is a boat deck brush on a handmade Calcutta bamboo handle in the {name} colorway ({colors}). {blurb} It's built to match our gaffs and spikes, so your cleanup gear looks as good as your fishing gear.</p>
<h3>Built for the washdown</h3>
<p>A fish-cleaning deck brush has to deal with blood, scales, bait and dried salt every trip. The Calcutta handle is light, strong and naturally buoyant, and the cord wrap gives you a secure grip when everything is wet.</p>
<h3>Choose your length</h3>
<ul>
<li><strong>3 ft:</strong> compact for smaller boats, cockpits and storage lockers.</li>
<li><strong>4 ft:</strong> the all-around length for most center consoles and sportfishers.</li>
<li><strong>5 ft:</strong> more reach for larger decks, transoms and swim steps.</li>
</ul>
<h3>Care</h3>
<p>Rinse the brush and handle with fresh water after use and store it out of direct sun to keep the wrap and cane looking good for years. For tips on picking the right brush, read <a href="/blogs/news/best-deck-brush-for-saltwater-boats">the best deck brush for saltwater boats</a>.</p>
{LEAD}
<p>{('Match it with the ' + matching(name, 'brush') + ', or design') if matching(name, 'brush') else 'Or design'} your own with the <a href="/products/custom-brush-builder">Custom Deck Brush Builder</a>.</p>"""
    seo_t = f"{name} Boat Deck Brush – Calcutta Bamboo Handle"
    seo_d = f"{name} boat deck brush with a handmade Calcutta bamboo handle in {colors}. 3, 4 or 5 ft. Built for saltwater washdowns. From ${p['min']}."
    return html, seo_t, seo_d


def pick(p):
    colors = p["title"].split("PICK GAFF")[-1].strip()
    html = f"""<p>The <strong>Calcutta Pick Gaff</strong> in {colors} is a short, handmade Calcutta bamboo gaff for close-quarters work: sticking fish at the rail, landing fish from a kayak or skiff, and handling fish on deck.</p>
<h3>Features</h3>
<ul>
<li><strong>Two lengths:</strong> 24" for kayaks, skiffs and tight cockpits, or 32" for a little more reach from a bay boat or center console.</li>
<li><strong>Calcutta bamboo shaft</strong> that's light, strong and naturally buoyant.</li>
<li><strong>Cord wrap</strong> for a sure grip with wet hands.</li>
<li><strong>Optional butt cap</strong> (+$5) for a finished end.</li>
</ul>
<p>Short gaffs are easy to stow and quick to swing, so they make a good partner to a longer <a href="/collections/traditional-gaffs">traditional Calcutta gaff</a> on bigger boats.</p>
{LEAD}
<p>Want a different look? Design your own with the <a href="/products/custom-gaff-builder">Custom Gaff Builder</a>.</p>"""
    seo_t = f"Calcutta Bamboo Pick Gaff – {colors} | 24\" or 32\""
    seo_d = f"Handmade Calcutta bamboo pick gaff in {colors}. Short 24\" or 32\" gaff for kayaks, skiffs and close work at the rail. Floats. From ${p['min']}."
    return html, seo_t, seo_d


BUILDERS = {
    "custom-gaff-builder": (
        """<p>Design a <strong>custom Calcutta bamboo fishing gaff</strong> that's yours from end to end. Match your boat, your rods, your crew shirts or your tournament team. Every custom gaff is handmade to order from Calcutta bamboo.</p>
<h3>What you can customize</h3>
<ul>
<li><strong>Wrap colors and graphics</strong> for a one-of-one look.</li>
<li><strong>Length:</strong> from short kayak and skiff gaffs up to long sportfishing gaffs.</li>
<li><strong>Action:</strong> lighter and more flexible, or stiff and direct.</li>
<li><strong>Hook:</strong> ceramic-coated Mustad, marine-grade 316 stainless steel, or titanium, in the gap size for your target species.</li>
</ul>
<h3>Why Calcutta bamboo?</h3>
<ul>""" + WHY_CALCUTTA + """</ul>
<p>Custom gaffs also make a great gift for a captain, a crew or a fishing buddy. Wondering about cost? Read <a href="/blogs/news/how-much-does-a-bamboo-fishing-gaff-cost">how much a bamboo fishing gaff costs</a>, or browse <a href="/blogs/news/custom-gaff-build-examples">custom gaff build examples</a> for ideas.</p>""" + LEAD +
        """<p>Very particular about your build? Call us and we'll get it exactly right.</p>""",
        "Custom Fishing Gaff Builder – Handmade Calcutta Bamboo Gaff",
        "Design your own custom Calcutta bamboo fishing gaff: choose wrap colors, length, action and hook. Handmade to order. Floats and flexes. From $149.99."),
    "custom-brush-builder": (
        """<p>Build a <strong>custom boat deck brush</strong> on a handmade Calcutta bamboo handle, wrapped in the colors you choose. It's the finishing touch for a boat already rigged with matching gaffs and rods.</p>
<ul>
<li><strong>Your colors:</strong> match your boat, your gaff or your team.</li>
<li><strong>Calcutta bamboo handle</strong> that's light, strong and naturally buoyant.</li>
<li><strong>Cord wrap grip</strong> that holds when everything is wet.</li>
</ul>
<p>Built for washing blood, scales and bait off the deck after a long day. Tips on choosing one: <a href="/blogs/news/choosing-marine-deck-brush-for-boats">choosing a marine deck brush for your boat</a>.</p>""" + LEAD,
        "Custom Boat Deck Brush Builder – Calcutta Bamboo Handle",
        "Design a custom boat deck brush on a handmade Calcutta bamboo handle. Pick your wrap colors to match your boat and gaff. Handmade to order. From $149.99."),
    "custom-bait-net-builder": (
        """<p>Build a <strong>custom bait net</strong> with a handmade Calcutta bamboo handle, wrapped in your colors. It's made for scooping anchovies, sardines, mackerel and other live bait out of the tank quickly and gently, so your bait stays lively.</p>
<ul>
<li><strong>Your colors:</strong> match your gaff, deck brush and boat.</li>
<li><strong>Calcutta bamboo handle</strong> that's light, strong and naturally buoyant.</li>
<li><strong>Cord wrap grip</strong> for control with wet hands.</li>
</ul>
<p>New to bait nets? Read <a href="/blogs/news/how-to-use-a-bait-net">how to use a bait net</a> and <a href="/blogs/news/best-bait-net-for-boat-use">the best bait net for boat use</a>.</p>""" + LEAD,
        "Custom Bait Net Builder – Calcutta Bamboo Bait Net",
        "Design a custom bait net with a handmade Calcutta bamboo handle in your colors. Scoop live bait fast and gently. Handmade to order. From $119.99."),
    "custom-bait-net-builder-copy": (
        """<p>Build a <strong>custom tuna spike</strong>: a handmade ike jime brain spike with a Calcutta bamboo handle, wrapped in the colors you choose.</p>
<p>A quick spike to the brain stops a fish from thrashing, which means less bruising, less lactic acid and better-tasting fish. It's the first step of the Japanese <em>ike jime</em> method. More in <a href="/blogs/news/what-is-a-tuna-spike">what is a tuna spike</a>.</p>
<ul>
<li><strong>316 stainless steel spike</strong>, marine-grade.</li>
<li><strong>Calcutta bamboo handle</strong> that's light, grippy and naturally buoyant.</li>
<li><strong>Your colors</strong> to match your gaff and deck brush.</li>
</ul>""" + LEAD,
        "Custom Tuna Spike Builder – Ike Jime Brain Spike",
        "Design a custom tuna spike: 316 stainless ike jime brain spike on a Calcutta bamboo handle in your colors. Handmade to order. From $94.99."),
}


def tee(p):
    name = p["title"].replace(" TEE", "").title()
    html = f"""<p>The <strong>{name} Tee</strong> from Fishscale Gaff Co. puts one of our signature Calcutta gaff colorways on a shirt for the landing, the boat or the bar. Available in sizes S–3XL.</p>
<p>Match it to your {matching(name, 'tee').replace(' and ', ', ', 1) if matching(name, 'tee').count(' and ') > 1 else matching(name, 'tee')}.</p>"""
    return html, f"{name} T-Shirt – Fishscale Gaff Co.", f"Fishscale Gaff Co. {name} tee. Our signature Calcutta gaff colorway on a shirt, sizes S–3XL. $19.99."


PRODUCTS = json.loads(Path(__file__).with_name("products.json").read_text())

out = []
for p in PRODUCTS:
    t = p["title"]
    if p["handle"] in BUILDERS:
        html, st, sd = BUILDERS[p["handle"]]
    elif "TUNA SPIKE" in t:
        html, st, sd = spike(p)
    elif "DECK BRUSH" in t:
        html, st, sd = brush(p)
    elif "PICK GAFF" in t:
        html, st, sd = pick(p)
    elif "CALCUTTA GAFF" in t:
        html, st, sd = gaff(p)
    elif t.endswith(" TEE"):
        html, st, sd = tee(p)
    else:
        continue
    out.append({"id": p["id"], "handle": p["handle"], "title": t,
                "descriptionHtml": "\n".join(l.strip() for l in html.strip().splitlines()),
                "seo": {"title": st, "description": sd}})

def fix_the(o):
    h = o["descriptionHtml"].replace("<p>The <strong>The White", "<p><strong>The White").replace("in the The White colorway", "in The White colorway")
    h = h.replace("the matching <a href=\"/collections/deck-brushes\">The White deck brush", "the matching <a href=\"/collections/deck-brushes\">The White deck brush")
    h = h.replace("with the <a href=\"/collections/traditional-gaffs\">The White", "with <a href=\"/collections/traditional-gaffs\">The White")
    h = h.replace("the matching <a href=\"/collections/traditional-gaffs\">The White", "<a href=\"/collections/traditional-gaffs\">The White")
    h = h.replace("the matching <a href=\"/collections/deck-brushes\">The White", "<a href=\"/collections/deck-brushes\">The White")
    h = h.replace("Match it to your <a href=\"/collections/traditional-gaffs\">The White", "Match it to <a href=\"/collections/traditional-gaffs\">The White")
    if "deck-brush" in o["handle"]:
        h = h.replace("for a laid-back look with a serious point.", "for a laid-back look on a hard-working tool.")
    o["descriptionHtml"] = h
    o["seo"]["description"] = o["seo"]["description"].replace("Handmade The White Calcutta bamboo fishing gaff in Grey/White.", "Handmade Calcutta bamboo fishing gaff in The White colorway (Grey/White).")
    return o


out = [fix_the(o) for o in out]
Path(__file__).with_name("product_copy.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(len(out), "products")
for o in out:
    print(len(o["seo"]["title"]), len(o["seo"]["description"]), o["seo"]["title"])
