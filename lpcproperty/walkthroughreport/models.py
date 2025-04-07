

# from django.db import models

# # === CATEGORY CONSTANTS ===
# K = 'K'   # Kitchen
# BA = 'BA' # Bathroom
# B = 'B'   # Bedroom

# # === MCQ OPTIONS ===
# MCQ_CHOICES = [
#     ('na', 'N/A'),
#     ('compliant', 'Compliant'),
#     ('heads_up', 'Heads-Up'),
#     ('non_compliant', 'Non-Compliant'),
# ]

# # === Custom Field with Category Tag ===
# class CategoryCharField(models.CharField):
#     def __init__(self, *args, category=None, **kwargs):
#         self.category = category
#         super().__init__(*args, **kwargs)

# # === Main Model ===
# class InspectionReport(models.Model):
#     inspector_name = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)

#     # Kitchen Questions
#     kitchen_counter_clean = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=K,verbose_name="Is the kitchen clean ?")
#     kitchen_counter_clean_remarks = models.TextField(blank=True, null=True)

#     kitchen_appliances_working = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=K)
#     kitchen_appliances_working_remarks = models.TextField(blank=True, null=True)

#     kitchen_floor_clean = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=K)
#     kitchen_floor_clean_remarks = models.TextField(blank=True, null=True)

#     # Bedroom Questions
#     bedroom_bed_made = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=B)
#     bedroom_bed_made_remarks = models.TextField(blank=True, null=True)

#     bedroom_lights_functional = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=B)
#     bedroom_lights_functional_remarks = models.TextField(blank=True, null=True)

#     bedroom_clean_floor = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=B)
#     bedroom_clean_floor_remarks = models.TextField(blank=True, null=True)

#     # Bathroom Questions
#     bathroom_sink_clean = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=BA)
#     bathroom_sink_clean_remarks = models.TextField(blank=True, null=True)

#     bathroom_toilet_sanitized = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=BA)
#     bathroom_toilet_sanitized_remarks = models.TextField(blank=True, null=True)

#     bathroom_floor_dry = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=BA,verbose_name="Is the bathroom floor dry?")
#     bathroom_floor_dry_remarks = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.inspector_name} ({self.created_at.date()})"

#     def get_fields_by_category(self, category_code):
#         return [
#             (field.name, getattr(self, field.name))
#             for field in self._meta.fields
#             if hasattr(field, 'category') and field.category == category_code
#         ]


# Starting of walkthrough Report Here ------------------------------------------------------------------------
from django.db import models
from mainapp.models import Client, Vendor  # Import from mainapp

from django.db import models

# Assuming this is defined somewhere in your code
MCQ_CHOICES = [
    ("N/A", "N/A"),
    ("Compliant", "Compliant"),
    ("Heads-Up", "Heads-Up"),
    ("Non-Compliant", "Non-Compliant"),
]

GIE = "General Items - Exterior"
GII = "General Items - Interior"
GARAGE = "Garage"
LAUNDRY = "Laundry / Mudroom"
KITCHEN = "Kitchen"
BUTLERS = "Butlers"
BREAKFAST_AREA = "Breakfast Area"
ENTRY_FOYER = "Entry / Foyer"
GREAT_ROOM = "Great Room / Family Room"
DINING_ROOM = "Dining Room / Area"
CLOSETS_MAIN_LEVEL = "Closets - Main Level"
CLOSETS_UPPER_LEVEL = "Closets - Upper Level"
HALLWAYS_MAIN_LEVEL = "Hallways - Main Level"
HALLWAYS_UPPER_LEVEL = "Hallways - Upper Level"
BEDROOM1 = "Bedroom 1 (Master Bedroom)"
BEDROOM2 = "Bedroom 2"
BEDROOM3 = "Bedroom 3"
BEDROOM4 = "Bedroom 4"
BATHROOM1 = "Bathroom 1 (Master Bath)"
BATHROOM2 = "Bathroom 2"
BATHROOM3 = "Bathroom 3"
BATHROOM4 = "Bathroom 4"
BATHROOM5 = "Bathroom 5"
GYM = "Gym"
THEATRE_MUSIC_ROOM = "Theatre / Music Room"
GUEST_HOUSE_SLEEPING_LIVING = "Guest House - Sleeping / Living"
GUEST_HOUSE_BATHROOM = "Guest House - Bathroom"

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Open', 'Open'),
    ('Completed', 'Completed'),
    ('Denied', 'Denied'),
]

