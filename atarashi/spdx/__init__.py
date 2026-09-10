#!/usr/bin/env python3
"""Atarashi SPDX-License-Identifier detection: high-precision, abstains when absent.

SPDX-License-Identifier: GPL-2.0-only
"""
from atarashi.spdx.detector import SpdxMatch, detect

__all__ = ["detect", "SpdxMatch"]
