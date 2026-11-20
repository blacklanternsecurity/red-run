---
name: session-fixation
description: >
  Determine whether an application rotates its session identifier on successful
  authentication, and demonstrate account takeover when it does not. Use when a
  cookie-based session exists and you can observe the login response, or when a
  finding mentions session hygiene, session lifecycle, or URL-rewritten session
  IDs. Do NOT use for stealing an already-authenticated session (that is XSS,
  network interception, or token leakage), nor for token-based auth where the
  credential is issued at login and never pre-exists — there is nothing to fix.
keywords:
  - session fixation
  - session id not rotated
  - session not regenerated
  - jsessionid
  - phpsessid
  - session hygiene
  - session lifecycle
  - url rewriting session
  - cookie fixation
  - pre-authentication session
  - session takeover
  - CWE-384
tools:
  - curl
  - browser-server (delivery-vector verification only)
opsec: low
---

# Session Fixation

You are helping a penetration tester determine whether an application issues a
new session identifier when a user authenticates. When it does not, an
identifier obtained before login stays valid after it — so an attacker who
plants their own identifier in a victim's browser holds an authenticated
session the moment the victim logs in, **without ever learning a password**.
All testing is under explicit written authorization.

This is not session *theft*. Nothing is stolen: the attacker supplies the
identifier up front and simply waits for the application to elevate it.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[session-fixation] Activated → <target>` to the screen on activation.
- **Evidence** → save every request/response pair to `engagement/evidence/`
  with descriptive filenames (`sessfix-1-preauth-headers.txt`,
  `sessfix-3-replay-body.html`). The cookie jars themselves are evidence —
  keep them.

## State Management

Call `get_state_summary()` from the state MCP server to read current
engagement state. Use it to:
- Find credentials you can use as the *victim* — this technique needs an
  account you are authorized to log in as, not a real user's
- Check whether a session cookie and its flags are already recorded
- Understand what's been tried and failed (check Blocked section)

Your return summary must include:
- Whether the identifier rotated on authentication (the finding itself)
- The negative control result — **without it the test proves nothing**
- Access gained (user, privilege level, method)
- Whether the impact crosses into a separate component or auth mechanism
  (this drives the CVSS scope metric — see Step 5)
- Blocked items (what failed and why, whether retryable)

## Web Interaction

**curl is the right tool for the core test.** You need byte-level control over
which cookie jar is sent on which request, and you must be able to freeze a jar
so it is not rewritten. A browser hides exactly the thing you are measuring.

Use browser tools only for Step 6, when demonstrating that a delivery vector
actually plants the identifier in a real browser.

## Prerequisites

- A cookie-based session (the server sets a session cookie before login)
- Credentials for an account you are authorized to authenticate as
- An endpoint that returns authenticated content, to prove the takeover

Identify the session cookie name first. Common ones:

| Stack | Cookie |
|---|---|
| Java / Tomcat / Struts | `JSESSIONID` |
| PHP | `PHPSESSID` |
| ASP.NET | `ASP.NET_SessionId` |
| Rails | `_<app>_session` |
| Express | `connect.sid` |

## Step 1: Assess — obtain a pre-authentication identifier

Request any unauthenticated page that sets a session cookie.

```bash
curl -s -c jar-attacker.txt -o /dev/null -D h1.txt \
     --connect-timeout 5 --max-time 15 \
     https://app.example.org/login
grep -i set-cookie h1.txt
```

If no session cookie is set before login, fixation is not applicable — the
identifier does not pre-exist. Record that and stop.

**Freeze a copy immediately.**

```bash
cp jar-attacker.txt jar-attacker-FROZEN.txt
```

This copy is the whole experiment. `curl` rewrites a jar on **every** request
that returns a cookie; without a frozen copy you cannot later tell a *retained*
identifier from a *freshly issued* one, and your result will be meaningless.
Never pass `-c jar-attacker-FROZEN.txt` to anything.

## Step 2: Confirm — authenticate on that identifier

Log in as the victim account **while presenting the attacker's jar**.

```bash
curl -s -b jar-attacker.txt -D h2.txt \
     --connect-timeout 5 --max-time 15 \
     -d "username=<VICTIM_USER>" -d "password=<PASSWORD>" \
     https://app.example.org/authenticate
