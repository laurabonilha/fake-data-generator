import json
from typing import List, Dict
from django.http import HttpResponse


class JSONExporter:
    """Exportador de dados para formato JSON."""
    
    @staticmethod
    def export(data: List[Dict], filename: str = 'data.json') -> HttpResponse:
        """
        Exporta dados para JSON e retorna como download.
        
        Args:
            data: Lista de dicionários com os dados
            filename: Nome do arquivo para download
            
        Returns:
            HttpResponse com o arquivo JSON
        """
        response = HttpResponse(
            json.dumps(data, ensure_ascii=False, indent=2),
            content_type='application/json'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response