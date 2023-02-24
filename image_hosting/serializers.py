from rest_framework import serializers

from .models import UploadedFile, User, TempUrl


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


class FileSerializer(serializers.ModelSerializer):
    """
    Serializer of the Uploaded File model
    """
    created_by = serializers.ReadOnlyField(source='created_by.username')
    created_by_id = serializers.ReadOnlyField(source='created_by.id', required=False, default=None)

    class Meta:
        model = UploadedFile
        fields = ['id',
                  'created_by',
                  'created_by_id',
                  'name',
                  'file_format',
                  'date_started',
                  'last_edited'
                  ]


class FileBasicSerializer(FileSerializer):
    """
    Serializer of the Uploaded File model for users at the Basic tier
    """

    image_url = serializers.ImageField(required=True, write_only=True)
    image_thumbnail200 = serializers.ImageField(read_only=True)

    class Meta(FileSerializer.Meta):
        fields = FileSerializer.Meta.fields + ['image_url', 'image_thumbnail200',]


class FilePremiumSerializer(serializers.ModelSerializer):
    """
    Serializer of the Uploaded File model for the users in the Premium tier
    """

    image_url = serializers.ImageField(required=True)

    image_thumbnail200 = serializers.ImageField(read_only=True)
    image_thumbnail400 = serializers.ImageField(read_only=True)

    class Meta(FileSerializer.Meta):
        fields = FileSerializer.Meta.fields + ['image_url', 'image_thumbnail200', 'image_thumbnail400', ]


class FileEnterpriseSerializer(serializers.ModelSerializer):
    """
    Serializer of the Uploaded File model for the users in Enterprise tier
    """

    image_url = serializers.ImageField(required=True)

    image_thumbnail200 = serializers.ImageField(read_only=True)
    image_thumbnail400 = serializers.ImageField(read_only=True)

    class Meta(FileSerializer.Meta):
        fields = FileSerializer.Meta.fields + ['image_url', 'image_thumbnail200', 'image_thumbnail400', ]


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer of the customized User model
    """

    images = serializers.PrimaryKeyRelatedField(many=True, queryset=UploadedFile.objects.all())
    expiry_links = serializers.PrimaryKeyRelatedField(many=True, queryset=TempUrl.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'tier', 'images', 'expiry_links']


class TempUrlSerializer(serializers.ModelSerializer):
    """
    Serializer of the TempUrl model
    """

    token = serializers.CharField(write_only=True)
    temp_url = serializers.SerializerMethodField()

    class Meta:
        model = TempUrl
        fields = ['id',

                  'token',
                  'expiry_date',
                  'temp_url']

    def get_temp_url(self, obj):
        request = self.context.get('request')
        _link = f"{request.scheme}://{request.META['HTTP_HOST']}/exp/use/{obj.token}/"
        return _link
