from Autodesk.Revit.UI import TaskDialog

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

selection = [doc.GetElement(elId) for elId in uidoc.Selection.GetElementIds()]
ft_mm = 304.8


def get_crv_data(crv):
    crv_start = crv.GetEndPoint(0)
    crv_end = crv.GetEndPoint(1)
    crv_len = crv.Length
    return [crv_start, crv_end, crv_len]

if len(selection) == 1:
    line_obj = selection[0]

    try:
        line_start, line_end, line_len = get_crv_data(line_obj.Location.Curve)

    except:
        if selection[0].Category.Name == "Grids":
            grid_line = selection[0].Curve
            line_start, line_end, line_len = get_crv_data(grid_line)

    # rvt internal feet measurements:
    # print("Line Start Coordinate: " + str(line_start))
    # print("Line End Coordinate: " + str(line_end))
    # print("Line Coordinate Deltas: " + str(line_start - line_end))
    # print("Line Length: " + str(line_len))

    # mm:
    print("Line Start Coordinate mm: " + str(line_start * ft_mm))
    print("Line End Coordinate mm: " + str(line_end * ft_mm))
    print("Line Coordinate Deltas mm: " + str((line_start - line_end) * ft_mm))
    print("Line Length mm: " + str(line_len * ft_mm))

else:
    __window__.Close()
    TaskDialog.Show('pyRevit', 'Exactly one detail line must be selected.')
