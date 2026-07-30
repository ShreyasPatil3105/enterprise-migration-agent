import os
import subprocess
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn

app = FastAPI()

@app.get("/")
def health_check():
    # Redirect visitors straight to the Streamlit UI or return OK for Render
    return RedirectResponse(url="/streamlit", status_code=303)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8501))
    # Run Uvicorn as the main process to satisfy Render, and spawn Streamlit alongside it
    import threading
    def run_streamlit():
        os.system(f"streamlit run app.py --server.port=8502 --server.address=0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false")
    
    threading.Thread(target=run_streamlit, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=port)
