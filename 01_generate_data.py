import json, random
random.seed(42)

segments = [
    {"id": "daily",   "label": "Daily Wage Earner",   "pct": 26, "budget_range": "₱50–₱99",   "payday_cycle": "Daily",   "sari_sari_reliance": "High",   "upsizing_readiness": "Low"},
    {"id": "semi",    "label": "Semi-Monthly Earner", "pct": 44, "budget_range": "₱100–₱199", "payday_cycle": "14 days", "sari_sari_reliance": "Medium", "upsizing_readiness": "High"},
    {"id": "monthly", "label": "Monthly Earner",      "pct": 30, "budget_range": "₱150–₱249", "payday_cycle": "30 days", "sari_sari_reliance": "Low",    "upsizing_readiness": "High"},
]

# Category labels: abstract IDs, no real names
# Format language: "small pack" / "bulk pack" / "premium format" / "bundle pack" — all generic
categories = [
    {
        "id": "cat1", "label": "Category A",
        "small_format": "small pack", "big_format": "bulk pack",
        "small_share": 70,
        "barrier_1": "Dosage guidance",
        "barrier_1_why": "Shoppers rely on a sensory cue (visible lather) to judge how much to use — but this signal only indicates underdosing, not overdosing. With no upper limit cue, consumption runs roughly twice the intended amount, cutting expected pack duration in half.",
        "barrier_2": "Pack duration to next payday",
        "barrier_2_why": "When the bulk pack runs out before next payday, shoppers top up with small packs from a nearby store at a higher per-unit cost. This experience makes the big pack feel more expensive in hindsight, even when the economics favor it.",
        "exception_note": "Shoppers who receive explicit dosing guidance — via pack markings or in-home demonstration — show significantly higher repeat rates.",
        "barriers": {"price_point": 2, "value_comms": 0, "dosage": 0, "mileage": 0, "convenience": 1}
    },
    {
        "id": "cat2", "label": "Category B",
        "small_format": "small pack", "big_format": "large-format pack",
        "small_share": 60,
        "barrier_1": "Storage and handling convenience",
        "barrier_1_why": "Large-format packs without resealable closures tip over easily in cramped home usage areas — especially in households with children or pets. A single spill wastes a meaningful share of the pack and eliminates the value-for-money rationale, sending the shopper back to small packs.",
        "barrier_2": "Dosage guidance",
        "barrier_2_why": "Shoppers add product until they detect a scent in the rinse — but this only signals underdosing. There is no corresponding cue for overdosing, so consumption runs 40–60% above intended levels.",
        "exception_note": "Packs with resealable closures see meaningfully higher repeat. The closure resolves the #1 barrier before the shopper encounters it.",
        "barriers": {"price_point": 2, "value_comms": 0, "dosage": 0, "mileage": 1, "convenience": 0}
    },
    {
        "id": "cat3", "label": "Category C",
        "small_format": "small pack", "big_format": "standard or premium format",
        "small_share": 55,
        "barrier_1": "Entry price point",
        "barrier_1_why": "The premium big-pack format is priced above the range where the vast majority of shopping trips occur. Fewer than 5% of trips are at that price tier, meaning most shoppers auto-reject the upgrade at shelf without comparing value.",
        "barrier_2": "Value communication",
        "barrier_2_why": "Shoppers who have tried the standard big-pack format report it ran out faster than expected. Without a clear on-pack claim quantifying how many small packs it replaces, the value proposition is invisible — and a single poor experience is hard to reverse.",
        "exception_note": "Standard big-pack formats at accessible price points see stronger trial. A secondary premium tier can coexist once the entry format builds the habit.",
        "barriers": {"price_point": 0, "value_comms": 0, "dosage": 1, "mileage": 0, "convenience": 1}
    },
    {
        "id": "cat4", "label": "Category D",
        "small_format": "single unit", "big_format": "bundle pack",
        "small_share": 45,
        "barrier_1": "Value communication",
        "barrier_1_why": "Most shoppers already know bundle packs last longer — the mileage case is intuitive. The barrier is legibility: the per-unit savings aren't visible enough at a glance, so shoppers anchor on the higher total price and default to the single unit out of habit.",
        "barrier_2": "Upfront price perception",
        "barrier_2_why": "Even when the per-unit math favors the bundle, the total sticker price reads as a larger outlay than a single unit. Shoppers who could afford the bundle still choose singles because the upfront number feels larger.",
        "exception_note": "Brands that make the peso savings legible in under two seconds at shelf — through absolute amount callouts rather than percentage discounts — convert significantly more first-time bundle buyers.",
        "barriers": {"price_point": 0, "value_comms": 0, "dosage": 2, "mileage": 2, "convenience": 2}
    },
]