grep -i set-cookie h2.txt
```

Read the response headers. This is the finding:

- **No `Set-Cookie` for the session cookie** → the identifier was not rotated.
  Vulnerable.
- **`Set-Cookie` with a different value** → rotated correctly. Not vulnerable;
  record it as a control that held and stop.

Then compare the jars directly, and say so in your report:

```bash
diff jar-attacker-FROZEN.txt jar-attacker.txt && echo "IDENTICAL — not rotated"
```

## Step 3: Negative control — MANDATORY

**Do not skip this. A result without it is not evidence.**

Take a second pre-auth identifier that is *never* used to authenticate, and
request the same protected endpoint.

```bash
curl -s -c jar-control.txt -o /dev/null https://app.example.org/login
curl -s -b jar-control.txt -D h-ctrl.txt -o /dev/null \
     https://app.example.org/account
head -1 h-ctrl.txt
```

**It must be refused** — 302 to login, 401, or an empty body.

If it is *accepted*, you have not demonstrated fixation. You have demonstrated
that the server accepts arbitrary session identifiers, which is a different and
often worse defect — record it as such, do not report it as fixation.

Without this control, "the frozen jar worked" is indistinguishable from "any
value works", and a reviewer is right to reject the finding.

## Step 4: Prove the takeover

Replay the **frozen** jar against an endpoint that returns identity-bearing
content. The attacker has typed no credentials at any point.

```bash
curl -s -b jar-attacker-FROZEN.txt -D h4.txt -o proof.html \
     https://app.example.org/account
