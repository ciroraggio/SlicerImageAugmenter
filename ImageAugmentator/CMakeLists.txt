#-----------------------------------------------------------------------------
set(MODULE_NAME ImageAugmentator)

#-----------------------------------------------------------------------------
set(MODULE_PYTHON_SCRIPTS
  ${MODULE_NAME}.py
  ${MODULE_NAME}Lib/ImageAugmentatorDataset.py
  ${MODULE_NAME}Lib/ImageAugmentatorValidator.py
  ${MODULE_NAME}Lib/ImageAugmentatorUtils.py
  ${MODULE_NAME}Lib/ImageAugmentatorTransformationParser.py
  ${MODULE_NAME}Lib/ImageAugmentatorIntensity.py
  ${MODULE_NAME}Lib/ImageAugmentatorSpatial.py
  ${MODULE_NAME}Lib/ImageAugmentatorTransformControllerInterface.py
  ${MODULE_NAME}Lib/ImageAugmentatorCrop.py
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
