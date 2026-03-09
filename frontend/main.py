import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from frontend.router import router

app = FastAPI(title="SSAUScheduleFrontend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        __name__ + ":app",
        host='127.0.0.1',
        port=7001,
        reload=True
    )