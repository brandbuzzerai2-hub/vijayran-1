#!/usr/bin/env python3
"""
Static site generator for The Vijayran Palace (Sujan Design DNA).
Modelled directly on thesujanlife.com:
- Minion Pro editorial serif display + Brandon Grotesque sans body
- Minimalist luxury layouts: Alabaster #F6F3EF, Deep Espresso #3E362F, Sujan Gold #D1A555
- Lenis smooth scroll + GSAP ScrollTrigger + Line-masked text reveals
- Sticky story section with parallax drifting gallery
- Continuous moving image ribbon above the dark footer
- Live weather widget & Instagram feed widget
- Verbatim content & media from royalquestresorts.com
"""

import os, html, json

OUT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://www.royalquestresorts.com/"
LIVE = "https://www.royalquestresorts.com/wp-content/uploads/"
BOOK = "https://www.swiftbook.io/inst/#home?propertyId=622MTqtrrTvISYL6ULEQBTI2zhv8o6h6TcrQI2OTA=&JDRN=Y"
PHONE_ROOMS, PHONE_EVENTS = "+91 99998 22609", "+91 9999163809"
TEL_ROOMS, TEL_EVENTS = "+919999822609", "+919999163809"
EMAIL, EMAIL_SALES = "resv@royalquestresorts.com", "sales@royalquestresorts.com"
ADDRESS = "NH-8, Kukas, Village Kacherawala, Jaipur, Rajasthan 302028, India"
ADDRESS_OLD = "NH-8, Kukas, Village Kacherawala, Jaipur, Rajasthan, India, 302028."
IG_URL = "https://www.instagram.com/vijayranresorts/"

e = html.escape

class P:
    R = ""

def u(slug=""):
    return P.R + (slug + "/" if slug else "")

def img(path, alt="", cls="", eager=False):
    lz = "" if eager else ' loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{P.R}media/wp-content/uploads/{path}" data-live="{LIVE}{path}" '
            f'onerror="if(this.dataset.live){{this.src=this.dataset.live;this.removeAttribute(\'data-live\')}}" '
            f'alt="{e(alt)}"{lz} decoding="async">')

SKETCH = """<svg class="sketch_svg" viewBox="0 0 380 300" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
<path d="M70 92 Q190 18 310 92"/><path d="M82 92 Q190 32 298 92"/><path d="M190 22v-12M186 12h8M190 4v-2"/>
<path d="M62 92h256v10H62z"/><path d="M70 102h240"/>
<path d="M150 52 Q190 30 230 52" opacity=".6"/><circle cx="190" cy="34" r="3"/>
<path d="M78 102v118M302 102v118M96 102v118M284 102v118"/>
<path d="M96 220 V150 Q96 118 128 112 Q150 108 160 118 Q190 96 220 118 Q230 108 252 112 Q284 118 284 150 V220"/>
<path d="M112 220 V154 Q112 128 136 124 Q154 122 162 132 Q190 112 218 132 Q226 122 244 124 Q268 128 268 154 V220" opacity=".7"/>
<path d="M190 124 V220" opacity=".35"/><path d="M112 172h156" opacity=".35"/>
<path d="M60 220h260v14H60z"/><path d="M66 234 l8 14 h232 l8 -14"/>
<path d="M74 248 v22 M306 248 v22 M120 248 q10 22 20 0 M160 248 q10 22 20 0 M200 248 q10 22 20 0 M240 248 q10 22 20 0"/>
<path d="M40 270 h300" opacity=".5"/><path d="M20 282 q40 -10 80 0 t80 0 t80 0 t80 0" opacity=".35"/>
<path d="M330 214 q16 -40 2 -76 q-4 30 -14 44 q14 -6 22 -20" opacity=".5"/><path d="M332 214v56" opacity=".5"/>
<path d="M44 214 q-12 -32 0 -60 q6 26 12 34" opacity=".5"/><path d="M46 214v56" opacity=".5"/>
</svg>"""

