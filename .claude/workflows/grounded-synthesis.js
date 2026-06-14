/*
 * grounded-synthesis — reusable "best credible answer" workflow.
 *
 * Pattern: source-partitioned extract -> single-authority synthesize -> adversarial verify -> reconcile.
 * Each source (a file, or a distinct web search angle) is owned by exactly one extraction agent, so no two
 * agents read the same material or re-derive the same concept. Overlaps are merged once, by the synthesizer.
 *
 * Invoke:
 *   Workflow({ name: 'grounded-synthesis', args: {
 *     question: 'the task/idea/topic to answer credibly',   // required
 *     files:   ['/abs/path/a.md', '/abs/path/b.md'],        // optional — one extraction agent each
 *     web:     true | false | { breadth: 'shallow'|'medium'|'deep' }, // optional; defaults: on iff no files
 *     outputKind: 'report' | 'answer' | 'taxonomy',         // optional, shapes the deliverable (default report)
 *     focus:   'extra emphasis for extractors'              // optional
 *   }})
 *
 * args may also be a bare string — treated as { question, web:on }.
 * breadth -> web angle count: shallow=2, medium=4, deep=6.
 */

export const meta = {
  name: 'grounded-synthesis',
  description: 'Produce a credible, grounded answer by ingesting files and/or source-partitioned web research, then verifying',
  whenToUse: 'When you want the most credible synthesized answer/report on a topic from multiple files and/or web research, with no concept overlap between agents and adversarial credibility-checking.',
  phases: [
    { title: 'Extract', detail: 'one agent per disjoint source (file or web angle) — no read/concept overlap' },
    { title: 'Synthesize', detail: 'single authority dedupes/clusters claims, tags consensus vs contested' },
    { title: 'Verify', detail: 'completeness critic + credibility verifier, in parallel, adversarial' },
    { title: 'Reconcile', detail: 'fold critiques into final deliverable with confidence + sources' },
  ],
}

// ---- arg normalization -------------------------------------------------
function normalize(a) {
  const asQuestion = q => ({ question: q, files: [], web: { enabled: true, breadth: 'medium' }, outputKind: 'report', focus: '' })
  if (!a) return asQuestion('')
  // args may arrive as a JSON-encoded object string depending on how the workflow is invoked — parse it back to an object.
  if (typeof a === 'string') {
    const s = a.trim()
    if (s.startsWith('{') || s.startsWith('[')) {
      try { a = JSON.parse(s) } catch (e) { return asQuestion(a) }
    } else {
      return asQuestion(a)
    }
  }
  const files = Array.isArray(a.files) ? a.files : []
  let web
  if (a.web === true) web = { enabled: true, breadth: 'medium' }
  else if (a.web === false) web = { enabled: false, breadth: 'none' }
  else if (a.web && typeof a.web === 'object') web = { enabled: true, breadth: a.web.breadth || 'medium' }
  else web = { enabled: files.length === 0, breadth: 'medium' } // default: web on only if no files supplied
  return {
    question: a.question || a.task || a.topic || '',
    files,
    web,
    outputKind: a.outputKind || 'report',
    focus: a.focus || '',
  }
}

const cfg = normalize(args)
const base = p => p.split('/').filter(Boolean).pop()

const WEB_ANGLES = [
  'Authoritative & primary sources: official docs, standards, original papers, the source-of-truth material.',
  'Expert & practitioner perspective: experienced practitioners, well-regarded write-ups/talks, real-world usage and caveats.',
  'Recent developments: changes, releases, or shifts in roughly the last 12 months.',
  'Critical & contrarian views: failure cases, criticisms, known pitfalls, where the common advice is wrong.',
  'Quantitative evidence: benchmarks, studies, measured data and results.',
  'Comparisons & alternatives: how the leading options/approaches differ and when to pick which.',
]
const BREADTH_COUNT = { none: 0, shallow: 2, medium: 4, deep: 6 }

// ---- schemas -----------------------------------------------------------
const EVIDENCE_SCHEMA = {
  type: 'object',
  properties: {
    source: { type: 'string' },
    source_kind: { type: 'string', enum: ['file', 'web'] },
    claims: { type: 'array', items: { type: 'object', properties: {
      statement: { type: 'string' },
      support_quote: { type: 'string' },
      citation: { type: 'string' },
      credibility: { type: 'string', enum: ['high', 'medium', 'low', 'unknown'] },
      credibility_reason: { type: 'string' },
      tags: { type: 'array', items: { type: 'string' } },
    }, required: ['statement', 'citation', 'credibility'] } },
    gaps: { type: 'array', items: { type: 'string' } },
  },
  required: ['source', 'source_kind', 'claims'],
}

