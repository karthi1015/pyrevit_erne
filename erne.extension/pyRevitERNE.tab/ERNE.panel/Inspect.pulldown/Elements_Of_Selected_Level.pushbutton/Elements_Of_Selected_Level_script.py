from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.UI import TaskDialog
from collections import defaultdict
from rpw import doc, uidoc


def sep_line(length):
    return length * "_"


selection = [doc.GetElement(elId) for elId in uidoc.Selection.GetElementIds()]
all_elements = Fec(doc).WhereElementIsNotElementType().ToElements()
element_categories = defaultdict(list)
ws_table = doc.GetWorksetTable()

if len(selection) == 1:
    if "Level" in str(selection[0].GetType):
        selected_level = selection[0]
        counter = 0
        print(selected_level.Name)

        for i, element in enumerate(all_elements):
            if element.LevelId == selected_level.Id:
                counter += 1
                element_categories[element.Category.Name].append(element)

        for cat in element_categories:
            print("{}{}: {}".format(sep_line(15), cat, len(element_categories[cat])))
            for elem in element_categories[cat]:
                print("id: {} - workset: {}".format(elem.Id.IntegerValue, ws_table.GetWorkset(elem.WorksetId).Name))

        print("{}{} Categories found in {}:".format(sep_line(15), len(element_categories), selected_level.Name))

        for cat in element_categories:
            print("{}: {}".format(cat, (len(element_categories[cat]))))

        print("{} Elements found in {}".format(counter, selected_level.Name))
        print("{} Elements found in project.".format(all_elements.Count))

    else:
        TaskDialog.Show('pyRevit', 'Exactly one level must be selected.')
else:
    TaskDialog.Show('pyRevit', 'Exactly one level must be selected.')