ICONS = {
 "Instagram": '<svg viewBox="0 0 24 24"><path d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5zm0 2a3 3 0 0 0-3 3v10a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3V7a3 3 0 0 0-3-3zm5 3.5a4.5 4.5 0 1 1 0 9 4.5 4.5 0 0 1 0-9zm0 2a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM17.5 5.5a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>',
 "Facebook": '<svg viewBox="0 0 24 24"><path d="M14 8V6.5c0-.8.2-1.5 1.5-1.5H17V2h-2.6C11.6 2 11 3.9 11 5.9V8H9v3h2v11h3V11h2.4l.6-3z"/></svg>',
 "YouTube": '<svg viewBox="0 0 24 24"><path d="M22 8.2s-.2-1.6-.9-2.3c-.8-.9-1.8-.9-2.2-1C15.8 4.7 12 4.7 12 4.7s-3.8 0-6.9.2c-.4.1-1.4.1-2.2 1C2.2 6.6 2 8.2 2 8.2S1.8 10 1.8 12v1.7c0 1.8.2 3.6.2 3.6s.2 1.6.9 2.3c.8.9 1.9.9 2.4 1 1.7.2 6.7.2 6.7.2s3.8 0 6.9-.3c.4 0 1.4-.1 2.2-1 .7-.7.9-2.3.9-2.3s.2-1.8.2-3.6V12c0-1.9-.2-3.8-.2-3.8zM9.9 15.3V8.9l6 3.2z"/></svg>',
 "Pinterest": '<svg viewBox="0 0 24 24"><path d="M12.2 2C6.7 2 4 5.9 4 9.2c0 2 .8 3.7 2.3 4.4.3.1.5 0 .6-.3l.2-.9c.1-.3 0-.4-.2-.7-.5-.6-.8-1.3-.8-2.4 0-3.1 2.3-5.8 6-5.8 3.3 0 5.1 2 5.1 4.7 0 3.5-1.6 6.5-3.9 6.5-1.3 0-2.2-1-1.9-2.3.4-1.5 1.1-3.2 1.1-4.3 0-1-.5-1.8-1.6-1.8-1.3 0-2.3 1.3-2.3 3.1 0 1.1.4 1.9.4 1.9L7.5 18c-.4 1.8-.1 4 0 4.2 0 .1.2.2.3.1.1-.1 1.4-1.8 1.9-3.4l.7-2.8c.4.7 1.4 1.3 2.6 1.3 3.4 0 5.7-3.1 5.7-7.3C18.7 5 16.1 2 12.2 2z"/></svg>',
 "X": '<svg viewBox="0 0 24 24"><path d="M17.8 3h3.1l-6.8 7.7L22 21h-6.2l-4.9-6.3L5.3 21H2.2l7.2-8.3L2 3h6.4l4.4 5.8zm-1.1 16.2h1.7L7.4 4.7H5.6z"/></svg>',
}
SOCIAL = [("Instagram", "https://instagram.com/vijayranresorts?utm_medium=copy_link"),
          ("Facebook", "https://www.facebook.com/vijayranresorts/"),
          ("Pinterest", "https://in.pinterest.com/vijayranresorts/_created/"),
          ("YouTube", "https://www.youtube.com/channel/UCkOLuu3C4PpCjX_KS8nZ5zg"),
          ("X", "https://twitter.com/vijayranresorts")]

ROOMS = [
 dict(slug="presidential-villas", name="Presidential Villas", short="Private pool & garden", count="5 villas",
  hero="2021/05/img01.jpg", card="2021/04/Villa-Master-Room.jpg",
  desc="Our Presidential Villa provides the world-class experience of finest luxuries and supreme comfort. The tasteful interiors, finest tapestry, lavish furniture and aesthetically pleasing art décor take you into a new world where you cannot help but fall in love with The Vijayran Palace."),
 dict(slug="terrace-haveli-suites", name="Terrace Haveli Suites", short="Sunset terraces & outdoor dining", count="5 suites",
  hero="2021/05/tr-02.jpg", card="2021/04/Haveli-Terrace-Suite.jpg",
  desc="Beautiful sunset, refreshing weather and gorgeous green surroundings: a spectacular view to die for, right from the terrace of your Haveli Suite. Embracing the atithi devo bhavah feel of Indian hospitality, The Vijayran Palace brings you its finest Terrace Haveli Suites."),
 dict(slug="courtyard-haveli-suites", name="Courtyard Haveli Suites", short="Private garden courtyards", count="11 suites · 1,345 sq ft",
  hero="2021/05/cou-01.jpg", card="2021/04/Haveli-Suite-Room.jpg",
  desc="If you ever wondered how a king would feel sitting in an expansive courtyard right beside his majestic room deciding what to have for dinner, book The Vijayran Palace's Courtyard Haveli Suite: the perfect blend of glorious old-world charm and modern amenities."),
 dict(slug="balcony-haveli-suites", name="Balcony Haveli Suites", short="Aangan-style courtyards & sunrise views", count="6 suites · 800 sq ft",
  hero="2021/05/bl-03.jpg", card="2021/04/Balcony-Haveli-Suites.jpg",
  desc="The Vijayran Palace offers Balcony Haveli Suites for guests who wish to enjoy the drizzles in a capacious aangan-style courtyard attached within their own suite. Enjoy the rain, cool breeze, mesmerising dusks and dawn."),
 dict(slug="jharoka-haveli-suites-2", name="Jharoka Haveli Suites", short="Hand-carved jharokas", count="4 suites · 600 sq ft",
  hero="2021/05/jslide1.jpg", card="2021/04/Jharoka-Haveli-Suites.jpg",
  desc="Ever seen those Mughal art paintings where the beautiful queen and her king stand in beautifully carved Jharokas, lost in the sonnets sung by nature? You can be that King or Queen at The Vijayran Palace's Jharoka Haveli Suites."),
 dict(slug="haveli-room-twin-bed", name="Haveli Room Twin Bed", short="Twin-bed rooms, thoughtfully priced", count="4 rooms · 450 sq ft",
  hero="2021/05/havali.jpg", card="2021/04/Haveli-Room-with-Twin-Bed.jpg",
  desc="On a slightly tight budget yet want a luxurious feel? For The Vijayran Palace all its guests are special. Book the Haveli Room with twin spring beds that cuddle you to sleep with monarch-like comfort."),
]

