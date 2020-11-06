import clr
import Autodesk.Revit.DB
import Autodesk.Revit.UI
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.UI import TaskDialog

from collections import defaultdict

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

selection = [doc.GetElement(elId) for elId in uidoc.Selection.GetElementIds()]
allElements = FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements()
element_categories = defaultdict(list)
ws_table = doc.GetWorksetTable()

if len(selection) == 1:
    if "Level" in str(selection[0].GetType):
        sel_Level = selection[0]
        counter = 0
        print(sel_Level.Name)

        for i, e in enumerate(allElements):
            if e.LevelId == sel_Level.Id:
                counter += 1
                element_categories[e.Category.Name].append(e)
        # print(element_categories)

        for cat in element_categories:
            print(15*"_" + cat + ": " + str(len(element_categories[cat])))
            for elem in element_categories[cat]:
                print("id: {} - workset: {}".format(elem.Id.IntegerValue, ws_table.GetWorkset(elem.WorksetId).Name))

        print(15*"_" + str(len(element_categories)) + " Categories found in " + sel_Level.Name + ":")

        for cat in element_categories:
            print(str(cat) + ": " + str(len(element_categories[cat])))

        print(str(counter) + " Elements found in " + sel_Level.Name)
        print(str(allElements.Count) + " Elements found in project.")

    else:
        pass
        __window__.Close()
        TaskDialog.Show('pyRevit', 'Exactly one level must be selected.')
else:
    pass
    __window__.Close()
    TaskDialog.Show('pyRevit', 'Exactly one level must be selected.')
