
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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending',blank=True, null=True)
    client_approval = models.BooleanField(default=False)  # Yes/No approval field
    gie1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="Visual Inspection: Exterior of House")
    gie1_remarks = models.CharField(max_length=500, blank=True, null=True)
    gie2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="Drives / Walkways")
    gie2_remarks = models.CharField(max_length=500, blank=True, null=True)
    gie3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="Generator: Reading Operational")
    gie3_remarks = models.CharField(max_length=500, blank=True, null=True)
    gie4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="Irrigation: Zones & Heads Tested")
    gie4_remarks = models.CharField(max_length=500, blank=True, null=True)
    gie5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="Propane Tank Meter Read")
    gie5_remarks = models.CharField(max_length=500, blank=True, null=True)
    gie6 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="A/C Air Handling Unit #1")
    gie6_remarks = models.CharField(max_length=500, blank=True, null=True)
    gie7 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="A/C Air Handling Unit #2")
    gie7_remarks = models.CharField(max_length=500, blank=True, null=True)
    gie8 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="A/C Air Handling Unit #3")
    gie8_remarks = models.CharField(max_length=500, blank=True, null=True)
    gie9 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="A/C Air Handling Unit #4")
    gie9_remarks = models.CharField(max_length=500, blank=True, null=True)
    gie10 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="A/C Air Handling Unit #5")
    gie10_remarks = models.CharField(max_length=500, blank=True, null=True)
    gie11 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="Mail / Newspapers / Notifications")
    gie11_remarks = models.CharField(max_length=500, blank=True, null=True)
    gie12 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="Outdoor Furniture")
    gie12_remarks = models.CharField(max_length=500, blank=True, null=True)
    gie13 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="Roof Eaves, Fascias, Gutters")
    gie13_remarks = models.CharField(max_length=500, blank=True, null=True)
    gie14 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="Exterior Lights (Sconces, Flood)")
    gie14_remarks = models.CharField(max_length=500, blank=True, null=True)
    gie15 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GIE, verbose_name="Mailbox")
    gie15_remarks = models.CharField(max_length=500, blank=True, null=True)

    gii1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GII, verbose_name="Visual Inspection: Interior of House")
    gii1_remarks = models.CharField(max_length=500, blank=True, null=True)
    gii2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GII, verbose_name="Exterior Doors Codes")
    gii2_remarks = models.CharField(max_length=500, blank=True, null=True)
    gii3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GII, verbose_name="Exterior Doors & Hardware")
    gii3_remarks = models.CharField(max_length=500, blank=True, null=True)
    gii4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GII, verbose_name="Exterior Windows & Hardware")
    gii4_remarks = models.CharField(max_length=500, blank=True, null=True)
    gii5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GII, verbose_name="Smoke Detectors")
    gii5_remarks = models.CharField(max_length=500, blank=True, null=True)
    gii6 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GII, verbose_name="A/C Air Handling Unit #1")
    gii6_remarks = models.CharField(max_length=500, blank=True, null=True)
    gii7 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GII, verbose_name="A/C Air Handling Unit #2")
    gii7_remarks = models.CharField(max_length=500, blank=True, null=True)
    gii8 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GII, verbose_name="A/C Air Handling Unit #3")
    gii8_remarks = models.CharField(max_length=500, blank=True, null=True)
    gii9 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GII, verbose_name="A/C Air Handling Unit #4")
    gii9_remarks = models.CharField(max_length=500, blank=True, null=True)
    # gii10 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category=GII, verbose_name="Some question for GII 10")
    # gii10_remarks = models.TextField(blank=True, null=True)

    # garage 
    garage1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Garage", verbose_name="Refrigerator: Make sure the fridge is running and cool inside")
    garage1_remarks = models.CharField(max_length=500, blank=True, null=True)
    garage2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Garage", verbose_name="Freezer: Make sure freezer is cold and not frozen solid")
    garage2_remarks = models.CharField(max_length=500, blank=True, null=True)
    garage3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Garage", verbose_name="Wine Refrigerator: Holding proper temperature")
    garage3_remarks = models.CharField(max_length=500, blank=True, null=True)
    garage4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Garage", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    garage4_remarks = models.CharField(max_length=500, blank=True, null=True)
    garage5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Garage", verbose_name="Sinks: Run hot and cold water; Check underneath for signs of leaks")
    garage5_remarks = models.CharField(max_length=500, blank=True, null=True)
    garage6 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Garage", verbose_name="Lights: Any burnt out requiring replacement?")
    garage6_remarks = models.CharField(max_length=500, blank=True, null=True)
    garage7 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Garage", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    garage7_remarks = models.CharField(max_length=500, blank=True, null=True)
    garage8 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Garage", verbose_name="Garage Doors & Operators: Hardware working properly")
    garage8_remarks = models.CharField(max_length=500, blank=True, null=True)
    garage9 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Garage", verbose_name="Flooring: Acceptable")
    garage9_remarks = models.CharField(max_length=500, blank=True, null=True)

    # laundry 
    laundry1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Laundry", verbose_name="Washer / Dryer: Any visual concerns")
    laundry1_remarks = models.CharField(max_length=500, blank=True, null=True)
    laundry2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Laundry", verbose_name="Sink: Faucet leaking, drain acceptable, overall condition")
    laundry2_remarks = models.CharField(max_length=500, blank=True, null=True)
    laundry3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Laundry", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    laundry3_remarks = models.CharField(max_length=500, blank=True, null=True)
    laundry4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Laundry", verbose_name="Lights: Any burnt out requiring replacement?")
    laundry4_remarks = models.CharField(max_length=500, blank=True, null=True)
    laundry5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Laundry", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    laundry5_remarks = models.CharField(max_length=500, blank=True, null=True)
    laundry6 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Laundry", verbose_name="Doors: Hardware working properly")
    laundry6_remarks = models.CharField(max_length=500, blank=True, null=True)

    # kitchen
    kitchen1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Kitchen", verbose_name="Refrigerator: Make sure the fridge is running and cool inside")
    kitchen1_remarks = models.CharField(max_length=500, blank=True, null=True)
    kitchen2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Kitchen", verbose_name="Freezer: Make sure freezer is cold and not frozen solid")
    kitchen2_remarks = models.CharField(max_length=500, blank=True, null=True)
    kitchen3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Kitchen", verbose_name="Ice Maker: Ice in bin, working properly")
    kitchen3_remarks = models.CharField(max_length=500, blank=True, null=True)
    kitchen4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Kitchen", verbose_name="Wine Refrigerator: Holding proper temperature")
    kitchen4_remarks = models.CharField(max_length=500, blank=True, null=True)
    kitchen5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Kitchen", verbose_name="Range: All burners working, oven works")
    kitchen5_remarks = models.CharField(max_length=500, blank=True, null=True)
    kitchen6 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Kitchen", verbose_name="Microwave: Working properly")
    kitchen6_remarks = models.CharField(max_length=500, blank=True, null=True)
    kitchen7 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Kitchen", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    kitchen7_remarks = models.CharField(max_length=500, blank=True, null=True)
    kitchen8 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Kitchen", verbose_name="Dishwasher: Run dishwasher monthly")
    kitchen8_remarks = models.CharField(max_length=500, blank=True, null=True)
    kitchen9 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Kitchen", verbose_name="Sinks: Run hot and cold water; Check underneath for signs of leaks")
    kitchen9_remarks = models.CharField(max_length=500, blank=True, null=True)
    kitchen10 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Kitchen", verbose_name="Lights: Any burnt out requiring replacement?")
    kitchen10_remarks = models.CharField(max_length=500, blank=True, null=True)
    kitchen11 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Kitchen", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    kitchen11_remarks = models.CharField(max_length=500, blank=True, null=True)
    kitchen12 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Kitchen", verbose_name="Doors: Hardware working properly")
    kitchen12_remarks = models.CharField(max_length=500, blank=True, null=True)

    # 6. Butlers Pantry
    butlers1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Butlers", verbose_name="Refrigerator: Make sure the fridge is running and cool inside")
    butlers1_remarks = models.CharField(max_length=500, blank=True, null=True)
    butlers2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Butlers", verbose_name="Freezer: Make sure freezer is cold and not frozen solid")
    butlers2_remarks = models.CharField(max_length=500, blank=True, null=True)
    butlers3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Butlers", verbose_name="Ice Maker: Ice in bin, working properly")
    butlers3_remarks = models.CharField(max_length=500, blank=True, null=True)
    butlers4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Butlers", verbose_name="Wine Refrigerator: Holding proper temperature")
    butlers4_remarks = models.CharField(max_length=500, blank=True, null=True)
    butlers5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Butlers", verbose_name="Range: All burners working, oven works")
    butlers5_remarks = models.CharField(max_length=500, blank=True, null=True)
    butlers6 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Butlers", verbose_name="Microwave: Working properly")
    butlers6_remarks = models.CharField(max_length=500, blank=True, null=True)
    butlers7 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Butlers", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    butlers7_remarks = models.CharField(max_length=500, blank=True, null=True)
    butlers8 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Butlers", verbose_name="Dishwasher: Run dishwasher monthly")
    butlers8_remarks = models.CharField(max_length=500, blank=True, null=True)
    butlers9 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Butlers", verbose_name="Sinks: Run hot and cold water; Check underneath for signs of leaks")
    butlers9_remarks = models.CharField(max_length=500, blank=True, null=True)
    butlers10 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Butlers", verbose_name="Lights: Any burnt out requiring replacement?")
    butlers10_remarks = models.CharField(max_length=500, blank=True, null=True)
    butlers11 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Butlers", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    butlers11_remarks = models.CharField(max_length=500, blank=True, null=True)
    butlers12 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Butlers", verbose_name="Doors: Hardware working properly")
    butlers12_remarks = models.CharField(max_length=500, blank=True, null=True)

    # Breakfast Area 
    breakfast1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Breakfast Area", verbose_name="Lights: Any burnt out requiring replacement?")
    breakfast1_remarks = models.CharField(max_length=500, blank=True, null=True)
    breakfast2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Breakfast Area", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    breakfast2_remarks = models.CharField(max_length=500, blank=True, null=True)
    breakfast3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Breakfast Area", verbose_name="Doors: Hardware working properly")
    breakfast3_remarks = models.CharField(max_length=500, blank=True, null=True)
    breakfast4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Breakfast Area", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    breakfast4_remarks = models.CharField(max_length=500, blank=True, null=True)
    breakfast5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Breakfast Area", verbose_name="Furniture: Note any damage")
    breakfast5_remarks = models.CharField(max_length=500, blank=True, null=True)

    # 8. Entry / Foyer
    entry1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Entry / Foyer", verbose_name="Lights: Any burnt out requiring replacement?")
    entry1_remarks = models.CharField(max_length=500, blank=True, null=True)
    entry2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Entry / Foyer", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    entry2_remarks = models.CharField(max_length=500, blank=True, null=True)
    entry3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Entry / Foyer", verbose_name="Doors: Hardware working properly")
    entry3_remarks = models.CharField(max_length=500, blank=True, null=True)
    entry4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Entry / Foyer", verbose_name="Furniture: Note any damage")
    entry4_remarks = models.CharField(max_length=500, blank=True, null=True)

    # 9. Great Room / Family Room
    greatroom1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Great Room / Family Room", verbose_name="Lights: Any burnt out requiring replacement?")
    greatroom1_remarks = models.CharField(max_length=500, blank=True, null=True)
    greatroom2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Great Room / Family Room", verbose_name="Floors / Walls / Ceilings: Visual check of floors/walls/ceilings")
    greatroom2_remarks = models.CharField(max_length=500, blank=True, null=True)
    greatroom3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Great Room / Family Room", verbose_name="Doors: Hardware working properly")
    greatroom3_remarks = models.CharField(max_length=500, blank=True, null=True)
    greatroom4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Great Room / Family Room", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    greatroom4_remarks = models.CharField(max_length=500, blank=True, null=True)
    greatroom5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Great Room / Family Room", verbose_name="Furniture: Note any damage")
    greatroom5_remarks = models.CharField(max_length=500, blank=True, null=True)

    # 10. Dining Room / Area
    dining1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Dining Room / Area", verbose_name="Lights: Any burnt out requiring replacement?")
    dining1_remarks = models.CharField(max_length=500, blank=True, null=True)
    dining2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Dining Room / Area", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    dining2_remarks = models.CharField(max_length=500, blank=True, null=True)
    dining3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Dining Room / Area", verbose_name="Doors: Hardware working properly")
    dining3_remarks = models.CharField(max_length=500, blank=True, null=True)
    dining4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Dining Room / Area", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    dining4_remarks = models.CharField(max_length=500, blank=True, null=True)
    dining5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Dining Room / Area", verbose_name="Furniture: Note any damage")
    dining5_remarks = models.CharField(max_length=500, blank=True, null=True)

    # 11. Closets - Main Level
    closets1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Closets - Main Level", verbose_name="Lights: Any burnt out requiring replacement?")
    closets1_remarks = models.CharField(max_length=500, blank=True, null=True)
    closets2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Closets - Main Level", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    closets2_remarks = models.CharField(max_length=500, blank=True, null=True)
    closets3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Closets - Main Level", verbose_name="Doors: Hardware working properly")
    closets3_remarks = models.CharField(max_length=500, blank=True, null=True)
    closets4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Closets - Main Level", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    closets4_remarks = models.CharField(max_length=500, blank=True, null=True)
    closets5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Closets - Main Level", verbose_name="Furniture: Note any damage")
    closets5_remarks = models.CharField(max_length=500, blank=True, null=True)

    # 12. Closets - Upper Level
    closets_upper1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Closets - Upper Level", verbose_name="Lights: Any burnt out requiring replacement?")
    closets_upper1_remarks = models.CharField(max_length=500, blank=True, null=True)
    closets_upper2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Closets - Upper Level", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    closets_upper2_remarks = models.CharField(max_length=500, blank=True, null=True)
    closets_upper3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Closets - Upper Level", verbose_name="Doors: Hardware working properly")
    closets_upper3_remarks = models.CharField(max_length=500, blank=True, null=True)
    closets_upper4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Closets - Upper Level", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    closets_upper4_remarks = models.CharField(max_length=500, blank=True, null=True)
    closets_upper5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Closets - Upper Level", verbose_name="Furniture: Note any damage")
    closets_upper5_remarks = models.CharField(max_length=500, blank=True, null=True)

    # 13. Hallways - Main Level
    hallways_main1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Hallways - Main Level", verbose_name="Lights: Any burnt out requiring replacement?")
    hallways_main1_remarks = models.CharField(max_length=500, blank=True, null=True)
    hallways_main2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Hallways - Main Level", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    hallways_main2_remarks = models.CharField(max_length=500, blank=True, null=True)
    hallways_main3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Hallways - Main Level", verbose_name="Doors: Hardware working properly")
    hallways_main3_remarks = models.CharField(max_length=500, blank=True, null=True)
    hallways_main4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Hallways - Main Level", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    hallways_main4_remarks = models.CharField(max_length=500, blank=True, null=True)
    hallways_main5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Hallways - Main Level", verbose_name="Furniture: Note any damage")
    hallways_main5_remarks = models.CharField(max_length=500, blank=True, null=True)

    # 13. Hallways - Upper Level
    hallways_upper1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Hallways - Upper Level", verbose_name="Lights: Any burnt out requiring replacement?")
    hallways_upper1_remarks = models.CharField(max_length=500, blank=True, null=True)
    hallways_upper2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Hallways - Upper Level", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    hallways_upper1_remarks = models.CharField(max_length=500, blank=True, null=True)
    hallways_upper3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Hallways - Upper Level", verbose_name="Doors: Hardware working properly")
    hallways_upper3_remarks = models.CharField(max_length=500, blank=True, null=True)
    hallways_upper4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Hallways - Upper Level", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    hallways_upper4_remarks = models.CharField(max_length=500, blank=True, null=True)
    hallways_upper5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Hallways - Upper Level", verbose_name="Furniture: Note any damage")
    hallways_upper5_remarks = models.CharField(max_length=500, blank=True, null=True)


    # Bedroom 1 ( masterbedroom )
    bedroom1_1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 1 (Master Bedroom)", verbose_name="Furniture: Note any damage")
    bedroom1_1_remarks = models.CharField(max_length=500, blank=True, null=True)
    bedroom1_2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 1 (Master Bedroom)", verbose_name="Lights: Any burnt out requiring replacement?")
    bedroom1_2_remarks = models.CharField(max_length=500, blank=True, null=True)
    bedroom1_3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 1 (Master Bedroom)", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    bedroom1_3_remarks = models.CharField(max_length=500, blank=True, null=True)
    bedroom1_4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 1 (Master Bedroom)", verbose_name="Doors: Hardware working properly")
    bedroom1_4_remarks = models.CharField(max_length=500, blank=True, null=True)


    # Bedroom 2 
    bedroom2_1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 2", verbose_name="Furniture: Note any damage")
    bedroom2_1_remarks = models.CharField(max_length=500, blank=True, null=True)
    bedroom2_2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 2", verbose_name="Lights: Any burnt out requiring replacement?")
    bedroom2_2_remarks = models.CharField(max_length=500, blank=True, null=True)
    bedroom2_3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 2", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    bedroom2_3_remarks = models.CharField(max_length=500, blank=True, null=True)
    bedroom2_4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 2", verbose_name="Doors: Hardware working properly")
    bedroom2_4_remarks = models.CharField(max_length=500, blank=True, null=True)

    # Bedroom 3
    bedroom3_1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 3", verbose_name="Furniture: Note any damage")
    bedroom3_1_remarks = models.CharField(max_length=500, blank=True, null=True)
    bedroom3_2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 3", verbose_name="Lights: Any burnt out requiring replacement?")
    bedroom3_2_remarks = models.CharField(max_length=500, blank=True, null=True)
    bedroom3_3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 3", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    bedroom3_3_remarks = models.CharField(max_length=500, blank=True, null=True)
    bedroom3_4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 3", verbose_name="Doors: Hardware working properly")
    bedroom3_4_remarks = models.CharField(max_length=500, blank=True, null=True)

    # Bedroom 4
    bedroom4_1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 4", verbose_name="Furniture: Note any damage")
    bedroom4_1_remarks = models.CharField(max_length=500, blank=True, null=True)
    bedroom4_2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 4", verbose_name="Lights: Any burnt out requiring replacement?")
    bedroom4_2_remarks = models.CharField(max_length=500, blank=True, null=True)
    bedroom4_3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 4", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    bedroom4_3_remarks = models.CharField(max_length=500, blank=True, null=True)
    bedroom4_4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bedroom 4", verbose_name="Doors: Hardware working properly")
    bedroom4_4_remarks = models.CharField(max_length=500, blank=True, null=True)

    # Bathroom 1
    bathroom1_1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 1 (Master Bath)", verbose_name="Sinks: Faucet leaking, drain acceptable, overall condition")
    bathroom1_1_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom1_2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 1 (Master Bath)", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    bathroom1_2_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom1_3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 1 (Master Bath)", verbose_name="Shower: Faucet leaking, drain acceptable, overall condition")
    bathroom1_3_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom1_4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 1 (Master Bath)", verbose_name="Bath/Hot Tub: Faucet leaking, drain acceptable, overall condition")
    bathroom1_4_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom1_5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 1 (Master Bath)", verbose_name="Toilet: Tank refills properly, Handle operational")
    bathroom1_5_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom1_6 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 1 (Master Bath)", verbose_name="Lights: Any burnt out requiring replacement?")
    bathroom1_6_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom1_7 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 1 (Master Bath)", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    bathroom1_7_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom1_8 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 1 (Master Bath)", verbose_name="Doors: Hardware working properly")
    bathroom1_8_remarks = models.CharField(max_length=500, blank=True, null=True)

    # Barhroom 2 
    bathroom2_1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 2 (Secondary Bath)", verbose_name="Sinks: Faucet leaking, drain acceptable, overall condition")
    bathroom2_1_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom2_2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 2 (Secondary Bath)", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    bathroom2_2_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom2_3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 2 (Secondary Bath)", verbose_name="Shower: Faucet leaking, drain acceptable, overall condition")
    bathroom2_3_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom2_4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 2 (Secondary Bath)", verbose_name="Bath/Hot Tub: Faucet leaking, drain acceptable, overall condition")
    bathroom2_4_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom2_5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 2 (Secondary Bath)", verbose_name="Toilet: Tank refills properly, Handle operational")
    bathroom2_5_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom2_6 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 2 (Secondary Bath)", verbose_name="Lights: Any burnt out requiring replacement?")
    bathroom2_6_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom2_7 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 2 (Secondary Bath)", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    bathroom2_7_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom2_8 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 2 (Secondary Bath)", verbose_name="Doors: Hardware working properly")
    bathroom2_8_remarks = models.CharField(max_length=500, blank=True, null=True)


    # Bathroom 3 
    bathroom3_1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 3 (Guest Bath)", verbose_name="Sinks: Faucet leaking, drain acceptable, overall condition")
    bathroom3_1_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom3_2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 3 (Guest Bath)", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    bathroom3_2_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom3_3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 3 (Guest Bath)", verbose_name="Shower: Faucet leaking, drain acceptable, overall condition")
    bathroom3_3_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom3_4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 3 (Guest Bath)", verbose_name="Bath/Hot Tub: Faucet leaking, drain acceptable, overall condition")
    bathroom3_4_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom3_5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 3 (Guest Bath)", verbose_name="Toilet: Tank refills properly, Handle operational")
    bathroom3_5_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom3_6 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 3 (Guest Bath)", verbose_name="Lights: Any burnt out requiring replacement?")
    bathroom3_6_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom3_7 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 3 (Guest Bath)", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    bathroom3_7_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom3_8 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 3 (Guest Bath)", verbose_name="Doors: Hardware working properly")
    bathroom3_8_remarks = models.CharField(max_length=500, blank=True, null=True)

    # Barhroom 4
    bathroom4_1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 4 (Powder Room)", verbose_name="Sinks: Faucet leaking, drain acceptable, overall condition")
    bathroom4_1_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom4_2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 4 (Powder Room)", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    bathroom4_2_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom4_3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 4 (Powder Room)", verbose_name="Shower: Faucet leaking, drain acceptable, overall condition")
    bathroom4_3_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom4_4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 4 (Powder Room)", verbose_name="Bath/Hot Tub: Faucet leaking, drain acceptable, overall condition")
    bathroom4_4_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom4_5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 4 (Powder Room)", verbose_name="Toilet: Tank refills properly, Handle operational")
    bathroom4_5_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom4_6 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 4 (Powder Room)", verbose_name="Lights: Any burnt out requiring replacement?")
    bathroom4_6_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom4_7 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 4 (Powder Room)", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    bathroom4_7_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom4_8 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 4 (Powder Room)", verbose_name="Doors: Hardware working properly")
    bathroom4_8_remarks = models.CharField(max_length=500, blank=True, null=True)

    bathroom5_1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 4 (Powder Room)", verbose_name="Sinks: Faucet leaking, drain acceptable, overall condition")
    bathroom5_1_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom5_2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 4 (Powder Room)", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    bathroom5_2_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom5_3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 4 (Powder Room)", verbose_name="Shower: Faucet leaking, drain acceptable, overall condition")
    bathroom5_3_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom5_4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 4 (Powder Room)", verbose_name="Bath/Hot Tub: Faucet leaking, drain acceptable, overall condition")
    bathroom5_4_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom5_5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 4 (Powder Room)", verbose_name="Toilet: Tank refills properly, Handle operational")
    bathroom5_5_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom5_6 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 4 (Powder Room)", verbose_name="Lights: Any burnt out requiring replacement?")
    bathroom5_6_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom5_7 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 4 (Powder Room)", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    bathroom5_7_remarks = models.CharField(max_length=500, blank=True, null=True)
    bathroom5_8 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Bathroom 4 (Powder Room)", verbose_name="Doors: Hardware working properly")
    bathroom5_8_remarks = models.CharField(max_length=500, blank=True, null=True)

    # Gym 
    gym_1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Gym", verbose_name="Aa Sinks: Faucet leaking, drain acceptable, overall condition")
    gym_1_remarks = models.CharField(max_length=500, blank=True, null=True)
    gym_2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Gym", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    gym_2_remarks = models.CharField(max_length=500, blank=True, null=True)
    gym_3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Gym", verbose_name="Shower: Faucet leaking, drain acceptable, overall condition")
    gym_3_remarks = models.CharField(max_length=500, blank=True, null=True)
    gym_4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Gym", verbose_name="Toilet: Tank refills properly, Handle operational")
    gym_4_remarks = models.CharField(max_length=500, blank=True, null=True)
    gym_5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Gym", verbose_name="Lights: Any burnt out requiring replacement?")
    gym_5_remarks = models.CharField(max_length=500, blank=True, null=True)
    gym_6 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Gym", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    gym_6_remarks = models.CharField(max_length=500, blank=True, null=True)
    gym_7 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Gym", verbose_name="Doors: Hardware working properly")
    gym_7_remarks = models.CharField(max_length=500, blank=True, null=True)

    # Theater 
    theatre_1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Theatre / Music Room", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    theatre_1_remarks = models.CharField(max_length=500, blank=True, null=True)
    theatre_2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Theatre / Music Room", verbose_name="Lights: Any burnt out requiring replacement?")
    theatre_2_remarks = models.CharField(max_length=500, blank=True, null=True)
    theatre_3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Theatre / Music Room", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    theatre_3_remarks = models.CharField(max_length=500, blank=True, null=True)
    theatre_4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Theatre / Music Room", verbose_name="Doors: Hardware working properly")
    theatre_4_remarks = models.CharField(max_length=500, blank=True, null=True)
    theatre_5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Theatre / Music Room", verbose_name="Furniture: Note any damage")
    theatre_5_remarks = models.CharField(max_length=500, blank=True, null=True)

    # Guest House 
    guest_house_1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Sleeping / Living", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    guest_house_1_remarks = models.CharField(max_length=500, blank=True, null=True)
    guest_house_2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Sleeping / Living", verbose_name="Doors: Hardware working properly")
    guest_house_2_remarks = models.CharField(max_length=500, blank=True, null=True)
    guest_house_3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Sleeping / Living", verbose_name="Furniture: Note any damage")
    guest_house_3_remarks = models.CharField(max_length=500, blank=True, null=True)
    guest_house_4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Sleeping / Living", verbose_name="Lights: Any burnt out requiring replacement?")
    guest_house_4_remarks = models.CharField(max_length=500, blank=True, null=True)
    guest_house_5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Sleeping / Living", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    guest_house_5_remarks = models.CharField(max_length=500, blank=True, null=True)

    # Guest House Bathrooms
    guest_house_bath_1 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Bathroom", verbose_name="Sinks: Faucet leaking, drain acceptable, overall condition")
    guest_house_bath_1_remarks = models.CharField(max_length=500, blank=True, null=True)
    guest_house_bath_2 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Bathroom", verbose_name="Cabinets / Tops: Visual Check of cabinets, countertops")
    guest_house_bath_2_remarks = models.CharField(max_length=500, blank=True, null=True)
    guest_house_bath_3 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Bathroom", verbose_name="Shower: Faucet leaking, drain acceptable, overall condition")
    guest_house_bath_3_remarks = models.CharField(max_length=500, blank=True, null=True)
    guest_house_bath_4 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Bathroom", verbose_name="Bath/Hot Tub: Faucet leaking, drain acceptable, overall condition")
    guest_house_bath_4_remarks = models.CharField(max_length=500, blank=True, null=True)
    guest_house_bath_5 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Bathroom", verbose_name="Toilet: Tank refills properly, Handle operational")
    guest_house_bath_5_remarks = models.CharField(max_length=500, blank=True, null=True)
    guest_house_bath_6 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Bathroom", verbose_name="Lights: Any burnt out requiring replacement?")
    guest_house_bath_6_remarks = models.CharField(max_length=500, blank=True, null=True)
    guest_house_bath_7 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Bathroom", verbose_name="Flooring / Walls / Ceilings: Visual check of floors/walls/ceilings")
    guest_house_bath_7_remarks = models.CharField(max_length=500, blank=True, null=True)
    guest_house_bath_8 = CategoryCharField(max_length=20, choices=MCQ_CHOICES, blank=True, null=True, category="Guest House - Bathroom", verbose_name="Doors: Hardware working properly")
    guest_house_bath_8_remarks = models.CharField(max_length=500, blank=True, null=True)
