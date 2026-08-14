#!/usr/bin/env python3
"""Regenerate the portfolio plates block in portfolio.html from PHOTOS below.

Edit PHOTOS, run this, and the gallery markup is rebuilt. Beats
hand-editing twenty near-identical HTML blocks and getting one wrong.
"""
from pathlib import Path
from PIL import Image

# name, category, caption, marker, alt
PHOTOS = [
 ("eng-01","engagements","A Front Range overlook","Newly engaged",
  "An engaged couple sitting on a rock outcrop above the foothills, she in a red gown looking up at him."),
 ("eng-02","engagements","The ring","Just said yes",
  "A close-up of a woman's hand showing her engagement ring while she and her fiance kiss behind it."),
 ("mat-01","maternity","Golden hour in the field","Expecting",
  "An expectant couple sitting together on a blanket in a dry winter field, both hands resting on her bump."),
 ("mat-02","maternity","Winter maternity, first snow","Expecting",
  "An expectant mother in a green dress standing in a snowy field, holding her bump and smiling."),
 ("mat-03","maternity","The first scan","Announcement",
  "A close-up of an expectant couple's hands holding an ultrasound photo against her bump."),
 ("mat-04","maternity","Telling everyone","Announcement",
  "A couple in a field of autumn trees holding up an ultrasound photo toward the camera."),
 ("nb-01","newborn","Asleep in the basket","Newborn",
  "A swaddled newborn sleeping in a woven basket lined with white fur."),
 ("nb-02","newborn","Ten toes","Newborn",
  "A black and white photograph of a newborn's feet cupped in a parent's hands."),
 ("nb-03","newborn","The bear bonnet","Newborn",
  "A newborn in a knitted bear bonnet lying beside a small crocheted teddy."),
 ("nb-04","newborn","Mom and the twins","Twins",
  "An overhead photograph of a mother lying down with a swaddled newborn asleep on either side of her head."),
 ("fam-01","family","Under the aspens","Autumn",
  "A family of four standing together in a meadow beneath a golden aspen, mountains behind them."),
 ("fam-02","family","Everyone in motion","Spring",
  "Parents embracing on a dirt path while three children run and hold hands around them."),
 ("fam-03","family","The whole family","Extended family",
  "A large extended family gathered on a rock overlook with Pikes Peak in the distance, grandparents kissing at the centre."),
 ("fam-04","family","Forehead to forehead","Mother and daughter",
  "A mother kneeling on a path holding her toddler daughter, foreheads touching, foothills behind them."),
 ("fam-05","family","All three at once","Mother and daughters",
  "A mother laughing in a wicker chair in a meadow while her three daughters climb around her."),
 ("fam-06","family","Big sister","Announcing number two",
  "A toddler in a pink sweater reading Big Sis, holding both parents' hands and looking at the camera."),
 ("ms-01","milestones","Cake smash","First birthday",
  "A one-year-old in a lilac tulle dress reaching toward a cupcake beneath hanging flowers."),
 ("ms-02","milestones","Three of them, holding still","Holiday minis",
  "Three children lying on a bed in front of a Merry Christmas garland, chins in their hands."),
 ("ms-03","milestones","The whole crew","Holiday minis",
  "A family of four sitting on a leather sofa beside a decorated Christmas tree."),
 ("ms-04","milestones","Just the two of them","Holiday minis",
  "A couple sitting together in front of a lit Christmas tree in a bright studio."),
]

# Works whether the pages sit at the repo root or inside site/.
repo = Path(__file__).resolve().parent.parent
root = repo / "site" if (repo / "site").is_dir() else repo
out = []
for name, cat, caption, marker, alt in PHOTOS:
    with Image.open(root / "images" / f"{name}.jpg") as im:
        w, h = im.size
    out.append(f"""        <figure class="plate rise" data-category="{cat}">
          <picture>
            <source type="image/webp"
              srcset="images/{name}-800.webp 800w, images/{name}.webp {w}w"
              sizes="(min-width: 48rem) 45vw, 100vw">
            <img src="images/{name}.jpg"
              srcset="images/{name}-800.jpg 800w, images/{name}.jpg {w}w"
              sizes="(min-width: 48rem) 45vw, 100vw"
              width="{w}" height="{h}" loading="lazy" decoding="async"
              alt="{alt}">
          </picture>
          <figcaption><span>{caption}</span><span class="marker">{marker}</span></figcaption>
        </figure>""")

page = (root / "portfolio.html").read_text()
start = page.index('      <div class="plates">')
end = page.index("      </div>", start) + len("      </div>")
page = page[:start] + '      <div class="plates">\n\n' + "\n\n".join(out) + "\n\n      </div>" + page[end:]
(root / "portfolio.html").write_text(page)
print(f"wrote {len(PHOTOS)} plates")
