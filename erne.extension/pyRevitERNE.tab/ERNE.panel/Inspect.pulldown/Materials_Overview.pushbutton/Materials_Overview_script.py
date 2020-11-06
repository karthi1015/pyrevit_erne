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

mats_dict = defaultdict(list)

mats = fec(doc).OfClass(Autodesk.Revit.DB.Material).ToElements()
pats = fec(doc).OfClass(Autodesk.Revit.DB.FillPatternElement).ToElements()


for i, mat in enumerate(mats):
    mat_cut_pattern_name = ""
    try:
        mat_cut_pattern_name = doc.GetElement(mat.Id).Name
    except:
        pass
    if mat_cut_pattern_name:
        mats_dict[mat.Id].append([mat.Name, mat_cut_pattern_name])
    # print([i, mat.Name, mat_cut_pattern_name])

    print('{0} Id: {1} Material: {2} MaterialCreator: {3} CutPattern: {4}'.format(
        str(i).zfill(3).rjust(4),
        str(mat.Id.IntegerValue).rjust(8),
        str(mat.Name.decode("utf-8", "replace")).ljust(45),
        Autodesk.Revit.DB.WorksharingUtils.GetWorksharingTooltipInfo(doc, mat.Id).Creator.ljust(11),
        str(mat_cut_pattern_name.decode("utf-8", "replace")).ljust(70)))

"""
with codecs.open(slog, mode="r", encoding="utf-16") as f:
    content = f.readlines()

str(mat_list[213].Name.decode("utf-8", "replace"))
"""
