# maindef main():
#    a print("Hello from firstwork-assignment!")
#
#
# if __name__ == "__main__":
#     main()

from fastapi import FastAPI
from app.api.rule import router as rules_router
from app.api.contract import router as contract_router
app = FastAPI()
app.include_router(rules_router)
app.include_router(contract_router)