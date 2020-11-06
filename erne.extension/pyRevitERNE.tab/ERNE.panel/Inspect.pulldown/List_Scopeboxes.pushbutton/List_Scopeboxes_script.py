# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, WorksharingUtils
from collections import defaultdict
from rpw import doc

selection = [doc.GetElement(elId) for elId in __revit__.ActiveUIDocument.Selection.GetElementIds()]

cl = FilteredElementCollector(doc)
scopeboxes = cl.OfCategory(BuiltInCategory.OST_VolumeOfInterest).WhereElementIsNotElementType().ToElements()

sb_dict = defaultdict(list)

for sb in scopeboxes:
    name = sb.Name
    sb_dict[name].append(sb)

for n, s in sorted(zip(sb_dict.keys(), sb_dict.values())):
    creator = WorksharingUtils.GetWorksharingTooltipInfo(doc, s[0].Id).Creator
    print("Scopebox: {0} created by:{1}".format(
            str(n).rjust(30),
            creator.rjust(15),
    ))
