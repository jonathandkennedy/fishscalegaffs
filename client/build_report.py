"""Builds the client-facing SEO report PDF for Fishscale Gaff Co."""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, NextPageTemplate, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("Sans", FONT_DIR + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", FONT_DIR + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-Bold", italic="Sans", boldItalic="Sans-Bold")

NAVY = colors.HexColor("#0E2A3B")
TEAL = colors.HexColor("#127C7C")
TEAL_LIGHT = colors.HexColor("#E3F2F1")
SAND = colors.HexColor("#F6F1E7")
GREEN = colors.HexColor("#2E7D32")
GREEN_LIGHT = colors.HexColor("#E8F5E9")
ORANGE = colors.HexColor("#C75B12")
ORANGE_LIGHT = colors.HexColor("#FDF0E6")
GREY = colors.HexColor("#5B6770")
RULE = colors.HexColor("#D5DBDF")

OUT = Path(__file__).with_name("Fishscale-Gaff-Co-Website-Growth-Plan.pdf")
W, H = letter
MARGIN = 0.75 * inch

base = dict(fontName="Sans", fontSize=10.5, leading=15, textColor=NAVY)
S = {
    "body": ParagraphStyle("body", **base, spaceAfter=6),
    "small": ParagraphStyle("small", **{**base, "fontSize": 9, "leading": 12.5, "textColor": GREY}),
    "h1": ParagraphStyle("h1", **{**base, "fontName": "Sans-Bold", "fontSize": 22, "leading": 27, "textColor": NAVY}, spaceAfter=4),
    "kicker": ParagraphStyle("kicker", **{**base, "fontName": "Sans-Bold", "fontSize": 9, "textColor": TEAL}, spaceAfter=2),
    "h2": ParagraphStyle("h2", **{**base, "fontName": "Sans-Bold", "fontSize": 14, "leading": 18}, spaceBefore=8, spaceAfter=6),
    "h3": ParagraphStyle("h3", **{**base, "fontName": "Sans-Bold", "fontSize": 12, "leading": 16}),
    "step": ParagraphStyle("step", **base),
    "stepnum": ParagraphStyle("stepnum", **{**base, "fontName": "Sans-Bold", "textColor": colors.white, "alignment": TA_CENTER}),
    "cell": ParagraphStyle("cell", **{**base, "fontSize": 9.5, "leading": 13}),
    "cellb": ParagraphStyle("cellb", **{**base, "fontSize": 9.5, "leading": 13, "fontName": "Sans-Bold"}),
    "cellh": ParagraphStyle("cellh", **{**base, "fontSize": 9, "leading": 12, "fontName": "Sans-Bold", "textColor": colors.white}),
    "callout": ParagraphStyle("callout", **{**base, "fontSize": 10.5, "leading": 15}),
}


def P(text, style="body"):
    return Paragraph(text, S[style])


def box(flowables, bg, border=None, pad=12):
    t = Table([[flowables]], colWidths=[W - 2 * MARGIN])
    st = [("BACKGROUND", (0, 0), (-1, -1), bg),
          ("LEFTPADDING", (0, 0), (-1, -1), pad), ("RIGHTPADDING", (0, 0), (-1, -1), pad),
          ("TOPPADDING", (0, 0), (-1, -1), pad - 2), ("BOTTOMPADDING", (0, 0), (-1, -1), pad)]
    if border:
        st.append(("LINEBEFORE", (0, 0), (0, -1), 4, border))
    t.setStyle(TableStyle(st))
    return t


def simple(text, label="In plain English", color=TEAL, bg=TEAL_LIGHT):
    return box([P(f'<font color="{color.hexval()}"><b>{label}</b></font>', "kicker"), P(text, "callout")], bg, color)


