import streamlit as st
from fraud_detector import FraudDetector
from workflow import fraud_workflow
import json
import pandas as pd
from streamlit.components.v1 import html

# --- Page Config (MUST BE FIRST) ---
st.set_page_config(
    page_title="FraudShield AI",  # Updated name
    page_icon="🌐",
    layout="wide"
)

# Load model metadata with default values
try:
    with open("models/model_metadata.json", "r") as f:
        metadata = json.load(f)
except FileNotFoundError:
    st.error("Model metadata file not found. Using default values.")
    metadata = {
        "model_version": "1.0.0",
        "training_date": "2023-10-01",
        "top_features": {
            "Feature": {
                "1": "Transaction Amount",
                "2": "Time of Day",
                "3": "Location"
            }
        }
    }

# Ensure required keys exist in metadata
metadata.setdefault("model_version", "1.0.0")
metadata.setdefault("training_date", "2023-10-01")
metadata.setdefault("top_features", {
    "Feature": {
        "1": "Transaction Amount",
        "2": "Time of Day",
        "3": "Location"
    }
})

# Initialize FraudDetector
detector = FraudDetector()

# Custom CSS for fintech styling
st.markdown("""
<style>
:root {
    --primary: #007BFF;  /* Updated to fintech blue */
    --secondary: #00D1FF;  /* Updated to fintech teal */
    --accent: #ec4899;
    --dark: #0f172a;
    --light: #f8fafc;
}

* {
    font-family: 'Inter', sans-serif;
}

body {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: var(--light);
}

.stApp {
    max-width: 100%;
    margin: 0;
    padding: 0;
}

.fintech-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(16px);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 2rem;
    margin: 1rem 0;
    transition: transform 0.3s ease;
}

.fintech-card:hover {
    transform: translateY(-5px);
}

.risk-badge {
    padding: 0.5rem 1rem;
    border-radius: 2rem;
    font-weight: 700;
    width: fit-content;
}

# Update the gradient-text class in your CSS:
.gradient-text {
    background: linear-gradient(45deg, #ffffff, var(--secondary));  /* Change to white for better visibility */
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: bold;  /* Make it bolder for better visibility */
}

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
}

.pulse {
    animation: pulse 2s infinite;
}

.stProgress > div > div {
    background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;  /* Updated gradient */
}

</style>
""", unsafe_allow_html=True)

# Confetti animation
def confetti():
    html("""
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <script>
    function fireConfetti() {
        var end = Date.now() + (3 * 1000);
        var colors = ['#6366f1', '#a855f7', '#ec4899'];

        function frame() {
            confetti({
                particleCount: 3,
                angle: 60,
                spread: 55,
                origin: { x: 0 },
                colors: colors
            });
            confetti({
                particleCount: 3,
                angle: 120,
                spread: 55,
                origin: { x: 1 },
                colors: colors
            });

            if (Date.now() < end) requestAnimationFrame(frame);
        }
        frame();
    }
    </script>
    """)

