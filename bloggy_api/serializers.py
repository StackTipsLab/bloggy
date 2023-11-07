from rest_framework import serializers

from bloggy.models import Post, User, Category, Quiz
from bloggy.models.comment import Comment
from bloggy.models.course import Course


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'article_count',
            'slug',
            'description',
            'color',
            'logo',
            'publish_status',
            'created_date',
            'updated_date',
        ]


class AuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')

    class Meta:
        model = User
        fields = (
            'name',
            'username',
            'profile_photo',
            'website',
            'twitter',
            'youtube',
            'github',
            'bio',
        )


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    profile_photo = serializers.ImageField()
    website = serializers.CharField()
    twitter = serializers.CharField()
    youtube = serializers.CharField()
    github = serializers.CharField()
    bio = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'username',
            'profile_photo',
            'website',
            'twitter',
            'youtube',
            'github',
            'bio',
        ]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'display_order',
            'slug',
            'excerpt',
            'description',
            'difficulty',
            'is_featured',
            'author',
            'thumbnail',
            'category',
            'published_date',
        ]


class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    author = AuthorSerializer(many=False, read_only=True)
    course = CourseSerializer(many=False, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'excerpt',
            'difficulty',
            'post_type',
            'template_type',
            'is_featured',
            'author',
            'thumbnail',
            'category',
            'display_order',
            'published_date',
            'course',
        ]


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False, required=False)
    reply_set = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'parent',
            'user',
            'comment_content',
            'comment_author_name',
            'comment_author_email',
            'comment_author_url',
            'comment_date',
            'active',
            'reply_set'
        ]


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = [
            'id',
            'title',
            'question_set',
            'excerpt',
            'content',
            'duration',
            'difficulty',
            'is_featured',
            'thumbnail',
            'category',
            'display_order',
            'updated_date',
            'published_date',
            'slug',
        ]
