"""
CEASIOMpy: Conceptual Aircraft Design Software

Developed by CFS ENGINEERING, 1015 Lausanne, Switzerland

Calculate outlet conditions fot turbojet and turbofan engines

| Author: Francesco Marcucci
| Creation: 2023
"""

# =================================================================================================
#   IMPORTS
# =================================================================================================

from pathlib import Path

from ceasiompy.ThermoData.func.ThermoDataRun import (
    ThermoData_run,
)

from ceasiompy.utils.ceasiomlogger import get_logger

from ceasiompy.utils.moduleinterfaces import (
    check_cpacs_input_requirements,
    get_toolinput_file_path,
    get_tooloutput_file_path,
)
from ceasiompy.utils.commonxpath import (
    REF_XPATH,
    CLCALC_XPATH,
    ENGINE_TYPE_XPATH,
)
from ceasiompy.utils.commonnames import (
    ENGINE_BOUNDARY_CONDITIONS,
)
from cpacspy.cpacsfunctions import (
    get_value_or_default,
)
from cpacspy.cpacsfunctions import create_branch, get_value, get_value_or_default
from cpacspy.cpacspy import CPACS
from markdownpy.markdownpy import MarkdownDoc
from ceasiompy.utils.ceasiompyutils import get_results_directory


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

    # current_dir = Path(case_dir_path, propeller_uid)
    # current_dir.mkdir()

    # EngineBC = Path(ENGINE_BOUNDARY_CONDITIONS)

    results_dir = get_results_directory("ThermoData")

    ThermoData_run(cpacs_path, cpacs_out_path, results_dir)

    log.info("----- End of " + MODULE_NAME + " -----")


if __name__ == "__main__":

    cpacs_path = get_toolinput_file_path(MODULE_NAME)
    cpacs_out_path = get_tooloutput_file_path(MODULE_NAME)

    main(cpacs_path, cpacs_out_path)
