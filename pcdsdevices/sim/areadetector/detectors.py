#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########
# Module #
##########
from .cam import (CamBase, PulnixCam)
from .plugins import (StatsPlugin, ImagePlugin)
from ..component import Component
from ...epics.areadetector import detectors


class DetectorBase(detectors.DetectorBase):
    pass


class PulnixDetector(detectors.PulnixDetector, DetectorBase):
    cam = Component(PulnixCam, ":")

class SimDetector(detectors.DetectorBase):
    """
    Generic simulated detector that has image, stats and cam components.
    """
    cam = Component(CamBase, ":")
    image = Component(ImagePlugin, ":IMAGE:", read_attrs=["array_data"])
    stats = Component(StatsPlugin, ":Stats:", read_attrs=['centroid',
                                                          'mean_value'])

    def __init__(self, prefix, read_attrs=None, *args, **kwargs):
        if read_attrs is None:
            read_attrs = ["cam", "image", "stats"]
        super().__init__(prefix, read_attrs=read_attrs, *args, **kwargs)
    
    def centroid_x(self):
        return self.stats.centroid.x.value
    
    def centroid_y(self):
        return self.stats.centroid.y.value

    @property
    def centroid(self):
        return (self.centroid_x, self.centroid_y)
    
