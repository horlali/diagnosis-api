from multiprocessing import Process
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import FileUploadParser, MultiPartParser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

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

        print(file_obj)
        print(email)
        print(record_type)

        operations = Operations(
            file_object=file_obj,
            email=email,
            csv_type=record_type,
        )
        process = Process(target=operations.service)
        process.start()

        resp = {"status": "success", "detail": "Upload Successsfully"}
        return Response(resp, status=status.HTTP_200_OK)


# TODO: Uploading files :DONE
# TODO: Emails and Django Signals :SWAPPED FOR MULTIPROCESSING
# TODO: Multiprocess the upload view and send the email after :DONE
# TODO: Optimize and clean code :DONE

# TODO: Seed data into database
# TODO: Unit test
