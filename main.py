from fastapi import FastAPI, HTTPException
from models import Block

import time

app = FastAPI()


blockchain = []


@app.get("/")
async def index():
    return {"message": "The blockchain peer app is running", "time": time.time()}


@app.post("/receiveBlock")
async def receive_block(block: Block):
    print(f"Received Block: {block.index}, Hash: {block.hash}")

    if len(blockchain) > 0 and blockchain[-1].hash != block.previousHash:
        raise HTTPException(status_code=400, detail="Invalid previous hash!")

    blockchain.append(block)
    return {"message": "Block added successfully!", "block_index": block.index}


@app.get("/getBlockchain")
async def get_blockchain():
    return blockchain


if __name__ == "__main__":
    import uvicorn

    print("Starting blockchain peer node...")
    uvicorn.run(__name__ + ":app", host="0.0.0.0", port=3000, reload=True)
