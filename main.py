from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    Request
)
from fastapi.security import (
    OAuth2PasswordRequestForm
)
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.database import (
    get_db
)

from database.model import (
    User,
    PredictionHistory
)

from database.schema import (
    UserCreate,
    UserLogin
)

from database.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    admin_required
)

from fastapi.responses import (
    HTMLResponse
)

from fastapi.templating import (
    Jinja2Templates
)

from fastapi.staticfiles import (
    StaticFiles
)


import pandas as pd 
import joblib

#FastAPI app

app=FastAPI(
    title="Air Quality Classification and pollution analysis API"
)
templates = Jinja2Templates(
    directory="templates"
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)
def no_cache(response):

    response.headers[
        "Cache-Control"
    ] = "no-store"

    response.headers[
        "Pragma"
    ] = "no-cache"

    response.headers[
        "Expires"
    ] = "0"

    return response



#load saved files 
model_info = joblib.load( "models/air_quality_model.pkl" ) 

model = model_info["model"] 

requires_scaling = ( model_info["requires_scaling"] )
 
scaler = joblib.load( "models/scaler.pkl" ) 

label_encoder = joblib.load( "models/label_encoder.pkl" )
 
feature_columns = joblib.load( "models/feature_columns.pkl" )

# INPUT SCHEMA 
class AirQualityInput(BaseModel): 
    PM2_5: float 
    PM10: float 
    NO: float 
    NO2: float 
    NOx: float 
    NH3: float 
    CO: float 
    SO2: float 
    O3: float 
    Benzene: float 
    Toluene: float 
    Xylene: float 
    AQI: float
    

# Home route
@app.get(
    "/",
    response_class=HTMLResponse
)
def home(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="home.html"
    )
    
# HTML PAGES

@app.get(
    "/login-page",
    response_class=HTMLResponse
)
def login_page(
    request: Request
):

   return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


@app.get(
    "/register-page",
    response_class=HTMLResponse
)
def register_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="register.html"
    )
    
@app.get(
    "/landing-page",
    response_class=HTMLResponse
)
def landing_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html"
    )
    return no_cache(
        response
    )

@app.get(
    "/dashboard",
    response_class=HTMLResponse
)
def dashboard_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="analytics.html"
    )
    return no_cache(
        response
    )

    
@app.get(
    "/predict-page",
    response_class=HTMLResponse
)
def predict_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="predict.html"
    )
    return no_cache(
        response
    )

@app.get(
    "/history-page",
    response_class=HTMLResponse
)
def history_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="history.html"
    )
    return no_cache(
        response
    )

@app.get("/users-page")
def users_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="users.html"
    )


#register 
@app.post("/register")

def register_user(

    user: UserCreate,

    db: Session = Depends(
        get_db
    )
):

    existing_user = db.query(
        User
    ).filter(

        User.username ==user.username
    ).first()

    if existing_user:

        raise HTTPException(

            status_code=400,

            detail="Username already exists"
        )

    hashed_password = (
        get_password_hash(
            user.password
        )
    )

    new_user = User(

        username=user.username,

        email=user.email,

        hashed_password=hashed_password,

        role=user.role
    )

    db.add(
        new_user
    )

    db.commit()

    db.refresh(
        new_user
    )

    return {

        "message":
        "User Registered Successfully"
    }

#login route 
@app.post("/login")

def login_user(

    form_data: OAuth2PasswordRequestForm= Depends(),

    db: Session = Depends(
        get_db
    )
):

    db_user = db.query(
        User
    ).filter(

        User.username ==
        form_data.username

    ).first()

    if not db_user:

        raise HTTPException(

            status_code=401,

            detail=
            "Invalid Username"
        )

    if not verify_password(

        form_data.password,

        db_user.hashed_password

    ):

        raise HTTPException(

            status_code=401,

            detail=
            "Invalid Password"
        )

    access_token = (

        create_access_token(

            {
                "sub":db_user.username,
                "role": db_user.role
            }
        )
    )

    return {

        "access_token":
        access_token,

        "token_type":
        "bearer",
        "username": db_user.username,
        "role": db_user.role
    }

    
