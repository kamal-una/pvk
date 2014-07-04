from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from history.models import HistoricalRecords
import logging


# Create your models here.
class Facility(models.Model):
    name = models.CharField(max_length=100)
    seated = models.BooleanField()
    number_of_seats = models.BigIntegerField(null=True)
    created = models.DateField(auto_now_add=True)
    last_update = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.name


class FacilitySeat(models.Model):
    facility = models.ForeignKey(Facility)
    section = models.CharField(max_length=10)
    row = models.CharField(max_length=10)
    seat = models.IntegerField()

    def __unicode__(self):
        return self.section + " - " + self.row + " - " + str(self.seat)


class BuyerGroup(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class BuyerType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class BuyerGroupMapping(models.Model):
    buyer_type = models.ForeignKey(BuyerType)
    buyer_group = models.ForeignKey(BuyerGroup)

    def __unicode__(self):
        return "%s - %s" & str(self.buyer_group), str(self.buyer_type)


class EventRun(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
        return str(self.name)


class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
        return str(self.name)


class PaymentType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class PriceMatrix(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
        return str(self.name)


class PriceCategory(models.Model):
    name = models.CharField(max_length=100)
    facility = models.ForeignKey(Facility)

    def __unicode__(self):
        return "%s - %s" % (self.facility, self.name)


class Price(models.Model):
    matrix = models.ForeignKey(PriceMatrix, null=True)
    category = models.ForeignKey(PriceCategory, null=False)
    buyer_type = models.ForeignKey(BuyerType)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    enabled = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s - %s - %s " % (str(self.matrix), str(self.buyer_type), str(self.price))


class Event(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(EventCategory, null=True, blank=True)
    run = models.ForeignKey(EventRun, null=True, blank=True)
    facility = models.ForeignKey(Facility)
    price_matrix = models.ForeignKey(PriceMatrix, null=True)
    date = models.DateField()
    sale_start = models.DateTimeField(blank=True, null=True)
    sale_end = models.DateTimeField(blank=True, null=True)
    image_url = models.URLField(null=True)
    doors_open = models.DateTimeField(blank=True, null=True)
    product_id = models.IntegerField(null=True)
    min_tickets = models.IntegerField(null=True)
    max_tickets = models.IntegerField(null=True)
    information = models.TextField(null=True)

    def get_prices(self):
        prices = Price.objects.filter(matrix=self.price_matrix, 
                                      enabled=True)
        prices = sorted(prices, key=lambda mapping: [mapping.category.name,
                                                     mapping.buyer_type.name])
        return prices

    def lock_seats(self, transaction, buyer, price, number_of_seats=1):
        # find an available seat...
        available_seats = self.seat_set.filter(status=0)
        locked_seats = []
        pointer = 0
        while len(locked_seats) < number_of_seats:

            logging.info('looping through seats: %s', (pointer))
            try:
                seat = available_seats[pointer]
                logging.info('Got possible available seat: %s', (seat.id))

                key_seat = self.seat_set.get(id=seat.id)
                if key_seat.status == 0:
                    seat = seat.lock_seat(transaction, buyer, price)
                    locked_seats.append(seat.id)
                    logging.info('Seat sucessfully locked: %s', (seat.id))

                pointer += 1

            except:
                logging.info('Not enough seats available')
                # release any locked seats
                logging.info('Releasing locked seats...')
                for seat in locked_seats:
                    this_seat = Seat.objects.get(id=seat)
                    this_seat.unlock_seat(transaction)
                    logging.info('Release %s', (this_seat.id))
                return False

        return True

    def save(self, *args, **kwargs):
        # save the performance...
        if self.pk is None:
            do_seats = True
        else:
            do_seats = False

        super(Event, self).save(*args, **kwargs)

        # if new performance
        if do_seats:
            # a new transaction for creating these seats...
            new_transaction = Transaction()
            new_transaction.save()

            # create the seats...
            all_seats = FacilitySeat.objects.filter(facility__exact=self.facility)
            for new_seat in all_seats:
                new_seat_record = Seat(seat=new_seat, status=0, transaction=new_transaction, event=self, price=0)
                new_seat_record.save()

    def __unicode__(self):
        return str(self.name)


class EventBuyerMapping(models.Model):
    key = models.CharField(primary_key=True, default=None, editable=False, max_length=100)
    event = models.ForeignKey(Event)
    buyer_type = models.ForeignKey(BuyerType)

    def save(self):
        composite = "%s-%s" % (self.event, self.buyer_type)
        self.key = hash(composite)
        super(EventBuyerMapping, self).save()

    def __unicode__(self):
        return "%s - %s" % (self.buyer_type, self.event)


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    title = models.CharField(max_length=10, blank=True)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50, blank=True)
    address3 = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    post_code = models.CharField(max_length=50)
    home_number = models.CharField(max_length=15, blank=True)
    mobile_number = models.CharField(max_length=15, blank=True)

    dob = models.DateField(null=True, blank=True)
    last_update = models.DateField(auto_now=True)

    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])


class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.id)


class Seat(models.Model):
    AVAILABLE = 0
    LOCKED = 1
    UNPAID = 2
    CONSIGNED = 3
    PAID = 4
    PRINTED = 5
    STATUS_CHOICES = (
        (AVAILABLE, 'Available'),
        (LOCKED, 'Locked'),
        (UNPAID, 'Unpaid'),
        (CONSIGNED, 'Consigned'),
        (PAID, 'Paid'),
        (PRINTED, 'Printed'),
    )

    transaction = models.ForeignKey(Transaction)
    event = models.ForeignKey(Event)
    seat = models.ForeignKey(FacilitySeat, related_name='+')
    status = models.IntegerField(choices=STATUS_CHOICES, default=AVAILABLE)
    buyer_type = models.ForeignKey(BuyerType, null=True)
    payment_type = models.ForeignKey(PaymentType, null=True, blank=True)
    user = models.ForeignKey(CustomUser, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    payment_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    history = HistoricalRecords()

    def lock_seat(self, transaction, buyer, price):
        self.buyer_type = buyer
        self.price = price
        if self.status == Seat.AVAILABLE:
            self.update_seat(transaction, Seat.LOCKED)
            logging.info('locked seat: %s', (self.id))
            return self
        else:
            logging.error('Failed lock')
            return False
        

    def unlock_seat(self, transaction):
        self.buyer_type = None
        self.price = 0
        self.update_seat(transaction, Seat.AVAILABLE)

    def pay_seat(self, transaction, user):
        self.user = user
        self.update_seat(transaction, Seat.PAID)


    def update_seat(self, transaction, status):
        self.transaction = transaction
        self.status = status
        self.save()

    def __unicode__(self):
        return str(self.event) + " - " + str(self.transaction) + " - " + str(self.seat)

    class Meta:
        ordering = ['event', 'transaction', 'seat']
