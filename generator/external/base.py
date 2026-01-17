# generator/generators/external/base.py
"""Classe base para geradores que consomem APIs externas."""
import requests
from typing import Dict, Any, Optional
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)


class BaseExternalGenerator:
    """
    Classe base para geradores que consomem APIs externas.
    
    Fornece funcionalidades comuns como:
    - Cache de requisições
    - Tratamento de erros
    - Timeout configurável
    - Retry logic
    """
    
    BASE_URL: str = ""
    TIMEOUT: int = 5
    CACHE_SIZE: int = 100
    
    def _make_request(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        use_cache: bool = True
    ) -> Optional[Dict]:
        """
        Faz requisição HTTP para a API externa.
        
        Args:
            endpoint: Endpoint da API
            params: Parâmetros da requisição
            use_cache: Se deve usar cache
            
        Returns:
            Dicionário com resposta ou None em caso de erro
        """
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            if use_cache:
                return self._cached_request(url, frozenset(params.items()) if params else None)
            else:
                response = requests.get(url, params=params, timeout=self.TIMEOUT)
                response.raise_for_status()
                return response.json()
                
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout ao acessar {url}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao acessar API: {e}")
            return None
    
    @lru_cache(maxsize=100)
    def _cached_request(self, url: str, frozen_params):
        """Versão cacheada da requisição."""
        params = dict(frozen_params) if frozen_params else None
        response = requests.get(url, params=params, timeout=self.TIMEOUT)
        response.raise_for_status()
        return response.json()
    
    def _generate_fallback(self) -> Dict:
        """
        Gera dados fake como fallback quando API está indisponível.
        Deve ser implementado pelas classes filhas.
        """
        raise NotImplementedError("Subclasses devem implementar _generate_fallback")