"""Собирает index.html страницы «Qwen4-Max vs Gemini 4 Hydrogen» в стиле «Журнал Pro» (как gpt-6-2-sol-solo).

Цифры — только из ДАННЫЕ_ДЛЯ_МОНТАЖА.md трёх тестов (вписаны ниже в DATA).
Тест 2 вслепую: на странице «Вариант 1 / Вариант 2», ответ — по кнопке. Когда Костя разрешит раскрыть сразу,
поставь BLIND = False и пересобери:  python _src/build.py
"""
import base64, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLIND = True
REPO = "https://github.com/KostiKoNeuro/qwen4-vs-hydrogen"

M = {
    "q": {"name": "Qwen4-Max", "maker": "Alibaba", "logo": "media/logos/qwen.png"},
    "h": {"name": "Gemini 4 Hydrogen", "maker": "Google", "logo": "media/logos/gemini.png"},
}
# время работы модели (м:с) и цены $ официально / через CometAPI — из ДАННЫЕ_ДЛЯ_МОНТАЖА.md
DATA = {
    1: {"q": ("25:18", 0.79, 0.63, None), "h": ("50:12", 5.80, 4.64, None)},
    2: {"q": ("39:18", 1.32, 1.05, None), "h": ("43:48", 2.92, 2.33, None)},
    3: {"q": ("102:18", 3.57, 2.94, 0.40), "h": ("65:48", 10.18, 8.37, 1.11)},
}
TOTAL = {"q": ("2:46:54", 5.68, 4.62), "h": ("2:39:48", 18.90, 15.34)}   # суммы строк DATA (так же в ролике: $5,68 / $18,90)
BLIND_MAP = {"1": "q", "2": "h"}   # _logs/blind_map.json: "02": ["qwen4", "hyd"]


def rl(ru, en):
    return f'<span class="l-ru">{ru}</span><span class="l-en">{en}</span>'


def usd(x):
    return rl(f"${x:.2f}".replace(".", ","), f"${x:.2f}")


def mins(t):
    """'102:18' -> секунды"""
    p = [int(v) for v in t.split(":")]
    return sum(v * 60 ** i for i, v in enumerate(reversed(p)))


def clock(t):
    s = mins(t)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else t


def bar(v, mx):
    return f'<div class="mbar"><i style="width:{v / mx * 100:.1f}%"></i></div>'


def metrics(n, k, extra_time=""):
    t, off, comet, assets = DATA[n][k]
    o = DATA[n]["h" if k == "q" else "q"]
    tmax, pmax = max(mins(t), mins(o[0])), max(off, o[1])
    a = f' · {rl("ассеты", "assets")} {usd(assets)}' if assets else ""
    return f'''<div class="metrics">
      <div class="metric"><small>{rl("Время работы", "Working time")}</small><b>{clock(t)}</b>{bar(mins(t), tmax)}{f"<em>{extra_time}</em>" if extra_time else ""}</div>
      <div class="metric"><small>{rl("Цена официально", "List price")}</small><b>{usd(off)}</b>{bar(off, pmax)}<em>{rl("через CometAPI", "via CometAPI")} {usd(comet)}{a}</em></div>
    </div>'''


def who(k):
    m = M[k]
    return f'<div class="who"><img src="{m["logo"]}" alt=""><div>{m["name"]}<small>{m["maker"]}</small></div></div>'


def prompt_block(n, file):
    text = html.escape((ROOT / "prompts" / file).read_text(encoding="utf-8").strip())
    return f'''<details class="prompt mini"><summary><span>{rl("Промпт теста", "The prompt")} · {rl("одинаковый для обеих", "same for both")}</span></summary>
    <p class="pnote">{rl("Дословно, как получили модели.", "Verbatim, in Russian, exactly as both models got it.")}</p>
    <div class="ptext">{text}</div></details>'''


def head_block(n, icon, meta, title, text):
    return f'''<div class="test-head">
    <div class="num">0{n}<img src="media/icons/{icon}.png" alt=""></div>
    <div><div class="meta">{meta}</div><h3>{title}</h3><p>{text}</p></div>
  </div>'''


