#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .component import FormattedComponent
from .device import Device
from .iocadmin import IocAdmin


class IocDevice(Device):
    """
    Device that has an IOC that we can check and manipulate over EPICS
    """
    ioc = FormattedComponent(IocAdmin, "{self._iocadmin}")

    def __init__(self, prefix, *, ioc="", read_attrs=None, name=None,
                 **kwargs):
        self._iocadmin = ioc
        super().__init__(prefix, read_attrs=read_attrs, name=name, **kwargs)
