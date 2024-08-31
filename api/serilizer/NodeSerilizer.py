from rest_framework import serializers

class NodeStructureSerializer(serializers.Serializer):
    target = serializers.CharField()
    location = serializers.CharField()

class NodeSerializer(serializers.Serializer):
    id = serializers.CharField()
    structure = serializers.DictField(child=NodeStructureSerializer())
