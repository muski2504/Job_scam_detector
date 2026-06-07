import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from rules import check_rules

# ============================================================
# SCAMSHIELD — predictor.py
# Model load + prediction
# ============================================================

MODEL_PATH = 'models/scamshield_model'

# Model aur tokenizer load karo
tokenizer = DistilBertTokenizer.from_pretrained(MODEL_PATH)
model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()  # inference mode — training nahi kar rahe

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

print("✅ Model loaded!")

def get_ml_score(text):
    """
    DistilBERT se scam probability nikalo
    
    Returns: 0.0 to 1.0
    1.0 = definitely scam
    0.0 = definitely legit
    """
    # Text tokenize karo
    encoding = tokenizer(
        text,
        max_length=128,
        padding='max_length',
        truncation=True,
        return_tensors='pt'
    )
    
    input_ids      = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)
    
    # Model se prediction lo
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        probabilities = torch.softmax(outputs.logits, dim=1)
        scam_prob = probabilities[0][1].item()  # index 1 = scam class
    
    return scam_prob

def get_trust_score(rule_score, ml_score):
    """
    Rule score + ML score combine karke trust score banao
    
    Rule score  → 0-100  (high = scam)
    ML score    → 0-1    (high = scam)
    Trust score → 0-10   (low = scam, high = legit)
    
    Formula:
    Combined scam score = 60% ML + 40% Rules
    Trust score = 10 - (combined * 10)
    """
    # Normalize rule score to 0-1
    rule_normalized = rule_score / 100
    
    # Combine — ML zyada important hai
    combined_scam = (0.4 * ml_score) + (0.6 * rule_normalized)

    
    # Trust score — ulta karo (scam high → trust low)
    trust = round(10 - (combined_scam * 10), 1)
    trust = max(0, min(10, trust))  # 0-10 ke beech rakho
    
    return trust

def predict(text):
    """
    Main function — poora pipeline
    
    Input:  job post text
    Output: {
        trust_score: 0-10,
        verdict: SCAM/SUSPICIOUS/LEGIT,
        ml_score: 0-1,
        rule_score: 0-100,
        flags: [reasons list]
    }
    """
    # Step 1 — Rules check karo
    rule_result = check_rules(text)
    rule_score  = rule_result['rule_score']
    flags       = rule_result['flags']
    
    # Step 2 — ML model se score lo
    ml_score = get_ml_score(text)
    
    # Step 3 — Trust score calculate karo
    trust_score = get_trust_score(rule_score, ml_score)
    
    # Step 4 — Verdict decide karo
    if trust_score <= 3:
        verdict = "SCAM"
        emoji   = "🔴"
    elif trust_score <= 6:
        verdict = "SUSPICIOUS"
        emoji   = "🟡"
    else:
        verdict = "LEGIT"
        emoji   = "🟢"
    
    return {
        "trust_score": trust_score,
        "verdict":     verdict,
        "emoji":       emoji,
        "ml_score":    round(ml_score, 4),
        "rule_score":  rule_score,
        "flags":       flags
    }

# ── Test karo ─────────────────────────────────────────────
if __name__ == "__main__":
    
    test1 = """
    URGENT! Work from home data entry job.
    Earn 1.5 lakh per month. No experience needed.
    WhatsApp: 9876543210. Fee 500 rs refundable.
    Contact: hrjobs2024@gmail.com
    """
    
    test2 = """
    TCS hiring 2024 batch. Associate Software Engineer.
    Package 3.36 LPA. Apply at careers.tcs.com.
    Last date 30th May 2024.
    """
    
    test3 = """
    Startup hiring Python developer. 2+ years experience.
    CTC 8-12 LPA. Remote. Apply: careers@techstartup.com
    Skills: Python, Django, PostgreSQL.
    """
    
    for i, post in enumerate([test1, test2, test3], 1):
        print(f"\n{'='*50}")
        print(f"TEST {i}")
        print('='*50)
        result = predict(post)
        print(f"{result['emoji']} Verdict: {result['verdict']}")
        print(f"Trust Score: {result['trust_score']}/10")
        print(f"ML Score: {result['ml_score']}")
        print(f"Rule Score: {result['rule_score']}/100")
        if result['flags']:
            print("Red Flags:")
            for f in result['flags']:
                print(f"  ❌ {f}")
        else:
            print("  ✅ No red flags")