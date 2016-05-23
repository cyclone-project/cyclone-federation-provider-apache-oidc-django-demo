from __future__ import unicode_literals

from django.contrib.auth.middleware import RemoteUserMiddleware, PersistentRemoteUserMiddleware
from django.contrib.auth.models import Group, User, PermissionsMixin, UserManager
from django.core.mail import send_mail
from django.db import models
from django.core import validators

# Create your models here.
from django.db.models.signals import post_save
from django.utils import timezone
from django.contrib.auth import get_user_model

from mysite import settings


class CustomHeaderMiddleware(RemoteUserMiddleware):
    # header = 'OIDC_CLAIM_eduPersonPrincipalName'
    header = 'OIDC_CLAIM_email'
    force_logout_if_no_header = False


def post_save_receiver(sender, instance, created, **kwargs):
    if created:
        if len(get_user_model().objects.all()) is 1:
            # The first user to connect to the site is super_user
            instance.is_staff = True
            instance.is_superuser = True
            instance.save()
        else:
            # if not instance.is_staff:
            g = Group.objects.get_or_create(name="Users not requesting account")[0]
            g.user_set.add(instance)
            g.save()
            instance.is_active = False
            instance.save()
            # instance.groups.add(Group.objects.get_or_create(name="New users to validate"))
    pass


post_save.connect(post_save_receiver, sender=getattr(settings, 'AUTH_USER_MODEL', User))

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')

        extra_fields.setdefault('first_name', 'John')
        extra_fields.setdefault('last_name', 'Doe')
        extra_fields.setdefault('email', email)

        email = self.normalize_email(email)
        user = self.model(username=username,
                          # email=extra_fields.get('email'),
                          # first_name=extra_fields.get('first_name'),
                          # last_name=extra_fields.get('last_name'),
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        print username, extra_fields
        extra_fields.setdefault('first_name', 'Jane')
        extra_fields.setdefault('last_name', 'Doe')
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        blank=True,
    )
    # date_of_birth = models.DateField()
    # is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    username = models.CharField(
        _('username'),
        max_length=255,
        unique=True,
        help_text=_('Required. 255 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid username. This value may contain only '
                  'letters, numbers ' 'and @/./+/-/_ characters.')
            ),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=63, blank=True)
    last_name = models.CharField(_('last name'), max_length=63, blank=True)
    city = models.CharField(
        _('city'),
        max_length=255,
        help_text=_('The city of your professional address.'),
        blank=True)
    affiliation = models.CharField(
        _('affiliation'),
        max_length=255,
        help_text=_('The institution(s) you belong to.'),
        blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    # is_superuser = models.BooleanField(
    #    _('superuser status'),
    #    default=False,
    #    help_text=_(
    #        'Designates that this user has all permissions without '
    #        'explicitly assigning them.'
    #    ),
    # )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

        # @property
        # def is_staff(self):
        #    "Is the user a member of staff?"
        #    # Simplest possible answer: All admins are staff
        #    return self.is_staff
