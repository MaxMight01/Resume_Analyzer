def compute_score(analysis: dict) -> dict:
    raw = analysis.get("score_breakdown", {})
    breakdown = {
        "section_completeness": min(25, raw.get("section_completeness", 0)),
        "content_richness": min(25, raw.get("content_richness", 0)),
        "clarity_professionalism": min(25, raw.get("clarity_professionalism", 0)),
        "role_alignment": min(25, raw.get("role_alignment", 0)),
    }
    breakdown["total_score"] = min(100, sum(breakdown.values()))
    return breakdown