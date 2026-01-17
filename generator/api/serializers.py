# generator/api/serializers.py
"""Serializers para a API REST."""
from rest_framework import serializers


class GenerateDataSerializer(serializers.Serializer):
    """
    Serializer para validar parâmetros de geração de dados.
    """
    quantity = serializers.IntegerField(
        min_value=1,
        max_value=1000,
        default=10,
        help_text="Quantidade de registros a gerar (1-1000)"
    )
    
    def validate_quantity(self, value):
        """Valida a quantidade."""
        if value < 1:
            raise serializers.ValidationError("A quantidade deve ser no mínimo 1")
        if value > 1000:
            raise serializers.ValidationError("A quantidade deve ser no máximo 1000")
        return value


class PersonSerializer(serializers.Serializer):
    """Serializer para representar dados de uma pessoa."""
    nome_completo = serializers.CharField()
    cpf = serializers.CharField()
    rg = serializers.CharField()
    email = serializers.EmailField()
    data_nascimento = serializers.CharField()
    telefone_fixo = serializers.CharField()
    celular = serializers.CharField()
    profissao = serializers.CharField()
    endereco = serializers.DictField()


class CompanySerializer(serializers.Serializer):
    """Serializer para representar dados de uma empresa."""
    razao_social = serializers.CharField()
    nome_fantasia = serializers.CharField()
    cnpj = serializers.CharField()
    email = serializers.EmailField()
    telefone = serializers.CharField()
    endereco = serializers.DictField()


class GeneratedDataResponseSerializer(serializers.Serializer):
    """Serializer para a resposta da API."""
    success = serializers.BooleanField()
    data = serializers.ListField()
    total = serializers.IntegerField()
    message = serializers.CharField(required=False)