from rest_framework import serializers

class DonationSerializer(serializers.Serializer):
    food_name = serializers.CharField()
    quantity = serializers.IntegerField()

    def validate_quantity(self,value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero")
        return value



from rest_framework.exceptions import ValidationError


def validate_quantity(quantity):
    if quantity <= 0:
        raise ValidationError(
            "Quantity must be positive."
        )