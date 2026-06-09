import streamlit as st

# ============================================================
# SCAMSHIELD — app.py
# Streamlit UI
# ============================================================

st.set_page_config(
    page_title="ScamShield",
    page_icon="🛡️",
    layout="centered"
)

# Header
st.title("🛡️ ScamShield")
st.subheader("Intelligent Job Fraud Detection System")
st.markdown("---")

# Input
st.markdown("### Paste Job Post / Recruiter Message / Offer Letter")
text = st.text_area(
    label="Job Post Text",
    label_visibility="collapsed",
    placeholder="Paste any job post, WhatsApp message, or recruiter email here...",
    height=200
)

# Example buttons
st.markdown("**Try an example:**")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔴 Scam Example"):
        text = "URGENT! Work from home. Earn 1.5 lakh/month. No experience needed. WhatsApp 9876543210. Registration fee 500rs refundable. hrjobs2024@gmail.com"

with col2:
    if st.button("🟢 Legit Example"):
        text = "TCS hiring 2024 batch. Associate Software Engineer. Package 3.36 LPA. Apply at careers.tcs.com. Last date 30th May 2024."

with col3:
    if st.button("🟡 Suspicious Example"):
        text = "BPO hiring freshers. Salary 25000/month. Night shift US process. No experience. Join: bpohiring99@gmail.com"

# Analyse button
if st.button("🔍 Analyse", type="primary", use_container_width=True):
    if not text or len(text.strip()) < 10:
        st.error("Please paste a job post first!")
    else:
        with st.spinner("Analysing..."):
            try:
                # Flask API call
                from predictor import predict
                result = predict(text)

                st.markdown("---")
                st.markdown("### Results")

                # Verdict badge
                verdict  = result['verdict']
                score    = result['trust_score']
                emoji    = result['emoji']

                if verdict == "SCAM":
                    st.error(f"{emoji} **{verdict}** — Trust Score: {score}/10")
                elif verdict == "SUSPICIOUS":
                    st.warning(f"{emoji} **{verdict}** — Trust Score: {score}/10")
                else:
                    st.success(f"{emoji} **{verdict}** — Trust Score: {score}/10")

                # Trust score bar
                st.markdown("**Trust Score:**")
                st.progress(int(score * 10))

                # Scores breakdown
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("ML Score", f"{result['ml_score']:.2f}")
                with col2:
                    st.metric("Rule Score", f"{result['rule_score']}/100")

                # Red flags
                st.markdown("### Red Flags Detected")
                flags = result['flags']
                if flags:
                    for flag in flags:
                        st.error(f"❌ {flag}")
                else:
                    st.success("✅ No red flags found!")

            except Exception as e:
                st.error(f"API Error — make sure api.py is running! {e}")

st.markdown("---")
st.caption("ScamShield — Protecting job seekers from fraud | Built with DistilBERT + Flask")