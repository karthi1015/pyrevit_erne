# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import ElementId, WorksharingUtils
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import BuiltInCategory as Bic
from collections import defaultdict
from rpw import doc

view_lines = defaultdict(int)

lines_in_project = Fec(doc).OfCategory(Bic.OST_Lines).WhereElementIsNotElementType().ToElements()
lines = [l for l in lines_in_project]

for line in lines:
    try:
        view_id = line.OwnerViewId.IntegerValue
        view_lines[view_id] += 1
    except:
        pass

for line_count, view_id in sorted(zip(view_lines.values(), view_lines.keys()), reverse=True):
    rvt_view_id = ElementId(view_id)
    try:
        view_name = doc.GetElement(rvt_view_id).Name
    except:
        view_name = "NoNameInDB"
    print('{0} Lines in ViewId:{1} ViewCreator: {2} ViewName: {3}'.format(
        str(line_count).rjust(6),
        str(view_id).rjust(9),
        WorksharingUtils.GetWorksharingTooltipInfo(doc, rvt_view_id).Creator.ljust(15),
        view_name.ljust(60)))

info = "{} lines in {} views ".format(len(lines), len(view_lines))
print(info)# parser check #
