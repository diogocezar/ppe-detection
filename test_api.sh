#!/bin/bash

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Testando endpoint de saúde...${NC}"
curl -s http://localhost:8000/health | python3 -m json.tool

echo -e "\n${BLUE}📸 Processando imagens de teste...${NC}"
python3 process_images.py 