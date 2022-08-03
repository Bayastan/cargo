from django.db import models
from django.core.validators import MinValueValidator

from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Customer(models.Model):
    name = models.CharField(
        max_length=70,
        verbose_name='Имя',
    )
    surname = PhoneNumberField(
        max_length=70,
        verbose_name='Фамилия',
    )
    telephone_number = PhoneNumberField(
        verbose_name='Номер телефона',
        unique=True
    )
    passport = models.CharField(
        max_length=25,
        verbose_name='Номер пасспорта',
        unique=True
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания записи'
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления записи'
    )
    
    def _str_(self):
        return f'{self.surname} {self.name}'
    
    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        self.surname = self.surname.capitalize()
        
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('-created_date', )
        

class Cargo(models.Model):
    length = models.DecimalField(
        validators=[
            MinValueValidator(0)
        ],
        max_digits=12,
        decimal_places=2,
        verbose_name='Длинна груза',
        help_text='М'
    )
    width = models.DecimalField(
        validators=[
            MinValueValidator(0)
        ],
        max_digits=12,
        decimal_places=2,
        verbose_name='Ширина груза',
        help_text='М'
    )
    height = models.DecimalField(
        validators=[
            MinValueValidator(0)
        ],
        max_digits=12,
        decimal_places=2,
        verbose_name='Высота груза',
        help_text='М'
    )
    weight = models.DecimalField(
        validators=[
            MinValueValidator(0)
        ],
        max_digits=12,
        decimal_places=2,
        verbose_name='Вес',
        help_text='КГ'
    )
    volume = models.DecimalField(
        validators=[
            MinValueValidator(0)
        ],
        max_digits=12,
        decimal_places=3,
        verbose_name='Объем',
        help_text='Куб. м',
        blank=True
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        verbose_name='Категория',
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания записи'
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления записи'
    )
    
    
    def _str_(self):
        return f'Груз № {self.id}'
    
    def save(self, *args, **kwargs):
        self.volume = self.height * self.length * self.width
        
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Груз'
        verbose_name_plural = 'Грузы'
        ordering = ('-created_date', )
 

class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название категории'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания записи'
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления записи'
    )
    
    def _str_(self):
        return str(self.name)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('-created_date', )
    
       
class Truck(models.Model):
    truck_number = models.CharField(
        max_length=25,
        verbose_name='Гос номер'
    )
    weight = models.DecimalField(
        validators=[
            MinValueValidator(0)
        ],
        max_digits=25,
        decimal_places=3,
        verbose_name='Грузоподъемность',
        help_text='В тоннах'
    )
    volume = models.DecimalField(
        validators=[
            MinValueValidator(0)
        ],
        max_digits=25,
        decimal_places=3,
        verbose_name='Объем',
        help_text='Куб. м'
    )
    brend = models.CharField(
        max_length=25,
        verbose_name='Марка'
    )
    model = models.CharField(
        max_length=25,
        verbose_name='Модель'
    )
    vin_code = models.CharField(
        max_length=25,
        verbose_name='VIN код',
        unique=True
    )
    cargo_category = models.ManyToManyField(
        Category,
        verbose_name='Категория груза',
        related_name='truck_categories'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания записи'
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления записи'
    )
    
    def _str_(self):
        return f'{self.vin_code} | {self.truck_number}'
    
    class Meta:
        verbose_name = 'Грузовик'
        verbose_name_plural = 'Грузовики'
        ordering = ('-created_date', )
    
    
class Driver(models.Model):
    name = models.CharField(
        max_length=25,
        verbose_name='Имя'
    )
    surname = models.CharField(
        max_length=25,
        verbose_name='Фамилия'
    )
    telephone_number = PhoneNumberField(
        verbose_name='Номер телефона',
        unique=True
    )
    passport = models.CharField(
        max_length=25,
        verbose_name='Номер пасспорта',
        unique=True
    )
    driver_license = models.CharField(
        max_length=25,
        verbose_name='Номер прав',
        unique=True
    )
    cargo_category = models.ManyToManyField(
        Category,
        verbose_name='Категория груза',
        related_name='driver_categories'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания записи'
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления записи'
    )
    
    def _str_(self):
        return f'{self.name} {self.surname}'
    
    class Meta:
        verbose_name = 'Водитель'
        verbose_name_plural = 'Водители'
        ordering = ('-created_date', )
    
    
class Location(models.Model):
    city = models.CharField(
        max_length=25,
        verbose_name='Город'
    )
    country = models.CharField(
        max_length=25,
        verbose_name='Страна'
    )
    address = models.CharField(
        max_length=25,
        verbose_name='Адрес'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания записи'
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления записи'
    )
    
    def _str_(self):
        return f'{self.country} {self.city} {self.address}'
    
    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
        ordering = ('-created_date', )
        unique_together = ('country', 'city', 'address')
        
    
class Invoice(models.Model):
     
    customer = models.ForeignKey(
         Customer,
         on_delete=models.PROTECT
    )   
    cargo = models.ManyToManyField(
        Cargo,
        related_name='my_cargos',
        verbose_name='Мои грузы'
    )
    point_a = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name='invoice_loaction_a'
    )
    point_b = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name='invoice_loaction_b'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания записи'
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления записи'
    )
    
    def _str_(self):
        return f'Заявка № {self.id}'
    
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ('-created_date', )

    
class WayBill(models.Model):
    
    drivers = models.ForeignKey(
        Driver,
        on_delete=models.PROTECT
    )
    truck = models.ForeignKey(
        Truck,
        on_delete=models.PROTECT,
    )
    point_a = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name='waybill_loaction_a'
    )
    point_b = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name='waybill_loaction_b'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания записи'
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления записи'
    )
    
    def _str_(self):
        return f'Путевой лист № {self.id}'
    
    class Meta:
        verbose_name = 'Путевой лист'
        verbose_name_plural = 'Путевые листы'
        ordering = ('-created_date', )
    
    
class Order(models.Model):
    invoice = models.ManyToManyField(
        Invoice,
        verbose_name='Заказ',
        related_name='orders'
    )
    way_bill = models.OneToOneField(
        WayBill,
        on_delete=models.PROTECT,
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания записи'
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления записи'
    )
    
    def _str_(self):
        return f'Заказ № {self.id}'
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-created_date', )