head -1 h4.txt; wc -c proof.html
grep -oE '(user|account|tenant)[Ii]d[^,<]{0,40}' proof.html | head -3
```

A large body containing the victim's identity is the proof. Save it.

Prefer an endpoint whose response is *unambiguously* the victim's — a name, an
account number, a tenant identifier. A generic dashboard that renders the same
for everyone proves nothing.

## Step 5: Assess impact and scope

Two questions decide severity.

**Does the impact stay inside the vulnerable component?** If the fixed session
also unlocks a *separate* component with its own authentication — a second API,
a different backend, an SSO-linked service — that is a CVSS scope change
(`S:C`), and it raises the score substantially. Check whether the authenticated
response hands you anything usable elsewhere: a bearer token, an API key, an
identity assertion.

**What does the victim have to do?** Fixation always requires the victim to
authenticate on the planted identifier, so `UI:R` applies. This lowers
likelihood but does **not** cap severity when the scope changes — a common
scoring mistake.

Typical vector for full account takeover with a scope change:

```
AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N
```

Compute the score rather than asserting it — an inconsistent vector/score pair
is the first thing a reviewer notices.

## Step 6: Delivery vector

Fixation without a delivery vector is a design flaw; fixation *with* one is an
attack. Establish which vector the application permits — never assume, and
never assume it is the same on every path.

**URL-borne identifiers.** Some stacks accept the identifier in the request
itself, so a bare link is enough — no XSS, no network position.

| Stack | Form |
|---|---|
| Java servlet containers | `;jsessionid=<ID>` path parameter |
| PHP (`session.use_trans_sid`) | `?PHPSESSID=<ID>` query parameter |
| Legacy ASP / custom | app-specific query parameter |

Test it, do not infer it from the stack. Request a path with a **known-valid**
identifier and no cookie, and read the response headers:

- **No `Set-Cookie` for the session cookie** → the identifier was adopted
- **`Set-Cookie` with a different value** → it was ignored and replaced

**Run the fabricated-identifier control.** Repeat with a value the server never
issued. If that is *also* adopted, the finding is not fixation — the server
accepts arbitrary identifiers, which is worse and scored differently. If it is
replaced while the valid one was adopted, the contrast proves genuine adoption
rather than an artefact of the code path.

**Check per path.** Applications commonly expose several entry points — a
legacy form, an SSO redirect chain, an SPA route. They frequently differ: one
may adopt a supplied identifier while another discards it and mints a fresh one
at every hop. A vector that works on one path and is published against another
makes the whole finding look false when a reader tries to reproduce it. Name the
exact path that works.

**Check propagation.** Adoption on the landing page is not enough — the
identifier must survive to the login submission. Read the login form's `action`
and any in-page links: if the framework rewrites them with the adopted
identifier, the victim carries it forward without having to keep the original
URL. If it does not, the vector may break at the moment the victim submits.

**Cookie injection from a related origin.** A subdomain can set a cookie for the
parent domain. If any subdomain is attacker-influenced, it can plant the
identifier — and this route is unaffected by `HttpOnly`.

**Response splitting or header injection**, where reflected input reaches
`Set-Cookie` or a redirect.

**Shared or unattended browsers** — kiosk, shared workstation, lab machine.
Weaker but requires no application-level vector at all.

If none of these work, say so. "Fixation confirmed, no practical delivery
vector identified" is an honest and useful finding — it changes remediation
priority without overstating exploitability.

### Precedence: what wins when a cookie and a URL identifier disagree?

If the victim's browser already holds a session cookie, two identifiers are in
play. **Which one the server honours is configuration- and container-dependent —
test it, never assume.** The answer bounds who the attack can reach:

- **Cookie wins** → the link only works against a victim with no valid session
  cookie at click time: first visit, private browsing, cleared or expired
  cookies. Note this precondition is largely *implied* by the scenario anyway —
  a victim who must log in is by definition one without an active session — so
  it rarely justifies lowering severity, but it does explain reproduction
  failures and it matters for remediation.
- **URL wins** → the link hijacks the session of a user who is *already* active.
  Materially worse; revisit the severity.

**A trap when testing this.** The obvious marker — whether the framework
rewrites links with the identifier — does **not** discriminate. Servlet
containers stop URL-encoding the session id as soon as a valid session cookie is
recognised, whichever session they then act on. Both hypotheses produce an
identical page. Use a **functional** marker instead: authenticate one of the two
sessions, leave the other anonymous, then request a protected endpoint and see
which identity comes back. Test both directions and require them to converge.

## Step 7: Escalate or Pivot

- Authenticated session → enumerate what that identity reaches (route to the
  appropriate discovery skill)
- Bearer token or API key in the authenticated response → separate credential
  finding, with provenance linking back to this one
- Session survives logout → chain with a session-lifecycle finding
- Identifier accepted across subdomains or environments → widen the target set

## OPSEC Notes

- The traffic is a normal login plus a few authenticated reads. Nothing here is
  noisy or destructive.
- You authenticate as an account you are authorized to use. **Never fix a
  session onto a real user** — that is an actual account compromise, not a test.
- The planted session stays valid until it expires. Note it in the engagement
  record so it is not mistaken later for an intruder.

## Troubleshooting

**The fixed identifier redirects me to the login page.**
Usually correct behaviour rather than a failure. Work through these in order —
each is common, and more than one can apply at once:
1. **No authentication happened on that identifier.** Fixation pays off only
   *after* a victim logs in on it. An identifier that was never authenticated
   must be refused — that is Step 3, the negative control, working as intended.
2. **A session cookie is already present** and takes precedence over the one in
   the URL. Retry with a clean cookie jar, or in a private browsing context.
   See the precedence section in Step 6.
3. **The session expired.** Containers typically drop idle sessions after
   ~30 minutes. Re-run the sequence end to end; never reuse an old identifier.
4. **Wrong entry point.** Applications frequently have several login paths, and
   they do not behave alike — one may adopt a supplied identifier while another
   discards it. Use the path that set the session you captured. Probe with
   `curl --max-redirs 0` and read `Location`; never follow a redirect blindly,
   it may leave the authorized scope.

**Nothing visible happens when I open the crafted link.**
Expected. Adoption is silent: the response is the same login page whether the
server took your identifier or issued a fresh one. There is nothing to see in the
rendered page, and no error is shown. The only observable difference is in the
response headers — the presence or absence of `Set-Cookie` for the session
cookie. Read the headers, not the page.

**The jars differ but the identifier looks the same.**
Compare the cookie *value*, not the file. Jars also carry expiry timestamps
that change without the identifier changing.

**No `Set-Cookie` on login, but the frozen jar is refused afterwards.**
The server probably tracks rotation server-side, invalidating the old
identifier without issuing a visible new one. Not fixation. Record it as a
control that held.

**Login succeeds but the protected endpoint returns the login page anyway.**
The endpoint may require a second factor, a tenant selection step, or a
different cookie. Follow the application's own post-login navigation once as an
authenticated user to find the endpoint that genuinely proves identity.

**The application uses a bearer token, not a cookie.**
Fixation does not apply: the credential is issued at authentication and does
not pre-exist. Record it as not applicable and move on.
