/* Barbershop – Reinlaufen. Keine Abhängigkeiten. */
(() => {
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fq = new URLSearchParams(location.search).get('farbe');
  if (fq) { const [b, a] = fq.split(','); const rgb = h => [0, 2, 4].map(i => parseInt(h.substr(i, 2), 16)).join(', '); const st = document.documentElement.style;
    if (b) { st.setProperty('--bg', '#' + b); st.setProperty('--bg-rgb', rgb(b)); } if (a) { st.setProperty('--or', '#' + a); st.setProperty('--or-rgb', rgb(a)); } }

  // Kopfzeile: dunkel über dunklen, hell über hellen Abschnitten
  const hd = $('.hd');
  const onHd = () => { if (!hd) return; const y = hd.offsetHeight / 2; const el = document.elementsFromPoint(innerWidth / 2, y + 1).find(e => !hd.contains(e)); const light = el && el.closest('.light'); hd.classList.toggle('on-light', !!light); hd.classList.toggle('solid', scrollY > 30 && !light); };
  addEventListener('scroll', onHd, { passive: true }); addEventListener('load', onHd); onHd();
  $('.burger')?.addEventListener('click', () => { const o = document.body.classList.toggle('menu-open'); $('.burger').setAttribute('aria-expanded', o); });
  $$('.nav a').forEach(a => a.addEventListener('click', () => document.body.classList.remove('menu-open')));

  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: .2 });
  $$('.rv, .kin, .ed, .roll').forEach(el => io.observe(el));
  const fmt = (v, d) => v.toLocaleString('de-DE', { minimumFractionDigits: d, maximumFractionDigits: d });
  const cio = new IntersectionObserver(es => es.forEach(e => { if (!e.isIntersecting) return; cio.unobserve(e.target); const el = e.target, to = +el.dataset.count, d = +(el.dataset.dec || 0), pre = el.dataset.pre || '', suf = el.dataset.suf || ''; if (reduce) { el.textContent = pre + fmt(to, d) + suf; return; } const t0 = performance.now(); const tick = t => { const k = clamp((t - t0) / 1600, 0, 1); el.textContent = pre + fmt(to * (1 - Math.pow(1 - k, 3)), d) + suf; if (k < 1) requestAnimationFrame(tick); }; requestAnimationFrame(tick); }), { threshold: .5 });
  $$('[data-count]').forEach(el => cio.observe(el));

  // ---------- Reinlaufen: Film per Scroll (Bildfolge) oder Standbild-Fahrt ----------
  const walk = $('.walk');
  if (walk) {
    const stage = $('.stage', walk), cv = $('canvas.cv', walk), ctx = cv.getContext('2d'), stills = $$('.still', walk).filter(s => $('img', s));
    const sets = $$('[data-at]', walk); let mob = innerWidth < 760;
    const N = +(stage.dataset.n || 0), pat = () => stage.dataset[mob ? 'seqm' : 'seq']; const frames = [];
    if (N && pat()) for (let i = 0; i < N; i++) { const im = new Image(); im.decoding = 'async'; if (i === 0) im.onload = () => { stage.classList.add('seq'); draw(true); }; im.src = pat().replace('###', String(i).padStart(3, '0')); frames.push(im); }
    const size = () => { const r = devicePixelRatio > 1 ? 1.5 : 1; cv.width = Math.round(innerWidth * r); cv.height = Math.round(innerHeight * r); };
    let p = 0, last = -1;
    function draw(force) {
      if (!frames.length) return; let i = clamp(Math.round(p * (N - 1)), 0, N - 1); while (i > 0 && !frames[i].complete) i--;
      if (i === last && !force) return; last = i; const f = frames[i]; if (!f.naturalWidth) return;
      const W = cv.width, H = cv.height, s = Math.max(W / f.naturalWidth, H / f.naturalHeight), w = f.naturalWidth * s, h = f.naturalHeight * s;
      ctx.drawImage(f, (W - w) / 2, (H - h) / 2, w, h);
    }
    size(); addEventListener('resize', () => { mob = innerWidth < 760; size(); draw(true); });
    const upd = () => {
      const r = walk.getBoundingClientRect(), total = walk.offsetHeight - innerHeight; p = clamp(-r.top / total, 0, 1);
      if (!stage.classList.contains('seq')) {
        // Standbild-Fahrt: Straße → Halle → Stuhl, jedes Bild zoomt auf die Tür / den Gang zu
        const seg = stills.length === 3 ? [[0, .42], [.36, .76], [.7, 1]] : stills.length === 2 ? [[0, .55], [.5, 1]] : [[0, 1]];
        stills.forEach((s, i) => { const [a, b] = seg[i]; const k = clamp((p - a) / (b - a), 0, 1); const fadeIn = i === 0 ? 1 : clamp((p - a) / .06, 0, 1); const fadeOut = i === stills.length - 1 ? 1 : clamp((b - p) / .06, 0, 1); s.style.opacity = Math.min(fadeIn, fadeOut); $('img', s).style.transform = `scale(${1 + k * (i === 2 ? .12 : .55)})`; });
      } else draw();
      sets.forEach(el => { const [a, b] = el.dataset.at.split('-').map(Number); el.classList.toggle('off', !(p >= a && p < b)); });
      const cnt = $('.counter', walk); if (cnt) cnt.textContent = String(Math.round(p * 100)).padStart(3, '0') + ' %';
    };
    addEventListener('scroll', () => requestAnimationFrame(upd), { passive: true }); upd();
    if (!reduce && scrollY < 10) { let t0; const auto = t => { t0 = t0 || t; const k = (t - t0) / 1800; if (k < 1 && scrollY < 10) { const q = Math.sin(k * Math.PI) * .05; if (stage.classList.contains('seq')) { p = q; draw(); } else if (stills[0]) $('img', stills[0]).style.transform = `scale(${1 + q * 8 * .55})`; requestAnimationFrame(auto); } }; setTimeout(() => requestAnimationFrame(auto), 700); }
  }

  // Wisch-Übergang dunkel → hell
  const wp = $('.wipe');
  if (wp) addEventListener('scroll', () => { const r = wp.getBoundingClientRect(); wp.style.setProperty('--w', clamp(r.top / (innerHeight * .8), 0, 1)); }, { passive: true });

  // Menü: Hover tauscht Foto
  const ml = $$('.mlist a'), mp = $$('.mpic img');
  ml.forEach((a, i) => { const on = () => { ml.forEach(x => x.classList.toggle('on', x === a)); mp.forEach((m, j) => m.classList.toggle('on', j === i)); }; a.addEventListener('mouseenter', on); a.addEventListener('focus', on); });

  // Fade-Höhe
  const fh = $('.fh');
  if (fh) { const T = { low: ['Low Fade', 'Beginnt knapp über dem Ohr. Dezent, wächst unauffällig raus – bürotauglich.'], mid: ['Mid Fade', 'Auf Schläfenhöhe. Der Klassiker, sichtbar, aber nicht laut.'], high: ['High Fade', 'Bis zur Kopfrundung. Starker Kontrast, braucht alle 2 Wochen Pflege.'] };
    $$('.seg button', fh).forEach(b => b.addEventListener('click', () => { $$('.seg button', fh).forEach(x => x.classList.toggle('on', x === b)); $$('.zone', fh).forEach(z => z.classList.toggle('on', z.dataset.z === b.dataset.z)); $('h3', fh).textContent = T[b.dataset.z][0]; $('.fh-t', fh).textContent = T[b.dataset.z][1]; })); }

  // ---------- Buchen (Beispiel) ----------
  const bk = $('#booking');
  if (bk) {
    const st = { svc: null, bb: null, day: null, slot: null }; const days = $('.days', bk), slots = $('.slots', bk), sum = $('.sum p', bk), go = $('.sum .btn', bk);
    const wd = ['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa'], now = new Date(); let h = '';
    for (let i = 0, n = 0; n < 7; i++) { const d = new Date(now); d.setDate(now.getDate() + i); if (d.getDay() === 0 || d.getDay() === 1) continue; h += `<button class="opt" data-d="${d.toISOString().slice(0, 10)}">${i === 0 ? 'Heute' : wd[d.getDay()]}<small>${d.getDate()}.${d.getMonth() + 1}.</small></button>`; n++; }
    days.innerHTML = h;
    const times = ['10:00', '10:30', '11:00', '11:30', '12:00', '13:00', '13:30', '14:00', '15:00', '16:00', '17:30', '19:00'];
    const rs = () => { let x = 0; for (const c of (st.day || '') + (st.bb || '')) x = (x * 31 + c.charCodeAt(0)) >>> 0; slots.innerHTML = times.map((t, i) => `<button class="opt" ${(((x >> (i % 24)) & 3) === 0 || (x + i * 5) % 4 === 0) ? 'disabled' : ''} data-t="${t}">${t}</button>`).join(''); $$('button', slots).forEach(b => b.addEventListener('click', () => { $$('button', slots).forEach(y => y.classList.toggle('on', y === b)); st.slot = b.dataset.t; sync(); })); };
    const sync = () => { const n = st.bb ? $(`.bb[data-b="${st.bb}"]`, bk).dataset.name : 'egal wer'; sum.innerHTML = `<b>${st.svc || 'Leistung wählen'}</b> · ${n}${st.day ? ' · ' + new Date(st.day).toLocaleDateString('de-DE', { weekday: 'short', day: 'numeric', month: 'numeric' }) : ''}${st.slot ? ' · ' + st.slot : ''}`; const ok = st.svc && st.day && st.slot; go.toggleAttribute('disabled', !ok); go.style.opacity = ok ? 1 : .45; };
    const pick = (sel, key, attr, after) => $$(sel, bk).forEach(b => b.addEventListener('click', () => { $$(sel, bk).forEach(x => x.classList.toggle('on', x === b)); st[key] = b.dataset[attr]; after && after(); sync(); }));
    pick('[data-svc]', 'svc', 'svc'); pick('.bb', 'bb', 'b', () => { st.slot = null; rs(); }); pick('.days .opt', 'day', 'd', () => { st.slot = null; rs(); });
    $('.again .btn', bk)?.addEventListener('click', () => { $(`[data-svc="Skin Fade"]`, bk)?.click(); $('.bb[data-b="milan"]', bk)?.click(); $('.days .opt', bk)?.click(); const f = $('.slots .opt:not([disabled])', bk); f && f.click(); });
    const lk = new URLSearchParams(location.search).get('look'); if (lk) { const b = $(`[data-svc="${lk}"]`, bk); b && b.click(); }
    rs(); sync();
    go.addEventListener('click', () => { if (go.hasAttribute('disabled')) return; $('#dlg-ok p').innerHTML = `${sum.innerHTML}.<br>Demo – es wurde nichts gebucht. Im echten Betrieb kommt jetzt eine SMS, 24 h vorher eine Erinnerung.`; $('#dlg-ok').classList.add('on'); });
    // Live-Stuhlplan (Beispiel): wechselt alle paar Sekunden
    const ch = $$('.chairs i'); const fr = $('.free-n'); const tickC = () => { let n = 0; ch.forEach(c => { const f = Math.random() < .28; c.className = f ? 'free' : 'busy'; n += f; }); if (fr) fr.textContent = n; }; if (ch.length) { tickC(); setInterval(tickC, 6000); }
  }
  $$('.dlg').forEach(d => d.addEventListener('click', e => { if (e.target === d || e.target.closest('[data-close]')) d.classList.remove('on'); }));
  addEventListener('keydown', e => { if (e.key === 'Escape') $$('.dlg.on').forEach(d => d.classList.remove('on')); });

  const ap = $('.apply');
  if (ap) { const steps = $$('.step', ap), bar = $('.prog60 i', ap), tm = $('.timer', ap); let t0, iv; const show = i => { steps.forEach((s, j) => s.classList.toggle('on', j === i)); bar.style.width = (i / (steps.length - 1) * 100) + '%'; if (!t0 && i > 0) { t0 = Date.now(); iv = setInterval(() => tm.textContent = Math.max(0, 60 - Math.round((Date.now() - t0) / 1000)) + ' s', 500); } if (i === steps.length - 1) clearInterval(iv); };
    $$('[data-next]', ap).forEach(b => b.addEventListener('click', () => show(steps.indexOf(b.closest('.step')) + 1))); $('form', ap)?.addEventListener('submit', e => { e.preventDefault(); show(steps.length - 1); }); }

  const revs = $$('.rev'); if (revs.length) { let i = 0; revs[0].classList.add('on'); setInterval(() => { revs[i].classList.remove('on'); i = (i + 1) % revs.length; revs[i].classList.add('on'); }, 5000); }


  // Kalender-Erinnerung „Wann wieder?“ (.ics, lokal erzeugt)
  $$('[data-ics]').forEach(b => b.addEventListener('click', () => {
    const d = new Date(); d.setDate(d.getDate() + 7 * +b.dataset.ics); const z = n => String(n).padStart(2, '0');
    const day = `${d.getFullYear()}${z(d.getMonth() + 1)}${z(d.getDate())}`;
    const ics = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Demo//DE', 'BEGIN:VEVENT', 'UID:' + Date.now() + '@demo', 'DTSTAMP:' + day + 'T090000', 'DTSTART;VALUE=DATE:' + day, 'SUMMARY:' + b.dataset.title, 'END:VEVENT', 'END:VCALENDAR'].join('\r\n');
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([ics], { type: 'text/calendar' })); a.download = 'erinnerung.ics'; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 2000);
  }));
  $$('a[data-sub]').forEach(a => a.addEventListener('click', () => { try { sessionStorage.setItem('bb-back', JSON.stringify({ y: scrollY })); } catch (e) {} }));
  if (location.hash === '#zurueck') { try { const s = JSON.parse(sessionStorage.getItem('bb-back') || 'null'); if (s) { history.replaceState(null, '', location.pathname); requestAnimationFrame(() => scrollTo(0, s.y)); } } catch (e) {} }
})();
