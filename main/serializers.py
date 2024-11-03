from rest_framework import serializers


class CalculatorSerializer(serializers.Serializer):
    input_a = serializers.CharField()
    input_b = serializers.CharField()
    operator = serializers.CharField()


class CalculatorResponseSerializer(serializers.Serializer):
    result = serializers.CharField()
