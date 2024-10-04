import uuid
import os
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _


def hotel_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/hotel-image', filename)


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_field):
        if not email:
            raise ValueError('user most have an email address')

        user = self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        if not email:
            raise ValueError('user most have some email address')

        user = self.create_user(email, password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    birth_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'{self.f_name} {self.l_name}: {self.email}'


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    total_rooms = models.IntegerField(null=True, blank=True)
    available_rooms = models.IntegerField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, upload_to=hotel_image_path)

    def __str__(self):
        return self.name


class Room(models.Model):

    class RoomType(models.TextChoices):
        SINGLE = 'SI', _('Single')
        DOUBLE = 'DO', _('Double')
        SUITE = 'SU', _('Suite')

    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE)
    room_number = models.IntegerField()
    type = models.CharField(max_length=2, choices=RoomType.choices, default=RoomType.SINGLE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.room_number}\'th room in {self.hotel.__str__()} hotel'


class Reservation(models.Model):

    class ReservationStatus(models.TextChoices):
        PENDING = 'PE', _('Pending')
        CONFIRMED = 'CO', _('Confirmed')
        CANCELED = 'CA', _('Canceled')

    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='room', on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    status = models.CharField(max_length=2, choices=ReservationStatus.choices, default=ReservationStatus.PENDING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Reservation: {self.user.__str__()} -> {self.room.__str__()}'
