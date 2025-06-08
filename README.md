# PPE Detection API

API para detecção de Equipamentos de Proteção Individual (EPIs) em imagens usando YOLOv8.

## Funcionalidades

- Detecção de EPIs em imagens
- Suporte para múltiplos tipos de EPIs:
  - Capacetes
  - Coletes de segurança
  - Máscaras
  - Botas de segurança
  - Luvas
  - Óculos de proteção
  - Proteção auditiva
- Retorna resultados com scores de confiança e bounding boxes
- Gera imagens anotadas com as detecções

## Requisitos

- Python 3.8+
- FastAPI
- Ultralytics YOLOv8
- OpenCV

## Instalação

1. Clone o repositório:
```bash
git clone <repository-url>
cd labs
```

2. Crie e ative um ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip3 install -r requirements.txt
```

4. (Opcional) Baixe o modelo YOLOv8 para detecção de EPIs e coloque na pasta `models/` se necessário.

## Uso

1. Inicie o servidor:
```bash
uvicorn main:app --reload
```

2. Acesse a documentação da API em `http://localhost:8000/docs`

3. Use o endpoint `/detect` para fazer upload e processar imagens:
```bash
curl -X POST "http://localhost:8000/detect" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@caminho/para/sua/imagem.jpg"
```

## Endpoints

- `GET /`: Informações da API
- `GET /health`: Verificação de saúde
- `POST /detect`: Upload e processamento de imagem

## Formato da Resposta

O endpoint `/detect` retorna uma resposta JSON com a seguinte estrutura:

```json
{
    "detections": [
        {
            "class": "helmet",
            "confidence": 0.95,
            "bbox": [x1, y1, x2, y2]
        }
    ],
    "result_image": "caminho/para/imagem/processada.jpg"
}
```

## Estrutura do Projeto

```
labs/
├── main.py              # Aplicação FastAPI principal
├── process_images.py     # Funções de processamento de imagem
├── logger.py             # Logger customizado
├── requirements.txt      # Dependências do projeto
├── README.md             # Documentação
├── models/               # Modelos YOLOv8
├── results/              # Imagens processadas
├── test_images/          # Imagens de teste
├── temp/                 # Arquivos temporários
└── venv/                 # Ambiente virtual (não versionar)
```

## Contribuindo

1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Commit suas alterações
4. Faça push para a branch
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

## 📧 Suporte

Para suporte, envie um email para [seu-email@exemplo.com] ou abra uma issue no repositório. 