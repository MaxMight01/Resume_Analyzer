def compute_score(analysis: dict) -> dict:
    score = 0

    # Content Completeness (30)
    required_sections = {"Summary", "Skills", "Experience", "Education"}
    optional_sections = {"Projects", "Certifications", "Awards", "Publications"}

    detected = set(s.strip().lower() for s in analysis.get("sections_detected", []))
    missing = set(s.strip().lower() for s in analysis.get("missing_sections", []))

    required_found = len([s for s in required_sections if s.lower() in detected])
    content_score = min(30, required_found * 7.5)
    score += content_score

    # Relevance & Specificity (25)
    well_written = analysis.get("well_written_sections", [])
    relevance_score = min(25, len(well_written) * 8.5)
    score += relevance_score

    # Achievements & Impact (20)
    achievement_keywords = ['led', 'built', 'developed', 'improved', 'designed', 'launched', 'managed']
    achievement_points = 0
    for section in well_written:
        if any(kw in section.lower() for kw in achievement_keywords):
            achievement_points += 5
    achievements_score = min(20, achievement_points)
    score += achievements_score

    # Skills Matching (10)
    sentiment = analysis.get("skills_sentiment_summary", "").lower()
    if "strong" in sentiment or "confident" in sentiment:
        skills_score = 10
    elif "specific" in sentiment:
        skills_score = 7
    elif "neutral" in sentiment:
        skills_score = 4
    else:
        skills_score = 1
    score += skills_score

    # Formatting & Structure (5)
    if len(detected) >= 6 and all(len(s.split()) < 4 for s in detected):
        formatting_score = 5
    elif len(detected) >= 5:
        formatting_score = 3
    else:
        formatting_score = 1
    score += formatting_score

    # LLM Evaluation (10)
    llm_eval_raw = analysis.get("llm_evaluation", 0)
    llm_eval_clamped = max(0, min(llm_eval_raw, 10))
    llm_score = round(llm_eval_clamped)
    score += llm_score

    total_score = min(100, round(score))

    return {
        "total_score": total_score,
        "content_completeness": content_score,
        "relevance_specificity": relevance_score,
        "achievements_impact": achievements_score,
        "skills_matching": skills_score,
        "formatting_structure": formatting_score,
        "llm_evaluation": llm_score
    }
