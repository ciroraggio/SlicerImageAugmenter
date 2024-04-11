import slicer
from typing import Dict, List
try:
    from monai.transforms import ScaleIntensity, RandScaleIntensityd, AdjustContrast, RandAdjustContrastd, RandGaussianNoised, ShiftIntensity, RandShiftIntensityd, NormalizeIntensity, ThresholdIntensity, MedianSmooth, GaussianSmooth, RandGaussianSmoothd
    from munch import Munch, munchify
except ModuleNotFoundError:
    slicer.util.pip_install("monai[itk]")
    slicer.util.pip_install("munch")
    from monai.transforms import ScaleIntensity, RandScaleIntensityd, AdjustContrast, RandAdjustContrastd, RandGaussianNoised, ShiftIntensity, RandShiftIntensityd, NormalizeIntensity, ThresholdIntensity, MedianSmooth, GaussianSmooth, RandGaussianSmoothd
    from munch import Munch, munchify

from SlicerAugmentatorLib.SlicerAugmentatorTransformControllerInterface import SlicerAugmentatorTransformControllerInterface

class SlicerAugmentatorIntensityController(SlicerAugmentatorTransformControllerInterface):
    def __init__(self, ui, mappedTransformations: List[object], dictKeys: Dict[str, str]) -> None:
        self.ui = ui
        self.transformations: Munch = munchify(self.getTransformations())
        self.mappedTransformations: List[object] = mappedTransformations
        self.dictKeys: Dict[str, str] = dictKeys

    def getTransformations(self) -> Dict[str, Dict]:
        return {
            "scaleIntensity": {
                "enabled": self.ui.scaleIntensityEnabled.isChecked(),
                "factor": self.ui.scaleIntensityFactor.text,
            },
            "randomScaleIntensity": {
                "enabled": self.ui.randomScaleIntensityEnabled.isChecked(),
                "factorFrom": self.ui.randomScaleIntensityFactorFrom.text,
                "factorTo": self.ui.randomScaleIntensityFactorTo.text,
            },
            "adjustContrast": {
                "enabled": self.ui.adjustContrastEnabled.isChecked(),
                "gamma": self.ui.adjustContrastGamma.text,
                "invertImage": self.ui.adjustContrastInvertImage.isChecked(),
            },
            "randomAdjustContrast": {
                "enabled": self.ui.randomAdjustContrastEnabled.isChecked(),
                "gammaFrom": self.ui.randomAdjustContrastGammaFrom.text,
                "gammaTo": self.ui.randomAdjustContrastGammaTo.text,
                "invertImage": self.ui.randomAdjustContrastInvertImage.isChecked(),
            },
            "randomGaussianNoise": {
                "enabled": self.ui.randomGaussianNoiseEnabled.isChecked(),
                "mean": self.ui.randomGaussianNoiseMean.text,
                "std": self.ui.randomGaussianNoiseStd.text,
            },
            "shiftIntensity": {
                "enabled": self.ui.shiftIntensityEnabled.isChecked(),
                "offset": self.ui.shiftIntensityOffset.text,
            },
            "randomShiftIntensity": {
                "enabled": self.ui.randomShiftIntensityEnabled.isChecked(),
                "offsetFrom": self.ui.randomShiftIntensityFrom.text,
                "offsetTo": self.ui.randomShiftIntensityTo.text,
            },
            "normalizeIntensity": {
                "enabled": self.ui.normalizeIntensityEnabled.isChecked(),
                "subtrahend": self.ui.normalizeIntensitySubtrahend.text,
                "divisor": self.ui.normalizeIntensityDivisor.text,
                "nonZero": self.ui.normalizeIntensityNonZero.isChecked(),
            },
            "thresholdIntensity": {
                "enabled": self.ui.thresholdIntensityEnabled.isChecked(),
                "thresholdValue": self.ui.thresholdIntensityValue.text,
                "cVal": self.ui.thresholdIntensityCVal.text,
                "above": self.ui.thresholdIntensityAbove.isChecked(),
            },
            "medianSmooth": {
                "enabled": self.ui.medianSmoothEnabled.isChecked(),
                "radius": self.ui.medianSmoothRadius.text,
            },
            "gaussianSmooth": {
                "enabled": self.ui.gaussianSmoothEnabled.isChecked(),
                "sigma": self.ui.gaussianSmoothSigma.text,
                "kernel": self.ui.gaussianSmoothKernelType.currentText,
            },
            "randGaussianSmooth": {
                "enabled": self.ui.randGaussianSmoothEnabled.isChecked(),
                "sigmaFromX": self.ui.randGaussianSmoothSigmaXFrom.text,
                "sigmaToX": self.ui.randGaussianSmoothSigmaXTo.text,
                "sigmaFromY": self.ui.randGaussianSmoothSigmaYFrom.text,
                "sigmaToY": self.ui.randGaussianSmoothSigmaYTo.text,
                "sigmaFromZ": self.ui.randGaussianSmoothSigmaZFrom.text,
                "sigmaToZ": self.ui.randGaussianSmoothSigmaZTo.text,
                "kernel": self.ui.randGaussianSmoothKernelType.currentText,
            },
        }

    def mapTransformations(self) -> List[object]:
        if (self.transformations.scaleIntensity.enabled):
            if (self.transformations.scaleIntensity.factor == ""):
                raise ValueError(
                    "The 'Scale Intensity' transformation is enabled but factor is not specified")

            self.mappedTransformations.append(ScaleIntensity(
                factor=(float(self.transformations.scaleIntensity.factor))))

        if (self.transformations.randomScaleIntensity.enabled):
            if (self.transformations.randomScaleIntensity.factorFrom == "" or self.transformations.randomScaleIntensity.factorTo == ""):
                raise ValueError(
                    "The 'Randomd Scale Intensity' transformation is enabled but factors are not specified")

            self.mappedTransformations.append(RandScaleIntensityd(prob=1,
                                                                  factors=(float(self.transformations.randomScaleIntensity.factorFrom),
                                                                           float(self.transformations.randomScaleIntensity.factorTo)),
                                                                  keys=self.dictKeys,
                                                                  allow_missing_keys=True
                                                                  ))

        if (self.transformations.adjustContrast.enabled):
            if (self.transformations.adjustContrast.gamma == ""):
                raise ValueError(
                    "The 'Adjust Contrast' transformation is enabled but gamma value is not specified")

            self.mappedTransformations.append(AdjustContrast(gamma=(float(self.transformations.adjustContrast.gamma)),
                                                             invert_image=self.transformations.adjustContrast.invertImage,
                                                             retain_stats=True
                                                             )
                                              )

        if (self.transformations.randomAdjustContrast.enabled):
            if (self.transformations.randomAdjustContrast.gammaFrom == "" or self.transformations.randomAdjustContrast.gammaTo == ""):
                raise ValueError(
                    "The 'Random Adjust Contrast' transformation is enabled but gamma values are not specified")

            self.mappedTransformations.append(RandAdjustContrastd(prob=1,
                                                                  gamma=(float(self.transformations.randomAdjustContrast.gammaFrom), float(
                                                                      self.transformations.randomAdjustContrast.gammaTo)),
                                                                  invert_image=self.transformations.randomAdjustContrast.invertImage,
                                                                  retain_stats=True,
                                                                  keys=self.dictKeys,
                                                                  allow_missing_keys=True
                                                                  )
                                              )
        if (self.transformations.randomGaussianNoise.enabled):
            mean = float(self.transformations.randomGaussianNoise.mean) if (
                self.transformations.randomGaussianNoise.mean != "") else 0.0
            std = float(self.transformations.randomGaussianNoise.std) if (
                self.transformations.randomGaussianNoise.std != "") else 0.1
            self.mappedTransformations.append(RandGaussianNoised(prob=1,
                                                                 mean=mean,
                                                                 std=std,
                                                                 keys=self.dictKeys,
                                                                 allow_missing_keys=True))

        if (self.transformations.shiftIntensity.enabled):
            if (self.transformations.shiftIntensity.offset == ""):
                raise ValueError(
                    "The 'Shift Intensity' transformation is enabled but offset value is not specified")

            self.mappedTransformations.append(ShiftIntensity(
                offset=float(self.transformations.shiftIntensity.offset)))

        if (self.transformations.randomShiftIntensity.enabled):
            if (self.transformations.randomShiftIntensity.offsetFrom == "" or self.transformations.randomShiftIntensity.offsetTo == ""):
                raise ValueError(
                    "The 'Random Shift Intensity' transformation is enabled but offsets values are not specified")

            self.mappedTransformations.append(RandShiftIntensityd(prob=1,
                                                                  offsets=(float(
                                                                      self.transformations.randomShiftIntensity.offsetFrom, self.transformations.randomShiftIntensity.offsetTo)),
                                                                  keys=self.dictKeys,
                                                                  allow_missing_keys=True))

        if (self.transformations.normalizeIntensity.enabled):
            if (self.transformations.normalizeIntensity.subtrahend == "" or self.transformations.normalizeIntensity.divisor == ""):
                raise ValueError(
                    "The 'Normalize Intensity' transformation is enabled but values are not specified")

            self.mappedTransformations.append(NormalizeIntensity(subtrahend=float(self.transformations.normalizeIntensity.subtrahend),
                                                                 divisor=float(
                                                                     self.transformations.normalizeIntensity.divisor),
                                                                 nonzero=self.transformations.normalizeIntensity.nonZero))

        if (self.transformations.thresholdIntensity.enabled):
            if (self.transformations.thresholdIntensity.thresholdValue == ""):
                raise ValueError(
                    "The 'Threshold Intensity' transformation is enabled but threshold value are not specified")

            cVal = float(
                self.transformations.thresholdIntensity.cVal) if self.transformations.thresholdIntensity.cVal else 0.0
            self.mappedTransformations.append(ThresholdIntensity(threshold=float(
                self.transformations.thresholdIntensity.thresholdValue), cval=cVal, above=self.transformations.thresholdIntensity.above))

        if (self.transformations.medianSmooth.enabled):
            radius = float(
                self.transformations.medianSmooth.radius) if self.transformations.medianSmooth.radius else 1
            self.mappedTransformations.append(MedianSmooth(radius=radius))

        if (self.transformations.gaussianSmooth.enabled):
            sigma = float(
                self.transformations.gaussianSmooth.sigma) if self.transformations.gaussianSmooth.sigma else 1
            self.mappedTransformations.append(GaussianSmooth(
                sigma=sigma, approx=self.transformations.gaussianSmooth.kernel))

        if (self.transformations.randGaussianSmooth.enabled):
            sigmaX, sigmaY, sigmaZ = [0, 0], [0, 0], [0, 0]

            try:
                if (self.transformations.randGaussianSmooth.sigmaFromX != "" and self.transformations.randGaussianSmooth.sigmaToX != ""):
                    sigmaX = [float(self.transformations.randGaussianSmooth.sigmaFromX), float(
                        self.transformations.randGaussianSmooth.sigmaToX)]
                if (self.transformations.randGaussianSmooth.sigmaFromY != "" and self.transformations.randGaussianSmooth.sigmaToY != ""):
                    sigmaY = [float(self.transformations.randGaussianSmooth.sigmaFromY), float(
                        self.transformations.randGaussianSmooth.sigmaToY)]
                if (self.transformations.randGaussianSmooth.sigmaFromZ != "" and self.transformations.randGaussianSmooth.sigmaToZ != ""):
                    sigmaZ = [float(self.transformations.randGaussianSmooth.sigmaFromZ), float(
                        self.transformations.randGaussianSmooth.sigmaToZ)]

                self.mappedTransformations.append(RandGaussianSmoothd(prob=1,
                                                                      sigma_x=sigmaX,
                                                                      sigma_y=sigmaY,
                                                                      sigma_z=sigmaZ,
                                                                      approx=self.transformations.randGaussianSmooth.kernel,
                                                                      keys=self.dictKeys,
                                                                      allow_missing_keys=True))
            except Exception as e:
                raise ValueError(e)

        return self.mappedTransformations
