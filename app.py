from fastapi import FastAPI,Request,Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import numpy as np
import mlflow 
from mlflow import MlflowClient
import dagshub
import json

app=FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
template=Jinja2Templates('templates')


dagshub.init(
    repo_owner="umiii-786",
    repo_name="placement-prediction-Model",
    mlflow=True
)
mlflow.set_tracking_uri("https://dagshub.com/umiii-786/placement-prediction-Model.mlflow")
print(mlflow.get_tracking_uri())
# def read_ids(file_path):
#     with open(file_path,'r') as f:
#        ids=json.load(f)
#        return ids



MODEL_URI="models:/placement_prediction_model@production"
# model = mlflow.pyfunc.load_model(
# )
model = mlflow.sklearn.load_model(MODEL_URI)


@app.get('/')
def showIndex(request:Request):
    print('request ai')
    return template.TemplateResponse(request=request,name='index.html')



@app.post('/predict')
async def predict(request:Request):
   form = await request.form()
   record=np.array([[
        float(form.get('cgpa')),
        int(form.get('internship')),
        int(form.get('certification')),
        int(form.get('projects')),
        int(form.get('apptitude_score')),
        float(form.get('softskill_rating')),
        int(form.get('ExtracurricularActivities')),
        int(form.get('placementT')),
        int(form.get('SSC')),
        int(form.get('HSC')),
      ]])
   print(model)
   print(record)
   
   result=model.predict(record)
   prob=model.predict_proba(record)
   print(result)
   print(prob)


   return {
        "prediction": int(result[0]),              # ✅ FIX
        "probability": prob[0].tolist()            # ✅ better way
    }

