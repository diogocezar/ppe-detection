from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from ultralytics import YOLO
import time
import os
from typing import List, Optional
from pydantic import BaseModel
import shutil
from pathlib import Path
from logger import logger

# Create FastAPI app
app = FastAPI(
    title="EPI Detection API",
    description="API for detecting Personal Protective Equipment (PPE) in images",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração dos diretórios
BASE_DIR = Path(__file__).parent
MODEL_DIR = BASE_DIR / "models"
TEMP_DIR = BASE_DIR / "temp"

# Criar diretórios necessários
MODEL_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)
logger.info("📁 Diretórios verificados/criados")

# Configuração do modelo
DEFAULT_MODEL = "yolov8n-ppe.pt"  # Modelo específico para EPIs
MODEL_PATH = MODEL_DIR / DEFAULT_MODEL

# Classes reais do modelo PPE
PPE_CLASSES = {
    0: "helmet",
    1: "shield",
    2: "jacket",
    3: "dust_mask",
    4: "eye_wear",
    5: "glove",
    6: "protection_boots"
}

def download_model():
    """Download o modelo YOLO se não existir."""
    if not MODEL_PATH.exists():
        logger.info(f"🔄 Baixando modelo {DEFAULT_MODEL}...")
        try:
            # Por enquanto, usamos o modelo base do YOLOv8
            # TODO: Substituir por um modelo treinado especificamente para EPIs
            model = YOLO("yolov8n.pt")
            # Salvar o modelo na pasta models
            model.save(MODEL_PATH)
            logger.info(f"✅ Modelo salvo em {MODEL_PATH}")
            return model
        except Exception as e:
            logger.error(f"❌ Erro ao baixar modelo: {e}")
            raise
    else:
        logger.info(f"✅ Modelo encontrado em {MODEL_PATH}")
        return YOLO(MODEL_PATH)

# Load YOLO model
try:
    logger.info("🔄 Carregando modelo YOLO...")
    model = download_model()
    logger.info("✅ Modelo YOLO carregado com sucesso")
except Exception as e:
    logger.error(f"❌ Erro ao carregar modelo: {e}")
    model = None

class Detection(BaseModel):
    class_name: str
    confidence: float
    bbox: List[float]

class DetectionResponse(BaseModel):
    status: str
    detections: List[Detection]
    processing_time: float

@app.post("/detect-ppe", response_model=DetectionResponse)
async def detect_ppe(
    image: UploadFile = File(...),
    confidence: Optional[float] = 0.3,  # Reduzindo o limiar de confiança
    min_objects: Optional[int] = 1
):
    logger.info(f"📤 Recebendo imagem: {image.filename}")
    
    # Validate file type
    if not image.content_type or not image.content_type.startswith("image/"):
        logger.warning(f"⚠️ Tipo de arquivo inválido: {image.content_type}")
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Save uploaded file temporarily
    temp_path = TEMP_DIR / image.filename
    try:
        with temp_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        logger.info(f"💾 Imagem salva temporariamente: {temp_path}")
    except Exception as e:
        logger.error(f"❌ Erro ao salvar arquivo: {e}")
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    try:
        # Read image
        img = cv2.imread(str(temp_path))
        if img is None:
            logger.error("❌ Erro ao ler imagem")
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Start timing
        start_time = time.time()
        logger.info("⏱️ Iniciando detecção...")
        
        # Run detection with lower confidence threshold for debugging
        results = model(img, conf=0.1)  # Using lower confidence for debugging
        logger.info(f"🔍 Resultados brutos: {results}")
        
        # Process results
        detections = []
        
        # Agora, para cada detecção, considerar todo EPI válido
        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls[0])
                box_coords = box.xyxy[0].tolist()
                conf = float(box.conf[0])
                
                logger.info(f"📦 Objeto detectado: classe={class_id}, confiança={conf:.2f}, bbox={box_coords}")
                
                # Só aceita classes conhecidas de EPI
                class_name = PPE_CLASSES.get(class_id)
                if class_name is None:
                    logger.info(f"❌ Classe não mapeada: {class_id}")
                    continue
                logger.info(f"✅ Mapeado para EPI: {class_name}")
                
                if conf >= confidence:
                    detection = Detection(
                        class_name=class_name,
                        confidence=conf,
                        bbox=box_coords
                    )
                    detections.append(detection)
                    logger.info(f"✅ Detecção adicionada: {class_name} ({conf:.2f})")
                else:
                    logger.info(f"❌ Confiança muito baixa: {conf:.2f} < {confidence}")
        
        # Calculate processing time
        processing_time = time.time() - start_time
        logger.info(f"✅ Detecção concluída em {processing_time:.2f} segundos")
        logger.info(f"📊 {len(detections)} objetos detectados")
        
        # Check minimum objects
        if len(detections) < min_objects:
            logger.warning(f"⚠️ Mínimo de objetos não atingido: {len(detections)} < {min_objects}")
            raise HTTPException(
                status_code=400,
                detail=f"Minimum number of objects ({min_objects}) not detected"
            )
        
        return DetectionResponse(
            status="success",
            detections=detections,
            processing_time=processing_time
        )
    
    except Exception as e:
        logger.error(f"❌ Erro durante o processamento: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Clean up temporary file
        if temp_path.exists():
            temp_path.unlink()
            logger.info("🧹 Arquivo temporário removido")

@app.get("/health")
async def health_check():
    status = "healthy" if model is not None else "unhealthy"
    logger.info(f"🏥 Health check: {status}")
    return {
        "status": status,
        "model_loaded": model is not None,
        "model_path": str(MODEL_PATH) if MODEL_PATH.exists() else None
    }

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 API iniciada")
    logger.info(f"🌐 Servidor rodando em http://localhost:8000")
    logger.info(f"📁 Diretório de modelos: {MODEL_DIR}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 API encerrada")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 