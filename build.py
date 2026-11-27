#!/usr/bin/env python3
"""Barbershop – Seiten bauen. python3 build.py   (Markenname in BRAND)"""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); V = '27b'
BRAND = 'KANTE'
has = lambda k: os.path.exists(os.path.join(H, 'assets/img', k + '.webp'))
SEQ = json.load(open(os.path.join(H, 'assets/seq/seq.json'))) if os.path.exists(os.path.join(H, 'assets/seq/seq.json')) else None
NAV = [('Termin', '#buchen'), ('Looks', '#looks'), ('Team', 'team.html'), ('Akademie', '#akademie'), ('Besuch', '#besuch')]


def pic(key, alt, lazy=True, cls=''):
    if not has(key): return ''
    m = f'<source media="(max-width: 760px)" srcset="assets/img/{key}-m.webp">' if has(key + '-m') else ''
    return f'<picture class="{cls}">{m}<img src="assets/img/{key}.webp" alt="{alt}" {"loading=lazy" if lazy else "fetchpriority=high"} decoding="async"></picture>'


def head(title, desc, extra=''):
    return f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title><meta name="description" content="{desc}"><meta name="theme-color" content="#0b0b0b">
<link rel="preload" href="assets/fonts/anton-latin-1.woff2" as="font" type="font/woff2" crossorigin>{extra}
<link rel="stylesheet" href="assets/css/fonts.css?v={V}"><link rel="stylesheet" href="assets/css/style.css?v={V}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%230b0b0b'/%3E%3Crect x='6' y='14' width='20' height='4' fill='%23d4ff3a'/%3E%3C/svg%3E">
</head><body>'''


def header(sub=False):
    links = ''.join(f'<a href="{("index.html" + h) if sub and h.startswith("#") else h}">{t}</a>' for t, h in NAV)
    return f'''<header class="hd"><a class="logo" href="{"index.html" if sub else "#top"}" aria-label="{BRAND} Startseite"><i></i>{BRAND}</a>
<nav class="nav" id="nav">{links}<a class="btn" href="{"index.html" if sub else ""}#buchen">Stuhl buchen</a></nav>
<button class="burger" aria-label="Menü" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button></header>'''


def foot(sub=False):
    p = 'index.html' if sub else ''
    return f'''<footer class="ft" id="besuch">{pic('street', 'Barbershop bei Nacht von der Straße')}<div class="wrap">
