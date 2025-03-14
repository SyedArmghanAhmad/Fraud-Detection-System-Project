# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy ALL application files (including models directory)
COPY . .

# Expose ports
EXPOSE 8000 8501

# Run the app
CMD ["sh", "-c", "uvicorn Api:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 8501 --server.address 0.0.0.0"]