def test1():
    notes = {
        "q": rl("Холмы, 4 полосы, тайм-атака с чекпоинтами, near-miss комбо до ×10, нитро до 422 км/ч, слоу-мо при аварии. Сам играл в свою игру ботом-автопилотом и починил двойной бип отсчёта.",
                "Hills, 4 lanes, a checkpoint time attack, near-miss combos up to ×10, nitro up to 422 km/h, slow-mo crashes. It played its own game with an autopilot bot and fixed a double countdown beep."),
        "h": rl("Выбор машины, телеметрия аварии, слипстрим, предупреждение о встречке, горы на горизонте. Игру в браузере открыл всего 2 раза, проверял в основном чтением кода.",
                "Car select, crash telemetry, slipstream, an oncoming-traffic warning, mountains on the horizon. It opened the game in a browser only twice and checked mostly by reading the code."),
    }
    keys = {
        "q": rl("<kbd>Enter</kbd> старт · <kbd>←</kbd><kbd>→</kbd> / <kbd>A</kbd><kbd>D</kbd> руль, газ сам · <kbd>↓</kbd> тормоз · <kbd>Space</kbd> нитро · <kbd>P</kbd> пауза · <kbd>M</kbd> звук",
                "<kbd>Enter</kbd> start · <kbd>←</kbd><kbd>→</kbd> / <kbd>A</kbd><kbd>D</kbd> steer, auto throttle · <kbd>↓</kbd> brake · <kbd>Space</kbd> nitro · <kbd>P</kbd> pause · <kbd>M</kbd> sound"),
        "h": rl("<kbd>Enter</kbd> или <kbd>Space</kbd> старт · <kbd>↑</kbd> / <kbd>W</kbd> газ · <kbd>←</kbd><kbd>→</kbd> / <kbd>A</kbd><kbd>D</kbd> руль · <kbd>↓</kbd> / <kbd>S</kbd> тормоз · <kbd>Space</kbd> или <kbd>Shift</kbd> нитро · <kbd>Esc</kbd> выбор машины",
                "<kbd>Enter</kbd> or <kbd>Space</kbd> start · <kbd>↑</kbd> / <kbd>W</kbd> throttle · <kbd>←</kbd><kbd>→</kbd> / <kbd>A</kbd><kbd>D</kbd> steer · <kbd>↓</kbd> / <kbd>S</kbd> brake · <kbd>Space</kbd> or <kbd>Shift</kbd> nitro · <kbd>Esc</kbd> car select"),
    }
    extra = {"q": "", "h": rl("по часам 1:32:42: минус 6 мин зависшего вызова и 36 мин ожидания провайдера", "1:32:42 on the clock, minus a 6-min stalled call and 36 min waiting on the provider")}
    path = {"q": "1-race/qwen4/", "h": "1-race/hydrogen/"}
    sides = "".join(f'''
    <div class="side {k}">
      {who(k)}
      <a class="shot" data-local href="{path[k]}"><img src="media/race-{k}.jpg" alt=""></a>
      {metrics(1, k, extra[k])}
      <p class="note">{notes[k]}</p>
      <p class="keys">{keys[k]}</p>
      <div class="cta"><a class="btn" data-local href="{path[k]}">{rl("Играть", "Play")} ↗</a></div>
    </div>''' for k in "qh")
    return f'''<article class="test" id="race">
  {head_block(1, "stopwatch", rl("Тест 01 / 03 · браузерная игра", "Test 01 / 03 · browser game"),
              rl("Спидран: Neon Night Racer", "Speedrun: Neon Night Racer"),
              rl("Аркадная гонка в духе 80-х по одному промпту: неоновый город, трафик, нитро, synthwave кодом. Кто соберёт быстрее и дешевле, и в какую интереснее играть.",
                 "An 80s arcade racer from one prompt: a neon city, traffic, nitro, synthwave written in code. Who builds it faster and cheaper, and which one is more fun to play."))}
  <div class="duel">{sides}
  </div>
  {prompt_block(1, "1-race.md")}
</article>'''


BLIND_MAP3 = {"1": "q", "2": "h"}   # _logs/blind_map.json: "03": ["qwen4", "hyd"]; = «Заставка 1/2» в ролике и у SMM


