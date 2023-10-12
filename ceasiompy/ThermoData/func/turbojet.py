"""
CEASIOMpy: Conceptual Aircraft Design Software

Developed by CFS ENGINEERING, 1015 Lausanne, Switzerland

Small description of the script

Python version: >=3.8

| Author: Name
| Creation: YEAR-MONTH-DAY

TODO:

    * Things to improve ...
    * Things to add ...

"""


# ==============================================================================
#   IMPORTS
# ==============================================================================

from ceasiompy.utils.ceasiomlogger import get_logger

from pathlib import Path

from ambiance import Atmosphere
from ceasiompy.utils.ceasiomlogger import get_logger
from ceasiompy.utils.ceasiompyutils import get_results_directory
from ceasiompy.utils.commonxpath import (
    CLCALC_XPATH,
    MASSBREAKDOWN_XPATH,
    REF_XPATH,
    SU2_FIXED_CL_XPATH,
    SU2_TARGET_CL_XPATH,
    SU2_XPATH,
    RANGE_XPATH,
)
from ceasiompy.utils.moduleinterfaces import (
    check_cpacs_input_requirements,
    get_toolinput_file_path,
    get_tooloutput_file_path,
)
from cpacspy.cpacsfunctions import create_branch, get_value, get_value_or_default
from cpacspy.cpacspy import CPACS
from markdownpy.markdownpy import MarkdownDoc


import sys

import openmdao.api as om

import pycycle.api as pyc

log = get_logger()


MODULE_DIR = Path(__file__).parent
MODULE_NAME = MODULE_DIR.name
cpacs_path = get_toolinput_file_path(MODULE_NAME)
cpacs = CPACS(cpacs_path)
tixi = cpacs.tixi

altitude_path = RANGE_XPATH + "/cruiseAltitude"
mach_path = RANGE_XPATH + "/cruiseMach"

cruise_alt = get_value_or_default(tixi, altitude_path, 12000.0)

cruise_mach = get_value_or_default(tixi, mach_path, 0.78)


# ==============================================================================
#   CLASSES
# ==============================================================================


# ==============================================================================
#   FUNCTIONS
# ==============================================================================


def simple_turbojet(Mach, Alt, Fn):

    """Function to calculate ...
    Function to calculate output variables of interest from a simple turbojet

    Source:
       * Reference paper or book, with author and date

    Args:
        Mach (float):  Argument 1 [adim]
        Alt (float): Argument 2 [feet]
        Fn (float): Argument 3 [lbf]

    Returns:
        P_out_nozzle: Return 1 [psi]
        T_out_nozzle: Return 2 [degr]
        V_out_nozzle: Return 3 []

    .. warning::

        Example of warning
    """

    return (T_out_nozzle, Mach_out_nozzle)


# ==============================================================================
#    MAIN
# ==============================================================================


if __name__ == "__main__":

    print("Nothing to execute!")
