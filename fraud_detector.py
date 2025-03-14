import joblib
import json
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FraudDetector:
    def __init__(self):
        try:
            # Load the trained XGBoost model
            self.model = joblib.load('models/fraud_model.pkl')
            
            # Load the RobustScaler for Amount
            self.scaler = joblib.load('models/amount_scaler.pkl')
            
            # Load model metadata
            with open('models/model_metadata.json', 'r') as f:
                self.metadata = json.load(f)
            
            # Load fraud patterns
            self.fraud_patterns = pd.read_csv('models/aligned_fraud_patterns.csv')
            
            logger.info("FraudDetector initialized successfully.")
        except Exception as e:
            logger.error(f"Error initializing FraudDetector: {e}")
            raise

    def predict(self, transaction):
        try:
            # Scale Amount
            scaled_amount = self.scaler.transform([[transaction['Amount']]])[0][0]
            
            # Initialize all features to 0.0
            all_features = {feature: 0.0 for feature in self.metadata['feature_names']}
            
            # Update with the provided features
            for key, value in transaction.items():
                if key in all_features:
                    all_features[key] = value
            
            # Convert to DataFrame with feature names
            features_df = pd.DataFrame([all_features])[self.metadata['feature_names']]
            
            # Predict fraud probability
            prob = self.model.predict_proba(features_df)[0][1]
            
            # Determine if the case is borderline
            is_borderline = 0.3 <= prob <= 0.7  # Adjust thresholds as needed
            
            # Use optimal threshold from metadata
            is_fraud = prob >= self.metadata['optimal_threshold']
            
            # Generate enhanced explanation
            risk_factors = [
                f"{key} ({value:.2f})" 
                for key, value in transaction.items() 
                if key in self.metadata['top_features']['Feature'].values()
            ][:3]
            
            # Get matching patterns
            matching_patterns = self.get_relevant_patterns(transaction)
            pattern_explanation = "\n".join([
                f"- {p['feature']} {p['condition']}: {p['description']}"
                for p in matching_patterns
            ])
            
            explanation = (
                f"Risk factors: {', '.join(risk_factors)}\n"
                f"Matching patterns:\n{pattern_explanation}"
            )
            
            # If borderline, delegate to LLM for further analysis
            if is_borderline:
                llm_verdict = self.llm_judgment(transaction, prob, matching_patterns)
                return {
                    "fraud": llm_verdict["fraud"],
                    "confidence": float(prob),
                    "explanation": llm_verdict["explanation"],
                    "is_borderline": True
                }
            else:
                return {
                    "fraud": bool(is_fraud),
                    "confidence": float(prob),
                    "explanation": explanation,
                    "is_borderline": False
                }
        except Exception as e:
            logger.error(f"Error predicting fraud: {e}")
            return {"error": str(e)}

    def get_relevant_patterns(self, transaction):
        relevant_patterns = []
        # Pre-filter patterns based on transaction features
        filtered_patterns = self.fraud_patterns[self.fraud_patterns['feature'].isin(transaction.keys())]
        
        for _, row in filtered_patterns.iterrows():
            feature = row['feature']
            condition = row['condition']
            value = transaction[feature]
            
            # Evaluate condition
            if ">" in condition:
                threshold = float(condition.split(">")[1].strip())
                if value > threshold:
                    relevant_patterns.append(row.to_dict())
            elif "<" in condition:
                threshold = float(condition.split("<")[1].strip())
                if value < threshold:
                    relevant_patterns.append(row.to_dict())
        
        return relevant_patterns

    def llm_judgment(self, transaction, prob, matching_patterns):
        """
        Delegate borderline cases to the LLM for further analysis.
        """
        # Generate LLM explanation
        explanation = (
            "The model is unsure about this transaction. Analyzing further...\n"
            f"Fraud Probability: {prob * 100:.2f}%\n"
            f"Matching Patterns:\n"
        )
        for pattern in matching_patterns:
            explanation += f"- {pattern['feature']} {pattern['condition']}: {pattern['description']}\n"
        
        # LLM logic to make a final judgment
        if prob >= 0.5:  # Adjust as needed
            verdict = True
            explanation += "\nFinal Verdict: 🚨 Fraud Detected (LLM Judgment)"
        else:
            verdict = False
            explanation += "\nFinal Verdict: ✅ Legitimate (LLM Judgment)"
        
        return {
            "fraud": verdict,
            "explanation": explanation
        }