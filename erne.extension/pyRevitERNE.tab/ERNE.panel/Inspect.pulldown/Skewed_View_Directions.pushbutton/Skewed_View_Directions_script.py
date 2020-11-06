import clr
from Autodesk.Revit.DB import View, ViewType
from Autodesk.Revit.DB import FilteredElementCollector as Fec

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

views = Fec(doc).OfClass(View).WhereElementIsNotElementType().ToElements()


def print_view_stats(view, vw, up, ri):
    print("_" * 50)
    print(view.Name)
    print(view.ViewType)
    print("Is Viewtemplate: " + str(view.IsTemplate))
    print("Id: " + str(view.Id.IntegerValue))
    print(v_vw_dir)
    print(v_vw_dir[0])
    print(v_up_dir)
    print(v_up_dir[0])
    print(v_ri_dir)
    print(v_ri_dir[0])


for i, v in enumerate(views):
    if not v.IsTemplate:
        if v.ViewType != ViewType.ThreeD:

            v_vw_dir = v.ViewDirection
            v_up_dir = v.UpDirection
            v_ri_dir = v.RightDirection

            if not v_up_dir[0].is_integer():
                print_view_stats(v, v_vw_dir, v_up_dir, v_ri_dir)

            elif not v_ri_dir[0].is_integer():
                print_view_stats(v, v_vw_dir, v_up_dir, v_ri_dir)