# Main App
def main():
    # Navigation
    with st.container():
        col1, col2 = st.columns([1,3])
        with col1:
            st.markdown("<h1 class='gradient-text'>FraudShield AI</h1>", unsafe_allow_html=True)  # Updated name
        with col2:
            st.markdown("""
            <div style="display: flex; gap: 2rem; justify-content: flex-end;">
                <button onclick="window.scrollTo(0,0)" style="background:none; border:none; color:white; cursor:pointer">Dashboard</button>
                <button onclick="scrollToSection('analyze')" style="background:none; border:none; color:white; cursor:pointer">Analyze</button>
                <button onclick="scrollToSection('history')" style="background:none; border:none; color:white; cursor:pointer">History</button>
            </div>
            <script>
            function scrollToSection(sectionId) {
                document.getElementById(sectionId).scrollIntoView({behavior: 'smooth'});
            }
            </script>
            """, unsafe_allow_html=True)

    # Initialize session state for fraud pattern data
    if "fraud_pattern_data" not in st.session_state:
        st.session_state.fraud_pattern_data = pd.DataFrame({
            "hour": [],
            "fraud_attempts": [],
            "amount": []
        })

    # Analysis Section
    st.markdown('<div id="analyze"></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown("### Transaction Analysis")
        input_method = st.radio("Select Input Method", ["Batch Analysis", "Single Transaction"], 
                              horizontal=True, label_visibility='collapsed')

        if input_method == "Batch Analysis":
            uploaded_file = st.file_uploader("Drag and drop CSV file or click to browse", 
                                            type=["csv"],
                                            help="Supported format: CSV with transaction details")

            if uploaded_file:
                try:
                    with st.spinner('Analyzing transactions...'):
                        df = pd.read_csv(uploaded_file)
                        progress_bar = st.progress(0)
                        results = []

                        for index, row in df.iterrows():
                            transaction = row.to_dict()
                            workflow_state = fraud_workflow.invoke({"transaction": transaction})
                            results.append(workflow_state)
                            progress_bar.progress((index + 1) / len(df))

                        st.success(f"Processed {len(df)} transactions!")

                        # Simulate time distribution (if no timestamp is available)
                        hours = list(range(24))  # Distribute transactions across 24 hours
                        fraud_attempts = [result["fraud_result"]["fraud"] for result in results]
                        amounts = [result["transaction"].get("Amount", 0) for result in results]
                        simulated_hours = [hours[i % 24] for i in range(len(fraud_attempts))]  # Distribute across hours

                        # Update fraud pattern data
                        new_data = pd.DataFrame({
                            "hour": simulated_hours,
                            "fraud_attempts": fraud_attempts,
                            "amount": amounts
                        })
                        st.session_state.fraud_pattern_data = pd.concat([st.session_state.fraud_pattern_data, new_data])

                        # Display results
                        for idx, result in enumerate(results, start=1):
                            with st.expander(f"Transaction {result['transaction'].get('id', f'#{idx}')}", expanded=False):
                                col1, col2 = st.columns([1,2])
                                with col1:
                                    st.markdown(f"""
                                    <div class="fintech-card">
                                        <div style="font-size: 1.5rem">{result['fraud_result']['confidence']*100:.1f}%</div>
                                        <div class="pulse" style="color: {'#ef4444' if result['fraud_result']['fraud'] else '#10b981'}">
                                            {'🚨 High Risk' if result['fraud_result']['fraud'] else '✅ Verified'}
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                with col2:
                                    st.markdown(f"**Pattern Analysis**: {result['explanation']}")

                                    # Transaction details table
                                    st.table(pd.DataFrame.from_dict(result['transaction'], orient='index', columns=['Value']))
                except Exception as e:
                    st.error(f"Error processing CSV file: {e}")

        else:
            transaction = {}
            query = st.text_input("Enter transaction details (format: key=value, key=value)")

            if query:
                try:
                    for pair in query.split(','):
                        key, value = pair.strip().split('=')
                        transaction[key.strip()] = float(value.strip())
                except Exception as e:
                    st.error(f"Invalid format: {e}")

            if st.button("Analyze Transaction", type="primary"):
                with st.spinner('Detecting anomalies...'):
                    workflow_state = fraud_workflow.invoke({"transaction": transaction})

                    # Update fraud pattern data
                    current_hour = pd.Timestamp.now().hour
                    new_data = pd.DataFrame({
                        "hour": [current_hour],
                        "fraud_attempts": [workflow_state["fraud_result"]["fraud"]],
                        "amount": [workflow_state["transaction"].get("Amount", 0)]
                    })
                    st.session_state.fraud_pattern_data = pd.concat([st.session_state.fraud_pattern_data, new_data])

                    col1, col2 = st.columns([1,2])
                    with col1:
                        st.markdown(f"""
                        <div class="fintech-card">
                            <div style="font-size: 2rem; margin-bottom: 1rem">
                                {workflow_state['fraud_result']['confidence']*100:.1f}%
                            </div>
                            <div class="risk-badge" style="background: {
                                '#ef444422' if workflow_state['fraud_result']['fraud'] else '#10b98122'
                            }; color: {
                                '#ef4444' if workflow_state['fraud_result']['fraud'] else '#10b981'
                            }">
                                {'High Risk' if workflow_state['fraud_result']['fraud'] else 'Low Risk'}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        if workflow_state['fraud_result']['fraud']:
                            confetti()
                            html("<script>fireConfetti()</script>")

                    with col2:
                        st.markdown("### Transaction Details")
                        cols = st.columns(3)
                        for idx, (key, value) in enumerate(workflow_state['transaction'].items()):
                            with cols[idx%3]:
                                st.markdown(f"""
                                <div class="fintech-card" style="padding: 1rem; margin-bottom: 1rem">
                                    <div style="font-size: 0.8rem; opacity: 0.8">{key}</div>
                                    <div style="font-size: 1.2rem">{value}</div>
                                </div>
                                """, unsafe_allow_html=True)

                        st.markdown("### AI Explanation")
                        st.markdown(workflow_state['explanation'])
    # System Info
    st.markdown('<div id="history"></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown("### Model Insights")
        with st.expander("System Performance Metrics", expanded=False):
            cols = st.columns(3)
            with cols[0]:
                st.markdown("**Model Performance Metrics**")
                st.metric("Precision", f"{metadata['precision']*100:.0f}%",
                        help="Proportion of correctly identified fraud cases out of all predicted fraud cases.")
                st.metric("Recall", f"{metadata['recall']*100:.0f}%",
                        help="Proportion of actual fraud cases correctly identified by the model.")
                st.metric("AUPRC", f"{metadata['auprc']:.2f}",
                        help="Area Under the Precision-Recall Curve, measuring model performance for imbalanced datasets.")

            with cols[1]:
                st.markdown("**Model Metadata**")
                st.metric("Model Version", metadata["model_version"],
                        help="Current version of the deployed fraud detection model.")
                st.metric("Training Date", "9 March 2025",
                        help="Date when the model was last trained.")
                st.metric("Optimal Threshold", f"{metadata['optimal_threshold']:.2f}",
                        help="Threshold for classifying transactions as fraudulent.")

            with cols[2]:
                st.markdown("**Top Predictive Features**")
                for rank, feature in metadata["top_features"]["Feature"].items():
                    importance = metadata["top_features"]["Importance"][rank]
                    st.markdown(f"- **{feature}** (Importance: {importance:.3f})")
                st.markdown("""
                <style>
                .feature-list {
                    padding-left: 1.5rem;
                    border-left: 2px solid #6366f1;
                }
                </style>
                <div class="feature-list">
                <p>These features contribute most to the model's fraud detection capabilities.</p>
                </div>
                """, unsafe_allow_html=True)

    # Footer with Copyright and Social Links
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; color: #a1a1aa;">
        <p style="font-size: 0.9rem;">© 2025 FraudShield AI. All rights reserved.</p>  <!-- Updated name -->
        <p style="font-size: 0.9rem;">Made with ❤️ by <span class="gradient-text">Syed Armghan</span></p>
        <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 0.5rem;">
            <a href="https://www.linkedin.com/in/syed-armghan-ahmad/" target="_blank">
                <img src="https://img.icons8.com/fluent/48/000000/linkedin.png" width="24" height="24" alt="LinkedIn"/>
            </a>
            <a href="https://github.com/SyedArmghanAhmad" target="_blank">
                <img src="https://img.icons8.com/fluent/48/000000/github.png" width="24" height="24" alt="GitHub"/>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()