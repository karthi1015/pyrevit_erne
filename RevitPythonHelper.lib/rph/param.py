#-*- coding: UTF-8 -*-
import re
from collections import namedtuple
from rpw import doc, DB


def print_param_mapping(param_dict, title="", verbose=True):
    """
    Prints a key value pairs of the parameter dict
    Args:
        param_dict:
    Returns:
    """
    if verbose:
        print(title)
        for key in param_dict:
            print(35 * "-")
            print(key)
            print(param_dict[key])


def get_info_map(element, verbose=None, name=None, regex=None):
    """
    Retrieve an overview of parameters of the provided element.
    Prints out the gathered parameter information
    Args:
        element: Element that holds the parameters.
    Returns:
        Returns two dictionaries: Instance dict, Type dict.
        If no type is available second dict is None
    """
    info_map = []
    info_map.extend(collect_infos(element))
    if "GetTypeId" in dir(element):
        if element.GetTypeId() != DB.ElementId.InvalidElementId:
            elem_type = doc.GetElement(element.GetTypeId())
            info_map.extend(collect_infos(elem_type, is_type_param=True))

    if name:
        return sorted(pi for pi in info_map if pi.name == name)

    if regex:
        re_filter = re.compile(regex)
        return sorted(pi for pi in info_map if re.match(re_filter, str(pi)))

    return sorted(info_map)



def collect_infos(param_element, is_type_param=False):
    """
    Collects parameters of the provided element.
    Args:
        param_element: Element that holds the parameters.
    Returns:
        Returns a dictionary, with parameters.
    """

    parameters = param_element.Parameters
    param_infos = []

    for param in parameters:
        param_value = get_val(None, None, param)

        param_info = ParamInfo(
            is_type_param,
            param.Definition.Name,
            param_value,
            param.StorageType,
            param.HasValue,
            param.IsShared,
            param.IsReadOnly,
            param,
        )
        param_infos.append(param_info)

    return param_infos


def get_val(elem, param_name, param=None):
    """
    Retrieves parameter value of element or parameter
    or its standard empty value for its type.
    :param elem: the element holding the parameter
    :param param_name: name of the parameter
    :param param: optionally the param instead of elem
    :return: value of the parameter or empty of type
    """
    if not param:
        param = elem.LookupParameter(param_name)
    if param:
        dtype = param.StorageType
        if param.HasValue:
            return dtype_methods[dtype](param)
        return dtype_empty[dtype]


def set_val(elem, param_name, value, param=None):
    """
    Sets parameter value of element or parameter.
    :param elem:
    :param param_name:
    :param value:
    :param param:
    :return:
    """
    if not param:
        param = elem.LookupParameter(param_name)
    if param:
        param.Set(value)
    else:
        print("param not found: {}".format(param_name))


dtype_methods = {
    DB.StorageType.String   : DB.Parameter.AsString,
    DB.StorageType.Integer  : DB.Parameter.AsDouble,
    DB.StorageType.Double   : DB.Parameter.AsDouble,
    DB.StorageType.ElementId: DB.Parameter.AsElementId,
}
dtype_empty = {
    DB.StorageType.String : "",
    DB.StorageType.Integer: 0,
    DB.StorageType.Double : 0.0,
    DB.StorageType.ElementId: DB.ElementId(-1),
}

ParamInfo = namedtuple("ParamInfo", "type_param name value dtype has_value shared read_only param")
TITLE_INST_PARAMS = "INSTANCE PARAMETERS" + 50 * "_"
TITLE_TYPE_PARAMS = "TYPE PARAMETERS    " + 50 * "_"

