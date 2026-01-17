# generator/api/views.py
"""Views da API REST."""
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from generator.generators import PersonGenerator, CompanyGenerator
from generator.exporters import JSONExporter, CSVExporter
from .serializers import (
    GenerateDataSerializer,
    GeneratedDataResponseSerializer,
    PersonSerializer,
    CompanySerializer
)


class GeneratePersonAPIView(APIView):
    """
    API para gerar dados fake de pessoas.
    
    Gera dados realistas de pessoas brasileiras incluindo nome, CPF, RG,
    email, telefone e endereço completo.
    """
    
    @extend_schema(
        summary="Gerar dados de pessoas",
        description="Gera dados fake de pessoas brasileiras com informações completas",
        parameters=[
            OpenApiParameter(
                name='quantity',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Quantidade de pessoas a gerar (1-1000)',
                required=False,
                default=10
            ),
            OpenApiParameter(
                name='export_format',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Formato de exportação (json ou csv)',
                required=False,
                default='json',
                enum=['json', 'csv']
            ),
        ],
        responses={
            200: GeneratedDataResponseSerializer,
            400: OpenApiTypes.OBJECT
        },
        tags=['Geração de Dados']
    )
    def get(self, request):
        """Endpoint GET para gerar pessoas."""
        # Valida os parâmetros
        serializer = GenerateDataSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        quantity = serializer.validated_data['quantity']
        export_format = request.query_params.get('export_format', 'json')
        
        # Gera os dados
        generator = PersonGenerator()
        data = generator.generate(quantity=quantity)
        
        # Retorna no formato solicitado
        if export_format == 'csv':
            csv_response = CSVExporter.export(data, filename=f'pessoas_{quantity}.csv')
            return csv_response
        else:
            return Response({
                'success': True,
                'data': data,
                'total': len(data),
                'message': f'{len(data)} pessoa(s) gerada(s) com sucesso'
            })


class GenerateCompanyAPIView(APIView):
    """
    API para gerar dados fake de empresas.
    
    Gera dados realistas de empresas brasileiras incluindo razão social,
    CNPJ, email, telefone e endereço completo.
    """
    
    @extend_schema(
        summary="Gerar dados de empresas",
        description="Gera dados fake de empresas brasileiras com informações completas",
        parameters=[
            OpenApiParameter(
                name='quantity',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Quantidade de empresas a gerar (1-1000)',
                required=False,
                default=10
            ),
            OpenApiParameter(
                name='export_format',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Formato de exportação (json ou csv)',
                required=False,
                default='json',
                enum=['json', 'csv']
            ),
        ],
        responses={
            200: GeneratedDataResponseSerializer,
            400: OpenApiTypes.OBJECT
        },
        tags=['Geração de Dados']
    )
    def get(self, request):
        """Endpoint GET para gerar empresas."""
        # Valida os parâmetros
        serializer = GenerateDataSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        quantity = serializer.validated_data['quantity']
        export_format = request.query_params.get('export_format', 'json')
        
        # Gera os dados
        generator = CompanyGenerator()
        data = generator.generate(quantity=quantity)
        
        # Retorna no formato solicitado
        if export_format == 'csv':
            csv_response = CSVExporter.export(data, filename=f'empresas_{quantity}.csv')
            return csv_response
        else:
            return Response({
                'success': True,
                'data': data,
                'total': len(data),
                'message': f'{len(data)} empresa(s) gerada(s) com sucesso'
            })


class APIRootView(APIView):
    """
    API Root - Informações sobre a API.
    """
    
    @extend_schema(
        summary="Informações da API",
        description="Retorna informações sobre os endpoints disponíveis na API",
        responses={200: OpenApiTypes.OBJECT},
        tags=['Informações']
    )
    def get(self, request):
        """Retorna informações sobre a API."""
        return Response({
            'message': 'Bem-vindo à Fake Data Generator API',
            'version': '1.0.0',
            'endpoints': {
                'persons': request.build_absolute_uri('/api/v1/generate/person/'),
                'companies': request.build_absolute_uri('/api/v1/generate/company/'),
                'docs': request.build_absolute_uri('/api/v1/docs/'),
                'schema': request.build_absolute_uri('/api/v1/schema/'),
            },
            'documentation': 'Acesse /api/v1/docs/ para ver a documentação completa',
        })