GALLERY = [
 "2021/06/Main-Gate.jpg", "2021/06/g11.jpg", "2021/06/g10.jpg", "2021/06/g9.jpg",
 "2021/06/g8.jpg", "2021/06/g7-scaled.jpg", "2021/06/g6.jpg", "2021/06/g5.jpg",
 "2021/06/g4.jpg", "2021/06/g3.jpg", "2021/06/g2.jpg"
]
GALLERY_ALT = [
 "Main gate of The Vijayran Palace", "Pre-wedding shoot at The Vijayran Palace", "Wedding palace in Rajasthan",
 "Day outing at The Vijayran Palace", "Pre-wedding shoot location", "Heritage architecture",
 "Wedding venue", "Wedding celebrations", "Destination wedding in Jaipur",
 "The Vijayran Palace by Royal Quest Resorts", "Destination wedding"
]

def header():
    return f"""<nav class="g_nav_w">
  <div class="nav_bar">
    <button class="menu_trigger" aria-label="Open menu">
      <div class="menu_lines"><span></span><span></span><span></span></div>
      <span>Menu</span>
    </button>
    <a class="nav_logo" href="{u()}" aria-label="The Vijayran Palace Home">
      <span class="nav_logo_text">THE VIJAYRAN PALACE</span>
      <span class="nav_logo_sub">BY ROYAL QUEST RESORTS</span>
    </a>
    <div class="book_wrapper">
      <button class="main_b book_btn" aria-haspopup="true">
        <div class="d_y_button">
          <span>Book Now</span>
          <span class="ab" aria-hidden="true">Book Now</span>
        </div>
        <svg class="b_arrow" viewBox="0 0 10 6" fill="none" stroke="currentColor"><path d="M1 1l4 4 4-4"/></svg>
      </button>
      <div class="book_dropdown">
        <a href="{BOOK}" target="_blank" rel="noopener">Book a Stay<small>Check rates &amp; availability</small></a>
        <a href="{u('best-destination-wedding-venues-in-jaipur')}#enquire">Plan a Wedding / Event<small>Send an enquiry</small></a>
        <a href="{u('resort-near-jaipur-for-day-outing')}">Day Outing Packages<small>Pool, high tea &amp; dinner</small></a>
        <a href="tel:{TEL_ROOMS}">Call Reservations<small>{PHONE_ROOMS}</small></a>
      </div>
    </div>
  </div>
</nav>

<div class="g_nav_open" aria-hidden="true">
  <div class="nav_cards_row">
    <a class="nav_card_item" href="{u('accommodation')}">
      <div class="nc_img_wrap">{img('2021/04/Villa-Master-Room.jpg', 'Accommodation')}
        <div class="nc_line"></div>
      </div>
      <div class="nc_title">Accommodation</div>
      <div class="nc_label">35 Villas, Haveli Suites &amp; Rooms</div>
    </a>
    <a class="nav_card_item" href="{u('best-destination-wedding-venues-in-jaipur')}">
      <div class="nc_img_wrap">{img('2021/06/g10.jpg', 'Destination Weddings')}
        <div class="nc_line"></div>
      </div>
      <div class="nc_title">Weddings</div>
      <div class="nc_label">Palace Grandeur &amp; Celebrations</div>
    </a>
    <a class="nav_card_item" href="{u('yoga-spa-pool-luxury-resort-jaipur-rajasthan')}">
      <div class="nc_img_wrap">{img('2021/06/ambertallpool-img.jpg', 'Experiences')}
        <div class="nc_line"></div>
      </div>
      <div class="nc_title">Experiences</div>
      <div class="nc_label">Culture, Safaris &amp; Wellness</div>
    </a>
  </div>
  <div class="nav_links_grid">
    <div class="nav_links_left">
      <div class="nav_col">
        <h4>Stay</h4>
        <a href="{u('presidential-villas')}">Presidential Villas</a>
        <a href="{u('terrace-haveli-suites')}">Terrace Haveli Suites</a>
        <a href="{u('courtyard-haveli-suites')}">Courtyard Haveli Suites</a>
        <a href="{u('balcony-haveli-suites')}">Balcony Haveli Suites</a>
        <a href="{u('jharoka-haveli-suites-2')}">Jharoka Haveli Suites</a>
        <a href="{u('haveli-room-twin-bed')}">Haveli Room Twin Bed</a>
      </div>
      <div class="nav_col">
        <h4>Experience</h4>
        <a href="{u('yoga-spa-pool-luxury-resort-jaipur-rajasthan')}">Activities</a>
        <a href="{u('top-holiday-resort-in-jaipur-for-family')}">Attractions</a>
        <a href="{u('best-luxury-dining-resort-in-jaipur')}">Dining</a>
        <a href="{u('heritage-wedding-resort-jaipur-rajasthan')}">Gallery</a>
      </div>
    </div>
    <div class="nav_links_right">
      <a href="{u('best-destination-wedding-venues-in-jaipur')}"><span>Wedding</span> →</a>
      <a href="{u('resort-near-jaipur-for-day-outing')}"><span>Day Outing</span> →</a>
      <a href="{u('get-in-touch-resort-in-kukas-jaipur')}"><span>Get In Touch</span> →</a>
      <a href="{u('covid19')}"><span>Covid-19 Safety</span> →</a>
    </div>
  </div>
</div>"""

