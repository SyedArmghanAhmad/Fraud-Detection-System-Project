from fastapi import FastAPI
import subprocess
import uvicorn
import os

app = FastAPI()

@app.get("/")
def start_streamlit():
    # Run Streamlit as a subprocess
    streamlit_command = "streamlit run ui.py --server.port=8501 --server.address=0.0.0.0"
    subprocess.Popen(streamlit_command, shell=True)
    return {"message": "Streamlit app started on port 8501"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)