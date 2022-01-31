# ===================================================================
#
# Copyright (c) 2016, Legrandin <helderijs@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ===================================================================

import os
import sys


def pycryptodome_filename(dir_comps, filename):
    """Return the complete file name for the module

    dir_comps : list of string
        The list of directory names in the PyCryptodome package.
        The first element must be "Crypto".

    filename : string
        The filename (inclusing extension) in the target directory.
    """
    if dir_comps[0] != "Crypto":
        raise ValueError("Only available for modules under 'Crypto'")

    _, ext = os.path.splitext(filename)
    if hasattr(sys, 'frozen') and ext == ".pyd":
        # We're running from a py2exe installation - pyd files can't be loaded from within the zip. Instead, they are
        # added in the root folder with their path parts concatenated by periods (ex. Crypto/Cipher/_raw_ecb.pyd becomes
        # Crypto.Cipher/_raw_ecb.pyd).
        root_lib = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        dir_comps.append(filename)
        filename = ".".join(dir_comps)

        return os.path.join(root_lib, filename)

    dir_comps = list(dir_comps[1:]) + [filename]

    util_lib, _ = os.path.split(os.path.abspath(__file__))
    root_lib = os.path.join(util_lib, "..")

    return os.path.join(root_lib, *dir_comps)

