#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ceasiompy.utils.ceasiompyutils import get_reasonable_nb_cpu
from ceasiompy.utils.moduleinterfaces import CPACSInOut
from ceasiompy.utils.commonxpath import CEASIOMPY_XPATH, REF_XPATH, SU2_XPATH


# ===== CPACS inputs and outputs =====

cpacs_inout = CPACSInOut()

# ----- Input -----

cpacs_inout.add_input(
    var_name="nb_proc",
    var_type=int,
    default_value=get_reasonable_nb_cpu(),
    unit="1",
    descr="Number of proc to use to run SU2",
    xpath=SU2_XPATH + "/settings/nbProc",
    gui=True,
    gui_name="Nb of processor",
    gui_group="CPU",
)

cpacs_inout.add_input(
    var_name="su2_mesh_path",
    var_type="pathtype",
    default_value="-",
    unit="1",
    descr="Absolute path of the SU2 mesh",
    xpath=CEASIOMPY_XPATH + "/filesPath/su2Mesh",
    gui=True,
    gui_name="SU2 Mesh",
    gui_group="Inputs",
)

cpacs_inout.add_input(
    var_name="control_surf",
    var_type=bool,
    default_value=False,
    unit="1",
    descr="To check if control surfaces deflections should be calculated or not",
    xpath=SU2_XPATH + "/options/clalculateCotrolSurfacesDeflections",
    gui=True,
    gui_name="Control Surfaces",
    gui_group="Inputs",
)

# TODO: add TED,deflection and symetry selection

cpacs_inout.add_input(
    var_name="ref_len",
    var_type=float,
    default_value=None,
    unit="m",
    descr="Reference length of the aircraft",
    xpath=REF_XPATH + "/length",
    gui=False,
    gui_name=None,
    gui_group=None,
)

cpacs_inout.add_input(
    var_name="ref_area",
    var_type=float,
    default_value=None,
    unit="m^2",
    descr="Reference area of the aircraft",
    xpath=REF_XPATH + "/area",
    gui=False,
    gui_name=None,
    gui_group=None,
)

for direction in ["x", "y", "z"]:
    cpacs_inout.add_input(
        var_name=f"ref_ori_moment_{direction}",
        var_type=float,
        default_value=0.0,
        unit="m",
        descr=f"Fuselage scaling on {direction} axis",
        xpath=REF_XPATH + f"/point/{direction}",
        gui=False,
        gui_name=None,
        gui_group=None,
    )


# ----- Output -----

# TODO: add it or not?
# cpacs_inout.add_output(
#     var_name='wetted_area',
#     var_type=float,
#     default_value=None,
#     unit='m^2',
#     descr='Aircraft wetted area calculated by SU2',
#     xpath=CEASIOMPY_XPATH + '/geometry/analyses/wettedArea',
# )

cpacs_inout.add_output(
    var_name="su2_def_mesh_list",
    var_type=list,
    default_value=None,
    unit="1",
    descr="List of SU2 deformed meshes generated by SU2MeshDef",
    xpath=SU2_XPATH + "/availableDeformedMesh",
)

cpacs_inout.add_output(
    var_name="bc_wall_list",
    var_type=list,
    default_value=None,
    unit="1",
    descr="Wall boundary conditions found in the SU2 mesh",
    xpath=SU2_XPATH + "/boundaryConditions/wall",
)
