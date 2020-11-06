# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, WorksharingUtils
from collections import defaultdict
from rpw import doc

selection = [doc.GetElement(elId) for elId in __revit__.ActiveUIDocument.Selection.GetElementIds()]

cl = FilteredElementCollector(doc)
scopeboxes = cl.OfCategory(BuiltInCategory.OST_VolumeOfInterest).WhereElementIsNotElementType().ToElements()

sb_dict = defaultdict(list)

for scopebox in scopeboxes:
    name = scopebox.Name
    sb_dict[name].append(scopebox)

for name, scopeboxes in sorted(zip(sb_dict.keys(), sb_dict.values())):
    creator = WorksharingUtils.GetWorksharingTooltipInfo(
        doc, scopeboxes[0].Id).Creator
    info = "Scopebox: {0} created by:{1}".format(
        str(name).rjust(30),
        creator.rjust(15),
    )
    print(info)# parser check #
