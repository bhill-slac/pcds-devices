#!/usr/bin/env python
# -*- coding: utf-8 -*-
from copy import deepcopy
from .signal import EpicsSignalRO
from .component import Component, FormattedComponent
from .iocdevice import IocDevice
from .iocadmin import IocAdminOld
from .state import InOutStatesIoc, InOutCCMStatesIoc, statesrecord_class


class PulsePicker(IocDevice):
    """
    Device that lets us pick which beam pulses reach the sample.
    """
    in_out = FormattedComponent(InOutStatesIoc, "{self._states}",
                                ioc="{self._states_ioc}")
    blade = Component(EpicsSignalRO, ":READ_DF", string=True)
    mode = Component(EpicsSignalRO, ":SE", string=True)
    ioc = deepcopy(IocDevice.ioc)
    ioc.cls = IocAdminOld

    def __init__(self, prefix, *, states="", ioc="", states_ioc="",
                 read_attrs=None, name=None, **kwargs):
        self._states = states
        self._states_ioc = states_ioc
        if read_attrs is None:
            read_attrs = ["mode", "blade", "in_out"]
        super().__init__(prefix, ioc=ioc, read_attrs=read_attrs, name=name,
                         **kwargs)

    def move_out(self):
        """
        Move the pulsepicker to the "out" position in y.
        """
        self.in_out.value = "OUT"

    def move_in(self):
        """
        Move the pulsepicker to the "in" position in y.
        """
        self.in_out.value = "IN"


class PulsePickerCCM(PulsePicker):
    """
    Device that lets us pick which beam pulses reach the sample.
    This is the version with a third position state in addition to IN and OUT,
    and that's the CCM state: IN but at the CCM offset.
    """
    in_out = deepcopy(PulsePicker.in_out)
    in_out.cls = InOutCCMStatesIoc

    def move_ccm(self):
        """
        Move the pulsepicker to the "ccm" position in y.
        """
        self.in_out.value = "CCM"


TempStates = statesrecord_class("TempStates", ":PINK", ":CCM", ":OUT",
                                has_ioc=True)


class PulsePickerPink(PulsePickerCCM):
    """
    Current state syntax that I plan to change
    """
    in_out = deepcopy(PulsePickerCCM.in_out)
    in_out.cls = TempStates

    def move_in(self):
        self.in_out.value = "PINK"
