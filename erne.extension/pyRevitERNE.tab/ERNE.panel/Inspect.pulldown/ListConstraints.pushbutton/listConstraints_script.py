import clr
import Autodesk.Revit.DB
import Autodesk.Revit.UI
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import BuiltInCategory

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

collector = FilteredElementCollector(doc)
constraints = collector.OfCategory(BuiltInCategory.OST_Constraints).WhereElementIsNotElementType().ToElements()

for i, c in enumerate(constraints):
    print(50*"_" + str(i + 1) + ":")
    print(str(c.Id.IntegerValue) + " constraint: between these elements: ")
    for ref in c.References:
        category = doc.GetElement(ref.ElementId).Category.Name
        name = doc.GetElement(ref.ElementId).Name
        id = ref.ElementId.IntegerValue
        print(str(id) + " - " + category + " - " + name)

print(50*"_")
print(str(constraints.Count) + " constraints found in model.")
