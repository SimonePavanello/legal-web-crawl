# Report Violazioni GDPR – Cookie Consent Compliance

**Data analisi**: 2026-02-22 13:52  
**Siti analizzati**: 8  
**Fonte tracker list**: Disconnect.me (Advertising, Analytics, Social, Fingerprinting)  
**Definizione cookie non necessari**: cookie il cui eTLD+1 è diverso dal sito visitato *(euristica di automazione — v. Note Metodologiche)*

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

> **Nota – Cookie con finalità di profilazione.** Tra i cookie rilevati, `yandexuid` (`.yandex.com` e `.yandex.ru`, scadenza 2027) costituisce un identificatore utente persistente a lungo termine, classificato come cookie di profilazione da Yandex stessa nella propria informativa. Analogamente, `bh` (behaviour history) e `_yasc` (yet another session cookie) sono associati ad analisi comportamentale. Questi cookie presentano una finalità di tracciamento più netta rispetto ad altri che potrebbero avere interpretazioni ambigue (es. cookie di sessione tecnici). La presenza di `gdpr_popup` su `.yandex.ru` con scadenza di sessione suggerisce che il sito rileva la giurisdizione GDPR, rendendo l'assenza di consenso preventivo ancora più significativa dal punto di vista giuridico.

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

> **Nota – Violazione del flusso di dati, non dello storage.** In assenza di cookie di terze parti, la violazione V3 di facebook.com è di natura diversa rispetto ai casi con cookie rilasciati: si tratta di una **violazione del flusso di dati**. Il contatto HTTP verso `facebook.com`, classificato come *Fingerprinting* nella lista Disconnect.me, implica la trasmissione dell'indirizzo IP dell'utente e di altri metadata HTTP (User-Agent, Referer) al server di Facebook. Ai sensi dell'art. 4 n. 1 GDPR, l'indirizzo IP è un dato personale. Il suo trasferimento a una terza parte senza base giuridica (il consenso è stato negato e non è stato valutato alcun legittimo interesse) configura un trattamento illecito ai sensi dell'art. 6 GDPR. Il fatto che non venga impostato alcun cookie non esclude l'illiceità: il fingerprinting può avvenire senza storage lato client.

### https://cloudflare.com

**Violazione V3 rilevata.**

**Cookie di terze parti impostati dopo il rifiuto:**

*Nessun cookie di terze parti rilevato.*

**Tracker contattati dopo il rifiuto:**

- `cloudflareinsights.com` (Analytics)

> **Nota – Violazione del flusso di dati (Analytics).** Come nel caso di facebook.com, la violazione rilevata per cloudflare.com è una **violazione del flusso di dati**: nessun cookie di terze parti viene impostato, ma il contatto HTTP con `cloudflareinsights.com` (servizio Cloudflare Web Analytics) comporta il trasferimento dei dati di navigazione dell'utente — incluso indirizzo IP — a Cloudflare. Poiché il tracker rientra nella categoria *Analytics*, il trattamento richiede consenso ai sensi dell'art. 6(1)(a) GDPR e del Considerando 47 (che esclude il legittimo interesse per il tracking analitico di terze parti). Il rifiuto esplicito del consenso rende il trattamento privo di base giuridica.

### https://youtube.com

**Violazione V3 rilevata.**

**Cookie di terze parti impostati dopo il rifiuto:**

| Cookie | Host | Scadenza | HttpOnly | SameSite |
|--------|------|----------|----------|----------|
| `__Host-GAPS` | `accounts.google.com` | 2027-03-27 | Sì | unspecified |

