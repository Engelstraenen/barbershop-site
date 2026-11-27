#!/usr/bin/env python3
"""KANTE – Barbershop „Wisch drüber“ (Aubergine + Mint). python3 build.py"""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); V = '28d'
BRAND = 'KANTE'
has = lambda k: os.path.exists(os.path.join(H, 'assets/img', k + '.webp'))
SEQ = json.load(open(os.path.join(H, 'assets/seq/seq.json'))) if os.path.exists(os.path.join(H, 'assets/seq/seq.json')) else None
NAV = [('Wisch drüber', '#top'), ('Barber', '#wand'), ('Fade', '#hoehe'), ('Termin', '#termin'), ('Liste', '#liste'), ('Karriere', '#karriere'), ('Bewertungen', '#bewertungen')]
TEAM = [('milan', 'Milan', 'Fade & Line-up'), ('yusuf', 'Yusuf', 'Kontur & Bart'), ('noah', 'Noah', 'Locken'), ('ben', 'Ben', 'Meister · Akademie')]
LOOKS = [('fade-low', 'Low Fade', 'Startet knapp über dem Ohr. Dezent, wächst unauffällig raus.', '3–4 Wochen'),
         ('nachher', 'Mid Fade', 'Auf Schläfenhöhe. Der Klassiker, sichtbar, aber nicht laut.', '2–3 Wochen'),
         ('fade-high', 'High Fade', 'Bis zur Kopfrundung. Starker Kontrast, braucht oft Pflege.', '2 Wochen'),
         ('buzz-bart', 'Buzz + Bart', 'Eine Länge rundum, dazu ein scharf konturierter Bart.', '3 Wochen')]
PLIST = [('Haare', [('Haarschnitt', '45 Min.', 'fade.html'), ('Skin Fade', '45 Min.', 'fade.html'), ('Buzz Cut', '20 Min.', 'fade.html'), ('Jungs bis 14', '30 Min.', 'fade.html')]),
         ('Bart', [('Bart in Form', '30 Min.', 'bart.html'), ('Haare &amp; Bart', '60 Min.', 'bart.html'), ('Bart färben', '20 Min.', 'bart.html')]),
         ('Kontur', [('Line-up', '15 Min.', 'kontur.html'), ('Nacken frei', '10 Min.', 'kontur.html'), ('Augenbrauen', '10 Min.', 'kontur.html')])]
SVC = ['Haarschnitt', 'Skin Fade', 'Haare & Bart', 'Bart in Form', 'Line-up']


def pic(key, alt, lazy=True, cls=''):
    if not has(key): return ''
    m = f'<source media="(max-width: 900px) and (min-height: 501px)" srcset="assets/img/{key}-m.webp">' if has(key + '-m') else ''
    return f'<picture class="{cls}">{m}<img src="assets/img/{key}.webp" alt="{alt}" {"loading=lazy" if lazy else "fetchpriority=high"} decoding="async"></picture>'


def head(title, desc, extra=''):
    return f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title><meta name="description" content="{desc}"><meta name="theme-color" content="#24121f">
<link rel="preload" href="assets/fonts/syne-latin-3.woff2" as="font" type="font/woff2" crossorigin>{extra}
<link rel="stylesheet" href="assets/css/fonts.css?v={V}"><link rel="stylesheet" href="assets/css/style.css?v={V}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%2324121f'/%3E%3Crect x='10' y='6' width='12' height='20' rx='6' fill='none' stroke='%239fe3c6' stroke-width='3'/%3E%3C/svg%3E">
</head><body>'''


def header(sub=False):
    links = ''.join(f'<a href="{("index.html" + h) if sub else h}">{t}</a>' for t, h in NAV)
    return f'''<header class="hd"><a class="logo" href="{"index.html" if sub else "#top"}" aria-label="{BRAND} Startseite"><i></i>{BRAND}</a>
<nav class="nav" id="nav">{links}<a class="btn" href="{"index.html" if sub else ""}#termin">Stuhl buchen</a></nav>
<button class="burger" aria-label="Menü" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button></header>'''


def foot(sub=False):
    p = 'index.html' if sub else ''
    return f'''<footer class="ft" id="kontakt"><div class="wrap"><span class="kick">Besuch</span><h2 class="disp">Setz dich.<br>Wir machen den Rest.</h2>
