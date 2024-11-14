from datetime import timedelta
from django.db import IntegrityError
from django.utils import timezone
from django.test import TestCase
from users.models import User
from users.serializers import UserSerializer
from django.db import models


class UserClass:
    def __init__(
        self,
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        user_fullname: str,
        is_superuser: bool,
        is_active: bool,
        password: str,
        last_login: str,
        date_joined: str,
    ) -> None:
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.user_fullname = user_fullname
        self.is_superuser = is_superuser
        self.is_active = is_active
        self.password = password
        self.last_login = last_login
        self.date_joined = date_joined


class TestUserModel(TestCase):
    def test_attrs(self):
        expected_attr_names = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "last_login",
            "date_joined",
            "reset_code",
            "reset_code_expires_at",
            "groups",
            "user_permissions",
        ]

        attr_names = []
        for attr in User._meta.get_fields():
            if isinstance(attr, models.Field):
                attr_names.append(attr.name)

        for name in expected_attr_names:
            self.assertIn(name, attr_names)

        self.assertEqual(len(expected_attr_names), len(attr_names))

    def test_name_attr(self):
        username_field = User._meta.get_field("username")
        self.assertIsInstance(username_field, models.CharField)
        self.assertEqual(username_field.max_length, 150)

        password_field = User._meta.get_field("password")
        self.assertIsInstance(password_field, models.CharField)
        self.assertEqual(password_field.max_length, 128)

        first_name_field = User._meta.get_field("first_name")
        self.assertIsInstance(first_name_field, models.CharField)
        self.assertEqual(first_name_field.max_length, 150)
        self.assertEqual(first_name_field.blank, True)

        last_name_field = User._meta.get_field("last_name")
        self.assertIsInstance(last_name_field, models.CharField)
        self.assertEqual(last_name_field.max_length, 150)
        self.assertEqual(last_name_field.blank, True)

        email_field = User._meta.get_field("email")
        self.assertIsInstance(email_field, models.EmailField)
        self.assertEqual(email_field.max_length, 254)

        last_login_field = User._meta.get_field("last_login")
        self.assertIsInstance(last_login_field, models.DateTimeField)
        self.assertEqual(last_login_field.blank, True)
        self.assertEqual(last_login_field.null, True)

        reset_code_field = User._meta.get_field("reset_code")
        self.assertIsInstance(reset_code_field, models.CharField)
        self.assertEqual(reset_code_field.max_length, 6)
        self.assertEqual(reset_code_field.blank, True)
        self.assertEqual(reset_code_field.null, True)

        reset_code_expires_at_field = User._meta.get_field(
            "reset_code_expires_at"
        )
        self.assertIsInstance(
            reset_code_expires_at_field, models.DateTimeField
        )
        self.assertEqual(reset_code_expires_at_field.blank, True)
        self.assertEqual(reset_code_expires_at_field.null, True)

        is_staff_field = User._meta.get_field("is_staff")
        self.assertIsInstance(is_staff_field, models.BooleanField)
        self.assertEqual(is_staff_field.default, False)

        is_active_field = User._meta.get_field("is_active")
        self.assertIsInstance(is_active_field, models.BooleanField)
        self.assertEqual(is_active_field.default, True)

        date_joined_field = User._meta.get_field("date_joined")
        self.assertIsInstance(date_joined_field, models.DateTimeField)
        self.assertEqual(date_joined_field.default, timezone.now)


class TestUser(TestCase):
    def setUp(self) -> User:
        self.user_create = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="12345678",
            first_name="Test",
            last_name="User",
        )

    def test_user_instance_attrs(self):
        user = UserClass(
            "testuser",
            "test@example.com",
            "Test",
            "User",
            "test test",
            False,
            True,
            "12345678",
            "2024-11-11T15:30:00",
            "2023-06-25T08:45:00",
        )
        self.assertEqual(type(user.username), str)
        self.assertEqual(type(user.email), str)
        self.assertEqual(type(user.first_name), str)
        self.assertEqual(type(user.last_name), str)
        self.assertEqual(type(user.user_fullname), str)
        self.assertEqual(type(user.is_superuser), bool)
        self.assertEqual(type(user.is_active), bool)
        self.assertEqual(type(user.password), str)
        self.assertEqual(type(user.last_login), str)
        self.assertEqual(type(user.date_joined), str)

    def test_unique_username(self):
        User.objects.create_user(
            username="uniqueuser",
            email="unique@example.com",
            password="12345678",
        )
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="uniqueuser",
                email="otherunique@example.com",
                password="12345678",
            )

    def test_unique_email(self):
        User.objects.create_user(
            username="uniqueuser",
            email="unique@example.com",
            password="12345678",
        )
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="otheruniqueuser",
                email="unique@example.com",
                password="12345678",
            )

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            username="superuser",
            email="super@example.com",
            password="12345678",
        )

        self.assertTrue(user.is_superuser)

    def test_user_fullname(self):
        user = self.user_create
        serializer = UserSerializer(user)

        self.assertEqual(
            serializer.get_user_fullname(user),
            f"{user.first_name} {user.last_name}",
        )

    def test_user_serializer(self):
        user = self.user_create

        serializer = UserSerializer(user)
        data = serializer.data

        self.assertEqual(data["user_fullname"], "Test User")
        self.assertEqual(data["username"], "testuser")
        self.assertEqual(data["email"], "test@example.com")
        self.assertEqual(data["first_name"], "Test")
        self.assertEqual(data["last_name"], "User")

    def test_generate_reset_code(self):
        user = self.user_create
        reset_code = user.generate_reset_code()

        self.assertIsNotNone(user.reset_code)
        self.assertEqual(len(user.reset_code), 6)
        self.assertEqual(user.reset_code, reset_code)
        self.assertTrue(user.reset_code_expires_at > timezone.now())

    def test_is_reset_code_valid(self):
        user = self.user_create
        reset_code = user.generate_reset_code()

        self.assertTrue(user.is_reset_code_valid(reset_code))
        self.assertFalse(user.is_reset_code_valid("WRONGCODE"))

        user.reset_code_expires_at = timezone.now() - timedelta(minutes=1)
        user.save()
        self.assertFalse(user.is_reset_code_valid(reset_code))
