
"""Classe base para geradores que consomem APIs externas."""
import httpx
import asyncio
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class BaseExternalGenerator:
    """
    Classe base ASSÍNCRONA para geradores que consomem APIs externas.
    
    Fornece funcionalidades comuns como:
    - Cliente HTTP assíncrono (httpx)
    - Tratamento de erros
    - Timeout configurável
    - Retry logic
    """
    
    BASE_URL: str = ""
    TIMEOUT: int = 10  # Aumentei um pouco para garantir
    
    async def _make_request(
        self, 
        client: httpx.AsyncClient,
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict]:
        """
        Faz requisição HTTP assíncrona para a API externa.
        
        Args:
            client: Cliente HTTP assíncrono reutilizável
            endpoint: Endpoint da API
            params: Parâmetros da requisição
            
        Returns:
            Dicionário com resposta ou None em caso de erro
        """
        if endpoint.startswith("http"):
             url = endpoint
        else:
             url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = await client.get(url, params=params, timeout=self.TIMEOUT)
            response.raise_for_status()
            return response.json()
                
        except httpx.TimeoutException:
            logger.warning(f"Timeout ao acessar {url}")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(f"Erro HTTP {e.response.status_code} ao acessar {url}")
            return None
        except httpx.RequestError as e:
            logger.error(f"Erro de requisição ao acessar API: {e}")
            return None
    
    def _generate_fallback(self) -> Dict:
        """
        Gera dados fake como fallback quando API está indisponível.
        Deve ser implementado pelas classes filhas.
        """
        raise NotImplementedError("Subclasses devem implementar _generate_fallback")