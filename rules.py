import re

# ============================================================
# SCAMSHIELD — rules.py
# Rule-based scam detector
# ============================================================

# Scam phrases — India specific
SCAM_PHRASES = [
    "work from home", "earn from home", "no experience needed",
    "urgently hiring", "immediate joining", "part time job",
    "data entry", "registration fee", "refundable deposit",
    "training fee", "whatsapp to apply", "call hr directly",
    "no interview", "unlimited earning", "be your own boss",
    "earn daily", "guaranteed income", "work from mobile",
    "google form", "limited seats", "hurry"
]

# Personal email domains — company email nahi hoga scam mein
PERSONAL_EMAILS = [
    "gmail.com", "yahoo.com", "hotmail.com",
    "outlook.com", "rediffmail.com", "ymail.com"
]

# Urgency words
URGENCY_WORDS = [
    "urgent", "immediately", "today only", "last date tomorrow",
    "hurry", "limited", "fast", "quickly", "asap"
]

def extract_salary(text):
    """
    Text se salary nikalo
    
    Kya karta hai:
    "earn 1.5 lakh" → 150000
    "50k per month" → 50000
    "salary 80000"  → 80000
    """
    text = text.lower()
    
    # "1.5 lakh", "2 lakh" pattern
    lakh = re.search(r'(\d+\.?\d*)\s*lakh', text)
    if lakh:
        return float(lakh.group(1)) * 100000
    
    # "50k", "80k per month" pattern
    k_month = re.search(r'(\d+)\s*k\s*(per month|/month|monthly)?', text)
    if k_month:
        return float(k_month.group(1)) * 1000
    
    # "50000", "80000" direct number
    direct = re.search(r'(\d{4,6})\s*(per month|/month|monthly|rs|rupees)?', text)
    if direct:
        return float(direct.group(1))
    
    return None

def extract_email(text):
    """Text se email nikalo"""
    email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return email.group(0) if email else None

def extract_whatsapp(text):
    """WhatsApp number hai?"""
    whatsapp = re.search(r'whatsapp\s*:?\s*[\d\s\+\-]{10,}', text.lower())
    return bool(whatsapp)

def check_rules(text):
    """
    Main function — text andar, score bahar
    
    Returns:
    {
        "rule_score": 0-100,
        "flags": ["reason1", "reason2"],
        "verdict": "SCAM" / "SUSPICIOUS" / "LEGIT"
    }
    """
    flags = []
    score = 0
    text_lower = text.lower()
    
    # ── Check 1: Scam phrases ──────────────────────
    for phrase in SCAM_PHRASES:
        if phrase in text_lower:
            flags.append(f"Suspicious phrase: '{phrase}'")
            score += 10
    
    # ── Check 2: Unrealistic salary ───────────────
    salary = extract_salary(text_lower)
    if salary:
        if salary > 100000:  # 1 lakh+ for fresher = suspicious
            flags.append(f"Unrealistic salary: ₹{salary:,.0f}/month")
            score += 25
        elif salary > 50000:
            flags.append(f"High salary claim: ₹{salary:,.0f}/month")
            score += 10
    
    # ── Check 3: Personal email ───────────────────
    email = extract_email(text)
    if email:
        domain = email.split("@")[-1].lower()
        if domain in PERSONAL_EMAILS:
            flags.append(f"Personal email used: {email}")
            score += 30
    
    # ── Check 4: WhatsApp apply ───────────────────
    if extract_whatsapp(text):
        flags.append("WhatsApp contact — not professional")
        score += 25
    
    # ── Check 5: Urgency words ────────────────────
    urgency_found = []
    for word in URGENCY_WORDS:
        if word in text_lower:
            urgency_found.append(word)
    
    if urgency_found:
        flags.append(f"Urgency words: {', '.join(urgency_found)}")
        score += 15
    # Google Form = red flag
    if "google.com/forms" in text_lower or "docs.google.com" in text_lower:
        flags.append("Google Form registration — suspicious")
        score += 20
    
    # ── Cap score at 100 ──────────────────────────
    score = min(score, 100)
    
    # ── Verdict ───────────────────────────────────
    if score >= 60:
        verdict = "SCAM"
    elif score >= 30:
        verdict = "SUSPICIOUS"
    else:
        verdict = "LEGIT"
    
    return {
        "rule_score": score,
        "flags": flags,
        "verdict": verdict
    }

# ── Test karo ─────────────────────────────────────────────
if __name__ == "__main__":
    
    # Test 1 — Obvious scam
    scam_post = """
    URGENT HIRING! Work from home data entry job.
    Earn 1.5 lakh per month. No experience needed.
    WhatsApp: 9876543210. Registration fee 500 rs refundable.
    Contact: hrjobs2024@gmail.com
    """
    
    # Test 2 — Legit job
    legit_post = """
    TCS hiring 2024 batch. Role: Associate Software Engineer.
    Package: 3.36 LPA. Apply at careers.tcs.com.
    Last date: 30th May 2024.
    """
    
    print("=" * 50)
    print("TEST 1 — SCAM POST")
    print("=" * 50)
    result1 = check_rules(scam_post)
    print(f"Score: {result1['rule_score']}/100")
    print(f"Verdict: {result1['verdict']}")
    print("Flags:")
    for f in result1['flags']:
        print(f"  ❌ {f}")
    
    print("\n" + "=" * 50)
    print("TEST 2 — LEGIT POST")
    print("=" * 50)
    result2 = check_rules(legit_post)
    print(f"Score: {result2['rule_score']}/100")
    print(f"Verdict: {result2['verdict']}")
    if result2['flags']:
        for f in result2['flags']:
            print(f"  ❌ {f}")
    else:
        print("  ✅ No red flags found")