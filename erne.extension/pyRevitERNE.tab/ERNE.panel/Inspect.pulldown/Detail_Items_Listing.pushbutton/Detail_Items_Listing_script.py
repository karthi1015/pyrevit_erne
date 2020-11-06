import clr
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import BuiltInCategory as Bic
from Autodesk.Revit.DB import ViewType
from collections import defaultdict

doc = __revit__.ActiveUIDocument.Document

types_dict = defaultdict(list)
det_comps = Fec(doc).OfCategory(Bic.OST_DetailComponents).WhereElementIsNotElementType().ToElements()

for det in det_comps:
    hostView = doc.GetElement(det.OwnerViewId)
    if hostView.ViewType == ViewType.Legend:
        types_dict[det.Name].append(doc.GetElement(det.OwnerViewId).Name)

for type_name in types_dict:
    print("Instances of type: " + type_name)
    print("on following views:")
    for view in types_dict[type_name]:
        print("   - " + view)
