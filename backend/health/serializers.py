from rest_framework import serializers

class LivenessResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    service = serializers.CharField()

class ReadinessResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    database = serializers.CharField()