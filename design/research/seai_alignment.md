# SEAI alignment — what the primary sources actually say

Compiled 6 September 2026, for wording the PlanitBER proposal (pack document 01) against
verified fact rather than assumption.

**Amended 6 September 2026 after a second pass over the same sources.** Two statements in
the first version were wrong and are corrected below, marked CORRECTION. Four findings were
missing and are added. The corrections matter: bulk use *is* expressly prohibited, not
merely impractical, and Regulation 27(4)(c) is a weaker instrument than first described.

**Method note.** `seai.ie` and `irishstatutebook.ie` both return HTTP 403 to automated
fetching. Everything below marked *first-hand* was read in a real browser session against
the live page or a downloaded PDF, not from search snippets or memory. Where something
could not be verified that way it is marked plainly and must not be treated as settled.

---

## 1. Eligibility — who may join the Trusted Partner trial

**First-hand.** Source: <https://www.seai.ie/pilot-projects> and Schedule 2 of the
Trusted Partner Agreement,
<https://www.seai.ie/sites/default/files/pilot-projects/Trusted-Partner-Agreement.pdf>

The page defines the participant type:

> "For the purposes of this trial, a home energy service provider is described as an
> entity working in the residential market actively engaging with homeowners promoting
> the retrofit concept and providing advisory services to them on energy efficiency
> upgrades to their homes, along with cost estimates for different packages of works."

On who may apply:

> "This trial is open to all market actors provided they can meet the terms and
> conditions and eligibility criteria set out in the Trusted Partner Agreement."

Schedule 2, headed **ELIGIBILITY CRITERIA FOR TRUSTED PARTNERS**, opens:

> "This Trial is open to any entities or partnerships that can demonstrate compliance
> with the following criteria:"

The five key requirements, verbatim headings from the web page, are: *Must provide a Home
Upgrade Service*; *Must propose a technology solution*; *Must have a registered BER
Assessor*; *Must have a Consent Management Process*; *Must conduct a DPIA*. The third
reads:

> "Must have a registered BER Assessor assigned as the requestor of BER data for the
> duration of the trial to ensure BER data is interpreted and processed in a manner that
> align with SEAI DEAP methodology and to fulfil Article 27(4c) (iii) of S.I. 243,"

**Answer to the question asked.** It is **not** restricted to One Stop Shops or registered
contractors. The words are "all market actors" and "any entities or partnerships". A
registered BER assessor practice is not excluded, and the trial positively *requires* a
registered BER assessor as the data requestor, which such a practice has in-house.

**AMBIGUOUS — the one point to put to SEAI.** Schedule 2 criterion 1 requires that the
partner "will use the Service to help develop the One-Stop-Shop service delivery model in
the domestic retrofit market", and requires partners to

> "demonstrate at a minimum their involvement in Stages 1 and 2 of the home upgrade
> customer journey"

where stage 2 is

> "Stage 2 - Assessments and quotations: providing tailored consumer advice using the
> Service and organising quotes for recommended works."

Two readings compete. Either "organising quotes" means the partner itself arranges
contractor quotes, in the manner of a One Stop Shop, or it covers putting a priced scope
to the market so the homeowner obtains comparable quotes — which is what the Pricing
Schedule does. The wording does not settle it. **Do not assert eligibility in the pack.**
Ask SEAI whether an assessor practice issuing a schedule for the homeowner to tender
satisfies stage 2.

**AMBIGUOUS — a second one, on legal form.** The Agreement's party block presupposes a
company:

> "(2) ______________, a private company limited by shares registered in Ireland with
> company number _______ and located at ________________________( "Trusted Partner")"

while clause 1.2.4 of the same document reads:

> "a reference to a person shall include a reference to a firm, a body corporate, an
> unincorporated association, a partnership or to an individual's executors or
> administrators;"

and Schedule 2 says "any entities or partnerships". Either the party block is boilerplate
to be adapted, or it is substantive and excludes unincorporated practices. The documents do
not resolve it. If this practice is not a company limited by shares, add it to the
questions for SEAI.

**Application mechanism.** In writing, by email:

> "Prospective Trusted Partners need to submit in writing to nastpapi@seai.ie evidence of
> how they intend to comply with the five key requirements listed above, and review fully
> the terms and conditions and eligibility criteria in the Trusted Partner Agreement."

> "All technical and other queries to nastpapi@seai.ie."

---

## 2. What the API provides, and what it does not

**First-hand**, <https://www.seai.ie/pilot-projects>:

> "The Service - termed the "NAS Trusted Partner API" - will enable eligible participants
> to access electronic BER datafiles (JSON) in real-time via an Application Programming
> Interface (API) and to submit modified BER datafiles to the SEAI DEAP calculation engine
> to return estimated energy uplifts."

So all three are confirmed: JSON datafile retrieval, submission of modified files to DEAP,
and return of estimated uplifts.

**What it does not provide.**

**CORRECTION.** The first version of this file said bulk use was precluded in practice
rather than by explicit prohibition. That was wrong. The Terms and Conditions prohibit it
in terms, at paragraph 10 — first-hand, from
<https://www.seai.ie/sites/default/files/pilot-projects/Trusted-Partner-Terms-and-Conditions.pdf>
(note the canonical path; the shorter `/pilot-projects/…` URL redirects here):

> "10. You agree not to use the Service and Data:
> • In a way that could or does negatively impact the performance of the system or network
> for us or other users (for example, bulk calls to the Service);
> • Download or transit any viruses, Trojan horses or any other programs that are designed
> to, or reasonably could be expected to, interfere or damage the Service and Data; and
> • For any commercial purposes other than as set out in these Terms and Conditions."

The prohibition is framed around system performance rather than as a data-protection rule,
so quote it as written. The same paragraph also limits commercial use, which is worth
knowing before a commercial product is described to SEAI. Paragraph 20 adds:

> "We do not endorse or recommend for public use any specific Application developed for the
> use of its APIs, and any statements implying or claiming that we have made such an
> endorsement are strictly prohibited."

**ADDITION — the API does not return the address.** Agreement Schedule 1, first-hand:

> "The property address, client details, and BER Assessor details will not be returned to
> the Trusted Partner."

Any workflow that assumes an address-identified record comes back from the API is wrong.
The MPRN is the identifier.

On top of those, the per-request gate. Schedule 2 criterion 3.4 requires, per request:

> "The Trusted Party shall upload evidence of ownership and/or occupancy when submitting a
> request to the Service (e.g. utility bill with MPRN, details of the relevant BER
> Assessor involved in the request …)"

and 3.6:

> "The uploaded file must contain a clearly printed MPRN that is legible to an Optical
> Character Recognition ("OCR") engine. The Service will not return a BER datafile if the
> MPRN in the uploaded file does not match the MPRN in the service request."

One dwelling, one consent, one evidence file, per call. The data catalogue entry agrees:
access rights **restricted**, personal data **yes**, open data **no**, primary identifier
**MPRN** — <https://datacatalogue.gov.ie/dataset/domestic-building-energy-rating-data>:

> "Users of the service are required to sign a trusted partner agreement with SEAI,
> demonstrate eligibility to use the service, and obtain consent from homeowners to
> retrieve their data."

---

## 3. Consent, and the legal basis without the API

**Per request, first-hand from the web page:**

> "the Trusted Partner will display and capture the required consent for SEAI to release
> the data, and separately display and capture the required consent for the Trusted
> Partner to further process the BER data to provide the advisory service."

Two separate consents. Capture is by declaration checkbox or signed consent form, with
evidence of ownership or occupancy, and "The wording of the homeowner declaration and
consent must be agreed with SEAI prior to publishing."

**A named assessor attaches to every request.** Schedule 2 criterion 6:

> "In respect of each request to the Service, the Trusted Partner shall provide to SEAI
> full details of the relevant BER Assessor involved (including but not limited to the BER
> Assessor's name and registration number and any other details as may be requested by
> SEAI from time to time)."

Criterion 3.1 names the legal basis directly: consent captured "in compliance with GDPR
Article 6(1) and Regulation 27(4)(c) of SI 243/2012".