<div class="grid"><div><p style="max-width:40ch;color:var(--mute)">Kölner Straße 88 · 40211 Düsseldorf (Demo-Adresse)<br>Telefon 0211 000 000 1 (Demo)</p><p style="margin-top:20px;display:flex;gap:10px;flex-wrap:wrap"><a class="btn" href="{p}#termin">Stuhl buchen</a><a class="btn ghost" href="besuch.html">Anfahrt</a></p></div>
<div><span class="kick">Öffnungszeiten</span><div style="margin-top:10px"><div class="row"><span>Mo</span><span>zu</span></div><div class="row"><span>Di – Fr</span><span>10 – 20 Uhr</span></div><div class="row"><span>Sa</span><span>9 – 17 Uhr</span></div><div class="row"><span>Walk-in</span><span>Di – Fr 10 – 13 Uhr</span></div></div></div>
<div><span class="kick">Mehr</span><ul style="margin-top:6px"><li><a href="fade.html">Fade</a></li><li><a href="bart.html">Bart</a></li><li><a href="kontur.html">Kontur</a></li><li><a href="team.html">Barber</a></li><li><a href="akademie.html">Akademie</a></li></ul></div></div>
<div class="fine"><span>{BRAND} ist eine Demo-Webseite eines Musterbetriebs. Formulare senden nichts, Termine sind Beispiele.</span><span><a href="impressum.html">Impressum</a> · <a href="datenschutz.html">Datenschutz</a></span></div></div></footer>
<div class="dlg" id="dlg-ok" role="dialog" aria-modal="true" aria-labelledby="dlg-t"><div class="box"><h3 id="dlg-t">Stuhl reserviert</h3><p></p><button class="btn" data-close>Alles klar</button></div></div>
<script src="assets/js/app.js?v={V}" defer></script></body></html>'''


def swipe(a, b, alt_a, alt_b, auto=False, lazy=True):
    return f'''<div class="mirror swipe" tabindex="0" role="slider" aria-label="Vorher / Nachher, zum Vergleichen ziehen" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50"{" data-auto" if auto else ""}>
 {pic(a, alt_a, lazy)}{pic(b, alt_b, lazy, 'after')}<span class="bar"></span><span class="knob">↔</span><span class="tag l">Vorher</span><span class="tag r">Nachher</span></div>'''


def index():
    pre = '<link rel="preload" as="image" href="assets/img/vorher.webp" media="(min-width: 901px), (max-height: 500px)" fetchpriority="high"><link rel="preload" as="image" href="assets/img/vorher-m.webp" media="(max-width: 900px) and (min-height: 501px)" fetchpriority="high">'
    bcards = ''.join(f'<button class="bcard" data-b="{k}">{"<img src=assets/img/team-" + k + ".webp alt=" + n + " loading=lazy>" if has("team-" + k) else ""}<span><b>{n}</b><small>{r}</small></span></button>' for k, n, r in TEAM)
    bbs = ''.join(f'<button class="opt bb" data-b="{k}" data-name="{n}">{n}</button>' for k, n, r in TEAM)
    seq = f' data-n="{SEQ["n"]}" data-seq="assets/seq/d/f_###.webp?v={V}" data-seqm="assets/seq/m/f_###.webp?v={V}"' if SEQ else ''
    stills = ''.join(pic(k, a).replace('loading=lazy', 'loading=eager') for k, a in [('vorher', 'Vorher'), ('clipper', 'Arbeit'), ('nachher', 'Nachher')] if has(k))
    cfgimgs = ''.join(f'<img src="assets/img/{k}.webp" alt="{n}" loading="lazy" class="{"on" if k == "nachher" else ""}">' for k, n, *_ in LOOKS if has(k))
    chips = ''.join(f'<button class="chip{" on" if k == "nachher" else ""}" data-name="{n}" data-txt="{t}">{n}</button>' for k, n, t, _ in LOOKS if has(k))
    return head(f'{BRAND} – Barbershop', f'{BRAND}: Barbershop für Fade, Bart und Kontur. Vorher/Nachher wischen, Barber wählen, Stuhl online buchen.', pre) + header() + f'''
