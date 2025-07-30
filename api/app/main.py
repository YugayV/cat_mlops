import logging
import json
from typing import Any

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder

from api.app import __version__, schemas
from api.app.config import get_logger, settings
from catboost_model.predict import make_prediction
from catboost_model import __version__ as model_version

from fastapi import FastAPI, APIRouter
from typing import Union

# setup logging
_logger = get_logger(logger_name=__name__)

app = FastAPI(
    title=settings.PROJECT_NAME, 
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version=__version__
)

root_router = APIRouter()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "CatBoost ML API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/version")
async def get_version():
    """Получить информацию о версии API и модели"""
    return {
        "api_version": __version__,
        "model_version": model_version,
        "status": "active"
    }

@root_router.get("/", response_class=HTMLResponse)
def index() -> str:
    """Главная страница с формой для предсказаний."""
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CatBoost ML API</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #333;
                text-align: center;
                margin-bottom: 30px;
            }}
            .version-info {{
                background-color: #e8f4fd;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 30px;
                border-left: 4px solid #007bff;
            }}
            .form-group {{
                margin-bottom: 20px;
            }}
            label {{
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
                color: #555;
            }}
            input[type="number"] {{
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 16px;
                box-sizing: border-box;
            }}
            button {{
                background-color: #007bff;
                color: white;
                padding: 12px 30px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                width: 100%;
                margin-top: 20px;
            }}
            button:hover {{
                background-color: #0056b3;
            }}
            .result {{
                margin-top: 30px;
                padding: 20px;
                background-color: #f8f9fa;
                border-radius: 5px;
                border: 1px solid #dee2e6;
            }}
            .error {{
                background-color: #f8d7da;
                border-color: #f5c6cb;
                color: #721c24;
            }}
            .success {{
                background-color: #d4edda;
                border-color: #c3e6cb;
                color: #155724;
            }}
            .links {{
                text-align: center;
                margin-top: 30px;
            }}
            .links a {{
                color: #007bff;
                text-decoration: none;
                margin: 0 15px;
            }}
            .links a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 CatBoost ML API</h1>
            
            <div class="version-info">
                <strong>Информация о версии:</strong><br>
                API версия: {__version__}<br>
                Модель версия: {model_version}
            </div>

            <h2>Форма для предсказания</h2>
            <form id="predictionForm">
                <div class="form-group">
                    <label for="dv_r">DV_R (Доходы от продаж):</label>
                    <input type="number" id="dv_r" name="dv_r" required>
                </div>
                
                <div class="form-group">
                    <label for="da_r">DA_R (Дебиторская задолженность):</label>
                    <input type="number" id="da_r" name="da_r" required>
                </div>
                
                <div class="form-group">
                    <label for="av_r">AV_R (Активы):</label>
                    <input type="number" id="av_r" name="av_r" required>
                </div>
                
                <div class="form-group">
                    <label for="aa_r">AA_R (Оборотные активы):</label>
                    <input type="number" id="aa_r" name="aa_r" required>
                </div>
                
                <div class="form-group">
                    <label for="pm_r">PM_R (Прибыль):</label>
                    <input type="number" id="pm_r" name="pm_r" required>
                </div>
                
                <button type="submit">Получить предсказание</button>
            </form>

            <div id="result" class="result" style="display: none;"></div>

            <div class="links">
                <a href="/docs">📚 API Документация</a>
                <a href="/version">ℹ️ Информация о версии</a>
                <a href="/health">❤️ Проверка здоровья</a>
            </div>
        </div>

        <script>
            document.getElementById('predictionForm').addEventListener('submit', async function(e) {{
                e.preventDefault();
                
                const formData = new FormData(e.target);
                const data = {{
                    inputs: [{{
                        DV_R: parseInt(formData.get('dv_r')),
                        DA_R: parseInt(formData.get('da_r')),
                        AV_R: parseInt(formData.get('av_r')),
                        AA_R: parseInt(formData.get('aa_r')),
                        PM_R: parseInt(formData.get('pm_r'))
                    }}]
                }};

                const resultDiv = document.getElementById('result');
                resultDiv.style.display = 'block';
                resultDiv.innerHTML = '<p>Загрузка...</p>';

                try {{
                    const response = await fetch('/predict', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json',
                        }},
                        body: JSON.stringify(data)
                    }});

                    const result = await response.json();

                    if (response.ok) {{
                        const prediction = result.predictions[0];
                        const probabilities = result.probabilities[0];
                        const predictionText = prediction === 1 ? 'Положительный прогноз' : 'Отрицательный прогноз';
                        
                        resultDiv.className = 'result success';
                        resultDiv.innerHTML = `
                            <h3>Результат предсказания:</h3>
                            <p><strong>Предсказание:</strong> ${{predictionText}} (класс: ${{prediction}})</p>
                            <p><strong>Вероятности:</strong></p>
                            <ul>
                                <li>Класс 0: ${{(probabilities[0] * 100).toFixed(2)}}%</li>
                                <li>Класс 1: ${{(probabilities[1] * 100).toFixed(2)}}%</li>
                            </ul>
                            <p><small>Версия модели: ${{result.version}}</small></p>
                        `;
                    }} else {{
                        resultDiv.className = 'result error';
                        resultDiv.innerHTML = `<h3>Ошибка:</h3><p>${{result.detail || 'Произошла ошибка при получении предсказания'}}</p>`;
                    }}
                }} catch (error) {{
                    resultDiv.className = 'result error';
                    resultDiv.innerHTML = `<h3>Ошибка:</h3><p>Не удалось подключиться к серверу: ${{error.message}}</p>`;
                }}
            }});
        </script>
    </body>
    </html>
    """
    return html_content

@root_router.post("/predict", response_model=schemas.PredictionResults, status_code=200)
async def predict(input_data: Union[schemas.MultipleDataInputs, schemas.SingleDataInput]) -> Any:
    """
    Make CatBoost predictions with the trained model
    Поддерживает как одиночные запросы, так и множественные
    """
    
    # Преобразуем входные данные в единый формат
    if isinstance(input_data, schemas.SingleDataInput):
        # Преобразуем одиночный запрос в список
        inputs_list = [input_data.model_dump()]
    else:
        # Уже множественный запрос
        inputs_list = [item.model_dump() for item in input_data.inputs]
    
    input_df = pd.DataFrame(inputs_list)

    # Advanced: You can improve performance of your API by rewriting the
    # `make prediction` function to be async and using await here.
    _logger.info(f"Making prediction on inputs: {inputs_list}")
    results = make_prediction(input_data=input_df.replace({np.nan: None}))

    if results.get("errors") is not None:
        _logger.warning(f"Prediction validation error: {results.get('errors')}")
        raise HTTPException(status_code=400, detail=json.loads(results["errors"]))

    _logger.info(f"Prediction results: {results.get('predictions')}")

    return results


app.include_router(root_router)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")