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

# =================================================================================================
#   IMPORTS
# =================================================================================================

from pathlib import Path


from ambiance import Atmosphere
from ceasiompy.ModuleTemplate.func.subfunc import my_subfunc
from ceasiompy.utils.ceasiomlogger import get_logger
from ceasiompy.utils.moduleinterfaces import (
    check_cpacs_input_requirements,
    get_toolinput_file_path,
    get_tooloutput_file_path,
)
from ceasiompy.utils.commonxpath import FUSELAGES_XPATH
from cpacspy.cpacsfunctions import (
    add_float_vector,
    add_string_vector,
    add_uid,
    copy_branch,
    create_branch,
    get_float_vector,
    get_string_vector,
    get_tigl_configuration,
    get_uid,
    get_value,
    get_value_or_default,
    get_xpath_parent,
    open_tigl,
    open_tixi,
)

# new imports
import sys

import openmdao.api as om

import pycycle.api as pyc

log = get_logger()

MODULE_DIR = Path(__file__).parent
MODULE_NAME = MODULE_DIR.name


# =================================================================================================
#   CLASSES
# =================================================================================================


# =================================================================================================
#   FUNCTIONS
# =================================================================================================


# =================================================================================================
#    MAIN
# =================================================================================================


def main(cpacs_path, cpacs_out_path):

    log.info("----- Start of " + MODULE_NAME + " -----")

    check_cpacs_input_requirements(cpacs_path)

    # Define other inputs value
    my_value1 = 6
    my_value2 = 5.5

    # Call 'sum_function'
    my_total = sum_funcion(my_value1, my_value2)
    log.info("My total is equal to: " + str(my_total))

    # Call a function which use CPACS inputs
    x, y, z = get_fuselage_scaling(cpacs_path, cpacs_out_path)
    log.info("Value x,y,z as been calculated")
    log.info("x = " + str(x))
    log.info("y = " + str(y))
    log.info("z = " + str(z))

    log.info("----- End of " + MODULE_NAME + " -----")


if __name__ == "__main__":

    cpacs_path = get_toolinput_file_path(MODULE_NAME)
    cpacs_out_path = get_tooloutput_file_path(MODULE_NAME)

    main(cpacs_path, cpacs_out_path)
