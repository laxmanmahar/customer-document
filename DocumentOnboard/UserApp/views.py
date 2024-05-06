from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from UserApp import serializers as UserAppSerializer
from UserApp import models as UserAppModel
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
import pytesseract
from django.http import JsonResponse
from django.core.files.base import ContentFile
from PIL import Image
import pytesseract


class Signup(APIView):
    permission_classes = []

    def post(self: "Signup", request, version):
        post_serializers = UserAppSerializer.UserRegisterSerializers
        data = request.data
        if UserAppModel.CustomeUser.objects.filter(email=data.get("email")).exists():
            return Response({"error": "Email is already registered"}, 400)

        serializer = post_serializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": "User has been created."},
                status=status.HTTP_200_OK,
            )

        else:
            return Response({"error": serializer.errors}, 400)


class SetPassword(APIView):
    permission_classes = []

    def post(self, request, version):
        data = request.data
        userObj = get_object_or_404(UserAppModel.CustomeUser, pk=data.get("user_id"))
        userObj.set_password(data.get("password"))
        print(userObj.password)
        userObj.save()
        return Response({"success": "password successfully set"}, 200)


class UserLogin(APIView):
    permission_classes = []

    def post(self, request, version):
        data = request.data
        if not UserAppModel.CustomeUser.objects.filter(
            email=data.get("email")
        ).exists():
            return Response(
                {"error": "Invalid Credentials.", "active_subscriber": True},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        user = authenticate(
            request, username=data.get("email"), password=data.get("password")
        )
        if user is not None:
            tokenObj, created = Token.objects.get_or_create(user=user)
            return Response({"success": "login successfully", "key": tokenObj.key})
        else:
            return Response(
                {"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class FileUpload(APIView):
    permission_classes = []

    def post(self, request, version):
        data = request.data
        userfileobj = UserAppModel.CustomeUser.objects.get(id=data.get("userImage"))
        print(userfileobj)
        createdObj = UserAppModel.FileUpload.objects.create(
            file=data.get("file"), userImage=userfileobj
        )

        image_file = createdObj.file

        if image_file:
            image = Image.open(image_file)
            extracted_text = pytesseract.image_to_string(image)
            lines = extracted_text.split("\n")
            name = ""
            nationality = ""
            surname = ""
            dob = ""
            for line in lines:
                if "PATER" in line:
                    name = line.split("PATER")[-1].split("?")[0].strip()
                elif "orig" in line:
                    surname = line.split("/")[-1].strip()
                elif "Ethiopian" in line:
                    nationality = line.split("National ib")[-1].split("Digital")[0].strip()
                elif "Sep" in line:
                    dob = line 
                elif "Male" in line:
                    gender = line
                    print(gender)

            UserAppModel.Country.objects.create(name=nationality)
            country_obj = UserAppModel.Country.objects.get(id=2)
            UserAppModel.Customer.objects.create(
                surname=surname,
                firstName=surname.split(",")[0],
                nationality=country_obj,
                gender=gender
            )

            return Response(
                {"extracted_text": extracted_text, "message": "Customer created successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "No image file provided"}, status=status.HTTP_400_BAD_REQUEST
            )


class GetCustomer(APIView):
    permission_classes = []

    def get(self, request, version, pk):
        customer = get_object_or_404(
            UserAppModel.Customer, pk=pk
        )

        serializer = UserAppSerializer.CustomerSerializer(
            customer, context={"request": request}
        )
        return Response({"success": True, "detail": serializer.data})