<span class="kick lime">Besuch</span><h2 class="disp">Tür auf.<br>Stuhl frei.</h2>
<div class="grid"><div><p style="max-width:40ch;opacity:.85">Kölner Straße 88 · 40211 Düsseldorf (Demo-Adresse)<br>Telefon 0211 000 000 1 (Demo)</p><p style="margin-top:20px;display:flex;gap:10px;flex-wrap:wrap"><a class="btn" href="{p}#buchen">Stuhl buchen</a><a class="btn ghost" href="besuch.html">Anfahrt</a></p></div>
<div><span class="kick lime">Öffnungszeiten</span><div style="margin-top:10px"><div class="row"><span>Mo</span><span>zu</span></div><div class="row"><span>Di – Fr</span><span>10 – 20 Uhr</span></div><div class="row"><span>Sa</span><span>9 – 17 Uhr</span></div><div class="row"><span>Walk-in</span><span>Di – Fr 10 – 13 Uhr</span></div></div></div>
<div><span class="kick lime">Mehr</span><ul style="margin-top:6px"><li><a href="fade.html">Fade</a></li><li><a href="bart.html">Bart</a></li><li><a href="kontur.html">Kontur &amp; Rasur</a></li><li><a href="team.html">Team</a></li><li><a href="akademie.html">Akademie</a></li></ul></div></div>
<div class="fine"><span>{BRAND} ist eine Demo-Webseite eines Musterbetriebs. Formulare senden nichts, Termine sind Beispiele.</span><span><a href="impressum.html">Impressum</a> · <a href="datenschutz.html">Datenschutz</a></span></div></div></footer>
<div class="dlg" id="dlg-ok" role="dialog" aria-modal="true" aria-labelledby="dlg-t"><div class="box"><h3 id="dlg-t">Stuhl reserviert</h3><p></p><button class="btn dark" data-close>Alles klar</button></div></div>
<script src="assets/js/app.js?v={V}" defer></script></body></html>'''


LOOKS = [('look1', 'High Skin Fade', 'Kurz oben, Haut an den Seiten', '2 Wochen', ['High Fade von 0 auf 6 mm, Linie über der Kopfrundung', 'Oberkopf mit der Maschine, Kanten mit der Schere gebrochen', 'Kontur mit Foliendrehrasierer, matte Paste']),
         ('look2', 'Textured Crop', 'Pony, Low Taper', '3–4 Wochen', ['Oberkopf mit der Schere texturiert, kurzer Pony', 'Low Taper an Schläfe und Nacken', 'Puder für Volumen, mit den Fingern gestylt']),
         ('look3', 'Curly Drop Fade', 'Locken, Line-up', '2–3 Wochen', ['Locken trocken in Form geschnitten', 'Drop Fade, hinter dem Ohr tiefer gezogen', 'Line-up an Stirn und Schläfe, Curl-Creme']),
         ('look4', 'Buzz + Bart', 'Kurz rundum, voller Bart', '3 Wochen', ['Buzz Cut 6 mm rundum', 'Bart auf Länge, Kinn etwas länger', 'Wangen- und Halslinie scharf, Bartöl'])]
SVC = [('Haarschnitt', '45 Min.', 'Waschen, Schnitt, Styling', 'fade.html'), ('Skin Fade', '45 Min.', 'Fade bis auf die Haut', 'fade.html'), ('Haare &amp; Bart', '60 Min.', 'Schnitt plus Bart in einem', 'bart.html'),
       ('Bart', '30 Min.', 'Form, Länge, Kontur', 'bart.html'), ('Kontur &amp; Rasur', '20 Min.', 'Linien nachziehen, Nacken frei', 'kontur.html'), ('Jungs bis 14', '30 Min.', 'Schnitt für Kids', 'fade.html')]
TEAM = [('milan', 'Milan', 'Fade', 'team-milan'), ('yusuf', 'Yusuf', 'Bart', 'team-yusuf'), ('noah', 'Noah', 'Locken', 'team-noah'), ('ben', 'Ben', 'Meister · Akademie', 'team-ben')]


def index():
    seq = f' data-n="{SEQ["n"]}" data-seq="assets/seq/d/f_###.webp" data-seqm="assets/seq/m/f_###.webp"' if SEQ else ''
    pre = '<link rel="preload" as="image" href="assets/img/street.webp" media="(min-width: 761px)" fetchpriority="high"><link rel="preload" as="image" href="assets/img/street-m.webp" media="(max-width: 760px)" fetchpriority="high">'
    stills = ''.join(f'<div class="still s{i}">{pic(k, a, lazy=i > 0)}</div>' for i, (k, a) in enumerate([('street', 'Barbershop bei Nacht, Glastür, warmes Licht innen'), ('hall', 'Lange Betonhalle mit Lichtraster und schwarzen Stühlen'), ('chair', 'Barber blendet einen Skin Fade')]))
    looks = ''.join(f'<a class="blook rv" href="look-{k}.html" data-sub><figure>{pic(k, n)}</figure><b>{n}</b><small>{s}</small></a>' for k, n, s, *_ in LOOKS)
    mimgs = ''.join(f'<img src="assets/img/{k}.webp" alt="" loading="lazy" class="{"on" if i == 0 else ""}">' for i, k in enumerate(['chair', 'look1', 'team', 'akademie', 'street']) if has(k))
    bbs = ''.join(f'<button class="bb" data-b="{k}" data-name="{n}">{"<img src=assets/img/" + a + ".webp alt=" + n + " loading=lazy>" if has(a) else ""}{n}<small>{r}</small></button>' for k, n, r, a in TEAM)
    return head(f'{BRAND} – Barbershop', f'{BRAND}: Barbershop für Fade, Bart und Kontur. Stuhl online buchen, Barber wählen, Walk-in-Zeiten.', pre) + header() + f'''
<main id="top">
<section class="walk" aria-label="Von der Straße bis zum Stuhl">
 <div class="stage"{seq}>{stills}<canvas class="cv" aria-hidden="true"></canvas>
  <div class="corner c-tl wordset"><span class="kick" data-at="0-.4">Barbershop · Düsseldorf</span><span class="kick off" data-at=".4-.75">Zwölf Stühle · Beton · Licht</span><span class="kick off" data-at=".75-1.1">Stuhl 12 · Milan</span></div>
  <div class="corner c-tr"><span class="lime">● Heute offen</span><br>Walk-in Di – Fr 10 – 13</div>
  <div class="corner c-bl wordset"><div data-at="0-.36"><h1 class="disp">Ohne<br>Umweg.</h1><p>Scroll und komm rein. Von der Straße bis zum Stuhl.</p></div>
   <div class="off" data-at=".36-.72"><h2 class="disp">Zwölf Stühle.<br><span class="lime">Ein Anspruch.</span></h2></div>
   <div class="off" data-at=".72-1.1"><h2 class="disp">Der Fade<br>sitzt.</h2><p>Jeder Übergang freihand ausgeblendet. Ohne Kante, ohne Eile.</p></div></div>
  <div class="corner c-br"><span class="counter">000 %</span><a class="btn" href="#buchen">Stuhl buchen</a></div>
 </div>
