import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import WorksharingUtils
from rpw import doc as DOC


def get_elem_creator(elem, doc=None):
    if not doc:
        doc = DOC
    return WorksharingUtils.GetWorksharingTooltipInfo(doc, elem.Id).Creator

