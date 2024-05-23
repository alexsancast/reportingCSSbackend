from fastapi import FastAPI
from routes.reporting import report_detail
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  #  métodos específicos en lugar de ["*"]
    allow_headers=["*"],  #  headers específicos en lugar de ["*"]
)

app.include_router(report_detail)

