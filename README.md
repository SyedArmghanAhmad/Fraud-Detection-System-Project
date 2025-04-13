
# FraudShield AI: Real-Time Fraud Detection System

FraudShield AI is an advanced fraud detection system that combines **machine learning** and **generative AI** to identify fraudulent transactions in real-time. Built with **XGBoost** for predictive modeling and enhanced with **LangChain**, **LangGraph**, and **LlamaIndex** for explainability and workflow automation, this system is designed to handle highly imbalanced datasets and provide actionable insights.

---

## Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Tech Stack](#tech-stack)
4. [How It Works](#how-it-works)
5. [Installation](#installation)
6. [Docker Deployment](#docker-deployment)
7. [Usage](#usage)
8. [Demonstration](#demonstration)
9. [Model Training](#model-training)
10. [Dataset](#dataset)
11. [Contributing](#contributing)
12. [License](#license)

---

## Overview

FraudShield AI is a full-stack application that detects fraudulent credit card transactions using a hybrid approach:

- **Machine Learning**: An XGBoost model trained on the [Kaggle Credit Card Fraud Dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) to predict fraud with high precision and recall.
- **Generative AI**: Leverages **LangChain** and **LlamaIndex** to provide human-readable explanations for fraud predictions, especially in borderline cases.
- **Workflow Automation**: Uses **LangGraph** to orchestrate the fraud detection pipeline, ensuring seamless integration of ML and AI components.

The system is deployed as a **Streamlit** web application with a modern, fintech-inspired UI and is fully **Dockerized** for easy deployment.

---

## Key Features

- **Real-Time Fraud Detection**: Analyze single transactions or batch uploads in real-time.
- **Explainable AI**: Get detailed explanations for fraud predictions using **LangChain** and **LlamaIndex**.
- **Borderline Case Handling**: Delegate uncertain predictions to a **Large Language Model (LLM)** for further analysis.
- **Fraud Pattern Recognition**: Identify common fraud patterns using **LlamaIndex**-powered document retrieval.
- **Interactive Dashboard**: Visualize fraud trends, model performance, and transaction details.
- **Scalable Workflow**: Built with **LangGraph** for modular and scalable fraud detection pipelines.
- **Dockerized**: Easily deployable using Docker and available on **Docker Hub**.
- **Demonstration**: Includes a **demo video** and **sample data** for testing.

---

## Tech Stack

### Machine Learning

- **XGBoost**: For fraud prediction using a highly imbalanced dataset.
- **Scikit-learn**: For data preprocessing, evaluation, and metrics.
- **SMOTE**: For handling class imbalance during training.

### Generative AI

- **LangChain**: For generating human-readable explanations and handling borderline cases.
- **LlamaIndex**: For fraud pattern retrieval and document-based reasoning.
- **Groq API**: For fast LLM inference using the `llama-3.1-8b-instant` model.

### Workflow Automation

- **LangGraph**: For orchestrating the fraud detection pipeline.

### Web Application

- **Streamlit**: For building the interactive web interface.
- **FastAPI**: For backend API integration.
- **Custom CSS**: For a modern, fintech-inspired UI.

### Deployment

- **Docker**: For containerization and easy deployment.
- **Docker Hub**: Hosting the Docker image for public access.
- **Joblib**: For saving and loading trained models and scalers.

---

## How It Works

1. **Transaction Input**:
   - Users can upload a CSV file for batch analysis or enter transaction details manually.

2. **Fraud Detection Pipeline**:
   - The transaction is preprocessed (e.g., scaling the `Amount` feature).
   - The **XGBoost model** predicts the probability of fraud.
   - If the prediction is borderline (confidence between 0.3 and 0.7), the system delegates the decision to an **LLM** for further analysis.

3. **Explainability**:
   - **LangChain** generates a detailed explanation of the prediction, highlighting key risk factors and matching fraud patterns.
   - **LlamaIndex** retrieves relevant fraud patterns from a pre-built index for additional context.

4. **Visualization**:
   - The results are displayed in an interactive dashboard, including:
     - Fraud probability and confidence.
     - Transaction details.
     - Matching fraud patterns and explanations.

---

## Installation

### Prerequisites

- Python 3.9 or higher.
- [Groq API Key](https://wow.groq.com/) for LLM inference.
- Docker (optional, for containerized deployment).

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/SyedArmghanAhmad/Fraud-Detection-System-Project.git
   cd Fraud-Detection-System-Project
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file and add your Groq API key:

     ```plaintext
     GROQ_API_KEY=your_api_key_here
     ```

4. Run the application:

   ```bash
   streamlit run app.py
   ```

---

## Docker Deployment

### Pull from Docker Hub

You can pull the pre-built Docker image from Docker Hub:

```bash
docker pull your-dockerhub-atmghan/fraud-detection:latest
```

### Run the Docker Container

```bash
docker run -p 8501:8501 -e GROQ_API_KEY=your_api_key_here your-dockerhub-username/fraudshield-ai
```

### Build Locally

1. Build the Docker image:

   ```bash
   docker build -t fraud-detection .
   ```

2. Run the container:

   ```bash
   docker run -p 8501:8501 -e GROQ_API_KEY=your_api_key_here fraudshield-ai
   ```

The application will be available at `http://localhost:8501`.

---

## Usage

1. **Single Transaction Analysis**:
   - Enter transaction details in the format `key=value, key=value`.
   - Click **Analyze Transaction** to get real-time results.

2. **Batch Analysis**:
   - Upload a CSV file containing transaction data.
   - The system will process the file and display results for each transaction.

3. **Model Insights**:
   - View model performance metrics, and top predictive features.

---

## Demonstration

To help you get started, we’ve included a **demonstration folder** containing:

- **Demo Video**: A walkthrough of the application’s features and functionality.
- **Sample Data**: Example CSV files for testing the batch analysis feature.

### How to Use the Sample Data

1. Navigate to the `demonstration` folder.
2. Use the provided CSV files (e.g., `sample_transactions.csv`) to test the batch analysis feature.
3. Watch the demo video to see the system in action.

---

## Model Training

The XGBoost model was trained on the [Kaggle Credit Card Fraud Dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud). Key steps included:

- **Data Preprocessing**: Scaling the `Amount` feature using **RobustScaler**.
- **Handling Class Imbalance**: Using **SMOTE** to oversample the minority class (frauds).
- **Model Training**: Training an XGBoost classifier with optimized hyperparameters.
- **Evaluation**: Achieving an **AUPRC of 0.87** and **recall of 0.86** on the test set.

For detailed training code, refer to the [Model Training Notebook].

---

## Dataset

The dataset contains credit card transactions made in September 2013 by European cardholders. Key details:

- **Total Transactions**: 284,807
- **Fraudulent Transactions**: 492 (0.172%)
- **Features**:
  - `V1-V28`: Principal components obtained from PCA.
  - `Amount`: Transaction amount.
  - `Class`: Target variable (1 for fraud, 0 for legitimate).

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [Kaggle](https://www.kaggle.com/) for providing the dataset.
- [LangChain](https://www.langchain.com/), [LlamaIndex](https://www.llamaindex.ai/), and [LangGraph](https://www.langgraph.com/) for enabling generative AI capabilities.
- [Streamlit](https://streamlit.io/) for the interactive web interface.
- [Docker](https://www.docker.com/) for containerization and deployment.
