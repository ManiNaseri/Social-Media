from rest_framework import serializers
from .models import Post , PostMedia, SavedPost
from .validators import MediaValidationMixin


class CreatePostSerializer(MediaValidationMixin,serializers.ModelSerializer):
    media_required = True
    media_files = serializers.ListField(child=serializers.FileField(),write_only=True,required=True)

    class Meta:
        model = Post
        fields = (
            "caption",
            "visibility",
            "comments_enabled",
            "media_files",
        )



class PostMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostMedia
        fields = (
            "id",
            "file",
            "media_type",
            "order",
        )


class PostSerializer(serializers.ModelSerializer):

    media = PostMediaSerializer(many=True,read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "caption",
            "visibility",
            "comments_enabled",
            "likes_count",
            "comments_count",
            "created_at",
            "media",
        )



class UpdatePostSerializer(MediaValidationMixin,serializers.Serializer):
    media_required = False

    caption = serializers.CharField(required=False,allow_blank=True)
    visibility = serializers.ChoiceField(choices=Post.VisibilityChoices.choices,required=False)
    media_files = serializers.ListField(child=serializers.FileField(),required=False,write_only=True)
    delete_media_ids = serializers.ListField(child=serializers.IntegerField(),required=False,write_only=True)
    
    def validate(self, attrs):

        if not attrs:
            raise serializers.ValidationError("No data provided.")

        return attrs


class ExploreSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = Post
        exclude = ["updated_at"]

class SavedPostSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source="post.owner.username", read_only=True)
    media = PostMediaSerializer(many=True,read_only=True, source="post.media")
    caption = serializers.CharField(source="post.caption", read_only=True)
    likes_count = serializers.IntegerField(source="post.likes_count", read_only=True)
    comments_count = serializers.IntegerField(source="post.comments_count", read_only=True)
    post_id = serializers.IntegerField(source="post.id", read_only=True)

    class Meta:
        model = SavedPost
        fields = ["post_id", "owner", "media", "caption", "likes_count", "comments_count"]

