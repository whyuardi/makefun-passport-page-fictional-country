# The Passport Page of a Country That Isn't There

[![make.fun bounty](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A program that draws one invented passport spread — the data page and visa
page of a passport from the fictional **Republic of Valtoria** — and writes
it to `/output/entry.png`.

Built for the [make.fun bounty](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
"The Passport Page of a Country That Isn't There".

## How it works

`main.py` (Python 3.13, Pillow only, no network) draws the spread
deterministically with PIL:

- **Data page:** coat of arms, passport photo, holder details
  (Elena Mara Kovac, born 14 Mar 1994 in Marendor), issue 02 Jun 2026 /
  expiry 01 Jun 2036, signature, and a machine-readable zone whose
  check digits are computed per ICAO 9303.
- **Visa page:** a Talvere tourist-visa vignette with its telling
  condition ("holder must register with the local police within 72 hours
  of arrival", fee paid 12 denars), plus arrival/departure stamps from
  the neighbouring countries Dravenor, Ostmark and Talvere — every stamp
  dated after the passport's issue, telling one plausible travel history.

## Run

```sh
python3 main.py   # writes /output/entry.png (1024x640 PNG, < 1 MiB)
```

## License

MIT — see [LICENSE](LICENSE).
