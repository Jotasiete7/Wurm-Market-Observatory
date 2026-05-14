---
title: Methodology
toc: true
---

<div class="obs-page">

  <div class="obs-hero" style="padding-bottom:1.5rem">
    <div class="obs-hero-eyebrow">Methodology</div>
    <h1 class="obs-hero-title" style="font-size:1.8rem">What this is — and what it isn't</h1>
  </div>

  ## The two projects

  The Wurm Market Observatory is the second of two related but independent projects.

  **Project 1 — Historical Archive** preserves raw trade channel logs from Wurm Online.
  It stores original `.txt` files, deduplicates uploads, and shows temporal coverage.
  It does not interpret. It does not generate statistics. It is a custodial infrastructure.
  The raw logs are the canonical source.

  **Project 2 — This Observatory** reads restored corpora exported from the Archive and
  generates interpretive analyses. It never modifies the source data. Every number here
  is derived — not original.

  ## What are lenses?

  Analyses in this observatory are called *lenses* — deliberately. A lens is a way of
  looking, not a way of knowing. Each lens has its own parser, its own methodology, its
  own limitations. None is authoritative. All are partial.

  When you read "287 unique sellers," you are reading: *287 character names appeared in
  a selling context in the covered portions of this corpus.* That is a different
  claim from "287 people sold goods in November 2024."

  ## Coverage and gaps

  No corpus in this archive is complete. Coverage is expressed as a percentage of days
  in a period that contain at least one valid log entry. Gaps are periods with zero entries.

  Gaps are never interpolated. When a chart shows a hatched region, it means:
  *we do not know what happened here.* The chart does not guess.

  ## Rankings and counts

  All rankings use raw mention counts from the covered period only. A seller with low
  corpus coverage may appear lower in rankings not because they were less active, but
  because fewer of their activity days were captured. Coverage is always shown alongside
  the count.

  ## Stack

  This site is built with [Observable Framework](https://observablehq.com/framework/),
  a static site generator for data publications. Charts use
  [Observable Plot](https://observablehq.com/plot/). The site is hosted on
  Cloudflare Pages. All datasets are pre-computed JSON files — there is no live database
  query at render time.

  <div class="method-note" style="margin-top:2rem">
    <strong>A note on epistemic honesty —</strong>
    Wurm Online's trade channel is a public chat channel, not a formal marketplace.
    Sellers post, buyers respond, deals happen off-channel. This observatory observes
    the surface of economic activity, not the activity itself. Treat every number here
    as an estimate with unknown error bounds.
  </div>

</div>