# Dummy custom field if needed
class CategoryCharField(models.CharField):
    def __init__(self, *args, category=None, **kwargs):
        self.category = category
        super().__init__(*args, **kwargs)

class WalkthroughReport(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)  # Use Client from mainapp
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=200,blank=True, null=True, )
    updatedate = models.DateField(blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    cost = models.IntegerField(default=0,blank=True, null=True,)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    client_approval = models.BooleanField(default=False)  # Yes/No approval field
    gie1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="Visual Inspection: Exterior of House")
    gie1_remarks = models.CharField(max_length=500, blank=True, null=True)
    gie2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="Drives / Walkways")
    gie2_remarks = models.CharField(max_length=500, blank=True, null=True)
    gie3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="Generator: Reading Operational")
    gie3_remarks = models.CharField(max_length=500, blank=True, null=True)
    gie4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="Irrigation: Zones & Heads Tested")
    gie4_remarks = models.TextField(blank=True, null=True)
    gie5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="Propane Tank Meter Read")
    gie5_remarks = models.TextField(blank=True, null=True)
    gie6 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="A/C Air Handling Unit #1")
    gie6_remarks = models.TextField(blank=True, null=True)
    gie7 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="A/C Air Handling Unit #2")
    gie7_remarks = models.TextField(blank=True, null=True)
    gie8 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="A/C Air Handling Unit #3")
    gie8_remarks = models.TextField(blank=True, null=True)
    gie9 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="A/C Air Handling Unit #4")
    gie9_remarks = models.TextField(blank=True, null=True)
    gie10 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="A/C Air Handling Unit #5")
    gie10_remarks = models.TextField(blank=True, null=True)
    gie11 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="Mail / Newspapers / Notifications")
    gie11_remarks = models.TextField(blank=True, null=True)
    gie12 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="Outdoor Furniture")
    gie12_remarks = models.TextField(blank=True, null=True)
    gie13 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="Roof Eaves, Fascias, Gutters")
    gie13_remarks = models.TextField(blank=True, null=True)
    gie14 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="Exterior Lights (Sconces, Flood)")
    gie14_remarks = models.TextField(blank=True, null=True)
    gie15 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="Mailbox")
    gie15_remarks = models.TextField(blank=True, null=True)

    gii1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GII, verbose_name="Visual Inspection: Interior of House")
    gii1_remarks = models.TextField(blank=True, null=True)
    gii2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GII, verbose_name="Exterior Doors Codes")
    gii2_remarks = models.TextField(blank=True, null=True)
    gii3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GII, verbose_name="Exterior Doors & Hardware")
    gii3_remarks = models.TextField(blank=True, null=True)
    gii4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GII, verbose_name="Exterior Windows & Hardware")
    gii4_remarks = models.TextField(blank=True, null=True)
    gii5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GII, verbose_name="Smoke Detectors")
    gii5_remarks = models.TextField(blank=True, null=True)
    gii6 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GII, verbose_name="A/C Air Handling Unit #1")
    gii6_remarks = models.TextField(blank=True, null=True)
    gii7 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GII, verbose_name="A/C Air Handling Unit #2")
    gii7_remarks = models.TextField(blank=True, null=True)
    gii8 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GII, verbose_name="A/C Air Handling Unit #3")
    gii8_remarks = models.TextField(blank=True, null=True)
    gii9 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GII, verbose_name="A/C Air Handling Unit #4")
    gii9_remarks = models.TextField(blank=True, null=True)
    # gii10 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GII, verbose_name="Some question for GII 10")
    # gii10_remarks = models.TextField(blank=True, null=True)

    # garage 
    garage1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Garage", verbose_name="Refrigerator: Make sure the fridge is running and cool inside")
    garage2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Garage", verbose_name="Freezer: Make sure freezer is cold and not frozen solid")
    garage3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Garage", verbose_name="Wine Refrigerator: Holding proper temperature")
    garage4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Garage", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    garage5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Garage", verbose_name="Sinks: Run hot and cold water; Check underneath for signs of leaks")
    garage6 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Garage", verbose_name="Lights: Any burnt out requiring replacement?")
    garage7 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Garage", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    garage8 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Garage", verbose_name="Garage Doors & Operators: Hardware working properly")
    garage9 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Garage", verbose_name="Flooring: Acceptable")

    # laundry 
    laundry1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Laundry", verbose_name="Washer / Dryer: Any visual concerns")
    laundry2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Laundry", verbose_name="Sink: Faucet leaking, drain acceptable, overall condition")
    laundry3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Laundry", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    laundry4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Laundry", verbose_name="Lights: Any burnt out requiring replacement?")
    laundry5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Laundry", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    laundry6 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Laundry", verbose_name="Doors: Hardware working properly")

    # kitchen
    kitchen1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Kitchen", verbose_name="Refrigerator: Make sure the fridge is running and cool inside")
    kitchen2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Kitchen", verbose_name="Freezer: Make sure freezer is cold and not frozen solid")
    kitchen3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Kitchen", verbose_name="Ice Maker: Ice in bin, working properly")
    kitchen4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Kitchen", verbose_name="Wine Refrigerator: Holding proper temperature")
    kitchen5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Kitchen", verbose_name="Range: All burners working, oven works")
    kitchen6 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Kitchen", verbose_name="Microwave: Working properly")
    kitchen7 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Kitchen", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    kitchen8 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Kitchen", verbose_name="Dishwasher: Run dishwasher monthly")
    kitchen9 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Kitchen", verbose_name="Sinks: Run hot and cold water; Check underneath for signs of leaks")
    kitchen10 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Kitchen", verbose_name="Lights: Any burnt out requiring replacement?")
    kitchen11 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Kitchen", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    kitchen12 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Kitchen", verbose_name="Doors: Hardware working properly")

    # 6. Butlers Pantry
    butlers1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Butlers", verbose_name="Refrigerator: Make sure the fridge is running and cool inside")
    butlers2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Butlers", verbose_name="Freezer: Make sure freezer is cold and not frozen solid")
    butlers3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Butlers", verbose_name="Ice Maker: Ice in bin, working properly")
    butlers4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Butlers", verbose_name="Wine Refrigerator: Holding proper temperature")
    butlers5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Butlers", verbose_name="Range: All burners working, oven works")
    butlers6 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Butlers", verbose_name="Microwave: Working properly")
    butlers7 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Butlers", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    butlers8 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Butlers", verbose_name="Dishwasher: Run dishwasher monthly")
    butlers9 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Butlers", verbose_name="Sinks: Run hot and cold water; Check underneath for signs of leaks")
    butlers10 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Butlers", verbose_name="Lights: Any burnt out requiring replacement?")
    butlers11 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Butlers", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    butlers12 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Butlers", verbose_name="Doors: Hardware working properly")

    # Breakfast Area 
    breakfast1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Breakfast Area", verbose_name="Lights: Any burnt out requiring replacement?")
    breakfast2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Breakfast Area", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    breakfast3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Breakfast Area", verbose_name="Doors: Hardware working properly")
    breakfast4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Breakfast Area", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    breakfast5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Breakfast Area", verbose_name="Furniture: Note any damage")

    # 8. Entry / Foyer
    entry1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Entry / Foyer", verbose_name="Lights: Any burnt out requiring replacement?")
    entry2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Entry / Foyer", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    entry3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Entry / Foyer", verbose_name="Doors: Hardware working properly")
    entry4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Entry / Foyer", verbose_name="Furniture: Note any damage")

    # 9. Great Room / Family Room
    greatroom1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Great Room / Family Room", verbose_name="Lights: Any burnt out requiring replacement?")
    greatroom2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Great Room / Family Room", verbose_name="Floors / Walls / Ceilings: Visual check of floors/walls/ceilings")
    greatroom3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Great Room / Family Room", verbose_name="Doors: Hardware working properly")
    greatroom4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Great Room / Family Room", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    greatroom5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Great Room / Family Room", verbose_name="Furniture: Note any damage")

    # 10. Dining Room / Area
    dining1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Dining Room / Area", verbose_name="Lights: Any burnt out requiring replacement?")
    dining2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Dining Room / Area", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    dining3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Dining Room / Area", verbose_name="Doors: Hardware working properly")
    dining4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Dining Room / Area", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    dining5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Dining Room / Area", verbose_name="Furniture: Note any damage")

    # 11. Closets - Main Level
    closets1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Closets - Main Level", verbose_name="Lights: Any burnt out requiring replacement?")
    closets2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Closets - Main Level", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    closets3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Closets - Main Level", verbose_name="Doors: Hardware working properly")
    closets4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Closets - Main Level", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    closets5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Closets - Main Level", verbose_name="Furniture: Note any damage")

    # 12. Closets - Upper Level
    closets_upper1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Closets - Upper Level", verbose_name="Lights: Any burnt out requiring replacement?")
    closets_upper2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Closets - Upper Level", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    closets_upper3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Closets - Upper Level", verbose_name="Doors: Hardware working properly")
    closets_upper4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Closets - Upper Level", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    closets_upper5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Closets - Upper Level", verbose_name="Furniture: Note any damage")

    # 13. Hallways - Main Level
    hallways_main1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Hallways - Main Level", verbose_name="Lights: Any burnt out requiring replacement?")
    hallways_main2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Hallways - Main Level", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    hallways_main3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Hallways - Main Level", verbose_name="Doors: Hardware working properly")
    hallways_main4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Hallways - Main Level", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    hallways_main5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Hallways - Main Level", verbose_name="Furniture: Note any damage")

    # 13. Hallways - Upper Level
    hallways_upper1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Hallways - Upper Level", verbose_name="Lights: Any burnt out requiring replacement?")
    hallways_upper2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Hallways - Upper Level", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    hallways_upper3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Hallways - Upper Level", verbose_name="Doors: Hardware working properly")
    hallways_upper4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Hallways - Upper Level", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    hallways_upper5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Hallways - Upper Level", verbose_name="Furniture: Note any damage")


    # Bedroom 1 ( masterbedroom )
    bedroom1_1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 1 (Master Bedroom)", verbose_name="Furniture: Note any damage")
    bedroom1_2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 1 (Master Bedroom)", verbose_name="Lights: Any burnt out requiring replacement?")
    bedroom1_3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 1 (Master Bedroom)", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    bedroom1_4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 1 (Master Bedroom)", verbose_name="Doors: Hardware working properly")


    # Bedroom 2 
    bedroom2_1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 2", verbose_name="Furniture: Note any damage")
    bedroom2_2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 2", verbose_name="Lights: Any burnt out requiring replacement?")
    bedroom2_3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 2", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    bedroom2_4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 2", verbose_name="Doors: Hardware working properly")

    # Bedroom 3
    bedroom3_1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 3", verbose_name="Furniture: Note any damage")
    bedroom3_2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 3", verbose_name="Lights: Any burnt out requiring replacement?")
    bedroom3_3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 3", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    bedroom3_4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 3", verbose_name="Doors: Hardware working properly")

    # Bedroom 4
    bedroom4_1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 4", verbose_name="Furniture: Note any damage")
    bedroom4_2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 4", verbose_name="Lights: Any burnt out requiring replacement?")
    bedroom4_3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 4", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    bedroom4_4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 4", verbose_name="Doors: Hardware working properly")

    # Bathroom 1
    bathroom1_1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 1 (Master Bath)", verbose_name="Sinks: Faucet leaking, drain acceptable, overall condition")
    bathroom1_2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 1 (Master Bath)", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    bathroom1_3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 1 (Master Bath)", verbose_name="Shower: Faucet leaking, drain acceptable, overall condition")
    bathroom1_4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 1 (Master Bath)", verbose_name="Bath/Hot Tub: Faucet leaking, drain acceptable, overall condition")
    bathroom1_5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 1 (Master Bath)", verbose_name="Toilet: Tank refills properly, Handle operational")
    bathroom1_6 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 1 (Master Bath)", verbose_name="Lights: Any burnt out requiring replacement?")
    bathroom1_7 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 1 (Master Bath)", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    bathroom1_8 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 1 (Master Bath)", verbose_name="Doors: Hardware working properly")

    # Barhroom 2 
    bathroom2_1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 2 (Secondary Bath)", verbose_name="Sinks: Faucet leaking, drain acceptable, overall condition")
    bathroom2_2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 2 (Secondary Bath)", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    bathroom2_3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 2 (Secondary Bath)", verbose_name="Shower: Faucet leaking, drain acceptable, overall condition")
    bathroom2_4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 2 (Secondary Bath)", verbose_name="Bath/Hot Tub: Faucet leaking, drain acceptable, overall condition")
    bathroom2_5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 2 (Secondary Bath)", verbose_name="Toilet: Tank refills properly, Handle operational")
    bathroom2_6 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 2 (Secondary Bath)", verbose_name="Lights: Any burnt out requiring replacement?")
    bathroom2_7 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 2 (Secondary Bath)", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    bathroom2_8 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 2 (Secondary Bath)", verbose_name="Doors: Hardware working properly")


    # Bathroom 3 
    bathroom3_1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 3 (Guest Bath)", verbose_name="Sinks: Faucet leaking, drain acceptable, overall condition")
    bathroom3_2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 3 (Guest Bath)", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    bathroom3_3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 3 (Guest Bath)", verbose_name="Shower: Faucet leaking, drain acceptable, overall condition")
    bathroom3_4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 3 (Guest Bath)", verbose_name="Bath/Hot Tub: Faucet leaking, drain acceptable, overall condition")
    bathroom3_5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 3 (Guest Bath)", verbose_name="Toilet: Tank refills properly, Handle operational")
    bathroom3_6 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 3 (Guest Bath)", verbose_name="Lights: Any burnt out requiring replacement?")
    bathroom3_7 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 3 (Guest Bath)", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    bathroom3_8 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 3 (Guest Bath)", verbose_name="Doors: Hardware working properly")

    # Barhroom 4
    bathroom4_1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 4 (Powder Room)", verbose_name="Sinks: Faucet leaking, drain acceptable, overall condition")
    bathroom4_2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 4 (Powder Room)", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    bathroom4_3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 4 (Powder Room)", verbose_name="Shower: Faucet leaking, drain acceptable, overall condition")
    bathroom4_4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 4 (Powder Room)", verbose_name="Bath/Hot Tub: Faucet leaking, drain acceptable, overall condition")
    bathroom4_5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 4 (Powder Room)", verbose_name="Toilet: Tank refills properly, Handle operational")
    bathroom4_6 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 4 (Powder Room)", verbose_name="Lights: Any burnt out requiring replacement?")
    bathroom4_7 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 4 (Powder Room)", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    bathroom4_8 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 4 (Powder Room)", verbose_name="Doors: Hardware working properly")

    # Gym 
    gym_1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Gym", verbose_name="Sinks: Faucet leaking, drain acceptable, overall condition")
    gym_2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Gym", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    gym_3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Gym", verbose_name="Shower: Faucet leaking, drain acceptable, overall condition")
    gym_4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Gym", verbose_name="Toilet: Tank refills properly, Handle operational")
    gym_5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Gym", verbose_name="Lights: Any burnt out requiring replacement?")
    gym_6 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Gym", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    gym_7 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Gym", verbose_name="Doors: Hardware working properly")

    # Theater 
    theatre_1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Theatre / Music Room", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    theatre_2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Theatre / Music Room", verbose_name="Lights: Any burnt out requiring replacement?")
    theatre_3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Theatre / Music Room", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    theatre_4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Theatre / Music Room", verbose_name="Doors: Hardware working properly")
    theatre_5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Theatre / Music Room", verbose_name="Furniture: Note any damage")

    # Guest House 
    guest_house_1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Sleeping / Living", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    guest_house_2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Sleeping / Living", verbose_name="Doors: Hardware working properly")
    guest_house_3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Sleeping / Living", verbose_name="Furniture: Note any damage")
    guest_house_4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Sleeping / Living", verbose_name="Lights: Any burnt out requiring replacement?")
    guest_house_5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Sleeping / Living", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")

    # Guest House Bathrooms
    guest_house_bath_1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Bathroom", verbose_name="Sinks: Faucet leaking, drain acceptable, overall condition")
    guest_house_bath_2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Bathroom", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    guest_house_bath_3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Bathroom", verbose_name="Shower: Faucet leaking, drain acceptable, overall condition")
    guest_house_bath_4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Bathroom", verbose_name="Bath/Hot Tub: Faucet leaking, drain acceptable, overall condition")
    guest_house_bath_5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Bathroom", verbose_name="Toilet: Tank refills properly, Handle operational")
    guest_house_bath_6 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Bathroom", verbose_name="Lights: Any burnt out requiring replacement?")
    guest_house_bath_7 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Bathroom", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    guest_house_bath_8 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Bathroom", verbose_name="Doors: Hardware working properly")