<main id="top">
<section class="hero">
 <div><span class="kick">Barbershop · Düsseldorf</span><h1 class="disp">Wisch<br><em>drüber.</em></h1>
 <p class="lead">Links rein, rechts raus. Zieh die Linie über den Spiegel und sieh, was 45 Minuten bei uns ausmachen.</p>
 <div class="cta"><a class="btn" href="#termin">Stuhl buchen</a><a class="btn ghost" href="#wand">Barber wählen</a></div></div>
 {swipe('vorher', 'nachher', 'Kunde vorher mit langen, herausgewachsenen Locken im Spiegel', 'Derselbe Kunde nachher mit frischem Mid Skin Fade', auto=True, lazy=False)}
</section>

<section class="blk" id="wand"><div class="wrap">
 <span class="kick">Spiegelwand</span><h2 class="disp">Wen willst du?</h2><p class="lead">Vier Barber, vier Spiegel. Tipp auf einen: Er ist im Termin vorgewählt.</p>
 <div class="mirror wall rv">{pic('spiegelwand', 'Vier Barber in vier beleuchteten Spiegeln')}</div>
 <div class="barbers">{bcards}</div>
</div></section>

<section class="filmsec" aria-label="Vorher, Arbeit, Ergebnis im Spiegel">
 <div class="stage"{seq}><div class="mirror">{f'<div class="still">{stills}</div>' if stills else ''}<canvas aria-hidden="true"></canvas>
  <div class="filmtxt"><span class="kick">Im Spiegel</span><h2 class="disp">45 Minuten.<br>Ein Zug.</h2></div>
  <div class="steps3"><span class="on">Beratung</span><span>Fade blenden</span><span>Line-up &amp; Finish</span></div></div></div>
</section>

<section class="blk cfg" id="hoehe"><div class="wrap split">
 <div class="mirror rv">{cfgimgs}</div>
 <div><span class="kick">Fade-Höhe</span><h2 class="disp">Low, Mid oder High?</h2><p class="lead">Derselbe Kopf, vier Schnitte. Tipp durch und such dir deine Höhe aus, bevor du dich setzt.</p>
 <div class="chips">{chips}</div><div class="cfgname">Mid Fade</div><p class="cfgtxt lead" style="margin-top:6px">Auf Schläfenhöhe. Der Klassiker, sichtbar, aber nicht laut.</p>
 <a class="link" href="fade.html" data-sub>Alles über den Fade</a></div>
</div></section>

<section class="blk" id="bart"><div class="wrap split">
 <div><span class="kick">Bart</span><h2 class="disp">Auch hier: wisch drüber.</h2><p class="lead">Länge, Wangenlinie, Hals. Der Bart bekommt dieselbe Kante wie der Fade.</p><a class="link" href="bart.html" data-sub>Bart &amp; Kontur</a></div>
 {swipe('bart-vorher', 'bart-nachher', 'Bart vorher, ungleichmäßig', 'Bart nachher, scharf konturiert')}
</div></section>

<section class="blk" id="termin"><div class="wrap split" style="align-items:start">
 <div><span class="kick">Termin · 24/7</span><h2 class="disp">Dein Stuhl.<br>Deine Zeit.</h2><p class="lead" style="margin-bottom:22px">Kein Anruf, während die Maschine läuft. Barber und Zeit wählen, fertig.</p>
  <div class="gapcard"><span class="dot"></span><p><b>Lücke frei: heute 16:30</b>Jemand hat abgesagt. Auf der Warteliste bekommst du so etwas per SMS.</p><button class="btn">Nehmen</button></div>
  <p class="demo-note" style="margin-top:10px">Beispiel – im echten Betrieb live aus dem Kalender.</p></div>
 <div class="card" id="booking">
  <div class="again">{"<img src=assets/img/team-milan.webp alt=Milan>" if has("team-milan") else ""}<p><b>Wie immer?</b><br>Skin Fade bei Milan, nächster freier Termin.</p><button class="btn">Ein Tipp</button></div>
  <h3>1 · Leistung</h3><div class="opts">{''.join(f'<button class="opt" data-svc="{s}">{s.replace("&", "&amp;")}</button>' for s in SVC)}</div>
  <h3>2 · Barber</h3><div class="opts">{bbs}</div>
  <h3>3 · Tag &amp; Zeit</h3><div class="days"></div><div class="slots"></div>
  <div class="sum"><p></p><button class="btn" disabled>Stuhl buchen</button></div>
  <p class="demo-note" style="margin-top:10px">Demo: Zeiten sind Beispiele, es wird nichts gebucht.</p>
 </div>
</div></section>

