import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import BuiltInCategory as Bic
from Autodesk.Revit.DB import ViewType, View
from Autodesk.Revit.DB import WorksharingUtils

doc = __revit__.ActiveUIDocument.Document
views = Fec(doc).OfClass(View).WhereElementIsNotElementType().ToElements()

plan_views = []
not_sheeted_views = []

for i in views:
    if not i.IsTemplate:
        if i.ViewType == ViewType.AreaPlan:
            plan_views.append(i)
        elif i.ViewType == ViewType.CeilingPlan:
            plan_views.append(i)
        elif i.ViewType == ViewType.Detail:
            plan_views.append(i)
        elif i.ViewType == ViewType.DraftingView:
            plan_views.append(i)
        elif i.ViewType == ViewType.Elevation:
            plan_views.append(i)
        elif i.ViewType == ViewType.FloorPlan:
            plan_views.append(i)
        elif i.ViewType == ViewType.Section:
            plan_views.append(i)

for i, v in enumerate(plan_views):
    found_nr = ""
    shNrs = v.GetParameters("Sheet Number")
    for n in shNrs:
        found_nr += n.AsString()
    if found_nr == "---":
        not_sheeted_views.append(v)

for non_sheeted_view in not_sheeted_views:
    vName = non_sheeted_view.Name
    author = WorksharingUtils.GetWorksharingTooltipInfo(doc, non_sheeted_view.Id).Creator
    print(vName, author)

print(str(len(not_sheeted_views)) + " Views not on Sheets")