def blind_side(maps, v, label, media, notes, cta=""):
    k = maps[v]
    enc = base64.b64encode(f"{k}|{M[k]['name']}|{M[k]['maker']}|{M[k]['logo']}".encode()).decode()
    head = who(k) if not BLIND else f'<div class="who"><div>{label} {v}<small>{rl("модель скрыта", "model hidden")}</small></div></div>'
    return f'''
    <div class="side {k if not BLIND else "b"}" data-v="{enc}">
      {head}
      {media}
      <p class="note">{notes[v]}</p>
      {cta}
    </div>'''


def blind_bar(n, maps, word_ru, word_en):
    bymodel = "".join(f'''<div class="{k}"><span class="nm">{M[k]["name"]}</span>{clock(DATA[n][k][0])} · {usd(DATA[n][k][1])} <small>· CometAPI {usd(DATA[n][k][2])}{f" · {rl('ассеты', 'assets')} {usd(DATA[n][k][3])}" if DATA[n][k][3] else ""}</small></div>''' for k in "qh")
    ans = rl(f"{word_ru} 1 — {M[maps['1']]['name']}, {word_ru.lower()} 2 — {M[maps['2']]['name']}.",
             f"{word_en} 1 is {M[maps['1']]['name']}, {word_en.lower()} 2 is {M[maps['2']]['name']}.")
    return f'''<div class="blindbar">
    <div><div class="lbl">{rl("Замеры по моделям", "Numbers by model")}</div><div class="bymodel stack">{bymodel}</div></div>
    <button type="button" class="btn ghost reveal"{" hidden" if not BLIND else ""}>{rl("Показать ответ", "Show the answer")}</button>
    <p class="answer"{" hidden" if BLIND else ""}>{ans}</p>
  </div>'''


def test2():
    notes = {
        "1": rl("6 ларьков: лапша, бао, шашлычки, фрукты, чай, пиво. Воки с паром, качающиеся фонарики, мокрый асфальт с отражениями, скутер с водителем, около 18 человечков.",
                "6 stalls: noodles, bao, skewers, fruit, tea, beer. Steaming woks, swinging lanterns, wet asphalt with reflections, a scooter with a rider, about 18 little people."),
        "2": rl("Ворота 夜市, неоновые вывески с bloom, вок с пламенем, мангал с устрицами и искрами, аквариумы, автомат с напитками, рыжий кот, два скутера с фарами в лужах.",
                "A 夜市 gate, neon signs with bloom, a flaming wok, an oyster grill with sparks, fish tanks, a drinks machine, a ginger cat, two scooters whose headlights hit the puddles."),
    }
    sides = "".join(blind_side(BLIND_MAP, v, rl("Вариант", "Variant"),
                               f'''<a class="shot" data-local href="2-diorama/{v}/"><img src="media/d{v}.jpg" alt=""></a>''', notes,
                               f'''<div class="cta"><a class="btn" data-local href="2-diorama/{v}/">{rl("Открыть", "Open")} ↗</a></div>''')
                    for v in "12")
    return f'''<article class="test" id="diorama">
  {head_block(2, "poll", rl("Тест 02 / 03 · Three.js · вслепую", "Test 02 / 03 · Three.js · blind"),
              rl("Ночной рынок Шэньчжэня", "Shenzhen night market"),
              rl("Воксельная диорама: улица после дождя, всё из кубиков, всё кодом. При открытии 30-секундный облёт, клавиша <kbd>C</kbd> — свободная камера. Чья где, не говорю: сначала угадайте сами.",
                 "A voxel diorama: a street after the rain, all cubes, all code. A 30-second fly-through on open, press <kbd>C</kbd> for a free camera. I won't say which is which: guess first."))}
  <div class="duel">{sides}
  </div>
  {blind_bar(2, BLIND_MAP, "Вариант", "Variant")}
  {prompt_block(2, "2-diorama.md")}
</article>'''


