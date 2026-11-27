from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import VolunteerProfile,Organization,DonorProfile,CharityProfile



User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = ["id", "email", "password", "password_confirm", "role", "username"]
        read_only_fields = ["id"]

    def validate_role(self, value):
        allowed_roles = {User.Role.DONOR, User.Role.CHARITY, User.Role.VOLUNTEER}

        if value not in allowed_roles:
            raise serializers.ValidationError("Invalid registration role.")

        return value

    def validate_email(self, value):
        email = value.strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                "An account with this email already exits."
            )

        return email

    def validate_username(self, value):
        username = value.strip().lower()
        if User.objects.filter(username__iexact=username).exists():
            raise serializers.ValidationError(
                "An account with this username already exists."
            )
        return username

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Passwords do not match."}
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]
        read_only_fields = fields


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True, allow_blank=False)

    def validate_refresh(self, value):
        try:
            self.token = RefreshToken(value)
        except TokenError:
            raise serializers.ValidationError(
                "Invalid, expired, or revoked refresh token."
            )
        return value

    def save(self, **kwargs):
        try:
           self.token.blacklist()
        except TokenError:
            raise serializers.ValidationError(
                {"refresh":"Invalid, expired, or revoked refresh token."}
            )


class VolunteerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerProfile
        fields = [
            "id",
            "user",
            "is_available",
            "transport_mode"

            ]

        read_only_fields = ["id","user"]

    def validate(self,attrs):
        request = self.context["request"]
        user = request.user

        if user.role != User.Role.VOLUNTEER:
            raise serializers.ValidationError(
                "Only volunteers can manage volunteer profiles."

                )
        return attrs

    def create(self,validated_data):
        user = self.context["request"].user
        if VolunteerProfile.objects.filter(user=user).exists():
            raise serializers.ValidationError(
                "Volunteer profile already exists."

                )
        return VolunteerProfile.objects.create(
            user=user,
            **validated_data
            )


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "organization_type",
            "address",
            "is_verified",
            "created_at"



            ]

        read_only_fields = ["id","is_verified","created_at"]


    def validate_name(self,value):
        name = value.strip()

        if len(name) < 3:
            raise serializers.ValidationError(
                "Organization name must contain at least 3 characters. "

                )
        return name


class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonorProfile
        fields = [
            "id",
            "user",
            "organization"
            ]

        read_only_fields = ["id","user","organization"]


    def validate(self,attrs):
        request = self.context["request"]
        user = request.user
        if user.role != User.Role.DONOR:
            raise serializers.ValidationError(
                      "Only donors can manage donor profiles."
                )
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        if DonorProfile.objects.filter(user=user).exists():
            raise serializers.ValidationError(
                  "Donor profile already exists."
                
                )
        return DonorProfile.objects.create(user=user,**validated_data)



class CharitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CharityProfile
        fields = [
            "id",
            "user",
            "organization"
            ]

        read_only_fields = ["id","user","organization"]


    def validate(self,attrs):
        request = self.context["request"]
        user = request.user
        if user.role != User.Role.CHARITY:
            raise serializers.ValidationError(
                      "Only charity can manage charity profiles."
                )
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        if CharityProfile.objects.filter(user=user).exists():
            raise serializers.ValidationError(
                  "Charity profile already exists."
                
                )
        organization = validated_data.get("organization")
        if organization is None:
            raise serializers.ValidationError(
                {
                    "organization":"An authorized organization is required."

                    })
        return CharityProfile.objects.create(user=user,**validated_data)



