from django import forms
from .models import Room, Reservation


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'