> **Nota tecnica – Prefisso `__Host-` e cookie di autenticazione.** Il prefisso `__Host-` è definito dall'RFC 6265bis (Cookie Prefixes) e impone vincoli di sicurezza stringenti: il cookie deve avere l'attributo `Secure`, non può specificare un attributo `Domain` (è quindi legato esclusivamente all'host esatto `accounts.google.com`), e il percorso deve essere `/`. La presenza del flag `Sì` su HttpOnly è coerente. Tuttavia, il campo SameSite risulta `unspecified`, il che è anomalo per un cookie di autenticazione moderno e potrebbe indicare un cookie legacy. `__Host-GAPS` è associato all'autenticazione dell'account Google (Google Accounts Password Session). **Questione aperta:** se il crawl è stato eseguito con un profilo browser pulito (nessuna sessione Google preesistente), l'impostazione di questo cookie dopo il rifiuto del consenso non può essere giustificata da una sessione di autenticazione attiva, e la violazione V3 è documentata in modo robusto. Se invece il profilo conteneva credenziali Google precaricate, il cookie potrebbe rientrare nell'eccezione tecnica strettamente necessaria (art. 5(1)(c) GDPR, minimizzazione). Il presente report assume profili puliti, conformemente alla metodologia OpenWPM standard.

**Tracker contattati dopo il rifiuto:**

*Nessun tracker contattato.*

### https://apple.com

*Nessuna violazione V3 rilevata.*

> **Analisi – Apple.com come caso di best practice.** Apple.com è l'unico sito del campione a non presentare violazioni V3. Questa conformità può derivare da due fattori distinti, non mutuamente esclusivi:
>
> 1. **Assenza nativa di tracker di terze parti**: Apple utilizza prevalentemente propria infrastruttura (CDN, analytics interni) e non integra per default script di terze parti come Google Analytics o Meta Pixel. La sezione V2 conferma che nessun tracker esterno viene contattato nemmeno prima del consenso.
>
> 2. **Corretta implementazione del CMP**: il Consent Management Platform di Apple sembra bloccare effettivamente le chiamate asincrone post-rifiuto, a differenza di soluzioni CMP che si limitano a non impostare cookie ma lasciano attivi gli script di tracking.
>
> Dal punto di vista giuridico, il caso apple.com illustra che la conformità GDPR in materia di cookie non richiede necessariamente un banner elaborato, ma una progettazione *privacy-by-design* (art. 25 GDPR) che riduca ab origine la dipendenza da servizi di terze parti. Apple.com può essere citato come esempio di architettura conforme nel contesto di questa analisi.

### https://instagram.com

**Violazione V3 rilevata.**

**Cookie di terze parti impostati dopo il rifiuto:**

*Nessun cookie di terze parti rilevato.*

**Tracker contattati dopo il rifiuto:**

- `facebook.com` (Fingerprinting)

> **Nota – Violazione del flusso di dati tramite infrastruttura Meta.** Instagram è di proprietà di Meta Platforms Inc., la stessa entità giuridica che gestisce facebook.com. Il contatto HTTP verso `facebook.com` (Fingerprinting) da parte di instagram.com dopo il rifiuto del consenso ripropone la stessa violazione del flusso di dati descritta per facebook.com: trasferimento dell'indirizzo IP e dei metadata HTTP a Meta senza base giuridica. Va notato che, trattandosi dello stesso titolare del trattamento (Meta), la violazione assume rilevanza anche per il principio di trasparenza (art. 5(1)(a) GDPR): l'utente che rifiuta il consenso su Instagram non si aspetta che i propri dati siano comunque trasmessi a facebook.com.

---

## Tassonomia dei Tracker Rilevati

La seguente classificazione aggrega tutti i domini tracker rilevati nelle fasi V2 e V3, per categoria Disconnect.me, con indicazione del sito osservatore.

### Advertising

| Dominio tracker | Osservato su | Fase |
|----------------|--------------|------|
| `yadro.ru` | mail.ru | V2, V3 |
| `omtrdc.net` | aws.amazon.com/it | V2, V3 |

`yadro.ru` è la piattaforma pubblicitaria di Yandex; `omtrdc.net` è il dominio di raccolta dati di Adobe Analytics (Adobe Experience Cloud).

### Analytics

| Dominio tracker | Osservato su | Fase |
|----------------|--------------|------|
| `clarity.ms` | microsoft.com | V2, V3 |
| `cloudflareinsights.com` | cloudflare.com | V2, V3 |
| `google-analytics.com` | mail.ru | V3 |

La presenza di `google-analytics.com` esclusivamente nella fase V3 di mail.ru — e non nella V2 baseline — è un'anomalia degna di nota: suggerisce che Google Analytics venga attivato da mail.ru solo dopo l'interazione con il banner, potenzialmente come effetto collaterale di uno script legato al flusso di consenso.

### Social

| Dominio tracker | Osservato su | Fase |
|----------------|--------------|------|
| `mail.ru` | mail.ru | V2, V3 |
| `userapi.com` | mail.ru | V2, V3 |
| `vk.com` | mail.ru | V2, V3 |

`userapi.com` e `vk.com` sono infrastrutture del gruppo VK (VKontakte), direttamente integrati in mail.ru come widget social. La presenza simultanea in V2 e V3 indica un'integrazione statica non condizionata al consenso.

### Fingerprinting

| Dominio tracker | Osservato su | Fase |
|----------------|--------------|------|
| `facebook.com` | facebook.com | V2, V3 |
| `facebook.com` | instagram.com | V2, V3 |

Il rilevamento di `facebook.com` come tracker di tipo *Fingerprinting* sia su facebook.com stesso che su instagram.com conferma che l'infrastruttura Meta è attiva indipendentemente dal consenso espresso. La categoria *Fingerprinting* in Disconnect.me include tecniche di identificazione basate su caratteristiche del browser (canvas fingerprinting, font enumeration, WebGL) che non richiedono storage lato client.

---

## Analisi delle Scadenze dei Cookie

L'art. 5(1)(e) GDPR (limitazione della conservazione) e l'art. 5(1)(c) (minimizzazione dei dati) impongono che i dati personali non siano conservati in una forma che consenta l'identificazione degli interessati per un arco di tempo superiore a quello necessario alle finalità del trattamento. Cookie persistenti con scadenza pluriannuale, impostati prima o dopo il rifiuto del consenso, sono in tensione diretta con questi principi.

I seguenti cookie con scadenza nel 2027, identificati nel campione, sono particolarmente significativi:

| Cookie | Host | Sito | Fase | Scadenza | Durata approx. |
|--------|------|------|------|----------|----------------|
| `yandexuid` | `.yandex.com` / `.yandex.ru` | mail.ru | V1, V3 | 2027-03-22 / 2027-03-27 | ~13 mesi |
| `zencookie` | `.dzen.ru` | mail.ru | V1, V3 | 2027-03-22 / 2027-03-27 | ~13 mesi |
| `remixstlid` | `.vk.com` / `.vkvideo.ru` | mail.ru | V1, V3 | 2027-02-15 / 2027-02-20 | ~12 mesi |
| `__Host-GAPS` | `accounts.google.com` | youtube.com | V1, V3 | 2027-03-22 / 2027-03-27 | ~13 mesi |

**Osservazioni:**

- `yandexuid` è l'identificatore utente primario di Yandex, analogo al `_ga` di Google Analytics. Una durata di ~13 mesi per un cookie impostato *prima* del consenso configura una raccolta di dati identificativi senza base giuridica per un periodo prolungato, aggravando la violazione V1 rispetto a un cookie di sessione.
- `zencookie` (Dzen, già Yandex.Zen) e `remixstlid` (VK) sono identificatori di piattaforme editoriali e social che permettono il tracciamento cross-session degli utenti per finalità di profilazione.
- `__Host-GAPS` con scadenza 2027 persiste dopo il rifiuto del consenso su youtube.com. Se il profilo è pulito (v. sezione Limitazioni), questo costituisce un identificatore persistente impostato in assenza di qualsiasi base giuridica per un periodo di oltre un anno.
- La scadenza pluriannuale di questi cookie indica che i titolari del trattamento non applicano il principio di minimizzazione: una scadenza di sessione o di pochi giorni sarebbe sufficiente per finalità tecniche legittime.

---

## Limitazioni dello Strumento

L'analisi presentata si basa sullo strumento OpenWPM, una piattaforma di crawling automatizzato sviluppata per la ricerca sulla privacy web. La sua applicazione nel presente contesto introduce alcune limitazioni metodologiche che devono essere considerate nell'interpretazione dei risultati.

**1. Singola istanza browser – assenza di variabilità comportamentale**

OpenWPM simula un singolo utente con un singolo profilo browser. I siti reali servono contenuti diversi in base a fattori come geolocalizzazione dell'IP, versione del browser, presenza di cookie preesistenti o parametri di A/B testing. Un singolo crawl non è rappresentativo della variabilità nell'erogazione dei banner di consenso che un utente reale potrebbe sperimentare.

**2. Geolocalizzazione dell'IP e comportamento dei CMP**

Alcuni Consent Management Platform (CMP) mostrano banner GDPR-compliant solo a utenti con indirizzo IP europeo, rilevato tramite geolocalizzazione. Se il crawl è stato eseguito da un IP non europeo (es. server cloud statunitense o asiatico), alcuni siti potrebbero non aver mostrato alcun banner di consenso, rendendo l'analisi V3 parzialmente invalida per quei siti: non c'è rifiuto da registrare se il banner non viene mostrato. In tal caso, l'assenza di violazioni rilevate non equivale a conformità.

**3. Tracking puramente JavaScript (senza richieste di rete)**

OpenWPM rileva tracker attraverso richieste HTTP/HTTPS verso domini classificati da Disconnect.me. Tecniche di tracking che non generano richieste di rete verso domini terzi — come il fingerprinting locale (lettura di canvas, font, WebGL) elaborato on-device — non sono rilevabili con questo approccio. I risultati V2 e V3 rappresentano quindi un *lower bound* dell'attività di tracciamento effettiva.

**4. Copertura della lista Disconnect.me**

La lista Disconnect.me è aggiornata periodicamente ma non esaustiva. Tracker nuovi, oscurati sotto domini apparentemente di prima parte (CNAME cloaking), o non ancora classificati non vengono rilevati. In particolare, il CNAME cloaking — tecnica con cui un tracker viene servito su un sottodominio del sito principale — eluderebbe la classificazione basata su eTLD+1 utilizzata per V1 e V3, e non comparirebbe nella lista Disconnect.me come dominio separato.

**5. Profili browser e stato pre-esistente**

L'analisi assume profili browser puliti, privi di sessioni attive, cookie preesistenti o estensioni. Se i profili contenessero dati di navigazione precedenti (es. sessione Google attiva), alcuni cookie tecnici di autenticazione potrebbero essere legittimamente reimpostati dopo il rifiuto del consenso in quanto strettamente necessari alla sessione, e non costituirebbero violazione. La metodologia OpenWPM standard utilizza profili puliti, ma questo deve essere verificato nella configurazione specifica del crawl.

---

## Note Metodologiche

- **Cookie non necessari** (V1, V3): cookie il cui eTLD+1 host differisce dall'eTLD+1 del sito visitato. Identificati con la libreria `tldextract` (Public Suffix List). **Questa è un'euristica di terze parti adottata per ragioni di automazione, non una definizione giuridica.** Essa può generare falsi positivi: ad esempio, un cookie di autenticazione federata (SSO) impostato da un dominio Identity Provider diverso dal sito visitato potrebbe essere tecnicamente necessario e non avere finalità di tracciamento. Analogamente, cookie CDN o di load balancing su domini correlati potrebbero rientrare nella definizione automatizzata pur non essendo tracker. I risultati V1 e V3 devono pertanto essere interpretati come indicatori di potenziale violazione, da confermare con un'analisi qualitativa caso per caso.
- **Distinzione violazione di storage vs. violazione di flusso di dati**: non tutte le violazioni V3 sono equivalenti. Nei casi in cui vengono rilevati cookie di terze parti post-rifiuto (es. mail.ru, youtube.com), la violazione è dello storage: dati persistenti sono scritti sul dispositivo dell'utente. Nei casi in cui non vengono rilevati cookie ma vengono contattati tracker (es. facebook.com, cloudflare.com, instagram.com), la violazione è del flusso di dati: dati personali (indirizzo IP, metadata HTTP) vengono trasmessi a terze parti senza base giuridica. Entrambe le tipologie configurano violazioni del GDPR, ma con meccanismi tecnici e possibili rimedi diversi.
- **Domini tracker** (V2, V3): domini presenti nella lista Disconnect.me nelle categorie Advertising, Analytics, Social, Fingerprinting. Il confronto avviene sul `registered_domain`.
- I cookie sono deduplicati per `(host, nome)` — viene mantenuta l'ultima occorrenza nel log.
- I crawl sono separati (baseline, rejected, accepted): non è disponibile un timestamp preciso dell'interazione con il banner; i dati di baseline rappresentano lo stato pre-consenso, quelli di rejected lo stato post-rifiuto.
