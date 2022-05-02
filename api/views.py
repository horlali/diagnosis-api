from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import FileUploadParser

from api.models import Category, Diagnosis
from api.serializers import CategorySerializer, DiagnosisSerializer


class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            category_code = Category.objects.get(
                code=request.data.get("category_code")
            ).code
            if category_code == request.data.get("category_code"):
                err = {"status": "failed", "detail": "Category already exists"}
                return Response(err, status=status.HTTP_409_CONFLICT)
            else:
                raise Exception("I will look into this later")

        except:
            try:
                self.perform_create(serializer)
                resp = {
                    "status": "success",
                    "detail": "Category Created",
                    "data": serializer.data,
                }
                return Response(resp, status=status.HTTP_201_CREATED)

            except IntegrityError as e:
                code = request.data.get("category_code")
                err = {
                    "status": "failed",
                    "detail": f"Category with {code} already exist, consider updating!",
                }
                return Response(err, status=status.HTTP_409_CONFLICT)


class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "id"


class DiagnosisListView(ListCreateAPIView):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            category_id = Diagnosis.objects.get(
                diagnosis_code=request.data.get("diagnosis_code")
            ).category.id
            diagnosis_id = Diagnosis.objects.get(
                diagnosis_code=request.data.get("diagnosis_code")
            ).diagnosis_code

            if category_id == request.data.get(
                "category"
            ) and diagnosis_id == request.data.get("diagnosis_code"):
                err = {"status": "failed", "detail": "Diagnosis already exists"}
                return Response(err, status=status.HTTP_409_CONFLICT)

            else:
                raise Exception("I will look into this later")

        except:
            try:
                self.perform_create(serializer=serializer)

                resp = {
                    "status": "success",
                    "detail": "Diagnosis Created",
                    "data": serializer.data,
                }
                return Response(resp, status=status.HTTP_201_CREATED)

            except IntegrityError as e:
                err = {"status": "failed", "detail": "Diagnosis already exist"}
                return Response(err, status=status.HTTP_409_CONFLICT)


class DiagnosisDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer
    lookup_field = "id"


class UploadCSV(APIView):
    parser_classes = (FileUploadParser)

    def post(self, request):
        file_obj = request.FILES['csv_file']
        
    pass


# TODO: Uploading files
# TODO: Emails and Django Signals
# TODO: Unit test
# TODO: Seed data into database
# TODO: Optimize and clean code