def steps(items):
    rows = []
    for i, s in enumerate(items, 1):
        rows.append([P(str(i), "stepnum"), P(s, "step")])
    t = Table(rows, colWidths=[0.32 * inch, W - 2 * MARGIN - 0.45 * inch])
    st = [("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (1, 0), (1, -1), 0),
          ("LEFTPADDING", (1, 0), (1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]
    for r in range(len(rows)):
        st.append(("BACKGROUND", (0, r), (0, r), TEAL))
        st.append(("TOPPADDING", (0, r), (0, r), 2))
        st.append(("BOTTOMPADDING", (0, r), (0, r), 2))
    t.setStyle(TableStyle(st))
    return t


def table(header, rows, widths, zebra=True):
    data = [[P(h, "cellh") for h in header]] + [[P(c, "cellb" if j == 0 else "cell") for j, c in enumerate(r)] for r in rows]
    t = Table(data, colWidths=widths, repeatRows=1)
    st = [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LINEBELOW", (0, 1), (-1, -1), 0.5, RULE),
          ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
          ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]
    if zebra:
        for r in range(2, len(data), 2):
            st.append(("BACKGROUND", (0, r), (-1, r), SAND))
    t.setStyle(TableStyle(st))
    return t


def task(num, title, time, who, why, how, note=None):
    head = Table([[P(f'<font color="{ORANGE.hexval()}">TO-DO #{num}</font>', "kicker"),
                   P(f'<font color="{GREY.hexval()}">Time: <b>{time}</b> &nbsp;·&nbsp; Who: <b>{who}</b></font>', "small")]],
                 colWidths=[1.3 * inch, W - 2 * MARGIN - 1.3 * inch])
    head.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                              ("ALIGN", (1, 0), (1, 0), "RIGHT"), ("VALIGN", (0, 0), (-1, -1), "BOTTOM")]))
    parts = [head, P(title, "h2"), simple(why, "Why this matters", ORANGE, ORANGE_LIGHT), Spacer(1, 8),
             P("<b>How to do it:</b>"), steps(how)]
    if note:
        parts += [Spacer(1, 4), P(note, "small")]
    return [KeepTogether(parts), Spacer(1, 18)]