<section class="blk" id="liste" style="padding-top:20px"><div class="wrap">
 <span class="kick">Liste</span><h2 class="disp">Was wir machen.</h2><p class="lead">Mit Dauer. Den Preis siehst du beim Buchen, bevor du bestätigst.</p>
 <div class="plist">{''.join(f'<div class="pcard rv"><h3>{cat}</h3><table>' + ''.join(f'<tr><td><a href="{u}" data-sub>{n}</a></td><td>{t}</td></tr>' for n, t, u in rows) + '</table></div>' for cat, rows in PLIST)}</div>
</div></section>

<section class="blk" id="karriere"><div class="wrap split">
 <div class="mirror rv" style="aspect-ratio:16/10">{pic('feierabend', 'Leerer Stuhl vor dem Spiegel zum Feierabend, im Spiegel das lachende Team')}</div>
 <div><span class="kick">Dein Platz am Spiegel</span><div class="kin"><span>Ausbildung.</span><span>Feste Kundschaft.</span><span>Weiterbildung.</span></div>
 <p class="lead" style="margin-top:16px">Wir suchen Azubis und Barber. Eigener Stuhl, Stammkunden ab Tag eins, Akademie-Abend jeden Mittwoch.</p><a class="link" href="akademie.html" data-sub>Alles zur Akademie</a>
 <div class="apply"><span class="timer">60 s</span><h3>Bewerben in 60 Sekunden</h3><div class="prog60"><i></i></div>
  <div class="step on"><button class="btn" data-next>Los</button></div>
  <div class="step"><label>Was suchst du?</label><div class="opts">{''.join(f'<button class="opt" data-next>{t}</button>' for t in ['Ausbildung', 'Job als Barber', 'Abendkurs'])}</div></div>
  <div class="step"><form><label for="ap-n">Vorname</label><input id="ap-n" autocomplete="given-name" required><label for="ap-t">Handynummer</label><input id="ap-t" type="tel" autocomplete="tel" required><p style="margin-top:14px"><button class="btn" type="submit">Abschicken</button></p></form></div>
  <div class="step"><h3>Danke.</h3><p style="margin-top:8px;color:var(--mute)">Demo: Es wurde nichts gesendet. Im echten Betrieb meldet sich Ben innerhalb von 48 Stunden.</p></div></div></div>
</div>
<div class="wrap"><div class="nums">
  <div><b data-count="80118">0</b><p>Friseursalons in Deutschland Ende 2025 – 245 weniger als im Jahr davor.</p></div>
  <div><b data-count="7497">0</b><p>neue Ausbildungsverträge Friseur/-in 2025, bundesweit.</p></div>
  <div><b data-count="40.6" data-dec="1" data-pre="−" data-suf=" %">0</b><p>Friseur-Azubis in NRW seit 2014. Wer jetzt lernt, wird gebraucht.</p></div></div>
 <p class="src">Quellen: Zentralverband des Deutschen Friseurhandwerks, PM 06/2026 (Salons; Ausbildungsverträge nach BIBB); Bezirksregierung Arnsberg. Stand 11/2026.</p></div>
</section>

<section class="blk" id="bewertungen"><div class="wrap"><span class="kick">Stimmen</span><h2 class="disp">Was Kunden sagen könnten.</h2>
 <div class="revs"><div class="rev"><p>„Seit einem Jahr derselbe Barber, derselbe Schnitt. Ein Tipp und gebucht.“</p><small>Beispiel · noch keine echte Bewertung</small></div>
 <div class="rev"><p>„Vorher im Spiegel gezeigt, wie hoch der Fade geht. Genau so ist er geworden.“</p><small>Beispiel · noch keine echte Bewertung</small></div>
 <div class="rev"><p>„Lücke um 16:30 per SMS bekommen, um 17:15 saß der Fade.“</p><small>Beispiel · noch keine echte Bewertung</small></div></div>
 <p class="demo-note" style="margin-top:20px">Dieser Musterbetrieb hat noch keine echten Bewertungen. Im echten Betrieb stehen hier Google-Note, Anzahl und Stand.</p>
</div></section>
</main>''' + foot()


def steps(items): return '<div class="steps">' + ''.join(f'<div><b>{a}</b><p>{b}</p></div>' for a, b in items) + '</div>'
def faq(items): return '<div class="faq">' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in items) + '</div>'


def sub(title, kick, h1, lead, img, body, desc):
    return head(f'{title} – {BRAND}', desc) + header(True) + f'''<main>
