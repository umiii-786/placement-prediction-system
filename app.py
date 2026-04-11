from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import numpy as np
import mlflow
import os

# ------------------- App Setup -------------------
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ------------------- MLflow Setup -------------------
dagshub_pat = "a55ae4d7356bf84fa662753c4cff9084c43da67d"

if not dagshub_pat:
    raise EnvironmentError("DAGSHUB_PAT environment variable is not set")

os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_pat
os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_pat

mlflow.set_tracking_uri(
    "https://dagshub.com/umiii-786/placement-prediction-Model.mlflow"
)

MODEL_URI = "models:/placement_prediction_model@production"

# ------------------- Load Model -------------------
def get_model():
    return mlflow.sklearn.load_model(MODEL_URI)

model = None

def load_model_once():
    global model
    if model is None:
        model = get_model()
    return model

model = load_model_once()

# ------------------- Routes -------------------

@app.get("/")
def show_index(request: Request):
    return templates.TemplateResponse(
       name="index.html",
       request=request   # ✅ correct format
    )

@app.post("/predict")
async def predict(request: Request):
    print('request ai')
    try:
        form = await request.form()
        print(form)
        #  cgpa,internship,certification,projects,apptitude_score,softskill_rating,ExtracurricularActivities,placementT,SSC,HSC
        record = np.array([[ 
            float(form.get('cgpa')),
            int(form.get('internship')),
            int(form.get('certification')),
            int(form.get('projects')),
            int(form.get('apptitude_score')),
            float(form.get('softskill_rating')),
            int(form.get('ExtracurricularActivities')),
            int(form.get('placementT')),
            int(form.get('SSC')),
            int(form.get('HSC'))
        ]])
        print(record)

        result = model.predict(record)
        prob = model.predict_proba(record)
        print('result gya')
        print({
            "prediction": int(result[0]),
            "probability": prob[0].tolist()
        })
        return {
            "prediction": int(result[0]),
            "probability": prob[0].tolist()
        }

    except Exception as e:
        return {"error": str(e)}