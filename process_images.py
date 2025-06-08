import cv2
import json
import requests
import os
from pathlib import Path
from datetime import datetime

# Configuração dos diretórios
BASE_DIR = Path(__file__).parent
TEST_IMAGES_DIR = BASE_DIR / "test_images"
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

def draw_detections(image_path, detections):
    """Desenha as bounding boxes e labels na imagem."""
    # Ler a imagem
    img = cv2.imread(str(image_path))
    
    # Cores para diferentes classes de EPI (BGR)
    colors = {
        'helmet': (0, 255, 0),      # Verde
        'safety_glasses': (255, 0, 0), # Azul
        'gloves': (0, 0, 255),      # Vermelho
        'safety_boots': (255, 255, 0), # Ciano
        'safety_belt': (255, 0, 255),  # Magenta
        'ear_protection': (0, 255, 255), # Amarelo
        'respirator': (128, 0, 128),    # Roxo
        'safety_vest': (0, 128, 128)    # Verde água
    }
    
    # Desenhar cada detecção
    for detection in detections:
        # Extrair coordenadas da bounding box
        x1, y1, x2, y2 = map(int, detection['bbox'])
        
        # Escolher cor baseada na classe
        color = colors.get(detection['class_name'], (255, 255, 255))
        
        # Desenhar retângulo
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        
        # Preparar texto com classe e confiança
        label = f"{detection['class_name']}: {detection['confidence']:.2f}"
        
        # Desenhar fundo preto opaco para o texto
        (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        label_bg_top_left = (x1, y1 - text_height - 10)
        label_bg_bottom_right = (x1 + text_width + 6, y1)
        cv2.rectangle(img, label_bg_top_left, label_bg_bottom_right, (0, 0, 0), -1)
        
        # Desenhar texto branco mais espesso
        cv2.putText(img, label, (x1 + 3, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    return img

def process_image(image_path):
    """Processa uma imagem e salva o resultado."""
    print(f"🔄 Processando {image_path.name}...")
    
    # Detectar o tipo MIME
    ext = image_path.suffix.lower()
    if ext in ['.jpg', '.jpeg']:
        mime = 'image/jpeg'
    elif ext == '.png':
        mime = 'image/png'
    else:
        mime = 'application/octet-stream'
    
    # Fazer requisição para a API
    with open(image_path, 'rb') as f:
        files = {'image': (image_path.name, f, mime)}
        response = requests.post('http://localhost:8000/detect-ppe', files=files)
    
    if response.status_code == 200:
        # Processar resposta
        result = response.json()
        
        # Criar nome do arquivo de resultado
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_filename = f"result_{image_path.stem}_{timestamp}.jpg"
        result_path = RESULTS_DIR / result_filename
        
        # Desenhar detecções na imagem
        result_img = draw_detections(image_path, result['detections'])
        
        # Salvar imagem com detecções
        cv2.imwrite(str(result_path), result_img)
        
        # Salvar JSON com resultados
        json_path = RESULTS_DIR / f"result_{image_path.stem}_{timestamp}.json"
        with open(json_path, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"✅ Resultado salvo em {result_path}")
        print(f"📊 {len(result['detections'])} objetos detectados")
        print(f"⏱️ Tempo de processamento: {result['processing_time']:.2f}s")
    else:
        print(f"❌ Erro ao processar {image_path.name}: {response.text}")

def main():
    """Processa todas as imagens no diretório de teste."""
    print(f"📁 Processando imagens de {TEST_IMAGES_DIR}")
    
    # Processar cada imagem
    for image_path in TEST_IMAGES_DIR.glob("*.jpg"):
        process_image(image_path)
    
    print(f"\n✨ Processamento concluído! Resultados salvos em {RESULTS_DIR}")

if __name__ == "__main__":
    main() 