</section>

<section class="blk light wipe" id="edit"><div class="wrap ed">
 <figure>{pic('clipper', 'Hand mit Haarschneidemaschine, schwarz-weiß')}</figure>
 <div><span class="kick">Seit Tag eins</span><h2 class="disp">Null<br>Kompromiss.</h2><p>Wir schneiden nur Männer – und das jeden Tag. Fade, Bart, Kontur. Keine Wartezeit ohne Ansage, keine Linie, die nach drei Tagen schief ist.</p><a class="btn dark" href="fade.html" data-sub>Wie wir faden</a></div>
</div></section>

<section class="blk menu" id="menu"><div class="wrap grid roll">
 <ul class="mlist"><li><a href="#buchen">Termin<small>01</small></a></li><li><a href="#looks">Looks<small>02</small></a></li><li><a href="team.html" data-sub>Team<small>03</small></a></li><li><a href="#akademie" class="lime">Akademie<small>04</small></a></li><li><a href="#besuch">Besuch<small>05</small></a></li></ul>
 <div class="mpic">{mimgs}</div>
</div></section>

<section class="blk light" id="looks"><div class="wrap">
 <div class="lhead"><h2 class="disp">Was wir<br>können.</h2><p style="max-width:40ch;color:var(--mute)">Vier Schnitte, die wir täglich machen. Tipp auf einen Look: Ablauf, Pflege, wann du wiederkommen solltest.</p></div>
 <div class="grid4">{looks}</div>
 <div class="fh"><svg viewBox="0 0 300 300" aria-hidden="true"><path d="M150 30c-60 0-100 44-100 100 0 30 8 52 20 70l6 50h120l10-38c22-4 40-20 42-46 2-20-6-34-18-44 2-50-30-92-80-92z" fill="none" stroke="#0b0b0b" stroke-width="3"/>
  <path class="zone" data-z="high" d="M62 150c0-30 10-55 30-72l130 6c10 20 12 40 10 66z"/><path class="zone on" data-z="mid" d="M58 168c0-6 1-12 4-18h170c0 6-1 12-3 18z"/><path class="zone" data-z="low" d="M60 186c-2-6-2-12-2-18h171c-1 6-3 12-5 18z"/>
  <line class="lvl" x1="40" y1="150" x2="260" y2="150"/><line class="lvl" x1="40" y1="168" x2="260" y2="168"/><line class="lvl" x1="40" y1="186" x2="260" y2="186"/></svg>
  <div><span class="kick">Fade-Höhe</span><h3>Mid Fade</h3><div class="seg" role="group" aria-label="Fade-Höhe"><button data-z="low">Low</button><button data-z="mid" class="on">Mid</button><button data-z="high">High</button></div><p class="fh-t" style="color:var(--mute);max-width:40ch">Auf Schläfenhöhe. Der Klassiker, sichtbar, aber nicht laut.</p></div></div>
 <h3 class="disp" style="font-size:clamp(40px,5vw,80px);margin-top:80px">Leistungen</h3><p style="color:var(--mute)">Dauer statt Preisliste – den Preis siehst du beim Buchen.</p>
 <div class="svc">{''.join(f'<a href="{u}" data-sub><b>{n}</b><span class="d">{d}</span><i>{t}</i></a>' for n, t, d, u in SVC)}</div>
</div></section>

