import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import BuiltInCategory as Bic
from Autodesk.Revit.DB import GroupType, WorksharingUtils
from collections import defaultdict
from System.Diagnostics import Stopwatch
from pyrevit import script

stopwatch = Stopwatch()
stopwatch.Start()

doc = __revit__.ActiveUIDocument.Document
output = script.get_output()

groupsTypes = Fec(doc).OfClass(GroupType).ToElements()
modelGroupInst = Fec(doc).OfCategory(Bic.OST_IOSModelGroups).WhereElementIsNotElementType().ToElements()
detailGroupInst = Fec(doc).OfCategory(Bic.OST_IOSDetailGroups).WhereElementIsNotElementType().ToElements()

model_groups = defaultdict(list)
detail_groups = defaultdict(list)


def report_groups(collector, group_dict):
    counts = []
    for group in collector:
        if not group_dict[group.Name]:
            group_dict[group.Name] = {"last_id": "", "count": 0}
        group_dict[group.Name]["last_id"] = group.Id
        group_dict[group.Name]["count"] += 1

    for group in group_dict:
        counts.append(group_dict[group]["count"])

    for count, name in sorted(zip(counts, group_dict), reverse=True):
        click_id = output.linkify(group_dict[name]["last_id"])
        creator = WorksharingUtils.GetWorksharingTooltipInfo(doc, group_dict[name]["last_id"]).Creator
        output.print_md("<pre>{} last Id: {} by: {} has {} Instances</pre>".format(name.ljust(50),
                                                                                               click_id,
                                                                                               creator.ljust(12),
                                                                                               count))


print("groupsTypes: " + str(len((groupsTypes))))
print("modelGroupInst: " + str(len((modelGroupInst))))
print("detailGroupInst: " + str(len((detailGroupInst))))

print(68 * "-" + "Model_Groups")
report_groups(modelGroupInst, model_groups)
print(68 * "-" + "Detail_Groups")
report_groups(detailGroupInst, detail_groups)

print("HdMpyRevit_groups_overview listed in: ")
stopwatch.Stop()
timespan = stopwatch.Elapsed
print(timespan)
