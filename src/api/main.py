from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from api.routes import router



app_configs = {
        "title": "Analytics Service Backend",
        "servers": [
            {"url": "http://localhost:8000", "description": "Local"}
        ]
    }

# Initialize FastAPI
app = FastAPI(**app_configs)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)
    
# app.include_router(api_router, prefix='/api/v1')
app.include_router(router, prefix='/api')



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
