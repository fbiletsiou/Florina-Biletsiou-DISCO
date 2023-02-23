from rest_framework import serializers

from .models import UploadedFile, User


def validate_image_format(content_type):
    """
    Validating the image file format.
    Currently valid: png, jpeg
    """

    if content_type == "image/png":
        return "PNG"
    elif content_type == "image/jpeg":
        return "JPEG"
    else:
        raise serializers.ValidationError("Invalid file format")


class UploadedFileSerializer(serializers.ModelSerializer):
    """
    Serializer of the Uploaded File model
    """

    created_by = serializers.ReadOnlyField(source='created_by.username')
    created_by_id = serializers.ReadOnlyField(source='created_by.id', required=False, default=None)
    image_url = serializers.ImageField(required=True)

    image_thumbnail200 = serializers.ImageField(read_only=True)
    image_thumbnail400 = serializers.ImageField(read_only=True)

    class Meta:
        model = UploadedFile
        fields = ['id',
                  'created_by',
                  'created_by_id',
                  'name',
                  'file_format',
                  'file_size',
                  'image_url',
                  'image_thumbnail200',
                  'image_thumbnail400',
                  'date_started',
                  'last_edited'
                  ]

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')
        if request is not None and request.user.tier == 'Basic':
            fields.pop('image_thumbnail400', None)
            fields.pop('image_url', None)
        return fields


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer of the customized User model
    """

    images = serializers.PrimaryKeyRelatedField(many=True, queryset=UploadedFile.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'tier', 'images']
