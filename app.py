from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import numpy as np
import mlflow
import dagshub
import os 
# ------------------- App Setup -------------------
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ------------------- MLflow Setup -------------------

dagshub_pat=os.getenv("DAGSHUB_PAT")
if not dagshub_pat:
    raise EnvironmentError('DAGSHUB_PAT environment variable is not setted ') 
os.environ['MLFLOW_TRACKING_USERNAME']=dagshub_pat 
os.environ['MLFLOW_TRACKING_PASSWORD']=dagshub_pat 


mlflow.set_tracking_uri(
    "https://dagshub.com/umiii-786/placement-prediction-Model.mlflow"
)

MODEL_URI = "models:/placement_prediction_model@production"


# ------------------- Input Schema -------------------
class InputData(BaseModel):
    cgpa: float
    internship: int
    certification: int
    projects: int
    apptitude_score: int
    softskill_rating: float
    ExtracurricularActivities: int
    placementT: int
    SSC: int
    HSC: int


# ------------------- Load Model (Lazy Loading) -------------------
def get_model():
    return mlflow.sklearn.load_model(MODEL_URI)

model=None
def load_model_once():
    global model
    if model is None:
        model = get_model()
    return model


model = load_model_once()
# ------------------- Routes -------------------

@app.get("/")
def show_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
def predict(data: InputData):
    try:

        record = np.array([[
            data.cgpa,
            data.internship,
            data.certification,
            data.projects,
            data.apptitude_score,
            data.softskill_rating,
            data.ExtracurricularActivities,
            data.placementT,
            data.SSC,
            data.HSC
        ]])

        result = model.predict(record)
        prob = model.predict_proba(record)

        return {
            "prediction": int(result[0]),
            "probability": prob[0].tolist()
        }

    except Exception as e:
        return {
            "error": str(e)
        }