from rest_framework import serializers
from .models import User, Equipment, Request, Rating


# -------------------------
# User Serializer
# -------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id',
            'name',
            'email',
            'contact_no',
            'lat',
            'long',
            'create_date',
            'update_date'
        ]


# -------------------------
# Equipment Serializer
# -------------------------
class EquipmentSerializer(serializers.ModelSerializer):
    donor_name = serializers.CharField(source='donor.name', read_only=True)
    donor_lat = serializers.FloatField(source='donor.lat', read_only=True)
    donor_long = serializers.FloatField(source='donor.long', read_only=True)

    class Meta:
        model = Equipment
        fields = [
            'equipment_id',
            'equipment_name',
            'available_status',
            'equipment_img',
            'donor',
            'donor_name',
            'donor_lat',
            'donor_long',
            'create_date',
            'update_date'
        ]


# -------------------------
# Request Serializer
# -------------------------
class RequestSerializer(serializers.ModelSerializer):
    requester_name = serializers.CharField(source='requester.name', read_only=True)
    donor_name = serializers.CharField(source='donor.name', read_only=True)
    equipment_name = serializers.CharField(source='equipment.equipment_name', read_only=True)

    class Meta:
        model = Request
        fields = [
            'req_id',
            'req_date',
            'priority',
            'status',
            'update_date',
            'requester',
            'requester_name',
            'donor',
            'donor_name',
            'equipment',
            'equipment_name'
        ]


# -------------------------
# Rating Serializer
# -------------------------
class RatingSerializer(serializers.ModelSerializer):
    reporter_name = serializers.CharField(source='reporter.name', read_only=True)
    product_name = serializers.CharField(source='product.equipment_name', read_only=True)

    class Meta:
        model = Rating
        fields = [
            'rating_id',
            'score',
            'feedback',
            'rating_date',
            'reporter',
            'reporter_name',
            'product',
            'product_name'
        ]