<section class="sub-hero"><div class="wrap"><a class="back" href="index.html#zurueck">Zurück zum Spiegel</a><br><span class="kick">{kick}</span><h1 class="disp">{h1}</h1><p class="lead">{lead}</p></div></section>
<div class="wrap"><div class="mirror sub-img rv">{pic(img, title)}</div></div>
<section class="blk" style="padding-top:50px"><div class="wrap">{body}
<p style="margin-top:40px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn" href="index.html#termin">Stuhl buchen</a><a class="btn ghost" href="index.html#zurueck">Zurück zum Spiegel</a></p></div></section></main>''' + foot(True)


def lookgrid(skip=None):
    return '<h2 class="disp" style="font-size:clamp(30px,3.4vw,48px);margin:50px 0 16px">Die vier Höhen</h2><div class="plist">' + ''.join(f'<a class="pcard" href="look-{k}.html" style="text-decoration:none;padding:0;overflow:hidden">{pic(k, n)}<div style="padding:16px 18px"><h3 style="margin:0">{n}</h3><p style="color:var(--mute);font-size:14px">Wann wieder: {w}</p></div></a>' for k, n, t, w in LOOKS if k != skip) + '</div>'


PAGES = {
 'fade': ('Fade', 'Leistung · Fade', 'Ohne Kante.', 'Low, Mid, High, Skin: was die Begriffe heißen und wie wir ohne sichtbare Stufe blenden.', 'clipper',
   steps([('Beratung', 'Im Spiegel zeigen wir dir, wo die Linie startet.'), ('Linie setzen', 'Erste Linie mit 0,5 mm auf der gewählten Höhe.'), ('Blenden', 'Aufsätze 1,5 / 3 / 6 mm, halbe Stufen mit dem Hebel.'), ('Finish', 'Line-up an Stirn und Schläfe, Nacken frei.')])
   + '<div class="prose"><h2>Skin Fade oder Taper?</h2><p>Ein Skin Fade geht bis auf die Haut und wirkt am schärfsten, wächst aber nach 2 Wochen sichtbar raus. Ein Taper bleibt an Schläfe und Nacken kurz, ohne Haut, und hält 3–4 Wochen.</p></div>' + lookgrid()
   + faq([('Wie oft sollte ich kommen?', 'Skin Fade alle 2 Wochen, Taper alle 3–4 Wochen.'), ('Mit Maschine oder Schere oben?', 'Beides, je nach Länge und Haar. Wir sagen es dir vorher.')]), 'Fade-Arten und Ablauf.'),
 'bart': ('Bart', 'Leistung · Bart', 'Bart mit Kante.', 'Form, Länge und eine Kontur, die zur Gesichtsform passt.', 'bart-nachher',
   steps([('Länge', 'Mit Aufsatz auf eine Länge, Kinn etwas länger für Form.'), ('Wange', 'Natürliche oder scharfe Linie, nie zu tief.'), ('Hals', 'Zwei Finger über dem Adamsapfel.'), ('Pflege', 'Bartöl, Bürste, Tipp für zu Hause.')])
   + faq([('Wie lang muss mein Bart für eine Form sein?', 'Ab etwa 4 Wochen Wachstum lässt sich eine Form schneiden.'), ('Macht ihr auch Färben?', 'Ja, Grauabdeckung für den Bart in 20 Minuten.')]), 'Bartpflege und Kontur.'),
 'kontur': ('Kontur', 'Leistung · Kontur', 'Saubere Linie.', 'Linien nachziehen zwischen zwei Schnitten, in 15 Minuten, ohne Waschen.', 'nachher',
   steps([('Line-up', 'Stirn und Schläfe gerade gezogen.'), ('Ohren', 'Bogen um das Ohr frei.'), ('Nacken', 'Rund, eckig oder ausgefadet.'), ('Finish', 'Foliendrehrasierer, Balsam.')])
   + '<div class="prose"><h2>Hygiene</h2><p>Aufsätze und Klingen werden nach jedem Kunden desinfiziert. Wo wir nass rasieren, nehmen wir Einwegklingen.</p></div>', 'Kontur und Line-up.'),
 'team': ('Barber', 'Team', 'Vier Spiegel.', 'Jeder hat seinen Stuhl, seinen Schwerpunkt und seine Stammkunden.', 'spiegelwand',
   steps([(n, r) for _, n, r in TEAM]) + '<div class="prose"><h2>Wie immer, beim selben Barber</h2><p>Beim Buchen merkt sich die Seite deinen letzten Schnitt und deinen Barber. Ein Tipp, gleicher Look.</p></div>', 'Die Barber.'),
 'akademie': ('Akademie', 'Akademie · Karriere', 'Dein Platz am Spiegel.', 'Ausbildung, Abendkurse, Jobs. Offen und ohne Kleingedrucktes.', 'akademie',
   steps([('Ausbildung', '3 Jahre Friseur mit Barber-Schwerpunkt, eigene Kunden ab dem 2. Jahr.'), ('Abendkurs', 'Jeden Mittwoch 18–21 Uhr: Fades, Bart, Kontur an Übungsköpfen.'), ('Meister', 'Meisterkurs bezahlt, danach zwei Jahre bei uns.'), ('Job', 'Barber mit Erfahrung: fester Stuhl, Stammkunden ab Tag eins.')])
   + '<div class="prose"><h2>Warum jetzt</h2><p>80.118 Friseursalons, aber nur 7.497 neue Ausbildungsverträge 2025. In NRW gibt es 40,6 % weniger Friseur-Azubis als 2014.</p><p style="font-size:13px">Quellen: ZV Friseurhandwerk PM 06/2026; Bezirksregierung Arnsberg. Stand 11/2026.</p></div><p><a class="btn" href="index.html#karriere">In 60 Sekunden bewerben</a></p>', 'Ausbildung und Jobs.'),
 'besuch': ('Besuch', 'Besuch', 'Komm vorbei.', 'Anfahrt, Parken, Walk-in-Zeiten.', 'feierabend',
   steps([('Bahn', 'U-Bahn Oststraße, 3 Minuten zu Fuß (Demo).'), ('Auto', 'Parkhaus gegenüber, erste Stunde frei für Kunden (Demo).'), ('Walk-in', 'Di – Fr 10 – 13 Uhr ohne Termin.'), ('Termin', 'Rund um die Uhr online.')]), 'Anfahrt und Öffnungszeiten.'),
}


def lookpage(k, n, t, w):
    wk = int(w.split('–')[-1].split()[0])
    body = steps([('Beratung', 'Höhe im Spiegel festlegen.'), ('Schnitt', t), ('Finish', 'Line-up und Nacken.'), ('Wann wieder?', f'Nach {w}.')])
    body += f'<p><button class="btn ghost" data-ics="{wk}" data-title="{BRAND}: {n} nachschneiden">Erinnerung in {wk} Wochen in den Kalender</button></p>' + lookgrid(k)
    return sub(n, 'Look', n + '.', t, k, body, f'{n} bei {BRAND}.')


if __name__ == '__main__':
    open(os.path.join(H, 'index.html'), 'w').write(index())
    for k, v in PAGES.items(): open(os.path.join(H, k + '.html'), 'w').write(sub(*v))
    for L in LOOKS: open(os.path.join(H, f'look-{L[0]}.html'), 'w').write(lookpage(*L))
    L = '<div class="prose"><p>{}</p></div>'
    open(os.path.join(H, 'impressum.html'), 'w').write(sub('Impressum', 'Rechtliches', 'Impressum', f'{BRAND} ist eine Demo-Webseite eines Musterbetriebs.', 'feierabend', L.format(f'Es gibt keinen echten Barbershop {BRAND}. Konzept und Umsetzung: Projekt EX, projektex.de. Alle Personen auf den Fotos sind KI-generiert. Adresse, Telefon, Termine und Bewertungen sind Beispiele.'), 'Impressum'))
    open(os.path.join(H, 'datenschutz.html'), 'w').write(sub('Datenschutz', 'Rechtliches', 'Datenschutz', 'Kurz: Diese Demo speichert nichts und sendet nichts.', 'feierabend', L.format('Schriften liegen auf diesem Server, keine Übertragung an Google. Keine Cookies, kein Tracking, keine Formularübermittlung. Hosting: GitHub Pages (GitHub Inc.) mit technisch notwendigen Server-Logs.'), 'Datenschutz'))
    print('ok', 3 + len(PAGES) + len(LOOKS), 'Seiten')
