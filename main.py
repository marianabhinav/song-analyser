import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import music_backend.scripts.compute_knn as compute_knn
import music_backend.scripts.load_dataset as load_dataset

s = load_dataset.DataLoad()
c = compute_knn.CompSimilarityKRanking()
app = FastAPI()

main_path = Path(__file__).resolve().parent
static_folder_path = Path('music_frontend/static')
public_folder_path = Path('music_frontend/public/.')

app.mount("/static", StaticFiles(directory=os.path.join(main_path, static_folder_path)), name="static")

template = Jinja2Templates(directory=os.path.join(main_path, public_folder_path))


@app.get('/')
def home(request: Request):
    return template.TemplateResponse('index.html', {"request": request})


@app.get('/stats')
async def getStats():
    return s.map_meta_data()


@app.get('/getTestTracks/')
async def getTestTracks():
    return s.test_tracks


@app.get('/getKNeighbours/')
async def computeNeigh(trackID: int, k: int):
    return c.computeKnn(trackID, k)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
