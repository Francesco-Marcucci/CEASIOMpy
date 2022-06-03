"""
CEASIOMpy: Conceptual Aircraft Design Software

Developed by CFS ENGINEERING, 1015 Lausanne, Switzerland

Test functions for 'ceasiompy/CPACS2GMSH/exportbrep.py'

Python version: >=3.7

| Author : Tony Govoni
| Creation: 2022-03-22

"""

# =================================================================================================
#   IMPORTS
# =================================================================================================

import shutil
from pathlib import Path
from unittest.mock import patch

import pytest
from ceasiompy.CPACS2GMSH.func.exportbrep import export_brep
from ceasiompy.utils.commonpaths import CPACS_FILES_PATH
from cpacspy.cpacspy import CPACS

MODULE_DIR = Path(__file__).parent
CPACS_IN_PATH = Path(CPACS_FILES_PATH, "simpletest_cpacs.xml")
CPACS_IN_SIMPLE_ENGINE_PATH = Path(CPACS_FILES_PATH, "simple_engine.xml")
TEST_OUT_PATH = Path(MODULE_DIR, "ToolOutput")


# =================================================================================================
#   CLASSES
# =================================================================================================


# =================================================================================================
#   FUNCTIONS
# =================================================================================================


def test_export_brep():
    """Test function for 'export_brep'"""

    if TEST_OUT_PATH.exists():
        shutil.rmtree(TEST_OUT_PATH)
    TEST_OUT_PATH.mkdir()

    cpacs = CPACS(CPACS_IN_PATH)

    export_brep(cpacs, TEST_OUT_PATH)

    brep_files = list(TEST_OUT_PATH.glob("*.brep"))
    brep_file_names = [brep_file.name for brep_file in brep_files]

    assert len(brep_files) == 3  # simpletest_cpacs.xml containt only 3 parts
    assert "Wing.brep" in brep_file_names
    assert "Wing_mirrored.brep" in brep_file_names
    assert "SimpleFuselage.brep" in brep_file_names

    # Erase brep file generated by the test
    for brep_file in brep_files:
        brep_file.unlink()

    with pytest.raises(FileNotFoundError):
        with patch("ceasiompy.CPACS2GMSH.func.exportbrep.export_shapes", return_value=True):
            export_brep(cpacs, TEST_OUT_PATH)


def test_export_brep_with_engine():

    if TEST_OUT_PATH.exists():
        shutil.rmtree(TEST_OUT_PATH)
    TEST_OUT_PATH.mkdir()

    cpacs = CPACS(CPACS_IN_SIMPLE_ENGINE_PATH)

    export_brep(cpacs, TEST_OUT_PATH)

    brep_files = list(TEST_OUT_PATH.glob("*.brep"))
    brep_file_names = [brep_file.name for brep_file in brep_files]

    assert len(brep_files) == 7  # simple_engine.xml containt 7 parts
    assert "Wing.brep" in brep_file_names
    assert "Wing_mirrored.brep" in brep_file_names
    assert "SimpleFuselage.brep" in brep_file_names
    assert "Pylon.brep" in brep_file_names
    assert "Pylon_mirrored.brep" in brep_file_names
    assert "SimpleEngine.brep" in brep_file_names
    assert "SimpleEngine_mirrored.brep" in brep_file_names

    # Erase brep file generated by the test
    for brep_file in brep_files:
        brep_file.unlink()

    with pytest.raises(FileNotFoundError):
        with patch("ceasiompy.CPACS2GMSH.func.exportbrep.export_shapes", return_value=True):
            export_brep(cpacs, TEST_OUT_PATH)


# =================================================================================================
#    MAIN
# =================================================================================================

if __name__ == "__main__":

    print("Test CPACS2GMSH")
    print("To run test use the following command:")
    print(">> pytest -v")
