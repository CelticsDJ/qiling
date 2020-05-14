#!/usr/bin/env python3
#
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
# Built on top of Unicorn emulator (www.unicorn-engine.org)

import struct
import time
from qiling.os.windows.const import *
from qiling.os.const import *
from qiling.os.fncc import *
from qiling.os.windows.utils import *
from qiling.os.windows.thread import *
from qiling.os.windows.handle import *
from qiling.exception import *


# BOOL DuplicateHandle(
#   HANDLE   hSourceProcessHandle,
#   HANDLE   hSourceHandle,
#   HANDLE   hTargetProcessHandle,
#   LPHANDLE lpTargetHandle,
#   DWORD    dwDesiredAccess,
#   BOOL     bInheritHandle,
#   DWORD    dwOptions
# );
@winapi(cc=STDCALL, params={
    "hSourceProcessHandle": POINTER,
    "hSourceHandle": POINTER,
    "hTargetProcessHandle": POINTER,
    "lpTargetHandle": POINTER,
    "dwDesiredAccess": DWORD,
    "bInheritHandle": BOOL,
    "dwOptions": DWORD
})
def hook_DuplicateHandle(ql, address, params):
    # TODO for how we manage handle, i think this doesn't work
    content = params["hSourceHandle"]
    dst = params["lpTargetHandle"]
    ql.mem.write(dst, content.to_bytes(length=ql.pointersize, byteorder='little'))
    return 1


# BOOL CloseHandle(
#   HANDLE hObject
# );
@winapi(cc=STDCALL, params={
    "hObject": HANDLE
})
def hook_CloseHandle(ql, address, params):
    value = params["hObject"]
    handle = ql.os.handle_manager.get(value)
    if handle is None:
        ql.os.last_error = ERROR_INVALID_HANDLE
        return 0
    return 1
