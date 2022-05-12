from multiprocessing import Process
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import FileUploadParser, MultiPartParser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import validators

from api.models import Category, Diagnosis
from api.serializers import CategorySerializer, DiagnosisSerializer
from utils.services import Operations


class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            category_code = Category.objects.get(
                category_code=request.data.get("category_code")
            ).category_code
            if category_code == request.data.get("category_code"):
                err = {
                    "status": "failed",
                    "detail": f"Category with code {category_code} already exist",
                }
                return Response(err, status=status.HTTP_409_CONFLICT)

        except Category.DoesNotExist:
            self.perform_create(serializer)
            resp = {
                "status": "success",
                "detail": "Category Created",
                "data": serializer.data,
            }
            return Response(resp, status=status.HTTP_201_CREATED)


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
            category_code = Category.objects.get(
                id=request.data.get("category")
            ).category_code

        except Category.DoesNotExist:
            category_code = request.data.get("category_code")
            err = {
                "status": "failed",
                "detail": f"The category code {category_code} does not exist!\
                    ",
            }
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

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
    parser_classes = (MultiPartParser, FileUploadParser)

    params = [
        openapi.Parameter(
            "file",
            openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            description="CSV File to be uploaded",
        ),
        openapi.Parameter(
            "email",
            openapi.IN_FORM,
            type=openapi.TYPE_STRING,
            description="Email for notification",
        ),
        openapi.Parameter(
            "record_type",
            openapi.IN_FORM,
            type=openapi.TYPE_STRING,
            description="(category or diagnosis)",
        ),
    ]

    @swagger_auto_schema(manual_parameters=params)
    def post(self, request):
        file_obj = request.FILES["file"]
        email = request.data["email"]
        record_type = request.data["record_type"]

        if record_type.lower() == "category" or record_type.lower() == "diagnosis":
            if not validators.email(email):
                err = {"status": "failed", "detail": "Please enter a valid email"}
                return Response(err, status=status.HTTP_400_BAD_REQUEST)

            if str(file_obj).split(".")[-1].lower() != "csv":
                err = {
                    "status": "failed",
                    "detail": "Uploaded file is not a valid csv file",
                }
                return Response(err, status=status.HTTP_400_BAD_REQUEST)

            operations = Operations(
                file_object=file_obj,
                email=email,
                csv_type=record_type.lower(),
            )

            process = Process(target=operations.service)
            process.start()

            resp = {"status": "success", "detail": "Upload Successsfully"}
            return Response(resp, status=status.HTTP_200_OK)

        else:
            err = {
                "status": "failed",
                "detail": "KeyError [use 'category' or 'diagnosis']",
            }
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


# TODO: Seed data into database
# TODO: Unit test