const SYNTH_SCHEMA = {
  type: 'object',
  properties: {
    summary: { type: 'string' },
    key_findings: { type: 'array', items: { type: 'object', properties: {
      point: { type: 'string' },
      confidence: { type: 'string', enum: ['high', 'medium', 'low'] },
      agreement: { type: 'string', enum: ['consensus', 'contested', 'single_source'] },
      citations: { type: 'array', items: { type: 'string' } },
    }, required: ['point', 'confidence', 'agreement', 'citations'] } },
    contested: { type: 'array', items: { type: 'object', properties: {
      topic: { type: 'string' }, positions: { type: 'array', items: { type: 'string' } },
    }, required: ['topic', 'positions'] } },
    gaps: { type: 'array', items: { type: 'string' } },
    deliverable: { type: 'string' },
  },
  required: ['summary', 'key_findings', 'deliverable'],
}

const COMPLETENESS_SCHEMA = {
  type: 'object',
  properties: {
    missing: { type: 'array', items: { type: 'object', properties: {
      point: { type: 'string' }, why_it_matters: { type: 'string' }, suggested_source: { type: 'string' },
    }, required: ['point', 'why_it_matters'] } },
    underweighted: { type: 'array', items: { type: 'string' } },
    verdict: { type: 'string' },
  },
  required: ['missing', 'verdict'],
}

const CREDIBILITY_SCHEMA = {
  type: 'object',
  properties: {
    unsupported_or_overstated: { type: 'array', items: { type: 'object', properties: {
      point: { type: 'string' }, issue: { type: 'string' },
    }, required: ['point', 'issue'] } },
    low_credibility_sources: { type: 'array', items: { type: 'object', properties: {
      citation: { type: 'string' }, issue: { type: 'string' },
    }, required: ['citation', 'issue'] } },
    single_source_risks: { type: 'array', items: { type: 'string' } },
    verdict: { type: 'string' },
  },
  required: ['unsupported_or_overstated', 'verdict'],
}

// ---- prompt builders ---------------------------------------------------
function filePrompt(path) {
  return `You are extracting evidence to help produce a credible, grounded answer to this question/task:
"${cfg.question}"

Read this file FULLY: ${path}.
${cfg.focus ? 'Extra focus: ' + cfg.focus + '\n' : ''}
Extract DISCRETE, atomic claims relevant to the question. For each: a clear statement; a short verbatim support_quote; citation (this file + approx line); a credibility rating (this is a provided/local source — rate by how directly the text supports the claim: high/medium/low) with a one-line reason; and topical tags. Be exhaustive but never invent — only claims the file actually supports. Fill gaps: relevant sub-questions this file does NOT answer. Output is consumed by a synthesis step — return data, not prose.`
}

function webPrompt(angle) {
  return `You are researching the web to help produce a credible, grounded answer to this question/task:
"${cfg.question}"

Your assigned angle (STAY in this lane so you don't overlap the other researchers): ${angle}

Use web search, then OPEN and READ the most credible sources you can find for THIS angle before extracting — prefer primary/authoritative sources over aggregators or SEO content. Extract DISCRETE, atomic claims relevant to the question. For each: a clear statement; a short support_quote from the source; citation = the source URL (+ title); a credibility rating (high/medium/low/unknown) with a one-line reason grounded in source type, author expertise, recency, and corroboration; and topical tags. Note publication dates when they matter. Do NOT include any claim you could not tie to a real source you actually read. Fill gaps: relevant sub-questions you could not find credible answers to. Output is consumed by a synthesis step — return data, not prose.`
}

// ---- extraction units --------------------------------------------------
const fileUnits = cfg.files.map(p => ({ label: `file:${base(p)}`, prompt: filePrompt(p) }))
const webCount = BREADTH_COUNT[cfg.web.breadth] || 0
const webUnits = cfg.web.enabled
  ? WEB_ANGLES.slice(0, webCount).map((angle, i) => ({ label: `web:angle${i + 1}`, prompt: webPrompt(angle) }))
  : []
const units = [...fileUnits, ...webUnits]

if (!cfg.question) log('WARNING: no question/topic provided in args — extraction will be unfocused.')
if (!units.length) {
  log('No sources to extract from — supply args.files and/or enable args.web. Aborting.')
  return { error: 'no_sources', cfg }
}

