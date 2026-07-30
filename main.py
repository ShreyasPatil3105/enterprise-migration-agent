import os
import threading
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn

app = FastAPI()

@app.api_route("/", methods=["GET", "HEAD"])
def health_check():
    return RedirectResponse(url="/streamlit", status_code=303)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8501))
    
    def run_streamlit():
        os.system("streamlit run app.py --server.port=8502 --server.address=0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false")
    
    threading.Thread(target=run_streamlit, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=port)