<section class="blk light" id="buchen" style="padding-top:20px"><div class="wrap book">
 <div><span class="kick">Termin · 24/7</span><h2 class="disp">Dein<br>Stuhl.</h2><p style="color:var(--mute);max-width:40ch;margin:18px 0">Barber wählen, Zeit wählen, fertig. Kein Anruf, während die Maschine läuft.</p>
  <div><span class="kick">Jetzt im Laden · Beispiel</span><div class="chairs">{"<i></i>" * 12}</div><p style="font-size:14px"><b class="free-n">3</b> von 12 Stühlen frei · Walk-in lohnt sich</p></div></div>
 <div class="card" id="booking">
  <div class="again">{"<img src=assets/img/team-milan.webp alt=Milan>" if has("team-milan") else ""}<p><b>Wie immer?</b><br>Skin Fade bei Milan, nächster freier Termin.</p><button class="btn">Ein Tipp</button></div>
  <h3>1 · Leistung</h3><div class="opts">{''.join(f'<button class="opt" data-svc="{n.replace("&amp;", "&")}">{n}</button>' for n, *_ in SVC)}</div>
  <h3>2 · Barber</h3><div class="barbers">{bbs}</div>
  <h3>3 · Tag &amp; Zeit</h3><div class="days"></div><div class="slots"></div>
  <div class="sum"><p></p><button class="btn dark" disabled>Stuhl buchen</button></div>
  <p class="demo-note" style="margin-top:10px">Demo: Zeiten und Stuhlplan sind Beispiele, es wird nichts gebucht.</p>
 </div>
</div></section>

<section class="blk dark" id="akademie"><div class="wrap aka">
 <figure class="rv">{pic('akademie', 'Abendkurs in der Barber-Akademie: Azubis üben Fades an Übungsköpfen')}</figure>
 <div><span class="kick lime">Akademie · Karriere</span><div class="kin"><span>Barber</span><span>werden.</span><span>Bei uns.</span></div>
 <p style="opacity:.85;max-width:44ch;margin-top:18px">Ausbildung zum Friseur mit Barber-Schwerpunkt, Abendkurse jeden Mittwoch, Meister bezahlt. Und wir suchen Barber mit Erfahrung – feste Stammkunden ab Tag eins.</p>
 <a class="link" href="akademie.html" data-sub>Alles zur Akademie</a>
 <div class="apply"><span class="timer">60 s</span><h3>Bewerben in 60 Sekunden</h3><div class="prog60"><i></i></div>
  <div class="step on"><button class="btn dark" data-next>Los</button></div>
  <div class="step"><label>Was suchst du?</label><div class="opts">{''.join(f'<button class="opt" data-next>{t}</button>' for t in ['Ausbildung', 'Job als Barber', 'Abendkurs'])}</div></div>
  <div class="step"><form><label for="ap-n">Vorname</label><input id="ap-n" autocomplete="given-name" required><label for="ap-t">Handynummer</label><input id="ap-t" type="tel" autocomplete="tel" required><p style="margin-top:14px"><button class="btn dark" type="submit">Abschicken</button></p></form></div>
  <div class="step"><h3>Danke.</h3><p style="margin-top:8px;color:var(--mute)">Demo: Es wurde nichts gesendet. Im echten Betrieb meldet sich Ben innerhalb von 48 Stunden.</p></div></div>
 </div></div>
 <div class="wrap"><div class="nums">
  <div><b data-count="80118">0</b><p>Friseursalons in Deutschland Ende 2025 – 245 weniger als im Jahr davor.</p></div>
  <div><b data-count="7497">0</b><p>neue Ausbildungsverträge Friseur/-in 2025, bundesweit.</p></div>
  <div><b data-count="40.6" data-dec="1" data-pre="−" data-suf=" %">0</b><p>Friseur-Azubis in NRW seit 2014. Barber werden gebraucht.</p></div></div>
 <p class="src">Quellen: Zentralverband des Deutschen Friseurhandwerks, PM 06/2026 (Salons; Ausbildungsverträge nach BIBB); Bezirksregierung Arnsberg. Stand 11/2026.</p></div>
</section>

<section class="blk light" id="bewertungen"><div class="wrap"><span class="kick">Stimmen</span>
 <div class="revs"><div class="rev"><p>„Seit Monaten derselbe Barber, derselbe Schnitt. Ein Tipp und gebucht.“</p><small>Beispiel · noch keine echte Bewertung</small></div>
 <div class="rev"><p>„Walk-in um zehn, um halb elf saß der Fade.“</p><small>Beispiel · noch keine echte Bewertung</small></div>
 <div class="rev"><p>„Die Linie am Nacken hält wirklich zwei Wochen.“</p><small>Beispiel · noch keine echte Bewertung</small></div></div>
 <p style="color:var(--mute);font-size:14px;margin-top:20px">Dieser Musterbetrieb hat noch keine echten Bewertungen. Im echten Betrieb stehen hier Google-Note, Anzahl und Stand.</p>
