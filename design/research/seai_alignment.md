# SEAI alignment — what the primary sources actually say

Compiled 6 September 2026, for wording the PlanitBER proposal (pack document 01) against
verified fact rather than assumption.

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

**What it does not provide.** There is no statement anywhere granting bulk or register-wide
access, and bulk retrospective use is precluded in practice rather than by an explicit
prohibition. Schedule 2 criterion 3.4 requires, per request:

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

**What this means for our page-2 claim.** Sub-paragraph (i) is the important one and it is
already ours: a practice may work from the data files of assessments **it carried out**,
with no API and no new permission. Sub-paragraph (iii) is the consented route for any other
dwelling, and it is the route the trial itself is built on. Anything beyond those two is
outside the regulation.

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

**Ireland's national scheme — NOT VERIFIED FIRST-HAND.** No dated status claim is made
here. The SEAI EPBD Programme Development (Building Renovation Passports) candidate
booklet was not retrieved in this session. Do not put an Irish status claim in the pack
until it is read directly.

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