def footer():
    ribbon_figs = "".join(f'<div class="ribbon_card">{img(p, a)}</div>' for p, a in zip(GALLERY, GALLERY_ALT))
    soc = "".join(f'<a href="{h}" aria-label="{n}" target="_blank" rel="noopener">{ICONS[n]}</a>' for n, h in SOCIAL)
    return f"""
<section class="bottom_image_ribbon" aria-label="Palace Gallery Ribbon">
  <div class="ribbon_header">
    <span>The Vijayran Palace · Kukas, Jaipur</span>
    <i></i>
  </div>
  <div class="ribbon_wrapper">
    <div class="ribbon_track">{ribbon_figs}</div>
    <div class="ribbon_track" aria-hidden="true">{ribbon_figs}</div>
  </div>
</section>

<footer class="footer_s">
  <div class="footer_top_bar">
    <div class="footer_logo">
      <img src="{P.R}media/wp-content/uploads/2022/07/logo3.png" alt="Royal Quest Resorts Crest" width="90" height="96">
    </div>
    <div class="footer_awards">
      <img src="{P.R}assets/img/tripadvisor.svg" alt="Tripadvisor">
      <div>
        <b>4.5 of 5</b>
        <span>Tripadvisor · based on 284 reviews</span>
      </div>
    </div>
  </div>

  <div class="footer_grid">
    <div class="footer_col">
      <h4>Resort Address</h4>
      <p class="lbl">Jaipur Office</p>
      <p>The Vijayran Palace By Royal Quest Resorts<br>{ADDRESS_OLD}</p>
      <p class="lbl">Reservation For</p>
      <p>Room: <a class="wipe_link" href="tel:{TEL_ROOMS}">9999822609<span class="f_line"></span></a><br>
         Wedding/Event: <a class="wipe_link" href="tel:{TEL_EVENTS}">9999163809<span class="f_line"></span></a><br>
         Email: <a class="wipe_link" href="mailto:{EMAIL}">{EMAIL}<span class="f_line"></span></a></p>
      <div style="margin-top:20px">
        <a class="l_b_w white" href="{u('get-in-touch-resort-in-kukas-jaipur')}">
          <div class="d_y_button"><span>Contact Us</span><span class="ab">Contact Us</span></div>
        </a>
      </div>
    </div>

    <div class="footer_col">
      <h4>Quick Links</h4>
      <ul>
        <li><a class="f_link" href="{u('about-us-luxury-resort-of-jaipur')}">About us<span class="f_line"></span></a></li>
        <li><a class="f_link" href="{u('best-destination-wedding-venues-in-jaipur')}">Destination Wedding<span class="f_line"></span></a></li>
        <li><a class="f_link" href="{u('yoga-spa-pool-luxury-resort-jaipur-rajasthan')}">Resort Activities<span class="f_line"></span></a></li>
        <li><a class="f_link" href="{u('best-luxury-dining-resort-in-jaipur')}">Luxury Dining<span class="f_line"></span></a></li>
        <li><a class="f_link" href="{u('resort-near-jaipur-for-day-outing')}">Day Outing Resort<span class="f_line"></span></a></li>
        <li><a class="f_link" href="{u('terms-and-conditions')}">Terms &amp; Conditions<span class="f_line"></span></a></li>
        <li><a class="f_link" href="{u('career')}">Career<span class="f_line"></span></a></li>
        <li><a class="f_link" href="{u('faq')}">FAQ<span class="f_line"></span></a></li>
        <li><a class="f_link" href="{u('covid19')}">Covid-19 Safety<span class="f_line"></span></a></li>
      </ul>
    </div>

    <div class="footer_col">
      <h4>Stay Connected With Vijayran</h4>
      <form class="footer_form" onsubmit="event.preventDefault(); this.innerHTML='<p>Thank you for subscribing.</p>';">
        <input type="email" required placeholder="EMAIL ADDRESS" aria-label="Email address">
        <small>Receive news of seasonal packages, royal celebrations and offers from The Vijayran Palace. You may unsubscribe at any time.</small>
        <label><input type="checkbox" required> I accept the Terms &amp; Conditions</label>
        <div>
          <button class="main_b" type="submit" style="height:2.8rem;padding:0 1.6rem">
            <div class="d_y_button"><span>Sign Up</span><span class="ab">Sign Up</span></div>
          </button>
        </div>
      </form>
      <div class="footer_socials">{soc}</div>
    </div>
  </div>

  <div class="footer_bot_bar">
    <span>Copyright © <span data-year>2026</span> Royal Quest Resorts. All Rights Reserved.</span>
    <span>Website Designed &amp; Promoted By: <a href="https://digitalmarketingrajasthan.com/" target="_blank" rel="noopener">Digital Marketing Rajasthan</a></span>
  </div>
</footer>"""

