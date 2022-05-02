from rest_framework import serializers
from api.models import Category, Diagnosis


class CategorySerializer(serializers.ModelSerializer):
    category_code = serializers.CharField(max_length=25)
    category_title = serializers.CharField(max_length=1024)

    class Meta:
        model = Category
        fields = ["id", "category_code", "category_title"]


class DiagnosisSerializer(serializers.ModelSerializer):
    diagnosis_code = serializers.CharField(max_length=10)
    abbreviated_desc = serializers.CharField(max_length=2048)
    category_code = serializers.SerializerMethodField()
    category_title = serializers.SerializerMethodField()

    def get_category_code(self, obj):
        return str(obj.category.category_code)

    def get_category_title(self, obj):
        return str(obj.category.category_title)

    class Meta:
        model = Diagnosis
        fields = [
            "id",
            "icd_type",
            "category_code",
            "diagnosis_code",
            "full_code",
            "abbreviated_desc",
            "full_desc",
            "category",
            "category_title",
        ]
