# Report Violazioni GDPR – Cookie Consent Compliance

**Data analisi**: 2026-02-22 13:52  
**Siti analizzati**: 8  
**Fonte tracker list**: Disconnect.me (Advertising, Analytics, Social, Fingerprinting)  
**Definizione cookie non necessari**: cookie il cui eTLD+1 è diverso dal sito visitato

---

## Tabella Riassuntiva

| Sito | V1 – Cookie pre-consenso | V2 – Tracker pre-consenso | V3 – Post-rifiuto |
|------|--------------------------|---------------------------|-------------------|
| mail.ru | 27 cookie | 4 tracker | **SÌ** |
| aws.amazon.com/it | 5 cookie | 1 tracker | **SÌ** |
| microsoft.com | 8 cookie | 1 tracker | **SÌ** |
| facebook.com | 0 cookie | 1 tracker | **SÌ** |
| cloudflare.com | 0 cookie | 1 tracker | **SÌ** |
| youtube.com | 1 cookie | 0 tracker | **SÌ** |
| apple.com | 0 cookie | 0 tracker | No |
| instagram.com | 0 cookie | 1 tracker | **SÌ** |

---

## V1 – Cookie Non Necessari Prima del Consenso

> Cookie di terze parti rilevati nel crawl **baseline**,
> ossia prima di qualsiasi interazione con il banner di consenso.

### https://mail.ru

| Cookie | Host | Scadenza | HttpOnly | SameSite |
|--------|------|----------|----------|----------|
| `zencookie` | `.dzen.ru` | 2027-03-22 | No | unspecified |
| `prcl` | `.vk.com` | 2026-02-16 | Sì | unspecified |
| `remixlang` | `.vk.com` | 2027-02-17 | No | unspecified |
| `remixlns` | `.vk.com` | 2026-02-15 | No | unspecified |
| `remixstlid` | `.vk.com` | 2027-02-15 | No | unspecified |
| `prcl` | `.vkvideo.ru` | 2026-02-16 | Sì | unspecified |
| `remixstlid` | `.vkvideo.ru` | 2027-02-15 | No | unspecified |
| `_yasc` | `.yandex.com` | 2027-03-22 | No | unspecified |
| `bh` | `.yandex.com` | 2027-03-22 | No | no_restriction |
| `i` | `.yandex.com` | 2027-03-22 | Sì | no_restriction |
| `yandexuid` | `.yandex.com` | 2027-03-22 | No | no_restriction |
| `ymex` | `.yandex.com` | 2027-02-15 | No | no_restriction |
| `yuidss` | `.yandex.com` | 2027-02-15 | No | no_restriction |
| `_yasc` | `.yandex.ru` | 2027-03-22 | No | unspecified |
| `bh` | `.yandex.ru` | 2027-03-22 | No | no_restriction |
| `gdpr_popup` | `.yandex.ru` | session | No | unspecified |
| `i` | `.yandex.ru` | 2027-03-22 | Sì | no_restriction |
| `is_gdpr` | `.yandex.ru` | 2027-03-22 | No | no_restriction |
| `is_gdpr_b` | `.yandex.ru` | 2027-03-22 | No | no_restriction |
| `metrika_enabled` | `.yandex.ru` | session | No | unspecified |
| `yandex_gid` | `.yandex.ru` | 2026-03-17 | No | no_restriction |
| `yandexuid` | `.yandex.ru` | 2027-03-22 | No | no_restriction |
| `yashr` | `.yandex.ru` | 2027-02-15 | Sì | no_restriction |
| `yp` | `.yandex.ru` | 2027-03-22 | No | no_restriction |
| `yuidss` | `.yandex.ru` | 2027-03-22 | No | no_restriction |
| `yabs-sid` | `mc.yandex.com` | session | No | no_restriction |
| `tstc` | `ok6-5.vkuser.net` | 2027-03-22 | Sì | unspecified |

### https://aws.amazon.com/it/

| Cookie | Host | Scadenza | HttpOnly | SameSite |
|--------|------|----------|----------|----------|
| `VISITOR_INFO1_LIVE` | `.youtube.com` | 2026-08-14 | Sì | no_restriction |
| `VISITOR_PRIVACY_METADATA` | `.youtube.com` | 2026-08-14 | Sì | no_restriction |
| `YSC` | `.youtube.com` | session | Sì | no_restriction |
| `__Secure-ROLLOUT_TOKEN` | `.youtube.com` | 2026-08-14 | Sì | no_restriction |
| `__Secure-YNID` | `.youtube.com` | 2026-08-14 | Sì | no_restriction |

### https://microsoft.com

