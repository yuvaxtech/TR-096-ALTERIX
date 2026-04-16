import re

BIAS_KEYWORDS = {
    # Gender-biased — masculine coded
    "rockstar":     ("high",   "Masculine-coded; discourages non-male applicants."),
    "ninja":        ("high",   "Masculine-coded; associated with male gaming culture."),
    "guru":         ("medium", "Masculine-coded; implies a specific cultural identity."),
    "wizard":       ("medium", "Masculine-coded fantasy trope; alienates many candidates."),
    "dominant":     ("high",   "Signals aggressive masculinity over collaboration."),
    "aggressive":   ("high",   "Masculine-coded trait; drives away women & non-binary applicants."),
    "assertive":    ("medium", "Can signal gender bias; prefer 'confident' or 'decisive'."),
    "competitive":  ("medium", "Masculine-coded; signals a zero-sum culture."),
    "strong":       ("medium", "Can imply physical/masculine strength over skill."),
    "tackle":       ("medium", "Sports/masculine metaphor; prefer 'address' or 'solve'."),
    "crushing it":  ("medium", "Masculine slang; use 'excelling' or 'delivering results'."),
    "manpower":     ("high",   "Gendered; replace with 'workforce' or 'staffing'."),
    "mankind":      ("high",   "Gendered; use 'humanity' or 'people'."),
    "chairman":     ("high",   "Gendered role title; use 'chairperson' or 'chair'."),
    "salesman":     ("high",   "Gendered; use 'sales representative' or 'sales professional'."),
    "policeman":    ("high",   "Gendered; use 'police officer'."),
    "workmanship":  ("medium", "Gendered; use 'craftsmanship', 'quality', or 'skill'."),
    "he or she":    ("medium", "Binary gender assumption; use 'they' or restructure sentence."),
    "his/her":      ("medium", "Binary; use 'their' or rewrite to be gender-neutral."),
    "he":           ("high",   "Assumes male gender. Use 'they' or restructure the sentence."),
    "dominate":     ("high",   "Signals aggressive masculinity over collaboration."),

    # Gender-biased — feminine-coded (can deter men in imbalanced contexts)
    "nurturing":    ("medium", "Feminine-coded; consider 'supportive' or 'mentoring'."),
    "warm":         ("medium", "Feminine-coded personality trait when used as a requirement."),
    "collaborative":("low",    "Slightly feminine-coded; fine in balance with other traits."),

    # Age-biased
    "young":        ("high",   "Age discriminatory; illegal in many jurisdictions."),
    "energetic":    ("medium", "Often used as proxy for 'young'; focus on deliverables instead."),
    "recent graduate": ("high","Excludes experienced candidates; use specific skill requirements."),
    "fresh graduate":  ("high","Age discriminatory; describe skills needed, not career stage."),
    "digital native": ("high", "Age-coded; implies youth preference. Focus on specific tech skills."),
    "tech-savvy":   ("medium", "Age-coded; list specific technologies instead."),
    "mature":       ("medium", "Can be age-coded in either direction; be specific about experience."),
    "experienced":  ("low",    "Neutral alone, but watch for pairing with age-coded language."),
    "veteran":      ("low",    "Can imply age preference; use 'senior' with defined criteria."),

    # Exclusionary / ableist
    "must be able to lift": ("high",   "Specify exact physical requirements only when genuinely essential."),
    "physically fit":       ("high",   "Discriminatory unless physical fitness is a bona fide job requirement."),
    "able-bodied":          ("high",   "Ableist; use functional requirement language instead."),
    "native speaker":       ("high",   "Discriminatory; use 'fluent in English' or specify proficiency level."),
    "mother tongue":        ("medium", "Replace with a standardised language proficiency level."),
    "culture fit":          ("high",   "Often used to screen out diverse candidates; use 'culture add'."),
    "cultural fit":         ("high",   "Subjective screen; describe values and behaviours explicitly."),
    "fit in":               ("medium", "Implies homogeneity; focus on team values and working style."),
    "clean-shaven":         ("high",   "Religious/cultural discrimination; avoid appearance requirements."),

    # Socioeconomic / exclusionary
    "unpaid":               ("high",   "Unpaid roles exclude people who can't afford to work for free."),
    "prestige":             ("medium", "Implies elite network access; focus on demonstrated skills."),
    "ivy league":           ("high",   "Discriminates by socioeconomic background; focus on skills."),
    "top university":       ("high",   "Exclude candidates from less-resourced backgrounds."),
    "elite":                ("medium", "Signals exclusivity; describe the actual skill bar instead."),
}


