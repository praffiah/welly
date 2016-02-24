#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Defines wells.

:copyright: 2016 Agile Geoscience
:license: Apache 2.0
"""
import lasio

from . import utils
from .curve import Curve
from .header import Header
from .location import Location


class WellError(Exception):
    """
    Generic error class.
    """
    pass


class Well(object):
    """
    Well contains everything about the well.
    """
    def __init__(self, params):
        """
        Generic initializer for now.
        """
        for k, v in params.items():
            if k and v:
                setattr(self, k, v)

    @classmethod
    def from_lasio_well(cls, l):
        """
        If you already have the lasio object.
        """
        # Build a dict of curves.
        start = utils.lasio_get(l, 'well', 'STRT', 'value')
        step = utils.lasio_get(l, 'well', 'STEP', 'value')
        run = utils.lasio_get(l, 'params', 'RUN', 'value')
        null = utils.lasio_get(l, 'well', 'NULL', 'value')
        curves = {c.mnemonic: Curve.from_lasio_curve(c,
                                                     start=start,
                                                     step=step,
                                                     run=run,
                                                     null=null,
                                                     )
                  for c in l.curves}

        # Build a dict of the other well data.
        params = {}
        params = {'las': l,
                  'header': Header.from_lasio_well(l.well),
                  'location': Location.from_lasio_well(l.well),
                  'curves': curves,
                  }

        # Pass into __init__() to instatiate the object.
        return cls(params)

    @classmethod
    def from_las(cls, fname):
        """
        Wraps lasio.
        """
        l = lasio.read(fname)

        # Pass to other constructor.
        return cls.from_lasio_well(l)