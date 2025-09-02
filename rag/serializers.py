from rest_framework import serializers


class VectorStoreSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, allow_blank=True)
    user_id = serializers.CharField(required=True, allow_blank=False)