def page(path, title, desc, body):
    depth = path.count("/")
    P.R = "../" * depth
    canon = SITE + (path[:-10] if path.endswith("index.html") else path)
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}">
<link rel="icon" href="{P.R}media/wp-content/uploads/2022/07/logo3.png">
<link rel="apple-touch-icon" href="{P.R}media/wp-content/uploads/2022/07/logo3.png">
<link rel="stylesheet" href="{P.R}assets/css/site.css">
</head>
<body>
{header()}
<main id="main">
{body}
</main>
{footer()}
<script src="{P.R}assets/js/vendor/gsap.min.js"></script>
<script src="{P.R}assets/js/vendor/ScrollTrigger.min.js"></script>
<script src="{P.R}assets/js/vendor/lenis.min.js"></script>
<script src="{P.R}assets/js/site.js"></script>
</body>
</html>"""
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full) or OUT, exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(doc)

def build():
    # ---------- HOMEPAGE ----------
    P.R = ""
    room_cards = "".join(f"""
      <a class="camp_card" href="{u(r['slug'])}">
        <div class="ca_img_w">{img(r['card'], r['name'])}</div>
        <div class="ca_line_w"><div class="ca_line"></div></div>
        <div class="ca_name">{r['name']}</div>
        <p class="ca_desc">{r['short']}</p>
      </a>""" for r in ROOMS)

    story_photos = [
      ("2021/06/g3.jpg", ("left", "second"), "Destination Wedding"),
      ("2021/06/g5.jpg", ("right", "third"), "Wedding Celebrations"),
      ("2021/06/g9.jpg", ("left", "fourth"), "Palace Grounds"),
      ("2021/06/g4.jpg", ("right", "fifth"), "Heritage Haveli"),
      ("2021/06/g10.jpg", ("left", "second"), "Royal Ballroom")
    ]
    story_items = "".join(f"""
      <div class="story_items {align}" data-speed="{0.85 + 0.15 * i:.2f}">
        <div class="story_item_p {sz}">
          {img(p, alt, 'story_img_main', True)}
        </div>
      </div>""" for i, (p, (align, sz), alt) in enumerate(story_photos))

    ig_tiles = "".join(f"""
      <a class="ig_tile {'hide' if i > 12 else ''}" href="{IG_URL}" target="_blank" rel="noopener">
        <img src="assets/img/ig/{i:02d}.jpg" alt="Instagram post {i}">
      </a>""" for i in range(1, 21))

    home_body = f"""
<section class="hero_s">
  <div class="main_video">
    <video class="hero_video" autoplay loop muted playsinline preload="auto" poster="media/wp-content/uploads/2023/05/banner-01-1.jpg">
      <source src="media/wp-content/uploads/2021/04/TheVijayranPalaceJaipurnew.mp4" type="video/mp4">
      <source src="{LIVE}2021/04/TheVijayranPalaceJaipurnew.mp4" type="video/mp4">
    </video>
    <div class="video_bg_c"></div>
    <button class="sound_trigger" aria-label="Toggle sound">
      <svg class="s_off" viewBox="0 0 24 24"><path d="M4 9v6h4l5 4V5L8 9H4z"/><path d="M17 9l5 6M22 9l-5 6"/></svg>
      <svg class="s_on" viewBox="0 0 24 24"><path d="M4 9v6h4l5 4V5L8 9H4z"/><path d="M16.5 8.5a5 5 0 0 1 0 7M19 6a8.5 8.5 0 0 1 0 12"/></svg>
    </button>
  </div>
  <div class="h_p">
    <div class="d_y">
      <h1 class="h_title">Where dreams come true and once-in-a-lifetime memories are born.</h1>
    </div>
    <div class="d_y">
      <p class="h_sub">The Vijayran Palace by Royal Quest Resorts · Kukas, Jaipur</p>
    </div>
  </div>
  <div class="scroll_cue"><span>SCROLL</span></div>
</section>

