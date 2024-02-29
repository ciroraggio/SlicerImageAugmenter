#-----------------------------------------------------------------------------
set(MODULE_NAME SlicerAugmentator)

#-----------------------------------------------------------------------------
set(MODULE_PYTHON_SCRIPTS
  ${MODULE_NAME}.py
  ${MODULE_NAME}Lib/SlicerAugmentatorDataset.py
  ${MODULE_NAME}Lib/SlicerAugmentatorValidator.py
  ${MODULE_NAME}Lib/SlicerAugmentatorUtils.py
  ${MODULE_NAME}Lib/SlicerAugmentatorTransformationParser.py
  ${MODULE_NAME}Lib/SlicerAugmentatorIntensity.py
  ${MODULE_NAME}Lib/SlicerAugmentatorSpatial.py
  )

set(MODULE_PYTHON_RESOURCES
  Resources/Icons/${MODULE_NAME}.png
  Resources/UI/${MODULE_NAME}.ui
  )

#-----------------------------------------------------------------------------
slicerMacroBuildScriptedModule(
  NAME ${MODULE_NAME}
  SCRIPTS ${MODULE_PYTHON_SCRIPTS}
  RESOURCES ${MODULE_PYTHON_RESOURCES}
  WITH_GENERIC_TESTS
  )

#-----------------------------------------------------------------------------
if(BUILD_TESTING)

  # Register the unittest subclass in the main script as a ctest.
  # Note that the test will also be available at runtime.
  slicer_add_python_unittest(SCRIPT ${MODULE_NAME}.py)

  # Additional build-time testing
  add_subdirectory(Testing)
endif()
