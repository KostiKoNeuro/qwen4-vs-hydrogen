# Qwen4-Max vs Gemini 4 Hydrogen: race, voxel diorama, channel intro

Alibaba's new flagship against Google's new fast coder. The same short prompts, maximum reasoning for both. No hints from me: each model writes, runs and checks its own work.

**▶ Play in your browser:** https://kostikoneuro.github.io/qwen4-vs-hydrogen/
**🎬 Video (Russian):** (link after release)
**💬 Telegram:** https://t.me/kostik_neuro

> Русский: все игры и диорамы можно открыть прямо в браузере по ссылке выше. Промпты в папке [`prompts/`](prompts/).

## The tests

| # | Test | Qwen4-Max | Gemini 4 Hydrogen |
|---|---|---|---|
| 1 | **Neon Night Racer**: 80s arcade racer in the browser | [play](1-race/qwen4/) | [play](1-race/hydrogen/) |
| 2 | **Night market voxel diorama** in Shenzhen: 30-second fly-through, `C` = free camera | [open](2-diorama/qwen4/) | [open](2-diorama/hydrogen/) |
| 3 | **Channel intro**: 10 s, the model studies the channel by itself and makes the intro in [OpenMontage](https://github.com/calesthio/OpenMontage); $10 for everything | [video](3-intro/qwen4.mp4) | [video](3-intro/hydrogen.mp4) |

Controls in the race: Qwen4-Max: Enter = start, arrows / AD = steer (auto throttle), ↓ = brake, Space = nitro, P = pause, M = sound. Hydrogen: Enter or Space = start, ↑ / W = throttle, arrows / AD = steer, ↓ / S = brake, Space or Shift = nitro, Esc = car select.

## Time and cost

Price from the tokens each model used: official list per 1M tokens Qwen4-Max $1.50 in / $4.50 out, Gemini 4 Hydrogen $1.50 in / $7.50 out; through CometAPI 20% less. Time is the model's working time from the prompt to its last answer; minutes spent waiting on a hung server or on the API provider are not counted.

| Test | Qwen4-Max | Gemini 4 Hydrogen |
|---|---|---|
| 1 Race | 25 min · $0.79 list / $0.63 CometAPI | 50 min · $5.80 list / $4.64 CometAPI |
| 2 Diorama | 39 min · $1.32 list / $1.05 CometAPI | 44 min · $2.92 list / $2.33 CometAPI |
| 3 Intro | 102 min · $3.57 list / $2.94 CometAPI (assets $0.40) | 66 min · $10.18 list / $8.37 CometAPI (assets $1.11) |
| **Total** | **167 min · $5.67 list / $4.62 CometAPI** | **160 min · $18.89 list / $15.34 CometAPI** |



## How it was run

- Each model works as an autonomous agent in a fresh session with the same prompt and checks its own work in a browser. No personal instructions, no hints.
- Reasoning at the top level each model offers: `xhigh` for both. $10 per model per test, everything included. 1 prompt + at most 1 short fix in words.
- Prices are computed from the tokens each model used: the official list price and the CometAPI price (20% lower). Test 3 assets (music, sound effects, voice, images) were paid through CometAPI.
