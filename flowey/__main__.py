import uvicorn
import flowey.utils

env = flowey.utils.env

def start():
    uvicorn.run(
        "flowey.utils.starlette:app",
        host="0.0.0.0",
        port=env.port,
        log_level="info"
    )
    
if __name__ == "__main__":
    start()