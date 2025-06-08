import logging
import sys
from datetime import datetime
from pathlib import Path

# Criar diretório de logs se não existir
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Configuração dos emojis para diferentes níveis de log
EMOJI_MAP = {
    "DEBUG": "🔍",
    "INFO": "ℹ️",
    "WARNING": "⚠️",
    "ERROR": "❌",
    "CRITICAL": "💥"
}

class EmojiFormatter(logging.Formatter):
    """Formatador personalizado que adiciona emojis aos logs."""
    
    def format(self, record):
        # Adiciona emoji baseado no nível do log
        emoji = EMOJI_MAP.get(record.levelname, "ℹ️")
        record.emoji = emoji
        
        # Adiciona timestamp
        record.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return super().format(record)

def setup_logger(name: str) -> logging.Logger:
    """Configura e retorna um logger personalizado."""
    
    # Criar logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Formato do log
    log_format = "%(emoji)s [%(timestamp)s] %(levelname)s - %(message)s"
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(EmojiFormatter(log_format))
    logger.addHandler(console_handler)
    
    # Handler para arquivo
    log_file = LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(EmojiFormatter(log_format))
    logger.addHandler(file_handler)
    
    return logger

# Criar logger global
logger = setup_logger("ppe_detection") 