def detect_bias(text: str):
    """Scan text for biased phrases. Returns list of (phrase, severity, reason)."""
    text_lower = text.lower()
    findings = []
    seen = set()

    for phrase, (severity, reason) in BIAS_KEYWORDS.items():
        if re.search(r'\b' + re.escape(phrase) + r'\b', text_lower, re.IGNORECASE) and phrase.lower() not in seen:
            seen.add(phrase.lower())
            findings.append({
                "phrase": phrase,
                "severity": severity,
                "reason": reason,
            })

    return findings


def bias_score(findings):
    """Aggregate findings → overall score label."""
    if not findings:
        return "low"
    high   = sum(1 for f in findings if f["severity"] == "high")
    medium = sum(1 for f in findings if f["severity"] == "medium")
    if high >= 3 or (high >= 1 and medium >= 3):
        return "high"
    if high >= 1 or medium >= 2:
        return "medium"
    return "low"


def highlight_text(text: str, findings) -> str:
    """Return HTML with biased phrases highlighted."""
    result = text
    # Sort longest first to avoid substring clobbering
    sorted_findings = sorted(findings, key=lambda f: len(f["phrase"]), reverse=True)
    for f in sorted_findings:
        pattern = re.compile(r'\b' + re.escape(f["phrase"]) + r'\b', re.IGNORECASE)
        cls = "bias-high" if f["severity"] == "high" else "bias-medium"
        result = pattern.sub(
            lambda m: f'<span class="{cls}" title="{f["reason"]}">{m.group(0)}</span>',
            result
        )
    return result

REPLACEMENTS = {
    r"\brockstar\b": "high-performing professional",
    r"\bninja\b": "specialist",
    r"\bguru\b": "expert",
    r"\bwizard\b": "expert",
    r"\bdominant\b": "highly proficient",
    r"\bdominate\b": "lead effectively",
    r"\baggressive\b": "proactive and driven",
    r"\bassertive\b": "confident",
    r"\bcompetitive\b": "results-oriented",
    r"\btackle\b": "address",
    r"\bcrushing it\b": "excelling",
    r"\bmanpower\b": "workforce",
    r"\bmankind\b": "humanity",
    r"\bchairman\b": "chairperson",
    r"\bsalesman\b": "sales representative",
    r"\bpoliceman\b": "police officer",
    r"\bhe or she\b": "they",
    r"\bhis/her\b": "their",
    r"\bhe\b": "they",
    r"\bhis\b": "their",
    r"\bhim\b": "them",
    r"\bshe\b": "they",
    r"\bher\b": "their",
    r"\bstrong\b": "proven",
    r"\byoung\b": "motivated",
    r"\benergetic\b": "enthusiastic",
    r"\brecent graduate[s]?\b": "early-career professional",
    r"\bfresh graduate[s]?\b": "early-career professional",
    r"\bdigital native[s]?\b": "proficient with modern technologies",
    r"\btech-savvy\b": "technically adept",
    r"\bculture fit\b": "culture add",
    r"\bcultural fit\b": "culture add",
    r"\bfit in\b": "contribute positively to our team culture",
    r"\bnative[- ]speaker\b": "fluent in English",
    r"\bmother tongue\b": "primary language",
    r"\bivy league\b": "accredited institution",
    r"\btop universit(?:y|ies)\b": "accredited university",
    r"\belite\b": "high-calibre",
    r"\bphysically fit\b": "able to meet role-specific requirements",
    r"\bable-bodied\b": "able to meet role-specific requirements",
    r"\bnurturing\b": "supportive",
    r"\bclean-shaven\b": "[appearance requirements removed]",
}

INCLUSIVE_FOOTER = """

Equal Opportunity Statement:
We are an equal opportunity employer committed to building a diverse and inclusive team. We welcome applications from all qualified individuals regardless of race, gender, age, disability, religion, sexual orientation, or any other protected characteristic. Reasonable accommodations are available upon request."""

def rewrite_jd(text: str) -> str:
    """Apply rule-based substitutions to produce an inclusive JD."""
    result = text
    for pattern, replacement in REPLACEMENTS.items():
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    result += INCLUSIVE_FOOTER
    return result
