from typing import Dict, List
import csv
from django.http import HttpResponse
from io import StringIO


class CSVExporter:
    '''
    Exportador de dados para o formato CSV
    '''
    
    @staticmethod
    def _flatten_dict(d: Dict, parent_key: str = '', sep: str = '_') -> Dict:
        """
        Achata dicionários aninhados.
        
        Exemplo: {'endereco': {'cidade': 'SP'}} -> {'endereco_cidade': 'SP'}
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(CSVExporter._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    @staticmethod
    def export(data: List[Dict], filename: str = 'data.csv') -> HttpResponse:
        """
        Exporta dados para CSV e retorna como download.
        
        Args:
            data: Lista de dicionários com os dados
            filename: Nome do arquivo para download
            
        Returns:
            HttpResponse com o arquivo CSV
        """
        if not data:
            return HttpResponse("Nenhum dado para exportar", status=400)
        
        # Achata os dados
        flattened_data = [CSVExporter._flatten_dict(item) for item in data]
        
        # Cria o CSV
        output = StringIO()
        fieldnames = flattened_data[0].keys()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(flattened_data)
        
        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response