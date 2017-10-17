from django.contrib import admin


class GearAdmin(admin.ModelAdmin):
    # Make all the data about a certification be shown in the list display
    list_display = ("name", "department", "status", "checked_out_to", "due_date")

    # Choose which fields appear on the side as filters
    list_filter = ('status', "department")

    # Choose which fields can be searched for
    search_fields = ('name', 'rfid', "checked_out_to__first_name", "checked_out_to__last_name")
