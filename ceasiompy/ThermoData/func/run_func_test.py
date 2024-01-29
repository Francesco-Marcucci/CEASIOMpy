from pathlib import Path

from ceasiompy.ThermoData.func.turbofan_func import (
    turbofan_analysis,
    write_hbtf_file,
)

from ceasiompy.ThermoData.func.turbojet_func import (
    turbojet_analysis,
    write_turbojet_file,
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
    ENGINE_BC,
    RANGE_XPATH,
    SU2_AEROMAP_UID_XPATH,
)
from ceasiompy.utils.commonnames import (
    ENGINE_BOUNDARY_CONDITIONS,
    CONFIG_CFD_NAME,
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


def update_elements(tixi, parent_path, element_name, value):
    element_path = f"{parent_path}/{element_name}"
    if tixi.checkElement(element_path):
        tixi.updateDoubleElement(element_path, value, "%g")
    else:
        raise ValueError(
            f"Element '{element_name}' not found at path '{element_path}'."
        )


def thermo_data_run(cpacs_path, cpacs_out_path, wkdir):
    wkdir = Path(wkdir)
    if not wkdir.exists():
        raise OSError(f"The working directory: {wkdir} does not exist!")

    cpacs = CPACS(cpacs_path)
    tixi = cpacs.tixi
    Fn = get_value_or_default(tixi, RANGE_XPATH + "/NetForce", 2000)

    aeromap_list = cpacs.get_aeromap_uid_list()

    if aeromap_list:
        for aeromap_uid in aeromap_list:
            activate_aeromap = cpacs.get_aeromap_by_uid(aeromap_uid)
            alt_list, mach_list = (
                activate_aeromap.get("altitude").tolist(),
                activate_aeromap.get("machNumber").tolist(),
            )

            for case_nb, (alt, MN) in enumerate(zip(alt_list, mach_list)):
                case_dir_name = f"Aeromap{aeromap_uid}_Case{str(case_nb).zfill(2)}_alt{alt}_mach{round(MN, 2)}"
                case_dir_path = wkdir / case_dir_name

                if not case_dir_path.exists():
                    case_dir_path.mkdir()

                    EngineBC = case_dir_path / ENGINE_BOUNDARY_CONDITIONS
                    f = open(EngineBC, "w")

                    engine_type = get_value_or_default(tixi, ENGINE_TYPE_XPATH, 0)
                    create_branch(tixi, ENGINE_BC)
                    tixi.createElement(ENGINE_BC, "temperatureOutlet")
                    tixi.createElement(ENGINE_BC, "pressureOutlet")

                    if engine_type == 0:
                        (
                            T_tot_out,
                            V_stat_out,
                            MN_out,
                            P_tot_out,
                            massflow_stat_out,
                            T_stat_out,
                            P_stat_out,
                        ) = turbojet_analysis(alt, MN, Fn)

                        update_elements(tixi, ENGINE_BC, T_tot_out, P_tot_out)

                        f = write_turbojet_file(
                            f,
                            T_tot_out,
                            V_stat_out,
                            MN_out,
                            P_tot_out,
                            massflow_stat_out,
                            T_stat_out,
                            P_stat_out,
                        )

                    else:
                        (
                            T_tot_out_byp,
                            V_stat_out_byp,
                            MN_out_byp,
                            P_tot_out_byp,
                            massflow_stat_out_byp,
                            T_stat_out_byp,
                            T_tot_out_core,
                            V_stat_out_core,
                            MN_out_core,
                            P_tot_out_core,
                            massflow_stat_out_core,
                            T_stat_out_core,
                        ) = turbofan_analysis(alt, MN, Fn)

                        update_elements(tixi, ENGINE_BC, T_tot_out_core, P_tot_out_core)

                        f = write_hbtf_file(
                            f,
                            T_tot_out_byp,
                            V_stat_out_byp,
                            MN_out_byp,
                            P_tot_out_byp,
                            massflow_stat_out_byp,
                            T_stat_out_byp,
                            T_tot_out_core,
                            V_stat_out_core,
                            MN_out_core,
                            P_tot_out_core,
                            massflow_stat_out_core,
                            T_stat_out_core,
                        )

    cpacs.save_cpacs(cpacs_out_path, overwrite=True)