<div class="p_c">
  <!-- Section 1: Intro -->
  <section class="intro_s">
    <div class="i_p">
      <div class="d_y">
        <h2 class="i_title">A palace for the <span class="t_label">romantic,</span> the <span class="t_label">celebrant,</span> and those looking for <span class="t_label">the extraordinary.</span></h2>
      </div>
    </div>
    <div class="i_c">
      <div class="i_c_left">
        <div class="d_y">
          <p class="i_text">The Vijayran Palace – our heritage resort in Jaipur, Rajasthan is one of the finest royal resorts in entire Rajasthan. Set in the lap of the ancient Aravalli hills near Amer, you set your soul free and let your mind wander into the pristine, serene and solitary surroundings that sing the poetry of nature. An oasis of luxury and regal ambience that offers the perfect blend of modern age luxuries and a spiritual getaway.</p>
        </div>
        <div class="i_btn_w">
          <a href="{u('about-us-luxury-resort-of-jaipur')}" class="d_b_w">
            <div class="d_y_button">
              <span>Discover our story</span>
              <span class="ab" aria-hidden="true">Discover our story</span>
            </div>
            →
          </a>
        </div>
      </div>
      <div class="i_c_right">
        <div class="i_sketch_w">
          {SKETCH}
        </div>
      </div>
    </div>
  </section>

  <!-- Section 2: Full-Bleed Quote Banner -->
  <section class="certification_s">
    <div class="c_b_p">
      {img('2021/05/view.jpg', 'Aravalli Hills', 'c_img', True)}
      <div class="c_bg"></div>
    </div>
    <div class="c_p">
      <div class="c_c">
        <div class="c_label_p">
          <div class="c_line"></div>
          <div class="d_y"><div class="c_label_txt">Tripadvisor · 4.5 of 5 · 284 Reviews</div></div>
        </div>
        <div class="d_y">
          <p class="c_text">“A venue for the destination marriage appears like a dream come true. Beautiful lawns, well-appointed rooms and an old traditional look with all modern amenities.”</p>
        </div>
        <div class="d_y">
          <div class="c_author">Nidhi B · Guest Review</div>
        </div>
      </div>
    </div>
  </section>

  <!-- Section 3: Our Stays -->
  <section class="camp_section" id="accommodation">
    <div class="ca_top">
      <div class="ca_p_left">
        <div class="d_y"><h2 class="ca_title">Our Stays</h2></div>
        <div class="d_y"><p class="ca_text">Thirty-five villas, suites and rooms set around courtyards, terraces and gardens. Each is designed for a distinct way of living like royalty in the Aravalli hills.</p></div>
      </div>
      <div class="ca_p_right">
        <a href="{u('accommodation')}" class="y_b_w">
          <div class="d_y_button"><span>Discover all stays</span><span class="ab" aria-hidden="true">Discover all stays</span></div>
        </a>
      </div>
    </div>
    <div class="camp_track">{room_cards}</div>
  </section>

  <!-- Section 4: Sticky Weddings Story with Parallax Gallery -->
  <section class="story_s" id="weddings">
    <div class="story_p">
      <div class="story_stck">
        <div class="story_c">
          <div class="d_y">
            <h2 class="story_title">Weddings At The <span class="t_label">Vijayran</span> Palace</h2>
          </div>
          <div class="d_y">
            <p class="story_text">What can be more beautiful than a regal style wedding where the prince charming swoops his princess off feet. Royal tapestry, artistic décor and exotic ambience! The Vijayran Palace gifts you the amazing palace grandeur where you can choose to have a wedding like the Kings and Queens of yester-years. Rustic authentic feast, exotic backdrops for pre and post wedding photo shoots, beautiful theme-based décor and musical nights.</p>
          </div>
          <div class="d_y">
            <a href="{u('best-destination-wedding-venues-in-jaipur')}" class="d_b_w">
              <div class="d_y_button"><span>Discover weddings</span><span class="ab" aria-hidden="true">Discover weddings</span></div>
            </a>
          </div>
        </div>
      </div>
      <div class="story_img_hold">
        <div class="story_imgs_wrap">
          {story_items}
        </div>
      </div>
    </div>
  </section>

  <!-- Section 5: Pre-Weddings & Celebrations Split -->
  <section class="split_section">
    <div class="split_grid">
      <div class="split_img_w">
        {img('2023/05/pre-wedding.jpg', 'Pre-Wedding Shoot at The Vijayran Palace')}
      </div>
      <div class="split_content">
        <span class="label">Photo Shoots</span>
        <h3>Pre - Weddings</h3>
        <p>The Vijayran Palace’s beautiful architecture, lush greenery, Jharokas, the rugged Mountain View in backdrop and sunset by the pool side are an added attraction for the groom and bride who awaits their photo shoots with great enthusiasm. Imagine the photo shoots where you could be the royal queen standing in a Jharoka and your prince charming with his enigmatic smile stealing glances right beside you.</p>
        <div style="margin-top:24px">
          <a href="{u('best-destination-wedding-venues-in-jaipur')}" class="l_b_w">
            <div class="d_y_button"><span>Read More</span><span class="ab">Read More</span></div>
          </a>
        </div>
      </div>
    </div>
  </section>

  <section class="split_section" style="padding-top:0">
    <div class="split_grid rev">
      <div class="split_img_w">
        {img('2021/12/meetin-events.webp', 'Meeting & Events at The Vijayran Palace')}
      </div>
      <div class="split_content">
        <span class="label">Celebrations</span>
        <h3>Meeting &amp; Event</h3>
        <p>The Vijayran Palace offers another marvel in form of an on demand cultural show exclusively for wedding guests that include Rajasthan’s folk songs, folk dances and the much appreciated Ghoomar. Let the wedding guests twirl, sing &amp; dance, enjoy their heart’s content! A taste of Royal Rajasthan’s colorful culture and vibrancy. Let the music flow and feet tap in sync with the festive mood.</p>
        <div style="margin-top:24px">
          <a href="{u('best-destination-wedding-venues-in-jaipur')}" class="l_b_w">
            <div class="d_y_button"><span>Read More</span><span class="ab">Read More</span></div>
          </a>
        </div>
      </div>
    </div>
  </section>

  <!-- Section 6: Live Weather Widget -->
  <section class="weather_section" id="weather">
    <div class="wx_grid">
      <div>
        <span class="label">Live Weather · Kukas, Jaipur</span>
        <h2 style="font-size:clamp(28px,3.4vw,44px);margin:16px 0 20px">The weather at the palace, right now.</h2>
        <p style="max-width:48ch;font-size:15px;line-height:1.7;color:var(--text-body)">Check the sky over the Aravalli hills before you arrive: real-time temperature, wind, humidity, sunset and the five-day outlook for the resort, refreshed automatically.</p>
        <div style="margin-top:28px">
          <a href="{BOOK}" target="_blank" rel="noopener" class="main_b">
            <div class="d_y_button"><span>Book Your Stay</span><span class="ab">Book Your Stay</span></div>
          </a>
        </div>
      </div>
      <div class="wx_card">
        <div class="wx_head">
          <span class="wx_loc">The Vijayran Palace · Kukas</span>
          <span class="wx_live_badge">Live</span>
        </div>
        <div class="wx_temp_row">
          <div class="wx_icon"></div>
          <div>
            <div class="wx_temp_val"><span class="wx_temp_num">--</span><sup>°C</sup></div>
            <div class="wx_condition">Fetching weather…</div>
          </div>
        </div>
        <div class="wx_metrics">
          <div><small>Feels like</small><b data-wx-feels>--</b></div>
          <div><small>Humidity</small><b data-wx-hum>--</b></div>
          <div><small>Wind</small><b data-wx-wind>--</b></div>
          <div><small>Sunset</small><b data-wx-sun>--</b></div>
        </div>
        <div class="wx_forecast"></div>
      </div>
    </div>
  </section>

  <!-- Section 7: Instagram Feed Widget -->
  <section class="instagram_section" id="instagram">
    <div class="ig_header">
      <div class="ig_account">
        <div class="ig_avatar"><img src="media/wp-content/uploads/2022/07/logo3.png" alt="Vijayran Crest"></div>
        <div>
          <div class="ig_name">Instagram</div>
          <div class="ig_handle">@vijayranresorts</div>
        </div>
      </div>
      <a href="{IG_URL}" target="_blank" rel="noopener" class="d_b_w">
        <div class="d_y_button"><span>Follow on Instagram</span><span class="ab">Follow on Instagram</span></div>
      </a>
    </div>
    <div class="ig_grid">{ig_tiles}</div>
    <div style="text-align:center;margin-top:32px">
      <button class="l_b_w" data-ig-more type="button">
        <div class="d_y_button"><span>Load More...</span><span class="ab">Load More...</span></div>
      </button>
    </div>
  </section>