| Cookie | Host | Scadenza | HttpOnly | SameSite |
|--------|------|----------|----------|----------|
| `MSPBack` | `.login.live.com` | session | No | no_restriction |
| `MSPRequ` | `.login.live.com` | session | Sì | no_restriction |
| `OParams` | `.login.live.com` | session | Sì | no_restriction |
| `uaid` | `.login.live.com` | session | Sì | no_restriction |
| `esctx-QXpj6dzU1as` | `.login.microsoftonline.com` | 2026-02-15 | Sì | no_restriction |
| `fpc` | `login.microsoftonline.com` | 2026-03-17 | Sì | no_restriction |
| `stsservicecookie` | `login.microsoftonline.com` | session | Sì | no_restriction |
| `x-ms-gateway-slice` | `login.microsoftonline.com` | session | Sì | no_restriction |

### https://facebook.com

*Nessun cookie di terze parti rilevato.*

### https://cloudflare.com

*Nessun cookie di terze parti rilevato.*

### https://youtube.com

| Cookie | Host | Scadenza | HttpOnly | SameSite |
|--------|------|----------|----------|----------|
| `__Host-GAPS` | `accounts.google.com` | 2027-03-22 | Sì | unspecified |

### https://apple.com

*Nessun cookie di terze parti rilevato.*

### https://instagram.com

*Nessun cookie di terze parti rilevato.*

---

## V2 – Contatto con Tracker Prima del Consenso

> Richieste HTTP verso domini classificati come tracker (Disconnect.me)
> rilevate nel crawl **baseline**, prima di qualsiasi azione di consenso.

### https://mail.ru

- `yadro.ru` (Advertising)
- `mail.ru` (Social)
- `userapi.com` (Social)
- `vk.com` (Social)

### https://aws.amazon.com/it/

- `omtrdc.net` (Advertising)

### https://microsoft.com

- `clarity.ms` (Analytics)

### https://facebook.com

- `facebook.com` (Fingerprinting)

### https://cloudflare.com

- `cloudflareinsights.com` (Analytics)

### https://youtube.com

*Nessun tracker contattato.*

### https://apple.com

*Nessun tracker contattato.*

### https://instagram.com

- `facebook.com` (Fingerprinting)

---

## V3 – Persistenza Dopo il Rifiuto del Consenso

> Attività di tracking rilevata nel crawl **rejected**,
> ovvero dopo che l'utente ha esplicitamente negato il consenso.

### https://mail.ru

**Violazione V3 rilevata.**

**Cookie di terze parti impostati dopo il rifiuto:**

| Cookie | Host | Scadenza | HttpOnly | SameSite |
|--------|------|----------|----------|----------|
| `__cmpconsents1` | `.consentmanager.net` | 2026-03-06 | No | no_restriction |
| `__cmpcpcs1` | `.consentmanager.net` | 2026-03-06 | No | no_restriction |
| `__cmpcvcs1` | `.consentmanager.net` | 2026-03-06 | No | no_restriction |
| `zencookie` | `.dzen.ru` | 2027-03-27 | No | unspecified |
| `prcl` | `.vk.com` | 2026-02-21 | Sì | unspecified |
| `remixlang` | `.vk.com` | 2027-02-27 | No | unspecified |
| `remixlns` | `.vk.com` | 2026-02-20 | No | unspecified |
| `remixstlid` | `.vk.com` | 2027-02-20 | No | unspecified |
| `prcl` | `.vkvideo.ru` | 2026-02-21 | Sì | unspecified |
| `remixstlid` | `.vkvideo.ru` | 2027-02-20 | No | unspecified |
| `bh` | `.yandex.com` | 2027-03-27 | No | no_restriction |
| `i` | `.yandex.com` | 2027-03-27 | Sì | no_restriction |
| `yandexuid` | `.yandex.com` | 2027-03-27 | No | no_restriction |
| `ymex` | `.yandex.com` | 2027-02-20 | No | no_restriction |
| `yuidss` | `.yandex.com` | 2027-02-20 | No | no_restriction |
| `_yasc` | `.yandex.ru` | 2027-03-27 | No | unspecified |
| `bh` | `.yandex.ru` | 2027-03-27 | No | no_restriction |
| `gdpr_popup` | `.yandex.ru` | session | No | unspecified |
| `i` | `.yandex.ru` | 2027-03-27 | Sì | no_restriction |
| `is_gdpr` | `.yandex.ru` | 2027-03-27 | No | no_restriction |
| `is_gdpr_b` | `.yandex.ru` | 2027-03-27 | No | no_restriction |
| `metrika_enabled` | `.yandex.ru` | session | No | unspecified |
| `yandex_gid` | `.yandex.ru` | 2026-03-22 | No | no_restriction |
| `yandexuid` | `.yandex.ru` | 2027-03-27 | No | no_restriction |
| `yashr` | `.yandex.ru` | 2027-02-20 | Sì | no_restriction |
| `yp` | `.yandex.ru` | 2027-03-27 | No | no_restriction |
| `yuidss` | `.yandex.ru` | 2027-03-27 | No | no_restriction |
| `yabs-sid` | `mc.yandex.com` | session | No | no_restriction |

