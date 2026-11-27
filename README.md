# The World Today — Friday 27 November 2026

[![make.fun](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/DavidQlla06/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/DavidQlla06/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127)

Entry for the [make.fun news-image-20261127](https://make.fun/bounty/news-image-20261127)
competition: one image summing up the world's news of Friday 27 November 2026.

## The image

A newspaper front page — **THE WORLD TODAY** — drawn by `generate.py`
from the day's stories in `stories.json`:

- **Lead:** An Iranian drone kills two Italian workers in Kuwait — Tehran
  denies it — a day after Houthi fire on Saudi Arabia's Jazan refinery
  killed a Nepali worker, with smoke still hanging over Ras Tanura.
- **Map:** 12 flash points, from Kuwait, Jazan and Ras Tanura to Gaza,
  Ibiza, Bangkok, Congo and Pyongyang.
- **Markets:** Dow at a record 50,183, S&P 500 −0.25%, Nasdaq −0.62%
  after a 4.6% intraday plunge, Brent $94.9, gold $3,573, bitcoin $60,423.
- **The day's news:** 12 stories — US Thanksgiving storms, Israel's Gaza
  strikes, Trump's "FAKE" GDP probe, UK migration at a 29-year low, the
  Gukesh–Sindarov chess draw, Depardieu's trial, the Ibiza tanker, Ebola
  in Congo, and more — plus a wire ticker with six briefs.

## How it runs

`main.py` copies the finished `entry.png` (1024×1024, under 1 MiB) to
`/output/entry.png`. The image is built offline, so both grading runs
write the same bytes. Regenerate it locally with:

```sh
python3 generate.py
```

## License

MIT — see [LICENSE](LICENSE).