</div>"""

    page("index.html", "The Vijayran Palace | 5 Star Luxury Heritage Resort in Jaipur",
         "The Vijayran Palace by Royal Quest Resorts: luxury heritage resort in Jaipur, Rajasthan, with private pool villas, haveli suites and destination weddings.",
         home_body)

    # Rebuild inner pages
    for r in ROOMS:
        P.R = "../"
        room_body = f"""
        <div style="padding:140px var(--pad) 80px">
          <span class="label">{r['count']}</span>
          <h1 style="font-size:clamp(32px,4vw,56px);margin:16px 0 24px">{r['name']}</h1>
          <p style="max-width:64ch;font-size:16px;line-height:1.7">{r['desc']}</p>
          <div style="margin:40px 0;max-width:960px;aspect-ratio:16/9;overflow:hidden">
            {img(r['hero'], r['name'])}
          </div>
          <a class="main_b" href="{BOOK}" target="_blank" rel="noopener">
            <div class="d_y_button"><span>Check Availability</span><span class="ab">Check Availability</span></div>
          </a>
        </div>"""
        page(f"{r['slug']}/index.html", f"{r['name']} | The Vijayran Palace", r['desc'], room_body)

    # Other main pages
    P.R = "../"
    page("accommodation/index.html", "Accommodation | The Vijayran Palace", "All villas and haveli suites.",
         f"<div style='padding:140px var(--pad) 80px'><h1 style='font-size:48px;margin-bottom:40px'>Accommodation</h1><div class='camp_track' style='flex-wrap:wrap'>{room_cards}</div></div>")
    
    page("best-destination-wedding-venues-in-jaipur/index.html", "Destination Wedding Venues in Jaipur | The Vijayran Palace", "Weddings like kings and queens.",
         f"<div style='padding:140px var(--pad) 80px'><span class='label'>Weddings</span><h1 style='font-size:48px;margin:16px 0 24px'>Destination Weddings</h1><p style='max-width:60ch;font-size:16px;line-height:1.7'>Royal tapestry, artistic decor and exotic ambience! The Vijayran Palace gifts you the amazing palace grandeur where you can choose to have a wedding like the Kings and Queens of yester-years.</p><div style='margin-top:32px'><a href='{BOOK}' class='main_b'><div class='d_y_button'><span>Plan Celebration</span><span class='ab'>Plan Celebration</span></div></a></div></div>")

    page("resort-near-jaipur-for-day-outing/index.html", "Day Outing Resort near Jaipur | The Vijayran Palace", "Day outing packages near Jaipur.",
         f"<div style='padding:140px var(--pad) 80px'><span class='label'>Packages</span><h1 style='font-size:48px;margin:16px 0 24px'>Day Outing Resort in Jaipur</h1><p style='max-width:60ch;font-size:16px;line-height:1.7'>Summer Splash Package (Day Outing) ! Inclusive of Swimming pool access, Hi Tea, Dinner (Set Menu). Price: INR 2,500++ per person. Timing: 1400hrs till 2100hrs.</p><div style='margin-top:32px'><a href='tel:{TEL_ROOMS}' class='d_b_w'><div class='d_y_button'><span>Call to Book: {PHONE_ROOMS}</span><span class='ab'>Call to Book: {PHONE_ROOMS}</span></div></a></div></div>")

    page("get-in-touch-resort-in-kukas-jaipur/index.html", "Get In Touch | The Vijayran Palace", "Contact details for reservations and events.",
         f"<div style='padding:140px var(--pad) 80px'><span class='label'>Contact</span><h1 style='font-size:48px;margin:16px 0 24px'>Get In Touch</h1><p style='font-size:16px;line-height:1.8'><b>Jaipur Office:</b> {ADDRESS_OLD}<br><b>Room Reservations:</b> <a href='tel:{TEL_ROOMS}'>{PHONE_ROOMS}</a><br><b>Weddings / Events:</b> <a href='tel:{TEL_EVENTS}'>{PHONE_EVENTS}</a><br><b>Email:</b> <a href='mailto:{EMAIL}'>{EMAIL}</a></p></div>")

    page("covid19/index.html", "Covid-19 Precautions | The Vijayran Palace", "Sanitized environment and safe practices.",
         f"<div style='padding:140px var(--pad) 80px'><span class='label'>Safety Assurance</span><h1 style='font-size:48px;margin:16px 0 24px'>Covid-19 Precautions</h1><p style='max-width:64ch;font-size:16px;line-height:1.7'>For your assurance, our hotel partners have self-certified that your rooms and surroundings are sanitized as per WHO Advisory, and their staff is trained to prioritize your safety.</p></div>")

    page("about-us-luxury-resort-of-jaipur/index.html", "About Us | The Vijayran Palace", "About The Vijayran Palace luxury heritage resort.",
         f"<div style='padding:140px var(--pad) 80px'><span class='label'>Our Story</span><h1 style='font-size:48px;margin:16px 0 24px'>About The Vijayran Palace</h1><p style='max-width:64ch;font-size:16px;line-height:1.7'>The Vijayran Palace â€“ our heritage resort in Jaipur, Rajasthan is one of the finest royal resorts in entire Rajasthan.</p></div>")

    page("yoga-spa-pool-luxury-resort-jaipur-rajasthan/index.html", "Activities | The Vijayran Palace", "Yoga, spa, pool and recreational activities.",
         f"<div style='padding:140px var(--pad) 80px'><span class='label'>Experience</span><h1 style='font-size:48px;margin:16px 0 24px'>Activities</h1><p style='max-width:64ch;font-size:16px;line-height:1.7'>Choose a village safari, a majestic elephant ride, a ride on the finest horses, an open jeep safari, or simply gaze at the magnificent night sky.</p></div>")

    page("top-holiday-resort-in-jaipur-for-family/index.html", "Attractions | The Vijayran Palace", "Attractions near Jaipur.",
         f"<div style='padding:140px var(--pad) 80px'><span class='label'>Near the Palace</span><h1 style='font-size:48px;margin:16px 0 24px'>Attractions</h1><p style='max-width:64ch;font-size:16px;line-height:1.7'>Amber Fort is just 10 km away. Hawa Mahal, City Palace and Gaitore are all within easy reach.</p></div>")

    page("best-luxury-dining-resort-in-jaipur/index.html", "Dining | The Vijayran Palace", "Fine dining at Swarn Mahal.",
         f"<div style='padding:140px var(--pad) 80px'><span class='label'>Culinary</span><h1 style='font-size:48px;margin:16px 0 24px'>Dining</h1><p style='max-width:64ch;font-size:16px;line-height:1.7'>Our restaurant speaks of a bygone regal era through tastefully decorated interiors, fine tapestry and exquisite miniature artwork.</p></div>")

    page("heritage-wedding-resort-jaipur-rajasthan/index.html", "Gallery | The Vijayran Palace", "Photo gallery.",
         f"<div style='padding:140px var(--pad) 80px'><h1 style='font-size:48px;margin-bottom:40px'>Gallery</h1><div class='camp_track' style='flex-wrap:wrap'>{''.join(f'<div class=\"camp_card\">{img(p, a)}</div>' for p, a in zip(GALLERY, GALLERY_ALT))}</div></div>")

    page("career/index.html", "Careers | The Vijayran Palace", "Careers.",
         f"<div style='padding:140px var(--pad) 80px'><h1 style='font-size:48px;margin-bottom:20px'>Careers</h1><p>Join the team at The Vijayran Palace. Send your resume to <a href='mailto:{EMAIL_SALES}'>{EMAIL_SALES}</a>.</p></div>")

    page("faq/index.html", "FAQ | The Vijayran Palace", "Frequently asked questions.",
         f"<div style='padding:140px var(--pad) 80px'><h1 style='font-size:48px;margin-bottom:20px'>Frequently Asked Questions</h1><p>Check-in: 2:00 PM · Check-out: 11:00 AM. Location: NH-8 Kukas, Jaipur.</p></div>")

    page("terms-and-conditions/index.html", "Terms & Conditions | The Vijayran Palace", "Terms & conditions.",
         f"<div style='padding:140px var(--pad) 80px'><h1 style='font-size:48px;margin-bottom:20px'>Terms &amp; Conditions</h1><p>Website terms and booking conditions of The Vijayran Palace by Royal Quest Resorts.</p></div>")

    print("Build complete: 20 pages generated.")

if __name__ == "__main__":
    build()
