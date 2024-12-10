# run.py
from webhook import app
from multiprocessing import Process

def run_webhook():
    app.run(port=5000)

if __name__ == "__main__":
    app.run(port=5000)