def test3():
    notes = {
        "1": rl("«Тест 2» канала синей ручкой в тетради: семечка, линейка, домино, будильник будит хомяка-ботаника, тот кричит «Всем вайбкод-привет!», печать «10/10». Графика кодом, нейросети только для звука.",
                "The channel's “Test 2” drawn in blue pen in a notebook: a seed, a ruler, dominoes, an alarm wakes the nerdy hamster, he shouts a greeting, a “10/10” stamp. Graphics in code, AI only for sound."),
        "2": rl("Машина Голдберга на миллиметровке: импульс от промпта бежит к звонку, но за миллиметр до удара музыка обрывается — «ХОМЯК ВСЁ ЕЩЁ СПИТ!». Шутка про мой прошлый соло-тест.",
                "A Goldberg machine on graph paper: the prompt's pulse runs to the bell, but a millimetre before the hit the music stops: “THE HAMSTER IS STILL ASLEEP!” A joke about one of my earlier solo tests."),
    }
    sides = "".join(blind_side(BLIND_MAP3, v, rl("Заставка", "Intro"),
                               f'<video src="3-intro/{v}.mp4" poster="media/i{v}.jpg" controls playsinline preload="none"></video>', notes)
                    for v in "12")
    return f'''<article class="test" id="intro">
  {head_block(3, "appfile", rl("Тест 03 / 03 · OpenMontage · вслепую", "Test 03 / 03 · OpenMontage · blind"),
              rl("Заставка канала", "Channel intro"),
              rl("Модель сама изучает мой канал и делает 10-секундную заставку в OpenMontage. $10 на всё: токены, музыка, звуки, голос, картинки. Чья где, не говорю: голосуем в Telegram, какая заставка будет открывать мои ролики.",
                 "The model studies my channel on its own and makes a 10-second intro in OpenMontage. $10 for everything: tokens, music, sounds, voice, images. I won't say which is which: vote in my Telegram for the intro that will open my videos."))}
  <div class="duel">{sides}
  </div>
  {blind_bar(3, BLIND_MAP3, "Заставка", "Intro")}
  {prompt_block(3, "3-intro.md")}
</article>'''


def table():
    names = {1: rl("Спидран: гонка", "Speedrun: racer"), 2: rl("Ночной рынок", "Night market"), 3: rl("Заставка канала", "Channel intro")}
    rows = ""
    for n in (1, 2, 3):
        cells = ""
        for k in "qh":
            t, off, comet, assets = DATA[n][k]
            a = f'<br><small>{rl("ассеты", "assets")} {usd(assets)}</small>' if assets else ""
            cells += f'<td class="sep">{clock(t)}</td><td>{usd(off)}{a}</td><td>{usd(comet)}</td>'
        rows += f'<tr><th scope="row"><a href="#{["race", "diorama", "intro"][n - 1]}"><span class="n">0{n}</span>{names[n]}</a></th>{cells}</tr>'
    foot = "".join(f'<td class="sep">{TOTAL[k][0]}</td><td>{usd(TOTAL[k][1])}</td><td>{usd(TOTAL[k][2])}</td>' for k in "qh")
    sub = f'<th scope="col" class="sep">{rl("Время", "Time")}</th><th scope="col">{rl("Официально", "List")}</th><th scope="col">CometAPI</th>'
    mob = ""
    for k in "qh":
        r = ""
        for n in (1, 2, 3):
            t, off, comet, assets = DATA[n][k]
            a = "*" if assets else ""
            r += f'<tr><th scope="row"><span class="n">0{n}</span>{names[n]}</th><td>{clock(t)}</td><td>{usd(off)}{a}</td><td>{usd(comet)}{a}</td></tr>'
        mob += f'''<table><thead><tr><th colspan="4" class="g {k}">{M[k]["name"]}</th></tr>
      <tr><th scope="col">{rl("Тест", "Test")}</th><th scope="col">{rl("Время", "Time")}</th><th scope="col">{rl("Офиц.", "List")}</th><th scope="col">CometAPI</th></tr></thead>
      <tbody>{r}</tbody><caption>* {rl("с ассетами", "incl. assets")} {usd(DATA[3][k][3])}</caption><tfoot><tr><th scope="row">{rl("Итого", "Total")}</th><td>{TOTAL[k][0]}</td><td>{usd(TOTAL[k][1])}</td><td>{usd(TOTAL[k][2])}</td></tr></tfoot></table>'''
    return f'''<div class="mtables">{mob}</div><div class="table-wrap wide"><table>
    <thead><tr><th></th><th colspan="3" class="g q sep">Qwen4-Max</th><th colspan="3" class="g h sep">Gemini 4 Hydrogen</th></tr>
    <tr><th scope="col">{rl("Тест", "Test")}</th>{sub}{sub}</tr></thead>
    <tbody>{rows}</tbody>
    <tfoot><tr><th scope="row">{rl("Итого", "Total")}</th>{foot}</tr></tfoot>
  </table></div>'''


