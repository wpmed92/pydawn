# -*- coding: utf-8 -*-
#
# TARGET arch is: []
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes


class AsDictMixin:
    @classmethod
    def as_dict(cls, self):
        result = {}
        if not isinstance(self, AsDictMixin):
            # not a structure, assume it's already a python object
            return self
        if not hasattr(cls, "_fields_"):
            return result
        # sys.version_info >= (3, 5)
        # for (field, *_) in cls._fields_:  # noqa
        for field_tuple in cls._fields_:  # noqa
            field = field_tuple[0]
            if field.startswith('PADDING_'):
                continue
            value = getattr(self, field)
            type_ = type(value)
            if hasattr(value, "_length_") and hasattr(value, "_type_"):
                # array
                if not hasattr(type_, "as_dict"):
                    value = [v for v in value]
                else:
                    type_ = type_._type_
                    value = [type_.as_dict(v) for v in value]
            elif hasattr(value, "contents") and hasattr(value, "_type_"):
                # pointer
                try:
                    if not hasattr(type_, "as_dict"):
                        value = value.contents
                    else:
                        type_ = type_._type_
                        value = type_.as_dict(value.contents)
                except ValueError:
                    # nullptr
                    value = None
            elif isinstance(value, AsDictMixin):
                # other structure
                value = type_.as_dict(value)
            result[field] = value
        return result


class Structure(ctypes.Structure, AsDictMixin):

    def __init__(self, *args, **kwds):
        # We don't want to use positional arguments fill PADDING_* fields

        args = dict(zip(self.__class__._field_names_(), args))
        args.update(kwds)
        super(Structure, self).__init__(**args)

    @classmethod
    def _field_names_(cls):
        if hasattr(cls, '_fields_'):
            return (f[0] for f in cls._fields_ if not f[0].startswith('PADDING'))
        else:
            return ()

    @classmethod
    def get_type(cls, field):
        for f in cls._fields_:
            if f[0] == field:
                return f[1]
        return None

    @classmethod
    def bind(cls, bound_fields):
        fields = {}
        for name, type_ in cls._fields_:
            if hasattr(type_, "restype"):
                if name in bound_fields:
                    if bound_fields[name] is None:
                        fields[name] = type_()
                    else:
                        # use a closure to capture the callback from the loop scope
                        fields[name] = (
                            type_((lambda callback: lambda *args: callback(*args))(
                                bound_fields[name]))
                        )
                    del bound_fields[name]
                else:
                    # default callback implementation (does nothing)
                    try:
                        default_ = type_(0).restype().value
                    except TypeError:
                        default_ = None
                    fields[name] = type_((
                        lambda default_: lambda *args: default_)(default_))
            else:
                # not a callback function, use default initialization
                if name in bound_fields:
                    fields[name] = bound_fields[name]
                    del bound_fields[name]
                else:
                    fields[name] = type_()
        if len(bound_fields) != 0:
            raise ValueError(
                "Cannot bind the following unknown callback(s) {}.{}".format(
                    cls.__name__, bound_fields.keys()
            ))
        return cls(**fields)


class Union(ctypes.Union, AsDictMixin):
    pass



c_int128 = ctypes.c_ubyte*16
c_uint128 = c_int128
void = None
if ctypes.sizeof(ctypes.c_longdouble) == 16:
    c_long_double_t = ctypes.c_longdouble
else:
    c_long_double_t = ctypes.c_ubyte*16

def string_cast(char_pointer, encoding='utf-8', errors='strict'):
    value = ctypes.cast(char_pointer, ctypes.c_char_p).value
    if value is not None and encoding is not None:
        value = value.decode(encoding, errors=errors)
    return value


def char_pointer_cast(string, encoding='utf-8'):
    if encoding is not None:
        try:
            string = string.encode(encoding)
        except AttributeError:
            # In Python3, bytes has no encode attribute
            pass
    string = ctypes.c_char_p(string)
    return ctypes.cast(string, ctypes.POINTER(ctypes.c_char))

from pathlib import Path

_libraries = {}
root_project_path = Path(__file__).resolve().parent
dll_path = root_project_path / 'lib' / 'libwebgpu_dawn.so'

vulkan = ctypes.CDLL('/usr/lib/x86_64-linux-gnu/libvulkan.so.1', mode=ctypes.RTLD_GLOBAL)
_libraries['libwebgpu_dawn.so'] = ctypes.CDLL(str(dll_path))

class FunctionFactoryStub:
    def __getattr__(self, _):
      return ctypes.CFUNCTYPE(lambda y:y)

# libraries['FIXME_STUB'] explanation
# As you did not list (-l libraryname.so) a library that exports this function
# This is a non-working stub instead. 
# You can either re-run clan2py with -l /path/to/library.so
# Or manually fix this by comment the ctypes.CDLL loading
_libraries['FIXME_STUB'] = FunctionFactoryStub() #  ctypes.CDLL('FIXME_STUB')


WGPUFlags = ctypes.c_uint32
WGPUBool = ctypes.c_uint32
class struct_WGPUAdapterImpl(Structure):
    pass

WGPUAdapter = ctypes.POINTER(struct_WGPUAdapterImpl)
class struct_WGPUBindGroupImpl(Structure):
    pass

WGPUBindGroup = ctypes.POINTER(struct_WGPUBindGroupImpl)
class struct_WGPUBindGroupLayoutImpl(Structure):
    pass

WGPUBindGroupLayout = ctypes.POINTER(struct_WGPUBindGroupLayoutImpl)
class struct_WGPUBufferImpl(Structure):
    pass

WGPUBuffer = ctypes.POINTER(struct_WGPUBufferImpl)
class struct_WGPUCommandBufferImpl(Structure):
    pass

WGPUCommandBuffer = ctypes.POINTER(struct_WGPUCommandBufferImpl)
class struct_WGPUCommandEncoderImpl(Structure):
    pass

WGPUCommandEncoder = ctypes.POINTER(struct_WGPUCommandEncoderImpl)
class struct_WGPUComputePassEncoderImpl(Structure):
    pass

WGPUComputePassEncoder = ctypes.POINTER(struct_WGPUComputePassEncoderImpl)
class struct_WGPUComputePipelineImpl(Structure):
    pass

WGPUComputePipeline = ctypes.POINTER(struct_WGPUComputePipelineImpl)
class struct_WGPUDeviceImpl(Structure):
    pass

WGPUDevice = ctypes.POINTER(struct_WGPUDeviceImpl)
class struct_WGPUExternalTextureImpl(Structure):
    pass

WGPUExternalTexture = ctypes.POINTER(struct_WGPUExternalTextureImpl)
class struct_WGPUInstanceImpl(Structure):
    pass

WGPUInstance = ctypes.POINTER(struct_WGPUInstanceImpl)
class struct_WGPUPipelineLayoutImpl(Structure):
    pass

WGPUPipelineLayout = ctypes.POINTER(struct_WGPUPipelineLayoutImpl)
class struct_WGPUQuerySetImpl(Structure):
    pass

WGPUQuerySet = ctypes.POINTER(struct_WGPUQuerySetImpl)
class struct_WGPUQueueImpl(Structure):
    pass

WGPUQueue = ctypes.POINTER(struct_WGPUQueueImpl)
class struct_WGPURenderBundleImpl(Structure):
    pass

WGPURenderBundle = ctypes.POINTER(struct_WGPURenderBundleImpl)
class struct_WGPURenderBundleEncoderImpl(Structure):
    pass

WGPURenderBundleEncoder = ctypes.POINTER(struct_WGPURenderBundleEncoderImpl)
class struct_WGPURenderPassEncoderImpl(Structure):
    pass

WGPURenderPassEncoder = ctypes.POINTER(struct_WGPURenderPassEncoderImpl)
class struct_WGPURenderPipelineImpl(Structure):
    pass

WGPURenderPipeline = ctypes.POINTER(struct_WGPURenderPipelineImpl)
class struct_WGPUSamplerImpl(Structure):
    pass

WGPUSampler = ctypes.POINTER(struct_WGPUSamplerImpl)
class struct_WGPUShaderModuleImpl(Structure):
    pass

WGPUShaderModule = ctypes.POINTER(struct_WGPUShaderModuleImpl)
class struct_WGPUSharedBufferMemoryImpl(Structure):
    pass

WGPUSharedBufferMemory = ctypes.POINTER(struct_WGPUSharedBufferMemoryImpl)
class struct_WGPUSharedFenceImpl(Structure):
    pass

WGPUSharedFence = ctypes.POINTER(struct_WGPUSharedFenceImpl)
class struct_WGPUSharedTextureMemoryImpl(Structure):
    pass

WGPUSharedTextureMemory = ctypes.POINTER(struct_WGPUSharedTextureMemoryImpl)
class struct_WGPUSurfaceImpl(Structure):
    pass

WGPUSurface = ctypes.POINTER(struct_WGPUSurfaceImpl)
class struct_WGPUSwapChainImpl(Structure):
    pass

WGPUSwapChain = ctypes.POINTER(struct_WGPUSwapChainImpl)
class struct_WGPUTextureImpl(Structure):
    pass

WGPUTexture = ctypes.POINTER(struct_WGPUTextureImpl)
class struct_WGPUTextureViewImpl(Structure):
    pass

WGPUTextureView = ctypes.POINTER(struct_WGPUTextureViewImpl)

# values for enumeration 'WGPUWGSLFeatureName'
WGPUWGSLFeatureName__enumvalues = {
    0: 'WGPUWGSLFeatureName_Undefined',
    1: 'WGPUWGSLFeatureName_ReadonlyAndReadwriteStorageTextures',
    2: 'WGPUWGSLFeatureName_Packed4x8IntegerDotProduct',
    3: 'WGPUWGSLFeatureName_UnrestrictedPointerParameters',
    4: 'WGPUWGSLFeatureName_PointerCompositeAccess',
    1000: 'WGPUWGSLFeatureName_ChromiumTestingUnimplemented',
    1001: 'WGPUWGSLFeatureName_ChromiumTestingUnsafeExperimental',
    1002: 'WGPUWGSLFeatureName_ChromiumTestingExperimental',
    1003: 'WGPUWGSLFeatureName_ChromiumTestingShippedWithKillswitch',
    1004: 'WGPUWGSLFeatureName_ChromiumTestingShipped',
    2147483647: 'WGPUWGSLFeatureName_Force32',
}
WGPUWGSLFeatureName_Undefined = 0
WGPUWGSLFeatureName_ReadonlyAndReadwriteStorageTextures = 1
WGPUWGSLFeatureName_Packed4x8IntegerDotProduct = 2
WGPUWGSLFeatureName_UnrestrictedPointerParameters = 3
WGPUWGSLFeatureName_PointerCompositeAccess = 4
WGPUWGSLFeatureName_ChromiumTestingUnimplemented = 1000
WGPUWGSLFeatureName_ChromiumTestingUnsafeExperimental = 1001
WGPUWGSLFeatureName_ChromiumTestingExperimental = 1002
WGPUWGSLFeatureName_ChromiumTestingShippedWithKillswitch = 1003
WGPUWGSLFeatureName_ChromiumTestingShipped = 1004
WGPUWGSLFeatureName_Force32 = 2147483647
WGPUWGSLFeatureName = ctypes.c_uint32 # enum

# values for enumeration 'WGPUAdapterType'
WGPUAdapterType__enumvalues = {
    1: 'WGPUAdapterType_DiscreteGPU',
    2: 'WGPUAdapterType_IntegratedGPU',
    3: 'WGPUAdapterType_CPU',
    4: 'WGPUAdapterType_Unknown',
    2147483647: 'WGPUAdapterType_Force32',
}
WGPUAdapterType_DiscreteGPU = 1
WGPUAdapterType_IntegratedGPU = 2
WGPUAdapterType_CPU = 3
WGPUAdapterType_Unknown = 4
WGPUAdapterType_Force32 = 2147483647
WGPUAdapterType = ctypes.c_uint32 # enum

# values for enumeration 'WGPUAddressMode'
WGPUAddressMode__enumvalues = {
    0: 'WGPUAddressMode_Undefined',
    1: 'WGPUAddressMode_ClampToEdge',
    2: 'WGPUAddressMode_Repeat',
    3: 'WGPUAddressMode_MirrorRepeat',
    2147483647: 'WGPUAddressMode_Force32',
}
WGPUAddressMode_Undefined = 0
WGPUAddressMode_ClampToEdge = 1
WGPUAddressMode_Repeat = 2
WGPUAddressMode_MirrorRepeat = 3
WGPUAddressMode_Force32 = 2147483647
WGPUAddressMode = ctypes.c_uint32 # enum

# values for enumeration 'WGPUAlphaMode'
WGPUAlphaMode__enumvalues = {
    1: 'WGPUAlphaMode_Opaque',
    2: 'WGPUAlphaMode_Premultiplied',
    3: 'WGPUAlphaMode_Unpremultiplied',
    2147483647: 'WGPUAlphaMode_Force32',
}
WGPUAlphaMode_Opaque = 1
WGPUAlphaMode_Premultiplied = 2
WGPUAlphaMode_Unpremultiplied = 3
WGPUAlphaMode_Force32 = 2147483647
WGPUAlphaMode = ctypes.c_uint32 # enum

# values for enumeration 'WGPUBackendType'
WGPUBackendType__enumvalues = {
    0: 'WGPUBackendType_Undefined',
    1: 'WGPUBackendType_Null',
    2: 'WGPUBackendType_WebGPU',
    3: 'WGPUBackendType_D3D11',
    4: 'WGPUBackendType_D3D12',
    5: 'WGPUBackendType_Metal',
    6: 'WGPUBackendType_Vulkan',
    7: 'WGPUBackendType_OpenGL',
    8: 'WGPUBackendType_OpenGLES',
    2147483647: 'WGPUBackendType_Force32',
}
WGPUBackendType_Undefined = 0
WGPUBackendType_Null = 1
WGPUBackendType_WebGPU = 2
WGPUBackendType_D3D11 = 3
WGPUBackendType_D3D12 = 4
WGPUBackendType_Metal = 5
WGPUBackendType_Vulkan = 6
WGPUBackendType_OpenGL = 7
WGPUBackendType_OpenGLES = 8
WGPUBackendType_Force32 = 2147483647
WGPUBackendType = ctypes.c_uint32 # enum

# values for enumeration 'WGPUBlendFactor'
WGPUBlendFactor__enumvalues = {
    0: 'WGPUBlendFactor_Undefined',
    1: 'WGPUBlendFactor_Zero',
    2: 'WGPUBlendFactor_One',
    3: 'WGPUBlendFactor_Src',
    4: 'WGPUBlendFactor_OneMinusSrc',
    5: 'WGPUBlendFactor_SrcAlpha',
    6: 'WGPUBlendFactor_OneMinusSrcAlpha',
    7: 'WGPUBlendFactor_Dst',
    8: 'WGPUBlendFactor_OneMinusDst',
    9: 'WGPUBlendFactor_DstAlpha',
    10: 'WGPUBlendFactor_OneMinusDstAlpha',
    11: 'WGPUBlendFactor_SrcAlphaSaturated',
    12: 'WGPUBlendFactor_Constant',
    13: 'WGPUBlendFactor_OneMinusConstant',
    14: 'WGPUBlendFactor_Src1',
    15: 'WGPUBlendFactor_OneMinusSrc1',
    16: 'WGPUBlendFactor_Src1Alpha',
    17: 'WGPUBlendFactor_OneMinusSrc1Alpha',
    2147483647: 'WGPUBlendFactor_Force32',
}
WGPUBlendFactor_Undefined = 0
WGPUBlendFactor_Zero = 1
WGPUBlendFactor_One = 2
WGPUBlendFactor_Src = 3
WGPUBlendFactor_OneMinusSrc = 4
WGPUBlendFactor_SrcAlpha = 5
WGPUBlendFactor_OneMinusSrcAlpha = 6
WGPUBlendFactor_Dst = 7
WGPUBlendFactor_OneMinusDst = 8
WGPUBlendFactor_DstAlpha = 9
WGPUBlendFactor_OneMinusDstAlpha = 10
WGPUBlendFactor_SrcAlphaSaturated = 11
WGPUBlendFactor_Constant = 12
WGPUBlendFactor_OneMinusConstant = 13
WGPUBlendFactor_Src1 = 14
WGPUBlendFactor_OneMinusSrc1 = 15
WGPUBlendFactor_Src1Alpha = 16
WGPUBlendFactor_OneMinusSrc1Alpha = 17
WGPUBlendFactor_Force32 = 2147483647
WGPUBlendFactor = ctypes.c_uint32 # enum

# values for enumeration 'WGPUBlendOperation'
WGPUBlendOperation__enumvalues = {
    0: 'WGPUBlendOperation_Undefined',
    1: 'WGPUBlendOperation_Add',
    2: 'WGPUBlendOperation_Subtract',
    3: 'WGPUBlendOperation_ReverseSubtract',
    4: 'WGPUBlendOperation_Min',
    5: 'WGPUBlendOperation_Max',
    2147483647: 'WGPUBlendOperation_Force32',
}
WGPUBlendOperation_Undefined = 0
WGPUBlendOperation_Add = 1
WGPUBlendOperation_Subtract = 2
WGPUBlendOperation_ReverseSubtract = 3
WGPUBlendOperation_Min = 4
WGPUBlendOperation_Max = 5
WGPUBlendOperation_Force32 = 2147483647
WGPUBlendOperation = ctypes.c_uint32 # enum

# values for enumeration 'WGPUBufferBindingType'
WGPUBufferBindingType__enumvalues = {
    0: 'WGPUBufferBindingType_Undefined',
    1: 'WGPUBufferBindingType_Uniform',
    2: 'WGPUBufferBindingType_Storage',
    3: 'WGPUBufferBindingType_ReadOnlyStorage',
    2147483647: 'WGPUBufferBindingType_Force32',
}
WGPUBufferBindingType_Undefined = 0
WGPUBufferBindingType_Uniform = 1
WGPUBufferBindingType_Storage = 2
WGPUBufferBindingType_ReadOnlyStorage = 3
WGPUBufferBindingType_Force32 = 2147483647
WGPUBufferBindingType = ctypes.c_uint32 # enum

# values for enumeration 'WGPUBufferMapAsyncStatus'
WGPUBufferMapAsyncStatus__enumvalues = {
    0: 'WGPUBufferMapAsyncStatus_Success',
    1: 'WGPUBufferMapAsyncStatus_InstanceDropped',
    2: 'WGPUBufferMapAsyncStatus_ValidationError',
    3: 'WGPUBufferMapAsyncStatus_Unknown',
    4: 'WGPUBufferMapAsyncStatus_DeviceLost',
    5: 'WGPUBufferMapAsyncStatus_DestroyedBeforeCallback',
    6: 'WGPUBufferMapAsyncStatus_UnmappedBeforeCallback',
    7: 'WGPUBufferMapAsyncStatus_MappingAlreadyPending',
    8: 'WGPUBufferMapAsyncStatus_OffsetOutOfRange',
    9: 'WGPUBufferMapAsyncStatus_SizeOutOfRange',
    2147483647: 'WGPUBufferMapAsyncStatus_Force32',
}
WGPUBufferMapAsyncStatus_Success = 0
WGPUBufferMapAsyncStatus_InstanceDropped = 1
WGPUBufferMapAsyncStatus_ValidationError = 2
WGPUBufferMapAsyncStatus_Unknown = 3
WGPUBufferMapAsyncStatus_DeviceLost = 4
WGPUBufferMapAsyncStatus_DestroyedBeforeCallback = 5
WGPUBufferMapAsyncStatus_UnmappedBeforeCallback = 6
WGPUBufferMapAsyncStatus_MappingAlreadyPending = 7
WGPUBufferMapAsyncStatus_OffsetOutOfRange = 8
WGPUBufferMapAsyncStatus_SizeOutOfRange = 9
WGPUBufferMapAsyncStatus_Force32 = 2147483647
WGPUBufferMapAsyncStatus = ctypes.c_uint32 # enum

# values for enumeration 'WGPUBufferMapState'
WGPUBufferMapState__enumvalues = {
    1: 'WGPUBufferMapState_Unmapped',
    2: 'WGPUBufferMapState_Pending',
    3: 'WGPUBufferMapState_Mapped',
    2147483647: 'WGPUBufferMapState_Force32',
}
WGPUBufferMapState_Unmapped = 1
WGPUBufferMapState_Pending = 2
WGPUBufferMapState_Mapped = 3
WGPUBufferMapState_Force32 = 2147483647
WGPUBufferMapState = ctypes.c_uint32 # enum

# values for enumeration 'WGPUCallbackMode'
WGPUCallbackMode__enumvalues = {
    1: 'WGPUCallbackMode_WaitAnyOnly',
    2: 'WGPUCallbackMode_AllowProcessEvents',
    3: 'WGPUCallbackMode_AllowSpontaneous',
    2147483647: 'WGPUCallbackMode_Force32',
}
WGPUCallbackMode_WaitAnyOnly = 1
WGPUCallbackMode_AllowProcessEvents = 2
WGPUCallbackMode_AllowSpontaneous = 3
WGPUCallbackMode_Force32 = 2147483647
WGPUCallbackMode = ctypes.c_uint32 # enum

# values for enumeration 'WGPUCompareFunction'
WGPUCompareFunction__enumvalues = {
    0: 'WGPUCompareFunction_Undefined',
    1: 'WGPUCompareFunction_Never',
    2: 'WGPUCompareFunction_Less',
    3: 'WGPUCompareFunction_Equal',
    4: 'WGPUCompareFunction_LessEqual',
    5: 'WGPUCompareFunction_Greater',
    6: 'WGPUCompareFunction_NotEqual',
    7: 'WGPUCompareFunction_GreaterEqual',
    8: 'WGPUCompareFunction_Always',
    2147483647: 'WGPUCompareFunction_Force32',
}
WGPUCompareFunction_Undefined = 0
WGPUCompareFunction_Never = 1
WGPUCompareFunction_Less = 2
WGPUCompareFunction_Equal = 3
WGPUCompareFunction_LessEqual = 4
WGPUCompareFunction_Greater = 5
WGPUCompareFunction_NotEqual = 6
WGPUCompareFunction_GreaterEqual = 7
WGPUCompareFunction_Always = 8
WGPUCompareFunction_Force32 = 2147483647
WGPUCompareFunction = ctypes.c_uint32 # enum

# values for enumeration 'WGPUCompilationInfoRequestStatus'
WGPUCompilationInfoRequestStatus__enumvalues = {
    0: 'WGPUCompilationInfoRequestStatus_Success',
    1: 'WGPUCompilationInfoRequestStatus_InstanceDropped',
    2: 'WGPUCompilationInfoRequestStatus_Error',
    3: 'WGPUCompilationInfoRequestStatus_DeviceLost',
    4: 'WGPUCompilationInfoRequestStatus_Unknown',
    2147483647: 'WGPUCompilationInfoRequestStatus_Force32',
}
WGPUCompilationInfoRequestStatus_Success = 0
WGPUCompilationInfoRequestStatus_InstanceDropped = 1
WGPUCompilationInfoRequestStatus_Error = 2
WGPUCompilationInfoRequestStatus_DeviceLost = 3
WGPUCompilationInfoRequestStatus_Unknown = 4
WGPUCompilationInfoRequestStatus_Force32 = 2147483647
WGPUCompilationInfoRequestStatus = ctypes.c_uint32 # enum

# values for enumeration 'WGPUCompilationMessageType'
WGPUCompilationMessageType__enumvalues = {
    1: 'WGPUCompilationMessageType_Error',
    2: 'WGPUCompilationMessageType_Warning',
    3: 'WGPUCompilationMessageType_Info',
    2147483647: 'WGPUCompilationMessageType_Force32',
}
WGPUCompilationMessageType_Error = 1
WGPUCompilationMessageType_Warning = 2
WGPUCompilationMessageType_Info = 3
WGPUCompilationMessageType_Force32 = 2147483647
WGPUCompilationMessageType = ctypes.c_uint32 # enum

# values for enumeration 'WGPUCompositeAlphaMode'
WGPUCompositeAlphaMode__enumvalues = {
    0: 'WGPUCompositeAlphaMode_Auto',
    1: 'WGPUCompositeAlphaMode_Opaque',
    2: 'WGPUCompositeAlphaMode_Premultiplied',
    3: 'WGPUCompositeAlphaMode_Unpremultiplied',
    4: 'WGPUCompositeAlphaMode_Inherit',
    2147483647: 'WGPUCompositeAlphaMode_Force32',
}
WGPUCompositeAlphaMode_Auto = 0
WGPUCompositeAlphaMode_Opaque = 1
WGPUCompositeAlphaMode_Premultiplied = 2
WGPUCompositeAlphaMode_Unpremultiplied = 3
WGPUCompositeAlphaMode_Inherit = 4
WGPUCompositeAlphaMode_Force32 = 2147483647
WGPUCompositeAlphaMode = ctypes.c_uint32 # enum

# values for enumeration 'WGPUCreatePipelineAsyncStatus'
WGPUCreatePipelineAsyncStatus__enumvalues = {
    0: 'WGPUCreatePipelineAsyncStatus_Success',
    1: 'WGPUCreatePipelineAsyncStatus_InstanceDropped',
    2: 'WGPUCreatePipelineAsyncStatus_ValidationError',
    3: 'WGPUCreatePipelineAsyncStatus_InternalError',
    4: 'WGPUCreatePipelineAsyncStatus_DeviceLost',
    5: 'WGPUCreatePipelineAsyncStatus_DeviceDestroyed',
    6: 'WGPUCreatePipelineAsyncStatus_Unknown',
    2147483647: 'WGPUCreatePipelineAsyncStatus_Force32',
}
WGPUCreatePipelineAsyncStatus_Success = 0
WGPUCreatePipelineAsyncStatus_InstanceDropped = 1
WGPUCreatePipelineAsyncStatus_ValidationError = 2
WGPUCreatePipelineAsyncStatus_InternalError = 3
WGPUCreatePipelineAsyncStatus_DeviceLost = 4
WGPUCreatePipelineAsyncStatus_DeviceDestroyed = 5
WGPUCreatePipelineAsyncStatus_Unknown = 6
WGPUCreatePipelineAsyncStatus_Force32 = 2147483647
WGPUCreatePipelineAsyncStatus = ctypes.c_uint32 # enum

# values for enumeration 'WGPUCullMode'
WGPUCullMode__enumvalues = {
    0: 'WGPUCullMode_Undefined',
    1: 'WGPUCullMode_None',
    2: 'WGPUCullMode_Front',
    3: 'WGPUCullMode_Back',
    2147483647: 'WGPUCullMode_Force32',
}
WGPUCullMode_Undefined = 0
WGPUCullMode_None = 1
WGPUCullMode_Front = 2
WGPUCullMode_Back = 3
WGPUCullMode_Force32 = 2147483647
WGPUCullMode = ctypes.c_uint32 # enum

# values for enumeration 'WGPUDeviceLostReason'
WGPUDeviceLostReason__enumvalues = {
    1: 'WGPUDeviceLostReason_Unknown',
    2: 'WGPUDeviceLostReason_Destroyed',
    3: 'WGPUDeviceLostReason_InstanceDropped',
    4: 'WGPUDeviceLostReason_FailedCreation',
    2147483647: 'WGPUDeviceLostReason_Force32',
}
WGPUDeviceLostReason_Unknown = 1
WGPUDeviceLostReason_Destroyed = 2
WGPUDeviceLostReason_InstanceDropped = 3
WGPUDeviceLostReason_FailedCreation = 4
WGPUDeviceLostReason_Force32 = 2147483647
WGPUDeviceLostReason = ctypes.c_uint32 # enum

# values for enumeration 'WGPUErrorFilter'
WGPUErrorFilter__enumvalues = {
    1: 'WGPUErrorFilter_Validation',
    2: 'WGPUErrorFilter_OutOfMemory',
    3: 'WGPUErrorFilter_Internal',
    2147483647: 'WGPUErrorFilter_Force32',
}
WGPUErrorFilter_Validation = 1
WGPUErrorFilter_OutOfMemory = 2
WGPUErrorFilter_Internal = 3
WGPUErrorFilter_Force32 = 2147483647
WGPUErrorFilter = ctypes.c_uint32 # enum

# values for enumeration 'WGPUErrorType'
WGPUErrorType__enumvalues = {
    0: 'WGPUErrorType_NoError',
    1: 'WGPUErrorType_Validation',
    2: 'WGPUErrorType_OutOfMemory',
    3: 'WGPUErrorType_Internal',
    4: 'WGPUErrorType_Unknown',
    5: 'WGPUErrorType_DeviceLost',
    2147483647: 'WGPUErrorType_Force32',
}
WGPUErrorType_NoError = 0
WGPUErrorType_Validation = 1
WGPUErrorType_OutOfMemory = 2
WGPUErrorType_Internal = 3
WGPUErrorType_Unknown = 4
WGPUErrorType_DeviceLost = 5
WGPUErrorType_Force32 = 2147483647
WGPUErrorType = ctypes.c_uint32 # enum

# values for enumeration 'WGPUExternalTextureRotation'
WGPUExternalTextureRotation__enumvalues = {
    0: 'WGPUExternalTextureRotation_Rotate0Degrees',
    1: 'WGPUExternalTextureRotation_Rotate90Degrees',
    2: 'WGPUExternalTextureRotation_Rotate180Degrees',
    3: 'WGPUExternalTextureRotation_Rotate270Degrees',
    2147483647: 'WGPUExternalTextureRotation_Force32',
}
WGPUExternalTextureRotation_Rotate0Degrees = 0
WGPUExternalTextureRotation_Rotate90Degrees = 1
WGPUExternalTextureRotation_Rotate180Degrees = 2
WGPUExternalTextureRotation_Rotate270Degrees = 3
WGPUExternalTextureRotation_Force32 = 2147483647
WGPUExternalTextureRotation = ctypes.c_uint32 # enum

# values for enumeration 'WGPUFeatureName'
WGPUFeatureName__enumvalues = {
    0: 'WGPUFeatureName_Undefined',
    1: 'WGPUFeatureName_DepthClipControl',
    2: 'WGPUFeatureName_Depth32FloatStencil8',
    3: 'WGPUFeatureName_TimestampQuery',
    4: 'WGPUFeatureName_TextureCompressionBC',
    5: 'WGPUFeatureName_TextureCompressionETC2',
    6: 'WGPUFeatureName_TextureCompressionASTC',
    7: 'WGPUFeatureName_IndirectFirstInstance',
    8: 'WGPUFeatureName_ShaderF16',
    9: 'WGPUFeatureName_RG11B10UfloatRenderable',
    10: 'WGPUFeatureName_BGRA8UnormStorage',
    11: 'WGPUFeatureName_Float32Filterable',
    1002: 'WGPUFeatureName_DawnInternalUsages',
    1003: 'WGPUFeatureName_DawnMultiPlanarFormats',
    1004: 'WGPUFeatureName_DawnNative',
    1006: 'WGPUFeatureName_ChromiumExperimentalTimestampQueryInsidePasses',
    1007: 'WGPUFeatureName_ImplicitDeviceSynchronization',
    1008: 'WGPUFeatureName_SurfaceCapabilities',
    1009: 'WGPUFeatureName_TransientAttachments',
    1010: 'WGPUFeatureName_MSAARenderToSingleSampled',
    1011: 'WGPUFeatureName_DualSourceBlending',
    1012: 'WGPUFeatureName_D3D11MultithreadProtected',
    1013: 'WGPUFeatureName_ANGLETextureSharing',
    1014: 'WGPUFeatureName_ChromiumExperimentalSubgroups',
    1015: 'WGPUFeatureName_ChromiumExperimentalSubgroupUniformControlFlow',
    1017: 'WGPUFeatureName_PixelLocalStorageCoherent',
    1018: 'WGPUFeatureName_PixelLocalStorageNonCoherent',
    1019: 'WGPUFeatureName_Unorm16TextureFormats',
    1020: 'WGPUFeatureName_Snorm16TextureFormats',
    1021: 'WGPUFeatureName_MultiPlanarFormatExtendedUsages',
    1022: 'WGPUFeatureName_MultiPlanarFormatP010',
    1023: 'WGPUFeatureName_HostMappedPointer',
    1024: 'WGPUFeatureName_MultiPlanarRenderTargets',
    1025: 'WGPUFeatureName_MultiPlanarFormatNv12a',
    1026: 'WGPUFeatureName_FramebufferFetch',
    1027: 'WGPUFeatureName_BufferMapExtendedUsages',
    1028: 'WGPUFeatureName_AdapterPropertiesMemoryHeaps',
    1029: 'WGPUFeatureName_AdapterPropertiesD3D',
    1030: 'WGPUFeatureName_AdapterPropertiesVk',
    1031: 'WGPUFeatureName_R8UnormStorage',
    1032: 'WGPUFeatureName_FormatCapabilities',
    1033: 'WGPUFeatureName_DrmFormatCapabilities',
    1034: 'WGPUFeatureName_Norm16TextureFormats',
    1035: 'WGPUFeatureName_MultiPlanarFormatNv16',
    1036: 'WGPUFeatureName_MultiPlanarFormatNv24',
    1037: 'WGPUFeatureName_MultiPlanarFormatP210',
    1038: 'WGPUFeatureName_MultiPlanarFormatP410',
    1100: 'WGPUFeatureName_SharedTextureMemoryVkDedicatedAllocation',
    1101: 'WGPUFeatureName_SharedTextureMemoryAHardwareBuffer',
    1102: 'WGPUFeatureName_SharedTextureMemoryDmaBuf',
    1103: 'WGPUFeatureName_SharedTextureMemoryOpaqueFD',
    1104: 'WGPUFeatureName_SharedTextureMemoryZirconHandle',
    1105: 'WGPUFeatureName_SharedTextureMemoryDXGISharedHandle',
    1106: 'WGPUFeatureName_SharedTextureMemoryD3D11Texture2D',
    1107: 'WGPUFeatureName_SharedTextureMemoryIOSurface',
    1108: 'WGPUFeatureName_SharedTextureMemoryEGLImage',
    1200: 'WGPUFeatureName_SharedFenceVkSemaphoreOpaqueFD',
    1201: 'WGPUFeatureName_SharedFenceVkSemaphoreSyncFD',
    1202: 'WGPUFeatureName_SharedFenceVkSemaphoreZirconHandle',
    1203: 'WGPUFeatureName_SharedFenceDXGISharedHandle',
    1204: 'WGPUFeatureName_SharedFenceMTLSharedEvent',
    1205: 'WGPUFeatureName_SharedBufferMemoryD3D12Resource',
    1206: 'WGPUFeatureName_StaticSamplers',
    1207: 'WGPUFeatureName_YCbCrVulkanSamplers',
    1208: 'WGPUFeatureName_ShaderModuleCompilationOptions',
    1209: 'WGPUFeatureName_DawnLoadResolveTexture',
    2147483647: 'WGPUFeatureName_Force32',
}
WGPUFeatureName_Undefined = 0
WGPUFeatureName_DepthClipControl = 1
WGPUFeatureName_Depth32FloatStencil8 = 2
WGPUFeatureName_TimestampQuery = 3
WGPUFeatureName_TextureCompressionBC = 4
WGPUFeatureName_TextureCompressionETC2 = 5
WGPUFeatureName_TextureCompressionASTC = 6
WGPUFeatureName_IndirectFirstInstance = 7
WGPUFeatureName_ShaderF16 = 8
WGPUFeatureName_RG11B10UfloatRenderable = 9
WGPUFeatureName_BGRA8UnormStorage = 10
WGPUFeatureName_Float32Filterable = 11
WGPUFeatureName_DawnInternalUsages = 1002
WGPUFeatureName_DawnMultiPlanarFormats = 1003
WGPUFeatureName_DawnNative = 1004
WGPUFeatureName_ChromiumExperimentalTimestampQueryInsidePasses = 1006
WGPUFeatureName_ImplicitDeviceSynchronization = 1007
WGPUFeatureName_SurfaceCapabilities = 1008
WGPUFeatureName_TransientAttachments = 1009
WGPUFeatureName_MSAARenderToSingleSampled = 1010
WGPUFeatureName_DualSourceBlending = 1011
WGPUFeatureName_D3D11MultithreadProtected = 1012
WGPUFeatureName_ANGLETextureSharing = 1013
WGPUFeatureName_ChromiumExperimentalSubgroups = 1014
WGPUFeatureName_ChromiumExperimentalSubgroupUniformControlFlow = 1015
WGPUFeatureName_PixelLocalStorageCoherent = 1017
WGPUFeatureName_PixelLocalStorageNonCoherent = 1018
WGPUFeatureName_Unorm16TextureFormats = 1019
WGPUFeatureName_Snorm16TextureFormats = 1020
WGPUFeatureName_MultiPlanarFormatExtendedUsages = 1021
WGPUFeatureName_MultiPlanarFormatP010 = 1022
WGPUFeatureName_HostMappedPointer = 1023
WGPUFeatureName_MultiPlanarRenderTargets = 1024
WGPUFeatureName_MultiPlanarFormatNv12a = 1025
WGPUFeatureName_FramebufferFetch = 1026
WGPUFeatureName_BufferMapExtendedUsages = 1027
WGPUFeatureName_AdapterPropertiesMemoryHeaps = 1028
WGPUFeatureName_AdapterPropertiesD3D = 1029
WGPUFeatureName_AdapterPropertiesVk = 1030
WGPUFeatureName_R8UnormStorage = 1031
WGPUFeatureName_FormatCapabilities = 1032
WGPUFeatureName_DrmFormatCapabilities = 1033
WGPUFeatureName_Norm16TextureFormats = 1034
WGPUFeatureName_MultiPlanarFormatNv16 = 1035
WGPUFeatureName_MultiPlanarFormatNv24 = 1036
WGPUFeatureName_MultiPlanarFormatP210 = 1037
WGPUFeatureName_MultiPlanarFormatP410 = 1038
WGPUFeatureName_SharedTextureMemoryVkDedicatedAllocation = 1100
WGPUFeatureName_SharedTextureMemoryAHardwareBuffer = 1101
WGPUFeatureName_SharedTextureMemoryDmaBuf = 1102
WGPUFeatureName_SharedTextureMemoryOpaqueFD = 1103
WGPUFeatureName_SharedTextureMemoryZirconHandle = 1104
WGPUFeatureName_SharedTextureMemoryDXGISharedHandle = 1105
WGPUFeatureName_SharedTextureMemoryD3D11Texture2D = 1106
WGPUFeatureName_SharedTextureMemoryIOSurface = 1107
WGPUFeatureName_SharedTextureMemoryEGLImage = 1108
WGPUFeatureName_SharedFenceVkSemaphoreOpaqueFD = 1200
WGPUFeatureName_SharedFenceVkSemaphoreSyncFD = 1201
WGPUFeatureName_SharedFenceVkSemaphoreZirconHandle = 1202
WGPUFeatureName_SharedFenceDXGISharedHandle = 1203
WGPUFeatureName_SharedFenceMTLSharedEvent = 1204
WGPUFeatureName_SharedBufferMemoryD3D12Resource = 1205
WGPUFeatureName_StaticSamplers = 1206
WGPUFeatureName_YCbCrVulkanSamplers = 1207
WGPUFeatureName_ShaderModuleCompilationOptions = 1208
WGPUFeatureName_DawnLoadResolveTexture = 1209
WGPUFeatureName_Force32 = 2147483647
WGPUFeatureName = ctypes.c_uint32 # enum

# values for enumeration 'WGPUFilterMode'
WGPUFilterMode__enumvalues = {
    0: 'WGPUFilterMode_Undefined',
    1: 'WGPUFilterMode_Nearest',
    2: 'WGPUFilterMode_Linear',
    2147483647: 'WGPUFilterMode_Force32',
}
WGPUFilterMode_Undefined = 0
WGPUFilterMode_Nearest = 1
WGPUFilterMode_Linear = 2
WGPUFilterMode_Force32 = 2147483647
WGPUFilterMode = ctypes.c_uint32 # enum

# values for enumeration 'WGPUFrontFace'
WGPUFrontFace__enumvalues = {
    0: 'WGPUFrontFace_Undefined',
    1: 'WGPUFrontFace_CCW',
    2: 'WGPUFrontFace_CW',
    2147483647: 'WGPUFrontFace_Force32',
}
WGPUFrontFace_Undefined = 0
WGPUFrontFace_CCW = 1
WGPUFrontFace_CW = 2
WGPUFrontFace_Force32 = 2147483647
WGPUFrontFace = ctypes.c_uint32 # enum

# values for enumeration 'WGPUIndexFormat'
WGPUIndexFormat__enumvalues = {
    0: 'WGPUIndexFormat_Undefined',
    1: 'WGPUIndexFormat_Uint16',
    2: 'WGPUIndexFormat_Uint32',
    2147483647: 'WGPUIndexFormat_Force32',
}
WGPUIndexFormat_Undefined = 0
WGPUIndexFormat_Uint16 = 1
WGPUIndexFormat_Uint32 = 2
WGPUIndexFormat_Force32 = 2147483647
WGPUIndexFormat = ctypes.c_uint32 # enum

# values for enumeration 'WGPULoadOp'
WGPULoadOp__enumvalues = {
    0: 'WGPULoadOp_Undefined',
    1: 'WGPULoadOp_Clear',
    2: 'WGPULoadOp_Load',
    3: 'WGPULoadOp_ExpandResolveTexture',
    2147483647: 'WGPULoadOp_Force32',
}
WGPULoadOp_Undefined = 0
WGPULoadOp_Clear = 1
WGPULoadOp_Load = 2
WGPULoadOp_ExpandResolveTexture = 3
WGPULoadOp_Force32 = 2147483647
WGPULoadOp = ctypes.c_uint32 # enum

# values for enumeration 'WGPULoggingType'
WGPULoggingType__enumvalues = {
    1: 'WGPULoggingType_Verbose',
    2: 'WGPULoggingType_Info',
    3: 'WGPULoggingType_Warning',
    4: 'WGPULoggingType_Error',
    2147483647: 'WGPULoggingType_Force32',
}
WGPULoggingType_Verbose = 1
WGPULoggingType_Info = 2
WGPULoggingType_Warning = 3
WGPULoggingType_Error = 4
WGPULoggingType_Force32 = 2147483647
WGPULoggingType = ctypes.c_uint32 # enum

# values for enumeration 'WGPUMapAsyncStatus'
WGPUMapAsyncStatus__enumvalues = {
    0: 'WGPUMapAsyncStatus_Success',
    1: 'WGPUMapAsyncStatus_InstanceDropped',
    2: 'WGPUMapAsyncStatus_Error',
    3: 'WGPUMapAsyncStatus_Aborted',
    4: 'WGPUMapAsyncStatus_Unknown',
    2147483647: 'WGPUMapAsyncStatus_Force32',
}
WGPUMapAsyncStatus_Success = 0
WGPUMapAsyncStatus_InstanceDropped = 1
WGPUMapAsyncStatus_Error = 2
WGPUMapAsyncStatus_Aborted = 3
WGPUMapAsyncStatus_Unknown = 4
WGPUMapAsyncStatus_Force32 = 2147483647
WGPUMapAsyncStatus = ctypes.c_uint32 # enum

# values for enumeration 'WGPUMipmapFilterMode'
WGPUMipmapFilterMode__enumvalues = {
    0: 'WGPUMipmapFilterMode_Undefined',
    1: 'WGPUMipmapFilterMode_Nearest',
    2: 'WGPUMipmapFilterMode_Linear',
    2147483647: 'WGPUMipmapFilterMode_Force32',
}
WGPUMipmapFilterMode_Undefined = 0
WGPUMipmapFilterMode_Nearest = 1
WGPUMipmapFilterMode_Linear = 2
WGPUMipmapFilterMode_Force32 = 2147483647
WGPUMipmapFilterMode = ctypes.c_uint32 # enum

# values for enumeration 'WGPUPopErrorScopeStatus'
WGPUPopErrorScopeStatus__enumvalues = {
    0: 'WGPUPopErrorScopeStatus_Success',
    1: 'WGPUPopErrorScopeStatus_InstanceDropped',
    2147483647: 'WGPUPopErrorScopeStatus_Force32',
}
WGPUPopErrorScopeStatus_Success = 0
WGPUPopErrorScopeStatus_InstanceDropped = 1
WGPUPopErrorScopeStatus_Force32 = 2147483647
WGPUPopErrorScopeStatus = ctypes.c_uint32 # enum

# values for enumeration 'WGPUPowerPreference'
WGPUPowerPreference__enumvalues = {
    0: 'WGPUPowerPreference_Undefined',
    1: 'WGPUPowerPreference_LowPower',
    2: 'WGPUPowerPreference_HighPerformance',
    2147483647: 'WGPUPowerPreference_Force32',
}
WGPUPowerPreference_Undefined = 0
WGPUPowerPreference_LowPower = 1
WGPUPowerPreference_HighPerformance = 2
WGPUPowerPreference_Force32 = 2147483647
WGPUPowerPreference = ctypes.c_uint32 # enum

# values for enumeration 'WGPUPresentMode'
WGPUPresentMode__enumvalues = {
    0: 'WGPUPresentMode_Fifo',
    1: 'WGPUPresentMode_FifoRelaxed',
    2: 'WGPUPresentMode_Immediate',
    3: 'WGPUPresentMode_Mailbox',
    2147483647: 'WGPUPresentMode_Force32',
}
WGPUPresentMode_Fifo = 0
WGPUPresentMode_FifoRelaxed = 1
WGPUPresentMode_Immediate = 2
WGPUPresentMode_Mailbox = 3
WGPUPresentMode_Force32 = 2147483647
WGPUPresentMode = ctypes.c_uint32 # enum

# values for enumeration 'WGPUPrimitiveTopology'
WGPUPrimitiveTopology__enumvalues = {
    0: 'WGPUPrimitiveTopology_Undefined',
    1: 'WGPUPrimitiveTopology_PointList',
    2: 'WGPUPrimitiveTopology_LineList',
    3: 'WGPUPrimitiveTopology_LineStrip',
    4: 'WGPUPrimitiveTopology_TriangleList',
    5: 'WGPUPrimitiveTopology_TriangleStrip',
    2147483647: 'WGPUPrimitiveTopology_Force32',
}
WGPUPrimitiveTopology_Undefined = 0
WGPUPrimitiveTopology_PointList = 1
WGPUPrimitiveTopology_LineList = 2
WGPUPrimitiveTopology_LineStrip = 3
WGPUPrimitiveTopology_TriangleList = 4
WGPUPrimitiveTopology_TriangleStrip = 5
WGPUPrimitiveTopology_Force32 = 2147483647
WGPUPrimitiveTopology = ctypes.c_uint32 # enum

# values for enumeration 'WGPUQueryType'
WGPUQueryType__enumvalues = {
    1: 'WGPUQueryType_Occlusion',
    2: 'WGPUQueryType_Timestamp',
    2147483647: 'WGPUQueryType_Force32',
}
WGPUQueryType_Occlusion = 1
WGPUQueryType_Timestamp = 2
WGPUQueryType_Force32 = 2147483647
WGPUQueryType = ctypes.c_uint32 # enum

# values for enumeration 'WGPUQueueWorkDoneStatus'
WGPUQueueWorkDoneStatus__enumvalues = {
    0: 'WGPUQueueWorkDoneStatus_Success',
    1: 'WGPUQueueWorkDoneStatus_InstanceDropped',
    2: 'WGPUQueueWorkDoneStatus_Error',
    3: 'WGPUQueueWorkDoneStatus_Unknown',
    4: 'WGPUQueueWorkDoneStatus_DeviceLost',
    2147483647: 'WGPUQueueWorkDoneStatus_Force32',
}
WGPUQueueWorkDoneStatus_Success = 0
WGPUQueueWorkDoneStatus_InstanceDropped = 1
WGPUQueueWorkDoneStatus_Error = 2
WGPUQueueWorkDoneStatus_Unknown = 3
WGPUQueueWorkDoneStatus_DeviceLost = 4
WGPUQueueWorkDoneStatus_Force32 = 2147483647
WGPUQueueWorkDoneStatus = ctypes.c_uint32 # enum

# values for enumeration 'WGPURequestAdapterStatus'
WGPURequestAdapterStatus__enumvalues = {
    0: 'WGPURequestAdapterStatus_Success',
    1: 'WGPURequestAdapterStatus_InstanceDropped',
    2: 'WGPURequestAdapterStatus_Unavailable',
    3: 'WGPURequestAdapterStatus_Error',
    4: 'WGPURequestAdapterStatus_Unknown',
    2147483647: 'WGPURequestAdapterStatus_Force32',
}
WGPURequestAdapterStatus_Success = 0
WGPURequestAdapterStatus_InstanceDropped = 1
WGPURequestAdapterStatus_Unavailable = 2
WGPURequestAdapterStatus_Error = 3
WGPURequestAdapterStatus_Unknown = 4
WGPURequestAdapterStatus_Force32 = 2147483647
WGPURequestAdapterStatus = ctypes.c_uint32 # enum

# values for enumeration 'WGPURequestDeviceStatus'
WGPURequestDeviceStatus__enumvalues = {
    0: 'WGPURequestDeviceStatus_Success',
    1: 'WGPURequestDeviceStatus_InstanceDropped',
    2: 'WGPURequestDeviceStatus_Error',
    3: 'WGPURequestDeviceStatus_Unknown',
    2147483647: 'WGPURequestDeviceStatus_Force32',
}
WGPURequestDeviceStatus_Success = 0
WGPURequestDeviceStatus_InstanceDropped = 1
WGPURequestDeviceStatus_Error = 2
WGPURequestDeviceStatus_Unknown = 3
WGPURequestDeviceStatus_Force32 = 2147483647
WGPURequestDeviceStatus = ctypes.c_uint32 # enum

# values for enumeration 'WGPUSType'
WGPUSType__enumvalues = {
    0: 'WGPUSType_Invalid',
    1: 'WGPUSType_SurfaceDescriptorFromMetalLayer',
    2: 'WGPUSType_SurfaceDescriptorFromWindowsHWND',
    3: 'WGPUSType_SurfaceDescriptorFromXlibWindow',
    4: 'WGPUSType_SurfaceDescriptorFromCanvasHTMLSelector',
    5: 'WGPUSType_ShaderModuleSPIRVDescriptor',
    6: 'WGPUSType_ShaderModuleWGSLDescriptor',
    7: 'WGPUSType_PrimitiveDepthClipControl',
    8: 'WGPUSType_SurfaceDescriptorFromWaylandSurface',
    9: 'WGPUSType_SurfaceDescriptorFromAndroidNativeWindow',
    11: 'WGPUSType_SurfaceDescriptorFromWindowsCoreWindow',
    12: 'WGPUSType_ExternalTextureBindingEntry',
    13: 'WGPUSType_ExternalTextureBindingLayout',
    14: 'WGPUSType_SurfaceDescriptorFromWindowsSwapChainPanel',
    15: 'WGPUSType_RenderPassDescriptorMaxDrawCount',
    16: 'WGPUSType_DepthStencilStateDepthWriteDefinedDawn',
    17: 'WGPUSType_TextureBindingViewDimensionDescriptor',
    1000: 'WGPUSType_DawnTextureInternalUsageDescriptor',
    1003: 'WGPUSType_DawnEncoderInternalUsageDescriptor',
    1004: 'WGPUSType_DawnInstanceDescriptor',
    1005: 'WGPUSType_DawnCacheDeviceDescriptor',
    1006: 'WGPUSType_DawnAdapterPropertiesPowerPreference',
    1007: 'WGPUSType_DawnBufferDescriptorErrorInfoFromWireClient',
    1008: 'WGPUSType_DawnTogglesDescriptor',
    1009: 'WGPUSType_DawnShaderModuleSPIRVOptionsDescriptor',
    1010: 'WGPUSType_RequestAdapterOptionsLUID',
    1011: 'WGPUSType_RequestAdapterOptionsGetGLProc',
    1012: 'WGPUSType_RequestAdapterOptionsD3D11Device',
    1014: 'WGPUSType_DawnRenderPassColorAttachmentRenderToSingleSampled',
    1015: 'WGPUSType_RenderPassPixelLocalStorage',
    1016: 'WGPUSType_PipelineLayoutPixelLocalStorage',
    1017: 'WGPUSType_BufferHostMappedPointer',
    1018: 'WGPUSType_DawnExperimentalSubgroupLimits',
    1019: 'WGPUSType_AdapterPropertiesMemoryHeaps',
    1020: 'WGPUSType_AdapterPropertiesD3D',
    1021: 'WGPUSType_AdapterPropertiesVk',
    1022: 'WGPUSType_DawnComputePipelineFullSubgroups',
    1023: 'WGPUSType_DawnWireWGSLControl',
    1024: 'WGPUSType_DawnWGSLBlocklist',
    1025: 'WGPUSType_DrmFormatCapabilities',
    1026: 'WGPUSType_ShaderModuleCompilationOptions',
    1027: 'WGPUSType_ColorTargetStateExpandResolveTextureDawn',
    1101: 'WGPUSType_SharedTextureMemoryVkDedicatedAllocationDescriptor',
    1102: 'WGPUSType_SharedTextureMemoryAHardwareBufferDescriptor',
    1103: 'WGPUSType_SharedTextureMemoryDmaBufDescriptor',
    1104: 'WGPUSType_SharedTextureMemoryOpaqueFDDescriptor',
    1105: 'WGPUSType_SharedTextureMemoryZirconHandleDescriptor',
    1106: 'WGPUSType_SharedTextureMemoryDXGISharedHandleDescriptor',
    1107: 'WGPUSType_SharedTextureMemoryD3D11Texture2DDescriptor',
    1108: 'WGPUSType_SharedTextureMemoryIOSurfaceDescriptor',
    1109: 'WGPUSType_SharedTextureMemoryEGLImageDescriptor',
    1200: 'WGPUSType_SharedTextureMemoryInitializedBeginState',
    1201: 'WGPUSType_SharedTextureMemoryInitializedEndState',
    1202: 'WGPUSType_SharedTextureMemoryVkImageLayoutBeginState',
    1203: 'WGPUSType_SharedTextureMemoryVkImageLayoutEndState',
    1204: 'WGPUSType_SharedTextureMemoryD3DSwapchainBeginState',
    1205: 'WGPUSType_SharedFenceVkSemaphoreOpaqueFDDescriptor',
    1206: 'WGPUSType_SharedFenceVkSemaphoreOpaqueFDExportInfo',
    1207: 'WGPUSType_SharedFenceVkSemaphoreSyncFDDescriptor',
    1208: 'WGPUSType_SharedFenceVkSemaphoreSyncFDExportInfo',
    1209: 'WGPUSType_SharedFenceVkSemaphoreZirconHandleDescriptor',
    1210: 'WGPUSType_SharedFenceVkSemaphoreZirconHandleExportInfo',
    1211: 'WGPUSType_SharedFenceDXGISharedHandleDescriptor',
    1212: 'WGPUSType_SharedFenceDXGISharedHandleExportInfo',
    1213: 'WGPUSType_SharedFenceMTLSharedEventDescriptor',
    1214: 'WGPUSType_SharedFenceMTLSharedEventExportInfo',
    1215: 'WGPUSType_SharedBufferMemoryD3D12ResourceDescriptor',
    1216: 'WGPUSType_StaticSamplerBindingLayout',
    1217: 'WGPUSType_YCbCrVkDescriptor',
    1218: 'WGPUSType_SharedTextureMemoryAHardwareBufferProperties',
    1219: 'WGPUSType_AHardwareBufferProperties',
    2147483647: 'WGPUSType_Force32',
}
WGPUSType_Invalid = 0
WGPUSType_SurfaceDescriptorFromMetalLayer = 1
WGPUSType_SurfaceDescriptorFromWindowsHWND = 2
WGPUSType_SurfaceDescriptorFromXlibWindow = 3
WGPUSType_SurfaceDescriptorFromCanvasHTMLSelector = 4
WGPUSType_ShaderModuleSPIRVDescriptor = 5
WGPUSType_ShaderModuleWGSLDescriptor = 6
WGPUSType_PrimitiveDepthClipControl = 7
WGPUSType_SurfaceDescriptorFromWaylandSurface = 8
WGPUSType_SurfaceDescriptorFromAndroidNativeWindow = 9
WGPUSType_SurfaceDescriptorFromWindowsCoreWindow = 11
WGPUSType_ExternalTextureBindingEntry = 12
WGPUSType_ExternalTextureBindingLayout = 13
WGPUSType_SurfaceDescriptorFromWindowsSwapChainPanel = 14
WGPUSType_RenderPassDescriptorMaxDrawCount = 15
WGPUSType_DepthStencilStateDepthWriteDefinedDawn = 16
WGPUSType_TextureBindingViewDimensionDescriptor = 17
WGPUSType_DawnTextureInternalUsageDescriptor = 1000
WGPUSType_DawnEncoderInternalUsageDescriptor = 1003
WGPUSType_DawnInstanceDescriptor = 1004
WGPUSType_DawnCacheDeviceDescriptor = 1005
WGPUSType_DawnAdapterPropertiesPowerPreference = 1006
WGPUSType_DawnBufferDescriptorErrorInfoFromWireClient = 1007
WGPUSType_DawnTogglesDescriptor = 1008
WGPUSType_DawnShaderModuleSPIRVOptionsDescriptor = 1009
WGPUSType_RequestAdapterOptionsLUID = 1010
WGPUSType_RequestAdapterOptionsGetGLProc = 1011
WGPUSType_RequestAdapterOptionsD3D11Device = 1012
WGPUSType_DawnRenderPassColorAttachmentRenderToSingleSampled = 1014
WGPUSType_RenderPassPixelLocalStorage = 1015
WGPUSType_PipelineLayoutPixelLocalStorage = 1016
WGPUSType_BufferHostMappedPointer = 1017
WGPUSType_DawnExperimentalSubgroupLimits = 1018
WGPUSType_AdapterPropertiesMemoryHeaps = 1019
WGPUSType_AdapterPropertiesD3D = 1020
WGPUSType_AdapterPropertiesVk = 1021
WGPUSType_DawnComputePipelineFullSubgroups = 1022
WGPUSType_DawnWireWGSLControl = 1023
WGPUSType_DawnWGSLBlocklist = 1024
WGPUSType_DrmFormatCapabilities = 1025
WGPUSType_ShaderModuleCompilationOptions = 1026
WGPUSType_ColorTargetStateExpandResolveTextureDawn = 1027
WGPUSType_SharedTextureMemoryVkDedicatedAllocationDescriptor = 1101
WGPUSType_SharedTextureMemoryAHardwareBufferDescriptor = 1102
WGPUSType_SharedTextureMemoryDmaBufDescriptor = 1103
WGPUSType_SharedTextureMemoryOpaqueFDDescriptor = 1104
WGPUSType_SharedTextureMemoryZirconHandleDescriptor = 1105
WGPUSType_SharedTextureMemoryDXGISharedHandleDescriptor = 1106
WGPUSType_SharedTextureMemoryD3D11Texture2DDescriptor = 1107
WGPUSType_SharedTextureMemoryIOSurfaceDescriptor = 1108
WGPUSType_SharedTextureMemoryEGLImageDescriptor = 1109
WGPUSType_SharedTextureMemoryInitializedBeginState = 1200
WGPUSType_SharedTextureMemoryInitializedEndState = 1201
WGPUSType_SharedTextureMemoryVkImageLayoutBeginState = 1202
WGPUSType_SharedTextureMemoryVkImageLayoutEndState = 1203
WGPUSType_SharedTextureMemoryD3DSwapchainBeginState = 1204
WGPUSType_SharedFenceVkSemaphoreOpaqueFDDescriptor = 1205
WGPUSType_SharedFenceVkSemaphoreOpaqueFDExportInfo = 1206
WGPUSType_SharedFenceVkSemaphoreSyncFDDescriptor = 1207
WGPUSType_SharedFenceVkSemaphoreSyncFDExportInfo = 1208
WGPUSType_SharedFenceVkSemaphoreZirconHandleDescriptor = 1209
WGPUSType_SharedFenceVkSemaphoreZirconHandleExportInfo = 1210
WGPUSType_SharedFenceDXGISharedHandleDescriptor = 1211
WGPUSType_SharedFenceDXGISharedHandleExportInfo = 1212
WGPUSType_SharedFenceMTLSharedEventDescriptor = 1213
WGPUSType_SharedFenceMTLSharedEventExportInfo = 1214
WGPUSType_SharedBufferMemoryD3D12ResourceDescriptor = 1215
WGPUSType_StaticSamplerBindingLayout = 1216
WGPUSType_YCbCrVkDescriptor = 1217
WGPUSType_SharedTextureMemoryAHardwareBufferProperties = 1218
WGPUSType_AHardwareBufferProperties = 1219
WGPUSType_Force32 = 2147483647
WGPUSType = ctypes.c_uint32 # enum

# values for enumeration 'WGPUSamplerBindingType'
WGPUSamplerBindingType__enumvalues = {
    0: 'WGPUSamplerBindingType_Undefined',
    1: 'WGPUSamplerBindingType_Filtering',
    2: 'WGPUSamplerBindingType_NonFiltering',
    3: 'WGPUSamplerBindingType_Comparison',
    2147483647: 'WGPUSamplerBindingType_Force32',
}
WGPUSamplerBindingType_Undefined = 0
WGPUSamplerBindingType_Filtering = 1
WGPUSamplerBindingType_NonFiltering = 2
WGPUSamplerBindingType_Comparison = 3
WGPUSamplerBindingType_Force32 = 2147483647
WGPUSamplerBindingType = ctypes.c_uint32 # enum

# values for enumeration 'WGPUSharedFenceType'
WGPUSharedFenceType__enumvalues = {
    0: 'WGPUSharedFenceType_Undefined',
    1: 'WGPUSharedFenceType_VkSemaphoreOpaqueFD',
    2: 'WGPUSharedFenceType_VkSemaphoreSyncFD',
    3: 'WGPUSharedFenceType_VkSemaphoreZirconHandle',
    4: 'WGPUSharedFenceType_DXGISharedHandle',
    5: 'WGPUSharedFenceType_MTLSharedEvent',
    2147483647: 'WGPUSharedFenceType_Force32',
}
WGPUSharedFenceType_Undefined = 0
WGPUSharedFenceType_VkSemaphoreOpaqueFD = 1
WGPUSharedFenceType_VkSemaphoreSyncFD = 2
WGPUSharedFenceType_VkSemaphoreZirconHandle = 3
WGPUSharedFenceType_DXGISharedHandle = 4
WGPUSharedFenceType_MTLSharedEvent = 5
WGPUSharedFenceType_Force32 = 2147483647
WGPUSharedFenceType = ctypes.c_uint32 # enum

# values for enumeration 'WGPUStatus'
WGPUStatus__enumvalues = {
    0: 'WGPUStatus_Success',
    1: 'WGPUStatus_Error',
    2147483647: 'WGPUStatus_Force32',
}
WGPUStatus_Success = 0
WGPUStatus_Error = 1
WGPUStatus_Force32 = 2147483647
WGPUStatus = ctypes.c_uint32 # enum

# values for enumeration 'WGPUStencilOperation'
WGPUStencilOperation__enumvalues = {
    0: 'WGPUStencilOperation_Undefined',
    1: 'WGPUStencilOperation_Keep',
    2: 'WGPUStencilOperation_Zero',
    3: 'WGPUStencilOperation_Replace',
    4: 'WGPUStencilOperation_Invert',
    5: 'WGPUStencilOperation_IncrementClamp',
    6: 'WGPUStencilOperation_DecrementClamp',
    7: 'WGPUStencilOperation_IncrementWrap',
    8: 'WGPUStencilOperation_DecrementWrap',
    2147483647: 'WGPUStencilOperation_Force32',
}
WGPUStencilOperation_Undefined = 0
WGPUStencilOperation_Keep = 1
WGPUStencilOperation_Zero = 2
WGPUStencilOperation_Replace = 3
WGPUStencilOperation_Invert = 4
WGPUStencilOperation_IncrementClamp = 5
WGPUStencilOperation_DecrementClamp = 6
WGPUStencilOperation_IncrementWrap = 7
WGPUStencilOperation_DecrementWrap = 8
WGPUStencilOperation_Force32 = 2147483647
WGPUStencilOperation = ctypes.c_uint32 # enum

# values for enumeration 'WGPUStorageTextureAccess'
WGPUStorageTextureAccess__enumvalues = {
    0: 'WGPUStorageTextureAccess_Undefined',
    1: 'WGPUStorageTextureAccess_WriteOnly',
    2: 'WGPUStorageTextureAccess_ReadOnly',
    3: 'WGPUStorageTextureAccess_ReadWrite',
    2147483647: 'WGPUStorageTextureAccess_Force32',
}
WGPUStorageTextureAccess_Undefined = 0
WGPUStorageTextureAccess_WriteOnly = 1
WGPUStorageTextureAccess_ReadOnly = 2
WGPUStorageTextureAccess_ReadWrite = 3
WGPUStorageTextureAccess_Force32 = 2147483647
WGPUStorageTextureAccess = ctypes.c_uint32 # enum

# values for enumeration 'WGPUStoreOp'
WGPUStoreOp__enumvalues = {
    0: 'WGPUStoreOp_Undefined',
    1: 'WGPUStoreOp_Store',
    2: 'WGPUStoreOp_Discard',
    2147483647: 'WGPUStoreOp_Force32',
}
WGPUStoreOp_Undefined = 0
WGPUStoreOp_Store = 1
WGPUStoreOp_Discard = 2
WGPUStoreOp_Force32 = 2147483647
WGPUStoreOp = ctypes.c_uint32 # enum

# values for enumeration 'WGPUSurfaceGetCurrentTextureStatus'
WGPUSurfaceGetCurrentTextureStatus__enumvalues = {
    0: 'WGPUSurfaceGetCurrentTextureStatus_Success',
    1: 'WGPUSurfaceGetCurrentTextureStatus_Timeout',
    2: 'WGPUSurfaceGetCurrentTextureStatus_Outdated',
    3: 'WGPUSurfaceGetCurrentTextureStatus_Lost',
    4: 'WGPUSurfaceGetCurrentTextureStatus_OutOfMemory',
    5: 'WGPUSurfaceGetCurrentTextureStatus_DeviceLost',
    6: 'WGPUSurfaceGetCurrentTextureStatus_Error',
    2147483647: 'WGPUSurfaceGetCurrentTextureStatus_Force32',
}
WGPUSurfaceGetCurrentTextureStatus_Success = 0
WGPUSurfaceGetCurrentTextureStatus_Timeout = 1
WGPUSurfaceGetCurrentTextureStatus_Outdated = 2
WGPUSurfaceGetCurrentTextureStatus_Lost = 3
WGPUSurfaceGetCurrentTextureStatus_OutOfMemory = 4
WGPUSurfaceGetCurrentTextureStatus_DeviceLost = 5
WGPUSurfaceGetCurrentTextureStatus_Error = 6
WGPUSurfaceGetCurrentTextureStatus_Force32 = 2147483647
WGPUSurfaceGetCurrentTextureStatus = ctypes.c_uint32 # enum

# values for enumeration 'WGPUTextureAspect'
WGPUTextureAspect__enumvalues = {
    0: 'WGPUTextureAspect_Undefined',
    1: 'WGPUTextureAspect_All',
    2: 'WGPUTextureAspect_StencilOnly',
    3: 'WGPUTextureAspect_DepthOnly',
    4: 'WGPUTextureAspect_Plane0Only',
    5: 'WGPUTextureAspect_Plane1Only',
    6: 'WGPUTextureAspect_Plane2Only',
    2147483647: 'WGPUTextureAspect_Force32',
}
WGPUTextureAspect_Undefined = 0
WGPUTextureAspect_All = 1
WGPUTextureAspect_StencilOnly = 2
WGPUTextureAspect_DepthOnly = 3
WGPUTextureAspect_Plane0Only = 4
WGPUTextureAspect_Plane1Only = 5
WGPUTextureAspect_Plane2Only = 6
WGPUTextureAspect_Force32 = 2147483647
WGPUTextureAspect = ctypes.c_uint32 # enum

# values for enumeration 'WGPUTextureDimension'
WGPUTextureDimension__enumvalues = {
    0: 'WGPUTextureDimension_Undefined',
    1: 'WGPUTextureDimension_1D',
    2: 'WGPUTextureDimension_2D',
    3: 'WGPUTextureDimension_3D',
    2147483647: 'WGPUTextureDimension_Force32',
}
WGPUTextureDimension_Undefined = 0
WGPUTextureDimension_1D = 1
WGPUTextureDimension_2D = 2
WGPUTextureDimension_3D = 3
WGPUTextureDimension_Force32 = 2147483647
WGPUTextureDimension = ctypes.c_uint32 # enum

# values for enumeration 'WGPUTextureFormat'
WGPUTextureFormat__enumvalues = {
    0: 'WGPUTextureFormat_Undefined',
    1: 'WGPUTextureFormat_R8Unorm',
    2: 'WGPUTextureFormat_R8Snorm',
    3: 'WGPUTextureFormat_R8Uint',
    4: 'WGPUTextureFormat_R8Sint',
    5: 'WGPUTextureFormat_R16Uint',
    6: 'WGPUTextureFormat_R16Sint',
    7: 'WGPUTextureFormat_R16Float',
    8: 'WGPUTextureFormat_RG8Unorm',
    9: 'WGPUTextureFormat_RG8Snorm',
    10: 'WGPUTextureFormat_RG8Uint',
    11: 'WGPUTextureFormat_RG8Sint',
    12: 'WGPUTextureFormat_R32Float',
    13: 'WGPUTextureFormat_R32Uint',
    14: 'WGPUTextureFormat_R32Sint',
    15: 'WGPUTextureFormat_RG16Uint',
    16: 'WGPUTextureFormat_RG16Sint',
    17: 'WGPUTextureFormat_RG16Float',
    18: 'WGPUTextureFormat_RGBA8Unorm',
    19: 'WGPUTextureFormat_RGBA8UnormSrgb',
    20: 'WGPUTextureFormat_RGBA8Snorm',
    21: 'WGPUTextureFormat_RGBA8Uint',
    22: 'WGPUTextureFormat_RGBA8Sint',
    23: 'WGPUTextureFormat_BGRA8Unorm',
    24: 'WGPUTextureFormat_BGRA8UnormSrgb',
    25: 'WGPUTextureFormat_RGB10A2Uint',
    26: 'WGPUTextureFormat_RGB10A2Unorm',
    27: 'WGPUTextureFormat_RG11B10Ufloat',
    28: 'WGPUTextureFormat_RGB9E5Ufloat',
    29: 'WGPUTextureFormat_RG32Float',
    30: 'WGPUTextureFormat_RG32Uint',
    31: 'WGPUTextureFormat_RG32Sint',
    32: 'WGPUTextureFormat_RGBA16Uint',
    33: 'WGPUTextureFormat_RGBA16Sint',
    34: 'WGPUTextureFormat_RGBA16Float',
    35: 'WGPUTextureFormat_RGBA32Float',
    36: 'WGPUTextureFormat_RGBA32Uint',
    37: 'WGPUTextureFormat_RGBA32Sint',
    38: 'WGPUTextureFormat_Stencil8',
    39: 'WGPUTextureFormat_Depth16Unorm',
    40: 'WGPUTextureFormat_Depth24Plus',
    41: 'WGPUTextureFormat_Depth24PlusStencil8',
    42: 'WGPUTextureFormat_Depth32Float',
    43: 'WGPUTextureFormat_Depth32FloatStencil8',
    44: 'WGPUTextureFormat_BC1RGBAUnorm',
    45: 'WGPUTextureFormat_BC1RGBAUnormSrgb',
    46: 'WGPUTextureFormat_BC2RGBAUnorm',
    47: 'WGPUTextureFormat_BC2RGBAUnormSrgb',
    48: 'WGPUTextureFormat_BC3RGBAUnorm',
    49: 'WGPUTextureFormat_BC3RGBAUnormSrgb',
    50: 'WGPUTextureFormat_BC4RUnorm',
    51: 'WGPUTextureFormat_BC4RSnorm',
    52: 'WGPUTextureFormat_BC5RGUnorm',
    53: 'WGPUTextureFormat_BC5RGSnorm',
    54: 'WGPUTextureFormat_BC6HRGBUfloat',
    55: 'WGPUTextureFormat_BC6HRGBFloat',
    56: 'WGPUTextureFormat_BC7RGBAUnorm',
    57: 'WGPUTextureFormat_BC7RGBAUnormSrgb',
    58: 'WGPUTextureFormat_ETC2RGB8Unorm',
    59: 'WGPUTextureFormat_ETC2RGB8UnormSrgb',
    60: 'WGPUTextureFormat_ETC2RGB8A1Unorm',
    61: 'WGPUTextureFormat_ETC2RGB8A1UnormSrgb',
    62: 'WGPUTextureFormat_ETC2RGBA8Unorm',
    63: 'WGPUTextureFormat_ETC2RGBA8UnormSrgb',
    64: 'WGPUTextureFormat_EACR11Unorm',
    65: 'WGPUTextureFormat_EACR11Snorm',
    66: 'WGPUTextureFormat_EACRG11Unorm',
    67: 'WGPUTextureFormat_EACRG11Snorm',
    68: 'WGPUTextureFormat_ASTC4x4Unorm',
    69: 'WGPUTextureFormat_ASTC4x4UnormSrgb',
    70: 'WGPUTextureFormat_ASTC5x4Unorm',
    71: 'WGPUTextureFormat_ASTC5x4UnormSrgb',
    72: 'WGPUTextureFormat_ASTC5x5Unorm',
    73: 'WGPUTextureFormat_ASTC5x5UnormSrgb',
    74: 'WGPUTextureFormat_ASTC6x5Unorm',
    75: 'WGPUTextureFormat_ASTC6x5UnormSrgb',
    76: 'WGPUTextureFormat_ASTC6x6Unorm',
    77: 'WGPUTextureFormat_ASTC6x6UnormSrgb',
    78: 'WGPUTextureFormat_ASTC8x5Unorm',
    79: 'WGPUTextureFormat_ASTC8x5UnormSrgb',
    80: 'WGPUTextureFormat_ASTC8x6Unorm',
    81: 'WGPUTextureFormat_ASTC8x6UnormSrgb',
    82: 'WGPUTextureFormat_ASTC8x8Unorm',
    83: 'WGPUTextureFormat_ASTC8x8UnormSrgb',
    84: 'WGPUTextureFormat_ASTC10x5Unorm',
    85: 'WGPUTextureFormat_ASTC10x5UnormSrgb',
    86: 'WGPUTextureFormat_ASTC10x6Unorm',
    87: 'WGPUTextureFormat_ASTC10x6UnormSrgb',
    88: 'WGPUTextureFormat_ASTC10x8Unorm',
    89: 'WGPUTextureFormat_ASTC10x8UnormSrgb',
    90: 'WGPUTextureFormat_ASTC10x10Unorm',
    91: 'WGPUTextureFormat_ASTC10x10UnormSrgb',
    92: 'WGPUTextureFormat_ASTC12x10Unorm',
    93: 'WGPUTextureFormat_ASTC12x10UnormSrgb',
    94: 'WGPUTextureFormat_ASTC12x12Unorm',
    95: 'WGPUTextureFormat_ASTC12x12UnormSrgb',
    96: 'WGPUTextureFormat_R16Unorm',
    97: 'WGPUTextureFormat_RG16Unorm',
    98: 'WGPUTextureFormat_RGBA16Unorm',
    99: 'WGPUTextureFormat_R16Snorm',
    100: 'WGPUTextureFormat_RG16Snorm',
    101: 'WGPUTextureFormat_RGBA16Snorm',
    102: 'WGPUTextureFormat_R8BG8Biplanar420Unorm',
    103: 'WGPUTextureFormat_R10X6BG10X6Biplanar420Unorm',
    104: 'WGPUTextureFormat_R8BG8A8Triplanar420Unorm',
    105: 'WGPUTextureFormat_R8BG8Biplanar422Unorm',
    106: 'WGPUTextureFormat_R8BG8Biplanar444Unorm',
    107: 'WGPUTextureFormat_R10X6BG10X6Biplanar422Unorm',
    108: 'WGPUTextureFormat_R10X6BG10X6Biplanar444Unorm',
    109: 'WGPUTextureFormat_External',
    2147483647: 'WGPUTextureFormat_Force32',
}
WGPUTextureFormat_Undefined = 0
WGPUTextureFormat_R8Unorm = 1
WGPUTextureFormat_R8Snorm = 2
WGPUTextureFormat_R8Uint = 3
WGPUTextureFormat_R8Sint = 4
WGPUTextureFormat_R16Uint = 5
WGPUTextureFormat_R16Sint = 6
WGPUTextureFormat_R16Float = 7
WGPUTextureFormat_RG8Unorm = 8
WGPUTextureFormat_RG8Snorm = 9
WGPUTextureFormat_RG8Uint = 10
WGPUTextureFormat_RG8Sint = 11
WGPUTextureFormat_R32Float = 12
WGPUTextureFormat_R32Uint = 13
WGPUTextureFormat_R32Sint = 14
WGPUTextureFormat_RG16Uint = 15
WGPUTextureFormat_RG16Sint = 16
WGPUTextureFormat_RG16Float = 17
WGPUTextureFormat_RGBA8Unorm = 18
WGPUTextureFormat_RGBA8UnormSrgb = 19
WGPUTextureFormat_RGBA8Snorm = 20
WGPUTextureFormat_RGBA8Uint = 21
WGPUTextureFormat_RGBA8Sint = 22
WGPUTextureFormat_BGRA8Unorm = 23
WGPUTextureFormat_BGRA8UnormSrgb = 24
WGPUTextureFormat_RGB10A2Uint = 25
WGPUTextureFormat_RGB10A2Unorm = 26
WGPUTextureFormat_RG11B10Ufloat = 27
WGPUTextureFormat_RGB9E5Ufloat = 28
WGPUTextureFormat_RG32Float = 29
WGPUTextureFormat_RG32Uint = 30
WGPUTextureFormat_RG32Sint = 31
WGPUTextureFormat_RGBA16Uint = 32
WGPUTextureFormat_RGBA16Sint = 33
WGPUTextureFormat_RGBA16Float = 34
WGPUTextureFormat_RGBA32Float = 35
WGPUTextureFormat_RGBA32Uint = 36
WGPUTextureFormat_RGBA32Sint = 37
WGPUTextureFormat_Stencil8 = 38
WGPUTextureFormat_Depth16Unorm = 39
WGPUTextureFormat_Depth24Plus = 40
WGPUTextureFormat_Depth24PlusStencil8 = 41
WGPUTextureFormat_Depth32Float = 42
WGPUTextureFormat_Depth32FloatStencil8 = 43
WGPUTextureFormat_BC1RGBAUnorm = 44
WGPUTextureFormat_BC1RGBAUnormSrgb = 45
WGPUTextureFormat_BC2RGBAUnorm = 46
WGPUTextureFormat_BC2RGBAUnormSrgb = 47
WGPUTextureFormat_BC3RGBAUnorm = 48
WGPUTextureFormat_BC3RGBAUnormSrgb = 49
WGPUTextureFormat_BC4RUnorm = 50
WGPUTextureFormat_BC4RSnorm = 51
WGPUTextureFormat_BC5RGUnorm = 52
WGPUTextureFormat_BC5RGSnorm = 53
WGPUTextureFormat_BC6HRGBUfloat = 54
WGPUTextureFormat_BC6HRGBFloat = 55
WGPUTextureFormat_BC7RGBAUnorm = 56
WGPUTextureFormat_BC7RGBAUnormSrgb = 57
WGPUTextureFormat_ETC2RGB8Unorm = 58
WGPUTextureFormat_ETC2RGB8UnormSrgb = 59
WGPUTextureFormat_ETC2RGB8A1Unorm = 60
WGPUTextureFormat_ETC2RGB8A1UnormSrgb = 61
WGPUTextureFormat_ETC2RGBA8Unorm = 62
WGPUTextureFormat_ETC2RGBA8UnormSrgb = 63
WGPUTextureFormat_EACR11Unorm = 64
WGPUTextureFormat_EACR11Snorm = 65
WGPUTextureFormat_EACRG11Unorm = 66
WGPUTextureFormat_EACRG11Snorm = 67
WGPUTextureFormat_ASTC4x4Unorm = 68
WGPUTextureFormat_ASTC4x4UnormSrgb = 69
WGPUTextureFormat_ASTC5x4Unorm = 70
WGPUTextureFormat_ASTC5x4UnormSrgb = 71
WGPUTextureFormat_ASTC5x5Unorm = 72
WGPUTextureFormat_ASTC5x5UnormSrgb = 73
WGPUTextureFormat_ASTC6x5Unorm = 74
WGPUTextureFormat_ASTC6x5UnormSrgb = 75
WGPUTextureFormat_ASTC6x6Unorm = 76
WGPUTextureFormat_ASTC6x6UnormSrgb = 77
WGPUTextureFormat_ASTC8x5Unorm = 78
WGPUTextureFormat_ASTC8x5UnormSrgb = 79
WGPUTextureFormat_ASTC8x6Unorm = 80
WGPUTextureFormat_ASTC8x6UnormSrgb = 81
WGPUTextureFormat_ASTC8x8Unorm = 82
WGPUTextureFormat_ASTC8x8UnormSrgb = 83
WGPUTextureFormat_ASTC10x5Unorm = 84
WGPUTextureFormat_ASTC10x5UnormSrgb = 85
WGPUTextureFormat_ASTC10x6Unorm = 86
WGPUTextureFormat_ASTC10x6UnormSrgb = 87
WGPUTextureFormat_ASTC10x8Unorm = 88
WGPUTextureFormat_ASTC10x8UnormSrgb = 89
WGPUTextureFormat_ASTC10x10Unorm = 90
WGPUTextureFormat_ASTC10x10UnormSrgb = 91
WGPUTextureFormat_ASTC12x10Unorm = 92
WGPUTextureFormat_ASTC12x10UnormSrgb = 93
WGPUTextureFormat_ASTC12x12Unorm = 94
WGPUTextureFormat_ASTC12x12UnormSrgb = 95
WGPUTextureFormat_R16Unorm = 96
WGPUTextureFormat_RG16Unorm = 97
WGPUTextureFormat_RGBA16Unorm = 98
WGPUTextureFormat_R16Snorm = 99
WGPUTextureFormat_RG16Snorm = 100
WGPUTextureFormat_RGBA16Snorm = 101
WGPUTextureFormat_R8BG8Biplanar420Unorm = 102
WGPUTextureFormat_R10X6BG10X6Biplanar420Unorm = 103
WGPUTextureFormat_R8BG8A8Triplanar420Unorm = 104
WGPUTextureFormat_R8BG8Biplanar422Unorm = 105
WGPUTextureFormat_R8BG8Biplanar444Unorm = 106
WGPUTextureFormat_R10X6BG10X6Biplanar422Unorm = 107
WGPUTextureFormat_R10X6BG10X6Biplanar444Unorm = 108
WGPUTextureFormat_External = 109
WGPUTextureFormat_Force32 = 2147483647
WGPUTextureFormat = ctypes.c_uint32 # enum

# values for enumeration 'WGPUTextureSampleType'
WGPUTextureSampleType__enumvalues = {
    0: 'WGPUTextureSampleType_Undefined',
    1: 'WGPUTextureSampleType_Float',
    2: 'WGPUTextureSampleType_UnfilterableFloat',
    3: 'WGPUTextureSampleType_Depth',
    4: 'WGPUTextureSampleType_Sint',
    5: 'WGPUTextureSampleType_Uint',
    2147483647: 'WGPUTextureSampleType_Force32',
}
WGPUTextureSampleType_Undefined = 0
WGPUTextureSampleType_Float = 1
WGPUTextureSampleType_UnfilterableFloat = 2
WGPUTextureSampleType_Depth = 3
WGPUTextureSampleType_Sint = 4
WGPUTextureSampleType_Uint = 5
WGPUTextureSampleType_Force32 = 2147483647
WGPUTextureSampleType = ctypes.c_uint32 # enum

# values for enumeration 'WGPUTextureViewDimension'
WGPUTextureViewDimension__enumvalues = {
    0: 'WGPUTextureViewDimension_Undefined',
    1: 'WGPUTextureViewDimension_1D',
    2: 'WGPUTextureViewDimension_2D',
    3: 'WGPUTextureViewDimension_2DArray',
    4: 'WGPUTextureViewDimension_Cube',
    5: 'WGPUTextureViewDimension_CubeArray',
    6: 'WGPUTextureViewDimension_3D',
    2147483647: 'WGPUTextureViewDimension_Force32',
}
WGPUTextureViewDimension_Undefined = 0
WGPUTextureViewDimension_1D = 1
WGPUTextureViewDimension_2D = 2
WGPUTextureViewDimension_2DArray = 3
WGPUTextureViewDimension_Cube = 4
WGPUTextureViewDimension_CubeArray = 5
WGPUTextureViewDimension_3D = 6
WGPUTextureViewDimension_Force32 = 2147483647
WGPUTextureViewDimension = ctypes.c_uint32 # enum

# values for enumeration 'WGPUVertexFormat'
WGPUVertexFormat__enumvalues = {
    0: 'WGPUVertexFormat_Undefined',
    1: 'WGPUVertexFormat_Uint8x2',
    2: 'WGPUVertexFormat_Uint8x4',
    3: 'WGPUVertexFormat_Sint8x2',
    4: 'WGPUVertexFormat_Sint8x4',
    5: 'WGPUVertexFormat_Unorm8x2',
    6: 'WGPUVertexFormat_Unorm8x4',
    7: 'WGPUVertexFormat_Snorm8x2',
    8: 'WGPUVertexFormat_Snorm8x4',
    9: 'WGPUVertexFormat_Uint16x2',
    10: 'WGPUVertexFormat_Uint16x4',
    11: 'WGPUVertexFormat_Sint16x2',
    12: 'WGPUVertexFormat_Sint16x4',
    13: 'WGPUVertexFormat_Unorm16x2',
    14: 'WGPUVertexFormat_Unorm16x4',
    15: 'WGPUVertexFormat_Snorm16x2',
    16: 'WGPUVertexFormat_Snorm16x4',
    17: 'WGPUVertexFormat_Float16x2',
    18: 'WGPUVertexFormat_Float16x4',
    19: 'WGPUVertexFormat_Float32',
    20: 'WGPUVertexFormat_Float32x2',
    21: 'WGPUVertexFormat_Float32x3',
    22: 'WGPUVertexFormat_Float32x4',
    23: 'WGPUVertexFormat_Uint32',
    24: 'WGPUVertexFormat_Uint32x2',
    25: 'WGPUVertexFormat_Uint32x3',
    26: 'WGPUVertexFormat_Uint32x4',
    27: 'WGPUVertexFormat_Sint32',
    28: 'WGPUVertexFormat_Sint32x2',
    29: 'WGPUVertexFormat_Sint32x3',
    30: 'WGPUVertexFormat_Sint32x4',
    31: 'WGPUVertexFormat_Unorm10_10_10_2',
    2147483647: 'WGPUVertexFormat_Force32',
}
WGPUVertexFormat_Undefined = 0
WGPUVertexFormat_Uint8x2 = 1
WGPUVertexFormat_Uint8x4 = 2
WGPUVertexFormat_Sint8x2 = 3
WGPUVertexFormat_Sint8x4 = 4
WGPUVertexFormat_Unorm8x2 = 5
WGPUVertexFormat_Unorm8x4 = 6
WGPUVertexFormat_Snorm8x2 = 7
WGPUVertexFormat_Snorm8x4 = 8
WGPUVertexFormat_Uint16x2 = 9
WGPUVertexFormat_Uint16x4 = 10
WGPUVertexFormat_Sint16x2 = 11
WGPUVertexFormat_Sint16x4 = 12
WGPUVertexFormat_Unorm16x2 = 13
WGPUVertexFormat_Unorm16x4 = 14
WGPUVertexFormat_Snorm16x2 = 15
WGPUVertexFormat_Snorm16x4 = 16
WGPUVertexFormat_Float16x2 = 17
WGPUVertexFormat_Float16x4 = 18
WGPUVertexFormat_Float32 = 19
WGPUVertexFormat_Float32x2 = 20
WGPUVertexFormat_Float32x3 = 21
WGPUVertexFormat_Float32x4 = 22
WGPUVertexFormat_Uint32 = 23
WGPUVertexFormat_Uint32x2 = 24
WGPUVertexFormat_Uint32x3 = 25
WGPUVertexFormat_Uint32x4 = 26
WGPUVertexFormat_Sint32 = 27
WGPUVertexFormat_Sint32x2 = 28
WGPUVertexFormat_Sint32x3 = 29
WGPUVertexFormat_Sint32x4 = 30
WGPUVertexFormat_Unorm10_10_10_2 = 31
WGPUVertexFormat_Force32 = 2147483647
WGPUVertexFormat = ctypes.c_uint32 # enum

# values for enumeration 'WGPUVertexStepMode'
WGPUVertexStepMode__enumvalues = {
    0: 'WGPUVertexStepMode_Undefined',
    1: 'WGPUVertexStepMode_VertexBufferNotUsed',
    2: 'WGPUVertexStepMode_Vertex',
    3: 'WGPUVertexStepMode_Instance',
    2147483647: 'WGPUVertexStepMode_Force32',
}
WGPUVertexStepMode_Undefined = 0
WGPUVertexStepMode_VertexBufferNotUsed = 1
WGPUVertexStepMode_Vertex = 2
WGPUVertexStepMode_Instance = 3
WGPUVertexStepMode_Force32 = 2147483647
WGPUVertexStepMode = ctypes.c_uint32 # enum

# values for enumeration 'WGPUWaitStatus'
WGPUWaitStatus__enumvalues = {
    0: 'WGPUWaitStatus_Success',
    1: 'WGPUWaitStatus_TimedOut',
    2: 'WGPUWaitStatus_UnsupportedTimeout',
    3: 'WGPUWaitStatus_UnsupportedCount',
    4: 'WGPUWaitStatus_UnsupportedMixedSources',
    5: 'WGPUWaitStatus_Unknown',
    2147483647: 'WGPUWaitStatus_Force32',
}
WGPUWaitStatus_Success = 0
WGPUWaitStatus_TimedOut = 1
WGPUWaitStatus_UnsupportedTimeout = 2
WGPUWaitStatus_UnsupportedCount = 3
WGPUWaitStatus_UnsupportedMixedSources = 4
WGPUWaitStatus_Unknown = 5
WGPUWaitStatus_Force32 = 2147483647
WGPUWaitStatus = ctypes.c_uint32 # enum

# values for enumeration 'WGPUBufferUsage'
WGPUBufferUsage__enumvalues = {
    0: 'WGPUBufferUsage_None',
    1: 'WGPUBufferUsage_MapRead',
    2: 'WGPUBufferUsage_MapWrite',
    4: 'WGPUBufferUsage_CopySrc',
    8: 'WGPUBufferUsage_CopyDst',
    16: 'WGPUBufferUsage_Index',
    32: 'WGPUBufferUsage_Vertex',
    64: 'WGPUBufferUsage_Uniform',
    128: 'WGPUBufferUsage_Storage',
    256: 'WGPUBufferUsage_Indirect',
    512: 'WGPUBufferUsage_QueryResolve',
    2147483647: 'WGPUBufferUsage_Force32',
}
WGPUBufferUsage_None = 0
WGPUBufferUsage_MapRead = 1
WGPUBufferUsage_MapWrite = 2
WGPUBufferUsage_CopySrc = 4
WGPUBufferUsage_CopyDst = 8
WGPUBufferUsage_Index = 16
WGPUBufferUsage_Vertex = 32
WGPUBufferUsage_Uniform = 64
WGPUBufferUsage_Storage = 128
WGPUBufferUsage_Indirect = 256
WGPUBufferUsage_QueryResolve = 512
WGPUBufferUsage_Force32 = 2147483647
WGPUBufferUsage = ctypes.c_uint32 # enum
WGPUBufferUsageFlags = ctypes.c_uint32

# values for enumeration 'WGPUColorWriteMask'
WGPUColorWriteMask__enumvalues = {
    0: 'WGPUColorWriteMask_None',
    1: 'WGPUColorWriteMask_Red',
    2: 'WGPUColorWriteMask_Green',
    4: 'WGPUColorWriteMask_Blue',
    8: 'WGPUColorWriteMask_Alpha',
    15: 'WGPUColorWriteMask_All',
    2147483647: 'WGPUColorWriteMask_Force32',
}
WGPUColorWriteMask_None = 0
WGPUColorWriteMask_Red = 1
WGPUColorWriteMask_Green = 2
WGPUColorWriteMask_Blue = 4
WGPUColorWriteMask_Alpha = 8
WGPUColorWriteMask_All = 15
WGPUColorWriteMask_Force32 = 2147483647
WGPUColorWriteMask = ctypes.c_uint32 # enum
WGPUColorWriteMaskFlags = ctypes.c_uint32

# values for enumeration 'WGPUHeapProperty'
WGPUHeapProperty__enumvalues = {
    0: 'WGPUHeapProperty_Undefined',
    1: 'WGPUHeapProperty_DeviceLocal',
    2: 'WGPUHeapProperty_HostVisible',
    4: 'WGPUHeapProperty_HostCoherent',
    8: 'WGPUHeapProperty_HostUncached',
    16: 'WGPUHeapProperty_HostCached',
    2147483647: 'WGPUHeapProperty_Force32',
}
WGPUHeapProperty_Undefined = 0
WGPUHeapProperty_DeviceLocal = 1
WGPUHeapProperty_HostVisible = 2
WGPUHeapProperty_HostCoherent = 4
WGPUHeapProperty_HostUncached = 8
WGPUHeapProperty_HostCached = 16
WGPUHeapProperty_Force32 = 2147483647
WGPUHeapProperty = ctypes.c_uint32 # enum
WGPUHeapPropertyFlags = ctypes.c_uint32

# values for enumeration 'WGPUMapMode'
WGPUMapMode__enumvalues = {
    0: 'WGPUMapMode_None',
    1: 'WGPUMapMode_Read',
    2: 'WGPUMapMode_Write',
    2147483647: 'WGPUMapMode_Force32',
}
WGPUMapMode_None = 0
WGPUMapMode_Read = 1
WGPUMapMode_Write = 2
WGPUMapMode_Force32 = 2147483647
WGPUMapMode = ctypes.c_uint32 # enum
WGPUMapModeFlags = ctypes.c_uint32

# values for enumeration 'WGPUShaderStage'
WGPUShaderStage__enumvalues = {
    0: 'WGPUShaderStage_None',
    1: 'WGPUShaderStage_Vertex',
    2: 'WGPUShaderStage_Fragment',
    4: 'WGPUShaderStage_Compute',
    2147483647: 'WGPUShaderStage_Force32',
}
WGPUShaderStage_None = 0
WGPUShaderStage_Vertex = 1
WGPUShaderStage_Fragment = 2
WGPUShaderStage_Compute = 4
WGPUShaderStage_Force32 = 2147483647
WGPUShaderStage = ctypes.c_uint32 # enum
WGPUShaderStageFlags = ctypes.c_uint32

# values for enumeration 'WGPUTextureUsage'
WGPUTextureUsage__enumvalues = {
    0: 'WGPUTextureUsage_None',
    1: 'WGPUTextureUsage_CopySrc',
    2: 'WGPUTextureUsage_CopyDst',
    4: 'WGPUTextureUsage_TextureBinding',
    8: 'WGPUTextureUsage_StorageBinding',
    16: 'WGPUTextureUsage_RenderAttachment',
    32: 'WGPUTextureUsage_TransientAttachment',
    64: 'WGPUTextureUsage_StorageAttachment',
    2147483647: 'WGPUTextureUsage_Force32',
}
WGPUTextureUsage_None = 0
WGPUTextureUsage_CopySrc = 1
WGPUTextureUsage_CopyDst = 2
WGPUTextureUsage_TextureBinding = 4
WGPUTextureUsage_StorageBinding = 8
WGPUTextureUsage_RenderAttachment = 16
WGPUTextureUsage_TransientAttachment = 32
WGPUTextureUsage_StorageAttachment = 64
WGPUTextureUsage_Force32 = 2147483647
WGPUTextureUsage = ctypes.c_uint32 # enum
WGPUTextureUsageFlags = ctypes.c_uint32
WGPUBufferMapCallback = ctypes.CFUNCTYPE(None, WGPUBufferMapAsyncStatus, ctypes.POINTER(None))
WGPUCallback = ctypes.CFUNCTYPE(None, ctypes.POINTER(None))
class struct_WGPUCompilationInfo(Structure):
    pass

WGPUCompilationInfoCallback = ctypes.CFUNCTYPE(None, WGPUCompilationInfoRequestStatus, ctypes.POINTER(struct_WGPUCompilationInfo), ctypes.POINTER(None))
WGPUCreateComputePipelineAsyncCallback = ctypes.CFUNCTYPE(None, WGPUCreatePipelineAsyncStatus, ctypes.POINTER(struct_WGPUComputePipelineImpl), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None))
WGPUCreateRenderPipelineAsyncCallback = ctypes.CFUNCTYPE(None, WGPUCreatePipelineAsyncStatus, ctypes.POINTER(struct_WGPURenderPipelineImpl), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None))
WGPUDawnLoadCacheDataFunction = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.POINTER(None), ctypes.c_uint64, ctypes.POINTER(None), ctypes.c_uint64, ctypes.POINTER(None))
WGPUDawnStoreCacheDataFunction = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.c_uint64, ctypes.POINTER(None), ctypes.c_uint64, ctypes.POINTER(None))
WGPUDeviceLostCallback = ctypes.CFUNCTYPE(None, WGPUDeviceLostReason, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None))
WGPUDeviceLostCallbackNew = ctypes.CFUNCTYPE(None, ctypes.POINTER(ctypes.POINTER(struct_WGPUDeviceImpl)), WGPUDeviceLostReason, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None))
WGPUErrorCallback = ctypes.CFUNCTYPE(None, WGPUErrorType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None))
WGPULoggingCallback = ctypes.CFUNCTYPE(None, WGPULoggingType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None))
WGPUPopErrorScopeCallback = ctypes.CFUNCTYPE(None, WGPUPopErrorScopeStatus, WGPUErrorType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None))
WGPUProc = ctypes.CFUNCTYPE(None)
WGPUQueueWorkDoneCallback = ctypes.CFUNCTYPE(None, WGPUQueueWorkDoneStatus, ctypes.POINTER(None))
WGPURequestAdapterCallback = ctypes.CFUNCTYPE(None, WGPURequestAdapterStatus, ctypes.POINTER(struct_WGPUAdapterImpl), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None))
WGPURequestDeviceCallback = ctypes.CFUNCTYPE(None, WGPURequestDeviceStatus, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None))
WGPUBufferMapCallback2 = ctypes.CFUNCTYPE(None, WGPUMapAsyncStatus, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), ctypes.POINTER(None))
WGPUCompilationInfoCallback2 = ctypes.CFUNCTYPE(None, WGPUCompilationInfoRequestStatus, ctypes.POINTER(struct_WGPUCompilationInfo), ctypes.POINTER(None), ctypes.POINTER(None))
WGPUCreateComputePipelineAsyncCallback2 = ctypes.CFUNCTYPE(None, WGPUCreatePipelineAsyncStatus, ctypes.POINTER(struct_WGPUComputePipelineImpl), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), ctypes.POINTER(None))
WGPUCreateRenderPipelineAsyncCallback2 = ctypes.CFUNCTYPE(None, WGPUCreatePipelineAsyncStatus, ctypes.POINTER(struct_WGPURenderPipelineImpl), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), ctypes.POINTER(None))
WGPUPopErrorScopeCallback2 = ctypes.CFUNCTYPE(None, WGPUPopErrorScopeStatus, WGPUErrorType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), ctypes.POINTER(None))
WGPUQueueWorkDoneCallback2 = ctypes.CFUNCTYPE(None, WGPUQueueWorkDoneStatus, ctypes.POINTER(None), ctypes.POINTER(None))
WGPURequestAdapterCallback2 = ctypes.CFUNCTYPE(None, WGPURequestAdapterStatus, ctypes.POINTER(struct_WGPUAdapterImpl), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), ctypes.POINTER(None))
WGPURequestDeviceCallback2 = ctypes.CFUNCTYPE(None, WGPURequestDeviceStatus, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), ctypes.POINTER(None))
class struct_WGPUChainedStruct(Structure):
    pass

struct_WGPUChainedStruct._pack_ = 1 # source:False
struct_WGPUChainedStruct._fields_ = [
    ('next', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('sType', WGPUSType),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUChainedStruct = struct_WGPUChainedStruct
class struct_WGPUChainedStructOut(Structure):
    pass

struct_WGPUChainedStructOut._pack_ = 1 # source:False
struct_WGPUChainedStructOut._fields_ = [
    ('next', ctypes.POINTER(struct_WGPUChainedStructOut)),
    ('sType', WGPUSType),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUChainedStructOut = struct_WGPUChainedStructOut
class struct_WGPUAdapterInfo(Structure):
    pass

struct_WGPUAdapterInfo._pack_ = 1 # source:False
struct_WGPUAdapterInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStructOut)),
    ('vendor', ctypes.POINTER(ctypes.c_char)),
    ('architecture', ctypes.POINTER(ctypes.c_char)),
    ('device', ctypes.POINTER(ctypes.c_char)),
    ('description', ctypes.POINTER(ctypes.c_char)),
    ('backendType', WGPUBackendType),
    ('adapterType', WGPUAdapterType),
    ('vendorID', ctypes.c_uint32),
    ('deviceID', ctypes.c_uint32),
]

WGPUAdapterInfo = struct_WGPUAdapterInfo
class struct_WGPUAdapterProperties(Structure):
    pass

struct_WGPUAdapterProperties._pack_ = 1 # source:False
struct_WGPUAdapterProperties._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStructOut)),
    ('vendorID', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('vendorName', ctypes.POINTER(ctypes.c_char)),
    ('architecture', ctypes.POINTER(ctypes.c_char)),
    ('deviceID', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('name', ctypes.POINTER(ctypes.c_char)),
    ('driverDescription', ctypes.POINTER(ctypes.c_char)),
    ('adapterType', WGPUAdapterType),
    ('backendType', WGPUBackendType),
    ('compatibilityMode', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
]

WGPUAdapterProperties = struct_WGPUAdapterProperties
class struct_WGPUAdapterPropertiesD3D(Structure):
    pass

struct_WGPUAdapterPropertiesD3D._pack_ = 1 # source:False
struct_WGPUAdapterPropertiesD3D._fields_ = [
    ('chain', WGPUChainedStructOut),
    ('shaderModel', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUAdapterPropertiesD3D = struct_WGPUAdapterPropertiesD3D
class struct_WGPUAdapterPropertiesVk(Structure):
    pass

struct_WGPUAdapterPropertiesVk._pack_ = 1 # source:False
struct_WGPUAdapterPropertiesVk._fields_ = [
    ('chain', WGPUChainedStructOut),
    ('driverVersion', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUAdapterPropertiesVk = struct_WGPUAdapterPropertiesVk
class struct_WGPUBindGroupEntry(Structure):
    pass

struct_WGPUBindGroupEntry._pack_ = 1 # source:False
struct_WGPUBindGroupEntry._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('binding', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('buffer', ctypes.POINTER(struct_WGPUBufferImpl)),
    ('offset', ctypes.c_uint64),
    ('size', ctypes.c_uint64),
    ('sampler', ctypes.POINTER(struct_WGPUSamplerImpl)),
    ('textureView', ctypes.POINTER(struct_WGPUTextureViewImpl)),
]

WGPUBindGroupEntry = struct_WGPUBindGroupEntry
class struct_WGPUBlendComponent(Structure):
    _pack_ = 1 # source:False
    _fields_ = [
    ('operation', WGPUBlendOperation),
    ('srcFactor', WGPUBlendFactor),
    ('dstFactor', WGPUBlendFactor),
     ]

WGPUBlendComponent = struct_WGPUBlendComponent
class struct_WGPUBufferBindingLayout(Structure):
    pass

struct_WGPUBufferBindingLayout._pack_ = 1 # source:False
struct_WGPUBufferBindingLayout._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('type', WGPUBufferBindingType),
    ('hasDynamicOffset', ctypes.c_uint32),
    ('minBindingSize', ctypes.c_uint64),
]

WGPUBufferBindingLayout = struct_WGPUBufferBindingLayout
class struct_WGPUBufferDescriptor(Structure):
    pass

struct_WGPUBufferDescriptor._pack_ = 1 # source:False
struct_WGPUBufferDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', ctypes.POINTER(ctypes.c_char)),
    ('usage', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('size', ctypes.c_uint64),
    ('mappedAtCreation', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
]

WGPUBufferDescriptor = struct_WGPUBufferDescriptor
class struct_WGPUBufferHostMappedPointer(Structure):
    pass

struct_WGPUBufferHostMappedPointer._pack_ = 1 # source:False
struct_WGPUBufferHostMappedPointer._fields_ = [
    ('chain', WGPUChainedStruct),
    ('pointer', ctypes.POINTER(None)),
    ('disposeCallback', ctypes.CFUNCTYPE(None, ctypes.POINTER(None))),
    ('userdata', ctypes.POINTER(None)),
]

WGPUBufferHostMappedPointer = struct_WGPUBufferHostMappedPointer
class struct_WGPUBufferMapCallbackInfo(Structure):
    pass

struct_WGPUBufferMapCallbackInfo._pack_ = 1 # source:False
struct_WGPUBufferMapCallbackInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, WGPUBufferMapAsyncStatus, ctypes.POINTER(None))),
    ('userdata', ctypes.POINTER(None)),
]

WGPUBufferMapCallbackInfo = struct_WGPUBufferMapCallbackInfo
class struct_WGPUColor(Structure):
    pass

struct_WGPUColor._pack_ = 1 # source:False
struct_WGPUColor._fields_ = [
    ('r', ctypes.c_double),
    ('g', ctypes.c_double),
    ('b', ctypes.c_double),
    ('a', ctypes.c_double),
]

WGPUColor = struct_WGPUColor
class struct_WGPUColorTargetStateExpandResolveTextureDawn(Structure):
    pass

struct_WGPUColorTargetStateExpandResolveTextureDawn._pack_ = 1 # source:False
struct_WGPUColorTargetStateExpandResolveTextureDawn._fields_ = [
    ('chain', WGPUChainedStruct),
    ('enabled', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUColorTargetStateExpandResolveTextureDawn = struct_WGPUColorTargetStateExpandResolveTextureDawn
class struct_WGPUCommandBufferDescriptor(Structure):
    pass

struct_WGPUCommandBufferDescriptor._pack_ = 1 # source:False
struct_WGPUCommandBufferDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', ctypes.POINTER(ctypes.c_char)),
]

WGPUCommandBufferDescriptor = struct_WGPUCommandBufferDescriptor
class struct_WGPUCommandEncoderDescriptor(Structure):
    pass

struct_WGPUCommandEncoderDescriptor._pack_ = 1 # source:False
struct_WGPUCommandEncoderDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', ctypes.POINTER(ctypes.c_char)),
]

WGPUCommandEncoderDescriptor = struct_WGPUCommandEncoderDescriptor
class struct_WGPUCompilationInfoCallbackInfo(Structure):
    pass

struct_WGPUCompilationInfoCallbackInfo._pack_ = 1 # source:False
struct_WGPUCompilationInfoCallbackInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, WGPUCompilationInfoRequestStatus, ctypes.POINTER(struct_WGPUCompilationInfo), ctypes.POINTER(None))),
    ('userdata', ctypes.POINTER(None)),
]

WGPUCompilationInfoCallbackInfo = struct_WGPUCompilationInfoCallbackInfo
class struct_WGPUCompilationMessage(Structure):
    pass

struct_WGPUCompilationMessage._pack_ = 1 # source:False
struct_WGPUCompilationMessage._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('message', ctypes.POINTER(ctypes.c_char)),
    ('type', WGPUCompilationMessageType),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('lineNum', ctypes.c_uint64),
    ('linePos', ctypes.c_uint64),
    ('offset', ctypes.c_uint64),
    ('length', ctypes.c_uint64),
    ('utf16LinePos', ctypes.c_uint64),
    ('utf16Offset', ctypes.c_uint64),
    ('utf16Length', ctypes.c_uint64),
]

WGPUCompilationMessage = struct_WGPUCompilationMessage
class struct_WGPUComputePassTimestampWrites(Structure):
    pass

struct_WGPUComputePassTimestampWrites._pack_ = 1 # source:False
struct_WGPUComputePassTimestampWrites._fields_ = [
    ('querySet', ctypes.POINTER(struct_WGPUQuerySetImpl)),
    ('beginningOfPassWriteIndex', ctypes.c_uint32),
    ('endOfPassWriteIndex', ctypes.c_uint32),
]

WGPUComputePassTimestampWrites = struct_WGPUComputePassTimestampWrites
class struct_WGPUConstantEntry(Structure):
    pass

struct_WGPUConstantEntry._pack_ = 1 # source:False
struct_WGPUConstantEntry._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('key', ctypes.POINTER(ctypes.c_char)),
    ('value', ctypes.c_double),
]

WGPUConstantEntry = struct_WGPUConstantEntry
class struct_WGPUCopyTextureForBrowserOptions(Structure):
    pass

struct_WGPUCopyTextureForBrowserOptions._pack_ = 1 # source:False
struct_WGPUCopyTextureForBrowserOptions._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('flipY', ctypes.c_uint32),
    ('needsColorSpaceConversion', ctypes.c_uint32),
    ('srcAlphaMode', WGPUAlphaMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('srcTransferFunctionParameters', ctypes.POINTER(ctypes.c_float)),
    ('conversionMatrix', ctypes.POINTER(ctypes.c_float)),
    ('dstTransferFunctionParameters', ctypes.POINTER(ctypes.c_float)),
    ('dstAlphaMode', WGPUAlphaMode),
    ('internalUsage', ctypes.c_uint32),
]

WGPUCopyTextureForBrowserOptions = struct_WGPUCopyTextureForBrowserOptions
class struct_WGPUCreateComputePipelineAsyncCallbackInfo(Structure):
    pass

struct_WGPUCreateComputePipelineAsyncCallbackInfo._pack_ = 1 # source:False
struct_WGPUCreateComputePipelineAsyncCallbackInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, WGPUCreatePipelineAsyncStatus, ctypes.POINTER(struct_WGPUComputePipelineImpl), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None))),
    ('userdata', ctypes.POINTER(None)),
]

WGPUCreateComputePipelineAsyncCallbackInfo = struct_WGPUCreateComputePipelineAsyncCallbackInfo
class struct_WGPUCreateRenderPipelineAsyncCallbackInfo(Structure):
    pass

struct_WGPUCreateRenderPipelineAsyncCallbackInfo._pack_ = 1 # source:False
struct_WGPUCreateRenderPipelineAsyncCallbackInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, WGPUCreatePipelineAsyncStatus, ctypes.POINTER(struct_WGPURenderPipelineImpl), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None))),
    ('userdata', ctypes.POINTER(None)),
]

WGPUCreateRenderPipelineAsyncCallbackInfo = struct_WGPUCreateRenderPipelineAsyncCallbackInfo
class struct_WGPUDawnWGSLBlocklist(Structure):
    pass

struct_WGPUDawnWGSLBlocklist._pack_ = 1 # source:False
struct_WGPUDawnWGSLBlocklist._fields_ = [
    ('chain', WGPUChainedStruct),
    ('blocklistedFeatureCount', ctypes.c_uint64),
    ('blocklistedFeatures', ctypes.POINTER(ctypes.POINTER(ctypes.c_char))),
]

WGPUDawnWGSLBlocklist = struct_WGPUDawnWGSLBlocklist
class struct_WGPUDawnAdapterPropertiesPowerPreference(Structure):
    pass

struct_WGPUDawnAdapterPropertiesPowerPreference._pack_ = 1 # source:False
struct_WGPUDawnAdapterPropertiesPowerPreference._fields_ = [
    ('chain', WGPUChainedStructOut),
    ('powerPreference', WGPUPowerPreference),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUDawnAdapterPropertiesPowerPreference = struct_WGPUDawnAdapterPropertiesPowerPreference
class struct_WGPUDawnBufferDescriptorErrorInfoFromWireClient(Structure):
    pass

struct_WGPUDawnBufferDescriptorErrorInfoFromWireClient._pack_ = 1 # source:False
struct_WGPUDawnBufferDescriptorErrorInfoFromWireClient._fields_ = [
    ('chain', WGPUChainedStruct),
    ('outOfMemory', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUDawnBufferDescriptorErrorInfoFromWireClient = struct_WGPUDawnBufferDescriptorErrorInfoFromWireClient
class struct_WGPUDawnCacheDeviceDescriptor(Structure):
    pass

struct_WGPUDawnCacheDeviceDescriptor._pack_ = 1 # source:False
struct_WGPUDawnCacheDeviceDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('isolationKey', ctypes.POINTER(ctypes.c_char)),
    ('loadDataFunction', ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.POINTER(None), ctypes.c_uint64, ctypes.POINTER(None), ctypes.c_uint64, ctypes.POINTER(None))),
    ('storeDataFunction', ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.c_uint64, ctypes.POINTER(None), ctypes.c_uint64, ctypes.POINTER(None))),
    ('functionUserdata', ctypes.POINTER(None)),
]

WGPUDawnCacheDeviceDescriptor = struct_WGPUDawnCacheDeviceDescriptor
class struct_WGPUDawnComputePipelineFullSubgroups(Structure):
    pass

struct_WGPUDawnComputePipelineFullSubgroups._pack_ = 1 # source:False
struct_WGPUDawnComputePipelineFullSubgroups._fields_ = [
    ('chain', WGPUChainedStruct),
    ('requiresFullSubgroups', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUDawnComputePipelineFullSubgroups = struct_WGPUDawnComputePipelineFullSubgroups
class struct_WGPUDawnEncoderInternalUsageDescriptor(Structure):
    pass

struct_WGPUDawnEncoderInternalUsageDescriptor._pack_ = 1 # source:False
struct_WGPUDawnEncoderInternalUsageDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('useInternalUsages', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUDawnEncoderInternalUsageDescriptor = struct_WGPUDawnEncoderInternalUsageDescriptor
class struct_WGPUDawnExperimentalSubgroupLimits(Structure):
    pass

struct_WGPUDawnExperimentalSubgroupLimits._pack_ = 1 # source:False
struct_WGPUDawnExperimentalSubgroupLimits._fields_ = [
    ('chain', WGPUChainedStructOut),
    ('minSubgroupSize', ctypes.c_uint32),
    ('maxSubgroupSize', ctypes.c_uint32),
]

WGPUDawnExperimentalSubgroupLimits = struct_WGPUDawnExperimentalSubgroupLimits
class struct_WGPUDawnRenderPassColorAttachmentRenderToSingleSampled(Structure):
    pass

struct_WGPUDawnRenderPassColorAttachmentRenderToSingleSampled._pack_ = 1 # source:False
struct_WGPUDawnRenderPassColorAttachmentRenderToSingleSampled._fields_ = [
    ('chain', WGPUChainedStruct),
    ('implicitSampleCount', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUDawnRenderPassColorAttachmentRenderToSingleSampled = struct_WGPUDawnRenderPassColorAttachmentRenderToSingleSampled
class struct_WGPUDawnShaderModuleSPIRVOptionsDescriptor(Structure):
    pass

struct_WGPUDawnShaderModuleSPIRVOptionsDescriptor._pack_ = 1 # source:False
struct_WGPUDawnShaderModuleSPIRVOptionsDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('allowNonUniformDerivatives', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUDawnShaderModuleSPIRVOptionsDescriptor = struct_WGPUDawnShaderModuleSPIRVOptionsDescriptor
class struct_WGPUDawnTextureInternalUsageDescriptor(Structure):
    pass

struct_WGPUDawnTextureInternalUsageDescriptor._pack_ = 1 # source:False
struct_WGPUDawnTextureInternalUsageDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('internalUsage', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUDawnTextureInternalUsageDescriptor = struct_WGPUDawnTextureInternalUsageDescriptor
class struct_WGPUDawnTogglesDescriptor(Structure):
    pass

struct_WGPUDawnTogglesDescriptor._pack_ = 1 # source:False
struct_WGPUDawnTogglesDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('enabledToggleCount', ctypes.c_uint64),
    ('enabledToggles', ctypes.POINTER(ctypes.POINTER(ctypes.c_char))),
    ('disabledToggleCount', ctypes.c_uint64),
    ('disabledToggles', ctypes.POINTER(ctypes.POINTER(ctypes.c_char))),
]

WGPUDawnTogglesDescriptor = struct_WGPUDawnTogglesDescriptor
class struct_WGPUDawnWireWGSLControl(Structure):
    pass

struct_WGPUDawnWireWGSLControl._pack_ = 1 # source:False
struct_WGPUDawnWireWGSLControl._fields_ = [
    ('chain', WGPUChainedStruct),
    ('enableExperimental', ctypes.c_uint32),
    ('enableUnsafe', ctypes.c_uint32),
    ('enableTesting', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUDawnWireWGSLControl = struct_WGPUDawnWireWGSLControl
class struct_WGPUDepthStencilStateDepthWriteDefinedDawn(Structure):
    pass

struct_WGPUDepthStencilStateDepthWriteDefinedDawn._pack_ = 1 # source:False
struct_WGPUDepthStencilStateDepthWriteDefinedDawn._fields_ = [
    ('chain', WGPUChainedStruct),
    ('depthWriteDefined', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUDepthStencilStateDepthWriteDefinedDawn = struct_WGPUDepthStencilStateDepthWriteDefinedDawn
class struct_WGPUDeviceLostCallbackInfo(Structure):
    pass

struct_WGPUDeviceLostCallbackInfo._pack_ = 1 # source:False
struct_WGPUDeviceLostCallbackInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, ctypes.POINTER(ctypes.POINTER(struct_WGPUDeviceImpl)), WGPUDeviceLostReason, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None))),
    ('userdata', ctypes.POINTER(None)),
]

WGPUDeviceLostCallbackInfo = struct_WGPUDeviceLostCallbackInfo
class struct_WGPUDrmFormatProperties(Structure):
    pass

struct_WGPUDrmFormatProperties._pack_ = 1 # source:False
struct_WGPUDrmFormatProperties._fields_ = [
    ('modifier', ctypes.c_uint64),
    ('modifierPlaneCount', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUDrmFormatProperties = struct_WGPUDrmFormatProperties
class struct_WGPUExtent2D(Structure):
    pass

struct_WGPUExtent2D._pack_ = 1 # source:False
struct_WGPUExtent2D._fields_ = [
    ('width', ctypes.c_uint32),
    ('height', ctypes.c_uint32),
]

WGPUExtent2D = struct_WGPUExtent2D
class struct_WGPUExtent3D(Structure):
    pass

struct_WGPUExtent3D._pack_ = 1 # source:False
struct_WGPUExtent3D._fields_ = [
    ('width', ctypes.c_uint32),
    ('height', ctypes.c_uint32),
    ('depthOrArrayLayers', ctypes.c_uint32),
]

WGPUExtent3D = struct_WGPUExtent3D
class struct_WGPUExternalTextureBindingEntry(Structure):
    pass

struct_WGPUExternalTextureBindingEntry._pack_ = 1 # source:False
struct_WGPUExternalTextureBindingEntry._fields_ = [
    ('chain', WGPUChainedStruct),
    ('externalTexture', ctypes.POINTER(struct_WGPUExternalTextureImpl)),
]

WGPUExternalTextureBindingEntry = struct_WGPUExternalTextureBindingEntry
class struct_WGPUExternalTextureBindingLayout(Structure):
    _pack_ = 1 # source:False
    _fields_ = [
    ('chain', WGPUChainedStruct),
     ]

WGPUExternalTextureBindingLayout = struct_WGPUExternalTextureBindingLayout
class struct_WGPUFormatCapabilities(Structure):
    pass

struct_WGPUFormatCapabilities._pack_ = 1 # source:False
struct_WGPUFormatCapabilities._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStructOut)),
]

WGPUFormatCapabilities = struct_WGPUFormatCapabilities
class struct_WGPUFuture(Structure):
    pass

struct_WGPUFuture._pack_ = 1 # source:False
struct_WGPUFuture._fields_ = [
    ('id', ctypes.c_uint64),
]

WGPUFuture = struct_WGPUFuture
class struct_WGPUInstanceFeatures(Structure):
    pass

struct_WGPUInstanceFeatures._pack_ = 1 # source:False
struct_WGPUInstanceFeatures._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('timedWaitAnyEnable', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('timedWaitAnyMaxCount', ctypes.c_uint64),
]

WGPUInstanceFeatures = struct_WGPUInstanceFeatures
class struct_WGPULimits(Structure):
    pass

struct_WGPULimits._pack_ = 1 # source:False
struct_WGPULimits._fields_ = [
    ('maxTextureDimension1D', ctypes.c_uint32),
    ('maxTextureDimension2D', ctypes.c_uint32),
    ('maxTextureDimension3D', ctypes.c_uint32),
    ('maxTextureArrayLayers', ctypes.c_uint32),
    ('maxBindGroups', ctypes.c_uint32),
    ('maxBindGroupsPlusVertexBuffers', ctypes.c_uint32),
    ('maxBindingsPerBindGroup', ctypes.c_uint32),
    ('maxDynamicUniformBuffersPerPipelineLayout', ctypes.c_uint32),
    ('maxDynamicStorageBuffersPerPipelineLayout', ctypes.c_uint32),
    ('maxSampledTexturesPerShaderStage', ctypes.c_uint32),
    ('maxSamplersPerShaderStage', ctypes.c_uint32),
    ('maxStorageBuffersPerShaderStage', ctypes.c_uint32),
    ('maxStorageTexturesPerShaderStage', ctypes.c_uint32),
    ('maxUniformBuffersPerShaderStage', ctypes.c_uint32),
    ('maxUniformBufferBindingSize', ctypes.c_uint64),
    ('maxStorageBufferBindingSize', ctypes.c_uint64),
    ('minUniformBufferOffsetAlignment', ctypes.c_uint32),
    ('minStorageBufferOffsetAlignment', ctypes.c_uint32),
    ('maxVertexBuffers', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('maxBufferSize', ctypes.c_uint64),
    ('maxVertexAttributes', ctypes.c_uint32),
    ('maxVertexBufferArrayStride', ctypes.c_uint32),
    ('maxInterStageShaderComponents', ctypes.c_uint32),
    ('maxInterStageShaderVariables', ctypes.c_uint32),
    ('maxColorAttachments', ctypes.c_uint32),
    ('maxColorAttachmentBytesPerSample', ctypes.c_uint32),
    ('maxComputeWorkgroupStorageSize', ctypes.c_uint32),
    ('maxComputeInvocationsPerWorkgroup', ctypes.c_uint32),
    ('maxComputeWorkgroupSizeX', ctypes.c_uint32),
    ('maxComputeWorkgroupSizeY', ctypes.c_uint32),
    ('maxComputeWorkgroupSizeZ', ctypes.c_uint32),
    ('maxComputeWorkgroupsPerDimension', ctypes.c_uint32),
]

WGPULimits = struct_WGPULimits
class struct_WGPUMemoryHeapInfo(Structure):
    pass

struct_WGPUMemoryHeapInfo._pack_ = 1 # source:False
struct_WGPUMemoryHeapInfo._fields_ = [
    ('properties', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('size', ctypes.c_uint64),
]

WGPUMemoryHeapInfo = struct_WGPUMemoryHeapInfo
class struct_WGPUMultisampleState(Structure):
    pass

struct_WGPUMultisampleState._pack_ = 1 # source:False
struct_WGPUMultisampleState._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('count', ctypes.c_uint32),
    ('mask', ctypes.c_uint32),
    ('alphaToCoverageEnabled', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUMultisampleState = struct_WGPUMultisampleState
class struct_WGPUOrigin2D(Structure):
    pass

struct_WGPUOrigin2D._pack_ = 1 # source:False
struct_WGPUOrigin2D._fields_ = [
    ('x', ctypes.c_uint32),
    ('y', ctypes.c_uint32),
]

WGPUOrigin2D = struct_WGPUOrigin2D
class struct_WGPUOrigin3D(Structure):
    pass

struct_WGPUOrigin3D._pack_ = 1 # source:False
struct_WGPUOrigin3D._fields_ = [
    ('x', ctypes.c_uint32),
    ('y', ctypes.c_uint32),
    ('z', ctypes.c_uint32),
]

WGPUOrigin3D = struct_WGPUOrigin3D
class struct_WGPUPipelineLayoutDescriptor(Structure):
    pass

struct_WGPUPipelineLayoutDescriptor._pack_ = 1 # source:False
struct_WGPUPipelineLayoutDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', ctypes.POINTER(ctypes.c_char)),
    ('bindGroupLayoutCount', ctypes.c_uint64),
    ('bindGroupLayouts', ctypes.POINTER(ctypes.POINTER(struct_WGPUBindGroupLayoutImpl))),
]

WGPUPipelineLayoutDescriptor = struct_WGPUPipelineLayoutDescriptor
class struct_WGPUPipelineLayoutStorageAttachment(Structure):
    pass

struct_WGPUPipelineLayoutStorageAttachment._pack_ = 1 # source:False
struct_WGPUPipelineLayoutStorageAttachment._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('offset', ctypes.c_uint64),
    ('format', WGPUTextureFormat),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUPipelineLayoutStorageAttachment = struct_WGPUPipelineLayoutStorageAttachment
class struct_WGPUPopErrorScopeCallbackInfo(Structure):
    pass

struct_WGPUPopErrorScopeCallbackInfo._pack_ = 1 # source:False
struct_WGPUPopErrorScopeCallbackInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, WGPUPopErrorScopeStatus, WGPUErrorType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None))),
    ('oldCallback', ctypes.CFUNCTYPE(None, WGPUErrorType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None))),
    ('userdata', ctypes.POINTER(None)),
]

WGPUPopErrorScopeCallbackInfo = struct_WGPUPopErrorScopeCallbackInfo
class struct_WGPUPrimitiveDepthClipControl(Structure):
    pass

struct_WGPUPrimitiveDepthClipControl._pack_ = 1 # source:False
struct_WGPUPrimitiveDepthClipControl._fields_ = [
    ('chain', WGPUChainedStruct),
    ('unclippedDepth', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUPrimitiveDepthClipControl = struct_WGPUPrimitiveDepthClipControl
class struct_WGPUPrimitiveState(Structure):
    pass

struct_WGPUPrimitiveState._pack_ = 1 # source:False
struct_WGPUPrimitiveState._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('topology', WGPUPrimitiveTopology),
    ('stripIndexFormat', WGPUIndexFormat),
    ('frontFace', WGPUFrontFace),
    ('cullMode', WGPUCullMode),
]

WGPUPrimitiveState = struct_WGPUPrimitiveState
class struct_WGPUQuerySetDescriptor(Structure):
    pass

struct_WGPUQuerySetDescriptor._pack_ = 1 # source:False
struct_WGPUQuerySetDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', ctypes.POINTER(ctypes.c_char)),
    ('type', WGPUQueryType),
    ('count', ctypes.c_uint32),
]

WGPUQuerySetDescriptor = struct_WGPUQuerySetDescriptor
class struct_WGPUQueueDescriptor(Structure):
    pass

struct_WGPUQueueDescriptor._pack_ = 1 # source:False
struct_WGPUQueueDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', ctypes.POINTER(ctypes.c_char)),
]

WGPUQueueDescriptor = struct_WGPUQueueDescriptor
class struct_WGPUQueueWorkDoneCallbackInfo(Structure):
    pass

struct_WGPUQueueWorkDoneCallbackInfo._pack_ = 1 # source:False
struct_WGPUQueueWorkDoneCallbackInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, WGPUQueueWorkDoneStatus, ctypes.POINTER(None))),
    ('userdata', ctypes.POINTER(None)),
]

WGPUQueueWorkDoneCallbackInfo = struct_WGPUQueueWorkDoneCallbackInfo
class struct_WGPURenderBundleDescriptor(Structure):
    pass

struct_WGPURenderBundleDescriptor._pack_ = 1 # source:False
struct_WGPURenderBundleDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', ctypes.POINTER(ctypes.c_char)),
]

WGPURenderBundleDescriptor = struct_WGPURenderBundleDescriptor
class struct_WGPURenderBundleEncoderDescriptor(Structure):
    pass

struct_WGPURenderBundleEncoderDescriptor._pack_ = 1 # source:False
struct_WGPURenderBundleEncoderDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', ctypes.POINTER(ctypes.c_char)),
    ('colorFormatCount', ctypes.c_uint64),
    ('colorFormats', ctypes.POINTER(WGPUTextureFormat)),
    ('depthStencilFormat', WGPUTextureFormat),
    ('sampleCount', ctypes.c_uint32),
    ('depthReadOnly', ctypes.c_uint32),
    ('stencilReadOnly', ctypes.c_uint32),
]

WGPURenderBundleEncoderDescriptor = struct_WGPURenderBundleEncoderDescriptor
class struct_WGPURenderPassDepthStencilAttachment(Structure):
    pass

struct_WGPURenderPassDepthStencilAttachment._pack_ = 1 # source:False
struct_WGPURenderPassDepthStencilAttachment._fields_ = [
    ('view', ctypes.POINTER(struct_WGPUTextureViewImpl)),
    ('depthLoadOp', WGPULoadOp),
    ('depthStoreOp', WGPUStoreOp),
    ('depthClearValue', ctypes.c_float),
    ('depthReadOnly', ctypes.c_uint32),
    ('stencilLoadOp', WGPULoadOp),
    ('stencilStoreOp', WGPUStoreOp),
    ('stencilClearValue', ctypes.c_uint32),
    ('stencilReadOnly', ctypes.c_uint32),
]

WGPURenderPassDepthStencilAttachment = struct_WGPURenderPassDepthStencilAttachment
class struct_WGPURenderPassDescriptorMaxDrawCount(Structure):
    pass

struct_WGPURenderPassDescriptorMaxDrawCount._pack_ = 1 # source:False
struct_WGPURenderPassDescriptorMaxDrawCount._fields_ = [
    ('chain', WGPUChainedStruct),
    ('maxDrawCount', ctypes.c_uint64),
]

WGPURenderPassDescriptorMaxDrawCount = struct_WGPURenderPassDescriptorMaxDrawCount
class struct_WGPURenderPassTimestampWrites(Structure):
    pass

struct_WGPURenderPassTimestampWrites._pack_ = 1 # source:False
struct_WGPURenderPassTimestampWrites._fields_ = [
    ('querySet', ctypes.POINTER(struct_WGPUQuerySetImpl)),
    ('beginningOfPassWriteIndex', ctypes.c_uint32),
    ('endOfPassWriteIndex', ctypes.c_uint32),
]

WGPURenderPassTimestampWrites = struct_WGPURenderPassTimestampWrites
class struct_WGPURequestAdapterCallbackInfo(Structure):
    pass

struct_WGPURequestAdapterCallbackInfo._pack_ = 1 # source:False
struct_WGPURequestAdapterCallbackInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, WGPURequestAdapterStatus, ctypes.POINTER(struct_WGPUAdapterImpl), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None))),
    ('userdata', ctypes.POINTER(None)),
]

WGPURequestAdapterCallbackInfo = struct_WGPURequestAdapterCallbackInfo
class struct_WGPURequestAdapterOptions(Structure):
    pass

struct_WGPURequestAdapterOptions._pack_ = 1 # source:False
struct_WGPURequestAdapterOptions._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('compatibleSurface', ctypes.POINTER(struct_WGPUSurfaceImpl)),
    ('powerPreference', WGPUPowerPreference),
    ('backendType', WGPUBackendType),
    ('forceFallbackAdapter', ctypes.c_uint32),
    ('compatibilityMode', ctypes.c_uint32),
]

WGPURequestAdapterOptions = struct_WGPURequestAdapterOptions
class struct_WGPURequestDeviceCallbackInfo(Structure):
    pass

struct_WGPURequestDeviceCallbackInfo._pack_ = 1 # source:False
struct_WGPURequestDeviceCallbackInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, WGPURequestDeviceStatus, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None))),
    ('userdata', ctypes.POINTER(None)),
]

WGPURequestDeviceCallbackInfo = struct_WGPURequestDeviceCallbackInfo
class struct_WGPUSamplerBindingLayout(Structure):
    pass

struct_WGPUSamplerBindingLayout._pack_ = 1 # source:False
struct_WGPUSamplerBindingLayout._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('type', WGPUSamplerBindingType),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSamplerBindingLayout = struct_WGPUSamplerBindingLayout
class struct_WGPUSamplerDescriptor(Structure):
    pass

struct_WGPUSamplerDescriptor._pack_ = 1 # source:False
struct_WGPUSamplerDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', ctypes.POINTER(ctypes.c_char)),
    ('addressModeU', WGPUAddressMode),
    ('addressModeV', WGPUAddressMode),
    ('addressModeW', WGPUAddressMode),
    ('magFilter', WGPUFilterMode),
    ('minFilter', WGPUFilterMode),
    ('mipmapFilter', WGPUMipmapFilterMode),
    ('lodMinClamp', ctypes.c_float),
    ('lodMaxClamp', ctypes.c_float),
    ('compare', WGPUCompareFunction),
    ('maxAnisotropy', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 2),
]

WGPUSamplerDescriptor = struct_WGPUSamplerDescriptor
class struct_WGPUShaderModuleSPIRVDescriptor(Structure):
    pass

struct_WGPUShaderModuleSPIRVDescriptor._pack_ = 1 # source:False
struct_WGPUShaderModuleSPIRVDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('codeSize', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('code', ctypes.POINTER(ctypes.c_uint32)),
]

WGPUShaderModuleSPIRVDescriptor = struct_WGPUShaderModuleSPIRVDescriptor
class struct_WGPUShaderModuleWGSLDescriptor(Structure):
    pass

struct_WGPUShaderModuleWGSLDescriptor._pack_ = 1 # source:False
struct_WGPUShaderModuleWGSLDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('code', ctypes.POINTER(ctypes.c_char)),
]

WGPUShaderModuleWGSLDescriptor = struct_WGPUShaderModuleWGSLDescriptor
class struct_WGPUShaderModuleCompilationOptions(Structure):
    pass

struct_WGPUShaderModuleCompilationOptions._pack_ = 1 # source:False
struct_WGPUShaderModuleCompilationOptions._fields_ = [
    ('chain', WGPUChainedStruct),
    ('strictMath', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUShaderModuleCompilationOptions = struct_WGPUShaderModuleCompilationOptions
class struct_WGPUShaderModuleDescriptor(Structure):
    pass

struct_WGPUShaderModuleDescriptor._pack_ = 1 # source:False
struct_WGPUShaderModuleDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', ctypes.POINTER(ctypes.c_char)),
]

WGPUShaderModuleDescriptor = struct_WGPUShaderModuleDescriptor
class struct_WGPUSharedBufferMemoryBeginAccessDescriptor(Structure):
    pass

struct_WGPUSharedBufferMemoryBeginAccessDescriptor._pack_ = 1 # source:False
struct_WGPUSharedBufferMemoryBeginAccessDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('initialized', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('fenceCount', ctypes.c_uint64),
    ('fences', ctypes.POINTER(ctypes.POINTER(struct_WGPUSharedFenceImpl))),
    ('signaledValues', ctypes.POINTER(ctypes.c_uint64)),
]

WGPUSharedBufferMemoryBeginAccessDescriptor = struct_WGPUSharedBufferMemoryBeginAccessDescriptor
class struct_WGPUSharedBufferMemoryDescriptor(Structure):
    pass

struct_WGPUSharedBufferMemoryDescriptor._pack_ = 1 # source:False
struct_WGPUSharedBufferMemoryDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', ctypes.POINTER(ctypes.c_char)),
]

WGPUSharedBufferMemoryDescriptor = struct_WGPUSharedBufferMemoryDescriptor
class struct_WGPUSharedBufferMemoryEndAccessState(Structure):
    pass

struct_WGPUSharedBufferMemoryEndAccessState._pack_ = 1 # source:False
struct_WGPUSharedBufferMemoryEndAccessState._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStructOut)),
    ('initialized', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('fenceCount', ctypes.c_uint64),
    ('fences', ctypes.POINTER(ctypes.POINTER(struct_WGPUSharedFenceImpl))),
    ('signaledValues', ctypes.POINTER(ctypes.c_uint64)),
]

WGPUSharedBufferMemoryEndAccessState = struct_WGPUSharedBufferMemoryEndAccessState
class struct_WGPUSharedBufferMemoryProperties(Structure):
    pass

struct_WGPUSharedBufferMemoryProperties._pack_ = 1 # source:False
struct_WGPUSharedBufferMemoryProperties._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStructOut)),
    ('usage', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('size', ctypes.c_uint64),
]

WGPUSharedBufferMemoryProperties = struct_WGPUSharedBufferMemoryProperties
class struct_WGPUSharedFenceDXGISharedHandleDescriptor(Structure):
    pass

struct_WGPUSharedFenceDXGISharedHandleDescriptor._pack_ = 1 # source:False
struct_WGPUSharedFenceDXGISharedHandleDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('handle', ctypes.POINTER(None)),
]

WGPUSharedFenceDXGISharedHandleDescriptor = struct_WGPUSharedFenceDXGISharedHandleDescriptor
class struct_WGPUSharedFenceDXGISharedHandleExportInfo(Structure):
    pass

struct_WGPUSharedFenceDXGISharedHandleExportInfo._pack_ = 1 # source:False
struct_WGPUSharedFenceDXGISharedHandleExportInfo._fields_ = [
    ('chain', WGPUChainedStructOut),
    ('handle', ctypes.POINTER(None)),
]

WGPUSharedFenceDXGISharedHandleExportInfo = struct_WGPUSharedFenceDXGISharedHandleExportInfo
class struct_WGPUSharedFenceMTLSharedEventDescriptor(Structure):
    pass

struct_WGPUSharedFenceMTLSharedEventDescriptor._pack_ = 1 # source:False
struct_WGPUSharedFenceMTLSharedEventDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('sharedEvent', ctypes.POINTER(None)),
]

WGPUSharedFenceMTLSharedEventDescriptor = struct_WGPUSharedFenceMTLSharedEventDescriptor
class struct_WGPUSharedFenceMTLSharedEventExportInfo(Structure):
    pass

struct_WGPUSharedFenceMTLSharedEventExportInfo._pack_ = 1 # source:False
struct_WGPUSharedFenceMTLSharedEventExportInfo._fields_ = [
    ('chain', WGPUChainedStructOut),
    ('sharedEvent', ctypes.POINTER(None)),
]

WGPUSharedFenceMTLSharedEventExportInfo = struct_WGPUSharedFenceMTLSharedEventExportInfo
class struct_WGPUSharedFenceDescriptor(Structure):
    pass

struct_WGPUSharedFenceDescriptor._pack_ = 1 # source:False
struct_WGPUSharedFenceDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', ctypes.POINTER(ctypes.c_char)),
]

WGPUSharedFenceDescriptor = struct_WGPUSharedFenceDescriptor
class struct_WGPUSharedFenceExportInfo(Structure):
    pass

struct_WGPUSharedFenceExportInfo._pack_ = 1 # source:False
struct_WGPUSharedFenceExportInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStructOut)),
    ('type', WGPUSharedFenceType),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSharedFenceExportInfo = struct_WGPUSharedFenceExportInfo
class struct_WGPUSharedFenceVkSemaphoreOpaqueFDDescriptor(Structure):
    pass

struct_WGPUSharedFenceVkSemaphoreOpaqueFDDescriptor._pack_ = 1 # source:False
struct_WGPUSharedFenceVkSemaphoreOpaqueFDDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('handle', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSharedFenceVkSemaphoreOpaqueFDDescriptor = struct_WGPUSharedFenceVkSemaphoreOpaqueFDDescriptor
class struct_WGPUSharedFenceVkSemaphoreOpaqueFDExportInfo(Structure):
    pass

struct_WGPUSharedFenceVkSemaphoreOpaqueFDExportInfo._pack_ = 1 # source:False
struct_WGPUSharedFenceVkSemaphoreOpaqueFDExportInfo._fields_ = [
    ('chain', WGPUChainedStructOut),
    ('handle', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSharedFenceVkSemaphoreOpaqueFDExportInfo = struct_WGPUSharedFenceVkSemaphoreOpaqueFDExportInfo
class struct_WGPUSharedFenceVkSemaphoreSyncFDDescriptor(Structure):
    pass

struct_WGPUSharedFenceVkSemaphoreSyncFDDescriptor._pack_ = 1 # source:False
struct_WGPUSharedFenceVkSemaphoreSyncFDDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('handle', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSharedFenceVkSemaphoreSyncFDDescriptor = struct_WGPUSharedFenceVkSemaphoreSyncFDDescriptor
class struct_WGPUSharedFenceVkSemaphoreSyncFDExportInfo(Structure):
    pass

struct_WGPUSharedFenceVkSemaphoreSyncFDExportInfo._pack_ = 1 # source:False
struct_WGPUSharedFenceVkSemaphoreSyncFDExportInfo._fields_ = [
    ('chain', WGPUChainedStructOut),
    ('handle', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSharedFenceVkSemaphoreSyncFDExportInfo = struct_WGPUSharedFenceVkSemaphoreSyncFDExportInfo
class struct_WGPUSharedFenceVkSemaphoreZirconHandleDescriptor(Structure):
    pass

struct_WGPUSharedFenceVkSemaphoreZirconHandleDescriptor._pack_ = 1 # source:False
struct_WGPUSharedFenceVkSemaphoreZirconHandleDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('handle', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSharedFenceVkSemaphoreZirconHandleDescriptor = struct_WGPUSharedFenceVkSemaphoreZirconHandleDescriptor
class struct_WGPUSharedFenceVkSemaphoreZirconHandleExportInfo(Structure):
    pass

struct_WGPUSharedFenceVkSemaphoreZirconHandleExportInfo._pack_ = 1 # source:False
struct_WGPUSharedFenceVkSemaphoreZirconHandleExportInfo._fields_ = [
    ('chain', WGPUChainedStructOut),
    ('handle', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSharedFenceVkSemaphoreZirconHandleExportInfo = struct_WGPUSharedFenceVkSemaphoreZirconHandleExportInfo
class struct_WGPUSharedTextureMemoryD3DSwapchainBeginState(Structure):
    pass

struct_WGPUSharedTextureMemoryD3DSwapchainBeginState._pack_ = 1 # source:False
struct_WGPUSharedTextureMemoryD3DSwapchainBeginState._fields_ = [
    ('chain', WGPUChainedStruct),
    ('isSwapchain', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSharedTextureMemoryD3DSwapchainBeginState = struct_WGPUSharedTextureMemoryD3DSwapchainBeginState
class struct_WGPUSharedTextureMemoryDXGISharedHandleDescriptor(Structure):
    pass

struct_WGPUSharedTextureMemoryDXGISharedHandleDescriptor._pack_ = 1 # source:False
struct_WGPUSharedTextureMemoryDXGISharedHandleDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('handle', ctypes.POINTER(None)),
    ('useKeyedMutex', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSharedTextureMemoryDXGISharedHandleDescriptor = struct_WGPUSharedTextureMemoryDXGISharedHandleDescriptor
class struct_WGPUSharedTextureMemoryEGLImageDescriptor(Structure):
    pass

struct_WGPUSharedTextureMemoryEGLImageDescriptor._pack_ = 1 # source:False
struct_WGPUSharedTextureMemoryEGLImageDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('image', ctypes.POINTER(None)),
]

WGPUSharedTextureMemoryEGLImageDescriptor = struct_WGPUSharedTextureMemoryEGLImageDescriptor
class struct_WGPUSharedTextureMemoryIOSurfaceDescriptor(Structure):
    pass

struct_WGPUSharedTextureMemoryIOSurfaceDescriptor._pack_ = 1 # source:False
struct_WGPUSharedTextureMemoryIOSurfaceDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('ioSurface', ctypes.POINTER(None)),
]

WGPUSharedTextureMemoryIOSurfaceDescriptor = struct_WGPUSharedTextureMemoryIOSurfaceDescriptor
class struct_WGPUSharedTextureMemoryAHardwareBufferDescriptor(Structure):
    pass

struct_WGPUSharedTextureMemoryAHardwareBufferDescriptor._pack_ = 1 # source:False
struct_WGPUSharedTextureMemoryAHardwareBufferDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('handle', ctypes.POINTER(None)),
    ('useExternalFormat', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSharedTextureMemoryAHardwareBufferDescriptor = struct_WGPUSharedTextureMemoryAHardwareBufferDescriptor
class struct_WGPUSharedTextureMemoryBeginAccessDescriptor(Structure):
    pass

struct_WGPUSharedTextureMemoryBeginAccessDescriptor._pack_ = 1 # source:False
struct_WGPUSharedTextureMemoryBeginAccessDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('concurrentRead', ctypes.c_uint32),
    ('initialized', ctypes.c_uint32),
    ('fenceCount', ctypes.c_uint64),
    ('fences', ctypes.POINTER(ctypes.POINTER(struct_WGPUSharedFenceImpl))),
    ('signaledValues', ctypes.POINTER(ctypes.c_uint64)),
]

WGPUSharedTextureMemoryBeginAccessDescriptor = struct_WGPUSharedTextureMemoryBeginAccessDescriptor
class struct_WGPUSharedTextureMemoryDescriptor(Structure):
    pass

struct_WGPUSharedTextureMemoryDescriptor._pack_ = 1 # source:False
struct_WGPUSharedTextureMemoryDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', ctypes.POINTER(ctypes.c_char)),
]

WGPUSharedTextureMemoryDescriptor = struct_WGPUSharedTextureMemoryDescriptor
class struct_WGPUSharedTextureMemoryDmaBufPlane(Structure):
    pass

struct_WGPUSharedTextureMemoryDmaBufPlane._pack_ = 1 # source:False
struct_WGPUSharedTextureMemoryDmaBufPlane._fields_ = [
    ('fd', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('offset', ctypes.c_uint64),
    ('stride', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
]

WGPUSharedTextureMemoryDmaBufPlane = struct_WGPUSharedTextureMemoryDmaBufPlane
class struct_WGPUSharedTextureMemoryEndAccessState(Structure):
    pass

struct_WGPUSharedTextureMemoryEndAccessState._pack_ = 1 # source:False
struct_WGPUSharedTextureMemoryEndAccessState._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStructOut)),
    ('initialized', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('fenceCount', ctypes.c_uint64),
    ('fences', ctypes.POINTER(ctypes.POINTER(struct_WGPUSharedFenceImpl))),
    ('signaledValues', ctypes.POINTER(ctypes.c_uint64)),
]

WGPUSharedTextureMemoryEndAccessState = struct_WGPUSharedTextureMemoryEndAccessState
class struct_WGPUSharedTextureMemoryOpaqueFDDescriptor(Structure):
    pass

struct_WGPUSharedTextureMemoryOpaqueFDDescriptor._pack_ = 1 # source:False
struct_WGPUSharedTextureMemoryOpaqueFDDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('vkImageCreateInfo', ctypes.POINTER(None)),
    ('memoryFD', ctypes.c_int32),
    ('memoryTypeIndex', ctypes.c_uint32),
    ('allocationSize', ctypes.c_uint64),
    ('dedicatedAllocation', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSharedTextureMemoryOpaqueFDDescriptor = struct_WGPUSharedTextureMemoryOpaqueFDDescriptor
class struct_WGPUSharedTextureMemoryVkDedicatedAllocationDescriptor(Structure):
    pass

struct_WGPUSharedTextureMemoryVkDedicatedAllocationDescriptor._pack_ = 1 # source:False
struct_WGPUSharedTextureMemoryVkDedicatedAllocationDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('dedicatedAllocation', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSharedTextureMemoryVkDedicatedAllocationDescriptor = struct_WGPUSharedTextureMemoryVkDedicatedAllocationDescriptor
class struct_WGPUSharedTextureMemoryVkImageLayoutBeginState(Structure):
    pass

struct_WGPUSharedTextureMemoryVkImageLayoutBeginState._pack_ = 1 # source:False
struct_WGPUSharedTextureMemoryVkImageLayoutBeginState._fields_ = [
    ('chain', WGPUChainedStruct),
    ('oldLayout', ctypes.c_int32),
    ('newLayout', ctypes.c_int32),
]

WGPUSharedTextureMemoryVkImageLayoutBeginState = struct_WGPUSharedTextureMemoryVkImageLayoutBeginState
class struct_WGPUSharedTextureMemoryVkImageLayoutEndState(Structure):
    pass

struct_WGPUSharedTextureMemoryVkImageLayoutEndState._pack_ = 1 # source:False
struct_WGPUSharedTextureMemoryVkImageLayoutEndState._fields_ = [
    ('chain', WGPUChainedStructOut),
    ('oldLayout', ctypes.c_int32),
    ('newLayout', ctypes.c_int32),
]

WGPUSharedTextureMemoryVkImageLayoutEndState = struct_WGPUSharedTextureMemoryVkImageLayoutEndState
class struct_WGPUSharedTextureMemoryZirconHandleDescriptor(Structure):
    pass

struct_WGPUSharedTextureMemoryZirconHandleDescriptor._pack_ = 1 # source:False
struct_WGPUSharedTextureMemoryZirconHandleDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('memoryFD', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('allocationSize', ctypes.c_uint64),
]

WGPUSharedTextureMemoryZirconHandleDescriptor = struct_WGPUSharedTextureMemoryZirconHandleDescriptor
class struct_WGPUStaticSamplerBindingLayout(Structure):
    pass

struct_WGPUStaticSamplerBindingLayout._pack_ = 1 # source:False
struct_WGPUStaticSamplerBindingLayout._fields_ = [
    ('chain', WGPUChainedStruct),
    ('sampler', ctypes.POINTER(struct_WGPUSamplerImpl)),
]

WGPUStaticSamplerBindingLayout = struct_WGPUStaticSamplerBindingLayout
class struct_WGPUStencilFaceState(Structure):
    _pack_ = 1 # source:False
    _fields_ = [
    ('compare', WGPUCompareFunction),
    ('failOp', WGPUStencilOperation),
    ('depthFailOp', WGPUStencilOperation),
    ('passOp', WGPUStencilOperation),
     ]

WGPUStencilFaceState = struct_WGPUStencilFaceState
class struct_WGPUStorageTextureBindingLayout(Structure):
    pass

struct_WGPUStorageTextureBindingLayout._pack_ = 1 # source:False
struct_WGPUStorageTextureBindingLayout._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('access', WGPUStorageTextureAccess),
    ('format', WGPUTextureFormat),
    ('viewDimension', WGPUTextureViewDimension),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUStorageTextureBindingLayout = struct_WGPUStorageTextureBindingLayout
class struct_WGPUSurfaceCapabilities(Structure):
    pass

struct_WGPUSurfaceCapabilities._pack_ = 1 # source:False
struct_WGPUSurfaceCapabilities._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStructOut)),
    ('usages', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('formatCount', ctypes.c_uint64),
    ('formats', ctypes.POINTER(WGPUTextureFormat)),
    ('presentModeCount', ctypes.c_uint64),
    ('presentModes', ctypes.POINTER(WGPUPresentMode)),
    ('alphaModeCount', ctypes.c_uint64),
    ('alphaModes', ctypes.POINTER(WGPUCompositeAlphaMode)),
]

WGPUSurfaceCapabilities = struct_WGPUSurfaceCapabilities
class struct_WGPUSurfaceConfiguration(Structure):
    pass

struct_WGPUSurfaceConfiguration._pack_ = 1 # source:False
struct_WGPUSurfaceConfiguration._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('device', ctypes.POINTER(struct_WGPUDeviceImpl)),
    ('format', WGPUTextureFormat),
    ('usage', ctypes.c_uint32),
    ('viewFormatCount', ctypes.c_uint64),
    ('viewFormats', ctypes.POINTER(WGPUTextureFormat)),
    ('alphaMode', WGPUCompositeAlphaMode),
    ('width', ctypes.c_uint32),
    ('height', ctypes.c_uint32),
    ('presentMode', WGPUPresentMode),
]

WGPUSurfaceConfiguration = struct_WGPUSurfaceConfiguration
class struct_WGPUSurfaceDescriptor(Structure):
    pass

struct_WGPUSurfaceDescriptor._pack_ = 1 # source:False
struct_WGPUSurfaceDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', ctypes.POINTER(ctypes.c_char)),
]

WGPUSurfaceDescriptor = struct_WGPUSurfaceDescriptor
class struct_WGPUSurfaceDescriptorFromAndroidNativeWindow(Structure):
    pass

struct_WGPUSurfaceDescriptorFromAndroidNativeWindow._pack_ = 1 # source:False
struct_WGPUSurfaceDescriptorFromAndroidNativeWindow._fields_ = [
    ('chain', WGPUChainedStruct),
    ('window', ctypes.POINTER(None)),
]

WGPUSurfaceDescriptorFromAndroidNativeWindow = struct_WGPUSurfaceDescriptorFromAndroidNativeWindow
class struct_WGPUSurfaceDescriptorFromCanvasHTMLSelector(Structure):
    pass

struct_WGPUSurfaceDescriptorFromCanvasHTMLSelector._pack_ = 1 # source:False
struct_WGPUSurfaceDescriptorFromCanvasHTMLSelector._fields_ = [
    ('chain', WGPUChainedStruct),
    ('selector', ctypes.POINTER(ctypes.c_char)),
]

WGPUSurfaceDescriptorFromCanvasHTMLSelector = struct_WGPUSurfaceDescriptorFromCanvasHTMLSelector
class struct_WGPUSurfaceDescriptorFromMetalLayer(Structure):
    pass

struct_WGPUSurfaceDescriptorFromMetalLayer._pack_ = 1 # source:False
struct_WGPUSurfaceDescriptorFromMetalLayer._fields_ = [
    ('chain', WGPUChainedStruct),
    ('layer', ctypes.POINTER(None)),
]

WGPUSurfaceDescriptorFromMetalLayer = struct_WGPUSurfaceDescriptorFromMetalLayer
class struct_WGPUSurfaceDescriptorFromWaylandSurface(Structure):
    pass

struct_WGPUSurfaceDescriptorFromWaylandSurface._pack_ = 1 # source:False
struct_WGPUSurfaceDescriptorFromWaylandSurface._fields_ = [
    ('chain', WGPUChainedStruct),
    ('display', ctypes.POINTER(None)),
    ('surface', ctypes.POINTER(None)),
]

WGPUSurfaceDescriptorFromWaylandSurface = struct_WGPUSurfaceDescriptorFromWaylandSurface
class struct_WGPUSurfaceDescriptorFromWindowsHWND(Structure):
    pass

struct_WGPUSurfaceDescriptorFromWindowsHWND._pack_ = 1 # source:False
struct_WGPUSurfaceDescriptorFromWindowsHWND._fields_ = [
    ('chain', WGPUChainedStruct),
    ('hinstance', ctypes.POINTER(None)),
    ('hwnd', ctypes.POINTER(None)),
]

WGPUSurfaceDescriptorFromWindowsHWND = struct_WGPUSurfaceDescriptorFromWindowsHWND
class struct_WGPUSurfaceDescriptorFromWindowsCoreWindow(Structure):
    pass

struct_WGPUSurfaceDescriptorFromWindowsCoreWindow._pack_ = 1 # source:False
struct_WGPUSurfaceDescriptorFromWindowsCoreWindow._fields_ = [
    ('chain', WGPUChainedStruct),
    ('coreWindow', ctypes.POINTER(None)),
]

WGPUSurfaceDescriptorFromWindowsCoreWindow = struct_WGPUSurfaceDescriptorFromWindowsCoreWindow
class struct_WGPUSurfaceDescriptorFromWindowsSwapChainPanel(Structure):
    pass

struct_WGPUSurfaceDescriptorFromWindowsSwapChainPanel._pack_ = 1 # source:False
struct_WGPUSurfaceDescriptorFromWindowsSwapChainPanel._fields_ = [
    ('chain', WGPUChainedStruct),
    ('swapChainPanel', ctypes.POINTER(None)),
]

WGPUSurfaceDescriptorFromWindowsSwapChainPanel = struct_WGPUSurfaceDescriptorFromWindowsSwapChainPanel
class struct_WGPUSurfaceDescriptorFromXlibWindow(Structure):
    pass

struct_WGPUSurfaceDescriptorFromXlibWindow._pack_ = 1 # source:False
struct_WGPUSurfaceDescriptorFromXlibWindow._fields_ = [
    ('chain', WGPUChainedStruct),
    ('display', ctypes.POINTER(None)),
    ('window', ctypes.c_uint64),
]

WGPUSurfaceDescriptorFromXlibWindow = struct_WGPUSurfaceDescriptorFromXlibWindow
class struct_WGPUSurfaceTexture(Structure):
    pass

struct_WGPUSurfaceTexture._pack_ = 1 # source:False
struct_WGPUSurfaceTexture._fields_ = [
    ('texture', ctypes.POINTER(struct_WGPUTextureImpl)),
    ('suboptimal', ctypes.c_uint32),
    ('status', WGPUSurfaceGetCurrentTextureStatus),
]

WGPUSurfaceTexture = struct_WGPUSurfaceTexture
class struct_WGPUSwapChainDescriptor(Structure):
    pass

struct_WGPUSwapChainDescriptor._pack_ = 1 # source:False
struct_WGPUSwapChainDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', ctypes.POINTER(ctypes.c_char)),
    ('usage', ctypes.c_uint32),
    ('format', WGPUTextureFormat),
    ('width', ctypes.c_uint32),
    ('height', ctypes.c_uint32),
    ('presentMode', WGPUPresentMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSwapChainDescriptor = struct_WGPUSwapChainDescriptor
class struct_WGPUTextureBindingLayout(Structure):
    pass

struct_WGPUTextureBindingLayout._pack_ = 1 # source:False
struct_WGPUTextureBindingLayout._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('sampleType', WGPUTextureSampleType),
    ('viewDimension', WGPUTextureViewDimension),
    ('multisampled', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUTextureBindingLayout = struct_WGPUTextureBindingLayout
class struct_WGPUTextureBindingViewDimensionDescriptor(Structure):
    pass

struct_WGPUTextureBindingViewDimensionDescriptor._pack_ = 1 # source:False
struct_WGPUTextureBindingViewDimensionDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('textureBindingViewDimension', WGPUTextureViewDimension),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUTextureBindingViewDimensionDescriptor = struct_WGPUTextureBindingViewDimensionDescriptor
class struct_WGPUTextureDataLayout(Structure):
    pass

struct_WGPUTextureDataLayout._pack_ = 1 # source:False
struct_WGPUTextureDataLayout._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('offset', ctypes.c_uint64),
    ('bytesPerRow', ctypes.c_uint32),
    ('rowsPerImage', ctypes.c_uint32),
]

WGPUTextureDataLayout = struct_WGPUTextureDataLayout
class struct_WGPUTextureViewDescriptor(Structure):
    pass

struct_WGPUTextureViewDescriptor._pack_ = 1 # source:False
struct_WGPUTextureViewDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', ctypes.POINTER(ctypes.c_char)),
    ('format', WGPUTextureFormat),
    ('dimension', WGPUTextureViewDimension),
    ('baseMipLevel', ctypes.c_uint32),
    ('mipLevelCount', ctypes.c_uint32),
    ('baseArrayLayer', ctypes.c_uint32),
    ('arrayLayerCount', ctypes.c_uint32),
    ('aspect', WGPUTextureAspect),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUTextureViewDescriptor = struct_WGPUTextureViewDescriptor
class struct_WGPUUncapturedErrorCallbackInfo(Structure):
    pass

struct_WGPUUncapturedErrorCallbackInfo._pack_ = 1 # source:False
struct_WGPUUncapturedErrorCallbackInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('callback', ctypes.CFUNCTYPE(None, WGPUErrorType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None))),
    ('userdata', ctypes.POINTER(None)),
]

WGPUUncapturedErrorCallbackInfo = struct_WGPUUncapturedErrorCallbackInfo
class struct_WGPUVertexAttribute(Structure):
    pass

struct_WGPUVertexAttribute._pack_ = 1 # source:False
struct_WGPUVertexAttribute._fields_ = [
    ('format', WGPUVertexFormat),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('offset', ctypes.c_uint64),
    ('shaderLocation', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
]

WGPUVertexAttribute = struct_WGPUVertexAttribute
class struct_WGPUYCbCrVkDescriptor(Structure):
    pass

struct_WGPUYCbCrVkDescriptor._pack_ = 1 # source:False
struct_WGPUYCbCrVkDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('vkFormat', ctypes.c_uint32),
    ('vkYCbCrModel', ctypes.c_uint32),
    ('vkYCbCrRange', ctypes.c_uint32),
    ('vkComponentSwizzleRed', ctypes.c_uint32),
    ('vkComponentSwizzleGreen', ctypes.c_uint32),
    ('vkComponentSwizzleBlue', ctypes.c_uint32),
    ('vkComponentSwizzleAlpha', ctypes.c_uint32),
    ('vkXChromaOffset', ctypes.c_uint32),
    ('vkYChromaOffset', ctypes.c_uint32),
    ('vkChromaFilter', WGPUFilterMode),
    ('forceExplicitReconstruction', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('externalFormat', ctypes.c_uint64),
]

WGPUYCbCrVkDescriptor = struct_WGPUYCbCrVkDescriptor
class struct_WGPUAHardwareBufferProperties(Structure):
    _pack_ = 1 # source:False
    _fields_ = [
    ('yCbCrInfo', WGPUYCbCrVkDescriptor),
     ]

WGPUAHardwareBufferProperties = struct_WGPUAHardwareBufferProperties
class struct_WGPUAdapterPropertiesMemoryHeaps(Structure):
    pass

struct_WGPUAdapterPropertiesMemoryHeaps._pack_ = 1 # source:False
struct_WGPUAdapterPropertiesMemoryHeaps._fields_ = [
    ('chain', WGPUChainedStructOut),
    ('heapCount', ctypes.c_uint64),
    ('heapInfo', ctypes.POINTER(struct_WGPUMemoryHeapInfo)),
]

WGPUAdapterPropertiesMemoryHeaps = struct_WGPUAdapterPropertiesMemoryHeaps
class struct_WGPUBindGroupDescriptor(Structure):
    pass

struct_WGPUBindGroupDescriptor._pack_ = 1 # source:False
struct_WGPUBindGroupDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', ctypes.POINTER(ctypes.c_char)),
    ('layout', ctypes.POINTER(struct_WGPUBindGroupLayoutImpl)),
    ('entryCount', ctypes.c_uint64),
    ('entries', ctypes.POINTER(struct_WGPUBindGroupEntry)),
]

WGPUBindGroupDescriptor = struct_WGPUBindGroupDescriptor
class struct_WGPUBindGroupLayoutEntry(Structure):
    pass

struct_WGPUBindGroupLayoutEntry._pack_ = 1 # source:False
struct_WGPUBindGroupLayoutEntry._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('binding', ctypes.c_uint32),
    ('visibility', ctypes.c_uint32),
    ('buffer', WGPUBufferBindingLayout),
    ('sampler', WGPUSamplerBindingLayout),
    ('texture', WGPUTextureBindingLayout),
    ('storageTexture', WGPUStorageTextureBindingLayout),
]

WGPUBindGroupLayoutEntry = struct_WGPUBindGroupLayoutEntry
class struct_WGPUBlendState(Structure):
    _pack_ = 1 # source:False
    _fields_ = [
    ('color', WGPUBlendComponent),
    ('alpha', WGPUBlendComponent),
     ]

WGPUBlendState = struct_WGPUBlendState
struct_WGPUCompilationInfo._pack_ = 1 # source:False
struct_WGPUCompilationInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('messageCount', ctypes.c_uint64),
    ('messages', ctypes.POINTER(struct_WGPUCompilationMessage)),
]

WGPUCompilationInfo = struct_WGPUCompilationInfo
class struct_WGPUComputePassDescriptor(Structure):
    pass

struct_WGPUComputePassDescriptor._pack_ = 1 # source:False
struct_WGPUComputePassDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', ctypes.POINTER(ctypes.c_char)),
    ('timestampWrites', ctypes.POINTER(struct_WGPUComputePassTimestampWrites)),
]

WGPUComputePassDescriptor = struct_WGPUComputePassDescriptor
class struct_WGPUDepthStencilState(Structure):
    pass

struct_WGPUDepthStencilState._pack_ = 1 # source:False
struct_WGPUDepthStencilState._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('format', WGPUTextureFormat),
    ('depthWriteEnabled', ctypes.c_uint32),
    ('depthCompare', WGPUCompareFunction),
    ('stencilFront', WGPUStencilFaceState),
    ('stencilBack', WGPUStencilFaceState),
    ('stencilReadMask', ctypes.c_uint32),
    ('stencilWriteMask', ctypes.c_uint32),
    ('depthBias', ctypes.c_int32),
    ('depthBiasSlopeScale', ctypes.c_float),
    ('depthBiasClamp', ctypes.c_float),
]

WGPUDepthStencilState = struct_WGPUDepthStencilState
class struct_WGPUDrmFormatCapabilities(Structure):
    pass

struct_WGPUDrmFormatCapabilities._pack_ = 1 # source:False
struct_WGPUDrmFormatCapabilities._fields_ = [
    ('chain', WGPUChainedStructOut),
    ('propertiesCount', ctypes.c_uint64),
    ('properties', ctypes.POINTER(struct_WGPUDrmFormatProperties)),
]

WGPUDrmFormatCapabilities = struct_WGPUDrmFormatCapabilities
class struct_WGPUExternalTextureDescriptor(Structure):
    pass

struct_WGPUExternalTextureDescriptor._pack_ = 1 # source:False
struct_WGPUExternalTextureDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', ctypes.POINTER(ctypes.c_char)),
    ('plane0', ctypes.POINTER(struct_WGPUTextureViewImpl)),
    ('plane1', ctypes.POINTER(struct_WGPUTextureViewImpl)),
    ('visibleOrigin', WGPUOrigin2D),
    ('visibleSize', WGPUExtent2D),
    ('doYuvToRgbConversionOnly', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('yuvToRgbConversionMatrix', ctypes.POINTER(ctypes.c_float)),
    ('srcTransferFunctionParameters', ctypes.POINTER(ctypes.c_float)),
    ('dstTransferFunctionParameters', ctypes.POINTER(ctypes.c_float)),
    ('gamutConversionMatrix', ctypes.POINTER(ctypes.c_float)),
    ('mirrored', ctypes.c_uint32),
    ('rotation', WGPUExternalTextureRotation),
]

WGPUExternalTextureDescriptor = struct_WGPUExternalTextureDescriptor
class struct_WGPUFutureWaitInfo(Structure):
    pass

struct_WGPUFutureWaitInfo._pack_ = 1 # source:False
struct_WGPUFutureWaitInfo._fields_ = [
    ('future', WGPUFuture),
    ('completed', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUFutureWaitInfo = struct_WGPUFutureWaitInfo
class struct_WGPUImageCopyBuffer(Structure):
    pass

struct_WGPUImageCopyBuffer._pack_ = 1 # source:False
struct_WGPUImageCopyBuffer._fields_ = [
    ('layout', WGPUTextureDataLayout),
    ('buffer', ctypes.POINTER(struct_WGPUBufferImpl)),
]

WGPUImageCopyBuffer = struct_WGPUImageCopyBuffer
class struct_WGPUImageCopyExternalTexture(Structure):
    pass

struct_WGPUImageCopyExternalTexture._pack_ = 1 # source:False
struct_WGPUImageCopyExternalTexture._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('externalTexture', ctypes.POINTER(struct_WGPUExternalTextureImpl)),
    ('origin', WGPUOrigin3D),
    ('naturalSize', WGPUExtent2D),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUImageCopyExternalTexture = struct_WGPUImageCopyExternalTexture
class struct_WGPUImageCopyTexture(Structure):
    pass

struct_WGPUImageCopyTexture._pack_ = 1 # source:False
struct_WGPUImageCopyTexture._fields_ = [
    ('texture', ctypes.POINTER(struct_WGPUTextureImpl)),
    ('mipLevel', ctypes.c_uint32),
    ('origin', WGPUOrigin3D),
    ('aspect', WGPUTextureAspect),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUImageCopyTexture = struct_WGPUImageCopyTexture
class struct_WGPUInstanceDescriptor(Structure):
    pass

struct_WGPUInstanceDescriptor._pack_ = 1 # source:False
struct_WGPUInstanceDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('features', WGPUInstanceFeatures),
]

WGPUInstanceDescriptor = struct_WGPUInstanceDescriptor
class struct_WGPUPipelineLayoutPixelLocalStorage(Structure):
    pass

struct_WGPUPipelineLayoutPixelLocalStorage._pack_ = 1 # source:False
struct_WGPUPipelineLayoutPixelLocalStorage._fields_ = [
    ('chain', WGPUChainedStruct),
    ('totalPixelLocalStorageSize', ctypes.c_uint64),
    ('storageAttachmentCount', ctypes.c_uint64),
    ('storageAttachments', ctypes.POINTER(struct_WGPUPipelineLayoutStorageAttachment)),
]

WGPUPipelineLayoutPixelLocalStorage = struct_WGPUPipelineLayoutPixelLocalStorage
class struct_WGPUProgrammableStageDescriptor(Structure):
    pass

struct_WGPUProgrammableStageDescriptor._pack_ = 1 # source:False
struct_WGPUProgrammableStageDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('module', ctypes.POINTER(struct_WGPUShaderModuleImpl)),
    ('entryPoint', ctypes.POINTER(ctypes.c_char)),
    ('constantCount', ctypes.c_uint64),
    ('constants', ctypes.POINTER(struct_WGPUConstantEntry)),
]

WGPUProgrammableStageDescriptor = struct_WGPUProgrammableStageDescriptor
class struct_WGPURenderPassColorAttachment(Structure):
    pass

struct_WGPURenderPassColorAttachment._pack_ = 1 # source:False
struct_WGPURenderPassColorAttachment._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('view', ctypes.POINTER(struct_WGPUTextureViewImpl)),
    ('depthSlice', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('resolveTarget', ctypes.POINTER(struct_WGPUTextureViewImpl)),
    ('loadOp', WGPULoadOp),
    ('storeOp', WGPUStoreOp),
    ('clearValue', WGPUColor),
]

WGPURenderPassColorAttachment = struct_WGPURenderPassColorAttachment
class struct_WGPURenderPassStorageAttachment(Structure):
    pass

struct_WGPURenderPassStorageAttachment._pack_ = 1 # source:False
struct_WGPURenderPassStorageAttachment._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('offset', ctypes.c_uint64),
    ('storage', ctypes.POINTER(struct_WGPUTextureViewImpl)),
    ('loadOp', WGPULoadOp),
    ('storeOp', WGPUStoreOp),
    ('clearValue', WGPUColor),
]

WGPURenderPassStorageAttachment = struct_WGPURenderPassStorageAttachment
class struct_WGPURequiredLimits(Structure):
    pass

struct_WGPURequiredLimits._pack_ = 1 # source:False
struct_WGPURequiredLimits._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('limits', WGPULimits),
]

WGPURequiredLimits = struct_WGPURequiredLimits
class struct_WGPUSharedTextureMemoryAHardwareBufferProperties(Structure):
    _pack_ = 1 # source:False
    _fields_ = [
    ('chain', WGPUChainedStructOut),
    ('yCbCrInfo', WGPUYCbCrVkDescriptor),
     ]

WGPUSharedTextureMemoryAHardwareBufferProperties = struct_WGPUSharedTextureMemoryAHardwareBufferProperties
class struct_WGPUSharedTextureMemoryDmaBufDescriptor(Structure):
    pass

struct_WGPUSharedTextureMemoryDmaBufDescriptor._pack_ = 1 # source:False
struct_WGPUSharedTextureMemoryDmaBufDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('size', WGPUExtent3D),
    ('drmFormat', ctypes.c_uint32),
    ('drmModifier', ctypes.c_uint64),
    ('planeCount', ctypes.c_uint64),
    ('planes', ctypes.POINTER(struct_WGPUSharedTextureMemoryDmaBufPlane)),
]

WGPUSharedTextureMemoryDmaBufDescriptor = struct_WGPUSharedTextureMemoryDmaBufDescriptor
class struct_WGPUSharedTextureMemoryProperties(Structure):
    pass

struct_WGPUSharedTextureMemoryProperties._pack_ = 1 # source:False
struct_WGPUSharedTextureMemoryProperties._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStructOut)),
    ('usage', ctypes.c_uint32),
    ('size', WGPUExtent3D),
    ('format', WGPUTextureFormat),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSharedTextureMemoryProperties = struct_WGPUSharedTextureMemoryProperties
class struct_WGPUSupportedLimits(Structure):
    pass

struct_WGPUSupportedLimits._pack_ = 1 # source:False
struct_WGPUSupportedLimits._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStructOut)),
    ('limits', WGPULimits),
]

WGPUSupportedLimits = struct_WGPUSupportedLimits
class struct_WGPUTextureDescriptor(Structure):
    pass

struct_WGPUTextureDescriptor._pack_ = 1 # source:False
struct_WGPUTextureDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', ctypes.POINTER(ctypes.c_char)),
    ('usage', ctypes.c_uint32),
    ('dimension', WGPUTextureDimension),
    ('size', WGPUExtent3D),
    ('format', WGPUTextureFormat),
    ('mipLevelCount', ctypes.c_uint32),
    ('sampleCount', ctypes.c_uint32),
    ('viewFormatCount', ctypes.c_uint64),
    ('viewFormats', ctypes.POINTER(WGPUTextureFormat)),
]

WGPUTextureDescriptor = struct_WGPUTextureDescriptor
class struct_WGPUVertexBufferLayout(Structure):
    pass

struct_WGPUVertexBufferLayout._pack_ = 1 # source:False
struct_WGPUVertexBufferLayout._fields_ = [
    ('arrayStride', ctypes.c_uint64),
    ('stepMode', WGPUVertexStepMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('attributeCount', ctypes.c_uint64),
    ('attributes', ctypes.POINTER(struct_WGPUVertexAttribute)),
]

WGPUVertexBufferLayout = struct_WGPUVertexBufferLayout
class struct_WGPUBindGroupLayoutDescriptor(Structure):
    pass

struct_WGPUBindGroupLayoutDescriptor._pack_ = 1 # source:False
struct_WGPUBindGroupLayoutDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', ctypes.POINTER(ctypes.c_char)),
    ('entryCount', ctypes.c_uint64),
    ('entries', ctypes.POINTER(struct_WGPUBindGroupLayoutEntry)),
]

WGPUBindGroupLayoutDescriptor = struct_WGPUBindGroupLayoutDescriptor
class struct_WGPUColorTargetState(Structure):
    pass

struct_WGPUColorTargetState._pack_ = 1 # source:False
struct_WGPUColorTargetState._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('format', WGPUTextureFormat),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('blend', ctypes.POINTER(struct_WGPUBlendState)),
    ('writeMask', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
]

WGPUColorTargetState = struct_WGPUColorTargetState
class struct_WGPUComputePipelineDescriptor(Structure):
    pass

struct_WGPUComputePipelineDescriptor._pack_ = 1 # source:False
struct_WGPUComputePipelineDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', ctypes.POINTER(ctypes.c_char)),
    ('layout', ctypes.POINTER(struct_WGPUPipelineLayoutImpl)),
    ('compute', WGPUProgrammableStageDescriptor),
]

WGPUComputePipelineDescriptor = struct_WGPUComputePipelineDescriptor
class struct_WGPUDeviceDescriptor(Structure):
    pass

struct_WGPUDeviceDescriptor._pack_ = 1 # source:False
struct_WGPUDeviceDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', ctypes.POINTER(ctypes.c_char)),
    ('requiredFeatureCount', ctypes.c_uint64),
    ('requiredFeatures', ctypes.POINTER(WGPUFeatureName)),
    ('requiredLimits', ctypes.POINTER(struct_WGPURequiredLimits)),
    ('defaultQueue', WGPUQueueDescriptor),
    ('deviceLostCallback', ctypes.CFUNCTYPE(None, WGPUDeviceLostReason, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None))),
    ('deviceLostUserdata', ctypes.POINTER(None)),
    ('deviceLostCallbackInfo', WGPUDeviceLostCallbackInfo),
    ('uncapturedErrorCallbackInfo', WGPUUncapturedErrorCallbackInfo),
]

WGPUDeviceDescriptor = struct_WGPUDeviceDescriptor
class struct_WGPURenderPassDescriptor(Structure):
    pass

struct_WGPURenderPassDescriptor._pack_ = 1 # source:False
struct_WGPURenderPassDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', ctypes.POINTER(ctypes.c_char)),
    ('colorAttachmentCount', ctypes.c_uint64),
    ('colorAttachments', ctypes.POINTER(struct_WGPURenderPassColorAttachment)),
    ('depthStencilAttachment', ctypes.POINTER(struct_WGPURenderPassDepthStencilAttachment)),
    ('occlusionQuerySet', ctypes.POINTER(struct_WGPUQuerySetImpl)),
    ('timestampWrites', ctypes.POINTER(struct_WGPURenderPassTimestampWrites)),
]

WGPURenderPassDescriptor = struct_WGPURenderPassDescriptor
class struct_WGPURenderPassPixelLocalStorage(Structure):
    pass

struct_WGPURenderPassPixelLocalStorage._pack_ = 1 # source:False
struct_WGPURenderPassPixelLocalStorage._fields_ = [
    ('chain', WGPUChainedStruct),
    ('totalPixelLocalStorageSize', ctypes.c_uint64),
    ('storageAttachmentCount', ctypes.c_uint64),
    ('storageAttachments', ctypes.POINTER(struct_WGPURenderPassStorageAttachment)),
]

WGPURenderPassPixelLocalStorage = struct_WGPURenderPassPixelLocalStorage
class struct_WGPUVertexState(Structure):
    pass

struct_WGPUVertexState._pack_ = 1 # source:False
struct_WGPUVertexState._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('module', ctypes.POINTER(struct_WGPUShaderModuleImpl)),
    ('entryPoint', ctypes.POINTER(ctypes.c_char)),
    ('constantCount', ctypes.c_uint64),
    ('constants', ctypes.POINTER(struct_WGPUConstantEntry)),
    ('bufferCount', ctypes.c_uint64),
    ('buffers', ctypes.POINTER(struct_WGPUVertexBufferLayout)),
]

WGPUVertexState = struct_WGPUVertexState
class struct_WGPUFragmentState(Structure):
    pass

struct_WGPUFragmentState._pack_ = 1 # source:False
struct_WGPUFragmentState._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('module', ctypes.POINTER(struct_WGPUShaderModuleImpl)),
    ('entryPoint', ctypes.POINTER(ctypes.c_char)),
    ('constantCount', ctypes.c_uint64),
    ('constants', ctypes.POINTER(struct_WGPUConstantEntry)),
    ('targetCount', ctypes.c_uint64),
    ('targets', ctypes.POINTER(struct_WGPUColorTargetState)),
]

WGPUFragmentState = struct_WGPUFragmentState
class struct_WGPURenderPipelineDescriptor(Structure):
    pass

struct_WGPURenderPipelineDescriptor._pack_ = 1 # source:False
struct_WGPURenderPipelineDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', ctypes.POINTER(ctypes.c_char)),
    ('layout', ctypes.POINTER(struct_WGPUPipelineLayoutImpl)),
    ('vertex', WGPUVertexState),
    ('primitive', WGPUPrimitiveState),
    ('depthStencil', ctypes.POINTER(struct_WGPUDepthStencilState)),
    ('multisample', WGPUMultisampleState),
    ('fragment', ctypes.POINTER(struct_WGPUFragmentState)),
]

WGPURenderPipelineDescriptor = struct_WGPURenderPipelineDescriptor
class struct_WGPUBufferMapCallbackInfo2(Structure):
    pass

struct_WGPUBufferMapCallbackInfo2._pack_ = 1 # source:False
struct_WGPUBufferMapCallbackInfo2._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, WGPUMapAsyncStatus, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), ctypes.POINTER(None))),
    ('userdata1', ctypes.POINTER(None)),
    ('userdata2', ctypes.POINTER(None)),
]

WGPUBufferMapCallbackInfo2 = struct_WGPUBufferMapCallbackInfo2
class struct_WGPUCompilationInfoCallbackInfo2(Structure):
    pass

struct_WGPUCompilationInfoCallbackInfo2._pack_ = 1 # source:False
struct_WGPUCompilationInfoCallbackInfo2._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, WGPUCompilationInfoRequestStatus, ctypes.POINTER(struct_WGPUCompilationInfo), ctypes.POINTER(None), ctypes.POINTER(None))),
    ('userdata1', ctypes.POINTER(None)),
    ('userdata2', ctypes.POINTER(None)),
]

WGPUCompilationInfoCallbackInfo2 = struct_WGPUCompilationInfoCallbackInfo2
class struct_WGPUCreateComputePipelineAsyncCallbackInfo2(Structure):
    pass

struct_WGPUCreateComputePipelineAsyncCallbackInfo2._pack_ = 1 # source:False
struct_WGPUCreateComputePipelineAsyncCallbackInfo2._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, WGPUCreatePipelineAsyncStatus, ctypes.POINTER(struct_WGPUComputePipelineImpl), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), ctypes.POINTER(None))),
    ('userdata1', ctypes.POINTER(None)),
    ('userdata2', ctypes.POINTER(None)),
]

WGPUCreateComputePipelineAsyncCallbackInfo2 = struct_WGPUCreateComputePipelineAsyncCallbackInfo2
class struct_WGPUCreateRenderPipelineAsyncCallbackInfo2(Structure):
    pass

struct_WGPUCreateRenderPipelineAsyncCallbackInfo2._pack_ = 1 # source:False
struct_WGPUCreateRenderPipelineAsyncCallbackInfo2._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, WGPUCreatePipelineAsyncStatus, ctypes.POINTER(struct_WGPURenderPipelineImpl), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), ctypes.POINTER(None))),
    ('userdata1', ctypes.POINTER(None)),
    ('userdata2', ctypes.POINTER(None)),
]

WGPUCreateRenderPipelineAsyncCallbackInfo2 = struct_WGPUCreateRenderPipelineAsyncCallbackInfo2
class struct_WGPUPopErrorScopeCallbackInfo2(Structure):
    pass

struct_WGPUPopErrorScopeCallbackInfo2._pack_ = 1 # source:False
struct_WGPUPopErrorScopeCallbackInfo2._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, WGPUPopErrorScopeStatus, WGPUErrorType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), ctypes.POINTER(None))),
    ('userdata1', ctypes.POINTER(None)),
    ('userdata2', ctypes.POINTER(None)),
]

WGPUPopErrorScopeCallbackInfo2 = struct_WGPUPopErrorScopeCallbackInfo2
class struct_WGPUQueueWorkDoneCallbackInfo2(Structure):
    pass

struct_WGPUQueueWorkDoneCallbackInfo2._pack_ = 1 # source:False
struct_WGPUQueueWorkDoneCallbackInfo2._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, WGPUQueueWorkDoneStatus, ctypes.POINTER(None), ctypes.POINTER(None))),
    ('userdata1', ctypes.POINTER(None)),
    ('userdata2', ctypes.POINTER(None)),
]

WGPUQueueWorkDoneCallbackInfo2 = struct_WGPUQueueWorkDoneCallbackInfo2
class struct_WGPURequestAdapterCallbackInfo2(Structure):
    pass

struct_WGPURequestAdapterCallbackInfo2._pack_ = 1 # source:False
struct_WGPURequestAdapterCallbackInfo2._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, WGPURequestAdapterStatus, ctypes.POINTER(struct_WGPUAdapterImpl), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), ctypes.POINTER(None))),
    ('userdata1', ctypes.POINTER(None)),
    ('userdata2', ctypes.POINTER(None)),
]

WGPURequestAdapterCallbackInfo2 = struct_WGPURequestAdapterCallbackInfo2
class struct_WGPURequestDeviceCallbackInfo2(Structure):
    pass

struct_WGPURequestDeviceCallbackInfo2._pack_ = 1 # source:False
struct_WGPURequestDeviceCallbackInfo2._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, WGPURequestDeviceStatus, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None), ctypes.POINTER(None))),
    ('userdata1', ctypes.POINTER(None)),
    ('userdata2', ctypes.POINTER(None)),
]

WGPURequestDeviceCallbackInfo2 = struct_WGPURequestDeviceCallbackInfo2
WGPUProcAdapterInfoFreeMembers = ctypes.CFUNCTYPE(None, struct_WGPUAdapterInfo)
WGPUProcAdapterPropertiesFreeMembers = ctypes.CFUNCTYPE(None, struct_WGPUAdapterProperties)
WGPUProcAdapterPropertiesMemoryHeapsFreeMembers = ctypes.CFUNCTYPE(None, struct_WGPUAdapterPropertiesMemoryHeaps)
WGPUProcCreateInstance = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUInstanceImpl), ctypes.POINTER(struct_WGPUInstanceDescriptor))
WGPUProcDrmFormatCapabilitiesFreeMembers = ctypes.CFUNCTYPE(None, struct_WGPUDrmFormatCapabilities)
WGPUProcGetInstanceFeatures = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUInstanceFeatures))
WGPUProcGetProcAddress = ctypes.CFUNCTYPE(ctypes.CFUNCTYPE(None), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcSharedBufferMemoryEndAccessStateFreeMembers = ctypes.CFUNCTYPE(None, struct_WGPUSharedBufferMemoryEndAccessState)
WGPUProcSharedTextureMemoryEndAccessStateFreeMembers = ctypes.CFUNCTYPE(None, struct_WGPUSharedTextureMemoryEndAccessState)
WGPUProcSurfaceCapabilitiesFreeMembers = ctypes.CFUNCTYPE(None, struct_WGPUSurfaceCapabilities)
WGPUProcAdapterCreateDevice = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUAdapterImpl), ctypes.POINTER(struct_WGPUDeviceDescriptor))
WGPUProcAdapterEnumerateFeatures = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.POINTER(struct_WGPUAdapterImpl), ctypes.POINTER(WGPUFeatureName))
WGPUProcAdapterGetFormatCapabilities = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUAdapterImpl), WGPUTextureFormat, ctypes.POINTER(struct_WGPUFormatCapabilities))
WGPUProcAdapterGetInfo = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUAdapterImpl), ctypes.POINTER(struct_WGPUAdapterInfo))
WGPUProcAdapterGetInstance = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUInstanceImpl), ctypes.POINTER(struct_WGPUAdapterImpl))
WGPUProcAdapterGetLimits = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUAdapterImpl), ctypes.POINTER(struct_WGPUSupportedLimits))
WGPUProcAdapterGetProperties = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUAdapterImpl), ctypes.POINTER(struct_WGPUAdapterProperties))
WGPUProcAdapterHasFeature = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUAdapterImpl), WGPUFeatureName)
WGPUProcAdapterRequestDevice = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUAdapterImpl), ctypes.POINTER(struct_WGPUDeviceDescriptor), ctypes.CFUNCTYPE(None, WGPURequestDeviceStatus, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None)), ctypes.POINTER(None))
WGPUProcAdapterRequestDevice2 = ctypes.CFUNCTYPE(struct_WGPUFuture, ctypes.POINTER(struct_WGPUAdapterImpl), ctypes.POINTER(struct_WGPUDeviceDescriptor), struct_WGPURequestDeviceCallbackInfo2)
WGPUProcAdapterRequestDeviceF = ctypes.CFUNCTYPE(struct_WGPUFuture, ctypes.POINTER(struct_WGPUAdapterImpl), ctypes.POINTER(struct_WGPUDeviceDescriptor), struct_WGPURequestDeviceCallbackInfo)
WGPUProcAdapterAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUAdapterImpl))
WGPUProcAdapterRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUAdapterImpl))
WGPUProcBindGroupSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUBindGroupImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcBindGroupAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUBindGroupImpl))
WGPUProcBindGroupRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUBindGroupImpl))
WGPUProcBindGroupLayoutSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUBindGroupLayoutImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcBindGroupLayoutAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUBindGroupLayoutImpl))
WGPUProcBindGroupLayoutRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUBindGroupLayoutImpl))
WGPUProcBufferDestroy = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUBufferImpl))
WGPUProcBufferGetConstMappedRange = ctypes.CFUNCTYPE(ctypes.POINTER(None), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64, ctypes.c_uint64)
WGPUProcBufferGetMapState = ctypes.CFUNCTYPE(WGPUBufferMapState, ctypes.POINTER(struct_WGPUBufferImpl))
WGPUProcBufferGetMappedRange = ctypes.CFUNCTYPE(ctypes.POINTER(None), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64, ctypes.c_uint64)
WGPUProcBufferGetSize = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.POINTER(struct_WGPUBufferImpl))
WGPUProcBufferGetUsage = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUBufferImpl))
WGPUProcBufferMapAsync = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint32, ctypes.c_uint64, ctypes.c_uint64, ctypes.CFUNCTYPE(None, WGPUBufferMapAsyncStatus, ctypes.POINTER(None)), ctypes.POINTER(None))
WGPUProcBufferMapAsync2 = ctypes.CFUNCTYPE(struct_WGPUFuture, ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint32, ctypes.c_uint64, ctypes.c_uint64, struct_WGPUBufferMapCallbackInfo2)
WGPUProcBufferMapAsyncF = ctypes.CFUNCTYPE(struct_WGPUFuture, ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint32, ctypes.c_uint64, ctypes.c_uint64, struct_WGPUBufferMapCallbackInfo)
WGPUProcBufferSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUBufferImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcBufferUnmap = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUBufferImpl))
WGPUProcBufferAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUBufferImpl))
WGPUProcBufferRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUBufferImpl))
WGPUProcCommandBufferSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandBufferImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcCommandBufferAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandBufferImpl))
WGPUProcCommandBufferRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandBufferImpl))
WGPUProcCommandEncoderBeginComputePass = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUComputePassEncoderImpl), ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(struct_WGPUComputePassDescriptor))
WGPUProcCommandEncoderBeginRenderPass = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(struct_WGPURenderPassDescriptor))
WGPUProcCommandEncoderClearBuffer = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64, ctypes.c_uint64)
WGPUProcCommandEncoderCopyBufferToBuffer = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64, ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64, ctypes.c_uint64)
WGPUProcCommandEncoderCopyBufferToTexture = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(struct_WGPUImageCopyBuffer), ctypes.POINTER(struct_WGPUImageCopyTexture), ctypes.POINTER(struct_WGPUExtent3D))
WGPUProcCommandEncoderCopyTextureToBuffer = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(struct_WGPUImageCopyTexture), ctypes.POINTER(struct_WGPUImageCopyBuffer), ctypes.POINTER(struct_WGPUExtent3D))
WGPUProcCommandEncoderCopyTextureToTexture = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(struct_WGPUImageCopyTexture), ctypes.POINTER(struct_WGPUImageCopyTexture), ctypes.POINTER(struct_WGPUExtent3D))
WGPUProcCommandEncoderFinish = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUCommandBufferImpl), ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(struct_WGPUCommandBufferDescriptor))
WGPUProcCommandEncoderInjectValidationError = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcCommandEncoderInsertDebugMarker = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcCommandEncoderPopDebugGroup = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl))
WGPUProcCommandEncoderPushDebugGroup = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcCommandEncoderResolveQuerySet = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(struct_WGPUQuerySetImpl), ctypes.c_uint32, ctypes.c_uint32, ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64)
WGPUProcCommandEncoderSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcCommandEncoderWriteBuffer = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_uint64)
WGPUProcCommandEncoderWriteTimestamp = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(struct_WGPUQuerySetImpl), ctypes.c_uint32)
WGPUProcCommandEncoderAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl))
WGPUProcCommandEncoderRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl))
WGPUProcComputePassEncoderDispatchWorkgroups = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePassEncoderImpl), ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32)
WGPUProcComputePassEncoderDispatchWorkgroupsIndirect = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePassEncoderImpl), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64)
WGPUProcComputePassEncoderEnd = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePassEncoderImpl))
WGPUProcComputePassEncoderInsertDebugMarker = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePassEncoderImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcComputePassEncoderPopDebugGroup = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePassEncoderImpl))
WGPUProcComputePassEncoderPushDebugGroup = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePassEncoderImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcComputePassEncoderSetBindGroup = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePassEncoderImpl), ctypes.c_uint32, ctypes.POINTER(struct_WGPUBindGroupImpl), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint32))
WGPUProcComputePassEncoderSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePassEncoderImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcComputePassEncoderSetPipeline = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePassEncoderImpl), ctypes.POINTER(struct_WGPUComputePipelineImpl))
WGPUProcComputePassEncoderWriteTimestamp = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePassEncoderImpl), ctypes.POINTER(struct_WGPUQuerySetImpl), ctypes.c_uint32)
WGPUProcComputePassEncoderAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePassEncoderImpl))
WGPUProcComputePassEncoderRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePassEncoderImpl))
WGPUProcComputePipelineGetBindGroupLayout = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUBindGroupLayoutImpl), ctypes.POINTER(struct_WGPUComputePipelineImpl), ctypes.c_uint32)
WGPUProcComputePipelineSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePipelineImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcComputePipelineAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePipelineImpl))
WGPUProcComputePipelineRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePipelineImpl))
WGPUProcDeviceCreateBindGroup = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUBindGroupImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUBindGroupDescriptor))
WGPUProcDeviceCreateBindGroupLayout = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUBindGroupLayoutImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUBindGroupLayoutDescriptor))
WGPUProcDeviceCreateBuffer = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUBufferImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUBufferDescriptor))
WGPUProcDeviceCreateCommandEncoder = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUCommandEncoderDescriptor))
WGPUProcDeviceCreateComputePipeline = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUComputePipelineImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUComputePipelineDescriptor))
WGPUProcDeviceCreateComputePipelineAsync = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUComputePipelineDescriptor), ctypes.CFUNCTYPE(None, WGPUCreatePipelineAsyncStatus, ctypes.POINTER(struct_WGPUComputePipelineImpl), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None)), ctypes.POINTER(None))
WGPUProcDeviceCreateComputePipelineAsync2 = ctypes.CFUNCTYPE(struct_WGPUFuture, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUComputePipelineDescriptor), struct_WGPUCreateComputePipelineAsyncCallbackInfo2)
WGPUProcDeviceCreateComputePipelineAsyncF = ctypes.CFUNCTYPE(struct_WGPUFuture, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUComputePipelineDescriptor), struct_WGPUCreateComputePipelineAsyncCallbackInfo)
WGPUProcDeviceCreateErrorBuffer = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUBufferImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUBufferDescriptor))
WGPUProcDeviceCreateErrorExternalTexture = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUExternalTextureImpl), ctypes.POINTER(struct_WGPUDeviceImpl))
WGPUProcDeviceCreateErrorShaderModule = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUShaderModuleImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUShaderModuleDescriptor), ctypes.POINTER(ctypes.c_char))
WGPUProcDeviceCreateErrorTexture = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUTextureImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUTextureDescriptor))
WGPUProcDeviceCreateExternalTexture = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUExternalTextureImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUExternalTextureDescriptor))
WGPUProcDeviceCreatePipelineLayout = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUPipelineLayoutImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUPipelineLayoutDescriptor))
WGPUProcDeviceCreateQuerySet = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUQuerySetImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUQuerySetDescriptor))
WGPUProcDeviceCreateRenderBundleEncoder = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPURenderBundleEncoderImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPURenderBundleEncoderDescriptor))
WGPUProcDeviceCreateRenderPipeline = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPURenderPipelineImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPURenderPipelineDescriptor))
WGPUProcDeviceCreateRenderPipelineAsync = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPURenderPipelineDescriptor), ctypes.CFUNCTYPE(None, WGPUCreatePipelineAsyncStatus, ctypes.POINTER(struct_WGPURenderPipelineImpl), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None)), ctypes.POINTER(None))
WGPUProcDeviceCreateRenderPipelineAsync2 = ctypes.CFUNCTYPE(struct_WGPUFuture, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPURenderPipelineDescriptor), struct_WGPUCreateRenderPipelineAsyncCallbackInfo2)
WGPUProcDeviceCreateRenderPipelineAsyncF = ctypes.CFUNCTYPE(struct_WGPUFuture, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPURenderPipelineDescriptor), struct_WGPUCreateRenderPipelineAsyncCallbackInfo)
WGPUProcDeviceCreateSampler = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUSamplerImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUSamplerDescriptor))
WGPUProcDeviceCreateShaderModule = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUShaderModuleImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUShaderModuleDescriptor))
WGPUProcDeviceCreateSwapChain = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUSwapChainImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUSurfaceImpl), ctypes.POINTER(struct_WGPUSwapChainDescriptor))
WGPUProcDeviceCreateTexture = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUTextureImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUTextureDescriptor))
WGPUProcDeviceDestroy = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl))
WGPUProcDeviceEnumerateFeatures = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(WGPUFeatureName))
WGPUProcDeviceForceLoss = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl), WGPUDeviceLostReason, ctypes.POINTER(ctypes.c_char))
WGPUProcDeviceGetAHardwareBufferProperties = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(None), ctypes.POINTER(struct_WGPUAHardwareBufferProperties))
WGPUProcDeviceGetAdapter = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUAdapterImpl), ctypes.POINTER(struct_WGPUDeviceImpl))
WGPUProcDeviceGetLimits = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUSupportedLimits))
WGPUProcDeviceGetQueue = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUQueueImpl), ctypes.POINTER(struct_WGPUDeviceImpl))
WGPUProcDeviceGetSupportedSurfaceUsage = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUSurfaceImpl))
WGPUProcDeviceHasFeature = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUDeviceImpl), WGPUFeatureName)
WGPUProcDeviceImportSharedBufferMemory = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUSharedBufferMemoryImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUSharedBufferMemoryDescriptor))
WGPUProcDeviceImportSharedFence = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUSharedFenceImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUSharedFenceDescriptor))
WGPUProcDeviceImportSharedTextureMemory = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUSharedTextureMemoryImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUSharedTextureMemoryDescriptor))
WGPUProcDeviceInjectError = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl), WGPUErrorType, ctypes.POINTER(ctypes.c_char))
WGPUProcDevicePopErrorScope = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.CFUNCTYPE(None, WGPUErrorType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None)), ctypes.POINTER(None))
WGPUProcDevicePopErrorScope2 = ctypes.CFUNCTYPE(struct_WGPUFuture, ctypes.POINTER(struct_WGPUDeviceImpl), struct_WGPUPopErrorScopeCallbackInfo2)
WGPUProcDevicePopErrorScopeF = ctypes.CFUNCTYPE(struct_WGPUFuture, ctypes.POINTER(struct_WGPUDeviceImpl), struct_WGPUPopErrorScopeCallbackInfo)
WGPUProcDevicePushErrorScope = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl), WGPUErrorFilter)
WGPUProcDeviceSetDeviceLostCallback = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.CFUNCTYPE(None, WGPUDeviceLostReason, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None)), ctypes.POINTER(None))
WGPUProcDeviceSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcDeviceSetLoggingCallback = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.CFUNCTYPE(None, WGPULoggingType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None)), ctypes.POINTER(None))
WGPUProcDeviceSetUncapturedErrorCallback = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.CFUNCTYPE(None, WGPUErrorType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None)), ctypes.POINTER(None))
WGPUProcDeviceTick = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl))
WGPUProcDeviceValidateTextureDescriptor = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUTextureDescriptor))
WGPUProcDeviceAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl))
WGPUProcDeviceRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl))
WGPUProcExternalTextureDestroy = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUExternalTextureImpl))
WGPUProcExternalTextureExpire = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUExternalTextureImpl))
WGPUProcExternalTextureRefresh = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUExternalTextureImpl))
WGPUProcExternalTextureSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUExternalTextureImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcExternalTextureAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUExternalTextureImpl))
WGPUProcExternalTextureRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUExternalTextureImpl))
WGPUProcInstanceCreateSurface = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUSurfaceImpl), ctypes.POINTER(struct_WGPUInstanceImpl), ctypes.POINTER(struct_WGPUSurfaceDescriptor))
WGPUProcInstanceEnumerateWGSLLanguageFeatures = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.POINTER(struct_WGPUInstanceImpl), ctypes.POINTER(WGPUWGSLFeatureName))
WGPUProcInstanceHasWGSLLanguageFeature = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUInstanceImpl), WGPUWGSLFeatureName)
WGPUProcInstanceProcessEvents = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUInstanceImpl))
WGPUProcInstanceRequestAdapter = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUInstanceImpl), ctypes.POINTER(struct_WGPURequestAdapterOptions), ctypes.CFUNCTYPE(None, WGPURequestAdapterStatus, ctypes.POINTER(struct_WGPUAdapterImpl), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(None)), ctypes.POINTER(None))
WGPUProcInstanceRequestAdapter2 = ctypes.CFUNCTYPE(struct_WGPUFuture, ctypes.POINTER(struct_WGPUInstanceImpl), ctypes.POINTER(struct_WGPURequestAdapterOptions), struct_WGPURequestAdapterCallbackInfo2)
WGPUProcInstanceRequestAdapterF = ctypes.CFUNCTYPE(struct_WGPUFuture, ctypes.POINTER(struct_WGPUInstanceImpl), ctypes.POINTER(struct_WGPURequestAdapterOptions), struct_WGPURequestAdapterCallbackInfo)
WGPUProcInstanceWaitAny = ctypes.CFUNCTYPE(WGPUWaitStatus, ctypes.POINTER(struct_WGPUInstanceImpl), ctypes.c_uint64, ctypes.POINTER(struct_WGPUFutureWaitInfo), ctypes.c_uint64)
WGPUProcInstanceAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUInstanceImpl))
WGPUProcInstanceRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUInstanceImpl))
WGPUProcPipelineLayoutSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUPipelineLayoutImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcPipelineLayoutAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUPipelineLayoutImpl))
WGPUProcPipelineLayoutRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUPipelineLayoutImpl))
WGPUProcQuerySetDestroy = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUQuerySetImpl))
WGPUProcQuerySetGetCount = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUQuerySetImpl))
WGPUProcQuerySetGetType = ctypes.CFUNCTYPE(WGPUQueryType, ctypes.POINTER(struct_WGPUQuerySetImpl))
WGPUProcQuerySetSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUQuerySetImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcQuerySetAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUQuerySetImpl))
WGPUProcQuerySetRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUQuerySetImpl))
WGPUProcQueueCopyExternalTextureForBrowser = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUQueueImpl), ctypes.POINTER(struct_WGPUImageCopyExternalTexture), ctypes.POINTER(struct_WGPUImageCopyTexture), ctypes.POINTER(struct_WGPUExtent3D), ctypes.POINTER(struct_WGPUCopyTextureForBrowserOptions))
WGPUProcQueueCopyTextureForBrowser = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUQueueImpl), ctypes.POINTER(struct_WGPUImageCopyTexture), ctypes.POINTER(struct_WGPUImageCopyTexture), ctypes.POINTER(struct_WGPUExtent3D), ctypes.POINTER(struct_WGPUCopyTextureForBrowserOptions))
WGPUProcQueueOnSubmittedWorkDone = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUQueueImpl), ctypes.CFUNCTYPE(None, WGPUQueueWorkDoneStatus, ctypes.POINTER(None)), ctypes.POINTER(None))
WGPUProcQueueOnSubmittedWorkDone2 = ctypes.CFUNCTYPE(struct_WGPUFuture, ctypes.POINTER(struct_WGPUQueueImpl), struct_WGPUQueueWorkDoneCallbackInfo2)
WGPUProcQueueOnSubmittedWorkDoneF = ctypes.CFUNCTYPE(struct_WGPUFuture, ctypes.POINTER(struct_WGPUQueueImpl), struct_WGPUQueueWorkDoneCallbackInfo)
WGPUProcQueueSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUQueueImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcQueueSubmit = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUQueueImpl), ctypes.c_uint64, ctypes.POINTER(ctypes.POINTER(struct_WGPUCommandBufferImpl)))
WGPUProcQueueWriteBuffer = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUQueueImpl), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64, ctypes.POINTER(None), ctypes.c_uint64)
WGPUProcQueueWriteTexture = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUQueueImpl), ctypes.POINTER(struct_WGPUImageCopyTexture), ctypes.POINTER(None), ctypes.c_uint64, ctypes.POINTER(struct_WGPUTextureDataLayout), ctypes.POINTER(struct_WGPUExtent3D))
WGPUProcQueueAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUQueueImpl))
WGPUProcQueueRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUQueueImpl))
WGPUProcRenderBundleSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcRenderBundleAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleImpl))
WGPUProcRenderBundleRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleImpl))
WGPUProcRenderBundleEncoderDraw = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleEncoderImpl), ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32)
WGPUProcRenderBundleEncoderDrawIndexed = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleEncoderImpl), ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_int32, ctypes.c_uint32)
WGPUProcRenderBundleEncoderDrawIndexedIndirect = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleEncoderImpl), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64)
WGPUProcRenderBundleEncoderDrawIndirect = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleEncoderImpl), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64)
WGPUProcRenderBundleEncoderFinish = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPURenderBundleImpl), ctypes.POINTER(struct_WGPURenderBundleEncoderImpl), ctypes.POINTER(struct_WGPURenderBundleDescriptor))
WGPUProcRenderBundleEncoderInsertDebugMarker = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleEncoderImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcRenderBundleEncoderPopDebugGroup = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleEncoderImpl))
WGPUProcRenderBundleEncoderPushDebugGroup = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleEncoderImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcRenderBundleEncoderSetBindGroup = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleEncoderImpl), ctypes.c_uint32, ctypes.POINTER(struct_WGPUBindGroupImpl), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint32))
WGPUProcRenderBundleEncoderSetIndexBuffer = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleEncoderImpl), ctypes.POINTER(struct_WGPUBufferImpl), WGPUIndexFormat, ctypes.c_uint64, ctypes.c_uint64)
WGPUProcRenderBundleEncoderSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleEncoderImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcRenderBundleEncoderSetPipeline = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleEncoderImpl), ctypes.POINTER(struct_WGPURenderPipelineImpl))
WGPUProcRenderBundleEncoderSetVertexBuffer = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleEncoderImpl), ctypes.c_uint32, ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64, ctypes.c_uint64)
WGPUProcRenderBundleEncoderAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleEncoderImpl))
WGPUProcRenderBundleEncoderRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleEncoderImpl))
WGPUProcRenderPassEncoderBeginOcclusionQuery = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.c_uint32)
WGPUProcRenderPassEncoderDraw = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32)
WGPUProcRenderPassEncoderDrawIndexed = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_int32, ctypes.c_uint32)
WGPUProcRenderPassEncoderDrawIndexedIndirect = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64)
WGPUProcRenderPassEncoderDrawIndirect = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64)
WGPUProcRenderPassEncoderEnd = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl))
WGPUProcRenderPassEncoderEndOcclusionQuery = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl))
WGPUProcRenderPassEncoderExecuteBundles = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.c_uint64, ctypes.POINTER(ctypes.POINTER(struct_WGPURenderBundleImpl)))
WGPUProcRenderPassEncoderInsertDebugMarker = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcRenderPassEncoderPixelLocalStorageBarrier = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl))
WGPUProcRenderPassEncoderPopDebugGroup = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl))
WGPUProcRenderPassEncoderPushDebugGroup = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcRenderPassEncoderSetBindGroup = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.c_uint32, ctypes.POINTER(struct_WGPUBindGroupImpl), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint32))
WGPUProcRenderPassEncoderSetBlendConstant = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.POINTER(struct_WGPUColor))
WGPUProcRenderPassEncoderSetIndexBuffer = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.POINTER(struct_WGPUBufferImpl), WGPUIndexFormat, ctypes.c_uint64, ctypes.c_uint64)
WGPUProcRenderPassEncoderSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcRenderPassEncoderSetPipeline = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.POINTER(struct_WGPURenderPipelineImpl))
WGPUProcRenderPassEncoderSetScissorRect = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32)
WGPUProcRenderPassEncoderSetStencilReference = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.c_uint32)
WGPUProcRenderPassEncoderSetVertexBuffer = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.c_uint32, ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64, ctypes.c_uint64)
WGPUProcRenderPassEncoderSetViewport = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float)
WGPUProcRenderPassEncoderWriteTimestamp = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.POINTER(struct_WGPUQuerySetImpl), ctypes.c_uint32)
WGPUProcRenderPassEncoderAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl))
WGPUProcRenderPassEncoderRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl))
WGPUProcRenderPipelineGetBindGroupLayout = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUBindGroupLayoutImpl), ctypes.POINTER(struct_WGPURenderPipelineImpl), ctypes.c_uint32)
WGPUProcRenderPipelineSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPipelineImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcRenderPipelineAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPipelineImpl))
WGPUProcRenderPipelineRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPipelineImpl))
WGPUProcSamplerSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSamplerImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcSamplerAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSamplerImpl))
WGPUProcSamplerRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSamplerImpl))
WGPUProcShaderModuleGetCompilationInfo = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUShaderModuleImpl), ctypes.CFUNCTYPE(None, WGPUCompilationInfoRequestStatus, ctypes.POINTER(struct_WGPUCompilationInfo), ctypes.POINTER(None)), ctypes.POINTER(None))
WGPUProcShaderModuleGetCompilationInfo2 = ctypes.CFUNCTYPE(struct_WGPUFuture, ctypes.POINTER(struct_WGPUShaderModuleImpl), struct_WGPUCompilationInfoCallbackInfo2)
WGPUProcShaderModuleGetCompilationInfoF = ctypes.CFUNCTYPE(struct_WGPUFuture, ctypes.POINTER(struct_WGPUShaderModuleImpl), struct_WGPUCompilationInfoCallbackInfo)
WGPUProcShaderModuleSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUShaderModuleImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcShaderModuleAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUShaderModuleImpl))
WGPUProcShaderModuleRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUShaderModuleImpl))
WGPUProcSharedBufferMemoryBeginAccess = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUSharedBufferMemoryImpl), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.POINTER(struct_WGPUSharedBufferMemoryBeginAccessDescriptor))
WGPUProcSharedBufferMemoryCreateBuffer = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUBufferImpl), ctypes.POINTER(struct_WGPUSharedBufferMemoryImpl), ctypes.POINTER(struct_WGPUBufferDescriptor))
WGPUProcSharedBufferMemoryEndAccess = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUSharedBufferMemoryImpl), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.POINTER(struct_WGPUSharedBufferMemoryEndAccessState))
WGPUProcSharedBufferMemoryGetProperties = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUSharedBufferMemoryImpl), ctypes.POINTER(struct_WGPUSharedBufferMemoryProperties))
WGPUProcSharedBufferMemoryIsDeviceLost = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUSharedBufferMemoryImpl))
WGPUProcSharedBufferMemorySetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSharedBufferMemoryImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcSharedBufferMemoryAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSharedBufferMemoryImpl))
WGPUProcSharedBufferMemoryRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSharedBufferMemoryImpl))
WGPUProcSharedFenceExportInfo = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSharedFenceImpl), ctypes.POINTER(struct_WGPUSharedFenceExportInfo))
WGPUProcSharedFenceAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSharedFenceImpl))
WGPUProcSharedFenceRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSharedFenceImpl))
WGPUProcSharedTextureMemoryBeginAccess = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUSharedTextureMemoryImpl), ctypes.POINTER(struct_WGPUTextureImpl), ctypes.POINTER(struct_WGPUSharedTextureMemoryBeginAccessDescriptor))
WGPUProcSharedTextureMemoryCreateTexture = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUTextureImpl), ctypes.POINTER(struct_WGPUSharedTextureMemoryImpl), ctypes.POINTER(struct_WGPUTextureDescriptor))
WGPUProcSharedTextureMemoryEndAccess = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUSharedTextureMemoryImpl), ctypes.POINTER(struct_WGPUTextureImpl), ctypes.POINTER(struct_WGPUSharedTextureMemoryEndAccessState))
WGPUProcSharedTextureMemoryGetProperties = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUSharedTextureMemoryImpl), ctypes.POINTER(struct_WGPUSharedTextureMemoryProperties))
WGPUProcSharedTextureMemoryIsDeviceLost = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUSharedTextureMemoryImpl))
WGPUProcSharedTextureMemorySetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSharedTextureMemoryImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcSharedTextureMemoryAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSharedTextureMemoryImpl))
WGPUProcSharedTextureMemoryRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSharedTextureMemoryImpl))
WGPUProcSurfaceConfigure = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSurfaceImpl), ctypes.POINTER(struct_WGPUSurfaceConfiguration))
WGPUProcSurfaceGetCapabilities = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUSurfaceImpl), ctypes.POINTER(struct_WGPUAdapterImpl), ctypes.POINTER(struct_WGPUSurfaceCapabilities))
WGPUProcSurfaceGetCurrentTexture = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSurfaceImpl), ctypes.POINTER(struct_WGPUSurfaceTexture))
WGPUProcSurfaceGetPreferredFormat = ctypes.CFUNCTYPE(WGPUTextureFormat, ctypes.POINTER(struct_WGPUSurfaceImpl), ctypes.POINTER(struct_WGPUAdapterImpl))
WGPUProcSurfacePresent = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSurfaceImpl))
WGPUProcSurfaceUnconfigure = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSurfaceImpl))
WGPUProcSurfaceAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSurfaceImpl))
WGPUProcSurfaceRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSurfaceImpl))
WGPUProcSwapChainGetCurrentTexture = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUTextureImpl), ctypes.POINTER(struct_WGPUSwapChainImpl))
WGPUProcSwapChainGetCurrentTextureView = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUTextureViewImpl), ctypes.POINTER(struct_WGPUSwapChainImpl))
WGPUProcSwapChainPresent = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSwapChainImpl))
WGPUProcSwapChainAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSwapChainImpl))
WGPUProcSwapChainRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSwapChainImpl))
WGPUProcTextureCreateErrorView = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUTextureViewImpl), ctypes.POINTER(struct_WGPUTextureImpl), ctypes.POINTER(struct_WGPUTextureViewDescriptor))
WGPUProcTextureCreateView = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUTextureViewImpl), ctypes.POINTER(struct_WGPUTextureImpl), ctypes.POINTER(struct_WGPUTextureViewDescriptor))
WGPUProcTextureDestroy = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUTextureImpl))
WGPUProcTextureGetDepthOrArrayLayers = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUTextureImpl))
WGPUProcTextureGetDimension = ctypes.CFUNCTYPE(WGPUTextureDimension, ctypes.POINTER(struct_WGPUTextureImpl))
WGPUProcTextureGetFormat = ctypes.CFUNCTYPE(WGPUTextureFormat, ctypes.POINTER(struct_WGPUTextureImpl))
WGPUProcTextureGetHeight = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUTextureImpl))
WGPUProcTextureGetMipLevelCount = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUTextureImpl))
WGPUProcTextureGetSampleCount = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUTextureImpl))
WGPUProcTextureGetUsage = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUTextureImpl))
WGPUProcTextureGetWidth = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUTextureImpl))
WGPUProcTextureSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUTextureImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcTextureAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUTextureImpl))
WGPUProcTextureRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUTextureImpl))
WGPUProcTextureViewSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUTextureViewImpl), ctypes.POINTER(ctypes.c_char))
WGPUProcTextureViewAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUTextureViewImpl))
WGPUProcTextureViewRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUTextureViewImpl))
wgpuAdapterInfoFreeMembers = _libraries['libwebgpu_dawn.so'].wgpuAdapterInfoFreeMembers
wgpuAdapterInfoFreeMembers.restype = None
wgpuAdapterInfoFreeMembers.argtypes = [WGPUAdapterInfo]
wgpuAdapterPropertiesFreeMembers = _libraries['FIXME_STUB'].wgpuAdapterPropertiesFreeMembers
wgpuAdapterPropertiesFreeMembers.restype = None
wgpuAdapterPropertiesFreeMembers.argtypes = [WGPUAdapterProperties]
wgpuAdapterPropertiesMemoryHeapsFreeMembers = _libraries['libwebgpu_dawn.so'].wgpuAdapterPropertiesMemoryHeapsFreeMembers
wgpuAdapterPropertiesMemoryHeapsFreeMembers.restype = None
wgpuAdapterPropertiesMemoryHeapsFreeMembers.argtypes = [WGPUAdapterPropertiesMemoryHeaps]
wgpuCreateInstance = _libraries['libwebgpu_dawn.so'].wgpuCreateInstance
wgpuCreateInstance.restype = WGPUInstance
wgpuCreateInstance.argtypes = [ctypes.POINTER(struct_WGPUInstanceDescriptor)]
wgpuDrmFormatCapabilitiesFreeMembers = _libraries['libwebgpu_dawn.so'].wgpuDrmFormatCapabilitiesFreeMembers
wgpuDrmFormatCapabilitiesFreeMembers.restype = None
wgpuDrmFormatCapabilitiesFreeMembers.argtypes = [WGPUDrmFormatCapabilities]
wgpuGetInstanceFeatures = _libraries['libwebgpu_dawn.so'].wgpuGetInstanceFeatures
wgpuGetInstanceFeatures.restype = WGPUStatus
wgpuGetInstanceFeatures.argtypes = [ctypes.POINTER(struct_WGPUInstanceFeatures)]
wgpuGetProcAddress = _libraries['libwebgpu_dawn.so'].wgpuGetProcAddress
wgpuGetProcAddress.restype = WGPUProc
wgpuGetProcAddress.argtypes = [WGPUDevice, ctypes.POINTER(ctypes.c_char)]
wgpuSharedBufferMemoryEndAccessStateFreeMembers = _libraries['libwebgpu_dawn.so'].wgpuSharedBufferMemoryEndAccessStateFreeMembers
wgpuSharedBufferMemoryEndAccessStateFreeMembers.restype = None
wgpuSharedBufferMemoryEndAccessStateFreeMembers.argtypes = [WGPUSharedBufferMemoryEndAccessState]
wgpuSharedTextureMemoryEndAccessStateFreeMembers = _libraries['libwebgpu_dawn.so'].wgpuSharedTextureMemoryEndAccessStateFreeMembers
wgpuSharedTextureMemoryEndAccessStateFreeMembers.restype = None
wgpuSharedTextureMemoryEndAccessStateFreeMembers.argtypes = [WGPUSharedTextureMemoryEndAccessState]
wgpuSurfaceCapabilitiesFreeMembers = _libraries['libwebgpu_dawn.so'].wgpuSurfaceCapabilitiesFreeMembers
wgpuSurfaceCapabilitiesFreeMembers.restype = None
wgpuSurfaceCapabilitiesFreeMembers.argtypes = [WGPUSurfaceCapabilities]
wgpuAdapterCreateDevice = _libraries['libwebgpu_dawn.so'].wgpuAdapterCreateDevice
wgpuAdapterCreateDevice.restype = WGPUDevice
wgpuAdapterCreateDevice.argtypes = [WGPUAdapter, ctypes.POINTER(struct_WGPUDeviceDescriptor)]
size_t = ctypes.c_uint64
wgpuAdapterEnumerateFeatures = _libraries['FIXME_STUB'].wgpuAdapterEnumerateFeatures
wgpuAdapterEnumerateFeatures.restype = size_t
wgpuAdapterEnumerateFeatures.argtypes = [WGPUAdapter, ctypes.POINTER(WGPUFeatureName)]
wgpuAdapterGetFormatCapabilities = _libraries['libwebgpu_dawn.so'].wgpuAdapterGetFormatCapabilities
wgpuAdapterGetFormatCapabilities.restype = WGPUStatus
wgpuAdapterGetFormatCapabilities.argtypes = [WGPUAdapter, WGPUTextureFormat, ctypes.POINTER(struct_WGPUFormatCapabilities)]
wgpuAdapterGetInfo = _libraries['libwebgpu_dawn.so'].wgpuAdapterGetInfo
wgpuAdapterGetInfo.restype = WGPUStatus
wgpuAdapterGetInfo.argtypes = [WGPUAdapter, ctypes.POINTER(struct_WGPUAdapterInfo)]
wgpuAdapterGetInstance = _libraries['libwebgpu_dawn.so'].wgpuAdapterGetInstance
wgpuAdapterGetInstance.restype = WGPUInstance
wgpuAdapterGetInstance.argtypes = [WGPUAdapter]
wgpuAdapterGetLimits = _libraries['libwebgpu_dawn.so'].wgpuAdapterGetLimits
wgpuAdapterGetLimits.restype = WGPUStatus
wgpuAdapterGetLimits.argtypes = [WGPUAdapter, ctypes.POINTER(struct_WGPUSupportedLimits)]
wgpuAdapterGetProperties = _libraries['FIXME_STUB'].wgpuAdapterGetProperties
wgpuAdapterGetProperties.restype = WGPUStatus
wgpuAdapterGetProperties.argtypes = [WGPUAdapter, ctypes.POINTER(struct_WGPUAdapterProperties)]
wgpuAdapterHasFeature = _libraries['libwebgpu_dawn.so'].wgpuAdapterHasFeature
wgpuAdapterHasFeature.restype = WGPUBool
wgpuAdapterHasFeature.argtypes = [WGPUAdapter, WGPUFeatureName]
wgpuAdapterRequestDevice = _libraries['libwebgpu_dawn.so'].wgpuAdapterRequestDevice
wgpuAdapterRequestDevice.restype = None
wgpuAdapterRequestDevice.argtypes = [WGPUAdapter, ctypes.POINTER(struct_WGPUDeviceDescriptor), WGPURequestDeviceCallback, ctypes.POINTER(None)]
wgpuAdapterRequestDevice2 = _libraries['libwebgpu_dawn.so'].wgpuAdapterRequestDevice2
wgpuAdapterRequestDevice2.restype = WGPUFuture
wgpuAdapterRequestDevice2.argtypes = [WGPUAdapter, ctypes.POINTER(struct_WGPUDeviceDescriptor), WGPURequestDeviceCallbackInfo2]
wgpuAdapterRequestDeviceF = _libraries['libwebgpu_dawn.so'].wgpuAdapterRequestDeviceF
wgpuAdapterRequestDeviceF.restype = WGPUFuture
wgpuAdapterRequestDeviceF.argtypes = [WGPUAdapter, ctypes.POINTER(struct_WGPUDeviceDescriptor), WGPURequestDeviceCallbackInfo]
wgpuAdapterAddRef = _libraries['libwebgpu_dawn.so'].wgpuAdapterAddRef
wgpuAdapterAddRef.restype = None
wgpuAdapterAddRef.argtypes = [WGPUAdapter]
wgpuAdapterRelease = _libraries['libwebgpu_dawn.so'].wgpuAdapterRelease
wgpuAdapterRelease.restype = None
wgpuAdapterRelease.argtypes = [WGPUAdapter]
wgpuBindGroupSetLabel = _libraries['libwebgpu_dawn.so'].wgpuBindGroupSetLabel
wgpuBindGroupSetLabel.restype = None
wgpuBindGroupSetLabel.argtypes = [WGPUBindGroup, ctypes.POINTER(ctypes.c_char)]
wgpuBindGroupAddRef = _libraries['libwebgpu_dawn.so'].wgpuBindGroupAddRef
wgpuBindGroupAddRef.restype = None
wgpuBindGroupAddRef.argtypes = [WGPUBindGroup]
wgpuBindGroupRelease = _libraries['libwebgpu_dawn.so'].wgpuBindGroupRelease
wgpuBindGroupRelease.restype = None
wgpuBindGroupRelease.argtypes = [WGPUBindGroup]
wgpuBindGroupLayoutSetLabel = _libraries['libwebgpu_dawn.so'].wgpuBindGroupLayoutSetLabel
wgpuBindGroupLayoutSetLabel.restype = None
wgpuBindGroupLayoutSetLabel.argtypes = [WGPUBindGroupLayout, ctypes.POINTER(ctypes.c_char)]
wgpuBindGroupLayoutAddRef = _libraries['libwebgpu_dawn.so'].wgpuBindGroupLayoutAddRef
wgpuBindGroupLayoutAddRef.restype = None
wgpuBindGroupLayoutAddRef.argtypes = [WGPUBindGroupLayout]
wgpuBindGroupLayoutRelease = _libraries['libwebgpu_dawn.so'].wgpuBindGroupLayoutRelease
wgpuBindGroupLayoutRelease.restype = None
wgpuBindGroupLayoutRelease.argtypes = [WGPUBindGroupLayout]
wgpuBufferDestroy = _libraries['libwebgpu_dawn.so'].wgpuBufferDestroy
wgpuBufferDestroy.restype = None
wgpuBufferDestroy.argtypes = [WGPUBuffer]
wgpuBufferGetConstMappedRange = _libraries['libwebgpu_dawn.so'].wgpuBufferGetConstMappedRange
wgpuBufferGetConstMappedRange.restype = ctypes.POINTER(None)
wgpuBufferGetConstMappedRange.argtypes = [WGPUBuffer, size_t, size_t]
wgpuBufferGetMapState = _libraries['libwebgpu_dawn.so'].wgpuBufferGetMapState
wgpuBufferGetMapState.restype = WGPUBufferMapState
wgpuBufferGetMapState.argtypes = [WGPUBuffer]
wgpuBufferGetMappedRange = _libraries['libwebgpu_dawn.so'].wgpuBufferGetMappedRange
wgpuBufferGetMappedRange.restype = ctypes.POINTER(None)
wgpuBufferGetMappedRange.argtypes = [WGPUBuffer, size_t, size_t]
uint64_t = ctypes.c_uint64
wgpuBufferGetSize = _libraries['libwebgpu_dawn.so'].wgpuBufferGetSize
wgpuBufferGetSize.restype = uint64_t
wgpuBufferGetSize.argtypes = [WGPUBuffer]
wgpuBufferGetUsage = _libraries['libwebgpu_dawn.so'].wgpuBufferGetUsage
wgpuBufferGetUsage.restype = WGPUBufferUsageFlags
wgpuBufferGetUsage.argtypes = [WGPUBuffer]
wgpuBufferMapAsync = _libraries['libwebgpu_dawn.so'].wgpuBufferMapAsync
wgpuBufferMapAsync.restype = None
wgpuBufferMapAsync.argtypes = [WGPUBuffer, WGPUMapModeFlags, size_t, size_t, WGPUBufferMapCallback, ctypes.POINTER(None)]
wgpuBufferMapAsync2 = _libraries['libwebgpu_dawn.so'].wgpuBufferMapAsync2
wgpuBufferMapAsync2.restype = WGPUFuture
wgpuBufferMapAsync2.argtypes = [WGPUBuffer, WGPUMapModeFlags, size_t, size_t, WGPUBufferMapCallbackInfo2]
wgpuBufferMapAsyncF = _libraries['libwebgpu_dawn.so'].wgpuBufferMapAsyncF
wgpuBufferMapAsyncF.restype = WGPUFuture
wgpuBufferMapAsyncF.argtypes = [WGPUBuffer, WGPUMapModeFlags, size_t, size_t, WGPUBufferMapCallbackInfo]
wgpuBufferSetLabel = _libraries['libwebgpu_dawn.so'].wgpuBufferSetLabel
wgpuBufferSetLabel.restype = None
wgpuBufferSetLabel.argtypes = [WGPUBuffer, ctypes.POINTER(ctypes.c_char)]
wgpuBufferUnmap = _libraries['libwebgpu_dawn.so'].wgpuBufferUnmap
wgpuBufferUnmap.restype = None
wgpuBufferUnmap.argtypes = [WGPUBuffer]
wgpuBufferAddRef = _libraries['libwebgpu_dawn.so'].wgpuBufferAddRef
wgpuBufferAddRef.restype = None
wgpuBufferAddRef.argtypes = [WGPUBuffer]
wgpuBufferRelease = _libraries['libwebgpu_dawn.so'].wgpuBufferRelease
wgpuBufferRelease.restype = None
wgpuBufferRelease.argtypes = [WGPUBuffer]
wgpuCommandBufferSetLabel = _libraries['libwebgpu_dawn.so'].wgpuCommandBufferSetLabel
wgpuCommandBufferSetLabel.restype = None
wgpuCommandBufferSetLabel.argtypes = [WGPUCommandBuffer, ctypes.POINTER(ctypes.c_char)]
wgpuCommandBufferAddRef = _libraries['libwebgpu_dawn.so'].wgpuCommandBufferAddRef
wgpuCommandBufferAddRef.restype = None
wgpuCommandBufferAddRef.argtypes = [WGPUCommandBuffer]
wgpuCommandBufferRelease = _libraries['libwebgpu_dawn.so'].wgpuCommandBufferRelease
wgpuCommandBufferRelease.restype = None
wgpuCommandBufferRelease.argtypes = [WGPUCommandBuffer]
wgpuCommandEncoderBeginComputePass = _libraries['libwebgpu_dawn.so'].wgpuCommandEncoderBeginComputePass
wgpuCommandEncoderBeginComputePass.restype = WGPUComputePassEncoder
wgpuCommandEncoderBeginComputePass.argtypes = [WGPUCommandEncoder, ctypes.POINTER(struct_WGPUComputePassDescriptor)]
wgpuCommandEncoderBeginRenderPass = _libraries['libwebgpu_dawn.so'].wgpuCommandEncoderBeginRenderPass
wgpuCommandEncoderBeginRenderPass.restype = WGPURenderPassEncoder
wgpuCommandEncoderBeginRenderPass.argtypes = [WGPUCommandEncoder, ctypes.POINTER(struct_WGPURenderPassDescriptor)]
wgpuCommandEncoderClearBuffer = _libraries['libwebgpu_dawn.so'].wgpuCommandEncoderClearBuffer
wgpuCommandEncoderClearBuffer.restype = None
wgpuCommandEncoderClearBuffer.argtypes = [WGPUCommandEncoder, WGPUBuffer, uint64_t, uint64_t]
wgpuCommandEncoderCopyBufferToBuffer = _libraries['libwebgpu_dawn.so'].wgpuCommandEncoderCopyBufferToBuffer
wgpuCommandEncoderCopyBufferToBuffer.restype = None
wgpuCommandEncoderCopyBufferToBuffer.argtypes = [WGPUCommandEncoder, WGPUBuffer, uint64_t, WGPUBuffer, uint64_t, uint64_t]
wgpuCommandEncoderCopyBufferToTexture = _libraries['libwebgpu_dawn.so'].wgpuCommandEncoderCopyBufferToTexture
wgpuCommandEncoderCopyBufferToTexture.restype = None
wgpuCommandEncoderCopyBufferToTexture.argtypes = [WGPUCommandEncoder, ctypes.POINTER(struct_WGPUImageCopyBuffer), ctypes.POINTER(struct_WGPUImageCopyTexture), ctypes.POINTER(struct_WGPUExtent3D)]
wgpuCommandEncoderCopyTextureToBuffer = _libraries['libwebgpu_dawn.so'].wgpuCommandEncoderCopyTextureToBuffer
wgpuCommandEncoderCopyTextureToBuffer.restype = None
wgpuCommandEncoderCopyTextureToBuffer.argtypes = [WGPUCommandEncoder, ctypes.POINTER(struct_WGPUImageCopyTexture), ctypes.POINTER(struct_WGPUImageCopyBuffer), ctypes.POINTER(struct_WGPUExtent3D)]
wgpuCommandEncoderCopyTextureToTexture = _libraries['libwebgpu_dawn.so'].wgpuCommandEncoderCopyTextureToTexture
wgpuCommandEncoderCopyTextureToTexture.restype = None
wgpuCommandEncoderCopyTextureToTexture.argtypes = [WGPUCommandEncoder, ctypes.POINTER(struct_WGPUImageCopyTexture), ctypes.POINTER(struct_WGPUImageCopyTexture), ctypes.POINTER(struct_WGPUExtent3D)]
wgpuCommandEncoderFinish = _libraries['libwebgpu_dawn.so'].wgpuCommandEncoderFinish
wgpuCommandEncoderFinish.restype = WGPUCommandBuffer
wgpuCommandEncoderFinish.argtypes = [WGPUCommandEncoder, ctypes.POINTER(struct_WGPUCommandBufferDescriptor)]
wgpuCommandEncoderInjectValidationError = _libraries['libwebgpu_dawn.so'].wgpuCommandEncoderInjectValidationError
wgpuCommandEncoderInjectValidationError.restype = None
wgpuCommandEncoderInjectValidationError.argtypes = [WGPUCommandEncoder, ctypes.POINTER(ctypes.c_char)]
wgpuCommandEncoderInsertDebugMarker = _libraries['libwebgpu_dawn.so'].wgpuCommandEncoderInsertDebugMarker
wgpuCommandEncoderInsertDebugMarker.restype = None
wgpuCommandEncoderInsertDebugMarker.argtypes = [WGPUCommandEncoder, ctypes.POINTER(ctypes.c_char)]
wgpuCommandEncoderPopDebugGroup = _libraries['libwebgpu_dawn.so'].wgpuCommandEncoderPopDebugGroup
wgpuCommandEncoderPopDebugGroup.restype = None
wgpuCommandEncoderPopDebugGroup.argtypes = [WGPUCommandEncoder]
wgpuCommandEncoderPushDebugGroup = _libraries['libwebgpu_dawn.so'].wgpuCommandEncoderPushDebugGroup
wgpuCommandEncoderPushDebugGroup.restype = None
wgpuCommandEncoderPushDebugGroup.argtypes = [WGPUCommandEncoder, ctypes.POINTER(ctypes.c_char)]
uint32_t = ctypes.c_uint32
wgpuCommandEncoderResolveQuerySet = _libraries['libwebgpu_dawn.so'].wgpuCommandEncoderResolveQuerySet
wgpuCommandEncoderResolveQuerySet.restype = None
wgpuCommandEncoderResolveQuerySet.argtypes = [WGPUCommandEncoder, WGPUQuerySet, uint32_t, uint32_t, WGPUBuffer, uint64_t]
wgpuCommandEncoderSetLabel = _libraries['libwebgpu_dawn.so'].wgpuCommandEncoderSetLabel
wgpuCommandEncoderSetLabel.restype = None
wgpuCommandEncoderSetLabel.argtypes = [WGPUCommandEncoder, ctypes.POINTER(ctypes.c_char)]
wgpuCommandEncoderWriteBuffer = _libraries['libwebgpu_dawn.so'].wgpuCommandEncoderWriteBuffer
wgpuCommandEncoderWriteBuffer.restype = None
wgpuCommandEncoderWriteBuffer.argtypes = [WGPUCommandEncoder, WGPUBuffer, uint64_t, ctypes.POINTER(ctypes.c_ubyte), uint64_t]
wgpuCommandEncoderWriteTimestamp = _libraries['libwebgpu_dawn.so'].wgpuCommandEncoderWriteTimestamp
wgpuCommandEncoderWriteTimestamp.restype = None
wgpuCommandEncoderWriteTimestamp.argtypes = [WGPUCommandEncoder, WGPUQuerySet, uint32_t]
wgpuCommandEncoderAddRef = _libraries['libwebgpu_dawn.so'].wgpuCommandEncoderAddRef
wgpuCommandEncoderAddRef.restype = None
wgpuCommandEncoderAddRef.argtypes = [WGPUCommandEncoder]
wgpuCommandEncoderRelease = _libraries['libwebgpu_dawn.so'].wgpuCommandEncoderRelease
wgpuCommandEncoderRelease.restype = None
wgpuCommandEncoderRelease.argtypes = [WGPUCommandEncoder]
wgpuComputePassEncoderDispatchWorkgroups = _libraries['libwebgpu_dawn.so'].wgpuComputePassEncoderDispatchWorkgroups
wgpuComputePassEncoderDispatchWorkgroups.restype = None
wgpuComputePassEncoderDispatchWorkgroups.argtypes = [WGPUComputePassEncoder, uint32_t, uint32_t, uint32_t]
wgpuComputePassEncoderDispatchWorkgroupsIndirect = _libraries['libwebgpu_dawn.so'].wgpuComputePassEncoderDispatchWorkgroupsIndirect
wgpuComputePassEncoderDispatchWorkgroupsIndirect.restype = None
wgpuComputePassEncoderDispatchWorkgroupsIndirect.argtypes = [WGPUComputePassEncoder, WGPUBuffer, uint64_t]
wgpuComputePassEncoderEnd = _libraries['libwebgpu_dawn.so'].wgpuComputePassEncoderEnd
wgpuComputePassEncoderEnd.restype = None
wgpuComputePassEncoderEnd.argtypes = [WGPUComputePassEncoder]
wgpuComputePassEncoderInsertDebugMarker = _libraries['libwebgpu_dawn.so'].wgpuComputePassEncoderInsertDebugMarker
wgpuComputePassEncoderInsertDebugMarker.restype = None
wgpuComputePassEncoderInsertDebugMarker.argtypes = [WGPUComputePassEncoder, ctypes.POINTER(ctypes.c_char)]
wgpuComputePassEncoderPopDebugGroup = _libraries['libwebgpu_dawn.so'].wgpuComputePassEncoderPopDebugGroup
wgpuComputePassEncoderPopDebugGroup.restype = None
wgpuComputePassEncoderPopDebugGroup.argtypes = [WGPUComputePassEncoder]
wgpuComputePassEncoderPushDebugGroup = _libraries['libwebgpu_dawn.so'].wgpuComputePassEncoderPushDebugGroup
wgpuComputePassEncoderPushDebugGroup.restype = None
wgpuComputePassEncoderPushDebugGroup.argtypes = [WGPUComputePassEncoder, ctypes.POINTER(ctypes.c_char)]
wgpuComputePassEncoderSetBindGroup = _libraries['libwebgpu_dawn.so'].wgpuComputePassEncoderSetBindGroup
wgpuComputePassEncoderSetBindGroup.restype = None
wgpuComputePassEncoderSetBindGroup.argtypes = [WGPUComputePassEncoder, uint32_t, WGPUBindGroup, size_t, ctypes.POINTER(ctypes.c_uint32)]
wgpuComputePassEncoderSetLabel = _libraries['libwebgpu_dawn.so'].wgpuComputePassEncoderSetLabel
wgpuComputePassEncoderSetLabel.restype = None
wgpuComputePassEncoderSetLabel.argtypes = [WGPUComputePassEncoder, ctypes.POINTER(ctypes.c_char)]
wgpuComputePassEncoderSetPipeline = _libraries['libwebgpu_dawn.so'].wgpuComputePassEncoderSetPipeline
wgpuComputePassEncoderSetPipeline.restype = None
wgpuComputePassEncoderSetPipeline.argtypes = [WGPUComputePassEncoder, WGPUComputePipeline]
wgpuComputePassEncoderWriteTimestamp = _libraries['libwebgpu_dawn.so'].wgpuComputePassEncoderWriteTimestamp
wgpuComputePassEncoderWriteTimestamp.restype = None
wgpuComputePassEncoderWriteTimestamp.argtypes = [WGPUComputePassEncoder, WGPUQuerySet, uint32_t]
wgpuComputePassEncoderAddRef = _libraries['libwebgpu_dawn.so'].wgpuComputePassEncoderAddRef
wgpuComputePassEncoderAddRef.restype = None
wgpuComputePassEncoderAddRef.argtypes = [WGPUComputePassEncoder]
wgpuComputePassEncoderRelease = _libraries['libwebgpu_dawn.so'].wgpuComputePassEncoderRelease
wgpuComputePassEncoderRelease.restype = None
wgpuComputePassEncoderRelease.argtypes = [WGPUComputePassEncoder]
wgpuComputePipelineGetBindGroupLayout = _libraries['libwebgpu_dawn.so'].wgpuComputePipelineGetBindGroupLayout
wgpuComputePipelineGetBindGroupLayout.restype = WGPUBindGroupLayout
wgpuComputePipelineGetBindGroupLayout.argtypes = [WGPUComputePipeline, uint32_t]
wgpuComputePipelineSetLabel = _libraries['libwebgpu_dawn.so'].wgpuComputePipelineSetLabel
wgpuComputePipelineSetLabel.restype = None
wgpuComputePipelineSetLabel.argtypes = [WGPUComputePipeline, ctypes.POINTER(ctypes.c_char)]
wgpuComputePipelineAddRef = _libraries['libwebgpu_dawn.so'].wgpuComputePipelineAddRef
wgpuComputePipelineAddRef.restype = None
wgpuComputePipelineAddRef.argtypes = [WGPUComputePipeline]
wgpuComputePipelineRelease = _libraries['libwebgpu_dawn.so'].wgpuComputePipelineRelease
wgpuComputePipelineRelease.restype = None
wgpuComputePipelineRelease.argtypes = [WGPUComputePipeline]
wgpuDeviceCreateBindGroup = _libraries['libwebgpu_dawn.so'].wgpuDeviceCreateBindGroup
wgpuDeviceCreateBindGroup.restype = WGPUBindGroup
wgpuDeviceCreateBindGroup.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUBindGroupDescriptor)]
wgpuDeviceCreateBindGroupLayout = _libraries['libwebgpu_dawn.so'].wgpuDeviceCreateBindGroupLayout
wgpuDeviceCreateBindGroupLayout.restype = WGPUBindGroupLayout
wgpuDeviceCreateBindGroupLayout.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUBindGroupLayoutDescriptor)]
wgpuDeviceCreateBuffer = _libraries['libwebgpu_dawn.so'].wgpuDeviceCreateBuffer
wgpuDeviceCreateBuffer.restype = WGPUBuffer
wgpuDeviceCreateBuffer.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUBufferDescriptor)]
wgpuDeviceCreateCommandEncoder = _libraries['libwebgpu_dawn.so'].wgpuDeviceCreateCommandEncoder
wgpuDeviceCreateCommandEncoder.restype = WGPUCommandEncoder
wgpuDeviceCreateCommandEncoder.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUCommandEncoderDescriptor)]
wgpuDeviceCreateComputePipeline = _libraries['libwebgpu_dawn.so'].wgpuDeviceCreateComputePipeline
wgpuDeviceCreateComputePipeline.restype = WGPUComputePipeline
wgpuDeviceCreateComputePipeline.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUComputePipelineDescriptor)]
wgpuDeviceCreateComputePipelineAsync = _libraries['libwebgpu_dawn.so'].wgpuDeviceCreateComputePipelineAsync
wgpuDeviceCreateComputePipelineAsync.restype = None
wgpuDeviceCreateComputePipelineAsync.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUComputePipelineDescriptor), WGPUCreateComputePipelineAsyncCallback, ctypes.POINTER(None)]
wgpuDeviceCreateComputePipelineAsync2 = _libraries['libwebgpu_dawn.so'].wgpuDeviceCreateComputePipelineAsync2
wgpuDeviceCreateComputePipelineAsync2.restype = WGPUFuture
wgpuDeviceCreateComputePipelineAsync2.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUComputePipelineDescriptor), WGPUCreateComputePipelineAsyncCallbackInfo2]
wgpuDeviceCreateComputePipelineAsyncF = _libraries['libwebgpu_dawn.so'].wgpuDeviceCreateComputePipelineAsyncF
wgpuDeviceCreateComputePipelineAsyncF.restype = WGPUFuture
wgpuDeviceCreateComputePipelineAsyncF.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUComputePipelineDescriptor), WGPUCreateComputePipelineAsyncCallbackInfo]
wgpuDeviceCreateErrorBuffer = _libraries['libwebgpu_dawn.so'].wgpuDeviceCreateErrorBuffer
wgpuDeviceCreateErrorBuffer.restype = WGPUBuffer
wgpuDeviceCreateErrorBuffer.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUBufferDescriptor)]
wgpuDeviceCreateErrorExternalTexture = _libraries['libwebgpu_dawn.so'].wgpuDeviceCreateErrorExternalTexture
wgpuDeviceCreateErrorExternalTexture.restype = WGPUExternalTexture
wgpuDeviceCreateErrorExternalTexture.argtypes = [WGPUDevice]
wgpuDeviceCreateErrorShaderModule = _libraries['libwebgpu_dawn.so'].wgpuDeviceCreateErrorShaderModule
wgpuDeviceCreateErrorShaderModule.restype = WGPUShaderModule
wgpuDeviceCreateErrorShaderModule.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUShaderModuleDescriptor), ctypes.POINTER(ctypes.c_char)]
wgpuDeviceCreateErrorTexture = _libraries['libwebgpu_dawn.so'].wgpuDeviceCreateErrorTexture
wgpuDeviceCreateErrorTexture.restype = WGPUTexture
wgpuDeviceCreateErrorTexture.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUTextureDescriptor)]
wgpuDeviceCreateExternalTexture = _libraries['libwebgpu_dawn.so'].wgpuDeviceCreateExternalTexture
wgpuDeviceCreateExternalTexture.restype = WGPUExternalTexture
wgpuDeviceCreateExternalTexture.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUExternalTextureDescriptor)]
wgpuDeviceCreatePipelineLayout = _libraries['libwebgpu_dawn.so'].wgpuDeviceCreatePipelineLayout
wgpuDeviceCreatePipelineLayout.restype = WGPUPipelineLayout
wgpuDeviceCreatePipelineLayout.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUPipelineLayoutDescriptor)]
wgpuDeviceCreateQuerySet = _libraries['libwebgpu_dawn.so'].wgpuDeviceCreateQuerySet
wgpuDeviceCreateQuerySet.restype = WGPUQuerySet
wgpuDeviceCreateQuerySet.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUQuerySetDescriptor)]
wgpuDeviceCreateRenderBundleEncoder = _libraries['libwebgpu_dawn.so'].wgpuDeviceCreateRenderBundleEncoder
wgpuDeviceCreateRenderBundleEncoder.restype = WGPURenderBundleEncoder
wgpuDeviceCreateRenderBundleEncoder.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPURenderBundleEncoderDescriptor)]
wgpuDeviceCreateRenderPipeline = _libraries['libwebgpu_dawn.so'].wgpuDeviceCreateRenderPipeline
wgpuDeviceCreateRenderPipeline.restype = WGPURenderPipeline
wgpuDeviceCreateRenderPipeline.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPURenderPipelineDescriptor)]
wgpuDeviceCreateRenderPipelineAsync = _libraries['libwebgpu_dawn.so'].wgpuDeviceCreateRenderPipelineAsync
wgpuDeviceCreateRenderPipelineAsync.restype = None
wgpuDeviceCreateRenderPipelineAsync.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPURenderPipelineDescriptor), WGPUCreateRenderPipelineAsyncCallback, ctypes.POINTER(None)]
wgpuDeviceCreateRenderPipelineAsync2 = _libraries['libwebgpu_dawn.so'].wgpuDeviceCreateRenderPipelineAsync2
wgpuDeviceCreateRenderPipelineAsync2.restype = WGPUFuture
wgpuDeviceCreateRenderPipelineAsync2.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPURenderPipelineDescriptor), WGPUCreateRenderPipelineAsyncCallbackInfo2]
wgpuDeviceCreateRenderPipelineAsyncF = _libraries['libwebgpu_dawn.so'].wgpuDeviceCreateRenderPipelineAsyncF
wgpuDeviceCreateRenderPipelineAsyncF.restype = WGPUFuture
wgpuDeviceCreateRenderPipelineAsyncF.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPURenderPipelineDescriptor), WGPUCreateRenderPipelineAsyncCallbackInfo]
wgpuDeviceCreateSampler = _libraries['libwebgpu_dawn.so'].wgpuDeviceCreateSampler
wgpuDeviceCreateSampler.restype = WGPUSampler
wgpuDeviceCreateSampler.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUSamplerDescriptor)]
wgpuDeviceCreateShaderModule = _libraries['libwebgpu_dawn.so'].wgpuDeviceCreateShaderModule
wgpuDeviceCreateShaderModule.restype = WGPUShaderModule
wgpuDeviceCreateShaderModule.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUShaderModuleDescriptor)]
wgpuDeviceCreateSwapChain = _libraries['FIXME_STUB'].wgpuDeviceCreateSwapChain
wgpuDeviceCreateSwapChain.restype = WGPUSwapChain
wgpuDeviceCreateSwapChain.argtypes = [WGPUDevice, WGPUSurface, ctypes.POINTER(struct_WGPUSwapChainDescriptor)]
wgpuDeviceCreateTexture = _libraries['libwebgpu_dawn.so'].wgpuDeviceCreateTexture
wgpuDeviceCreateTexture.restype = WGPUTexture
wgpuDeviceCreateTexture.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUTextureDescriptor)]
wgpuDeviceDestroy = _libraries['libwebgpu_dawn.so'].wgpuDeviceDestroy
wgpuDeviceDestroy.restype = None
wgpuDeviceDestroy.argtypes = [WGPUDevice]
wgpuDeviceEnumerateFeatures = _libraries['FIXME_STUB'].wgpuDeviceEnumerateFeatures
wgpuDeviceEnumerateFeatures.restype = size_t
wgpuDeviceEnumerateFeatures.argtypes = [WGPUDevice, ctypes.POINTER(WGPUFeatureName)]
wgpuDeviceForceLoss = _libraries['libwebgpu_dawn.so'].wgpuDeviceForceLoss
wgpuDeviceForceLoss.restype = None
wgpuDeviceForceLoss.argtypes = [WGPUDevice, WGPUDeviceLostReason, ctypes.POINTER(ctypes.c_char)]
wgpuDeviceGetAHardwareBufferProperties = _libraries['libwebgpu_dawn.so'].wgpuDeviceGetAHardwareBufferProperties
wgpuDeviceGetAHardwareBufferProperties.restype = WGPUStatus
wgpuDeviceGetAHardwareBufferProperties.argtypes = [WGPUDevice, ctypes.POINTER(None), ctypes.POINTER(struct_WGPUAHardwareBufferProperties)]
wgpuDeviceGetAdapter = _libraries['libwebgpu_dawn.so'].wgpuDeviceGetAdapter
wgpuDeviceGetAdapter.restype = WGPUAdapter
wgpuDeviceGetAdapter.argtypes = [WGPUDevice]
wgpuDeviceGetLimits = _libraries['libwebgpu_dawn.so'].wgpuDeviceGetLimits
wgpuDeviceGetLimits.restype = WGPUStatus
wgpuDeviceGetLimits.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUSupportedLimits)]
wgpuDeviceGetQueue = _libraries['libwebgpu_dawn.so'].wgpuDeviceGetQueue
wgpuDeviceGetQueue.restype = WGPUQueue
wgpuDeviceGetQueue.argtypes = [WGPUDevice]
wgpuDeviceGetSupportedSurfaceUsage = _libraries['FIXME_STUB'].wgpuDeviceGetSupportedSurfaceUsage
wgpuDeviceGetSupportedSurfaceUsage.restype = WGPUTextureUsageFlags
wgpuDeviceGetSupportedSurfaceUsage.argtypes = [WGPUDevice, WGPUSurface]
wgpuDeviceHasFeature = _libraries['libwebgpu_dawn.so'].wgpuDeviceHasFeature
wgpuDeviceHasFeature.restype = WGPUBool
wgpuDeviceHasFeature.argtypes = [WGPUDevice, WGPUFeatureName]
wgpuDeviceImportSharedBufferMemory = _libraries['libwebgpu_dawn.so'].wgpuDeviceImportSharedBufferMemory
wgpuDeviceImportSharedBufferMemory.restype = WGPUSharedBufferMemory
wgpuDeviceImportSharedBufferMemory.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUSharedBufferMemoryDescriptor)]
wgpuDeviceImportSharedFence = _libraries['libwebgpu_dawn.so'].wgpuDeviceImportSharedFence
wgpuDeviceImportSharedFence.restype = WGPUSharedFence
wgpuDeviceImportSharedFence.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUSharedFenceDescriptor)]
wgpuDeviceImportSharedTextureMemory = _libraries['libwebgpu_dawn.so'].wgpuDeviceImportSharedTextureMemory
wgpuDeviceImportSharedTextureMemory.restype = WGPUSharedTextureMemory
wgpuDeviceImportSharedTextureMemory.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUSharedTextureMemoryDescriptor)]
wgpuDeviceInjectError = _libraries['libwebgpu_dawn.so'].wgpuDeviceInjectError
wgpuDeviceInjectError.restype = None
wgpuDeviceInjectError.argtypes = [WGPUDevice, WGPUErrorType, ctypes.POINTER(ctypes.c_char)]
wgpuDevicePopErrorScope = _libraries['libwebgpu_dawn.so'].wgpuDevicePopErrorScope
wgpuDevicePopErrorScope.restype = None
wgpuDevicePopErrorScope.argtypes = [WGPUDevice, WGPUErrorCallback, ctypes.POINTER(None)]
wgpuDevicePopErrorScope2 = _libraries['libwebgpu_dawn.so'].wgpuDevicePopErrorScope2
wgpuDevicePopErrorScope2.restype = WGPUFuture
wgpuDevicePopErrorScope2.argtypes = [WGPUDevice, WGPUPopErrorScopeCallbackInfo2]
wgpuDevicePopErrorScopeF = _libraries['libwebgpu_dawn.so'].wgpuDevicePopErrorScopeF
wgpuDevicePopErrorScopeF.restype = WGPUFuture
wgpuDevicePopErrorScopeF.argtypes = [WGPUDevice, WGPUPopErrorScopeCallbackInfo]
wgpuDevicePushErrorScope = _libraries['libwebgpu_dawn.so'].wgpuDevicePushErrorScope
wgpuDevicePushErrorScope.restype = None
wgpuDevicePushErrorScope.argtypes = [WGPUDevice, WGPUErrorFilter]
wgpuDeviceSetDeviceLostCallback = _libraries['FIXME_STUB'].wgpuDeviceSetDeviceLostCallback
wgpuDeviceSetDeviceLostCallback.restype = None
wgpuDeviceSetDeviceLostCallback.argtypes = [WGPUDevice, WGPUDeviceLostCallback, ctypes.POINTER(None)]
wgpuDeviceSetLabel = _libraries['libwebgpu_dawn.so'].wgpuDeviceSetLabel
wgpuDeviceSetLabel.restype = None
wgpuDeviceSetLabel.argtypes = [WGPUDevice, ctypes.POINTER(ctypes.c_char)]
wgpuDeviceSetLoggingCallback = _libraries['libwebgpu_dawn.so'].wgpuDeviceSetLoggingCallback
wgpuDeviceSetLoggingCallback.restype = None
wgpuDeviceSetLoggingCallback.argtypes = [WGPUDevice, WGPULoggingCallback, ctypes.POINTER(None)]
wgpuDeviceSetUncapturedErrorCallback = _libraries['FIXME_STUB'].wgpuDeviceSetUncapturedErrorCallback
wgpuDeviceSetUncapturedErrorCallback.restype = None
wgpuDeviceSetUncapturedErrorCallback.argtypes = [WGPUDevice, WGPUErrorCallback, ctypes.POINTER(None)]
wgpuDeviceTick = _libraries['libwebgpu_dawn.so'].wgpuDeviceTick
wgpuDeviceTick.restype = None
wgpuDeviceTick.argtypes = [WGPUDevice]
wgpuDeviceValidateTextureDescriptor = _libraries['libwebgpu_dawn.so'].wgpuDeviceValidateTextureDescriptor
wgpuDeviceValidateTextureDescriptor.restype = None
wgpuDeviceValidateTextureDescriptor.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUTextureDescriptor)]
wgpuDeviceAddRef = _libraries['libwebgpu_dawn.so'].wgpuDeviceAddRef
wgpuDeviceAddRef.restype = None
wgpuDeviceAddRef.argtypes = [WGPUDevice]
wgpuDeviceRelease = _libraries['libwebgpu_dawn.so'].wgpuDeviceRelease
wgpuDeviceRelease.restype = None
wgpuDeviceRelease.argtypes = [WGPUDevice]
wgpuExternalTextureDestroy = _libraries['libwebgpu_dawn.so'].wgpuExternalTextureDestroy
wgpuExternalTextureDestroy.restype = None
wgpuExternalTextureDestroy.argtypes = [WGPUExternalTexture]
wgpuExternalTextureExpire = _libraries['libwebgpu_dawn.so'].wgpuExternalTextureExpire
wgpuExternalTextureExpire.restype = None
wgpuExternalTextureExpire.argtypes = [WGPUExternalTexture]
wgpuExternalTextureRefresh = _libraries['libwebgpu_dawn.so'].wgpuExternalTextureRefresh
wgpuExternalTextureRefresh.restype = None
wgpuExternalTextureRefresh.argtypes = [WGPUExternalTexture]
wgpuExternalTextureSetLabel = _libraries['libwebgpu_dawn.so'].wgpuExternalTextureSetLabel
wgpuExternalTextureSetLabel.restype = None
wgpuExternalTextureSetLabel.argtypes = [WGPUExternalTexture, ctypes.POINTER(ctypes.c_char)]
wgpuExternalTextureAddRef = _libraries['libwebgpu_dawn.so'].wgpuExternalTextureAddRef
wgpuExternalTextureAddRef.restype = None
wgpuExternalTextureAddRef.argtypes = [WGPUExternalTexture]
wgpuExternalTextureRelease = _libraries['libwebgpu_dawn.so'].wgpuExternalTextureRelease
wgpuExternalTextureRelease.restype = None
wgpuExternalTextureRelease.argtypes = [WGPUExternalTexture]
wgpuInstanceCreateSurface = _libraries['libwebgpu_dawn.so'].wgpuInstanceCreateSurface
wgpuInstanceCreateSurface.restype = WGPUSurface
wgpuInstanceCreateSurface.argtypes = [WGPUInstance, ctypes.POINTER(struct_WGPUSurfaceDescriptor)]
wgpuInstanceEnumerateWGSLLanguageFeatures = _libraries['libwebgpu_dawn.so'].wgpuInstanceEnumerateWGSLLanguageFeatures
wgpuInstanceEnumerateWGSLLanguageFeatures.restype = size_t
wgpuInstanceEnumerateWGSLLanguageFeatures.argtypes = [WGPUInstance, ctypes.POINTER(WGPUWGSLFeatureName)]
wgpuInstanceHasWGSLLanguageFeature = _libraries['libwebgpu_dawn.so'].wgpuInstanceHasWGSLLanguageFeature
wgpuInstanceHasWGSLLanguageFeature.restype = WGPUBool
wgpuInstanceHasWGSLLanguageFeature.argtypes = [WGPUInstance, WGPUWGSLFeatureName]
wgpuInstanceProcessEvents = _libraries['libwebgpu_dawn.so'].wgpuInstanceProcessEvents
wgpuInstanceProcessEvents.restype = None
wgpuInstanceProcessEvents.argtypes = [WGPUInstance]
wgpuInstanceRequestAdapter = _libraries['libwebgpu_dawn.so'].wgpuInstanceRequestAdapter
wgpuInstanceRequestAdapter.restype = None
wgpuInstanceRequestAdapter.argtypes = [WGPUInstance, ctypes.POINTER(struct_WGPURequestAdapterOptions), WGPURequestAdapterCallback, ctypes.POINTER(None)]
wgpuInstanceRequestAdapter2 = _libraries['libwebgpu_dawn.so'].wgpuInstanceRequestAdapter2
wgpuInstanceRequestAdapter2.restype = WGPUFuture
wgpuInstanceRequestAdapter2.argtypes = [WGPUInstance, ctypes.POINTER(struct_WGPURequestAdapterOptions), WGPURequestAdapterCallbackInfo2]
wgpuInstanceRequestAdapterF = _libraries['libwebgpu_dawn.so'].wgpuInstanceRequestAdapterF
wgpuInstanceRequestAdapterF.restype = WGPUFuture
wgpuInstanceRequestAdapterF.argtypes = [WGPUInstance, ctypes.POINTER(struct_WGPURequestAdapterOptions), WGPURequestAdapterCallbackInfo]
wgpuInstanceWaitAny = _libraries['libwebgpu_dawn.so'].wgpuInstanceWaitAny
wgpuInstanceWaitAny.restype = WGPUWaitStatus
wgpuInstanceWaitAny.argtypes = [WGPUInstance, size_t, ctypes.POINTER(struct_WGPUFutureWaitInfo), uint64_t]
wgpuInstanceAddRef = _libraries['libwebgpu_dawn.so'].wgpuInstanceAddRef
wgpuInstanceAddRef.restype = None
wgpuInstanceAddRef.argtypes = [WGPUInstance]
wgpuInstanceRelease = _libraries['libwebgpu_dawn.so'].wgpuInstanceRelease
wgpuInstanceRelease.restype = None
wgpuInstanceRelease.argtypes = [WGPUInstance]
wgpuPipelineLayoutSetLabel = _libraries['libwebgpu_dawn.so'].wgpuPipelineLayoutSetLabel
wgpuPipelineLayoutSetLabel.restype = None
wgpuPipelineLayoutSetLabel.argtypes = [WGPUPipelineLayout, ctypes.POINTER(ctypes.c_char)]
wgpuPipelineLayoutAddRef = _libraries['libwebgpu_dawn.so'].wgpuPipelineLayoutAddRef
wgpuPipelineLayoutAddRef.restype = None
wgpuPipelineLayoutAddRef.argtypes = [WGPUPipelineLayout]
wgpuPipelineLayoutRelease = _libraries['libwebgpu_dawn.so'].wgpuPipelineLayoutRelease
wgpuPipelineLayoutRelease.restype = None
wgpuPipelineLayoutRelease.argtypes = [WGPUPipelineLayout]
wgpuQuerySetDestroy = _libraries['libwebgpu_dawn.so'].wgpuQuerySetDestroy
wgpuQuerySetDestroy.restype = None
wgpuQuerySetDestroy.argtypes = [WGPUQuerySet]
wgpuQuerySetGetCount = _libraries['libwebgpu_dawn.so'].wgpuQuerySetGetCount
wgpuQuerySetGetCount.restype = uint32_t
wgpuQuerySetGetCount.argtypes = [WGPUQuerySet]
wgpuQuerySetGetType = _libraries['libwebgpu_dawn.so'].wgpuQuerySetGetType
wgpuQuerySetGetType.restype = WGPUQueryType
wgpuQuerySetGetType.argtypes = [WGPUQuerySet]
wgpuQuerySetSetLabel = _libraries['libwebgpu_dawn.so'].wgpuQuerySetSetLabel
wgpuQuerySetSetLabel.restype = None
wgpuQuerySetSetLabel.argtypes = [WGPUQuerySet, ctypes.POINTER(ctypes.c_char)]
wgpuQuerySetAddRef = _libraries['libwebgpu_dawn.so'].wgpuQuerySetAddRef
wgpuQuerySetAddRef.restype = None
wgpuQuerySetAddRef.argtypes = [WGPUQuerySet]
wgpuQuerySetRelease = _libraries['libwebgpu_dawn.so'].wgpuQuerySetRelease
wgpuQuerySetRelease.restype = None
wgpuQuerySetRelease.argtypes = [WGPUQuerySet]
wgpuQueueCopyExternalTextureForBrowser = _libraries['libwebgpu_dawn.so'].wgpuQueueCopyExternalTextureForBrowser
wgpuQueueCopyExternalTextureForBrowser.restype = None
wgpuQueueCopyExternalTextureForBrowser.argtypes = [WGPUQueue, ctypes.POINTER(struct_WGPUImageCopyExternalTexture), ctypes.POINTER(struct_WGPUImageCopyTexture), ctypes.POINTER(struct_WGPUExtent3D), ctypes.POINTER(struct_WGPUCopyTextureForBrowserOptions)]
wgpuQueueCopyTextureForBrowser = _libraries['libwebgpu_dawn.so'].wgpuQueueCopyTextureForBrowser
wgpuQueueCopyTextureForBrowser.restype = None
wgpuQueueCopyTextureForBrowser.argtypes = [WGPUQueue, ctypes.POINTER(struct_WGPUImageCopyTexture), ctypes.POINTER(struct_WGPUImageCopyTexture), ctypes.POINTER(struct_WGPUExtent3D), ctypes.POINTER(struct_WGPUCopyTextureForBrowserOptions)]
wgpuQueueOnSubmittedWorkDone = _libraries['libwebgpu_dawn.so'].wgpuQueueOnSubmittedWorkDone
wgpuQueueOnSubmittedWorkDone.restype = None
wgpuQueueOnSubmittedWorkDone.argtypes = [WGPUQueue, WGPUQueueWorkDoneCallback, ctypes.POINTER(None)]
wgpuQueueOnSubmittedWorkDone2 = _libraries['libwebgpu_dawn.so'].wgpuQueueOnSubmittedWorkDone2
wgpuQueueOnSubmittedWorkDone2.restype = WGPUFuture
wgpuQueueOnSubmittedWorkDone2.argtypes = [WGPUQueue, WGPUQueueWorkDoneCallbackInfo2]
wgpuQueueOnSubmittedWorkDoneF = _libraries['libwebgpu_dawn.so'].wgpuQueueOnSubmittedWorkDoneF
wgpuQueueOnSubmittedWorkDoneF.restype = WGPUFuture
wgpuQueueOnSubmittedWorkDoneF.argtypes = [WGPUQueue, WGPUQueueWorkDoneCallbackInfo]
wgpuQueueSetLabel = _libraries['libwebgpu_dawn.so'].wgpuQueueSetLabel
wgpuQueueSetLabel.restype = None
wgpuQueueSetLabel.argtypes = [WGPUQueue, ctypes.POINTER(ctypes.c_char)]
wgpuQueueSubmit = _libraries['libwebgpu_dawn.so'].wgpuQueueSubmit
wgpuQueueSubmit.restype = None
wgpuQueueSubmit.argtypes = [WGPUQueue, size_t, ctypes.POINTER(ctypes.POINTER(struct_WGPUCommandBufferImpl))]
wgpuQueueWriteBuffer = _libraries['libwebgpu_dawn.so'].wgpuQueueWriteBuffer
wgpuQueueWriteBuffer.restype = None
wgpuQueueWriteBuffer.argtypes = [WGPUQueue, WGPUBuffer, uint64_t, ctypes.POINTER(None), size_t]
wgpuQueueWriteTexture = _libraries['libwebgpu_dawn.so'].wgpuQueueWriteTexture
wgpuQueueWriteTexture.restype = None
wgpuQueueWriteTexture.argtypes = [WGPUQueue, ctypes.POINTER(struct_WGPUImageCopyTexture), ctypes.POINTER(None), size_t, ctypes.POINTER(struct_WGPUTextureDataLayout), ctypes.POINTER(struct_WGPUExtent3D)]
wgpuQueueAddRef = _libraries['libwebgpu_dawn.so'].wgpuQueueAddRef
wgpuQueueAddRef.restype = None
wgpuQueueAddRef.argtypes = [WGPUQueue]
wgpuQueueRelease = _libraries['libwebgpu_dawn.so'].wgpuQueueRelease
wgpuQueueRelease.restype = None
wgpuQueueRelease.argtypes = [WGPUQueue]
wgpuRenderBundleSetLabel = _libraries['libwebgpu_dawn.so'].wgpuRenderBundleSetLabel
wgpuRenderBundleSetLabel.restype = None
wgpuRenderBundleSetLabel.argtypes = [WGPURenderBundle, ctypes.POINTER(ctypes.c_char)]
wgpuRenderBundleAddRef = _libraries['libwebgpu_dawn.so'].wgpuRenderBundleAddRef
wgpuRenderBundleAddRef.restype = None
wgpuRenderBundleAddRef.argtypes = [WGPURenderBundle]
wgpuRenderBundleRelease = _libraries['libwebgpu_dawn.so'].wgpuRenderBundleRelease
wgpuRenderBundleRelease.restype = None
wgpuRenderBundleRelease.argtypes = [WGPURenderBundle]
wgpuRenderBundleEncoderDraw = _libraries['libwebgpu_dawn.so'].wgpuRenderBundleEncoderDraw
wgpuRenderBundleEncoderDraw.restype = None
wgpuRenderBundleEncoderDraw.argtypes = [WGPURenderBundleEncoder, uint32_t, uint32_t, uint32_t, uint32_t]
int32_t = ctypes.c_int32
wgpuRenderBundleEncoderDrawIndexed = _libraries['libwebgpu_dawn.so'].wgpuRenderBundleEncoderDrawIndexed
wgpuRenderBundleEncoderDrawIndexed.restype = None
wgpuRenderBundleEncoderDrawIndexed.argtypes = [WGPURenderBundleEncoder, uint32_t, uint32_t, uint32_t, int32_t, uint32_t]
wgpuRenderBundleEncoderDrawIndexedIndirect = _libraries['libwebgpu_dawn.so'].wgpuRenderBundleEncoderDrawIndexedIndirect
wgpuRenderBundleEncoderDrawIndexedIndirect.restype = None
wgpuRenderBundleEncoderDrawIndexedIndirect.argtypes = [WGPURenderBundleEncoder, WGPUBuffer, uint64_t]
wgpuRenderBundleEncoderDrawIndirect = _libraries['libwebgpu_dawn.so'].wgpuRenderBundleEncoderDrawIndirect
wgpuRenderBundleEncoderDrawIndirect.restype = None
wgpuRenderBundleEncoderDrawIndirect.argtypes = [WGPURenderBundleEncoder, WGPUBuffer, uint64_t]
wgpuRenderBundleEncoderFinish = _libraries['libwebgpu_dawn.so'].wgpuRenderBundleEncoderFinish
wgpuRenderBundleEncoderFinish.restype = WGPURenderBundle
wgpuRenderBundleEncoderFinish.argtypes = [WGPURenderBundleEncoder, ctypes.POINTER(struct_WGPURenderBundleDescriptor)]
wgpuRenderBundleEncoderInsertDebugMarker = _libraries['libwebgpu_dawn.so'].wgpuRenderBundleEncoderInsertDebugMarker
wgpuRenderBundleEncoderInsertDebugMarker.restype = None
wgpuRenderBundleEncoderInsertDebugMarker.argtypes = [WGPURenderBundleEncoder, ctypes.POINTER(ctypes.c_char)]
wgpuRenderBundleEncoderPopDebugGroup = _libraries['libwebgpu_dawn.so'].wgpuRenderBundleEncoderPopDebugGroup
wgpuRenderBundleEncoderPopDebugGroup.restype = None
wgpuRenderBundleEncoderPopDebugGroup.argtypes = [WGPURenderBundleEncoder]
wgpuRenderBundleEncoderPushDebugGroup = _libraries['libwebgpu_dawn.so'].wgpuRenderBundleEncoderPushDebugGroup
wgpuRenderBundleEncoderPushDebugGroup.restype = None
wgpuRenderBundleEncoderPushDebugGroup.argtypes = [WGPURenderBundleEncoder, ctypes.POINTER(ctypes.c_char)]
wgpuRenderBundleEncoderSetBindGroup = _libraries['libwebgpu_dawn.so'].wgpuRenderBundleEncoderSetBindGroup
wgpuRenderBundleEncoderSetBindGroup.restype = None
wgpuRenderBundleEncoderSetBindGroup.argtypes = [WGPURenderBundleEncoder, uint32_t, WGPUBindGroup, size_t, ctypes.POINTER(ctypes.c_uint32)]
wgpuRenderBundleEncoderSetIndexBuffer = _libraries['libwebgpu_dawn.so'].wgpuRenderBundleEncoderSetIndexBuffer
wgpuRenderBundleEncoderSetIndexBuffer.restype = None
wgpuRenderBundleEncoderSetIndexBuffer.argtypes = [WGPURenderBundleEncoder, WGPUBuffer, WGPUIndexFormat, uint64_t, uint64_t]
wgpuRenderBundleEncoderSetLabel = _libraries['libwebgpu_dawn.so'].wgpuRenderBundleEncoderSetLabel
wgpuRenderBundleEncoderSetLabel.restype = None
wgpuRenderBundleEncoderSetLabel.argtypes = [WGPURenderBundleEncoder, ctypes.POINTER(ctypes.c_char)]
wgpuRenderBundleEncoderSetPipeline = _libraries['libwebgpu_dawn.so'].wgpuRenderBundleEncoderSetPipeline
wgpuRenderBundleEncoderSetPipeline.restype = None
wgpuRenderBundleEncoderSetPipeline.argtypes = [WGPURenderBundleEncoder, WGPURenderPipeline]
wgpuRenderBundleEncoderSetVertexBuffer = _libraries['libwebgpu_dawn.so'].wgpuRenderBundleEncoderSetVertexBuffer
wgpuRenderBundleEncoderSetVertexBuffer.restype = None
wgpuRenderBundleEncoderSetVertexBuffer.argtypes = [WGPURenderBundleEncoder, uint32_t, WGPUBuffer, uint64_t, uint64_t]
wgpuRenderBundleEncoderAddRef = _libraries['libwebgpu_dawn.so'].wgpuRenderBundleEncoderAddRef
wgpuRenderBundleEncoderAddRef.restype = None
wgpuRenderBundleEncoderAddRef.argtypes = [WGPURenderBundleEncoder]
wgpuRenderBundleEncoderRelease = _libraries['libwebgpu_dawn.so'].wgpuRenderBundleEncoderRelease
wgpuRenderBundleEncoderRelease.restype = None
wgpuRenderBundleEncoderRelease.argtypes = [WGPURenderBundleEncoder]
wgpuRenderPassEncoderBeginOcclusionQuery = _libraries['libwebgpu_dawn.so'].wgpuRenderPassEncoderBeginOcclusionQuery
wgpuRenderPassEncoderBeginOcclusionQuery.restype = None
wgpuRenderPassEncoderBeginOcclusionQuery.argtypes = [WGPURenderPassEncoder, uint32_t]
wgpuRenderPassEncoderDraw = _libraries['libwebgpu_dawn.so'].wgpuRenderPassEncoderDraw
wgpuRenderPassEncoderDraw.restype = None
wgpuRenderPassEncoderDraw.argtypes = [WGPURenderPassEncoder, uint32_t, uint32_t, uint32_t, uint32_t]
wgpuRenderPassEncoderDrawIndexed = _libraries['libwebgpu_dawn.so'].wgpuRenderPassEncoderDrawIndexed
wgpuRenderPassEncoderDrawIndexed.restype = None
wgpuRenderPassEncoderDrawIndexed.argtypes = [WGPURenderPassEncoder, uint32_t, uint32_t, uint32_t, int32_t, uint32_t]
wgpuRenderPassEncoderDrawIndexedIndirect = _libraries['libwebgpu_dawn.so'].wgpuRenderPassEncoderDrawIndexedIndirect
wgpuRenderPassEncoderDrawIndexedIndirect.restype = None
wgpuRenderPassEncoderDrawIndexedIndirect.argtypes = [WGPURenderPassEncoder, WGPUBuffer, uint64_t]
wgpuRenderPassEncoderDrawIndirect = _libraries['libwebgpu_dawn.so'].wgpuRenderPassEncoderDrawIndirect
wgpuRenderPassEncoderDrawIndirect.restype = None
wgpuRenderPassEncoderDrawIndirect.argtypes = [WGPURenderPassEncoder, WGPUBuffer, uint64_t]
wgpuRenderPassEncoderEnd = _libraries['libwebgpu_dawn.so'].wgpuRenderPassEncoderEnd
wgpuRenderPassEncoderEnd.restype = None
wgpuRenderPassEncoderEnd.argtypes = [WGPURenderPassEncoder]
wgpuRenderPassEncoderEndOcclusionQuery = _libraries['libwebgpu_dawn.so'].wgpuRenderPassEncoderEndOcclusionQuery
wgpuRenderPassEncoderEndOcclusionQuery.restype = None
wgpuRenderPassEncoderEndOcclusionQuery.argtypes = [WGPURenderPassEncoder]
wgpuRenderPassEncoderExecuteBundles = _libraries['libwebgpu_dawn.so'].wgpuRenderPassEncoderExecuteBundles
wgpuRenderPassEncoderExecuteBundles.restype = None
wgpuRenderPassEncoderExecuteBundles.argtypes = [WGPURenderPassEncoder, size_t, ctypes.POINTER(ctypes.POINTER(struct_WGPURenderBundleImpl))]
wgpuRenderPassEncoderInsertDebugMarker = _libraries['libwebgpu_dawn.so'].wgpuRenderPassEncoderInsertDebugMarker
wgpuRenderPassEncoderInsertDebugMarker.restype = None
wgpuRenderPassEncoderInsertDebugMarker.argtypes = [WGPURenderPassEncoder, ctypes.POINTER(ctypes.c_char)]
wgpuRenderPassEncoderPixelLocalStorageBarrier = _libraries['libwebgpu_dawn.so'].wgpuRenderPassEncoderPixelLocalStorageBarrier
wgpuRenderPassEncoderPixelLocalStorageBarrier.restype = None
wgpuRenderPassEncoderPixelLocalStorageBarrier.argtypes = [WGPURenderPassEncoder]
wgpuRenderPassEncoderPopDebugGroup = _libraries['libwebgpu_dawn.so'].wgpuRenderPassEncoderPopDebugGroup
wgpuRenderPassEncoderPopDebugGroup.restype = None
wgpuRenderPassEncoderPopDebugGroup.argtypes = [WGPURenderPassEncoder]
wgpuRenderPassEncoderPushDebugGroup = _libraries['libwebgpu_dawn.so'].wgpuRenderPassEncoderPushDebugGroup
wgpuRenderPassEncoderPushDebugGroup.restype = None
wgpuRenderPassEncoderPushDebugGroup.argtypes = [WGPURenderPassEncoder, ctypes.POINTER(ctypes.c_char)]
wgpuRenderPassEncoderSetBindGroup = _libraries['libwebgpu_dawn.so'].wgpuRenderPassEncoderSetBindGroup
wgpuRenderPassEncoderSetBindGroup.restype = None
wgpuRenderPassEncoderSetBindGroup.argtypes = [WGPURenderPassEncoder, uint32_t, WGPUBindGroup, size_t, ctypes.POINTER(ctypes.c_uint32)]
wgpuRenderPassEncoderSetBlendConstant = _libraries['libwebgpu_dawn.so'].wgpuRenderPassEncoderSetBlendConstant
wgpuRenderPassEncoderSetBlendConstant.restype = None
wgpuRenderPassEncoderSetBlendConstant.argtypes = [WGPURenderPassEncoder, ctypes.POINTER(struct_WGPUColor)]
wgpuRenderPassEncoderSetIndexBuffer = _libraries['libwebgpu_dawn.so'].wgpuRenderPassEncoderSetIndexBuffer
wgpuRenderPassEncoderSetIndexBuffer.restype = None
wgpuRenderPassEncoderSetIndexBuffer.argtypes = [WGPURenderPassEncoder, WGPUBuffer, WGPUIndexFormat, uint64_t, uint64_t]
wgpuRenderPassEncoderSetLabel = _libraries['libwebgpu_dawn.so'].wgpuRenderPassEncoderSetLabel
wgpuRenderPassEncoderSetLabel.restype = None
wgpuRenderPassEncoderSetLabel.argtypes = [WGPURenderPassEncoder, ctypes.POINTER(ctypes.c_char)]
wgpuRenderPassEncoderSetPipeline = _libraries['libwebgpu_dawn.so'].wgpuRenderPassEncoderSetPipeline
wgpuRenderPassEncoderSetPipeline.restype = None
wgpuRenderPassEncoderSetPipeline.argtypes = [WGPURenderPassEncoder, WGPURenderPipeline]
wgpuRenderPassEncoderSetScissorRect = _libraries['libwebgpu_dawn.so'].wgpuRenderPassEncoderSetScissorRect
wgpuRenderPassEncoderSetScissorRect.restype = None
wgpuRenderPassEncoderSetScissorRect.argtypes = [WGPURenderPassEncoder, uint32_t, uint32_t, uint32_t, uint32_t]
wgpuRenderPassEncoderSetStencilReference = _libraries['libwebgpu_dawn.so'].wgpuRenderPassEncoderSetStencilReference
wgpuRenderPassEncoderSetStencilReference.restype = None
wgpuRenderPassEncoderSetStencilReference.argtypes = [WGPURenderPassEncoder, uint32_t]
wgpuRenderPassEncoderSetVertexBuffer = _libraries['libwebgpu_dawn.so'].wgpuRenderPassEncoderSetVertexBuffer
wgpuRenderPassEncoderSetVertexBuffer.restype = None
wgpuRenderPassEncoderSetVertexBuffer.argtypes = [WGPURenderPassEncoder, uint32_t, WGPUBuffer, uint64_t, uint64_t]
wgpuRenderPassEncoderSetViewport = _libraries['libwebgpu_dawn.so'].wgpuRenderPassEncoderSetViewport
wgpuRenderPassEncoderSetViewport.restype = None
wgpuRenderPassEncoderSetViewport.argtypes = [WGPURenderPassEncoder, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float]
wgpuRenderPassEncoderWriteTimestamp = _libraries['libwebgpu_dawn.so'].wgpuRenderPassEncoderWriteTimestamp
wgpuRenderPassEncoderWriteTimestamp.restype = None
wgpuRenderPassEncoderWriteTimestamp.argtypes = [WGPURenderPassEncoder, WGPUQuerySet, uint32_t]
wgpuRenderPassEncoderAddRef = _libraries['libwebgpu_dawn.so'].wgpuRenderPassEncoderAddRef
wgpuRenderPassEncoderAddRef.restype = None
wgpuRenderPassEncoderAddRef.argtypes = [WGPURenderPassEncoder]
wgpuRenderPassEncoderRelease = _libraries['libwebgpu_dawn.so'].wgpuRenderPassEncoderRelease
wgpuRenderPassEncoderRelease.restype = None
wgpuRenderPassEncoderRelease.argtypes = [WGPURenderPassEncoder]
wgpuRenderPipelineGetBindGroupLayout = _libraries['libwebgpu_dawn.so'].wgpuRenderPipelineGetBindGroupLayout
wgpuRenderPipelineGetBindGroupLayout.restype = WGPUBindGroupLayout
wgpuRenderPipelineGetBindGroupLayout.argtypes = [WGPURenderPipeline, uint32_t]
wgpuRenderPipelineSetLabel = _libraries['libwebgpu_dawn.so'].wgpuRenderPipelineSetLabel
wgpuRenderPipelineSetLabel.restype = None
wgpuRenderPipelineSetLabel.argtypes = [WGPURenderPipeline, ctypes.POINTER(ctypes.c_char)]
wgpuRenderPipelineAddRef = _libraries['libwebgpu_dawn.so'].wgpuRenderPipelineAddRef
wgpuRenderPipelineAddRef.restype = None
wgpuRenderPipelineAddRef.argtypes = [WGPURenderPipeline]
wgpuRenderPipelineRelease = _libraries['libwebgpu_dawn.so'].wgpuRenderPipelineRelease
wgpuRenderPipelineRelease.restype = None
wgpuRenderPipelineRelease.argtypes = [WGPURenderPipeline]
wgpuSamplerSetLabel = _libraries['libwebgpu_dawn.so'].wgpuSamplerSetLabel
wgpuSamplerSetLabel.restype = None
wgpuSamplerSetLabel.argtypes = [WGPUSampler, ctypes.POINTER(ctypes.c_char)]
wgpuSamplerAddRef = _libraries['libwebgpu_dawn.so'].wgpuSamplerAddRef
wgpuSamplerAddRef.restype = None
wgpuSamplerAddRef.argtypes = [WGPUSampler]
wgpuSamplerRelease = _libraries['libwebgpu_dawn.so'].wgpuSamplerRelease
wgpuSamplerRelease.restype = None
wgpuSamplerRelease.argtypes = [WGPUSampler]
wgpuShaderModuleGetCompilationInfo = _libraries['libwebgpu_dawn.so'].wgpuShaderModuleGetCompilationInfo
wgpuShaderModuleGetCompilationInfo.restype = None
wgpuShaderModuleGetCompilationInfo.argtypes = [WGPUShaderModule, WGPUCompilationInfoCallback, ctypes.POINTER(None)]
wgpuShaderModuleGetCompilationInfo2 = _libraries['libwebgpu_dawn.so'].wgpuShaderModuleGetCompilationInfo2
wgpuShaderModuleGetCompilationInfo2.restype = WGPUFuture
wgpuShaderModuleGetCompilationInfo2.argtypes = [WGPUShaderModule, WGPUCompilationInfoCallbackInfo2]
wgpuShaderModuleGetCompilationInfoF = _libraries['libwebgpu_dawn.so'].wgpuShaderModuleGetCompilationInfoF
wgpuShaderModuleGetCompilationInfoF.restype = WGPUFuture
wgpuShaderModuleGetCompilationInfoF.argtypes = [WGPUShaderModule, WGPUCompilationInfoCallbackInfo]
wgpuShaderModuleSetLabel = _libraries['libwebgpu_dawn.so'].wgpuShaderModuleSetLabel
wgpuShaderModuleSetLabel.restype = None
wgpuShaderModuleSetLabel.argtypes = [WGPUShaderModule, ctypes.POINTER(ctypes.c_char)]
wgpuShaderModuleAddRef = _libraries['libwebgpu_dawn.so'].wgpuShaderModuleAddRef
wgpuShaderModuleAddRef.restype = None
wgpuShaderModuleAddRef.argtypes = [WGPUShaderModule]
wgpuShaderModuleRelease = _libraries['libwebgpu_dawn.so'].wgpuShaderModuleRelease
wgpuShaderModuleRelease.restype = None
wgpuShaderModuleRelease.argtypes = [WGPUShaderModule]
wgpuSharedBufferMemoryBeginAccess = _libraries['libwebgpu_dawn.so'].wgpuSharedBufferMemoryBeginAccess
wgpuSharedBufferMemoryBeginAccess.restype = WGPUBool
wgpuSharedBufferMemoryBeginAccess.argtypes = [WGPUSharedBufferMemory, WGPUBuffer, ctypes.POINTER(struct_WGPUSharedBufferMemoryBeginAccessDescriptor)]
wgpuSharedBufferMemoryCreateBuffer = _libraries['libwebgpu_dawn.so'].wgpuSharedBufferMemoryCreateBuffer
wgpuSharedBufferMemoryCreateBuffer.restype = WGPUBuffer
wgpuSharedBufferMemoryCreateBuffer.argtypes = [WGPUSharedBufferMemory, ctypes.POINTER(struct_WGPUBufferDescriptor)]
wgpuSharedBufferMemoryEndAccess = _libraries['libwebgpu_dawn.so'].wgpuSharedBufferMemoryEndAccess
wgpuSharedBufferMemoryEndAccess.restype = WGPUBool
wgpuSharedBufferMemoryEndAccess.argtypes = [WGPUSharedBufferMemory, WGPUBuffer, ctypes.POINTER(struct_WGPUSharedBufferMemoryEndAccessState)]
wgpuSharedBufferMemoryGetProperties = _libraries['libwebgpu_dawn.so'].wgpuSharedBufferMemoryGetProperties
wgpuSharedBufferMemoryGetProperties.restype = WGPUStatus
wgpuSharedBufferMemoryGetProperties.argtypes = [WGPUSharedBufferMemory, ctypes.POINTER(struct_WGPUSharedBufferMemoryProperties)]
wgpuSharedBufferMemoryIsDeviceLost = _libraries['libwebgpu_dawn.so'].wgpuSharedBufferMemoryIsDeviceLost
wgpuSharedBufferMemoryIsDeviceLost.restype = WGPUBool
wgpuSharedBufferMemoryIsDeviceLost.argtypes = [WGPUSharedBufferMemory]
wgpuSharedBufferMemorySetLabel = _libraries['libwebgpu_dawn.so'].wgpuSharedBufferMemorySetLabel
wgpuSharedBufferMemorySetLabel.restype = None
wgpuSharedBufferMemorySetLabel.argtypes = [WGPUSharedBufferMemory, ctypes.POINTER(ctypes.c_char)]
wgpuSharedBufferMemoryAddRef = _libraries['libwebgpu_dawn.so'].wgpuSharedBufferMemoryAddRef
wgpuSharedBufferMemoryAddRef.restype = None
wgpuSharedBufferMemoryAddRef.argtypes = [WGPUSharedBufferMemory]
wgpuSharedBufferMemoryRelease = _libraries['libwebgpu_dawn.so'].wgpuSharedBufferMemoryRelease
wgpuSharedBufferMemoryRelease.restype = None
wgpuSharedBufferMemoryRelease.argtypes = [WGPUSharedBufferMemory]
wgpuSharedFenceExportInfo = _libraries['libwebgpu_dawn.so'].wgpuSharedFenceExportInfo
wgpuSharedFenceExportInfo.restype = None
wgpuSharedFenceExportInfo.argtypes = [WGPUSharedFence, ctypes.POINTER(struct_WGPUSharedFenceExportInfo)]
wgpuSharedFenceAddRef = _libraries['libwebgpu_dawn.so'].wgpuSharedFenceAddRef
wgpuSharedFenceAddRef.restype = None
wgpuSharedFenceAddRef.argtypes = [WGPUSharedFence]
wgpuSharedFenceRelease = _libraries['libwebgpu_dawn.so'].wgpuSharedFenceRelease
wgpuSharedFenceRelease.restype = None
wgpuSharedFenceRelease.argtypes = [WGPUSharedFence]
wgpuSharedTextureMemoryBeginAccess = _libraries['libwebgpu_dawn.so'].wgpuSharedTextureMemoryBeginAccess
wgpuSharedTextureMemoryBeginAccess.restype = WGPUBool
wgpuSharedTextureMemoryBeginAccess.argtypes = [WGPUSharedTextureMemory, WGPUTexture, ctypes.POINTER(struct_WGPUSharedTextureMemoryBeginAccessDescriptor)]
wgpuSharedTextureMemoryCreateTexture = _libraries['libwebgpu_dawn.so'].wgpuSharedTextureMemoryCreateTexture
wgpuSharedTextureMemoryCreateTexture.restype = WGPUTexture
wgpuSharedTextureMemoryCreateTexture.argtypes = [WGPUSharedTextureMemory, ctypes.POINTER(struct_WGPUTextureDescriptor)]
wgpuSharedTextureMemoryEndAccess = _libraries['libwebgpu_dawn.so'].wgpuSharedTextureMemoryEndAccess
wgpuSharedTextureMemoryEndAccess.restype = WGPUBool
wgpuSharedTextureMemoryEndAccess.argtypes = [WGPUSharedTextureMemory, WGPUTexture, ctypes.POINTER(struct_WGPUSharedTextureMemoryEndAccessState)]
wgpuSharedTextureMemoryGetProperties = _libraries['libwebgpu_dawn.so'].wgpuSharedTextureMemoryGetProperties
wgpuSharedTextureMemoryGetProperties.restype = WGPUStatus
wgpuSharedTextureMemoryGetProperties.argtypes = [WGPUSharedTextureMemory, ctypes.POINTER(struct_WGPUSharedTextureMemoryProperties)]
wgpuSharedTextureMemoryIsDeviceLost = _libraries['libwebgpu_dawn.so'].wgpuSharedTextureMemoryIsDeviceLost
wgpuSharedTextureMemoryIsDeviceLost.restype = WGPUBool
wgpuSharedTextureMemoryIsDeviceLost.argtypes = [WGPUSharedTextureMemory]
wgpuSharedTextureMemorySetLabel = _libraries['libwebgpu_dawn.so'].wgpuSharedTextureMemorySetLabel
wgpuSharedTextureMemorySetLabel.restype = None
wgpuSharedTextureMemorySetLabel.argtypes = [WGPUSharedTextureMemory, ctypes.POINTER(ctypes.c_char)]
wgpuSharedTextureMemoryAddRef = _libraries['libwebgpu_dawn.so'].wgpuSharedTextureMemoryAddRef
wgpuSharedTextureMemoryAddRef.restype = None
wgpuSharedTextureMemoryAddRef.argtypes = [WGPUSharedTextureMemory]
wgpuSharedTextureMemoryRelease = _libraries['libwebgpu_dawn.so'].wgpuSharedTextureMemoryRelease
wgpuSharedTextureMemoryRelease.restype = None
wgpuSharedTextureMemoryRelease.argtypes = [WGPUSharedTextureMemory]
wgpuSurfaceConfigure = _libraries['libwebgpu_dawn.so'].wgpuSurfaceConfigure
wgpuSurfaceConfigure.restype = None
wgpuSurfaceConfigure.argtypes = [WGPUSurface, ctypes.POINTER(struct_WGPUSurfaceConfiguration)]
wgpuSurfaceGetCapabilities = _libraries['libwebgpu_dawn.so'].wgpuSurfaceGetCapabilities
wgpuSurfaceGetCapabilities.restype = WGPUStatus
wgpuSurfaceGetCapabilities.argtypes = [WGPUSurface, WGPUAdapter, ctypes.POINTER(struct_WGPUSurfaceCapabilities)]
wgpuSurfaceGetCurrentTexture = _libraries['libwebgpu_dawn.so'].wgpuSurfaceGetCurrentTexture
wgpuSurfaceGetCurrentTexture.restype = None
wgpuSurfaceGetCurrentTexture.argtypes = [WGPUSurface, ctypes.POINTER(struct_WGPUSurfaceTexture)]
wgpuSurfaceGetPreferredFormat = _libraries['FIXME_STUB'].wgpuSurfaceGetPreferredFormat
wgpuSurfaceGetPreferredFormat.restype = WGPUTextureFormat
wgpuSurfaceGetPreferredFormat.argtypes = [WGPUSurface, WGPUAdapter]
wgpuSurfacePresent = _libraries['libwebgpu_dawn.so'].wgpuSurfacePresent
wgpuSurfacePresent.restype = None
wgpuSurfacePresent.argtypes = [WGPUSurface]
wgpuSurfaceUnconfigure = _libraries['libwebgpu_dawn.so'].wgpuSurfaceUnconfigure
wgpuSurfaceUnconfigure.restype = None
wgpuSurfaceUnconfigure.argtypes = [WGPUSurface]
wgpuSurfaceAddRef = _libraries['libwebgpu_dawn.so'].wgpuSurfaceAddRef
wgpuSurfaceAddRef.restype = None
wgpuSurfaceAddRef.argtypes = [WGPUSurface]
wgpuSurfaceRelease = _libraries['libwebgpu_dawn.so'].wgpuSurfaceRelease
wgpuSurfaceRelease.restype = None
wgpuSurfaceRelease.argtypes = [WGPUSurface]
wgpuSwapChainGetCurrentTexture = _libraries['FIXME_STUB'].wgpuSwapChainGetCurrentTexture
wgpuSwapChainGetCurrentTexture.restype = WGPUTexture
wgpuSwapChainGetCurrentTexture.argtypes = [WGPUSwapChain]
wgpuSwapChainGetCurrentTextureView = _libraries['FIXME_STUB'].wgpuSwapChainGetCurrentTextureView
wgpuSwapChainGetCurrentTextureView.restype = WGPUTextureView
wgpuSwapChainGetCurrentTextureView.argtypes = [WGPUSwapChain]
wgpuSwapChainPresent = _libraries['FIXME_STUB'].wgpuSwapChainPresent
wgpuSwapChainPresent.restype = None
wgpuSwapChainPresent.argtypes = [WGPUSwapChain]
wgpuSwapChainAddRef = _libraries['FIXME_STUB'].wgpuSwapChainAddRef
wgpuSwapChainAddRef.restype = None
wgpuSwapChainAddRef.argtypes = [WGPUSwapChain]
wgpuSwapChainRelease = _libraries['FIXME_STUB'].wgpuSwapChainRelease
wgpuSwapChainRelease.restype = None
wgpuSwapChainRelease.argtypes = [WGPUSwapChain]
wgpuTextureCreateErrorView = _libraries['libwebgpu_dawn.so'].wgpuTextureCreateErrorView
wgpuTextureCreateErrorView.restype = WGPUTextureView
wgpuTextureCreateErrorView.argtypes = [WGPUTexture, ctypes.POINTER(struct_WGPUTextureViewDescriptor)]
wgpuTextureCreateView = _libraries['libwebgpu_dawn.so'].wgpuTextureCreateView
wgpuTextureCreateView.restype = WGPUTextureView
wgpuTextureCreateView.argtypes = [WGPUTexture, ctypes.POINTER(struct_WGPUTextureViewDescriptor)]
wgpuTextureDestroy = _libraries['libwebgpu_dawn.so'].wgpuTextureDestroy
wgpuTextureDestroy.restype = None
wgpuTextureDestroy.argtypes = [WGPUTexture]
wgpuTextureGetDepthOrArrayLayers = _libraries['libwebgpu_dawn.so'].wgpuTextureGetDepthOrArrayLayers
wgpuTextureGetDepthOrArrayLayers.restype = uint32_t
wgpuTextureGetDepthOrArrayLayers.argtypes = [WGPUTexture]
wgpuTextureGetDimension = _libraries['libwebgpu_dawn.so'].wgpuTextureGetDimension
wgpuTextureGetDimension.restype = WGPUTextureDimension
wgpuTextureGetDimension.argtypes = [WGPUTexture]
wgpuTextureGetFormat = _libraries['libwebgpu_dawn.so'].wgpuTextureGetFormat
wgpuTextureGetFormat.restype = WGPUTextureFormat
wgpuTextureGetFormat.argtypes = [WGPUTexture]
wgpuTextureGetHeight = _libraries['libwebgpu_dawn.so'].wgpuTextureGetHeight
wgpuTextureGetHeight.restype = uint32_t
wgpuTextureGetHeight.argtypes = [WGPUTexture]
wgpuTextureGetMipLevelCount = _libraries['libwebgpu_dawn.so'].wgpuTextureGetMipLevelCount
wgpuTextureGetMipLevelCount.restype = uint32_t
wgpuTextureGetMipLevelCount.argtypes = [WGPUTexture]
wgpuTextureGetSampleCount = _libraries['libwebgpu_dawn.so'].wgpuTextureGetSampleCount
wgpuTextureGetSampleCount.restype = uint32_t
wgpuTextureGetSampleCount.argtypes = [WGPUTexture]
wgpuTextureGetUsage = _libraries['libwebgpu_dawn.so'].wgpuTextureGetUsage
wgpuTextureGetUsage.restype = WGPUTextureUsageFlags
wgpuTextureGetUsage.argtypes = [WGPUTexture]
wgpuTextureGetWidth = _libraries['libwebgpu_dawn.so'].wgpuTextureGetWidth
wgpuTextureGetWidth.restype = uint32_t
wgpuTextureGetWidth.argtypes = [WGPUTexture]
wgpuTextureSetLabel = _libraries['libwebgpu_dawn.so'].wgpuTextureSetLabel
wgpuTextureSetLabel.restype = None
wgpuTextureSetLabel.argtypes = [WGPUTexture, ctypes.POINTER(ctypes.c_char)]
wgpuTextureAddRef = _libraries['libwebgpu_dawn.so'].wgpuTextureAddRef
wgpuTextureAddRef.restype = None
wgpuTextureAddRef.argtypes = [WGPUTexture]
wgpuTextureRelease = _libraries['libwebgpu_dawn.so'].wgpuTextureRelease
wgpuTextureRelease.restype = None
wgpuTextureRelease.argtypes = [WGPUTexture]
wgpuTextureViewSetLabel = _libraries['libwebgpu_dawn.so'].wgpuTextureViewSetLabel
wgpuTextureViewSetLabel.restype = None
wgpuTextureViewSetLabel.argtypes = [WGPUTextureView, ctypes.POINTER(ctypes.c_char)]
wgpuTextureViewAddRef = _libraries['libwebgpu_dawn.so'].wgpuTextureViewAddRef
wgpuTextureViewAddRef.restype = None
wgpuTextureViewAddRef.argtypes = [WGPUTextureView]
wgpuTextureViewRelease = _libraries['libwebgpu_dawn.so'].wgpuTextureViewRelease
wgpuTextureViewRelease.restype = None
wgpuTextureViewRelease.argtypes = [WGPUTextureView]
__all__ = \
    ['WGPUAHardwareBufferProperties', 'WGPUAdapter',
    'WGPUAdapterInfo', 'WGPUAdapterProperties',
    'WGPUAdapterPropertiesD3D', 'WGPUAdapterPropertiesMemoryHeaps',
    'WGPUAdapterPropertiesVk', 'WGPUAdapterType',
    'WGPUAdapterType_CPU', 'WGPUAdapterType_DiscreteGPU',
    'WGPUAdapterType_Force32', 'WGPUAdapterType_IntegratedGPU',
    'WGPUAdapterType_Unknown', 'WGPUAddressMode',
    'WGPUAddressMode_ClampToEdge', 'WGPUAddressMode_Force32',
    'WGPUAddressMode_MirrorRepeat', 'WGPUAddressMode_Repeat',
    'WGPUAddressMode_Undefined', 'WGPUAlphaMode',
    'WGPUAlphaMode_Force32', 'WGPUAlphaMode_Opaque',
    'WGPUAlphaMode_Premultiplied', 'WGPUAlphaMode_Unpremultiplied',
    'WGPUBackendType', 'WGPUBackendType_D3D11',
    'WGPUBackendType_D3D12', 'WGPUBackendType_Force32',
    'WGPUBackendType_Metal', 'WGPUBackendType_Null',
    'WGPUBackendType_OpenGL', 'WGPUBackendType_OpenGLES',
    'WGPUBackendType_Undefined', 'WGPUBackendType_Vulkan',
    'WGPUBackendType_WebGPU', 'WGPUBindGroup',
    'WGPUBindGroupDescriptor', 'WGPUBindGroupEntry',
    'WGPUBindGroupLayout', 'WGPUBindGroupLayoutDescriptor',
    'WGPUBindGroupLayoutEntry', 'WGPUBlendComponent',
    'WGPUBlendFactor', 'WGPUBlendFactor_Constant',
    'WGPUBlendFactor_Dst', 'WGPUBlendFactor_DstAlpha',
    'WGPUBlendFactor_Force32', 'WGPUBlendFactor_One',
    'WGPUBlendFactor_OneMinusConstant', 'WGPUBlendFactor_OneMinusDst',
    'WGPUBlendFactor_OneMinusDstAlpha', 'WGPUBlendFactor_OneMinusSrc',
    'WGPUBlendFactor_OneMinusSrc1',
    'WGPUBlendFactor_OneMinusSrc1Alpha',
    'WGPUBlendFactor_OneMinusSrcAlpha', 'WGPUBlendFactor_Src',
    'WGPUBlendFactor_Src1', 'WGPUBlendFactor_Src1Alpha',
    'WGPUBlendFactor_SrcAlpha', 'WGPUBlendFactor_SrcAlphaSaturated',
    'WGPUBlendFactor_Undefined', 'WGPUBlendFactor_Zero',
    'WGPUBlendOperation', 'WGPUBlendOperation_Add',
    'WGPUBlendOperation_Force32', 'WGPUBlendOperation_Max',
    'WGPUBlendOperation_Min', 'WGPUBlendOperation_ReverseSubtract',
    'WGPUBlendOperation_Subtract', 'WGPUBlendOperation_Undefined',
    'WGPUBlendState', 'WGPUBool', 'WGPUBuffer',
    'WGPUBufferBindingLayout', 'WGPUBufferBindingType',
    'WGPUBufferBindingType_Force32',
    'WGPUBufferBindingType_ReadOnlyStorage',
    'WGPUBufferBindingType_Storage',
    'WGPUBufferBindingType_Undefined',
    'WGPUBufferBindingType_Uniform', 'WGPUBufferDescriptor',
    'WGPUBufferHostMappedPointer', 'WGPUBufferMapAsyncStatus',
    'WGPUBufferMapAsyncStatus_DestroyedBeforeCallback',
    'WGPUBufferMapAsyncStatus_DeviceLost',
    'WGPUBufferMapAsyncStatus_Force32',
    'WGPUBufferMapAsyncStatus_InstanceDropped',
    'WGPUBufferMapAsyncStatus_MappingAlreadyPending',
    'WGPUBufferMapAsyncStatus_OffsetOutOfRange',
    'WGPUBufferMapAsyncStatus_SizeOutOfRange',
    'WGPUBufferMapAsyncStatus_Success',
    'WGPUBufferMapAsyncStatus_Unknown',
    'WGPUBufferMapAsyncStatus_UnmappedBeforeCallback',
    'WGPUBufferMapAsyncStatus_ValidationError',
    'WGPUBufferMapCallback', 'WGPUBufferMapCallback2',
    'WGPUBufferMapCallbackInfo', 'WGPUBufferMapCallbackInfo2',
    'WGPUBufferMapState', 'WGPUBufferMapState_Force32',
    'WGPUBufferMapState_Mapped', 'WGPUBufferMapState_Pending',
    'WGPUBufferMapState_Unmapped', 'WGPUBufferUsage',
    'WGPUBufferUsageFlags', 'WGPUBufferUsage_CopyDst',
    'WGPUBufferUsage_CopySrc', 'WGPUBufferUsage_Force32',
    'WGPUBufferUsage_Index', 'WGPUBufferUsage_Indirect',
    'WGPUBufferUsage_MapRead', 'WGPUBufferUsage_MapWrite',
    'WGPUBufferUsage_None', 'WGPUBufferUsage_QueryResolve',
    'WGPUBufferUsage_Storage', 'WGPUBufferUsage_Uniform',
    'WGPUBufferUsage_Vertex', 'WGPUCallback', 'WGPUCallbackMode',
    'WGPUCallbackMode_AllowProcessEvents',
    'WGPUCallbackMode_AllowSpontaneous', 'WGPUCallbackMode_Force32',
    'WGPUCallbackMode_WaitAnyOnly', 'WGPUChainedStruct',
    'WGPUChainedStructOut', 'WGPUColor', 'WGPUColorTargetState',
    'WGPUColorTargetStateExpandResolveTextureDawn',
    'WGPUColorWriteMask', 'WGPUColorWriteMaskFlags',
    'WGPUColorWriteMask_All', 'WGPUColorWriteMask_Alpha',
    'WGPUColorWriteMask_Blue', 'WGPUColorWriteMask_Force32',
    'WGPUColorWriteMask_Green', 'WGPUColorWriteMask_None',
    'WGPUColorWriteMask_Red', 'WGPUCommandBuffer',
    'WGPUCommandBufferDescriptor', 'WGPUCommandEncoder',
    'WGPUCommandEncoderDescriptor', 'WGPUCompareFunction',
    'WGPUCompareFunction_Always', 'WGPUCompareFunction_Equal',
    'WGPUCompareFunction_Force32', 'WGPUCompareFunction_Greater',
    'WGPUCompareFunction_GreaterEqual', 'WGPUCompareFunction_Less',
    'WGPUCompareFunction_LessEqual', 'WGPUCompareFunction_Never',
    'WGPUCompareFunction_NotEqual', 'WGPUCompareFunction_Undefined',
    'WGPUCompilationInfo', 'WGPUCompilationInfoCallback',
    'WGPUCompilationInfoCallback2', 'WGPUCompilationInfoCallbackInfo',
    'WGPUCompilationInfoCallbackInfo2',
    'WGPUCompilationInfoRequestStatus',
    'WGPUCompilationInfoRequestStatus_DeviceLost',
    'WGPUCompilationInfoRequestStatus_Error',
    'WGPUCompilationInfoRequestStatus_Force32',
    'WGPUCompilationInfoRequestStatus_InstanceDropped',
    'WGPUCompilationInfoRequestStatus_Success',
    'WGPUCompilationInfoRequestStatus_Unknown',
    'WGPUCompilationMessage', 'WGPUCompilationMessageType',
    'WGPUCompilationMessageType_Error',
    'WGPUCompilationMessageType_Force32',
    'WGPUCompilationMessageType_Info',
    'WGPUCompilationMessageType_Warning', 'WGPUCompositeAlphaMode',
    'WGPUCompositeAlphaMode_Auto', 'WGPUCompositeAlphaMode_Force32',
    'WGPUCompositeAlphaMode_Inherit', 'WGPUCompositeAlphaMode_Opaque',
    'WGPUCompositeAlphaMode_Premultiplied',
    'WGPUCompositeAlphaMode_Unpremultiplied',
    'WGPUComputePassDescriptor', 'WGPUComputePassEncoder',
    'WGPUComputePassTimestampWrites', 'WGPUComputePipeline',
    'WGPUComputePipelineDescriptor', 'WGPUConstantEntry',
    'WGPUCopyTextureForBrowserOptions',
    'WGPUCreateComputePipelineAsyncCallback',
    'WGPUCreateComputePipelineAsyncCallback2',
    'WGPUCreateComputePipelineAsyncCallbackInfo',
    'WGPUCreateComputePipelineAsyncCallbackInfo2',
    'WGPUCreatePipelineAsyncStatus',
    'WGPUCreatePipelineAsyncStatus_DeviceDestroyed',
    'WGPUCreatePipelineAsyncStatus_DeviceLost',
    'WGPUCreatePipelineAsyncStatus_Force32',
    'WGPUCreatePipelineAsyncStatus_InstanceDropped',
    'WGPUCreatePipelineAsyncStatus_InternalError',
    'WGPUCreatePipelineAsyncStatus_Success',
    'WGPUCreatePipelineAsyncStatus_Unknown',
    'WGPUCreatePipelineAsyncStatus_ValidationError',
    'WGPUCreateRenderPipelineAsyncCallback',
    'WGPUCreateRenderPipelineAsyncCallback2',
    'WGPUCreateRenderPipelineAsyncCallbackInfo',
    'WGPUCreateRenderPipelineAsyncCallbackInfo2', 'WGPUCullMode',
    'WGPUCullMode_Back', 'WGPUCullMode_Force32', 'WGPUCullMode_Front',
    'WGPUCullMode_None', 'WGPUCullMode_Undefined',
    'WGPUDawnAdapterPropertiesPowerPreference',
    'WGPUDawnBufferDescriptorErrorInfoFromWireClient',
    'WGPUDawnCacheDeviceDescriptor',
    'WGPUDawnComputePipelineFullSubgroups',
    'WGPUDawnEncoderInternalUsageDescriptor',
    'WGPUDawnExperimentalSubgroupLimits',
    'WGPUDawnLoadCacheDataFunction',
    'WGPUDawnRenderPassColorAttachmentRenderToSingleSampled',
    'WGPUDawnShaderModuleSPIRVOptionsDescriptor',
    'WGPUDawnStoreCacheDataFunction',
    'WGPUDawnTextureInternalUsageDescriptor',
    'WGPUDawnTogglesDescriptor', 'WGPUDawnWGSLBlocklist',
    'WGPUDawnWireWGSLControl', 'WGPUDepthStencilState',
    'WGPUDepthStencilStateDepthWriteDefinedDawn', 'WGPUDevice',
    'WGPUDeviceDescriptor', 'WGPUDeviceLostCallback',
    'WGPUDeviceLostCallbackInfo', 'WGPUDeviceLostCallbackNew',
    'WGPUDeviceLostReason', 'WGPUDeviceLostReason_Destroyed',
    'WGPUDeviceLostReason_FailedCreation',
    'WGPUDeviceLostReason_Force32',
    'WGPUDeviceLostReason_InstanceDropped',
    'WGPUDeviceLostReason_Unknown', 'WGPUDrmFormatCapabilities',
    'WGPUDrmFormatProperties', 'WGPUErrorCallback', 'WGPUErrorFilter',
    'WGPUErrorFilter_Force32', 'WGPUErrorFilter_Internal',
    'WGPUErrorFilter_OutOfMemory', 'WGPUErrorFilter_Validation',
    'WGPUErrorType', 'WGPUErrorType_DeviceLost',
    'WGPUErrorType_Force32', 'WGPUErrorType_Internal',
    'WGPUErrorType_NoError', 'WGPUErrorType_OutOfMemory',
    'WGPUErrorType_Unknown', 'WGPUErrorType_Validation',
    'WGPUExtent2D', 'WGPUExtent3D', 'WGPUExternalTexture',
    'WGPUExternalTextureBindingEntry',
    'WGPUExternalTextureBindingLayout',
    'WGPUExternalTextureDescriptor', 'WGPUExternalTextureRotation',
    'WGPUExternalTextureRotation_Force32',
    'WGPUExternalTextureRotation_Rotate0Degrees',
    'WGPUExternalTextureRotation_Rotate180Degrees',
    'WGPUExternalTextureRotation_Rotate270Degrees',
    'WGPUExternalTextureRotation_Rotate90Degrees', 'WGPUFeatureName',
    'WGPUFeatureName_ANGLETextureSharing',
    'WGPUFeatureName_AdapterPropertiesD3D',
    'WGPUFeatureName_AdapterPropertiesMemoryHeaps',
    'WGPUFeatureName_AdapterPropertiesVk',
    'WGPUFeatureName_BGRA8UnormStorage',
    'WGPUFeatureName_BufferMapExtendedUsages',
    'WGPUFeatureName_ChromiumExperimentalSubgroupUniformControlFlow',
    'WGPUFeatureName_ChromiumExperimentalSubgroups',
    'WGPUFeatureName_ChromiumExperimentalTimestampQueryInsidePasses',
    'WGPUFeatureName_D3D11MultithreadProtected',
    'WGPUFeatureName_DawnInternalUsages',
    'WGPUFeatureName_DawnLoadResolveTexture',
    'WGPUFeatureName_DawnMultiPlanarFormats',
    'WGPUFeatureName_DawnNative',
    'WGPUFeatureName_Depth32FloatStencil8',
    'WGPUFeatureName_DepthClipControl',
    'WGPUFeatureName_DrmFormatCapabilities',
    'WGPUFeatureName_DualSourceBlending',
    'WGPUFeatureName_Float32Filterable', 'WGPUFeatureName_Force32',
    'WGPUFeatureName_FormatCapabilities',
    'WGPUFeatureName_FramebufferFetch',
    'WGPUFeatureName_HostMappedPointer',
    'WGPUFeatureName_ImplicitDeviceSynchronization',
    'WGPUFeatureName_IndirectFirstInstance',
    'WGPUFeatureName_MSAARenderToSingleSampled',
    'WGPUFeatureName_MultiPlanarFormatExtendedUsages',
    'WGPUFeatureName_MultiPlanarFormatNv12a',
    'WGPUFeatureName_MultiPlanarFormatNv16',
    'WGPUFeatureName_MultiPlanarFormatNv24',
    'WGPUFeatureName_MultiPlanarFormatP010',
    'WGPUFeatureName_MultiPlanarFormatP210',
    'WGPUFeatureName_MultiPlanarFormatP410',
    'WGPUFeatureName_MultiPlanarRenderTargets',
    'WGPUFeatureName_Norm16TextureFormats',
    'WGPUFeatureName_PixelLocalStorageCoherent',
    'WGPUFeatureName_PixelLocalStorageNonCoherent',
    'WGPUFeatureName_R8UnormStorage',
    'WGPUFeatureName_RG11B10UfloatRenderable',
    'WGPUFeatureName_ShaderF16',
    'WGPUFeatureName_ShaderModuleCompilationOptions',
    'WGPUFeatureName_SharedBufferMemoryD3D12Resource',
    'WGPUFeatureName_SharedFenceDXGISharedHandle',
    'WGPUFeatureName_SharedFenceMTLSharedEvent',
    'WGPUFeatureName_SharedFenceVkSemaphoreOpaqueFD',
    'WGPUFeatureName_SharedFenceVkSemaphoreSyncFD',
    'WGPUFeatureName_SharedFenceVkSemaphoreZirconHandle',
    'WGPUFeatureName_SharedTextureMemoryAHardwareBuffer',
    'WGPUFeatureName_SharedTextureMemoryD3D11Texture2D',
    'WGPUFeatureName_SharedTextureMemoryDXGISharedHandle',
    'WGPUFeatureName_SharedTextureMemoryDmaBuf',
    'WGPUFeatureName_SharedTextureMemoryEGLImage',
    'WGPUFeatureName_SharedTextureMemoryIOSurface',
    'WGPUFeatureName_SharedTextureMemoryOpaqueFD',
    'WGPUFeatureName_SharedTextureMemoryVkDedicatedAllocation',
    'WGPUFeatureName_SharedTextureMemoryZirconHandle',
    'WGPUFeatureName_Snorm16TextureFormats',
    'WGPUFeatureName_StaticSamplers',
    'WGPUFeatureName_SurfaceCapabilities',
    'WGPUFeatureName_TextureCompressionASTC',
    'WGPUFeatureName_TextureCompressionBC',
    'WGPUFeatureName_TextureCompressionETC2',
    'WGPUFeatureName_TimestampQuery',
    'WGPUFeatureName_TransientAttachments',
    'WGPUFeatureName_Undefined',
    'WGPUFeatureName_Unorm16TextureFormats',
    'WGPUFeatureName_YCbCrVulkanSamplers', 'WGPUFilterMode',
    'WGPUFilterMode_Force32', 'WGPUFilterMode_Linear',
    'WGPUFilterMode_Nearest', 'WGPUFilterMode_Undefined', 'WGPUFlags',
    'WGPUFormatCapabilities', 'WGPUFragmentState', 'WGPUFrontFace',
    'WGPUFrontFace_CCW', 'WGPUFrontFace_CW', 'WGPUFrontFace_Force32',
    'WGPUFrontFace_Undefined', 'WGPUFuture', 'WGPUFutureWaitInfo',
    'WGPUHeapProperty', 'WGPUHeapPropertyFlags',
    'WGPUHeapProperty_DeviceLocal', 'WGPUHeapProperty_Force32',
    'WGPUHeapProperty_HostCached', 'WGPUHeapProperty_HostCoherent',
    'WGPUHeapProperty_HostUncached', 'WGPUHeapProperty_HostVisible',
    'WGPUHeapProperty_Undefined', 'WGPUImageCopyBuffer',
    'WGPUImageCopyExternalTexture', 'WGPUImageCopyTexture',
    'WGPUIndexFormat', 'WGPUIndexFormat_Force32',
    'WGPUIndexFormat_Uint16', 'WGPUIndexFormat_Uint32',
    'WGPUIndexFormat_Undefined', 'WGPUInstance',
    'WGPUInstanceDescriptor', 'WGPUInstanceFeatures', 'WGPULimits',
    'WGPULoadOp', 'WGPULoadOp_Clear',
    'WGPULoadOp_ExpandResolveTexture', 'WGPULoadOp_Force32',
    'WGPULoadOp_Load', 'WGPULoadOp_Undefined', 'WGPULoggingCallback',
    'WGPULoggingType', 'WGPULoggingType_Error',
    'WGPULoggingType_Force32', 'WGPULoggingType_Info',
    'WGPULoggingType_Verbose', 'WGPULoggingType_Warning',
    'WGPUMapAsyncStatus', 'WGPUMapAsyncStatus_Aborted',
    'WGPUMapAsyncStatus_Error', 'WGPUMapAsyncStatus_Force32',
    'WGPUMapAsyncStatus_InstanceDropped',
    'WGPUMapAsyncStatus_Success', 'WGPUMapAsyncStatus_Unknown',
    'WGPUMapMode', 'WGPUMapModeFlags', 'WGPUMapMode_Force32',
    'WGPUMapMode_None', 'WGPUMapMode_Read', 'WGPUMapMode_Write',
    'WGPUMemoryHeapInfo', 'WGPUMipmapFilterMode',
    'WGPUMipmapFilterMode_Force32', 'WGPUMipmapFilterMode_Linear',
    'WGPUMipmapFilterMode_Nearest', 'WGPUMipmapFilterMode_Undefined',
    'WGPUMultisampleState', 'WGPUOrigin2D', 'WGPUOrigin3D',
    'WGPUPipelineLayout', 'WGPUPipelineLayoutDescriptor',
    'WGPUPipelineLayoutPixelLocalStorage',
    'WGPUPipelineLayoutStorageAttachment',
    'WGPUPopErrorScopeCallback', 'WGPUPopErrorScopeCallback2',
    'WGPUPopErrorScopeCallbackInfo', 'WGPUPopErrorScopeCallbackInfo2',
    'WGPUPopErrorScopeStatus', 'WGPUPopErrorScopeStatus_Force32',
    'WGPUPopErrorScopeStatus_InstanceDropped',
    'WGPUPopErrorScopeStatus_Success', 'WGPUPowerPreference',
    'WGPUPowerPreference_Force32',
    'WGPUPowerPreference_HighPerformance',
    'WGPUPowerPreference_LowPower', 'WGPUPowerPreference_Undefined',
    'WGPUPresentMode', 'WGPUPresentMode_Fifo',
    'WGPUPresentMode_FifoRelaxed', 'WGPUPresentMode_Force32',
    'WGPUPresentMode_Immediate', 'WGPUPresentMode_Mailbox',
    'WGPUPrimitiveDepthClipControl', 'WGPUPrimitiveState',
    'WGPUPrimitiveTopology', 'WGPUPrimitiveTopology_Force32',
    'WGPUPrimitiveTopology_LineList',
    'WGPUPrimitiveTopology_LineStrip',
    'WGPUPrimitiveTopology_PointList',
    'WGPUPrimitiveTopology_TriangleList',
    'WGPUPrimitiveTopology_TriangleStrip',
    'WGPUPrimitiveTopology_Undefined', 'WGPUProc',
    'WGPUProcAdapterAddRef', 'WGPUProcAdapterCreateDevice',
    'WGPUProcAdapterEnumerateFeatures',
    'WGPUProcAdapterGetFormatCapabilities', 'WGPUProcAdapterGetInfo',
    'WGPUProcAdapterGetInstance', 'WGPUProcAdapterGetLimits',
    'WGPUProcAdapterGetProperties', 'WGPUProcAdapterHasFeature',
    'WGPUProcAdapterInfoFreeMembers',
    'WGPUProcAdapterPropertiesFreeMembers',
    'WGPUProcAdapterPropertiesMemoryHeapsFreeMembers',
    'WGPUProcAdapterRelease', 'WGPUProcAdapterRequestDevice',
    'WGPUProcAdapterRequestDevice2', 'WGPUProcAdapterRequestDeviceF',
    'WGPUProcBindGroupAddRef', 'WGPUProcBindGroupLayoutAddRef',
    'WGPUProcBindGroupLayoutRelease',
    'WGPUProcBindGroupLayoutSetLabel', 'WGPUProcBindGroupRelease',
    'WGPUProcBindGroupSetLabel', 'WGPUProcBufferAddRef',
    'WGPUProcBufferDestroy', 'WGPUProcBufferGetConstMappedRange',
    'WGPUProcBufferGetMapState', 'WGPUProcBufferGetMappedRange',
    'WGPUProcBufferGetSize', 'WGPUProcBufferGetUsage',
    'WGPUProcBufferMapAsync', 'WGPUProcBufferMapAsync2',
    'WGPUProcBufferMapAsyncF', 'WGPUProcBufferRelease',
    'WGPUProcBufferSetLabel', 'WGPUProcBufferUnmap',
    'WGPUProcCommandBufferAddRef', 'WGPUProcCommandBufferRelease',
    'WGPUProcCommandBufferSetLabel', 'WGPUProcCommandEncoderAddRef',
    'WGPUProcCommandEncoderBeginComputePass',
    'WGPUProcCommandEncoderBeginRenderPass',
    'WGPUProcCommandEncoderClearBuffer',
    'WGPUProcCommandEncoderCopyBufferToBuffer',
    'WGPUProcCommandEncoderCopyBufferToTexture',
    'WGPUProcCommandEncoderCopyTextureToBuffer',
    'WGPUProcCommandEncoderCopyTextureToTexture',
    'WGPUProcCommandEncoderFinish',
    'WGPUProcCommandEncoderInjectValidationError',
    'WGPUProcCommandEncoderInsertDebugMarker',
    'WGPUProcCommandEncoderPopDebugGroup',
    'WGPUProcCommandEncoderPushDebugGroup',
    'WGPUProcCommandEncoderRelease',
    'WGPUProcCommandEncoderResolveQuerySet',
    'WGPUProcCommandEncoderSetLabel',
    'WGPUProcCommandEncoderWriteBuffer',
    'WGPUProcCommandEncoderWriteTimestamp',
    'WGPUProcComputePassEncoderAddRef',
    'WGPUProcComputePassEncoderDispatchWorkgroups',
    'WGPUProcComputePassEncoderDispatchWorkgroupsIndirect',
    'WGPUProcComputePassEncoderEnd',
    'WGPUProcComputePassEncoderInsertDebugMarker',
    'WGPUProcComputePassEncoderPopDebugGroup',
    'WGPUProcComputePassEncoderPushDebugGroup',
    'WGPUProcComputePassEncoderRelease',
    'WGPUProcComputePassEncoderSetBindGroup',
    'WGPUProcComputePassEncoderSetLabel',
    'WGPUProcComputePassEncoderSetPipeline',
    'WGPUProcComputePassEncoderWriteTimestamp',
    'WGPUProcComputePipelineAddRef',
    'WGPUProcComputePipelineGetBindGroupLayout',
    'WGPUProcComputePipelineRelease',
    'WGPUProcComputePipelineSetLabel', 'WGPUProcCreateInstance',
    'WGPUProcDeviceAddRef', 'WGPUProcDeviceCreateBindGroup',
    'WGPUProcDeviceCreateBindGroupLayout',
    'WGPUProcDeviceCreateBuffer',
    'WGPUProcDeviceCreateCommandEncoder',
    'WGPUProcDeviceCreateComputePipeline',
    'WGPUProcDeviceCreateComputePipelineAsync',
    'WGPUProcDeviceCreateComputePipelineAsync2',
    'WGPUProcDeviceCreateComputePipelineAsyncF',
    'WGPUProcDeviceCreateErrorBuffer',
    'WGPUProcDeviceCreateErrorExternalTexture',
    'WGPUProcDeviceCreateErrorShaderModule',
    'WGPUProcDeviceCreateErrorTexture',
    'WGPUProcDeviceCreateExternalTexture',
    'WGPUProcDeviceCreatePipelineLayout',
    'WGPUProcDeviceCreateQuerySet',
    'WGPUProcDeviceCreateRenderBundleEncoder',
    'WGPUProcDeviceCreateRenderPipeline',
    'WGPUProcDeviceCreateRenderPipelineAsync',
    'WGPUProcDeviceCreateRenderPipelineAsync2',
    'WGPUProcDeviceCreateRenderPipelineAsyncF',
    'WGPUProcDeviceCreateSampler', 'WGPUProcDeviceCreateShaderModule',
    'WGPUProcDeviceCreateSwapChain', 'WGPUProcDeviceCreateTexture',
    'WGPUProcDeviceDestroy', 'WGPUProcDeviceEnumerateFeatures',
    'WGPUProcDeviceForceLoss',
    'WGPUProcDeviceGetAHardwareBufferProperties',
    'WGPUProcDeviceGetAdapter', 'WGPUProcDeviceGetLimits',
    'WGPUProcDeviceGetQueue',
    'WGPUProcDeviceGetSupportedSurfaceUsage',
    'WGPUProcDeviceHasFeature',
    'WGPUProcDeviceImportSharedBufferMemory',
    'WGPUProcDeviceImportSharedFence',
    'WGPUProcDeviceImportSharedTextureMemory',
    'WGPUProcDeviceInjectError', 'WGPUProcDevicePopErrorScope',
    'WGPUProcDevicePopErrorScope2', 'WGPUProcDevicePopErrorScopeF',
    'WGPUProcDevicePushErrorScope', 'WGPUProcDeviceRelease',
    'WGPUProcDeviceSetDeviceLostCallback', 'WGPUProcDeviceSetLabel',
    'WGPUProcDeviceSetLoggingCallback',
    'WGPUProcDeviceSetUncapturedErrorCallback', 'WGPUProcDeviceTick',
    'WGPUProcDeviceValidateTextureDescriptor',
    'WGPUProcDrmFormatCapabilitiesFreeMembers',
    'WGPUProcExternalTextureAddRef', 'WGPUProcExternalTextureDestroy',
    'WGPUProcExternalTextureExpire', 'WGPUProcExternalTextureRefresh',
    'WGPUProcExternalTextureRelease',
    'WGPUProcExternalTextureSetLabel', 'WGPUProcGetInstanceFeatures',
    'WGPUProcGetProcAddress', 'WGPUProcInstanceAddRef',
    'WGPUProcInstanceCreateSurface',
    'WGPUProcInstanceEnumerateWGSLLanguageFeatures',
    'WGPUProcInstanceHasWGSLLanguageFeature',
    'WGPUProcInstanceProcessEvents', 'WGPUProcInstanceRelease',
    'WGPUProcInstanceRequestAdapter',
    'WGPUProcInstanceRequestAdapter2',
    'WGPUProcInstanceRequestAdapterF', 'WGPUProcInstanceWaitAny',
    'WGPUProcPipelineLayoutAddRef', 'WGPUProcPipelineLayoutRelease',
    'WGPUProcPipelineLayoutSetLabel', 'WGPUProcQuerySetAddRef',
    'WGPUProcQuerySetDestroy', 'WGPUProcQuerySetGetCount',
    'WGPUProcQuerySetGetType', 'WGPUProcQuerySetRelease',
    'WGPUProcQuerySetSetLabel', 'WGPUProcQueueAddRef',
    'WGPUProcQueueCopyExternalTextureForBrowser',
    'WGPUProcQueueCopyTextureForBrowser',
    'WGPUProcQueueOnSubmittedWorkDone',
    'WGPUProcQueueOnSubmittedWorkDone2',
    'WGPUProcQueueOnSubmittedWorkDoneF', 'WGPUProcQueueRelease',
    'WGPUProcQueueSetLabel', 'WGPUProcQueueSubmit',
    'WGPUProcQueueWriteBuffer', 'WGPUProcQueueWriteTexture',
    'WGPUProcRenderBundleAddRef', 'WGPUProcRenderBundleEncoderAddRef',
    'WGPUProcRenderBundleEncoderDraw',
    'WGPUProcRenderBundleEncoderDrawIndexed',
    'WGPUProcRenderBundleEncoderDrawIndexedIndirect',
    'WGPUProcRenderBundleEncoderDrawIndirect',
    'WGPUProcRenderBundleEncoderFinish',
    'WGPUProcRenderBundleEncoderInsertDebugMarker',
    'WGPUProcRenderBundleEncoderPopDebugGroup',
    'WGPUProcRenderBundleEncoderPushDebugGroup',
    'WGPUProcRenderBundleEncoderRelease',
    'WGPUProcRenderBundleEncoderSetBindGroup',
    'WGPUProcRenderBundleEncoderSetIndexBuffer',
    'WGPUProcRenderBundleEncoderSetLabel',
    'WGPUProcRenderBundleEncoderSetPipeline',
    'WGPUProcRenderBundleEncoderSetVertexBuffer',
    'WGPUProcRenderBundleRelease', 'WGPUProcRenderBundleSetLabel',
    'WGPUProcRenderPassEncoderAddRef',
    'WGPUProcRenderPassEncoderBeginOcclusionQuery',
    'WGPUProcRenderPassEncoderDraw',
    'WGPUProcRenderPassEncoderDrawIndexed',
    'WGPUProcRenderPassEncoderDrawIndexedIndirect',
    'WGPUProcRenderPassEncoderDrawIndirect',
    'WGPUProcRenderPassEncoderEnd',
    'WGPUProcRenderPassEncoderEndOcclusionQuery',
    'WGPUProcRenderPassEncoderExecuteBundles',
    'WGPUProcRenderPassEncoderInsertDebugMarker',
    'WGPUProcRenderPassEncoderPixelLocalStorageBarrier',
    'WGPUProcRenderPassEncoderPopDebugGroup',
    'WGPUProcRenderPassEncoderPushDebugGroup',
    'WGPUProcRenderPassEncoderRelease',
    'WGPUProcRenderPassEncoderSetBindGroup',
    'WGPUProcRenderPassEncoderSetBlendConstant',
    'WGPUProcRenderPassEncoderSetIndexBuffer',
    'WGPUProcRenderPassEncoderSetLabel',
    'WGPUProcRenderPassEncoderSetPipeline',
    'WGPUProcRenderPassEncoderSetScissorRect',
    'WGPUProcRenderPassEncoderSetStencilReference',
    'WGPUProcRenderPassEncoderSetVertexBuffer',
    'WGPUProcRenderPassEncoderSetViewport',
    'WGPUProcRenderPassEncoderWriteTimestamp',
    'WGPUProcRenderPipelineAddRef',
    'WGPUProcRenderPipelineGetBindGroupLayout',
    'WGPUProcRenderPipelineRelease', 'WGPUProcRenderPipelineSetLabel',
    'WGPUProcSamplerAddRef', 'WGPUProcSamplerRelease',
    'WGPUProcSamplerSetLabel', 'WGPUProcShaderModuleAddRef',
    'WGPUProcShaderModuleGetCompilationInfo',
    'WGPUProcShaderModuleGetCompilationInfo2',
    'WGPUProcShaderModuleGetCompilationInfoF',
    'WGPUProcShaderModuleRelease', 'WGPUProcShaderModuleSetLabel',
    'WGPUProcSharedBufferMemoryAddRef',
    'WGPUProcSharedBufferMemoryBeginAccess',
    'WGPUProcSharedBufferMemoryCreateBuffer',
    'WGPUProcSharedBufferMemoryEndAccess',
    'WGPUProcSharedBufferMemoryEndAccessStateFreeMembers',
    'WGPUProcSharedBufferMemoryGetProperties',
    'WGPUProcSharedBufferMemoryIsDeviceLost',
    'WGPUProcSharedBufferMemoryRelease',
    'WGPUProcSharedBufferMemorySetLabel', 'WGPUProcSharedFenceAddRef',
    'WGPUProcSharedFenceExportInfo', 'WGPUProcSharedFenceRelease',
    'WGPUProcSharedTextureMemoryAddRef',
    'WGPUProcSharedTextureMemoryBeginAccess',
    'WGPUProcSharedTextureMemoryCreateTexture',
    'WGPUProcSharedTextureMemoryEndAccess',
    'WGPUProcSharedTextureMemoryEndAccessStateFreeMembers',
    'WGPUProcSharedTextureMemoryGetProperties',
    'WGPUProcSharedTextureMemoryIsDeviceLost',
    'WGPUProcSharedTextureMemoryRelease',
    'WGPUProcSharedTextureMemorySetLabel', 'WGPUProcSurfaceAddRef',
    'WGPUProcSurfaceCapabilitiesFreeMembers',
    'WGPUProcSurfaceConfigure', 'WGPUProcSurfaceGetCapabilities',
    'WGPUProcSurfaceGetCurrentTexture',
    'WGPUProcSurfaceGetPreferredFormat', 'WGPUProcSurfacePresent',
    'WGPUProcSurfaceRelease', 'WGPUProcSurfaceUnconfigure',
    'WGPUProcSwapChainAddRef', 'WGPUProcSwapChainGetCurrentTexture',
    'WGPUProcSwapChainGetCurrentTextureView',
    'WGPUProcSwapChainPresent', 'WGPUProcSwapChainRelease',
    'WGPUProcTextureAddRef', 'WGPUProcTextureCreateErrorView',
    'WGPUProcTextureCreateView', 'WGPUProcTextureDestroy',
    'WGPUProcTextureGetDepthOrArrayLayers',
    'WGPUProcTextureGetDimension', 'WGPUProcTextureGetFormat',
    'WGPUProcTextureGetHeight', 'WGPUProcTextureGetMipLevelCount',
    'WGPUProcTextureGetSampleCount', 'WGPUProcTextureGetUsage',
    'WGPUProcTextureGetWidth', 'WGPUProcTextureRelease',
    'WGPUProcTextureSetLabel', 'WGPUProcTextureViewAddRef',
    'WGPUProcTextureViewRelease', 'WGPUProcTextureViewSetLabel',
    'WGPUProgrammableStageDescriptor', 'WGPUQuerySet',
    'WGPUQuerySetDescriptor', 'WGPUQueryType',
    'WGPUQueryType_Force32', 'WGPUQueryType_Occlusion',
    'WGPUQueryType_Timestamp', 'WGPUQueue', 'WGPUQueueDescriptor',
    'WGPUQueueWorkDoneCallback', 'WGPUQueueWorkDoneCallback2',
    'WGPUQueueWorkDoneCallbackInfo', 'WGPUQueueWorkDoneCallbackInfo2',
    'WGPUQueueWorkDoneStatus', 'WGPUQueueWorkDoneStatus_DeviceLost',
    'WGPUQueueWorkDoneStatus_Error',
    'WGPUQueueWorkDoneStatus_Force32',
    'WGPUQueueWorkDoneStatus_InstanceDropped',
    'WGPUQueueWorkDoneStatus_Success',
    'WGPUQueueWorkDoneStatus_Unknown', 'WGPURenderBundle',
    'WGPURenderBundleDescriptor', 'WGPURenderBundleEncoder',
    'WGPURenderBundleEncoderDescriptor',
    'WGPURenderPassColorAttachment',
    'WGPURenderPassDepthStencilAttachment',
    'WGPURenderPassDescriptor',
    'WGPURenderPassDescriptorMaxDrawCount', 'WGPURenderPassEncoder',
    'WGPURenderPassPixelLocalStorage',
    'WGPURenderPassStorageAttachment',
    'WGPURenderPassTimestampWrites', 'WGPURenderPipeline',
    'WGPURenderPipelineDescriptor', 'WGPURequestAdapterCallback',
    'WGPURequestAdapterCallback2', 'WGPURequestAdapterCallbackInfo',
    'WGPURequestAdapterCallbackInfo2', 'WGPURequestAdapterOptions',
    'WGPURequestAdapterStatus', 'WGPURequestAdapterStatus_Error',
    'WGPURequestAdapterStatus_Force32',
    'WGPURequestAdapterStatus_InstanceDropped',
    'WGPURequestAdapterStatus_Success',
    'WGPURequestAdapterStatus_Unavailable',
    'WGPURequestAdapterStatus_Unknown', 'WGPURequestDeviceCallback',
    'WGPURequestDeviceCallback2', 'WGPURequestDeviceCallbackInfo',
    'WGPURequestDeviceCallbackInfo2', 'WGPURequestDeviceStatus',
    'WGPURequestDeviceStatus_Error',
    'WGPURequestDeviceStatus_Force32',
    'WGPURequestDeviceStatus_InstanceDropped',
    'WGPURequestDeviceStatus_Success',
    'WGPURequestDeviceStatus_Unknown', 'WGPURequiredLimits',
    'WGPUSType', 'WGPUSType_AHardwareBufferProperties',
    'WGPUSType_AdapterPropertiesD3D',
    'WGPUSType_AdapterPropertiesMemoryHeaps',
    'WGPUSType_AdapterPropertiesVk',
    'WGPUSType_BufferHostMappedPointer',
    'WGPUSType_ColorTargetStateExpandResolveTextureDawn',
    'WGPUSType_DawnAdapterPropertiesPowerPreference',
    'WGPUSType_DawnBufferDescriptorErrorInfoFromWireClient',
    'WGPUSType_DawnCacheDeviceDescriptor',
    'WGPUSType_DawnComputePipelineFullSubgroups',
    'WGPUSType_DawnEncoderInternalUsageDescriptor',
    'WGPUSType_DawnExperimentalSubgroupLimits',
    'WGPUSType_DawnInstanceDescriptor',
    'WGPUSType_DawnRenderPassColorAttachmentRenderToSingleSampled',
    'WGPUSType_DawnShaderModuleSPIRVOptionsDescriptor',
    'WGPUSType_DawnTextureInternalUsageDescriptor',
    'WGPUSType_DawnTogglesDescriptor', 'WGPUSType_DawnWGSLBlocklist',
    'WGPUSType_DawnWireWGSLControl',
    'WGPUSType_DepthStencilStateDepthWriteDefinedDawn',
    'WGPUSType_DrmFormatCapabilities',
    'WGPUSType_ExternalTextureBindingEntry',
    'WGPUSType_ExternalTextureBindingLayout', 'WGPUSType_Force32',
    'WGPUSType_Invalid', 'WGPUSType_PipelineLayoutPixelLocalStorage',
    'WGPUSType_PrimitiveDepthClipControl',
    'WGPUSType_RenderPassDescriptorMaxDrawCount',
    'WGPUSType_RenderPassPixelLocalStorage',
    'WGPUSType_RequestAdapterOptionsD3D11Device',
    'WGPUSType_RequestAdapterOptionsGetGLProc',
    'WGPUSType_RequestAdapterOptionsLUID',
    'WGPUSType_ShaderModuleCompilationOptions',
    'WGPUSType_ShaderModuleSPIRVDescriptor',
    'WGPUSType_ShaderModuleWGSLDescriptor',
    'WGPUSType_SharedBufferMemoryD3D12ResourceDescriptor',
    'WGPUSType_SharedFenceDXGISharedHandleDescriptor',
    'WGPUSType_SharedFenceDXGISharedHandleExportInfo',
    'WGPUSType_SharedFenceMTLSharedEventDescriptor',
    'WGPUSType_SharedFenceMTLSharedEventExportInfo',
    'WGPUSType_SharedFenceVkSemaphoreOpaqueFDDescriptor',
    'WGPUSType_SharedFenceVkSemaphoreOpaqueFDExportInfo',
    'WGPUSType_SharedFenceVkSemaphoreSyncFDDescriptor',
    'WGPUSType_SharedFenceVkSemaphoreSyncFDExportInfo',
    'WGPUSType_SharedFenceVkSemaphoreZirconHandleDescriptor',
    'WGPUSType_SharedFenceVkSemaphoreZirconHandleExportInfo',
    'WGPUSType_SharedTextureMemoryAHardwareBufferDescriptor',
    'WGPUSType_SharedTextureMemoryAHardwareBufferProperties',
    'WGPUSType_SharedTextureMemoryD3D11Texture2DDescriptor',
    'WGPUSType_SharedTextureMemoryD3DSwapchainBeginState',
    'WGPUSType_SharedTextureMemoryDXGISharedHandleDescriptor',
    'WGPUSType_SharedTextureMemoryDmaBufDescriptor',
    'WGPUSType_SharedTextureMemoryEGLImageDescriptor',
    'WGPUSType_SharedTextureMemoryIOSurfaceDescriptor',
    'WGPUSType_SharedTextureMemoryInitializedBeginState',
    'WGPUSType_SharedTextureMemoryInitializedEndState',
    'WGPUSType_SharedTextureMemoryOpaqueFDDescriptor',
    'WGPUSType_SharedTextureMemoryVkDedicatedAllocationDescriptor',
    'WGPUSType_SharedTextureMemoryVkImageLayoutBeginState',
    'WGPUSType_SharedTextureMemoryVkImageLayoutEndState',
    'WGPUSType_SharedTextureMemoryZirconHandleDescriptor',
    'WGPUSType_StaticSamplerBindingLayout',
    'WGPUSType_SurfaceDescriptorFromAndroidNativeWindow',
    'WGPUSType_SurfaceDescriptorFromCanvasHTMLSelector',
    'WGPUSType_SurfaceDescriptorFromMetalLayer',
    'WGPUSType_SurfaceDescriptorFromWaylandSurface',
    'WGPUSType_SurfaceDescriptorFromWindowsCoreWindow',
    'WGPUSType_SurfaceDescriptorFromWindowsHWND',
    'WGPUSType_SurfaceDescriptorFromWindowsSwapChainPanel',
    'WGPUSType_SurfaceDescriptorFromXlibWindow',
    'WGPUSType_TextureBindingViewDimensionDescriptor',
    'WGPUSType_YCbCrVkDescriptor', 'WGPUSampler',
    'WGPUSamplerBindingLayout', 'WGPUSamplerBindingType',
    'WGPUSamplerBindingType_Comparison',
    'WGPUSamplerBindingType_Filtering',
    'WGPUSamplerBindingType_Force32',
    'WGPUSamplerBindingType_NonFiltering',
    'WGPUSamplerBindingType_Undefined', 'WGPUSamplerDescriptor',
    'WGPUShaderModule', 'WGPUShaderModuleCompilationOptions',
    'WGPUShaderModuleDescriptor', 'WGPUShaderModuleSPIRVDescriptor',
    'WGPUShaderModuleWGSLDescriptor', 'WGPUShaderStage',
    'WGPUShaderStageFlags', 'WGPUShaderStage_Compute',
    'WGPUShaderStage_Force32', 'WGPUShaderStage_Fragment',
    'WGPUShaderStage_None', 'WGPUShaderStage_Vertex',
    'WGPUSharedBufferMemory',
    'WGPUSharedBufferMemoryBeginAccessDescriptor',
    'WGPUSharedBufferMemoryDescriptor',
    'WGPUSharedBufferMemoryEndAccessState',
    'WGPUSharedBufferMemoryProperties', 'WGPUSharedFence',
    'WGPUSharedFenceDXGISharedHandleDescriptor',
    'WGPUSharedFenceDXGISharedHandleExportInfo',
    'WGPUSharedFenceDescriptor', 'WGPUSharedFenceExportInfo',
    'WGPUSharedFenceMTLSharedEventDescriptor',
    'WGPUSharedFenceMTLSharedEventExportInfo', 'WGPUSharedFenceType',
    'WGPUSharedFenceType_DXGISharedHandle',
    'WGPUSharedFenceType_Force32',
    'WGPUSharedFenceType_MTLSharedEvent',
    'WGPUSharedFenceType_Undefined',
    'WGPUSharedFenceType_VkSemaphoreOpaqueFD',
    'WGPUSharedFenceType_VkSemaphoreSyncFD',
    'WGPUSharedFenceType_VkSemaphoreZirconHandle',
    'WGPUSharedFenceVkSemaphoreOpaqueFDDescriptor',
    'WGPUSharedFenceVkSemaphoreOpaqueFDExportInfo',
    'WGPUSharedFenceVkSemaphoreSyncFDDescriptor',
    'WGPUSharedFenceVkSemaphoreSyncFDExportInfo',
    'WGPUSharedFenceVkSemaphoreZirconHandleDescriptor',
    'WGPUSharedFenceVkSemaphoreZirconHandleExportInfo',
    'WGPUSharedTextureMemory',
    'WGPUSharedTextureMemoryAHardwareBufferDescriptor',
    'WGPUSharedTextureMemoryAHardwareBufferProperties',
    'WGPUSharedTextureMemoryBeginAccessDescriptor',
    'WGPUSharedTextureMemoryD3DSwapchainBeginState',
    'WGPUSharedTextureMemoryDXGISharedHandleDescriptor',
    'WGPUSharedTextureMemoryDescriptor',
    'WGPUSharedTextureMemoryDmaBufDescriptor',
    'WGPUSharedTextureMemoryDmaBufPlane',
    'WGPUSharedTextureMemoryEGLImageDescriptor',
    'WGPUSharedTextureMemoryEndAccessState',
    'WGPUSharedTextureMemoryIOSurfaceDescriptor',
    'WGPUSharedTextureMemoryOpaqueFDDescriptor',
    'WGPUSharedTextureMemoryProperties',
    'WGPUSharedTextureMemoryVkDedicatedAllocationDescriptor',
    'WGPUSharedTextureMemoryVkImageLayoutBeginState',
    'WGPUSharedTextureMemoryVkImageLayoutEndState',
    'WGPUSharedTextureMemoryZirconHandleDescriptor',
    'WGPUStaticSamplerBindingLayout', 'WGPUStatus',
    'WGPUStatus_Error', 'WGPUStatus_Force32', 'WGPUStatus_Success',
    'WGPUStencilFaceState', 'WGPUStencilOperation',
    'WGPUStencilOperation_DecrementClamp',
    'WGPUStencilOperation_DecrementWrap',
    'WGPUStencilOperation_Force32',
    'WGPUStencilOperation_IncrementClamp',
    'WGPUStencilOperation_IncrementWrap',
    'WGPUStencilOperation_Invert', 'WGPUStencilOperation_Keep',
    'WGPUStencilOperation_Replace', 'WGPUStencilOperation_Undefined',
    'WGPUStencilOperation_Zero', 'WGPUStorageTextureAccess',
    'WGPUStorageTextureAccess_Force32',
    'WGPUStorageTextureAccess_ReadOnly',
    'WGPUStorageTextureAccess_ReadWrite',
    'WGPUStorageTextureAccess_Undefined',
    'WGPUStorageTextureAccess_WriteOnly',
    'WGPUStorageTextureBindingLayout', 'WGPUStoreOp',
    'WGPUStoreOp_Discard', 'WGPUStoreOp_Force32', 'WGPUStoreOp_Store',
    'WGPUStoreOp_Undefined', 'WGPUSupportedLimits', 'WGPUSurface',
    'WGPUSurfaceCapabilities', 'WGPUSurfaceConfiguration',
    'WGPUSurfaceDescriptor',
    'WGPUSurfaceDescriptorFromAndroidNativeWindow',
    'WGPUSurfaceDescriptorFromCanvasHTMLSelector',
    'WGPUSurfaceDescriptorFromMetalLayer',
    'WGPUSurfaceDescriptorFromWaylandSurface',
    'WGPUSurfaceDescriptorFromWindowsCoreWindow',
    'WGPUSurfaceDescriptorFromWindowsHWND',
    'WGPUSurfaceDescriptorFromWindowsSwapChainPanel',
    'WGPUSurfaceDescriptorFromXlibWindow',
    'WGPUSurfaceGetCurrentTextureStatus',
    'WGPUSurfaceGetCurrentTextureStatus_DeviceLost',
    'WGPUSurfaceGetCurrentTextureStatus_Error',
    'WGPUSurfaceGetCurrentTextureStatus_Force32',
    'WGPUSurfaceGetCurrentTextureStatus_Lost',
    'WGPUSurfaceGetCurrentTextureStatus_OutOfMemory',
    'WGPUSurfaceGetCurrentTextureStatus_Outdated',
    'WGPUSurfaceGetCurrentTextureStatus_Success',
    'WGPUSurfaceGetCurrentTextureStatus_Timeout',
    'WGPUSurfaceTexture', 'WGPUSwapChain', 'WGPUSwapChainDescriptor',
    'WGPUTexture', 'WGPUTextureAspect', 'WGPUTextureAspect_All',
    'WGPUTextureAspect_DepthOnly', 'WGPUTextureAspect_Force32',
    'WGPUTextureAspect_Plane0Only', 'WGPUTextureAspect_Plane1Only',
    'WGPUTextureAspect_Plane2Only', 'WGPUTextureAspect_StencilOnly',
    'WGPUTextureAspect_Undefined', 'WGPUTextureBindingLayout',
    'WGPUTextureBindingViewDimensionDescriptor',
    'WGPUTextureDataLayout', 'WGPUTextureDescriptor',
    'WGPUTextureDimension', 'WGPUTextureDimension_1D',
    'WGPUTextureDimension_2D', 'WGPUTextureDimension_3D',
    'WGPUTextureDimension_Force32', 'WGPUTextureDimension_Undefined',
    'WGPUTextureFormat', 'WGPUTextureFormat_ASTC10x10Unorm',
    'WGPUTextureFormat_ASTC10x10UnormSrgb',
    'WGPUTextureFormat_ASTC10x5Unorm',
    'WGPUTextureFormat_ASTC10x5UnormSrgb',
    'WGPUTextureFormat_ASTC10x6Unorm',
    'WGPUTextureFormat_ASTC10x6UnormSrgb',
    'WGPUTextureFormat_ASTC10x8Unorm',
    'WGPUTextureFormat_ASTC10x8UnormSrgb',
    'WGPUTextureFormat_ASTC12x10Unorm',
    'WGPUTextureFormat_ASTC12x10UnormSrgb',
    'WGPUTextureFormat_ASTC12x12Unorm',
    'WGPUTextureFormat_ASTC12x12UnormSrgb',
    'WGPUTextureFormat_ASTC4x4Unorm',
    'WGPUTextureFormat_ASTC4x4UnormSrgb',
    'WGPUTextureFormat_ASTC5x4Unorm',
    'WGPUTextureFormat_ASTC5x4UnormSrgb',
    'WGPUTextureFormat_ASTC5x5Unorm',
    'WGPUTextureFormat_ASTC5x5UnormSrgb',
    'WGPUTextureFormat_ASTC6x5Unorm',
    'WGPUTextureFormat_ASTC6x5UnormSrgb',
    'WGPUTextureFormat_ASTC6x6Unorm',
    'WGPUTextureFormat_ASTC6x6UnormSrgb',
    'WGPUTextureFormat_ASTC8x5Unorm',
    'WGPUTextureFormat_ASTC8x5UnormSrgb',
    'WGPUTextureFormat_ASTC8x6Unorm',
    'WGPUTextureFormat_ASTC8x6UnormSrgb',
    'WGPUTextureFormat_ASTC8x8Unorm',
    'WGPUTextureFormat_ASTC8x8UnormSrgb',
    'WGPUTextureFormat_BC1RGBAUnorm',
    'WGPUTextureFormat_BC1RGBAUnormSrgb',
    'WGPUTextureFormat_BC2RGBAUnorm',
    'WGPUTextureFormat_BC2RGBAUnormSrgb',
    'WGPUTextureFormat_BC3RGBAUnorm',
    'WGPUTextureFormat_BC3RGBAUnormSrgb',
    'WGPUTextureFormat_BC4RSnorm', 'WGPUTextureFormat_BC4RUnorm',
    'WGPUTextureFormat_BC5RGSnorm', 'WGPUTextureFormat_BC5RGUnorm',
    'WGPUTextureFormat_BC6HRGBFloat',
    'WGPUTextureFormat_BC6HRGBUfloat',
    'WGPUTextureFormat_BC7RGBAUnorm',
    'WGPUTextureFormat_BC7RGBAUnormSrgb',
    'WGPUTextureFormat_BGRA8Unorm',
    'WGPUTextureFormat_BGRA8UnormSrgb',
    'WGPUTextureFormat_Depth16Unorm', 'WGPUTextureFormat_Depth24Plus',
    'WGPUTextureFormat_Depth24PlusStencil8',
    'WGPUTextureFormat_Depth32Float',
    'WGPUTextureFormat_Depth32FloatStencil8',
    'WGPUTextureFormat_EACR11Snorm', 'WGPUTextureFormat_EACR11Unorm',
    'WGPUTextureFormat_EACRG11Snorm',
    'WGPUTextureFormat_EACRG11Unorm',
    'WGPUTextureFormat_ETC2RGB8A1Unorm',
    'WGPUTextureFormat_ETC2RGB8A1UnormSrgb',
    'WGPUTextureFormat_ETC2RGB8Unorm',
    'WGPUTextureFormat_ETC2RGB8UnormSrgb',
    'WGPUTextureFormat_ETC2RGBA8Unorm',
    'WGPUTextureFormat_ETC2RGBA8UnormSrgb',
    'WGPUTextureFormat_External', 'WGPUTextureFormat_Force32',
    'WGPUTextureFormat_R10X6BG10X6Biplanar420Unorm',
    'WGPUTextureFormat_R10X6BG10X6Biplanar422Unorm',
    'WGPUTextureFormat_R10X6BG10X6Biplanar444Unorm',
    'WGPUTextureFormat_R16Float', 'WGPUTextureFormat_R16Sint',
    'WGPUTextureFormat_R16Snorm', 'WGPUTextureFormat_R16Uint',
    'WGPUTextureFormat_R16Unorm', 'WGPUTextureFormat_R32Float',
    'WGPUTextureFormat_R32Sint', 'WGPUTextureFormat_R32Uint',
    'WGPUTextureFormat_R8BG8A8Triplanar420Unorm',
    'WGPUTextureFormat_R8BG8Biplanar420Unorm',
    'WGPUTextureFormat_R8BG8Biplanar422Unorm',
    'WGPUTextureFormat_R8BG8Biplanar444Unorm',
    'WGPUTextureFormat_R8Sint', 'WGPUTextureFormat_R8Snorm',
    'WGPUTextureFormat_R8Uint', 'WGPUTextureFormat_R8Unorm',
    'WGPUTextureFormat_RG11B10Ufloat', 'WGPUTextureFormat_RG16Float',
    'WGPUTextureFormat_RG16Sint', 'WGPUTextureFormat_RG16Snorm',
    'WGPUTextureFormat_RG16Uint', 'WGPUTextureFormat_RG16Unorm',
    'WGPUTextureFormat_RG32Float', 'WGPUTextureFormat_RG32Sint',
    'WGPUTextureFormat_RG32Uint', 'WGPUTextureFormat_RG8Sint',
    'WGPUTextureFormat_RG8Snorm', 'WGPUTextureFormat_RG8Uint',
    'WGPUTextureFormat_RG8Unorm', 'WGPUTextureFormat_RGB10A2Uint',
    'WGPUTextureFormat_RGB10A2Unorm',
    'WGPUTextureFormat_RGB9E5Ufloat', 'WGPUTextureFormat_RGBA16Float',
    'WGPUTextureFormat_RGBA16Sint', 'WGPUTextureFormat_RGBA16Snorm',
    'WGPUTextureFormat_RGBA16Uint', 'WGPUTextureFormat_RGBA16Unorm',
    'WGPUTextureFormat_RGBA32Float', 'WGPUTextureFormat_RGBA32Sint',
    'WGPUTextureFormat_RGBA32Uint', 'WGPUTextureFormat_RGBA8Sint',
    'WGPUTextureFormat_RGBA8Snorm', 'WGPUTextureFormat_RGBA8Uint',
    'WGPUTextureFormat_RGBA8Unorm',
    'WGPUTextureFormat_RGBA8UnormSrgb', 'WGPUTextureFormat_Stencil8',
    'WGPUTextureFormat_Undefined', 'WGPUTextureSampleType',
    'WGPUTextureSampleType_Depth', 'WGPUTextureSampleType_Float',
    'WGPUTextureSampleType_Force32', 'WGPUTextureSampleType_Sint',
    'WGPUTextureSampleType_Uint', 'WGPUTextureSampleType_Undefined',
    'WGPUTextureSampleType_UnfilterableFloat', 'WGPUTextureUsage',
    'WGPUTextureUsageFlags', 'WGPUTextureUsage_CopyDst',
    'WGPUTextureUsage_CopySrc', 'WGPUTextureUsage_Force32',
    'WGPUTextureUsage_None', 'WGPUTextureUsage_RenderAttachment',
    'WGPUTextureUsage_StorageAttachment',
    'WGPUTextureUsage_StorageBinding',
    'WGPUTextureUsage_TextureBinding',
    'WGPUTextureUsage_TransientAttachment', 'WGPUTextureView',
    'WGPUTextureViewDescriptor', 'WGPUTextureViewDimension',
    'WGPUTextureViewDimension_1D', 'WGPUTextureViewDimension_2D',
    'WGPUTextureViewDimension_2DArray', 'WGPUTextureViewDimension_3D',
    'WGPUTextureViewDimension_Cube',
    'WGPUTextureViewDimension_CubeArray',
    'WGPUTextureViewDimension_Force32',
    'WGPUTextureViewDimension_Undefined',
    'WGPUUncapturedErrorCallbackInfo', 'WGPUVertexAttribute',
    'WGPUVertexBufferLayout', 'WGPUVertexFormat',
    'WGPUVertexFormat_Float16x2', 'WGPUVertexFormat_Float16x4',
    'WGPUVertexFormat_Float32', 'WGPUVertexFormat_Float32x2',
    'WGPUVertexFormat_Float32x3', 'WGPUVertexFormat_Float32x4',
    'WGPUVertexFormat_Force32', 'WGPUVertexFormat_Sint16x2',
    'WGPUVertexFormat_Sint16x4', 'WGPUVertexFormat_Sint32',
    'WGPUVertexFormat_Sint32x2', 'WGPUVertexFormat_Sint32x3',
    'WGPUVertexFormat_Sint32x4', 'WGPUVertexFormat_Sint8x2',
    'WGPUVertexFormat_Sint8x4', 'WGPUVertexFormat_Snorm16x2',
    'WGPUVertexFormat_Snorm16x4', 'WGPUVertexFormat_Snorm8x2',
    'WGPUVertexFormat_Snorm8x4', 'WGPUVertexFormat_Uint16x2',
    'WGPUVertexFormat_Uint16x4', 'WGPUVertexFormat_Uint32',
    'WGPUVertexFormat_Uint32x2', 'WGPUVertexFormat_Uint32x3',
    'WGPUVertexFormat_Uint32x4', 'WGPUVertexFormat_Uint8x2',
    'WGPUVertexFormat_Uint8x4', 'WGPUVertexFormat_Undefined',
    'WGPUVertexFormat_Unorm10_10_10_2', 'WGPUVertexFormat_Unorm16x2',
    'WGPUVertexFormat_Unorm16x4', 'WGPUVertexFormat_Unorm8x2',
    'WGPUVertexFormat_Unorm8x4', 'WGPUVertexState',
    'WGPUVertexStepMode', 'WGPUVertexStepMode_Force32',
    'WGPUVertexStepMode_Instance', 'WGPUVertexStepMode_Undefined',
    'WGPUVertexStepMode_Vertex',
    'WGPUVertexStepMode_VertexBufferNotUsed', 'WGPUWGSLFeatureName',
    'WGPUWGSLFeatureName_ChromiumTestingExperimental',
    'WGPUWGSLFeatureName_ChromiumTestingShipped',
    'WGPUWGSLFeatureName_ChromiumTestingShippedWithKillswitch',
    'WGPUWGSLFeatureName_ChromiumTestingUnimplemented',
    'WGPUWGSLFeatureName_ChromiumTestingUnsafeExperimental',
    'WGPUWGSLFeatureName_Force32',
    'WGPUWGSLFeatureName_Packed4x8IntegerDotProduct',
    'WGPUWGSLFeatureName_PointerCompositeAccess',
    'WGPUWGSLFeatureName_ReadonlyAndReadwriteStorageTextures',
    'WGPUWGSLFeatureName_Undefined',
    'WGPUWGSLFeatureName_UnrestrictedPointerParameters',
    'WGPUWaitStatus', 'WGPUWaitStatus_Force32',
    'WGPUWaitStatus_Success', 'WGPUWaitStatus_TimedOut',
    'WGPUWaitStatus_Unknown', 'WGPUWaitStatus_UnsupportedCount',
    'WGPUWaitStatus_UnsupportedMixedSources',
    'WGPUWaitStatus_UnsupportedTimeout', 'WGPUYCbCrVkDescriptor',
    'int32_t', 'size_t', 'struct_WGPUAHardwareBufferProperties',
    'struct_WGPUAdapterImpl', 'struct_WGPUAdapterInfo',
    'struct_WGPUAdapterProperties', 'struct_WGPUAdapterPropertiesD3D',
    'struct_WGPUAdapterPropertiesMemoryHeaps',
    'struct_WGPUAdapterPropertiesVk',
    'struct_WGPUBindGroupDescriptor', 'struct_WGPUBindGroupEntry',
    'struct_WGPUBindGroupImpl',
    'struct_WGPUBindGroupLayoutDescriptor',
    'struct_WGPUBindGroupLayoutEntry',
    'struct_WGPUBindGroupLayoutImpl', 'struct_WGPUBlendComponent',
    'struct_WGPUBlendState', 'struct_WGPUBufferBindingLayout',
    'struct_WGPUBufferDescriptor',
    'struct_WGPUBufferHostMappedPointer', 'struct_WGPUBufferImpl',
    'struct_WGPUBufferMapCallbackInfo',
    'struct_WGPUBufferMapCallbackInfo2', 'struct_WGPUChainedStruct',
    'struct_WGPUChainedStructOut', 'struct_WGPUColor',
    'struct_WGPUColorTargetState',
    'struct_WGPUColorTargetStateExpandResolveTextureDawn',
    'struct_WGPUCommandBufferDescriptor',
    'struct_WGPUCommandBufferImpl',
    'struct_WGPUCommandEncoderDescriptor',
    'struct_WGPUCommandEncoderImpl', 'struct_WGPUCompilationInfo',
    'struct_WGPUCompilationInfoCallbackInfo',
    'struct_WGPUCompilationInfoCallbackInfo2',
    'struct_WGPUCompilationMessage',
    'struct_WGPUComputePassDescriptor',
    'struct_WGPUComputePassEncoderImpl',
    'struct_WGPUComputePassTimestampWrites',
    'struct_WGPUComputePipelineDescriptor',
    'struct_WGPUComputePipelineImpl', 'struct_WGPUConstantEntry',
    'struct_WGPUCopyTextureForBrowserOptions',
    'struct_WGPUCreateComputePipelineAsyncCallbackInfo',
    'struct_WGPUCreateComputePipelineAsyncCallbackInfo2',
    'struct_WGPUCreateRenderPipelineAsyncCallbackInfo',
    'struct_WGPUCreateRenderPipelineAsyncCallbackInfo2',
    'struct_WGPUDawnAdapterPropertiesPowerPreference',
    'struct_WGPUDawnBufferDescriptorErrorInfoFromWireClient',
    'struct_WGPUDawnCacheDeviceDescriptor',
    'struct_WGPUDawnComputePipelineFullSubgroups',
    'struct_WGPUDawnEncoderInternalUsageDescriptor',
    'struct_WGPUDawnExperimentalSubgroupLimits',
    'struct_WGPUDawnRenderPassColorAttachmentRenderToSingleSampled',
    'struct_WGPUDawnShaderModuleSPIRVOptionsDescriptor',
    'struct_WGPUDawnTextureInternalUsageDescriptor',
    'struct_WGPUDawnTogglesDescriptor',
    'struct_WGPUDawnWGSLBlocklist', 'struct_WGPUDawnWireWGSLControl',
    'struct_WGPUDepthStencilState',
    'struct_WGPUDepthStencilStateDepthWriteDefinedDawn',
    'struct_WGPUDeviceDescriptor', 'struct_WGPUDeviceImpl',
    'struct_WGPUDeviceLostCallbackInfo',
    'struct_WGPUDrmFormatCapabilities',
    'struct_WGPUDrmFormatProperties', 'struct_WGPUExtent2D',
    'struct_WGPUExtent3D', 'struct_WGPUExternalTextureBindingEntry',
    'struct_WGPUExternalTextureBindingLayout',
    'struct_WGPUExternalTextureDescriptor',
    'struct_WGPUExternalTextureImpl', 'struct_WGPUFormatCapabilities',
    'struct_WGPUFragmentState', 'struct_WGPUFuture',
    'struct_WGPUFutureWaitInfo', 'struct_WGPUImageCopyBuffer',
    'struct_WGPUImageCopyExternalTexture',
    'struct_WGPUImageCopyTexture', 'struct_WGPUInstanceDescriptor',
    'struct_WGPUInstanceFeatures', 'struct_WGPUInstanceImpl',
    'struct_WGPULimits', 'struct_WGPUMemoryHeapInfo',
    'struct_WGPUMultisampleState', 'struct_WGPUOrigin2D',
    'struct_WGPUOrigin3D', 'struct_WGPUPipelineLayoutDescriptor',
    'struct_WGPUPipelineLayoutImpl',
    'struct_WGPUPipelineLayoutPixelLocalStorage',
    'struct_WGPUPipelineLayoutStorageAttachment',
    'struct_WGPUPopErrorScopeCallbackInfo',
    'struct_WGPUPopErrorScopeCallbackInfo2',
    'struct_WGPUPrimitiveDepthClipControl',
    'struct_WGPUPrimitiveState',
    'struct_WGPUProgrammableStageDescriptor',
    'struct_WGPUQuerySetDescriptor', 'struct_WGPUQuerySetImpl',
    'struct_WGPUQueueDescriptor', 'struct_WGPUQueueImpl',
    'struct_WGPUQueueWorkDoneCallbackInfo',
    'struct_WGPUQueueWorkDoneCallbackInfo2',
    'struct_WGPURenderBundleDescriptor',
    'struct_WGPURenderBundleEncoderDescriptor',
    'struct_WGPURenderBundleEncoderImpl',
    'struct_WGPURenderBundleImpl',
    'struct_WGPURenderPassColorAttachment',
    'struct_WGPURenderPassDepthStencilAttachment',
    'struct_WGPURenderPassDescriptor',
    'struct_WGPURenderPassDescriptorMaxDrawCount',
    'struct_WGPURenderPassEncoderImpl',
    'struct_WGPURenderPassPixelLocalStorage',
    'struct_WGPURenderPassStorageAttachment',
    'struct_WGPURenderPassTimestampWrites',
    'struct_WGPURenderPipelineDescriptor',
    'struct_WGPURenderPipelineImpl',
    'struct_WGPURequestAdapterCallbackInfo',
    'struct_WGPURequestAdapterCallbackInfo2',
    'struct_WGPURequestAdapterOptions',
    'struct_WGPURequestDeviceCallbackInfo',
    'struct_WGPURequestDeviceCallbackInfo2',
    'struct_WGPURequiredLimits', 'struct_WGPUSamplerBindingLayout',
    'struct_WGPUSamplerDescriptor', 'struct_WGPUSamplerImpl',
    'struct_WGPUShaderModuleCompilationOptions',
    'struct_WGPUShaderModuleDescriptor',
    'struct_WGPUShaderModuleImpl',
    'struct_WGPUShaderModuleSPIRVDescriptor',
    'struct_WGPUShaderModuleWGSLDescriptor',
    'struct_WGPUSharedBufferMemoryBeginAccessDescriptor',
    'struct_WGPUSharedBufferMemoryDescriptor',
    'struct_WGPUSharedBufferMemoryEndAccessState',
    'struct_WGPUSharedBufferMemoryImpl',
    'struct_WGPUSharedBufferMemoryProperties',
    'struct_WGPUSharedFenceDXGISharedHandleDescriptor',
    'struct_WGPUSharedFenceDXGISharedHandleExportInfo',
    'struct_WGPUSharedFenceDescriptor',
    'struct_WGPUSharedFenceExportInfo', 'struct_WGPUSharedFenceImpl',
    'struct_WGPUSharedFenceMTLSharedEventDescriptor',
    'struct_WGPUSharedFenceMTLSharedEventExportInfo',
    'struct_WGPUSharedFenceVkSemaphoreOpaqueFDDescriptor',
    'struct_WGPUSharedFenceVkSemaphoreOpaqueFDExportInfo',
    'struct_WGPUSharedFenceVkSemaphoreSyncFDDescriptor',
    'struct_WGPUSharedFenceVkSemaphoreSyncFDExportInfo',
    'struct_WGPUSharedFenceVkSemaphoreZirconHandleDescriptor',
    'struct_WGPUSharedFenceVkSemaphoreZirconHandleExportInfo',
    'struct_WGPUSharedTextureMemoryAHardwareBufferDescriptor',
    'struct_WGPUSharedTextureMemoryAHardwareBufferProperties',
    'struct_WGPUSharedTextureMemoryBeginAccessDescriptor',
    'struct_WGPUSharedTextureMemoryD3DSwapchainBeginState',
    'struct_WGPUSharedTextureMemoryDXGISharedHandleDescriptor',
    'struct_WGPUSharedTextureMemoryDescriptor',
    'struct_WGPUSharedTextureMemoryDmaBufDescriptor',
    'struct_WGPUSharedTextureMemoryDmaBufPlane',
    'struct_WGPUSharedTextureMemoryEGLImageDescriptor',
    'struct_WGPUSharedTextureMemoryEndAccessState',
    'struct_WGPUSharedTextureMemoryIOSurfaceDescriptor',
    'struct_WGPUSharedTextureMemoryImpl',
    'struct_WGPUSharedTextureMemoryOpaqueFDDescriptor',
    'struct_WGPUSharedTextureMemoryProperties',
    'struct_WGPUSharedTextureMemoryVkDedicatedAllocationDescriptor',
    'struct_WGPUSharedTextureMemoryVkImageLayoutBeginState',
    'struct_WGPUSharedTextureMemoryVkImageLayoutEndState',
    'struct_WGPUSharedTextureMemoryZirconHandleDescriptor',
    'struct_WGPUStaticSamplerBindingLayout',
    'struct_WGPUStencilFaceState',
    'struct_WGPUStorageTextureBindingLayout',
    'struct_WGPUSupportedLimits', 'struct_WGPUSurfaceCapabilities',
    'struct_WGPUSurfaceConfiguration', 'struct_WGPUSurfaceDescriptor',
    'struct_WGPUSurfaceDescriptorFromAndroidNativeWindow',
    'struct_WGPUSurfaceDescriptorFromCanvasHTMLSelector',
    'struct_WGPUSurfaceDescriptorFromMetalLayer',
    'struct_WGPUSurfaceDescriptorFromWaylandSurface',
    'struct_WGPUSurfaceDescriptorFromWindowsCoreWindow',
    'struct_WGPUSurfaceDescriptorFromWindowsHWND',
    'struct_WGPUSurfaceDescriptorFromWindowsSwapChainPanel',
    'struct_WGPUSurfaceDescriptorFromXlibWindow',
    'struct_WGPUSurfaceImpl', 'struct_WGPUSurfaceTexture',
    'struct_WGPUSwapChainDescriptor', 'struct_WGPUSwapChainImpl',
    'struct_WGPUTextureBindingLayout',
    'struct_WGPUTextureBindingViewDimensionDescriptor',
    'struct_WGPUTextureDataLayout', 'struct_WGPUTextureDescriptor',
    'struct_WGPUTextureImpl', 'struct_WGPUTextureViewDescriptor',
    'struct_WGPUTextureViewImpl',
    'struct_WGPUUncapturedErrorCallbackInfo',
    'struct_WGPUVertexAttribute', 'struct_WGPUVertexBufferLayout',
    'struct_WGPUVertexState', 'struct_WGPUYCbCrVkDescriptor',
    'uint32_t', 'uint64_t', 'wgpuAdapterAddRef',
    'wgpuAdapterCreateDevice', 'wgpuAdapterEnumerateFeatures',
    'wgpuAdapterGetFormatCapabilities', 'wgpuAdapterGetInfo',
    'wgpuAdapterGetInstance', 'wgpuAdapterGetLimits',
    'wgpuAdapterGetProperties', 'wgpuAdapterHasFeature',
    'wgpuAdapterInfoFreeMembers', 'wgpuAdapterPropertiesFreeMembers',
    'wgpuAdapterPropertiesMemoryHeapsFreeMembers',
    'wgpuAdapterRelease', 'wgpuAdapterRequestDevice',
    'wgpuAdapterRequestDevice2', 'wgpuAdapterRequestDeviceF',
    'wgpuBindGroupAddRef', 'wgpuBindGroupLayoutAddRef',
    'wgpuBindGroupLayoutRelease', 'wgpuBindGroupLayoutSetLabel',
    'wgpuBindGroupRelease', 'wgpuBindGroupSetLabel',
    'wgpuBufferAddRef', 'wgpuBufferDestroy',
    'wgpuBufferGetConstMappedRange', 'wgpuBufferGetMapState',
    'wgpuBufferGetMappedRange', 'wgpuBufferGetSize',
    'wgpuBufferGetUsage', 'wgpuBufferMapAsync', 'wgpuBufferMapAsync2',
    'wgpuBufferMapAsyncF', 'wgpuBufferRelease', 'wgpuBufferSetLabel',
    'wgpuBufferUnmap', 'wgpuCommandBufferAddRef',
    'wgpuCommandBufferRelease', 'wgpuCommandBufferSetLabel',
    'wgpuCommandEncoderAddRef', 'wgpuCommandEncoderBeginComputePass',
    'wgpuCommandEncoderBeginRenderPass',
    'wgpuCommandEncoderClearBuffer',
    'wgpuCommandEncoderCopyBufferToBuffer',
    'wgpuCommandEncoderCopyBufferToTexture',
    'wgpuCommandEncoderCopyTextureToBuffer',
    'wgpuCommandEncoderCopyTextureToTexture',
    'wgpuCommandEncoderFinish',
    'wgpuCommandEncoderInjectValidationError',
    'wgpuCommandEncoderInsertDebugMarker',
    'wgpuCommandEncoderPopDebugGroup',
    'wgpuCommandEncoderPushDebugGroup', 'wgpuCommandEncoderRelease',
    'wgpuCommandEncoderResolveQuerySet', 'wgpuCommandEncoderSetLabel',
    'wgpuCommandEncoderWriteBuffer',
    'wgpuCommandEncoderWriteTimestamp',
    'wgpuComputePassEncoderAddRef',
    'wgpuComputePassEncoderDispatchWorkgroups',
    'wgpuComputePassEncoderDispatchWorkgroupsIndirect',
    'wgpuComputePassEncoderEnd',
    'wgpuComputePassEncoderInsertDebugMarker',
    'wgpuComputePassEncoderPopDebugGroup',
    'wgpuComputePassEncoderPushDebugGroup',
    'wgpuComputePassEncoderRelease',
    'wgpuComputePassEncoderSetBindGroup',
    'wgpuComputePassEncoderSetLabel',
    'wgpuComputePassEncoderSetPipeline',
    'wgpuComputePassEncoderWriteTimestamp',
    'wgpuComputePipelineAddRef',
    'wgpuComputePipelineGetBindGroupLayout',
    'wgpuComputePipelineRelease', 'wgpuComputePipelineSetLabel',
    'wgpuCreateInstance', 'wgpuDeviceAddRef',
    'wgpuDeviceCreateBindGroup', 'wgpuDeviceCreateBindGroupLayout',
    'wgpuDeviceCreateBuffer', 'wgpuDeviceCreateCommandEncoder',
    'wgpuDeviceCreateComputePipeline',
    'wgpuDeviceCreateComputePipelineAsync',
    'wgpuDeviceCreateComputePipelineAsync2',
    'wgpuDeviceCreateComputePipelineAsyncF',
    'wgpuDeviceCreateErrorBuffer',
    'wgpuDeviceCreateErrorExternalTexture',
    'wgpuDeviceCreateErrorShaderModule',
    'wgpuDeviceCreateErrorTexture', 'wgpuDeviceCreateExternalTexture',
    'wgpuDeviceCreatePipelineLayout', 'wgpuDeviceCreateQuerySet',
    'wgpuDeviceCreateRenderBundleEncoder',
    'wgpuDeviceCreateRenderPipeline',
    'wgpuDeviceCreateRenderPipelineAsync',
    'wgpuDeviceCreateRenderPipelineAsync2',
    'wgpuDeviceCreateRenderPipelineAsyncF', 'wgpuDeviceCreateSampler',
    'wgpuDeviceCreateShaderModule', 'wgpuDeviceCreateSwapChain',
    'wgpuDeviceCreateTexture', 'wgpuDeviceDestroy',
    'wgpuDeviceEnumerateFeatures', 'wgpuDeviceForceLoss',
    'wgpuDeviceGetAHardwareBufferProperties', 'wgpuDeviceGetAdapter',
    'wgpuDeviceGetLimits', 'wgpuDeviceGetQueue',
    'wgpuDeviceGetSupportedSurfaceUsage', 'wgpuDeviceHasFeature',
    'wgpuDeviceImportSharedBufferMemory',
    'wgpuDeviceImportSharedFence',
    'wgpuDeviceImportSharedTextureMemory', 'wgpuDeviceInjectError',
    'wgpuDevicePopErrorScope', 'wgpuDevicePopErrorScope2',
    'wgpuDevicePopErrorScopeF', 'wgpuDevicePushErrorScope',
    'wgpuDeviceRelease', 'wgpuDeviceSetDeviceLostCallback',
    'wgpuDeviceSetLabel', 'wgpuDeviceSetLoggingCallback',
    'wgpuDeviceSetUncapturedErrorCallback', 'wgpuDeviceTick',
    'wgpuDeviceValidateTextureDescriptor',
    'wgpuDrmFormatCapabilitiesFreeMembers',
    'wgpuExternalTextureAddRef', 'wgpuExternalTextureDestroy',
    'wgpuExternalTextureExpire', 'wgpuExternalTextureRefresh',
    'wgpuExternalTextureRelease', 'wgpuExternalTextureSetLabel',
    'wgpuGetInstanceFeatures', 'wgpuGetProcAddress',
    'wgpuInstanceAddRef', 'wgpuInstanceCreateSurface',
    'wgpuInstanceEnumerateWGSLLanguageFeatures',
    'wgpuInstanceHasWGSLLanguageFeature', 'wgpuInstanceProcessEvents',
    'wgpuInstanceRelease', 'wgpuInstanceRequestAdapter',
    'wgpuInstanceRequestAdapter2', 'wgpuInstanceRequestAdapterF',
    'wgpuInstanceWaitAny', 'wgpuPipelineLayoutAddRef',
    'wgpuPipelineLayoutRelease', 'wgpuPipelineLayoutSetLabel',
    'wgpuQuerySetAddRef', 'wgpuQuerySetDestroy',
    'wgpuQuerySetGetCount', 'wgpuQuerySetGetType',
    'wgpuQuerySetRelease', 'wgpuQuerySetSetLabel', 'wgpuQueueAddRef',
    'wgpuQueueCopyExternalTextureForBrowser',
    'wgpuQueueCopyTextureForBrowser', 'wgpuQueueOnSubmittedWorkDone',
    'wgpuQueueOnSubmittedWorkDone2', 'wgpuQueueOnSubmittedWorkDoneF',
    'wgpuQueueRelease', 'wgpuQueueSetLabel', 'wgpuQueueSubmit',
    'wgpuQueueWriteBuffer', 'wgpuQueueWriteTexture',
    'wgpuRenderBundleAddRef', 'wgpuRenderBundleEncoderAddRef',
    'wgpuRenderBundleEncoderDraw',
    'wgpuRenderBundleEncoderDrawIndexed',
    'wgpuRenderBundleEncoderDrawIndexedIndirect',
    'wgpuRenderBundleEncoderDrawIndirect',
    'wgpuRenderBundleEncoderFinish',
    'wgpuRenderBundleEncoderInsertDebugMarker',
    'wgpuRenderBundleEncoderPopDebugGroup',
    'wgpuRenderBundleEncoderPushDebugGroup',
    'wgpuRenderBundleEncoderRelease',
    'wgpuRenderBundleEncoderSetBindGroup',
    'wgpuRenderBundleEncoderSetIndexBuffer',
    'wgpuRenderBundleEncoderSetLabel',
    'wgpuRenderBundleEncoderSetPipeline',
    'wgpuRenderBundleEncoderSetVertexBuffer',
    'wgpuRenderBundleRelease', 'wgpuRenderBundleSetLabel',
    'wgpuRenderPassEncoderAddRef',
    'wgpuRenderPassEncoderBeginOcclusionQuery',
    'wgpuRenderPassEncoderDraw', 'wgpuRenderPassEncoderDrawIndexed',
    'wgpuRenderPassEncoderDrawIndexedIndirect',
    'wgpuRenderPassEncoderDrawIndirect', 'wgpuRenderPassEncoderEnd',
    'wgpuRenderPassEncoderEndOcclusionQuery',
    'wgpuRenderPassEncoderExecuteBundles',
    'wgpuRenderPassEncoderInsertDebugMarker',
    'wgpuRenderPassEncoderPixelLocalStorageBarrier',
    'wgpuRenderPassEncoderPopDebugGroup',
    'wgpuRenderPassEncoderPushDebugGroup',
    'wgpuRenderPassEncoderRelease',
    'wgpuRenderPassEncoderSetBindGroup',
    'wgpuRenderPassEncoderSetBlendConstant',
    'wgpuRenderPassEncoderSetIndexBuffer',
    'wgpuRenderPassEncoderSetLabel',
    'wgpuRenderPassEncoderSetPipeline',
    'wgpuRenderPassEncoderSetScissorRect',
    'wgpuRenderPassEncoderSetStencilReference',
    'wgpuRenderPassEncoderSetVertexBuffer',
    'wgpuRenderPassEncoderSetViewport',
    'wgpuRenderPassEncoderWriteTimestamp', 'wgpuRenderPipelineAddRef',
    'wgpuRenderPipelineGetBindGroupLayout',
    'wgpuRenderPipelineRelease', 'wgpuRenderPipelineSetLabel',
    'wgpuSamplerAddRef', 'wgpuSamplerRelease', 'wgpuSamplerSetLabel',
    'wgpuShaderModuleAddRef', 'wgpuShaderModuleGetCompilationInfo',
    'wgpuShaderModuleGetCompilationInfo2',
    'wgpuShaderModuleGetCompilationInfoF', 'wgpuShaderModuleRelease',
    'wgpuShaderModuleSetLabel', 'wgpuSharedBufferMemoryAddRef',
    'wgpuSharedBufferMemoryBeginAccess',
    'wgpuSharedBufferMemoryCreateBuffer',
    'wgpuSharedBufferMemoryEndAccess',
    'wgpuSharedBufferMemoryEndAccessStateFreeMembers',
    'wgpuSharedBufferMemoryGetProperties',
    'wgpuSharedBufferMemoryIsDeviceLost',
    'wgpuSharedBufferMemoryRelease', 'wgpuSharedBufferMemorySetLabel',
    'wgpuSharedFenceAddRef', 'wgpuSharedFenceExportInfo',
    'wgpuSharedFenceRelease', 'wgpuSharedTextureMemoryAddRef',
    'wgpuSharedTextureMemoryBeginAccess',
    'wgpuSharedTextureMemoryCreateTexture',
    'wgpuSharedTextureMemoryEndAccess',
    'wgpuSharedTextureMemoryEndAccessStateFreeMembers',
    'wgpuSharedTextureMemoryGetProperties',
    'wgpuSharedTextureMemoryIsDeviceLost',
    'wgpuSharedTextureMemoryRelease',
    'wgpuSharedTextureMemorySetLabel', 'wgpuSurfaceAddRef',
    'wgpuSurfaceCapabilitiesFreeMembers', 'wgpuSurfaceConfigure',
    'wgpuSurfaceGetCapabilities', 'wgpuSurfaceGetCurrentTexture',
    'wgpuSurfaceGetPreferredFormat', 'wgpuSurfacePresent',
    'wgpuSurfaceRelease', 'wgpuSurfaceUnconfigure',
    'wgpuSwapChainAddRef', 'wgpuSwapChainGetCurrentTexture',
    'wgpuSwapChainGetCurrentTextureView', 'wgpuSwapChainPresent',
    'wgpuSwapChainRelease', 'wgpuTextureAddRef',
    'wgpuTextureCreateErrorView', 'wgpuTextureCreateView',
    'wgpuTextureDestroy', 'wgpuTextureGetDepthOrArrayLayers',
    'wgpuTextureGetDimension', 'wgpuTextureGetFormat',
    'wgpuTextureGetHeight', 'wgpuTextureGetMipLevelCount',
    'wgpuTextureGetSampleCount', 'wgpuTextureGetUsage',
    'wgpuTextureGetWidth', 'wgpuTextureRelease',
    'wgpuTextureSetLabel', 'wgpuTextureViewAddRef',
    'wgpuTextureViewRelease', 'wgpuTextureViewSetLabel']