**The statute, first-hand**, S.I. No. 243/2012, Regulation 27(4)(c),
<https://www.irishstatutebook.ie/eli/2012/si/243/made/en/print>:

> "(c) other than provided for in subparagraphs (a) and (b), a data file or other extract
> from a register relating to a BER assessment for a particular building shall normally
> only be made available to—
> (i) the BER assessor that carried out the relevant BER assessment, or his or her then
> employer,
> (ii) a BER assessor undertaking any subsequent BER assessment of the relevant building,
> or his or her employer, or
> (iii) the relevant owner of the building, or an agent acting on behalf of the owner, via
> a BER assessor;"

**CORRECTION — read the word "normally".** The first version of this file said
sub-paragraph (i) "is already ours". That overstated it. The provision reads "shall
**normally** only be made available to", which constrains SEAI's disclosure practice and
sets a default; it does not confer a right of access on the assessor. So: sub-paragraph (i)
covers a practice working from the data files of assessments **it carried out**, and is the
ordinary course rather than a guarantee. Sub-paragraph (iii) is the consented route for any
other dwelling, and is the route the trial is built on — note "via a BER assessor", which
makes the assessor the required conduit and is exactly what Schedule 2 criteria 5 to 7
operationalise. Anything beyond those two is outside the regulation.

SEAI's own page cites this as "Article 27(4c) (iii) of S.I. 243". The instrument says
"Regulation" and "(4)(c)(iii)"; cite it the instrument's way.

---

## 4. Renovation passports — and the limit on how strongly we may word this

**First-hand**, Directive (EU) 2024/1275, read on EUR-Lex,
<https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401275>

Article 12(1):

> "By 29 May 2026, Member States shall introduce a scheme for renovation passports based
> on the common framework set out in Annex VIII."

Article 12(2): the scheme "shall be of voluntary use by owners of buildings and building
units, unless the Member State decides to make it mandatory."

Article 12(4):

> "The renovation passport shall be issued in a digital format suitable for printing, by a
> qualified or certified expert, following an on-site visit."

**Annex VIII is in two halves, and the split is the whole point.**

Point 1 — "**The renovation passport shall include:**" — runs (a) to (j) and is entirely
energy, sequencing, funding signposting and advisory contact. The only cost-adjacent
mandatory item is 1(e)(iv), "the estimated savings on the energy bill, clearly indicating
the assumptions on energy costs used for the calculation". That is a **bill saving**, not
an investment cost.

Point 2 — "**The renovation passport may include:**" — is where the money sits:

> "(b) for each step: (i) a detailed description of the technologies, techniques and
> materials to be used, their advantages, disadvantages and costs; … (iii) the estimated
> costs for carrying out the step; (iv) the estimated payback period for the step, with
> and without any available financial support; … (vii) the estimated lifetime of measures
> and the estimated maintenance costs;"

**Conclusion, and it binds our wording.** Estimated investment cost is an **encouraged /
optional** element, not a required one. We may therefore say the three documents *carry the
cost layer a passport needs*. We may **not** say they are a passport, nor that a passport
requires cost information.

**CONTRADICTS THE CURRENT PACK.** Document 01, page 2, presently describes a passport as
"a document setting out the scope, the sequence and the cost of bringing one dwelling to a
target rating". The word "cost" there overstates Annex VIII. Fix in Part 2.

**Ireland's position — one verified source, and it is favourable.** SEAI's own *Domestic
Technical Standards and Specifications, Version 4.0, July 2026*, section 2.8, read
first-hand from
<https://www.seai.ie/sites/default/files/publications/Domestic-Technical-Standards-and-Specifications.pdf>:

> "Building Renovation Passport (BRP) is a dwelling-specific, homeowner-facing renovation
> Roadmap that builds on the published BER / DEAP baseline. The BRP Roadmap sets out a
> staged pathway of clear actionable step-by-step measures for improving the dwelling's
> energy performance over time, taking account of the dwelling's current condition,
> available evidence, technical risks, homeowner context and sequencing dependencies."

