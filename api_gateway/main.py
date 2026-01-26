from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routes import auth_routes  
app = FastAPI(title="MediSync 360 API Gateway")

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(auth_routes.router, prefix="/auth")
app.include_router(auth_routes.router, prefix="/chat")



@app.get("/")
async def root():
    return JSONResponse({"message": "WELCOME TO THE API GATEWAY"})
