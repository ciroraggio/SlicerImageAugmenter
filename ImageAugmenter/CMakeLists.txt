#-----------------------------------------------------------------------------
set(MODULE_NAME ImageAugmenter)

#-----------------------------------------------------------------------------
set(MODULE_PYTHON_SCRIPTS
  ${MODULE_NAME}.py
  ${MODULE_NAME}Lib/ImageAugmenterDataset.py
  ${MODULE_NAME}Lib/ImageAugmenterValidator.py
  ${MODULE_NAME}Lib/ImageAugmenterUtils.py
  ${MODULE_NAME}Lib/ImageAugmenterTransformationParser.py
  ${MODULE_NAME}Lib/ImageAugmenterIntensity.py
  ${MODULE_NAME}Lib/ImageAugmenterSpatial.py
  ${MODULE_NAME}Lib/ImageAugmenterTransformControllerInterface.py
  ${MODULE_NAME}Lib/ImageAugmenterCrop.py
  ${MODULE_NAME}Lib/UI/ImageAugmenterPreviewDialog.py
  ${MODULE_NAME}Lib/UI/ImageAugmenterUIUtils.py
  )

set(MODULE_PYTHON_RESOURCES
  Resources/Icons/${MODULE_NAME}.png
  Resources/UI/${MODULE_NAME}.ui
  Resources/Icons/cog.png
  Resources/Icons/regex.png
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
