import clr
clr.AddReference("RevitAPI")
import Autodesk.Revit.UI
from Autodesk.Revit.DB import FilteredElementCollector as fec
from collections import defaultdict
from System.Diagnostics import Stopwatch

stopwatch = Stopwatch()
stopwatch.Start()

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

rvt_version = app.VersionNumber

aView = doc.ActiveView

ind_tags = fec(doc, aView.Id).OfClass(Autodesk.Revit.DB.IndependentTag).ToElements()
spatial_tags = fec(doc, aView.Id).OfClass(Autodesk.Revit.DB.SpatialElementTag).ToElements()

orphaned_tag_views = defaultdict(list)
orphaned_tag_counter = 0

for i_tag in ind_tags:
    if i_tag.IsOrphaned:
        tag_view_id = i_tag.OwnerViewId
        orphaned_tag_views[tag_view_id].append(i_tag)

# only working from rvt 2017 onwards
if int(rvt_version) > 2016:
    for s_tag in spatial_tags:
        if s_tag.IsOrphaned:
            tag_view_id = s_tag.OwnerViewId
            orphaned_tag_views[tag_view_id].append(s_tag)

for view_id in orphaned_tag_views:
    tag_view_name = doc.GetElement(view_id).Name
    print(50*"_" + tag_view_name)
    for tag in orphaned_tag_views[view_id]:
        orphaned_tag_counter += 1
        tag_creator = Autodesk.Revit.DB.WorksharingUtils.GetWorksharingTooltipInfo(doc, tag.Id).Creator
        print(" Id: " + str(tag.Id.IntegerValue) +
              " " + tag_creator +
              " " + tag.Category.Name
              )

print("pyRevit findOrphanedTags found " + str(orphaned_tag_counter) + " orphaned tags run in: ")
stopwatch.Stop()
timespan = stopwatch.Elapsed
print(timespan)

print("WARNING: Revit 2016 and older does not allow check for orphaned area and room tags!!")