> "When a Building Energy Rating (BER) is published there is flexibility for separate
> issuance of a Building Renovation Passport (BRP). The BER remains the baseline energy
> assessment of the energy performance of a building. The BRP does not replace the BER."

So SEAI's current domestic standards already contemplate a BRP issued separately from a
BER, building on the DEAP baseline. That is close to the shape of our three documents.

**Transposition — no statutory scheme found, with a caveat.** The Article 12 deadline of
29 May 2026 has passed. A second pass found no Irish statutory instrument transposing
Article 12 or Annex VIII: the EU's national implementing measures register for the
directive lists only S.I. 642/2024 and S.I. 749/2024, and neither, nor S.I. 168/2026 nor
S.I. 195/2026, contains the phrase "renovation passport". **Caveat: that register can lag
notification, and the Irish Statute Book year indexes could not be enumerated, so treat
this as "none found", not "none exists".** Do not put a transposition-failure claim in the
pack; it reads as a jab at the body being addressed and needs legal advice first.

**A friction to note.** Article 12(4) requires a passport to be issued "by a qualified or
certified expert". Nothing in the directive says that credential is BER assessor
registration, and Ireland has not defined it. So BER registration alone should not be
assumed to authorise issuing an Article 12 passport. This is a further reason to say the
documents *carry the cost layer a passport needs* rather than that we can produce one.

---

## 5. The trial's stated objectives, verbatim

**First-hand**, <https://www.seai.ie/pilot-projects>, under "Key Objectives":

> - "Trial and evaluate a new SEAI Service that will enable the market to achieve
>   government objectives of retrofitting 500,000 homes to a B2 rating before 2030"
> - "Support Government Climate Action Plan actions related to making better use of BER
>   data and driving the development of a One Stop Shop retrofit model in Ireland"
> - "Evaluate and measure the benefit of providing BER data to home upgrade service
>   providers, with real time DEAP recalculations, in a format that can be applied to
>   assist homeowner decision making on home retrofit investment."
> - "Focus on the impact that providing BER data and BER recalculation has on consumer
>   decisions"
> - "Foster innovation in the marketplace by incentivising application developers to build
>   data driven solutions for homeowners to make the best decisions for their homes"

The third is the one our pilot ask should mirror: *evaluate and measure the benefit*.

Note the first objective still says "B2 rating", although B2 ceased to be a BER band on
24 May 2026. That is SEAI's wording, not ours; quote it as theirs if quoted at all.

---

## 6. Duration and dates

**First-hand.** The web page:

> "The Service will be available to participants ("Trusted Partners") for a period of 12
> months upon signing a "Trusted Partner Agreement"."

The Agreement defines it per participant, not as a fixed calendar window:

> ""Trial Period" means the period commencing on the Effective Date and ending on the date
> being twelve months from the Effective Date."

**The page does not state** a trial start date, an end date, a review date, or a closing
date for expressions of interest. It is written in the present tense with a live "How to
Apply" section and a live contact address, which is consistent with the trial being open,
but it does not say so and that inference should not be presented as fact.

One dating signal, first-hand from the published template: the execution line still reads

> "THIS AGREEMENT is made on the             day of           2021   (the "Effective Date")"

The published template therefore still carries 2021. That is a reason to **ask SEAI where
the trial currently stands** rather than to assume it is running.

---

## Summary for the drafter

**Safe to say.** The trial exists and is described as open to all market actors. It
requires a registered BER assessor as data requestor. It works per dwelling, on captured
homeowner consent, under Regulation 27(4)(c). A practice may already work from the files of
assessments it carried out itself, under 27(4)(c)(i). Article 12 obliges a renovation
passport scheme from 29 May 2026, issued by a qualified expert after an on-site visit.

**Not safe to say.** That we are eligible — the stage 2 wording is ambiguous, and that is a
question for SEAI. That a passport requires cost information — Annex VIII puts cost under
"may include". Anything about the current status of the Irish passport scheme, or of the
trial itself, which is unverified.

**Carried over from earlier work and NOT re-verified here.** The figure of 1.37 million
dwellings holding a published BER, which currently appears on page 2 of document 01. Verify
against the CSO release before the pack is issued.
