# Prompt para Desenvolvimento de API de Detecção de EPIs

## Descrição do Problema
Desenvolver uma API REST que receba imagens e automaticamente identifique o uso de Equipamentos de Proteção Individual (EPIs) nessas imagens. A API deve ser capaz de detectar diferentes tipos de EPIs comuns em ambientes industriais e de construção.

## Requisitos Funcionais

### 1. Endpoint da API
- Endpoint POST para upload de imagens
- Suporte para múltiplos formatos de imagem (JPG, PNG, JPEG)
- Resposta em formato JSON com os resultados da detecção
- Códigos de status HTTP apropriados para diferentes situações

### 2. Funcionalidades de Detecção
- Identificação de diferentes tipos de EPIs:
  - Capacete de segurança
  - Óculos de proteção
  - Luvas de proteção
  - Calçados de segurança
  - Cintos de segurança
  - Protetores auditivos
  - Máscaras respiratórias
  - Vestimentas de proteção

### 3. Processamento de Imagem
- Pré-processamento da imagem para melhorar a detecção
- Detecção de múltiplos EPIs em uma única imagem
- Geração de relatório com lista de EPIs identificados
- Coordenadas dos EPIs detectados na imagem (bounding boxes)

## Requisitos Não Funcionais

### 1. Performance
- Tempo de resposta máximo de 5 segundos para processamento de imagens
- Suporte para imagens de até 10MB
- Processamento assíncrono para imagens maiores

### 2. Segurança
- Validação de tipos de arquivo
- Proteção contra uploads maliciosos
- Limpeza automática de arquivos temporários

## Tecnologias Sugeridas

### Backend
- Python com FastAPI
- OpenCV para pré-processamento de imagens
- TensorFlow ou PyTorch para modelo de detecção

### Modelo de IA
- YOLOv5 ou YOLOv8 para detecção de objetos
- Dataset personalizado de EPIs para treinamento

## Testes e Uso

### Estrutura de Diretórios para Testes
```
test_images/
  ├── sample1.jpg
  ├── sample2.png
  └── sample3.jpeg
```

### Exemplos de Comandos CURL

1. Upload de imagem simples:
```bash
curl -X POST http://localhost:8000/detect-ppe \
  -F "image=@test_images/sample1.jpg"
```

2. Upload com parâmetros adicionais:
```bash
curl -X POST http://localhost:8000/detect-ppe \
  -F "image=@test_images/sample2.png" \
  -F "confidence=0.5" \
  -F "min_objects=1"
```

### Formato da Resposta
```json
{
  "status": "success",
  "detections": [
    {
      "class": "helmet",
      "confidence": 0.95,
      "bbox": [x1, y1, x2, y2]
    },
    {
      "class": "gloves",
      "confidence": 0.87,
      "bbox": [x1, y1, x2, y2]
    }
  ],
  "processing_time": 1.23
}
```

## Considerações Adicionais

### Dataset e Treinamento
- Necessidade de dataset robusto de imagens com EPIs
- Diferentes ângulos e condições de iluminação
- Diversidade de ambientes e situações

### Escalabilidade
- Possibilidade de processamento em lote
- Cache de resultados para imagens similares
- Arquitetura que permita escalar horizontalmente

### Manutenção
- Logs detalhados para debugging
- Monitoramento de performance
- Documentação clara do código e da API

## Próximos Passos
1. Configurar ambiente de desenvolvimento
2. Implementar endpoint básico
3. Desenvolver modelo de detecção
4. Implementar processamento de imagem
5. Adicionar validações e tratamento de erros
6. Testes com imagens reais
7. Documentação da API 