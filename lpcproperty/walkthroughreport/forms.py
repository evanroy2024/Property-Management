from django import forms
from .models import (
    WalkthroughReport,
    GeneralItemsExterior,
    GeneralItemsInterior,
    Garage,
    Laundry,
    Kitchen,
    Butlers,
    BreakfastArea,
    EntryFoyer,
    GreatRoom,
    DiningRoom,
    ClosetsMainLevel,
    ClosetsUpperLevel,
    HallwaysMainLevel,
    HallwaysUpperLevel,
    Bedroom1, Bedroom2, Bedroom3, Bedroom4, Bedroom5,
    Bedroom6, Bedroom7, Bedroom8, Bedroom9, Bedroom10,
    Bathroom1, Bathroom2, Bathroom3, Bathroom4, Bathroom5,
    Bathroom6, Bathroom7, Bathroom8, Bathroom9, Bathroom10,
    Bathroom11, Bathroom12,
    Gym,
    TheatreMusicRoom,
    GuestHouseSleepingLiving,
    GuestHouseBathroom
)


class WalkthroughReportForm(forms.ModelForm):
    class Meta:
        model = WalkthroughReport
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].label_from_instance = lambda obj: f"{obj.last_name}, {obj.first_name}"
        self.fields['property'].label_from_instance = lambda obj: obj.address


class BaseRoomForm(forms.ModelForm):
    """Base form class that handles amount fields properly"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all amount fields not required and set default to 0
        for field_name, field in self.fields.items():
            if 'amount' in field_name:
                field.required = False
                if isinstance(field.widget, forms.NumberInput):
                    field.widget.attrs['min'] = 0
                    field.widget.attrs['value'] = 0


class GeneralItemsExteriorForm(BaseRoomForm):
    class Meta:
        model = GeneralItemsExterior
        exclude = ['walkthrough_report']


class GeneralItemsInteriorForm(BaseRoomForm):
    class Meta:
        model = GeneralItemsInterior
        exclude = ['walkthrough_report']


class GarageForm(BaseRoomForm):
    class Meta:
        model = Garage
        exclude = ['walkthrough_report']


class LaundryForm(BaseRoomForm):
    class Meta:
        model = Laundry
        exclude = ['walkthrough_report']


class KitchenForm(BaseRoomForm):
    class Meta:
        model = Kitchen
        exclude = ['walkthrough_report']


class ButlersForm(BaseRoomForm):
    class Meta:
        model = Butlers
        exclude = ['walkthrough_report']


class BreakfastAreaForm(BaseRoomForm):
    class Meta:
        model = BreakfastArea
        exclude = ['walkthrough_report']


class EntryFoyerForm(BaseRoomForm):
    class Meta:
        model = EntryFoyer
        exclude = ['walkthrough_report']


class GreatRoomForm(BaseRoomForm):
    class Meta:
        model = GreatRoom
        exclude = ['walkthrough_report']


class DiningRoomForm(BaseRoomForm):
    class Meta:
        model = DiningRoom
        exclude = ['walkthrough_report']


class ClosetsMainLevelForm(BaseRoomForm):
    class Meta:
        model = ClosetsMainLevel
        exclude = ['walkthrough_report']


class ClosetsUpperLevelForm(BaseRoomForm):
    class Meta:
        model = ClosetsUpperLevel
        exclude = ['walkthrough_report']


class HallwaysMainLevelForm(BaseRoomForm):
    class Meta:
        model = HallwaysMainLevel
        exclude = ['walkthrough_report']


class HallwaysUpperLevelForm(BaseRoomForm):
    class Meta:
        model = HallwaysUpperLevel
        exclude = ['walkthrough_report']


class GymForm(BaseRoomForm):
    class Meta:
        model = Gym
        exclude = ['walkthrough_report']


class TheatreMusicRoomForm(BaseRoomForm):
    class Meta:
        model = TheatreMusicRoom
        exclude = ['walkthrough_report']


class GuestHouseSleepingForm(BaseRoomForm):
    class Meta:
        model = GuestHouseSleepingLiving
        exclude = ['walkthrough_report']


class GuestHouseBathForm(BaseRoomForm):
    class Meta:
        model = GuestHouseBathroom
        exclude = ['walkthrough_report']


# Bedroom Forms
class Bedroom1Form(BaseRoomForm):
    class Meta:
        model = Bedroom1
        exclude = ['walkthrough_report']


class Bedroom2Form(BaseRoomForm):
    class Meta:
        model = Bedroom2
        exclude = ['walkthrough_report']


class Bedroom3Form(BaseRoomForm):
    class Meta:
        model = Bedroom3
        exclude = ['walkthrough_report']


class Bedroom4Form(BaseRoomForm):
    class Meta:
        model = Bedroom4
        exclude = ['walkthrough_report']


class Bedroom5Form(BaseRoomForm):
    class Meta:
        model = Bedroom5
        exclude = ['walkthrough_report']


class Bedroom6Form(BaseRoomForm):
    class Meta:
        model = Bedroom6
        exclude = ['walkthrough_report']


class Bedroom7Form(BaseRoomForm):
    class Meta:
        model = Bedroom7
        exclude = ['walkthrough_report']


class Bedroom8Form(BaseRoomForm):
    class Meta:
        model = Bedroom8
        exclude = ['walkthrough_report']


class Bedroom9Form(BaseRoomForm):
    class Meta:
        model = Bedroom9
        exclude = ['walkthrough_report']


class Bedroom10Form(BaseRoomForm):
    class Meta:
        model = Bedroom10
        exclude = ['walkthrough_report']


# Bathroom Forms
class Bathroom1Form(BaseRoomForm):
    class Meta:
        model = Bathroom1
        exclude = ['walkthrough_report']


class Bathroom2Form(BaseRoomForm):
    class Meta:
        model = Bathroom2
        exclude = ['walkthrough_report']


class Bathroom3Form(BaseRoomForm):
    class Meta:
        model = Bathroom3
        exclude = ['walkthrough_report']


class Bathroom4Form(BaseRoomForm):
    class Meta:
        model = Bathroom4
        exclude = ['walkthrough_report']


class Bathroom5Form(BaseRoomForm):
    class Meta:
        model = Bathroom5
        exclude = ['walkthrough_report']


class Bathroom6Form(BaseRoomForm):
    class Meta:
        model = Bathroom6
        exclude = ['walkthrough_report']


class Bathroom7Form(BaseRoomForm):
    class Meta:
        model = Bathroom7
        exclude = ['walkthrough_report']


class Bathroom8Form(BaseRoomForm):
    class Meta:
        model = Bathroom8
        exclude = ['walkthrough_report']


class Bathroom9Form(BaseRoomForm):
    class Meta:
        model = Bathroom9
        exclude = ['walkthrough_report']


class Bathroom10Form(BaseRoomForm):
    class Meta:
        model = Bathroom10
        exclude = ['walkthrough_report']


class Bathroom11Form(BaseRoomForm):
    class Meta:
        model = Bathroom11
        exclude = ['walkthrough_report']


class Bathroom12Form(BaseRoomForm):
    class Meta:
        model = Bathroom12
        exclude = ['walkthrough_report']