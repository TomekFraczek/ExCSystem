"""
Python script to easily add a custom data field to a gear type in  safe way. This is initially experimental, but if it
works well, it should be added as a normal feature.
"""
from helper_scripts import setup_django
from django.core.exceptions import ObjectDoesNotExist
from core.models.GearModels import GearType, CustomDataField


def select_gear_type():

    print("Please type the name of the gear type you want to extend, type 'list' to see a list of all "
          "available gear, or 'exit' to exit.")
    choice = input("> ")

    if not choice:
        return select_gear_type()

    elif choice.lower() == 'list':
        all_types = GearType.objects.all()
        print("All available gear types:")
        for gt in all_types:
            print(f"{gt.name}: ")

    elif choice.lower() == 'exit':
        exit()

    else:
        try:
            this_type = GearType.objects.get(name=choice)
        except ObjectDoesNotExist:
            print(f"The gear type '{choice}' does not exist!")
            return select_gear_type()
        else:
            return this_type


def select_data_field():
    print("Please type the name of the custom data field you want to extend, type 'list' to see a list of all "
          "available data fields, or 'exit' to exit.")
    choice = input("> ")

    if not choice:
        return select_gear_type()

    elif choice.lower() == 'list':
        all_types = CustomDataField.objects.all()
        print("All available gear types:")
        for gt in all_types:
            print(f"{gt.name}: ")

    elif choice.lower() == 'exit':
        exit()

    else:
        try:
            this_field = CustomDataField.objects.get(name=choice)
        except ObjectDoesNotExist:
            print(f"The field '{choice}' does not exist!")
            return select_gear_type()
        else:
            return this_field


print("This will add an existing custom data field to an existing geartype. \n"
      "Please be careful as I cannot guarantee this will be reliable!")

gear_type = select_gear_type()