#prediction route
@app.post("/predict")

def predict(

    data: AirQualityInput,

    current_user: str =
    Depends(
        get_current_user
    ),

    db: Session =
    Depends(
        get_db
    )
):
    input_data = { 
                  "PM2.5": data.PM2_5, 
                  "PM10": data.PM10, 
                  "NO": data.NO, 
                  "NO2": data.NO2, 
                  "NOx": data.NOx, 
                  "NH3": data.NH3, 
                  "CO": data.CO, 
                  "SO2": data.SO2, 
                  "O3": data.O3, 
                  "Benzene": data.Benzene, 
                  "Toluene": data.Toluene, 
                  "Xylene": data.Xylene, 
                  "AQI": data.AQI 
                }
    # CONVERT TO DATAFRAME

    input_df = pd.DataFrame(
        [input_data]
    )

    # ARRANGE COLUMN ORDER

    input_df = input_df[
        feature_columns
    ]

    # SCALE IF REQUIRED

    if requires_scaling:

        input_df = scaler.transform(
            input_df
        )

    # PREDICTION

    prediction = model.predict(
        input_df
    )

    # DECODE PREDICTION

    predicted_category = (
        label_encoder.inverse_transform(
            prediction
        )
    )
    
    probabilities = model.predict_proba(
        input_df
    )

    confidence = (
        probabilities.max() * 100
    )
    
    # GET CURRENT USER

    db_user = db.query(
        User
    ).filter(
        User.username ==current_user["username"]
    ).first()

# SAVE PREDICTION HISTORY

    history = PredictionHistory(

        user_id=db_user.id,
        
        AQI=data.AQI,

        predicted_category=predicted_category[0],

        confidence=round(
            float(confidence),2
        )
    )

    db.add(
        history
    )

    db.commit()


    class_probabilities = {}

    for i, class_name in enumerate(
        label_encoder.classes_
    ):

       class_probabilities[class_name] = round(
        float(probabilities[0][i] * 100),2
    )
    
    return {

        "predicted_category":
            predicted_category[0],

        "confidence":
            round(
                float(confidence),2
            ),

        "all_classes_probabilities":
            class_probabilities
    }
    
@app.get("/history")
def get_history(
    page: int = 1,

    page_size: int = 10,

    current_user: str = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )
):

    db_user = db.query(
        User
    ).filter(
        User.username == current_user["username"]
    ).first()

    offset = (page - 1) * page_size

    total_records = db.query(
        PredictionHistory
    ).filter(
        PredictionHistory.user_id == db_user.id
    ).count()

    history = db.query(
        PredictionHistory
    ).filter(
        PredictionHistory.user_id == db_user.id
    ).offset(
        offset
    ).limit(
        page_size
    ).all()

    result = []

    for record in history:

        result.append(

            {
                "AQI":record.AQI,
                "predicted_category":record.predicted_category,
                "confidence":record.confidence,
                "created_at":record.created_at
            }
        )

    return {

        "username":db_user.username,

        "history":result,

        "total_records":total_records,

        "page":page,

        "page_size":page_size
    }

@app.get("/analytics")
def analytics(

    current_user: str = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )
):

    db_user = db.query(
        User
    ).filter(
        User.username == current_user["username"]
    ).first()

    history = db.query(
        PredictionHistory
    ).filter(
        PredictionHistory.user_id == db_user.id
    ).all()

    category_counts = {}

    for record in history:

        category = record.predicted_category

        category_counts[category] = (
            category_counts.get(category,0) + 1
        )

    trend = []

    for record in history:

        trend.append({

            "date":
            record.created_at.strftime(
                "%d-%b"
            ),

            "aqi":
            record.AQI
        })

    return {

        "categories":
        category_counts,

        "trend":
        trend
    }
@app.get("/users")
def get_all_users(

    current_user = Depends(
        admin_required
    ),

    db: Session = Depends(
        get_db
    )
):

    users = db.query(
        User
    ).all()

    result = []

    for user in users:

        result.append({

            "id": user.id,

            "username": user.username,

            "email": user.email,

            "role": user.role
        })

    return result
 