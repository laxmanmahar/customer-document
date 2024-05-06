from rest_framework import serializers
from UserApp import models as UserAppModel
import datetime


class UserRegisterSerializers(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=200)

    def create(self, validated_data):
        userObj = UserAppModel.CustomeUser.objects.create_user(
            username=validated_data.get("email"),
            email=validated_data.get("email"),
            password=str(datetime.datetime.now())
        )

        userObj.name = validated_data.get("name")
        userObj.save()
        return userObj


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAppModel.Customer
        fields = [
            "id",
            "surname",
            "firstName",
            "nationality",
            "gender"
        ]
