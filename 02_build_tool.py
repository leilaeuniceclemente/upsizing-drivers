import json
with open("/home/claude/data_v3.json") as f:
    data = json.load(f)
data_json = json.dumps(data, ensure_ascii=False)

html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>Upsizing Decision Console</title>
<style>
  :root {
    --bg: #0f1117; --surface: #1a1d27; --surface2: #22263a; --border: #2e3350;
    --accent: #7c6af7; --accent2: #4ecdc4; --warn: #f7b731; --danger: #fc5c65;
    --ok: #26de81; --text: #e8eaf0; --muted: #8b90a7;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: var(--bg); color: var(--text); font-family: 'Inter','Segoe UI',sans-serif; font-size: 14px; line-height: 1.6; min-height: 100vh; }

  .header { background: var(--surface); border-bottom: 1px solid var(--border); padding: 20px 32px; display: flex; align-items: center; gap: 16px; }
  .header-icon { width: 36px; height: 36px; background: linear-gradient(135deg,var(--accent),var(--accent2)); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0; }
  .header-title { font-size: 17px; font-weight: 700; letter-spacing: -0.02em; }
  .header-sub { font-size: 12px; color: var(--muted); margin-top: 2px; }
  .header-badge { margin-left: auto; background: var(--surface2); border: 1px solid var(--border); border-radius: 20px; padding: 4px 12px; font-size: 11px; color: var(--muted); flex-shrink: 0; }

  .tabs { display: flex; border-bottom: 1px solid var(--border); background: var(--surface); padding: 0 32px; }
  .tab { padding: 14px 20px; font-size: 13px; font-weight: 500; cursor: pointer; border-bottom: 2px solid transparent; color: var(--muted); transition: all 0.18s; white-space: nowrap; }
  .tab:hover { color: var(--text); }
  .tab.active { color: var(--accent); border-color: var(--accent); }

  .main { padding: 28px 32px; max-width: 1200px; margin: 0 auto; }
  .panel { display: none; }
  .panel.active { display: block; }
  .section-label { font-size: 11px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); margin-bottom: 12px; }

  .card { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 20px; }

  .control-row { display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 24px; align-items: flex-end; }
  .control-group { display: flex; flex-direction: column; gap: 6px; }
  .control-group label { font-size: 11px; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.07em; }
  .toggle-group { display: flex; gap: 6px; flex-wrap: wrap; }
  .toggle { border-radius: 20px; padding: 7px 16px; font-size: 12px; font-weight: 500; cursor: pointer; border: 1px solid var(--border); background: var(--surface2); color: var(--muted); transition: all 0.15s; }
  .toggle:hover { color: var(--text); border-color: var(--accent); }
  .toggle.active { background: var(--accent); border-color: var(--accent); color: #fff; }

  .badge { display: inline-flex; align-items: center; gap: 4px; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }
  .badge-ok     { background: rgba(38,222,129,0.12);  color: var(--ok); }
  .badge-warn   { background: rgba(247,183,49,0.12);  color: var(--warn); }
  .badge-danger { background: rgba(252,92,101,0.12);  color: var(--danger); }

  .profile-row { display: flex; gap: 12px; flex-wrap: wrap; }
  .profile-stat { background: var(--surface2); border-radius: 8px; padding: 12px 16px; min-width: 120px; }
  .profile-stat .stat-val   { font-size: 17px; font-weight: 700; }
  .profile-stat .stat-label { font-size: 11px; color: var(--muted); margin-top: 2px; }

  .sulit-row { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }
  .sulit-label { font-size: 12px; width: 170px; color: var(--muted); flex-shrink: 0; }
  .sulit-bar-bg { flex: 1; height: 8px; background: var(--surface2); border-radius: 4px; overflow: hidden; }
  .sulit-bar-fill { height: 100%; border-radius: 4px; transition: width 0.45s cubic-bezier(.4,0,.2,1); }
  .sulit-val { font-size: 12px; font-weight: 700; width: 40px; text-align: right; }
  #sulit-verdict { margin-top: 14px; padding: 12px 16px; border-radius: 8px; font-size: 13px; font-weight: 600; }

  .barrier-callout { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 16px 0; }
  @media (max-width: 700px) { .barrier-callout { grid-template-columns: 1fr; } }
  .barrier-block { border-radius: 8px; padding: 16px 18px; border: 1px solid; }
  .barrier-block.primary   { background: rgba(252,92,101,0.07); border-color: rgba(252,92,101,0.3); }
  .barrier-block.secondary { background: rgba(247,183,49,0.07); border-color: rgba(247,183,49,0.25); }
  .barrier-rank { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px; }
  .barrier-block.primary   .barrier-rank { color: var(--danger); }
  .barrier-block.secondary .barrier-rank { color: var(--warn); }
  .barrier-name { font-size: 14px; font-weight: 700; margin-bottom: 6px; }
  .barrier-why  { font-size: 12px; color: var(--muted); line-height: 1.55; }

  .pillar-grid { display: grid; grid-template-columns: repeat(5,1fr); gap: 10px; margin-top: 16px; }
  @media (max-width: 1000px) { .pillar-grid { grid-template-columns: repeat(3,1fr); } }
  @media (max-width: 600px)  { .pillar-grid { grid-template-columns: 1fr 1fr; } }
  .pillar-card { border-radius: 8px; padding: 14px; border: 1px solid transparent; }
  .pillar-card.ok     { background: rgba(38,222,129,0.07);  border-color: rgba(38,222,129,0.2); }
  .pillar-card.warn   { background: rgba(247,183,49,0.07);  border-color: rgba(247,183,49,0.22); }
  .pillar-card.danger { background: rgba(252,92,101,0.07);  border-color: rgba(252,92,101,0.28); }
  .pillar-icon   { font-size: 20px; margin-bottom: 8px; }
  .pillar-name   { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px; }
  .pillar-card.ok     .pillar-name { color: var(--ok); }
  .pillar-card.warn   .pillar-name { color: var(--warn); }
  .pillar-card.danger .pillar-name { color: var(--danger); }
  .pillar-status { font-size: 12px; color: var(--muted); }
  .pillar-reco   { font-size: 11px; margin-top: 8px; padding: 7px 9px; border-radius: 5px; background: rgba(0,0,0,0.22); line-height: 1.5; color: var(--muted); }

  .exception-cards { display: grid; grid-template-columns: repeat(3,1fr); gap: 12px; margin-top: 4px; }
  @media (max-width: 700px) { .exception-cards { grid-template-columns: 1fr; } }
  .exception-card { background: var(--surface2); border-radius: 8px; padding: 14px; border: 1px solid var(--border); }
  .exc-trigger { font-size: 12px; font-weight: 700; color: var(--accent2); margin-bottom: 4px; }
  .exc-desc    { font-size: 12px; color: var(--muted); }
  .exc-cat     { font-size: 11px; color: var(--accent); margin-top: 6px; }

  .divider { border: none; border-top: 1px solid var(--border); margin: 24px 0; }

  .tip-box { background: rgba(124,106,247,0.07); border: 1px solid rgba(124,106,247,0.2); border-radius: 8px; padding: 12px 16px; font-size: 12px; color: var(--muted); margin-top: 16px; }
  .tip-box strong { color: var(--accent); }

  .context-bar { background: var(--surface2); border-radius: 8px; padding: 14px 18px; display: flex; gap: 24px; margin-bottom: 20px; flex-wrap: wrap; }
  .ctx-item { display: flex; flex-direction: column; gap: 2px; }
  .ctx-label { font-size: 10px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.07em; }
  .ctx-val   { font-size: 13px; font-weight: 600; }

  .brand-compare { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-top: 4px; }
  @media (max-width: 800px) { .brand-compare { grid-template-columns: 1fr; } }
  .brand-card { background: var(--surface2); border-radius: 8px; padding: 16px; border: 1px solid var(--border); }
  .brand-card.leader { border-color: rgba(124,106,247,0.4); }
  .brand-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
  .brand-name { font-size: 14px; font-weight: 700; }
  .brand-pos.leader     { font-size: 11px; font-weight: 600; color: var(--ok); }
  .brand-pos.challenger { font-size: 11px; font-weight: 600; color: var(--warn); }
  .brand-pos.niche      { font-size: 11px; font-weight: 600; color: var(--muted); }
  .dim-row { display: flex; align-items: center; gap: 8px; margin-bottom: 7px; }
  .dim-label { font-size: 11px; color: var(--muted); width: 130px; flex-shrink: 0; }
  .dim-bar-bg { flex: 1; height: 5px; background: rgba(255,255,255,0.07); border-radius: 3px; overflow: hidden; }
  .dim-bar-fill { height: 100%; border-radius: 3px; background: linear-gradient(90deg,var(--accent),var(--accent2)); }
  .dim-score { font-size: 11px; font-weight: 700; width: 16px; text-align: right; color: var(--muted); }
  .total-score { margin-top: 10px; padding-top: 10px; border-top: 1px solid var(--border); display: flex; justify-content: space-between; font-size: 12px; align-items: center; }
  .total-val { font-weight: 800; font-size: 15px; color: var(--accent); }

  .principle-row { display: grid; grid-template-columns: 210px 1fr 52px; gap: 0; align-items: center; border-bottom: 1px solid var(--border); padding: 14px 0; }
  .principle-row:last-child { border-bottom: none; }
  .principle-num  { font-size: 22px; font-weight: 800; color: var(--accent); opacity: 0.35; display: inline; margin-right: 8px; }
  .principle-name { font-size: 13px; font-weight: 700; display: inline; }
  .principle-desc { font-size: 12px; color: var(--muted); padding: 0 20px; }
  .score-circle { width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 800; margin-left: auto; }
  .sc-danger { background: rgba(252,92,101,0.15); color: var(--danger); }
  .sc-warn   { background: rgba(247,183,49,0.15);  color: var(--warn); }
  .sc-ok     { background: rgba(38,222,129,0.15);  color: var(--ok); }

  .gap-table { width: 100%; border-collapse: collapse; font-size: 12px; }
  .gap-table th { font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.07em; color: var(--muted); padding: 8px 12px; text-align: left; border-bottom: 1px solid var(--border); }
  .gap-table td { padding: 10px 12px; border-bottom: 1px solid rgba(255,255,255,0.04); }
  .gap-table tr:last-child td { border-bottom: none; }
  .gap-table tr:hover td { background: rgba(255,255,255,0.02); }

  .footer { text-align: center; padding: 20px 32px; font-size: 11px; color: var(--muted); border-top: 1px solid var(--border); margin-top: 48px; }
</style>
</head>
<body>

<div class="header">
  <div class="header-icon">📦</div>
  <div>
    <div class="header-title">Upsizing Decision Console</div>
    <div class="header-sub">Consumer barrier mapping & growth playbook · Philippine FMCG · Synthetic data</div>
  </div>
  <div class="header-badge">Synthetic · noindex</div>
</div>

<div class="tabs">
  <div class="tab active" onclick="switchTab('consumer')">Consumer Barrier Scan</div>
  <div class="tab" onclick="switchTab('playbook')">Growth Playbook</div>
</div>

<div class="main">

  <!-- TAB 1 -->
  <div class="panel active" id="panel-consumer">
    <div class="control-row">
      <div class="control-group">
        <label>Shopper Segment</label>
        <div class="toggle-group" id="seg-grp">
          <button class="toggle active" onclick="setSeg('daily',this)">Daily Wage</button>
          <button class="toggle" onclick="setSeg('semi',this)">Semi-Monthly</button>
          <button class="toggle" onclick="setSeg('monthly',this)">Monthly</button>
        </div>
      </div>
      <div class="control-group">
        <label>Category</label>
        <div class="toggle-group" id="cat-grp">
          <button class="toggle active" onclick="setCat('cat1',this)">Category A</button>
          <button class="toggle" onclick="setCat('cat2',this)">Category B</button>
          <button class="toggle" onclick="setCat('cat3',this)">Category C</button>
          <button class="toggle" onclick="setCat('cat4',this)">Category D</button>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="section-label">Shopper Profile</div>
      <div class="profile-row" id="profile-stats"></div>
    </div>

    <div class="card" style="margin-top:16px">
      <div class="section-label">The "Sulit" Test — Is this big pack worth it?</div>
      <div style="font-size:12px;color:var(--muted);margin-bottom:14px;">
        Shoppers evaluate big packs against two conditions simultaneously. Both must pass for a purchase to feel <strong style="color:var(--text)">sulit</strong> (genuinely worth the money).
      </div>
      <div id="sulit-meter"></div>
      <div id="sulit-verdict"></div>
    </div>

    <div style="margin-top:16px">
      <div class="section-label">Category Barriers — What's stopping the switch</div>
      <div class="barrier-callout" id="barrier-callout"></div>
    </div>

    <div class="card">
      <div style="display:flex;gap:12px;margin-bottom:14px;font-size:12px;flex-wrap:wrap;align-items:center;">
        <span style="color:var(--muted)">Pillars by phase:</span>
        <span style="background:rgba(124,106,247,0.15);color:var(--accent);padding:2px 9px;border-radius:20px;font-size:11px;font-weight:600;">Drive Trial → Price Point · Value Comms</span>
        <span style="background:rgba(78,205,196,0.15);color:var(--accent2);padding:2px 9px;border-radius:20px;font-size:11px;font-weight:600;">Drive Repeat → Dosage · Mileage · Convenience</span>
      </div>
      <div class="pillar-grid" id="pillar-grid"></div>
    </div>

    <hr class="divider">

    <div class="section-label">When shoppers override the small-pack default</div>
    <div class="exception-cards" id="exception-cards"></div>

    <div class="tip-box">
      <strong>Key finding:</strong> ~60% of shopping trips at the trade-up price point still end in small-pack purchases.
      Fixing the #1 barrier per category unlocks the largest conversion opportunity — but driving repeat requires all three
      Repeat pillars to clear, especially dosage guidance in categories where consumers have no reliable sensory cue for correct usage.
    </div>
  </div>

  <!-- TAB 2 -->
  <div class="panel" id="panel-playbook">
    <div class="control-row">
      <div class="control-group">
        <label>Category</label>
        <div class="toggle-group" id="play-cat-grp">
          <button class="toggle active" onclick="setPlayCat('cat1',this)">Category A</button>
          <button class="toggle" onclick="setPlayCat('cat2',this)">Category B</button>
          <button class="toggle" onclick="setPlayCat('cat3',this)">Category C</button>
          <button class="toggle" onclick="setPlayCat('cat4',this)">Category D</button>
        </div>
      </div>
    </div>

    <div class="context-bar" id="play-context"></div>

    <div class="section-label">Brand Upsizing Scorecard (Synthetic)</div>
    <div class="brand-compare" id="brand-compare"></div>

    <hr class="divider">

    <div class="section-label">The 5 Growth Principles</div>
    <div class="card" id="principles-detail"></div>

    <div style="margin-top:16px">
      <div class="section-label">Priority Gap — Leader vs. Category Average</div>
      <div class="card">
        <table class="gap-table">
          <thead>
            <tr>
              <th>Principle</th><th>Leader</th><th>Cat. Avg</th><th>Gap</th><th>Priority</th>
            </tr>
          </thead>
          <tbody id="gap-tbody"></tbody>
        </table>
      </div>
    </div>

    <div class="tip-box" id="play-tip"></div>
  </div>

</div>

<div class="footer">
  Synthetic data · All brand names, category names, and scores are illustrative · No proprietary or confidential data included
</div>

<script>
const DATA = """ + data_json + r""";

const PILLAR_DEFS = [
  {
    id:"price_point", icon:"💰", label:"Price Point", phase:"trial",
    generic:{
      ok:     {status:"Big pack sits within the shopper's typical category budget", reco:"Maintain the entry price; monitor as costs shift to avoid drifting above the accessible range."},
      warn:   {status:"Borderline — shoppers may hesitate at the price step-up", reco:"Use a promotional price to close the gap; communicate savings explicitly on-pack."},
      danger: {status:"Price too far from budget — most shoppers auto-reject at shelf", reco:"Introduce an entry big pack priced near two weeks' worth of small packs, or run a sustained promo price to establish the habit."},
    },
    catOverride:{
      cat3:{
        ok:     {status:"Big pack sits in the price range where most trips occur", reco:"Protect this entry point; resist increases that push above the accessible band."},
        warn:   {status:"Premium format priced above where most shopping trips occur", reco:"Explore a smaller entry format at an accessible price point to capture more trip occasions."},
        danger: {status:"Premium format priced above the range of 95%+ of shopping trips — invisible to most shoppers", reco:"Launch an entry-tier format at the accessible price band; treat the premium format as an aspirational second tier."},
      },
      cat4:{
        ok:     {status:"Bundle total price within shopper's reach", reco:"Focus on making the per-unit savings visible — the price fit is there but shoppers aren't seeing it."},
        warn:   {status:"Bundle total price feels high despite per-unit savings", reco:"Consider a smaller starter bundle as a stepping stone; lower upfront commitment, same savings logic."},
        danger: {status:"Bundle sticker price anchors high — shoppers default to single unit without comparing", reco:"Add a prominent 'Save ₱XX vs. buying singles' shelf callout; make the savings legible before the price registers."},
      },
    },
  },
  {
    id:"value_comms", icon:"🏷️", label:"Value Comms", phase:"trial",
    generic:{
      ok:     {status:"On-pack clearly shows savings and how many uses the big pack delivers", reco:"Test absolute peso savings vs. percentage — absolute typically reads faster at shelf."},
      warn:   {status:"Some comms exist but savings aren't immediately legible", reco:"Shift to absolute peso saved; add small-pack equivalent count prominently on front panel."},
      danger: {status:"No mileage or savings claim — shopper can't justify the trade-up at a glance", reco:"Add 'Equivalent to X small packs' on the front panel; consider a distinctive name for the big format to make it feel like a separate, deliberate choice."},
    },
    catOverride:{
      cat3:{
        ok:     {status:"Big pack clearly communicates its small-pack equivalent", reco:"Reinforce the mileage claim in media to close the 'it runs out faster' perception gap."},
        warn:   {status:"Pack has no small-pack count — shoppers don't know what they're getting", reco:"Add a small-pack equivalence claim prominently on the front panel."},
        danger: {status:"No on-pack mileage claim — shoppers who misjudge pack duration on first use rarely come back", reco:"Equivalence count on front panel is the single highest-leverage fix; pair with a dosage marking inside the pack."},
      },
      cat4:{
        ok:     {status:"Per-unit savings vs. single format clearly visible", reco:"Ensure the claim stays accurate as prices change; audit quarterly."},
        warn:   {status:"Discount exists but isn't legible enough at a glance", reco:"Shift from percentage callout to absolute peso saved — peso savings reads faster."},
        danger: {status:"Shopper sees a higher total price and stops there — per-unit savings are invisible without deliberate comparison", reco:"Make savings legible in 2 seconds: large peso amount on front, not a percentage. Add 'X units for the price of Y' framing."},
      },
    },
  },
  {
    id:"dosage", icon:"🧪", label:"Dosage", phase:"repeat",
    generic:{
      ok:     {status:"Dosage is intuitive or physically guided", reco:"Maintain the dosage cue; reinforce via packaging."},
      warn:   {status:"Some overdosing risk — guide present but not prominent", reco:"Move dosage marking to a more visible location; add a visual reference."},
      danger: {status:"No dosage cue — consumers use product until a sensory signal appears, which indicates underdosing not overdosing", reco:"Add a physical measure (markings, measuring cap, or dose indicator) so shoppers have a clear stop point."},
    },
    catOverride:{
      cat1:{
        ok:     {status:"Shoppers correctly dose the big pack", reco:"Reinforce correct dosing via pack illustration; add a measuring tool if not already included."},
        warn:   {status:"Shoppers use a sensory cue that signals underdosing — not a reliable upper limit", reco:"Add measurement markings and a simple dosing guide on the side panel."},
        danger: {status:"The sensory cue shoppers rely on only indicates they haven't used too little — there's no signal for too much. Consumption runs roughly 2× intended, cutting pack duration in half.", reco:"Include a measuring tool and dosing guide; educate at point of sale that the familiar sensory cue is not a dosing signal."},
      },
      cat2:{
        ok:     {status:"Shoppers correctly dose the large-format pack", reco:"Maintain dosing indicator; consider an illustrated guide for first-time users."},
        warn:   {status:"Shoppers add product until they detect a scent — which only signals underdosing", reco:"Add a cap or closure with a visible fill line; a single clear marking reduces overdosing significantly."},
        danger: {status:"The scent-detection cue only tells shoppers they haven't used enough — there's no upper limit signal, so consumption runs 40–60% above intended levels", reco:"Dosing line on the closure plus an illustrated guide; pair with a repeat-use education moment at first purchase."},
      },
    },
  },
  {
    id:"mileage", icon:"📅", label:"Lasts to Payday", phase:"repeat",
    generic:{
      ok:     {status:"Big pack outlasts small-pack equivalent to next payday", reco:"Communicate this explicitly on-pack: 'Covers your full fortnight' or equivalent."},
      warn:   {status:"Borderline — pack may run short if shopper overdoses", reco:"Ensure entry pack size equals or exceeds the typical small-pack bundle; pair with dosage fix."},
      danger: {status:"Pack runs out before next payday → shopper tops up with small packs at higher unit cost → big pack feels more expensive in hindsight", reco:"Resize entry pack to match at least two weeks of small-pack usage at the correct dose; dosage fix is a prerequisite."},
    },
    catOverride:{
      cat1:{
        ok:     {status:"Big pack lasts the full period between paydays", reco:"Communicate duration on-pack with small-pack equivalence claim."},
        warn:   {status:"Big pack covers the period but only if shopper doses correctly — overdosing risk is real", reco:"Entry pack size should exceed the typical small-pack bundle; dosage fix is prerequisite."},
        danger: {status:"Overdosed packs run out in half the expected time. Shoppers top up with small packs and conclude the big pack was expensive.", reco:"Increase entry pack size to cover two weeks at the correct dose; make dosing guidance prominent and paired."},
      },
    },
  },
  {
    id:"convenience", icon:"🏡", label:"Convenience", phase:"repeat",
    generic:{
      ok:     {status:"Easier to store and use than small packs in a typical home", reco:"Highlight convenience as a trial message — it's a pull factor, not just a retention factor."},
      warn:   {status:"Adequate but not clearly better than small packs", reco:"Test a stand-up base or resealable closure; small format changes have outsized impact in cramped storage."},
      danger: {status:"Spills, hard to store, or too bulky — shoppers revert to small packs after one poor experience", reco:"Resealable closure or stable base is the minimum viable fix; explore a compact form factor for small households."},
    },
    catOverride:{
      cat2:{
        ok:     {status:"Large-format pack stores cleanly without spill risk", reco:"Feature the resealable closure in media — convenience is an underused trial driver in this category."},
        warn:   {status:"Pack can tip in a crowded usage area; some spill risk", reco:"Add a resealable closure on entry-size packs; this single feature resolves the #1 repeat barrier."},
        danger: {status:"Packs without resealable closures tip in cramped home spaces — one spill erases the value proposition and sends shoppers back to small packs permanently", reco:"Resealable closure on all entry packs is the minimum viable fix; explore a flat-base design."},
      },
      cat1:{
        ok:     {status:"Big pack stores and dispenses cleanly", reco:"Maintain; explore a resealable closure for premium tier."},
        warn:   {status:"Big pack is harder to store than a stack of small packs in small homes", reco:"Explore a stand-up base and reclosable closure; test in consumer home placement."},
        danger: {status:"Big packs that don't stand independently are harder to store than small packs in small homes — a practical friction that accelerates reversion", reco:"Stand-up base and reclosable closure are the priority fixes; the big pack should feel like an upgrade, not a compromise."},
      },
    },
  },
];

const DIMS = ["portfolio","pack_comms","pricing","distribution","atl_btl"];
const DIM_LABELS = {"portfolio":"Portfolio Coverage","pack_comms":"Pack Communication","pricing":"Price Advantage","distribution":"Shelf Availability","atl_btl":"Media & In-Store"};

let activeSeg = "daily", activeCat = "cat1", activePlayCat = "cat1";

function switchTab(t) {
  document.querySelectorAll(".tab").forEach((el,i)=>el.classList.toggle("active",["consumer","playbook"][i]===t));
  document.querySelectorAll(".panel").forEach(p=>p.classList.remove("active"));
  document.getElementById(`panel-${t}`).classList.add("active");
}
function setSeg(id,el) {
  activeSeg=id;
  document.getElementById("seg-grp").querySelectorAll(".toggle").forEach(t=>t.classList.remove("active"));
  el.classList.add("active");
  renderConsumer();
}
function setCat(id,el) {
  activeCat=id;
  document.getElementById("cat-grp").querySelectorAll(".toggle").forEach(t=>t.classList.remove("active"));
  el.classList.add("active");
  renderConsumer();
}
function setPlayCat(id,el) {
  activePlayCat=id;
  document.getElementById("play-cat-grp").querySelectorAll(".toggle").forEach(t=>t.classList.remove("active"));
  el.classList.add("active");
  renderPlaybook();
}

function getPillarText(p, barrierVal, catId) {
  const lvl = barrierVal===2?"ok":barrierVal===1?"warn":"danger";
  return p.catOverride?.[catId]?.[lvl] || p.generic[lvl];
}

function barColor(v) { return v>0.65?"var(--ok)":v>0.35?"var(--warn)":"var(--danger)"; }

function renderConsumer() {
  const seg = DATA.segments.find(s=>s.id===activeSeg);
  const cat = DATA.categories.find(c=>c.id===activeCat);
  const barriers = cat.barriers;

  document.getElementById("profile-stats").innerHTML = `
    <div class="profile-stat"><div class="stat-val">${seg.pct}%</div><div class="stat-label">Share of shoppers</div></div>
    <div class="profile-stat"><div class="stat-val">${seg.budget_range}</div><div class="stat-label">Typical category budget</div></div>
    <div class="profile-stat"><div class="stat-val">${seg.payday_cycle}</div><div class="stat-label">Payday cycle</div></div>
    <div class="profile-stat"><div class="stat-val">${seg.sari_sari_reliance}</div><div class="stat-label">Neighborhood store reliance</div></div>
    <div class="profile-stat">
      <div class="stat-val" style="color:${seg.upsizing_readiness==="High"?"var(--ok)":"var(--danger)"}">${seg.upsizing_readiness}</div>
      <div class="stat-label">Upsizing readiness</div>
    </div>`;

  const segMult = activeSeg==="daily"?0.5:activeSeg==="semi"?0.85:1.0;
  const priceAdj = Math.min(barriers.price_point/2*segMult,1);
  const mileAdj  = Math.min(barriers.mileage/2*(activeSeg==="daily"?0.6:1.0),1);

  document.getElementById("sulit-meter").innerHTML = `
    <div class="sulit-row">
      <div class="sulit-label">💰 Price fits budget</div>
      <div class="sulit-bar-bg"><div class="sulit-bar-fill" style="width:${priceAdj*100}%;background:${barColor(priceAdj)}"></div></div>
      <div class="sulit-val" style="color:${barColor(priceAdj)}">${Math.round(priceAdj*100)}%</div>
    </div>
    <div class="sulit-row">
      <div class="sulit-label">📅 Lasts to next payday</div>
      <div class="sulit-bar-bg"><div class="sulit-bar-fill" style="width:${mileAdj*100}%;background:${barColor(mileAdj)}"></div></div>
      <div class="sulit-val" style="color:${barColor(mileAdj)}">${Math.round(mileAdj*100)}%</div>
    </div>`;

  const bothPass = priceAdj>0.65&&mileAdj>0.65, onePass=priceAdj>0.45||mileAdj>0.45;
  const vEl = document.getElementById("sulit-verdict");
  if (bothPass) {
    vEl.style.cssText="background:rgba(38,222,129,0.08);border:1px solid rgba(38,222,129,0.25);color:var(--ok)";
    vEl.innerHTML=`✓ Sulit — This segment is primed for big packs in ${cat.label}. Both conditions are likely met; remaining barriers sit in the repeat phase.`;
  } else if (onePass) {
    vEl.style.cssText="background:rgba(247,183,49,0.08);border:1px solid rgba(247,183,49,0.25);color:var(--warn)";
    vEl.innerHTML=`⚠ Borderline — One Sulit condition is at risk for this segment. A promo price, pack resize, or dosage fix may be needed before the switch sticks.`;
  } else {
    vEl.style.cssText="background:rgba(252,92,101,0.08);border:1px solid rgba(252,92,101,0.25);color:var(--danger)";
    vEl.innerHTML=`✗ Not yet Sulit — Small packs remain the rational choice for this segment in ${cat.label}. Both conditions need to be addressed before big packs can compete.`;
  }

  document.getElementById("barrier-callout").innerHTML = `
    <div class="barrier-block primary">
      <div class="barrier-rank">🔴 #1 Barrier</div>
      <div class="barrier-name">${cat.barrier_1}</div>
      <div class="barrier-why">${cat.barrier_1_why}</div>
    </div>
    <div class="barrier-block secondary">
      <div class="barrier-rank">🟡 #2 Barrier</div>
      <div class="barrier-name">${cat.barrier_2}</div>
      <div class="barrier-why">${cat.barrier_2_why}</div>
    </div>`;

  document.getElementById("pillar-grid").innerHTML = PILLAR_DEFS.map(p=>{
    const val=barriers[p.id], cls=val===2?"ok":val===1?"warn":"danger";
    const txt=getPillarText(p,val,activeCat);
    const pill=p.phase==="trial"
      ?`<span style="font-size:10px;background:rgba(124,106,247,0.15);color:var(--accent);padding:1px 6px;border-radius:10px;margin-left:4px">Trial</span>`
      :`<span style="font-size:10px;background:rgba(78,205,196,0.15);color:var(--accent2);padding:1px 6px;border-radius:10px;margin-left:4px">Repeat</span>`;
    return `<div class="pillar-card ${cls}">
      <div class="pillar-icon">${p.icon}</div>
      <div class="pillar-name">${p.label}${pill}</div>
      <div class="pillar-status">${txt.status}</div>
      <div class="pillar-reco">${txt.reco}</div>
    </div>`;
  }).join("");

  document.getElementById("exception-cards").innerHTML = DATA.exceptions.map(e=>`
    <div class="exception-card">
      <div class="exc-trigger">⚡ ${e.trigger}</div>
      <div class="exc-desc">${e.description}</div>
      <div class="exc-cat">e.g. ${e.example_category}</div>
    </div>`).join("");
}

function renderPlaybook() {
  const cat = DATA.categories.find(c=>c.id===activePlayCat);
  const catBrands = DATA.brands.filter(b=>b.category_id===activePlayCat);

  document.getElementById("play-context").innerHTML = `
    <div class="ctx-item"><div class="ctx-label">Category</div><div class="ctx-val">${cat.label}</div></div>
    <div class="ctx-item"><div class="ctx-label">Small format</div><div class="ctx-val">${cat.small_format}</div></div>
    <div class="ctx-item"><div class="ctx-label">Big pack format</div><div class="ctx-val">${cat.big_format}</div></div>
    <div class="ctx-item"><div class="ctx-label">Est. small pack share</div><div class="ctx-val" style="color:var(--danger)">${cat.small_share}%</div></div>
    <div class="ctx-item"><div class="ctx-label">#1 barrier</div><div class="ctx-val" style="color:var(--warn)">${cat.barrier_1}</div></div>`;

  document.getElementById("brand-compare").innerHTML = catBrands.map(b=>`
    <div class="brand-card ${b.market_position.toLowerCase()}">
      <div class="brand-header">
        <div class="brand-name">${b.brand}</div>
        <div class="brand-pos ${b.market_position.toLowerCase()}">${b.market_position}</div>
      </div>
      ${DIMS.map(d=>`
        <div class="dim-row">
          <div class="dim-label">${DIM_LABELS[d]}</div>
          <div class="dim-bar-bg"><div class="dim-bar-fill" style="width:${b[d]/5*100}%"></div></div>
          <div class="dim-score">${b[d]}</div>
        </div>`).join("")}
      <div class="total-score"><span style="color:var(--muted)">Total</span><span class="total-val">${b.total}/25</span></div>
    </div>`).join("");

  const catAvg = DIMS.reduce((acc,d)=>{acc[d]=Math.round(catBrands.reduce((s,b)=>s+b[d],0)/catBrands.length*10)/10;return acc;},{});
  document.getElementById("principles-detail").innerHTML = DATA.growth_principles.map((p,i)=>{
    const avg=catAvg[p.id]||0, cls=avg>=4?"sc-ok":avg>=3?"sc-warn":"sc-danger";
    return `<div class="principle-row">
      <div><span class="principle-num">${String(i+1).padStart(2,"0")}</span><span class="principle-name">${p.label}</span></div>
      <div class="principle-desc">${p.description}</div>
      <div><div class="score-circle ${cls}" style="float:right">${avg}</div><div style="font-size:10px;color:var(--muted);text-align:right;margin-top:4px">avg</div></div>
    </div>`;
  }).join("");

  const leader = catBrands.find(b=>b.market_position==="Leader");
  document.getElementById("gap-tbody").innerHTML = DIMS.map(d=>{
    const ls=leader[d], avg=catAvg[d], gap=ls-avg;
    const label=DATA.growth_principles.find(p=>p.id===d)?.label||d;
    const priority=gap>1.5?"High":gap>0.7?"Medium":"Low";
    const pc=priority==="High"?"badge-danger":priority==="Medium"?"badge-warn":"badge-ok";
    const sc=ls>=4?"sc-ok":ls>=3?"sc-warn":"sc-danger";
    return `<tr>
      <td style="font-weight:600">${label}</td>
      <td><div class="score-circle ${sc}" style="width:28px;height:28px;font-size:12px;display:inline-flex">${ls}</div></td>
      <td style="color:var(--muted)">${avg}</td>
      <td style="color:${gap>1?"var(--ok)":"var(--muted)"}">+${gap.toFixed(1)}</td>
      <td><span class="badge ${pc}">${priority}</span></td>
    </tr>`;
  }).join("");

  document.getElementById("play-tip").innerHTML = `
    <strong>Category note:</strong> In ${cat.label}, the primary conversion barrier is <strong style="color:var(--accent)">${cat.barrier_1}</strong>.
    Brands that address this first will disproportionately capture conversion from the ~${cat.small_share}% of volume still in small formats.
    ${cat.exception_note}`;
}

renderConsumer();
renderPlaybook();
</script>
</body>
</html>"""

with open("/home/claude/index_v3.html","w",encoding="utf-8") as f:
    f.write(html)
print(f"v3 built — {len(html):,} chars")
