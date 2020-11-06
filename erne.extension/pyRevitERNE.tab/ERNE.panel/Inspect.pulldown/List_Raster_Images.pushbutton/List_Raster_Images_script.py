import clr
clr.AddReference("RevitAPI")
import Autodesk.Revit.UI
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import BuiltInCategory as Bic
from Autodesk.Revit.DB import WorksharingUtils
from System.Diagnostics import Stopwatch
from collections import defaultdict
from pyrevit import script

stopwatch = Stopwatch()
stopwatch.Start()

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
output = script.get_output()


def report_img(img_type, img_insts_dict):
    img_id = output.linkify(img_type.Id)
    creator = WorksharingUtils.GetWorksharingTooltipInfo(doc, img_type.Id).Creator
    type_name = img_type.LookupParameter("Type Name").AsString()
    insts_count = str(len(img_insts_dict[type_name]))
    inst_ids = ",".join([output.linkify(elem.Id) for elem in img_insts_dict[type_name]])
    # img_data = [img_id.ljust(10), creator.ljust(15), type_name, img_type.Path, insts_count, inst_ids]
    # this_script.output.print_md("<pre> Id:{} ; {} ; {} ; {} ; {} instances: ; {}</pre>".format(*img_data))
    img_type_data = [img_id.ljust(10), creator.ljust(15), type_name, img_type.Path]
    output.print_md("<pre> Id:{} ; {} ; {} ; {} </pre>".format(*img_type_data))
    output.print_md("<pre> {} instances: ; {}</pre>".format(insts_count.rjust(30), inst_ids))
    # print(inst_ids)


def count_raster_images(filtered, filter_paths):
    img_types = Fec(doc).OfClass(Autodesk.Revit.DB.ImageType).ToElements()
    img_insts = Fec(doc).OfCategory(Bic.OST_RasterImages).WhereElementIsNotElementType().ToElements()
    img_dict = defaultdict(list)

    for img_inst in img_insts:
        img_type_name = doc.GetElement(img_inst.GetTypeId()).LookupParameter("Type Name").AsString()
        img_dict[img_type_name].append(img_inst)

    if filtered == "all":
        for img in img_types:
            report_img(img, img_dict)
        return str(img_types.Count)

    if filtered == "non-project":
        counter = 0
        for img in img_types:
            for path in filter_paths:
                if path in img.Path:
                    counter += 1
                    report_img(img, img_dict)
        return str(counter)


non_project_paths = ["C:", "D:", "U:"]

print(40 * "-" + "all_raster_images")
count_all_images = count_raster_images("all", None)
print(40 * "-" + "non_project_raster_images")
count_non_project_images = count_raster_images("non-project", non_project_paths)

print("pyRevit findNonProjectPathImages found " + str(count_non_project_images) +
      " raster images types in non project paths in: ")
stopwatch.Stop()
timespan = stopwatch.Elapsed
print(timespan)