growth_principles = [
    {"id": "portfolio",    "label": "Portfolio Coverage",         "description": "Big packs present at the price points where most shopping trips occur. In most categories, 60–70% of trips fall in the ₱50–₱199 band — brands without an entry pack here are invisible to the majority of shoppers."},
    {"id": "pack_comms",   "label": "Pack Communication",         "description": "On-pack claims show absolute savings vs. small packs AND how many uses the big pack delivers (e.g. 'More than 30 small packs'). Distinctive pack names — 'Value Pack', 'Family Size' — help shoppers anchor the bigger size as a different, intentional choice."},
    {"id": "pricing",      "label": "Price per Unit Advantage",   "description": "Big pack price-per-unit must be meaningfully lower than the small pack equivalent. Brands offering ≥10% savings per unit grow faster; those offering <5% see weak conversion even with high shelf presence."},
    {"id": "distribution", "label": "Shelf Availability",        "description": "Winning brands expand big pack store coverage faster than small pack coverage. Where small packs plateau, leaders actively push big packs into more outlets — making them findable before the shopper reverts to the familiar small format."},
    {"id": "atl_btl",      "label": "Media & In-Store Alignment", "description": "Brands that show the same hero SKU across advertising and shelf grow faster. When a shopper sees a big pack in media but can't find it in-store — or signage shows a different pack — the conversion chain breaks."},
]

exceptions = [
    {"trigger": "Convenience advantage",   "description": "The big pack avoids spillage, storage mess, or handling friction that the small pack creates — the format itself removes a friction point.", "example_category": "Liquid categories with small sachet variants"},
    {"trigger": "Small visible price gap", "description": "When the step-up price feels small relative to the extra volume, shoppers anchor on the quantity gain rather than the peso outlay.", "example_category": "Categories with multipack vs. single-unit pricing"},
    {"trigger": "Low small-pack availability nearby", "description": "When neighborhood stores don't reliably stock the small format, shoppers pre-stock the large size at a supermarket rather than risk running out.", "example_category": "Categories where sari-sari stocking is thin"},
]

brands = []
configs_base = [
    ("Brand A", "Leader",     {"portfolio":4,"pack_comms":3,"pricing":4,"distribution":4,"atl_btl":3}),
    ("Brand B", "Challenger", {"portfolio":2,"pack_comms":1,"pricing":2,"distribution":3,"atl_btl":1}),
    ("Brand C", "Niche",      {"portfolio":2,"pack_comms":1,"pricing":2,"distribution":2,"atl_btl":1}),
]
overrides = {
    "cat2": {"portfolio":4,"pack_comms":4,"pricing":3,"distribution":5,"atl_btl":5},
    "cat3": {"portfolio":5,"pack_comms":3,"pricing":4,"distribution":5,"atl_btl":5},
    "cat4_B": {"pricing":4,"distribution":3},
}
for cat in categories:
    for i, (name, pos, base_scores) in enumerate(configs_base):
        scores = dict(base_scores)
        if i == 0:
            if cat["id"] in overrides:
                scores.update(overrides[cat["id"]])
        elif i == 1 and f"{cat['id']}_B" in overrides:
            scores.update(overrides[f"{cat['id']}_B"])
        brands.append({
            "brand": name, "category_id": cat["id"], "category_label": cat["label"],
            **scores, "total": sum(scores.values()), "market_position": pos,
        })

out = {"segments": segments, "categories": categories, "exceptions": exceptions, "growth_principles": growth_principles, "brands": brands}
with open("/home/claude/data_v3.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

print("v3 data written.")
for c in categories:
    print(f"  {c['label']}: #1={c['barrier_1']} | #2={c['barrier_2']}")