**Tracker contattati dopo il rifiuto:**

- `yadro.ru` (Advertising)
- `google-analytics.com` (Analytics)
- `mail.ru` (Social)
- `userapi.com` (Social)
- `vk.com` (Social)

### https://aws.amazon.com/it/

**Violazione V3 rilevata.**

**Cookie di terze parti impostati dopo il rifiuto:**

| Cookie | Host | Scadenza | HttpOnly | SameSite |
|--------|------|----------|----------|----------|
| `VISITOR_INFO1_LIVE` | `.youtube.com` | 2026-08-19 | Sì | no_restriction |
| `VISITOR_PRIVACY_METADATA` | `.youtube.com` | 2026-08-19 | Sì | no_restriction |
| `YSC` | `.youtube.com` | session | Sì | no_restriction |
| `__Secure-ROLLOUT_TOKEN` | `.youtube.com` | 2026-08-19 | Sì | no_restriction |

**Tracker contattati dopo il rifiuto:**

- `omtrdc.net` (Advertising)

### https://microsoft.com

**Violazione V3 rilevata.**

**Cookie di terze parti impostati dopo il rifiuto:**

| Cookie | Host | Scadenza | HttpOnly | SameSite |
|--------|------|----------|----------|----------|
| `MSPBack` | `.login.live.com` | session | No | no_restriction |
| `MSPRequ` | `.login.live.com` | session | Sì | no_restriction |
| `OParams` | `.login.live.com` | session | Sì | no_restriction |
| `uaid` | `.login.live.com` | session | Sì | no_restriction |
| `esctx-AlYEGhbG7K4` | `.login.microsoftonline.com` | session | Sì | no_restriction |
| `fpc` | `login.microsoftonline.com` | 2026-03-22 | Sì | no_restriction |
| `stsservicecookie` | `login.microsoftonline.com` | session | Sì | no_restriction |
| `x-ms-gateway-slice` | `login.microsoftonline.com` | session | Sì | no_restriction |

**Tracker contattati dopo il rifiuto:**

- `clarity.ms` (Analytics)

### https://facebook.com

**Violazione V3 rilevata.**

**Cookie di terze parti impostati dopo il rifiuto:**

*Nessun cookie di terze parti rilevato.*

**Tracker contattati dopo il rifiuto:**

- `facebook.com` (Fingerprinting)

### https://cloudflare.com

**Violazione V3 rilevata.**

**Cookie di terze parti impostati dopo il rifiuto:**

*Nessun cookie di terze parti rilevato.*

**Tracker contattati dopo il rifiuto:**

- `cloudflareinsights.com` (Analytics)

### https://youtube.com

**Violazione V3 rilevata.**

**Cookie di terze parti impostati dopo il rifiuto:**

| Cookie | Host | Scadenza | HttpOnly | SameSite |
|--------|------|----------|----------|----------|
| `__Host-GAPS` | `accounts.google.com` | 2027-03-27 | Sì | unspecified |

**Tracker contattati dopo il rifiuto:**

*Nessun tracker contattato.*

### https://apple.com

*Nessuna violazione V3 rilevata.*

### https://instagram.com

**Violazione V3 rilevata.**

**Cookie di terze parti impostati dopo il rifiuto:**

*Nessun cookie di terze parti rilevato.*

**Tracker contattati dopo il rifiuto:**

- `facebook.com` (Fingerprinting)

---

## Note Metodologiche

- **Cookie non necessari** (V1, V3): cookie il cui eTLD+1 host differisce dall'eTLD+1 del sito visitato. Identificati con la libreria `tldextract` (Public Suffix List).
- **Domini tracker** (V2, V3): domini presenti nella lista Disconnect.me nelle categorie Advertising, Analytics, Social, Fingerprinting. Il confronto avviene sul `registered_domain`.
- I cookie sono deduplicati per `(host, nome)` — viene mantenuta l'ultima occorrenza nel log.
- I crawl sono separati (baseline, rejected, accepted): non è disponibile un timestamp preciso dell'interazione con il banner; i dati di baseline rappresentano lo stato pre-consenso, quelli di rejected lo stato post-rifiuto.
