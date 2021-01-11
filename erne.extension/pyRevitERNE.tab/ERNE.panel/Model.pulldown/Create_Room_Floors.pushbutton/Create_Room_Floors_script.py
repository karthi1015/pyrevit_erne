"""
Creates a floor for each selected room or all rooms.
FloorType is selected from room parameter "Floor Finish" or first FloorType
"""
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import BuiltInCategory as Bic
from Autodesk.Revit.DB import BuiltInParameter, CurveArray, ElementId, Options
from Autodesk.Revit.DB import SpatialElementType
from Autodesk.Revit.DB import SpatialElementBoundaryOptions, AreaVolumeSettings
from System.Collections.Generic import List
from System.Diagnostics import Stopwatch
from collections import defaultdict
from rpw import doc, uidoc, db


def create_room_floor(longest_room_boundary, floor_type, level):
    print("room {}: creating floor object".format(room_id))
    floor = doc.Create.NewFloor(
        longest_room_boundary,
        floor_type,
        level,
        STRUCTURAL,
    )
    floor.LookupParameter("Kommentare").Set(room_guid)
    return floor


def add_opening(floor, curve_array):
    opening = doc.Create.NewOpening(
        floor,
        curve_array,
        True,
    )
    return opening


def get_boundaries_by_length(bound_segments):
    boundary_lengths = {}
    for boundary_list in bound_segments:
        length = 0.0
        for boundary in boundary_list:
            length += boundary.GetCurve().Length
        boundary_lengths[length] = boundary_list
    return boundary_lengths


def get_room_boundaries(room, doc):
    bound_loc = AreaVolumeSettings.GetAreaVolumeSettings(doc).GetSpatialElementBoundaryLocation(SpatialElementType.Room)
    spat_opt = SpatialElementBoundaryOptions()
    spat_opt.SpatialElementBoundaryLocation = bound_loc
    bound_segments = room.GetBoundarySegments(spat_opt)
    if len(bound_segments) > 1:
        print("more than one boundary curve detected - using the longest one!")
    boundaries_by_length = get_boundaries_by_length(bound_segments)
    curve_arrays_by_length = {}
    for length, boundary_loop in boundaries_by_length.items():
        curve_array = CurveArray()
        for boundary in boundary_loop:
            curve_array.Append(boundary.GetCurve())
        curve_arrays_by_length[length] = curve_array
    return curve_arrays_by_length


stopwatch = Stopwatch()
stopwatch.Start()

selection = [doc.GetElement(el_id) for el_id in uidoc.Selection.GetElementIds()]
selection_ids = [el_id for el_id in uidoc.Selection.GetElementIds()]
selected_ids = List[ElementId](selection_ids)

if not selection:
    floor_rooms = Fec(doc).OfCategory(Bic.OST_Rooms).ToElements()
else:
    floor_rooms = Fec(doc, selected_ids).OfCategory(Bic.OST_Rooms).ToElements()

STRUCTURAL = False
geo_opt = Options()

floors = Fec(doc).OfCategory(Bic.OST_Floors).WhereElementIsNotElementType().ToElements()
floors_by_room_guid = {fl.LookupParameter("Kommentare").AsString(): fl for fl in floors}

floor_types = Fec(doc).OfCategory(Bic.OST_Floors).WhereElementIsElementType().ToElements()
floor_types_by_name = {ft.LookupParameter("Typname").AsString(): ft for ft in floor_types}

floor_openings_to_add = defaultdict(list)

print("processing {} rooms.".format(len(floor_rooms)))

with db.Transaction("create/update_room_floors"):
    for room in floor_rooms:
        print(35 * "-")
        room_id = room.Id
        room_guid = room.UniqueId
        room_level = doc.GetElement(room.LevelId)
        room_boundaries = get_room_boundaries(room, doc)
        longest_room_boundary = room_boundaries[max(room_boundaries.keys())]
        room_floor_finish = room.get_Parameter(BuiltInParameter.ROOM_FINISH_FLOOR).AsString()

        floor_type = floor_types[0]
        # print(room_guid, floors_by_room_guid.get(room_guid))

        if room_guid in floors_by_room_guid:
            existing_room_floor = floors_by_room_guid[room_guid]
            print("room {}: floor for this room already exists - replacing it.".format(room_id))
            # could we instead just update? replace floor curve loop(s)?
            # https://thebuildingcoder.typepad.com/blog/2008/11/editing-a-floor-profile.html
            # this adds only floor openings not additional curve_arrays
            # https://thebuildingcoder.typepad.com/blog/2013/07/create-a-floor-with-an-opening-or-complex-boundary.html
            # -> Jeremy: "There is no way to create an exact copy of a floor with holes using API as in the UI."
            # continue
            doc.Delete(existing_room_floor.Id)
            doc.Regenerate()

        if room_floor_finish:
            print("room {}: found floor finish: {}".format(room_id, room_floor_finish))
            if floor_types_by_name.get(room_floor_finish):
                print("found appropriate floor type: {}".format(room_floor_finish))
                floor_type = floor_types_by_name[room_floor_finish]

        if longest_room_boundary:
            existing_room_floor = create_room_floor(
                longest_room_boundary,
                floor_type,
                room_level,
            )
        else:
            print("room {}: creating floor object skipped!!".format(room_id))

        if len(room_boundaries) > 1:
            opening_curve_array_lengths = sorted(room_boundaries.keys())[:-1]
            opening_curve_arrays = [room_boundaries[l] for l in opening_curve_array_lengths]
            for curve_array in opening_curve_arrays:
                floor_openings_to_add[existing_room_floor].append(curve_array)

with db.Transaction("add_floor_opening"):
        print("room {}: adding openings:".format(room_id))
        for floor, openings in floor_openings_to_add.items():
            for curve_array in openings:
                add_opening(floor, curve_array)

print("\n{} updated {} floor rooms in: ".format(__file__, len(floor_rooms)))

stopwatch.Stop()
print(stopwatch.Elapsed)