</div></section>
</main>''' + foot()


def steps(items): return '<div class="steps">' + ''.join(f'<div><b>{a}</b><p>{b}</p></div>' for a, b in items) + '</div>'
def faq(items): return '<div class="faq">' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in items) + '</div>'


def sub(title, kick, h1, lead, img, body, desc):
    return head(f'{title} – {BRAND}', desc) + header(True) + f'''<main class="light">
<section class="sub-hero"><div class="wrap"><a class="back" href="index.html#zurueck">Zurück in die Halle</a><br><span class="kick">{kick}</span><h1 class="disp">{h1}</h1><p class="lead">{lead}</p></div></section>
<div class="wrap"><div class="sub-img rv">{pic(img, title)}</div></div>
<section class="blk" style="padding-top:50px"><div class="wrap">{body}
<p style="margin-top:40px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn dark" href="index.html#buchen">Stuhl buchen</a><a class="btn ghost" href="index.html#zurueck">Zurück in die Halle</a></p></div></section></main>''' + foot(True)


PAGES = {
 'fade': ('Fade', 'Leistung · Fade', 'Der Fade<br>sitzt.', 'Low, Mid, High, Drop, Skin: was die Begriffe heißen und wie wir ohne Kante blenden.', 'chair',
   steps([('Linie setzen', 'Fade-Höhe festlegen, erste Linie mit 0,5 mm.'), ('Blenden', 'Aufsätze 1,5 / 3 / 6 mm, halbe Stufen mit dem Hebel.'), ('Freihand', 'Schere über Kamm, Trimmer für die Übergänge.'), ('Kontur', 'Schläfe, Ohr, Nacken – mit dem Foliendrehrasierer.')])
   + '<div class="prose"><h2>Skin Fade oder Taper?</h2><p>Ein Skin Fade geht bis auf die Haut und wirkt am schärfsten, wächst aber nach 2 Wochen sichtbar raus. Ein Taper bleibt an Schläfe und Nacken kurz, ohne Haut – hält 3–4 Wochen.</p><h2>Drop Fade</h2><p>Die Linie fällt hinter dem Ohr ab und folgt der Kopfform. Gut bei flachem Hinterkopf.</p></div>'
   + faq([('Wie oft sollte ich kommen?', 'Skin Fade alle 2 Wochen, Taper alle 3–4 Wochen.'), ('Mit Maschine oder Schere oben?', 'Beides – je nach Länge und Haar. Wir sagen es dir vorher.')]), 'Fade-Arten und Ablauf.'),
 'bart': ('Bart', 'Leistung · Bart', 'Bart mit<br>Linie.', 'Form, Länge und eine Kontur, die zur Gesichtsform passt.', 'bart',
   steps([('Länge', 'Mit Aufsatz auf eine Länge, Kinn länger für Form.'), ('Wange', 'Natürliche oder scharfe Linie, nie zu tief.'), ('Hals', 'Zwei Finger über dem Adamsapfel.'), ('Pflege', 'Bartöl, Bürste, Tipp für zu Hause.')])
   + faq([('Wie lang muss mein Bart für eine Form sein?', 'Ab etwa 4 Wochen Wachstum lässt sich eine Form schneiden.'), ('Macht ihr auch Färben?', 'Ja, Grauabdeckung für den Bart in 20 Minuten.')]), 'Bartpflege und Kontur.'),
 'kontur': ('Kontur & Rasur', 'Leistung · Kontur', 'Saubere<br>Kante.', 'Linien nachziehen zwischen zwei Schnitten – in 20 Minuten, ohne Waschen.', 'rasur',
   steps([('Line-up', 'Stirn und Schläfe gerade gezogen.'), ('Ohren', 'Bogen um das Ohr frei.'), ('Nacken', 'Rund, eckig oder ausgefadet.'), ('Finish', 'Foliendrehrasierer, Aftershave-Balsam.')])
   + '<div class="prose"><h2>Hygiene</h2><p>Aufsätze und Klingen werden nach jedem Kunden desinfiziert. Wo wir nass rasieren, nehmen wir Einwegklingen.</p></div>', 'Kontur und Rasur.'),
 'team': ('Team', 'Team', 'Vier<br>Barber.', 'Jeder hat seinen Stuhl, seinen Schwerpunkt – und seine Stammkunden.', 'team',
   steps([(n, r) for _, n, r, _ in TEAM]) + '<div class="prose"><h2>Wie immer – beim selben Barber</h2><p>Beim Buchen merkt sich die Seite deinen letzten Schnitt und deinen Barber. Ein Tipp, gleicher Look.</p></div>', 'Die Barber.'),
 'akademie': ('Akademie', 'Akademie · Karriere', 'Barber<br>werden.', 'Ausbildung, Abendkurse, Jobs. Offen und ohne Kleingedrucktes.', 'akademie',
   steps([('Ausbildung', '3 Jahre Friseur mit Barber-Schwerpunkt, eigene Kunden ab dem 2. Jahr.'), ('Abendkurs', 'Jeden Mittwoch 18–21 Uhr: Fades, Bart, Kontur an Übungsköpfen.'), ('Meister', 'Meisterkurs bezahlt, danach zwei Jahre bei uns.'), ('Job', 'Barber mit Erfahrung: fester Stuhl, Stammkunden ab Tag eins.')])
   + '<div class="prose"><h2>Warum jetzt</h2><p>80.118 Friseursalons, aber nur 7.497 neue Ausbildungsverträge 2025. In NRW gibt es 40,6 % weniger Friseur-Azubis als 2014.</p><p style="font-size:13px">Quellen: ZV Friseurhandwerk PM 06/2026; Bezirksregierung Arnsberg. Stand 11/2026.</p></div><p><a class="btn dark" href="index.html#akademie">In 60 Sekunden bewerben</a></p>', 'Ausbildung und Jobs.'),
 'besuch': ('Besuch', 'Besuch', 'Tür auf.<br>Stuhl frei.', 'Anfahrt, Parken, Walk-in-Zeiten.', 'hall',
   steps([('Bahn', 'U-Bahn Oststraße, 3 Minuten zu Fuß (Demo).'), ('Auto', 'Parkhaus gegenüber, erste Stunde frei für Kunden (Demo).'), ('Walk-in', 'Di – Fr 10 – 13 Uhr ohne Termin.'), ('Termin', 'Rund um die Uhr online.')]), 'Anfahrt und Öffnungszeiten.'),
}


def lookpage(k, n, s, rhythm, how):
    wk = int(rhythm.split('–')[-1].split()[0])
    body = steps([(f'Schritt {i + 1}', h) for i, h in enumerate(how)] + [('Wann wieder?', f'Nach {rhythm}.')])
    body += f'<p><button class="btn dark" data-ics="{wk}" data-title="{BRAND}: {n} nachschneiden">Erinnerung in {wk} Wochen in den Kalender</button></p>'
    body += '<h2 class="disp" style="font-size:clamp(36px,4vw,64px);margin-top:50px">Andere Looks</h2><div class="grid4">' + ''.join(f'<a class="blook" href="look-{k2}.html"><figure>{pic(k2, n2)}</figure><b>{n2}</b><small>{s2}</small></a>' for k2, n2, s2, *_ in LOOKS if k2 != k) + '</div>'
    return sub(n, 'Look', n + '.', s + '. Ablauf, Pflege und Rhythmus.', k, body, f'{n} bei {BRAND}.')


if __name__ == '__main__':
    open(os.path.join(H, 'index.html'), 'w').write(index())
    for k, v in PAGES.items(): open(os.path.join(H, k + '.html'), 'w').write(sub(*v))
    for L in LOOKS: open(os.path.join(H, f'look-{L[0]}.html'), 'w').write(lookpage(*L))
    L = '<div class="prose"><p>{}</p></div>'
    open(os.path.join(H, 'impressum.html'), 'w').write(sub('Impressum', 'Rechtliches', 'Impressum', f'{BRAND} ist eine Demo-Webseite eines Musterbetriebs.', 'hall', L.format(f'Es gibt keinen echten Barbershop {BRAND}. Konzept und Umsetzung: Projekt EX, projektex.de. Alle Personen auf den Fotos sind KI-generiert. Adresse, Telefon, Termine und Bewertungen sind Beispiele.'), 'Impressum'))
    open(os.path.join(H, 'datenschutz.html'), 'w').write(sub('Datenschutz', 'Rechtliches', 'Datenschutz', 'Kurz: Diese Demo speichert nichts und sendet nichts.', 'hall', L.format('Schriften liegen auf diesem Server, keine Übertragung an Google. Keine Cookies, kein Tracking, keine Formularübermittlung. Hosting: GitHub Pages (GitHub Inc.) mit technisch notwendigen Server-Logs.'), 'Datenschutz'))
    print('ok', 3 + len(PAGES) + len(LOOKS), 'Seiten')
