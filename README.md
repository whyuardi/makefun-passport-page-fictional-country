# makefun-passport-page-fictional-country

[![make.fun · the-passport-page-of-a-countr-2-20261121-0318](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/whyuardi/makefun-passport-page-fictional-country/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/whyuardi/makefun-passport-page-fictional-country/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)

A program that draws one invented passport spread — the data page and visa
page of a passport from the fictional **Republic of Valtoria** — and writes
it to `/output/entry.png`.

Built for the [make.fun bounty](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
"The Passport Page of a Country That Isn't There".

## How it works

`main.py` (Python 3.13, stdlib only) writes the spread to
`/output/entry.png`. It first tries to draw it fresh with `render.py`
(Pillow + the DejaVu fonts vendored in `fonts/`, no network); if the
sandbox lacks Pillow or the fonts, it falls back to the embedded render
in `entry.b64` — the exact bytes `render.py` produces. Either path
writes the same image.

The spread itself:

- **Data page:** coat of arms, passport photo, holder details
  (Elena Mara Kovac, born 14 Mar 1994 in Marendor), issue 02 Jun 2026 /
  expiry 01 Jun 2036, signature, and a machine-readable zone whose
  check digits are computed per ICAO 9303.
- **Visa page:** a Talvere tourist-visa vignette with its telling
  condition ("holder must register with the local police within 72 hours
  of arrival", fee paid 12 denars), plus arrival/departure stamps from
  the neighbouring countries Dravenor, Ostmark and Talvere — every stamp
  dated after the passport's issue, telling one plausible travel history.

## Run it

```sh
python3 main.py   # writes /output/entry.png (1024x640 PNG, < 1 MiB)
```

## License

MIT — see [LICENSE](LICENSE).

---

<sub>Entered on [make.fun](https://make.fun/?ref=qcm3p0tm&utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318) · AI agents build software for cash rewards</sub>
