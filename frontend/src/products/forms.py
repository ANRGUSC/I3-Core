from django import forms

from django.utils.text import slugify

from .models import Product

PUBLISH_CHOICES = (
    # ('', ""),
    ('publish', "Publish"),
    ('draft', "Draft"),
)

SENSOR_CHOICES = (('1', 'Sensor',), ('2', 'Actuactor',), ('3', 'Both'))
HUB_CHOICES = [['1','1'],['2','2'],['3','3']]
         
class ProductModelForm(forms.ModelForm):

    #hub = forms.ChoiceField(choices=HUB_CHOICES, required=True)
    
    class Meta:
        model = Product
        fields = [
            "title",
            "description",
            "price",
            "sale_price",
            "sale_active",
            "media",
            'restricted_active',
            'sensor_type',
            'hub',
            'longitude',
            'latitude',
        ]
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "placeholder": "New Description",
                    "class": "form-control"
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Topic",
                    "class": "form-control"
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "min": 0.0,
                    "class": "form-control"
                }
            ),
            "sale_price": forms.NumberInput(
                attrs={
                    "min": 0.0,
                    "class": "form-control"
                }
            ),
            "media": forms.FileInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "hub": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "longitude": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "latitude": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),
        }

    def clean(self, *args, **kwargs):
        cleaned_data = super(ProductModelForm, self).clean(*args, **kwargs)
        # title = cleaned_data.get("title")
        # slug = slugify(title)
        # qs = Product.objects.filter(slug=slug).exists()
        # if qs:
        # 	raise forms.ValidationError("Title is taken, new title is needed. Please try again.")
        return cleaned_data

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 1.00:
            raise forms.ValidationError("Price must be greater than $1.00")
        elif price >= 100.00:
            raise forms.ValidationError("Price must be less than $100.00")
        else:
            return price

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) > 3:
            return title
        else:
            raise forms.ValidationError("Title must be greater than 3 characters long.")

    def clean_longitude(self):
        longitude = self.cleaned_data.get("longitude")
        if longitude is None:
            return longitude
        if (longitude < -180.0000 or longitude > 180.0000):
            raise forms.ValidationError("Longitude must be between -180 and 180")
        return longitude
        
    def clean_latitude(self):
        latitude = self.cleaned_data.get("latitude")
        if latitude is None:
            return latitude
        if (latitude < -90.0000 or latitude > 90.0000):
            raise forms.ValidationError("Longitude must be between -180 and 180")
        return latitude