def done(title, what):
    t = Table([[P('<font color="#2E7D32" size="14"><b>✓</b></font>', "body"),
                [P(f"<b>{title}</b>"), P(what, "cell")]]],
              colWidths=[0.35 * inch, W - 2 * MARGIN - 0.35 * inch])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("BACKGROUND", (0, 0), (-1, -1), GREEN_LIGHT),
                           ("LEFTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 6), ("LINEBEFORE", (0, 0), (0, -1), 4, GREEN)]))
    return [t, Spacer(1, 4)]


# ---------- page decorations ----------
def cover(c, doc):
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, H * 0.42, W, H * 0.58, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(0, H * 0.42 - 8, W, 8, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Sans-Bold", 11)
    c.drawString(MARGIN, H - 1.2 * inch, "FISHSCALE GAFF CO.  ·  FISHSCALEGAFFS.COM")
    c.setFont("Sans-Bold", 34)
    c.drawString(MARGIN, H - 2.4 * inch, "Your Website")
    c.drawString(MARGIN, H - 2.95 * inch, "Growth Plan")
    c.setFont("Sans", 14)
    c.setFillColor(colors.HexColor("#BFE3E1"))
    c.drawString(MARGIN, H - 3.55 * inch, "What we fixed, what's next, and exactly how to do it,")
    c.drawString(MARGIN, H - 3.85 * inch, "step by step, in plain English.")
    c.setFillColor(colors.white)
    c.setFont("Sans", 10)
    c.drawString(MARGIN, H * 0.42 + 0.45 * inch, "Prepared September 24, 2026")
    c.restoreState()


def later(c, doc):
    c.saveState()
    c.setStrokeColor(RULE)
    c.line(MARGIN, 0.6 * inch, W - MARGIN, 0.6 * inch)
    c.setFont("Sans", 8)
    c.setFillColor(GREY)
    c.drawString(MARGIN, 0.42 * inch, "Fishscale Gaff Co. · Website Growth Plan")
    c.drawRightString(W - MARGIN, 0.42 * inch, f"Page {doc.page}")
    c.restoreState()


doc = BaseDocTemplate(str(OUT), pagesize=letter, leftMargin=MARGIN, rightMargin=MARGIN,
                      topMargin=MARGIN, bottomMargin=0.85 * inch,
                      title="Fishscale Gaff Co. – Website Growth Plan", author="Fishscale Gaff Co. SEO",
                      subject="SEO work completed and next steps")
frame_cover = Frame(MARGIN, 0.9 * inch, W - 2 * MARGIN, H * 0.42 - 1.3 * inch, id="cover")
frame_body = Frame(MARGIN, 0.85 * inch, W - 2 * MARGIN, H - MARGIN - 0.85 * inch, id="body")
doc.addPageTemplates([PageTemplate("cover", [frame_cover], onPage=cover),
                      PageTemplate("body", [frame_body], onPage=later)])

story = []

# ---------- cover summary ----------
story += [NextPageTemplate("body"),
          P("THE SHORT VERSION", "kicker"),
          P("Your gear is great, but Google didn't know how to talk about it. Almost every page on your site was "
            "empty: no words, no descriptions, nothing for Google to read. We filled in <b>54 product pages and "
            "6 collection pages</b>, fixed a pricing mistake that was letting people buy a $175 gaff for $18, and "
            "wrote a new buying guide. Now there are <b>12 simple jobs left</b>, and this guide shows you exactly how "
            "to do each one.", "callout"),
          PageBreak()]

# ---------- how google works ----------
story += [P("START HERE", "kicker"), P("How Google works (the 1-minute version)", "h1"), Spacer(1, 6),
          P("Imagine Google is a <b>giant librarian</b>. When someone types <i>\"bamboo fishing gaff\"</i>, the librarian "
            "runs around the internet looking for the page that best answers the question, then hands over the best "
            "10 books. Everyone reads the first few. Almost nobody looks at page 3."),
          P("The librarian can't see pictures and can't hold your gaff. <b>It can only read words.</b> So it picks pages that:"),
          steps(["<b>Use the same words people search for</b> (\"Calcutta bamboo gaff\", \"tuna spike\", \"boat deck brush\").",
                 "<b>Explain things clearly</b>: what it is, what it's made of, who it's for, how much it costs.",
                 "<b>Other websites talk about</b>. A link from another fishing site is like a friend saying \"this store is good\". "
                 "More good friends = more trust."]),
          Spacer(1, 10),
          simple("Before our work, your pages were like books with <b>blank pages inside</b>. Beautiful covers (your photos), "
                 "but the librarian had nothing to read, so it couldn't recommend you, even though your gear is better than "
                 "most of what it does recommend."),
          Spacer(1, 16),
          P("Where you were when we started", "h2"),
          table(["What we measured", "Your number", "What it means"],
                [["Google searches you show up for", "21", "All of them on page 3 to page 9 of Google, where almost nobody looks."],
                 ["Visitors from Google per month", "About 7", "Basically zero. Most of your visitors typed your web address in directly."],
                 ["Times you appeared in Google (3 months)", "13", "Google barely showed you to anyone."],
                 ["Products with a description", "0 of 54", "Every product page was blank."],
                 ["Real fishing websites linking to you", "~0", "The 62 sites linking to you are junk directories that don't help."]],
                [2.1 * inch, 1.0 * inch, W - 2 * MARGIN - 3.1 * inch]),
          PageBreak()]

# ---------- what we did ----------
story += [P("ALREADY DONE", "kicker"), P("What we already fixed for you", "h1"),
          P("You don't need to do anything for these. They're live on your website right now."), Spacer(1, 6)]
story += done("Fixed a pricing mistake that was costing you money",
              "On 11 of your Calcutta gaffs, one size (4 ft, Heavy, Mustad 3/0 hook) was priced at <b>$17.99 instead of $174.99</b>. "
              "Anyone could have bought a $175 gaff for $18, and your shop pages were showing \"From $17.99\". All 11 are fixed.")
story += done("Wrote descriptions for all 54 products",
              "Every gaff, tuna spike, deck brush, pick gaff, custom builder and tee now explains what it is, why Calcutta bamboo is "
              "better (it floats, flexes and grips when wet), the length, action and hook choices, which hook gap to pick for which "
              "fish, how to care for it, and how long shipping takes. Each colorway also got its own line (Niho Mano = \"shark's tooth\", "
              "La Bruja Del Mar = \"the Sea Witch\"), so every page is unique.")
story += done("Gave every product a Google title and Google description",
              "This is the blue headline and the two lines of grey text people see in Google search results. Before, it just said "
              "\"DEATH STICK CALCUTTA GAFF Black/Black\". Now it says <i>\"Death Stick Calcutta Bamboo Fishing Gaff – Black/Black\"</i> "
              "with a short sales pitch underneath, using the words people actually search for.")
story += done("Wrote text and FAQs for all 6 collection pages",
              "Traditional Gaffs, Fish Spikes, Deck Brushes, Pick Gaffs, Bait Nets and Build Your Own each got a Google title, a Google "
              "description, a short buying guide and common questions answered. <b>Note:</b> this text is saved but won't show on "
              "the page until you finish To-Do #1.")
story += done("Linked your pages together",
              "Products now link to the matching gaff, spike or brush in the same colorway, to the custom builders, and to your "
              "helpful blog posts. That's like putting signs in a store that say \"this goes great with that\", for shoppers and for Google.")
story += done("Wrote a new blog post: \"How Much Does a Bamboo Fishing Gaff Cost?\"",
              "A full price guide comparing DIY, budget, handmade and custom gaffs, with your real prices by length. It's saved "
              "as a <b>hidden draft</b> so you can read it first (see To-Do #2).")
story += done("Did the keyword research and set up tracking",
              "We checked about 150 search phrases to find the ones buyers really type into Google (see the next page), studied "
              "the competitors who show up above you (Morita Gaffs, Geronimo Tackle, Seaworx, LT Marine, AFTCO), ran a full "
              "check of all 154 pages on your site, and saved everything in a tracking project so we can measure progress.")
story += [PageBreak()]

# ---------- keywords ----------
story += [P("WHAT PEOPLE SEARCH FOR", "kicker"), P("The words we're trying to win", "h1"),
          P("These are real searches people type into Google in the US every month. We picked the ones where the person is "
            "<b>ready to buy</b> and where small handmade shops (like you) can realistically get to the top."), Spacer(1, 6),
          table(["Group", "Example searches (searches per month)", "Page that should show up"],
                [["Bamboo / Calcutta gaffs", "bamboo gaff (210), calcutta bamboo gaff (50), calcutta gaff (50), wooden gaff (30)", "Traditional Gaffs"],
                 ["Custom gaffs", "custom gaff (140), custom gaffs (140), custom fishing gaff (50)", "Custom Gaff Builder"],
                 ["Buying a gaff", "fishing gaff / fish gaff / gaff hook (2,900), fishing gaff for sale (140), tuna gaff (90)", "Traditional Gaffs + Google Shopping"],
                 ["Tuna spikes", "ike jime spike (480), ikejime tool (390), fish spike (390), tuna spike (320), brain spike (110)", "Fish Spikes"],
                 ["Boat brushes", "boat brush (720), boat deck brush (260), boat cleaning brush (260), boat scrub brush (140)", "Deck Brushes"],
                 ["Bait nets", "bait net (880), livewell net (320), bait dip net (110)", "Bait Nets"],
                 ["Gifts (Nov–Dec)", "gifts for fishermen (5,400), fishing gifts for men (1,900), boat gifts (1,600)", "New gift guide (To-Do #11)"],
                 ["Learning", "ike jime (3,600), what is a gaff (1,600), how to bleed a tuna (90)", "Blog posts"]],
                [1.35 * inch, 3.35 * inch, W - 2 * MARGIN - 4.7 * inch]),
          Spacer(1, 12),
          simple("The big searches like \"fishing gaff\" are owned by giant brands and Amazon, and they're hard to beat in normal "
                 "results. But the <b>bamboo, Calcutta and custom</b> searches are only fought over by small shops like Morita "
                 "and Geronimo. That's the fight you can win first, and those shoppers want exactly what you make."),
          Spacer(1, 10),
          box([P('<font color="#C75B12"><b>A word of warning about keyword lists</b></font>', "kicker"),
               P("Some tools spit out lists like \"bamboo fishing gaff cost per hour\" or \"does Medicare cover a bamboo fishing gaff\" "
                 "with big made-up numbers. We checked them, and nobody actually searches for those. Writing pages for fake "
                 "searches wastes your time and can make Google trust your site less. Every number in this guide comes from real "
                 "Google data.", "callout")], ORANGE_LIGHT, ORANGE),
          PageBreak()]

# ---------- to-do overview ----------
story += [P("YOUR TO-DO LIST", "kicker"), P("What's left, in order", "h1"),
          P("Do them top to bottom. The first ones are quick and matter most. <b>Tip:</b> any of the \"You or us\" jobs we can do "
            "for you. Just say the word."), Spacer(1, 6),
          table(["#", "Job", "Time", "Who"],
                [["1", "Fix the \"Deck brushes\" heading and show your collection text", "5 min", "You (theme editor)"],
                 ["2", "Read and publish the new price-guide blog post", "10 min", "You"],
                 ["3", "Give your homepage a Google title and description", "5 min", "You or us"],
                 ["4", "Point your menu at the right pages and remove the copies", "20 min", "You or us"],
                 ["5", "Clean up the web addresses that end in \"-copy\"", "10 min", "You or us"],
                 ["6", "Send an old broken link to the right page", "2 min", "You or us"],
                 ["7", "Describe your photos for Google (alt text)", "30–60 min", "You or us"],
                 ["8", "Get your products into Google Shopping for free", "30 min", "You"],
                 ["9", "Add a reviews app and ask customers for reviews", "20 min + ongoing", "You"],
                 ["10", "Get real fishing websites to link to you", "Ongoing", "You + us"],
                 ["11", "Make a Christmas gift guide before November", "1 hour", "Us (you approve)"],
                 ["12", "Keep adding helpful blog posts", "Ongoing", "Us (you approve)"]],
                [0.45 * inch, 3.75 * inch, 1.05 * inch, W - 2 * MARGIN - 5.25 * inch]),
          PageBreak()]

# ---------- tasks ----------
story += task(1, "Fix the \"Deck brushes\" heading and show your collection text", "5 minutes", "You",
              "Right now <b>every</b> collection page (Gaffs, Fish Spikes, Pick Gaffs, Bait Nets…) has the big heading "
              "<b>\"Deck brushes\"</b>. That's like putting a \"Shoes\" sign over the fishing aisle. It confuses shoppers "
              "and Google. And the new text we wrote for your collections can't show until this is fixed.",
              ["Log in to Shopify. On the left, click <b>Online Store</b>, then <b>Themes</b>.",
               "Next to your theme (\"Savor\"), click the <b>Customize</b> button.",
               "At the very top of the screen there's a menu that says <b>Home page</b>. Click it and choose "
               "<b>Collections</b>, then <b>Default collection</b>.",
               "On the left side, click the section called <b>Collection heading</b>, then click the <b>Title</b> text block under it.",
               "On the right you'll see a text box with <b>Deck brushes</b> in it. Delete those words.",
               "Click the small <b>stacked-circles icon</b> (it's called \"Insert dynamic source\") and pick "
               "<b>Collection</b> then <b>Title</b>. Keep the text style set to <b>Heading 1</b>.",
               "Still in the Collection heading section, click <b>Add block</b> and pick <b>Text</b>.",
               "Click the same stacked-circles icon on the new text block and pick <b>Collection</b> then <b>Description</b>.",
               "Click <b>Save</b> in the top right. Open your Fish Spikes page. The heading should now say \"Fish Spikes\" "
               "with the new text under it."],
              "If the description text looks too long at the top of the page, you can drag that text block below the products instead.")
story += task(2, "Read and publish the new price-guide blog post", "10 minutes", "You",
              "We wrote a full guide called <b>\"How Much Does a Bamboo Fishing Gaff Cost?\"</b>. People who search for prices are "
              "close to buying. It's hidden right now so you can check it first. It's your business and your name on it.",
              ["In Shopify, click <b>Content</b> (or <b>Online Store</b>), then <b>Blog posts</b>.",
               "Open <b>\"How Much Does a Bamboo Fishing Gaff Cost? (2026 Price Guide)\"</b>.",
               "Read it. Pay extra attention to the competitor price ranges ($50–$650). Change anything that doesn't sound like you.",
               "On the right, under <b>Visibility</b>, choose <b>Visible</b>.",
               "Click <b>Save</b>. Your post is now live."])
story += task(3, "Give your homepage a Google title and description", "5 minutes", "You or us",
              "Your homepage's Google headline is just \"Fishscale Gaff Co.\". Nobody searches that unless they already know you. "
              "It's like a store sign that only says your last name. Let's say what you <b>sell</b>.",
              ["In Shopify, click <b>Online Store</b>, then <b>Preferences</b>.",
               "In <b>Homepage title</b>, type: <i>Handmade Calcutta Bamboo Fishing Gaffs, Tuna Spikes &amp; Deck Brushes | Fishscale Gaff Co.</i>",
               "In <b>Homepage meta description</b>, type: <i>Handmade Calcutta bamboo fishing gaffs, ike jime tuna spikes, deck brushes and "
               "bait nets. Handmade to order, with custom colors available.</i>",
               "Click <b>Save</b>."],
              "Bonus: your homepage only has about 190 words. Adding a short paragraph about who you are and why Calcutta bamboo "
              "(the story from your About page is perfect) helps a lot.")
story += task(4, "Point your menu at the right pages and remove the copies", "20 minutes", "You or us",
              "You have <b>two pages for everything</b>: for example /pages/calcutta-gaffs and /collections/traditional-gaffs "
              "show the same gaffs. Google sees twins and doesn't know which one to show, so it often shows neither. "
              "The collection pages are the good ones now (they have all the new text), so the menu should point there.",
              ["In Shopify, click <b>Content</b> (or <b>Online Store</b>), then <b>Menus</b>, then <b>Main menu</b>.",
               "Click each menu item and change where it links to: <b>Traditional Gaffs</b> → Collections → Traditional Gaffs, "
               "<b>Fish Spikes</b> → Fish Spikes, <b>Deck Brushes</b> → Deck Brushes, <b>Pick Gaffs</b> → Pick Gaffs, "
               "<b>Bait Nets</b> → Bait Nets, <b>Build Your Own</b> → Build Your Own. Click <b>Save menu</b>.",
               "Now go to <b>Online Store</b>, then <b>Pages</b>. Open each copy page (Calcutta Gaffs, Calcutta Tuna Spikes, "
               "Boat Deck Brush, Pick Gaffs, Bait Nets, Build Your Own) and set it to <b>Hidden</b>, or delete it.",
               "Type <b>URL redirects</b> into the Shopify search bar at the top and open it. Click <b>Create URL redirect</b> "
               "for each old page, e.g. from <b>/pages/calcutta-gaffs</b> to <b>/collections/traditional-gaffs</b>. "
               "(Full list in the box below.)"],
              "Redirect list: /pages/calcutta-gaffs → /collections/traditional-gaffs · /pages/calcutta-tuna-spikes → /collections/fish-spikes · "
              "/pages/boat-deck-brush → /collections/deck-brushes · /pages/pick-gaffs → /collections/pick-gaffs · "
              "/pages/bait-nets → /collections/bait-nets · /pages/build-your-own → /collections/build-your-own")
story += task(5, "Clean up the web addresses that end in \"-copy\"", "10 minutes", "You or us",
              "When you duplicate a product, Shopify adds \"-copy\" to its web address. One of them is really confusing: your "
              "<b>Shaka Stick</b> gaff lives at an address that says <b>\"the-white…-copy\"</b>. Clean addresses help Google "
              "understand what's on the page.",
              ["In Shopify, click <b>Products</b> and open the product (list below).",
               "Scroll to the bottom to <b>Search engine listing</b> and click the pencil / <b>Edit</b>.",
               "Change the <b>URL handle</b> to the new one in the list below.",
               "Make sure the box <b>\"Create a URL redirect\"</b> is ticked. This keeps old links working.",
               "Click <b>Save</b>. Repeat for each product."],
              "Shaka Stick Calcutta Gaff → shaka-stick-calcutta-gaff-teal-black-white · Calcutta Pick Gaff Neon Green/Purple → "
              "calcutta-pick-gaff-neon-green-purple · High Seas Drifter Tuna Spike → high-seas-drifter-tuna-spike-aqua-blue-black · "
              "Slob Stick Tuna Spike → slob-stick-tuna-spike-neon-green-purple · Custom Tuna Spike Builder → custom-tuna-spike-builder")
story += task(6, "Send an old broken link to the right page", "2 minutes", "You or us",
              "Google still remembers an old address for your Ganja gaff, and it now leads to a \"page not found\" error. "
              "That's a dead end for anyone who clicks it. A redirect is like leaving a forwarding address at the post office.",
              ["Type <b>URL redirects</b> into the Shopify search bar and open it. Click <b>Create URL redirect</b>.",
               "Redirect from: <b>/products/ganja-gaff-x-rasta-colors-with-corrosion-resistant-pale-gold-finished-hook</b>",
               "Redirect to: <b>/products/ganja-gaff-calcutta-gaff-green-gold-red-black</b>",
               "Click <b>Save redirect</b>."])
story += task(7, "Describe your photos for Google (alt text)", "30–60 minutes", "You or us",
              "Remember, the librarian can't see pictures. <b>Alt text</b> is a short sentence that tells Google (and people who "
              "use screen readers) what's in a photo. Right now none of your product photos have one, so Google Images can't show "
              "your gear either.",
              ["In Shopify, click <b>Products</b> and open a product.",
               "Click on a photo. A window opens. Click <b>Add alt text</b> (or <b>Edit alt text</b>).",
               "Describe the photo like you'd describe it to a friend on the phone, e.g. <i>\"Death Stick Calcutta bamboo fishing "
               "gaff with black cord wrap and titanium hook\"</i>.",
               "Click <b>Save</b>. Do the first 3 photos of every product. They matter most."],
              "This one is repetitive, so we're happy to do all of it for you in one go.")
story += task(8, "Get your products into Google Shopping for free", "30 minutes", "You",
              "When people search \"fishing gaff\", \"boat deck brush\" or \"bait net\", the <b>top of Google is a row of product "
              "pictures with prices</b> (\"Popular products\"). You're not in it. Getting in is free, and it's the fastest way to show "
              "up for the big searches that are hard to win otherwise.",
              ["In Shopify, click <b>Settings</b>, then <b>Policies</b>. Make sure your <b>Refund policy</b> and <b>Shipping policy</b> "
               "are filled in. Google requires them.",
               "Click <b>Settings</b>, then <b>Shipping and delivery</b>, and check your shipping rates are set up.",
               "Go to the <b>Shopify App Store</b>, search for <b>Google &amp; YouTube</b> (made by Google) and install it.",
               "Follow its setup: sign in with your Google account, create or connect a <b>Google Merchant Center</b> account, "
               "and turn on <b>free listings</b>.",
               "Wait a few days for Google to approve your products. The app will tell you if anything needs fixing."])
story += task(9, "Add a reviews app and ask customers for reviews", "20 minutes, then ongoing", "You",
              "Reviews are like friends vouching for you. Google can show <b>gold stars</b> next to your products in search "
              "results, and people click stars. Google has already flagged that your products have no reviews.",
              ["Go to the <b>Shopify App Store</b> and install a reviews app (<b>Judge.me</b> has a free plan).",
               "Follow its setup so reviews show on your product pages.",
               "Turn on the automatic <b>review request email</b> so every customer gets asked a week or two after delivery.",
               "Personally message your past customers and ask for a review and a photo of the gaff "
               "with their catch. Those photos are gold."])
story += task(10, "Get real fishing websites to link to you", "Ongoing", "You + us",
              "Links from other websites are Google's biggest trust signal. Your closest competitor, Morita Gaffs, ranks in the "
              "top 5, and a big reason is that <b>tournaments, charter boats and fishing magazines</b> link to them. The links you have now come "
              "from junk directories that don't count. You already know these people. You just need to ask.",
              ["<b>Sponsor a local tournament</b> (yellowtail, tuna or kayak events). Donate a custom gaff as a prize and ask for "
               "your logo and a link on their sponsors page.",
               "<b>Gift a custom gaff to a few charter captains or landings</b> in SoCal. Ask them to list you as \"gear we use\" on their website.",
               "<b>Pitch BD Outdoors (Bloodydecks)</b>. They did an \"Artist Spotlight\" on Morita Gaffs. Email them your story "
               "and build photos.",
               "<b>Join fishing forums as a vendor</b> (BD Outdoors, The Hull Truth) and share build photos.",
               "<b>Make short videos</b> for YouTube and Instagram: how a gaff is built, how to spike a tuna. Link back to the product page."])
story += task(11, "Make a Christmas gift guide before November", "About 1 hour (we write it, you approve)", "Us (you approve)",
              "In November and December, thousands of people search <b>\"gifts for fishermen\"</b> (5,400 a month) and "
              "<b>\"fishing gifts for men\"</b> (1,900). A custom gaff in someone's boat colors is a perfect gift, but only if "
              "you show up. The page needs to be live by early November so Google has time to find it.",
              ["Tell us your holiday plans: any gift bundles (gaff + spike + brush in one colorway), discounts or order-by dates for Christmas.",
               "We write a \"Gifts for Fishermen\" page and blog post and send it to you.",
               "You read it and give the thumbs up. We publish it and link it from your homepage."])
story += task(12, "Keep adding helpful blog posts", "Ongoing (1–2 posts a month)", "Us (you approve)",
              "Every good post is another \"book\" on the librarian's shelf with your name on it. People who learn from you are more "
              "likely to buy from you. You already have 21 posts, which is a great start.",
              ["Next up: a complete <b>Ike Jime guide</b> (3,600 searches a month, easy to rank for) and an update to your "
               "<b>\"What is a gaff\"</b> post (1,600 a month).",
               "Send us your own photos and stories from trips. Real experience is what makes a post rank and sell.",
               "We write, you approve, it goes live. Every post links to the matching products."])

# ---------- expectations ----------
story += [PageBreak(), P("WHAT TO EXPECT", "kicker"), P("When will I see results?", "h1"),
          P("SEO is like planting a fruit tree, not flipping a light switch. Google needs time to re-read your pages and "
            "decide to trust them. Here's a realistic timeline:"), Spacer(1, 6),
          table(["When", "What usually happens"],
                [["Weeks 1–4", "Google re-reads your pages and picks up the new titles and descriptions. Free Shopping listings go live (To-Do #8)."],
                 ["Months 1–3", "You start moving up from page 3–5 of Google toward page 1–2 for bamboo, Calcutta, custom gaff and tuna spike searches. First clicks from Google Shopping."],
                 ["Months 3–6", "With reviews and real links coming in, the easier searches can reach the top 5. More of your sales start coming from Google instead of only word of mouth and Instagram."],
                 ["Months 6–12", "Your blog posts and gift guide bring a steady stream of new visitors every month, without paying for ads."]],
                [1.2 * inch, W - 2 * MARGIN - 1.2 * inch]),
          Spacer(1, 12),
          simple("We're tracking all of this for you: where you rank, how many people find you on Google, and which pages "
                 "bring sales. We'll check in with real numbers so you can see the tree growing.", "How we'll keep score"),
          PageBreak(),
          P("CHEAT SHEET", "kicker"), P("Words you might hear", "h1"), Spacer(1, 6),
          table(["Word", "What it means"],
                [["SEO", "Search Engine Optimization: making your website easy for Google to understand and recommend."],
                 ["Keyword", "The words someone types into Google, like \"tuna spike\"."],
                 ["Meta description", "The short grey text under your link in Google results. Your 2-line sales pitch."],
                 ["SEO title", "The big blue clickable headline in Google results."],
                 ["Alt text", "A sentence describing a photo, so Google knows what's in it."],
                 ["Redirect", "A forwarding address: sends anyone visiting an old web address to the new one."],
                 ["Backlink", "A link to your site from another website. Like a friend recommending you."],
                 ["Collection", "A group of products in Shopify, like \"Traditional Gaffs\"."],
                 ["H1 / heading", "The biggest title on a web page. Google reads it to learn what the page is about."]],
                [1.4 * inch, W - 2 * MARGIN - 1.4 * inch]),
          Spacer(1, 16),
          box([P("<b>Stuck on any step?</b> Don't worry. Anything marked \"You or us\" we can do for you. Just send a message "
                 "with the number of the to-do (for example \"Do #5 and #7\") and we'll handle it.", "callout")], TEAL_LIGHT, TEAL)]

doc.build(story)
print(OUT)
