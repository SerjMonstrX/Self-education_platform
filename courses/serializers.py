from rest_framework import serializers
from .models import Section, Material


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'section', 'title', 'content', 'owner']
        read_only_fields = ['owner']


class SectionSerializer(serializers.ModelSerializer):
    materials_count = serializers.SerializerMethodField()
    materials = MaterialSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = '__all__'
        read_only_fields = ['owner']

    def get_materials_count(self, instance):
        return instance.materials.count()  # lessons из модели Courses через related_name
