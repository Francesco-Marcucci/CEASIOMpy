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

# XPath definition

# ref_area_xpath = REF_XPATH + "/area"
# cruise_alt_xpath = CLCALC_XPATH + "/cruiseAltitude"
# cruise_mach_xpath = CLCALC_XPATH + "/cruiseMach"


def thermo_data_run(cpacs_path, cpacs_out_path, wkdir):

    if not wkdir.exists():
        raise OSError(f"The working directory : {wkdir} does not exit!")

    cpacs = CPACS(cpacs_path)
    tixi = cpacs.tixi

    # MN = get_value_or_default(tixi, RANGE_XPATH + "/cruiseMach", 0.3)
    Fn = get_value_or_default(tixi, RANGE_XPATH + "/NetForce", 2000)

    aeromap_list = cpacs.get_aeromap_uid_list()

    if aeromap_list:
        aeromap_default = aeromap_list[0]
        log.info(f"The aeromap is {aeromap_default}")
        aeromap_uid = get_value_or_default(
            cpacs.tixi, SU2_AEROMAP_UID_XPATH, aeromap_default
        )
        activate_aeromap = cpacs.get_aeromap_by_uid(aeromap_uid)
        alt_list = activate_aeromap.get("altitude").tolist()
        mach_list = activate_aeromap.get("machNumber").tolist()
        alt = alt_list[0]
        MN = mach_list[0]

    EngineBC = Path(wkdir, ENGINE_BOUNDARY_CONDITIONS)

    f = open(EngineBC, "w")

    engine_type = get_value_or_default(tixi, ENGINE_TYPE_XPATH, 0)
    create_branch(cpacs.tixi, ENGINE_BC)
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

        tixi.updateDoubleElement(ENGINE_BC + "/temperatureOutlet", T_tot_out, "%g")
        tixi.updateDoubleElement(ENGINE_BC + "/pressureOutlet", P_tot_out, "%g")

        f = write_turbojet_file(
            file=f,
            T_tot_out=T_tot_out,
            V_stat_out=V_stat_out,
            MN_out=MN_out,
            P_tot_out=P_tot_out,
            massflow_stat_out=massflow_stat_out,
            T_stat_out=T_stat_out,
            P_stat_out=P_stat_out,
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

        tixi.updateDoubleElement(ENGINE_BC + "/temperatureOutlet", T_tot_out_core, "%g")
        tixi.updateDoubleElement(ENGINE_BC + "/pressureOutlet", P_tot_out_core, "%g")

        f = write_hbtf_file(
            file=f,
            T_tot_out_byp=T_tot_out_byp,
            V_stat_out_byp=V_stat_out_byp,
            MN_out_byp=MN_out_byp,
            P_tot_out_byp=P_tot_out_byp,
            massflow_stat_out_byp=massflow_stat_out_byp,
            T_stat_out_byp=T_stat_out_byp,
            T_tot_out_core=T_tot_out_core,
            V_stat_out_core=V_stat_out_core,
            MN_out_core=MN_out_core,
            P_tot_out_core=P_tot_out_core,
            massflow_stat_out_core=massflow_stat_out_core,
            T_stat_out_core=T_stat_out_core,
        )

    cpacs.save_cpacs(cpacs_out_path, overwrite=True)
