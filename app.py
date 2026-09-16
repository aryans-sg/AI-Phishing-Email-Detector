import re
import joblib
import streamlit as st
from pathlib import Path

# -----------------------------
# Load trained model
# -----------------------------
BASE = Path(__file__).parent
vectorizer, model = joblib.load(
    BASE / "models" / "phishing_model.joblib"
)

# -----------------------------
# Page settings
# -----------------------------
st.set_page_config(
    page_title="AI Phishing Email Detector",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------
# Email cleaning
# -----------------------------
def clean(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\.\S+", " URL ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


# -----------------------------
# Custom design
# -----------------------------
st.markdown(
    """
    <style>

    /* Main page */
    .stApp {
        background-color: whitesmoke;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Header */
    .hero {
        padding: 30px;
        border-radius: 15px;
        background-color: darkblue;
        margin-bottom: 25px;
        border: 2px solid navy;
    }

    .hero h1 {
        font-size: 38px;
        margin-bottom: 8px;
        color: white;
    }

    .hero p {
        font-size: 17px;
        color: white;
        margin-bottom: 0;
    }

    /* Information cards */
    .card {
        padding: 22px;
        border-radius: 14px;
        background-color: white;
        border: 1px solid lightgray;
        margin-bottom: 20px;
    }

    .card h3 {
        color: black;
    }

    .card p {
        color: black;
    }

    .small-text {
        color: dimgray;
        font-size: 14px;
    }

    /* Result boxes */
    .result {
        padding: 25px;
        border-radius: 14px;
        margin-top: 20px;
    }

    .safe {
        background-color: lightgreen;
        border: 2px solid green;
    }

    .danger {
        background-color: mistyrose;
        border: 2px solid red;
    }

    .result h2,
    .result h3,
    .result p {
        color: black;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Header
# -----------------------------
st.markdown(
    """
    <div class="hero">
        <h1>🛡️ AI Phishing Email Detector</h1>
        <p>
            Analyze suspicious emails using machine learning
            and identify potential phishing threats.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Main layout
# -----------------------------
left, right = st.columns([1.5, 1])

with left:

    st.markdown(
        """
        <div class="card">
            <h3>📧 Email Analysis</h3>
            <p class="small-text">
                Enter the subject and body of an email below.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    subject = st.text_input(
        "Email Subject",
        placeholder="Example: Urgent account verification required"
    )

    body = st.text_area(
        "Email Body",
        height=220,
        placeholder="Paste the email message here..."
    )

    analyze = st.button(
        "🔍 Analyze Email",
        use_container_width=True
    )


with right:

    st.markdown(
        """
        <div class="card">
            <h3>🔎 How it works</h3>

            <p>
                <b>1. Clean</b><br>
                The email text is cleaned before analysis.
            </p>

            <p>
                <b>2. Convert</b><br>
                TF-IDF converts words into numerical features.
            </p>

            <p>
                <b>3. Predict</b><br>
                Logistic Regression classifies the email.
            </p>

            <p>
                <b>4. Result</b><br>
                A phishing risk score is displayed.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# -----------------------------
# Analyze email
# -----------------------------
if analyze:

    if not subject.strip() and not body.strip():

        st.warning(
            "⚠️ Please enter an email subject or email body."
        )

    else:

        email_text = clean(
            subject + " " + body
        )

        features = vectorizer.transform([email_text])

        prediction = model.predict(features)[0]

        probability = model.predict_proba(features)[0][1]

        risk = probability * 100


        # -----------------------------
        # Phishing result
        # -----------------------------
        if prediction == 1:

            st.markdown(
                f"""
                <div class="result danger">

                    <h2>🚨 PHISHING EMAIL DETECTED</h2>

                    <h3>Risk Score: {risk:.1f}%</h3>

                    <p>
                        This email contains patterns that are
                        commonly associated with phishing messages.
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.subheader("⚠️ Recommended Actions")

            st.write(
                "• Do not click links in the email."
            )

            st.write(
                "• Do not provide passwords or personal information."
            )

            st.write(
                "• Verify the sender using an official channel."
            )

            st.write(
                "• Report the message as phishing if appropriate."
            )


        # -----------------------------
        # Legitimate result
        # -----------------------------
        else:

            st.markdown(
                f"""
                <div class="result safe">

                    <h2>✅ LEGITIMATE EMAIL</h2>

                    <h3>Phishing Risk: {risk:.1f}%</h3>

                    <p>
                        The model did not detect strong phishing
                        patterns in this email.
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.subheader("🛡️ Security Reminder")

            st.write(
                "Even legitimate-looking emails should be checked "
                "carefully before clicking links or sharing "
                "sensitive information."
            )


# -----------------------------
# Footer
# -----------------------------
st.divider()

st.caption(
    "AI Phishing Email Detector • "
    "Machine Learning Cybersecurity Mini Project"
)

st.caption(
    "Educational use only. This tool should not be treated "
    "as a guarantee that an email is safe."
)