def hero():
    tots = "".join(f'''
    <div class="tot" style="--mc:var(--{k})">
      {who(k).replace('class="who"><img', 'class="who"><img').replace("<small>", '<small style="display:none">')}
      <div class="nums"><div><small>{rl("время", "time")}</small>{TOTAL[k][0]}{bar(mins(TOTAL[k][0]), mins(TOTAL["q"][0]))}</div><div><small>{rl("официально", "list price")}</small>{usd(TOTAL[k][1])}{bar(TOTAL[k][1], TOTAL["h"][1])}</div></div>
      <div class="sub">{rl("через CometAPI", "via CometAPI")} {usd(TOTAL[k][2])}</div>
    </div>''' for k in "qh")
    return f'''<section class="hero">
  <div class="hero-main">
    <div class="kicker"><span class="n">00</span><i></i>{rl("Дуэль моделей · 20.11.2026", "Model duel · 20.11.2026")}</div>
    <h1 class="duel-h1"><span class="mq">Qwen4-Max</span><em>vs</em><span class="mh">Gemini 4 Hydrogen</span></h1>
    <p class="lead">{rl("Новый флагман Alibaba против нового быстрого кодера Google. Три задания: аркадная гонка, ночной рынок из кубиков и заставка для моего канала. Одинаковые короткие промпты, максимум размышлений, никаких подсказок: каждая модель сама пишет, запускает и проверяет. Всё можно потыкать прямо здесь.",
                         "Alibaba's new flagship against Google's new fast coder. Three tasks: an arcade racer, a voxel night market and an intro for my channel. The same short prompts, maximum reasoning, no hints: each model writes, runs and checks its own work. Try every result right here.")}</p>
    <p class="mverdict"><b>{rl("×3,3", "×3.3")}</b> {rl("— во столько Qwen4-Max дешевле, по времени почти поровну.", "— that's how much cheaper Qwen4-Max is; the time is nearly even.")} <a href="#numbers">{rl("Замеры", "Numbers")} ↓</a></p>
  </div>
  <aside class="duelcard">
    <div class="cap">{rl("Итог трёх тестов", "Three tests in total")}</div>{tots}
    <div class="verdict"><b>{rl("×3,3", "×3.3")}</b><span>{rl("во столько Qwen4-Max дешевле. По времени почти поровну.", "that's how much cheaper Qwen4-Max is. The time is nearly even.")}</span></div>
  </aside>
</section>'''


def stats():
    s = [("terminal", "xhigh", rl("максимум размышлений у обеих моделей", "top reasoning level for both models")),
         ("appfile", rl("1 промпт", "1 prompt"), rl("и не больше одной правки словами", "and at most one fix in words")),
         ("coin", "$10", rl("бюджет на прогон, всё включено", "budget per run, everything included")),
         ("monitors", rl("сама", "on its own"), rl("модель сама запускает и проверяет результат", "the model runs and checks its own result"))]
    return '<section class="stats">' + "".join(f'<div class="stat"><div class="v"><img src="media/icons/{i}.png" alt="">{v}</div><p>{p}</p></div>' for i, v, p in s) + "</section>"


JS = """<script>
for(const b of document.querySelectorAll('.reveal'))b.addEventListener('click',()=>{const t=b.closest('.test');
 for(const s of t.querySelectorAll('.side[data-v]')){const[k,name,maker,logo]=atob(s.dataset.v).split('|');
  s.classList.remove('b');s.classList.add(k);s.querySelector('.who').innerHTML='<img src="'+logo+'" alt=""><div>'+name+'<small>'+maker+'</small></div>';}
 b.hidden=true;t.querySelector('.answer').hidden=false;});
</script>"""