// ---- Extract -----------------------------------------------------------
phase('Extract')
log(`Extracting from ${fileUnits.length} file(s) + ${webUnits.length} web angle(s) for: "${cfg.question}"`)
const evidence = (await parallel(units.map(u => () =>
  agent(u.prompt, { label: u.label, phase: 'Extract', schema: EVIDENCE_SCHEMA })
))).filter(Boolean)
const claimCount = evidence.reduce((n, e) => n + ((e.claims && e.claims.length) || 0), 0)
log(`Gathered ${claimCount} claims from ${evidence.length} source(s)`)
if (!evidence.length) return { error: 'no_evidence', cfg }

// ---- Synthesize --------------------------------------------------------
phase('Synthesize')
const synthPrompt = `You are the SINGLE synthesis authority. Below are evidence inventories gathered INDEPENDENTLY from disjoint sources (files and/or distinct web angles). They overlap — DEDUPLICATE and CLUSTER them into one coherent result with NO double-counted points.

Question/task: "${cfg.question}"
Desired output kind: ${cfg.outputKind}

<evidence>
${JSON.stringify(evidence, null, 1)}
</evidence>

Produce:
1. summary: a tight overview answer.
2. key_findings[]: each with the point, a confidence (high/medium/low), an agreement label (consensus = multiple independent sources agree; contested = sources disagree; single_source = only one source), and the citations supporting it. Down-rank confidence for single-source or low-credibility claims.
3. contested[]: topics where sources disagree, with the competing positions.
4. gaps[]: important sub-questions the evidence does not answer.
5. deliverable: the actual finished output for the user, tailored to the question and outputKind (a report, a direct answer, or a structured taxonomy). Be credible and specific; attribute contested points rather than flattening them.

Ground everything in the evidence; do not invent. Return data.`
const draft = await agent(synthPrompt, { label: 'synthesize', phase: 'Synthesize', schema: SYNTH_SCHEMA })

// ---- Verify (parallel, adversarial) ------------------------------------
phase('Verify')
const filesList = cfg.files.length ? cfg.files.join(', ') : '(none — web-only run)'
const completenessPrompt = `You are an adversarial completeness critic. Below is a synthesized result for the question: "${cfg.question}". Assume it dropped or under-weighted something important — prove it.
${cfg.files.length ? 'Re-read the source files in full as needed: ' + filesList + '.' : ''}
${cfg.web.enabled ? 'You may run targeted web searches to check for missing angles, recent developments, or counter-evidence.' : ''}
List concrete missing points (with why each matters and a suggested source) and any under-weighted points.

<result>${JSON.stringify(draft, null, 1)}</result>
Return data.`
const credibilityPrompt = `You are an adversarial credibility & grounding verifier. Below is a synthesized result for the question: "${cfg.question}". For each key finding, check whether its citation ACTUALLY supports it (re-read cited files; ${cfg.web.enabled ? 'and re-fetch a sample of cited URLs' : ''}). Flag: claims that are unsupported or overstated; sources that are low-credibility (SEO/aggregator/anonymous/outdated) with the reason; and findings that rest on a single source where that's risky.

<result>${JSON.stringify(draft, null, 1)}</result>
Return data.`
const [completeness, credibility] = await parallel([
  () => agent(completenessPrompt, { label: 'completeness-critic', phase: 'Verify', schema: COMPLETENESS_SCHEMA }),
  () => agent(credibilityPrompt, { label: 'credibility-verifier', phase: 'Verify', schema: CREDIBILITY_SCHEMA }),
])

// ---- Reconcile ---------------------------------------------------------
phase('Reconcile')
const reconcilePrompt = `Produce the FINAL result by folding these critiques into the draft. Add the completeness critic's missing/under-weighted points (where valid). Fix or remove anything the credibility verifier flagged as unsupported, overstated, or resting on weak/single sources — or explicitly down-rank its confidence and say so. Keep it deduped and coherent. The deliverable must end with a short "Sources & confidence" note summarizing what is well-supported vs shaky. Output the SAME schema as the draft, now final.

<draft>${JSON.stringify(draft, null, 1)}</draft>
<completeness_critique>${JSON.stringify(completeness || {}, null, 1)}</completeness_critique>
<credibility_critique>${JSON.stringify(credibility || {}, null, 1)}</credibility_critique>
Return data.`
const final = await agent(reconcilePrompt, { label: 'final', phase: 'Reconcile', schema: SYNTH_SCHEMA })

return {
  question: cfg.question,
  claimCount,
  fileCount: fileUnits.length,
  webAngles: webUnits.length,
  final,
  completeness,
  credibility,
}