def page():
    title_ru, title_en = "Qwen4-Max vs Gemini 4 Hydrogen: три теста", "Qwen4-Max vs Gemini 4 Hydrogen: three tests"
    desc = "Дуэль Qwen4-Max и Gemini 4 Hydrogen: аркадная гонка, воксельный ночной рынок вслепую и заставка канала. Время и цена каждого теста, всё можно открыть в браузере."
    return f'''<!doctype html>
<html lang="ru" class="ru" data-title-ru="{title_ru}" data-title-en="{title_en}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title_ru}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title_ru}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://kostikoneuro.github.io/qwen4-vs-hydrogen/media/race-q.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F4EDE1">
<link rel="icon" href="media/icons/hamster.png">
<script src="assets/lang.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Unbounded:wght@800&family=Manrope:wght@500;700;800&display=swap">
<link rel="stylesheet" href="assets/site.css">
</head>
<body><main>
<header class="top">
  <a class="brand" href="https://www.youtube.com/@kosti_neuro" target="_blank" rel="noopener">
    <img src="media/icons/hamster.png" alt="">
    <span><b>Ботанутый Костя</b><small>{rl("тесты нейросетей · YouTube", "AI model tests · YouTube")}</small></span>
  </a>
  <nav class="chips">
    <div class="lang" role="group" aria-label="Язык / Language"><button type="button" data-set-lang="ru" aria-pressed="true">RU</button><button type="button" data-set-lang="en" aria-pressed="false">EN</button></div>
    <a class="chip" href="https://t.me/kostik_neuro" target="_blank" rel="noopener"><img src="media/icons/plane.png" alt="">Telegram</a>
    <a class="chip" href="{REPO}" target="_blank" rel="noopener"><img src="media/icons/folder.png" alt="">GitHub</a>
  </nav>
</header>
{hero()}
{stats()}

<section class="section" id="tests">
  <div class="kicker"><span class="n">01-03</span><i></i>{rl("Потыкай сам", "Try it yourself")}</div>
  <h2>{rl("Три теста, <em>в браузере</em>", "Three tests, <em>in your browser</em>")}</h2>
  <div class="rows">
{test1()}
{test2()}
{test3()}
  </div>
</section>

<section class="section" id="numbers">
  <div class="kicker"><span class="n">04</span><i></i>{rl("Замеры", "Numbers")}</div>
  <h2>{rl("Время и <em>деньги</em>", "Time and <em>cost</em>")}</h2>
  {table()}
  <p class="small">{rl("Время — работа модели от промпта до последнего ответа; минуты, когда висел запущенный моделью сервер или провайдер не отвечал, не считаем. Цена — по токенам, которые потратила каждая модель, по публичному прайсу за 1 млн: Qwen4-Max $1,50 вход / $4,50 выход, Gemini 4 Hydrogen $1,50 / $7,50; через CometAPI на 20% дешевле. В тесте 3 в цену входят ассеты (музыка, звуки, голос, картинки), оплаченные через CometAPI.",
                         "Time is the model's working time from the prompt to its last answer; minutes when a server the model started hung or the provider did not answer are not counted. Price is from the tokens each model used at the public list price per 1M: Qwen4-Max $1.50 in / $4.50 out, Gemini 4 Hydrogen $1.50 / $7.50; 20% less via CometAPI. Test 3 includes assets (music, sounds, voice, images) paid through CometAPI.")}</p>
</section>
<section class="tg"><img src="media/icons/plane.png" alt="">
<div><b>@kostik_neuro</b><p>{rl("Кто какой вариант, голосования и новые тесты нейросетей — в Telegram-канале.", "Blind-test answers, polls and new AI model tests in my Telegram channel.")}</p></div>
<a class="btn or" href="https://t.me/kostik_neuro" target="_blank" rel="noopener">{rl("Подписаться", "Subscribe")} ↗</a></section>
<footer><span>© Ботанутый Костя · Qwen4-Max vs Gemini 4 Hydrogen · 20.11.2026</span><span><a href="https://www.youtube.com/@kosti_neuro">YouTube</a> · <a href="https://t.me/kostik_neuro">Telegram</a> · <a href="{REPO}">GitHub</a></span></footer>
</main>
{JS}
</body></html>
'''


if __name__ == "__main__":
    (ROOT / "index.html").write_text(page(), encoding="utf-8", newline="\n")
    print("index.html собран, BLIND =", BLIND)
