# -*- coding: utf-8 -*-
#
# TARGET arch is: ['-I/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX15.5.sdk/usr/include']
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 8
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



c_int128 = ctypes.c_ubyte*16
c_uint128 = c_int128
void = None
if ctypes.sizeof(ctypes.c_longdouble) == 8:
    c_long_double_t = ctypes.c_longdouble
else:
    c_long_double_t = ctypes.c_ubyte*8

class FunctionFactoryStub:
    def __getattr__(self, _):
      return ctypes.CFUNCTYPE(lambda y:y)

# libraries['FIXME_STUB'] explanation
# As you did not list (-l libraryname.so) a library that exports this function
# This is a non-working stub instead. 
# You can either re-run clan2py with -l /path/to/library.so
# Or manually fix this by comment the ctypes.CDLL loading
_libraries = {}
_libraries['FIXME_STUB'] = FunctionFactoryStub() #  ctypes.CDLL('FIXME_STUB')
_libraries['libwebgpu_dawn_subgroup_test.dylib'] = ctypes.CDLL('./pydawn/lib/libwebgpu_dawn_subgroup_test.dylib')


class struct_WGPUStringView(Structure):
    pass

struct_WGPUStringView._pack_ = 1 # source:False
struct_WGPUStringView._fields_ = [
    ('data', ctypes.POINTER(ctypes.c_char)),
    ('length', ctypes.c_uint64),
]

WGPUStringView = struct_WGPUStringView
WGPUFlags = ctypes.c_uint64
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
class struct_WGPURenderPipelineImpl(Structure):
    pass

WGPURenderPipeline = ctypes.POINTER(struct_WGPURenderPipelineImpl)
class struct_WGPUResourceTableImpl(Structure):
    pass

WGPUResourceTable = ctypes.POINTER(struct_WGPUResourceTableImpl)
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
class struct_WGPUTexelBufferViewImpl(Structure):
    pass

WGPUTexelBufferView = ctypes.POINTER(struct_WGPUTexelBufferViewImpl)
class struct_WGPUTextureImpl(Structure):
    pass

WGPUTexture = ctypes.POINTER(struct_WGPUTextureImpl)
class struct_WGPUTextureViewImpl(Structure):
    pass

WGPUTextureView = ctypes.POINTER(struct_WGPUTextureViewImpl)
class struct_WGPUCommandEncoderImpl(Structure):
    pass

WGPUCommandEncoder = ctypes.POINTER(struct_WGPUCommandEncoderImpl)
class struct_WGPUComputePassEncoderImpl(Structure):
    pass

WGPUComputePassEncoder = ctypes.POINTER(struct_WGPUComputePassEncoderImpl)
class struct_WGPURenderBundleEncoderImpl(Structure):
    pass

WGPURenderBundleEncoder = ctypes.POINTER(struct_WGPURenderBundleEncoderImpl)
class struct_WGPURenderPassEncoderImpl(Structure):
    pass

WGPURenderPassEncoder = ctypes.POINTER(struct_WGPURenderPassEncoderImpl)

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
    0: 'WGPUBufferBindingType_BindingNotUsed',
    1: 'WGPUBufferBindingType_Undefined',
    2: 'WGPUBufferBindingType_Uniform',
    3: 'WGPUBufferBindingType_Storage',
    4: 'WGPUBufferBindingType_ReadOnlyStorage',
    2147483647: 'WGPUBufferBindingType_Force32',
}
WGPUBufferBindingType_BindingNotUsed = 0
WGPUBufferBindingType_Undefined = 1
WGPUBufferBindingType_Uniform = 2
WGPUBufferBindingType_Storage = 3
WGPUBufferBindingType_ReadOnlyStorage = 4
WGPUBufferBindingType_Force32 = 2147483647
WGPUBufferBindingType = ctypes.c_uint32 # enum

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
    1: 'WGPUCompilationInfoRequestStatus_Success',
    2: 'WGPUCompilationInfoRequestStatus_CallbackCancelled',
    2147483647: 'WGPUCompilationInfoRequestStatus_Force32',
}
WGPUCompilationInfoRequestStatus_Success = 1
WGPUCompilationInfoRequestStatus_CallbackCancelled = 2
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

# values for enumeration 'WGPUComponentSwizzle'
WGPUComponentSwizzle__enumvalues = {
    0: 'WGPUComponentSwizzle_Undefined',
    1: 'WGPUComponentSwizzle_Zero',
    2: 'WGPUComponentSwizzle_One',
    3: 'WGPUComponentSwizzle_R',
    4: 'WGPUComponentSwizzle_G',
    5: 'WGPUComponentSwizzle_B',
    6: 'WGPUComponentSwizzle_A',
    2147483647: 'WGPUComponentSwizzle_Force32',
}
WGPUComponentSwizzle_Undefined = 0
WGPUComponentSwizzle_Zero = 1
WGPUComponentSwizzle_One = 2
WGPUComponentSwizzle_R = 3
WGPUComponentSwizzle_G = 4
WGPUComponentSwizzle_B = 5
WGPUComponentSwizzle_A = 6
WGPUComponentSwizzle_Force32 = 2147483647
WGPUComponentSwizzle = ctypes.c_uint32 # enum

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
    1: 'WGPUCreatePipelineAsyncStatus_Success',
    2: 'WGPUCreatePipelineAsyncStatus_CallbackCancelled',
    3: 'WGPUCreatePipelineAsyncStatus_ValidationError',
    4: 'WGPUCreatePipelineAsyncStatus_InternalError',
    2147483647: 'WGPUCreatePipelineAsyncStatus_Force32',
}
WGPUCreatePipelineAsyncStatus_Success = 1
WGPUCreatePipelineAsyncStatus_CallbackCancelled = 2
WGPUCreatePipelineAsyncStatus_ValidationError = 3
WGPUCreatePipelineAsyncStatus_InternalError = 4
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
    3: 'WGPUDeviceLostReason_CallbackCancelled',
    4: 'WGPUDeviceLostReason_FailedCreation',
    2147483647: 'WGPUDeviceLostReason_Force32',
}
WGPUDeviceLostReason_Unknown = 1
WGPUDeviceLostReason_Destroyed = 2
WGPUDeviceLostReason_CallbackCancelled = 3
WGPUDeviceLostReason_FailedCreation = 4
WGPUDeviceLostReason_Force32 = 2147483647
WGPUDeviceLostReason = ctypes.c_uint32 # enum

# values for enumeration 'WGPUDynamicBindingKind'
WGPUDynamicBindingKind__enumvalues = {
    0: 'WGPUDynamicBindingKind_Undefined',
    1: 'WGPUDynamicBindingKind_SampledTexture',
    2147483647: 'WGPUDynamicBindingKind_Force32',
}
WGPUDynamicBindingKind_Undefined = 0
WGPUDynamicBindingKind_SampledTexture = 1
WGPUDynamicBindingKind_Force32 = 2147483647
WGPUDynamicBindingKind = ctypes.c_uint32 # enum

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
    1: 'WGPUErrorType_NoError',
    2: 'WGPUErrorType_Validation',
    3: 'WGPUErrorType_OutOfMemory',
    4: 'WGPUErrorType_Internal',
    5: 'WGPUErrorType_Unknown',
    2147483647: 'WGPUErrorType_Force32',
}
WGPUErrorType_NoError = 1
WGPUErrorType_Validation = 2
WGPUErrorType_OutOfMemory = 3
WGPUErrorType_Internal = 4
WGPUErrorType_Unknown = 5
WGPUErrorType_Force32 = 2147483647
WGPUErrorType = ctypes.c_uint32 # enum

# values for enumeration 'WGPUExternalTextureRotation'
WGPUExternalTextureRotation__enumvalues = {
    1: 'WGPUExternalTextureRotation_Rotate0Degrees',
    2: 'WGPUExternalTextureRotation_Rotate90Degrees',
    3: 'WGPUExternalTextureRotation_Rotate180Degrees',
    4: 'WGPUExternalTextureRotation_Rotate270Degrees',
    2147483647: 'WGPUExternalTextureRotation_Force32',
}
WGPUExternalTextureRotation_Rotate0Degrees = 1
WGPUExternalTextureRotation_Rotate90Degrees = 2
WGPUExternalTextureRotation_Rotate180Degrees = 3
WGPUExternalTextureRotation_Rotate270Degrees = 4
WGPUExternalTextureRotation_Force32 = 2147483647
WGPUExternalTextureRotation = ctypes.c_uint32 # enum

# values for enumeration 'WGPUFeatureLevel'
WGPUFeatureLevel__enumvalues = {
    0: 'WGPUFeatureLevel_Undefined',
    1: 'WGPUFeatureLevel_Compatibility',
    2: 'WGPUFeatureLevel_Core',
    2147483647: 'WGPUFeatureLevel_Force32',
}
WGPUFeatureLevel_Undefined = 0
WGPUFeatureLevel_Compatibility = 1
WGPUFeatureLevel_Core = 2
WGPUFeatureLevel_Force32 = 2147483647
WGPUFeatureLevel = ctypes.c_uint32 # enum

# values for enumeration 'WGPUFeatureName'
WGPUFeatureName__enumvalues = {
    1: 'WGPUFeatureName_CoreFeaturesAndLimits',
    2: 'WGPUFeatureName_DepthClipControl',
    3: 'WGPUFeatureName_Depth32FloatStencil8',
    4: 'WGPUFeatureName_TextureCompressionBC',
    5: 'WGPUFeatureName_TextureCompressionBCSliced3D',
    6: 'WGPUFeatureName_TextureCompressionETC2',
    7: 'WGPUFeatureName_TextureCompressionASTC',
    8: 'WGPUFeatureName_TextureCompressionASTCSliced3D',
    9: 'WGPUFeatureName_TimestampQuery',
    10: 'WGPUFeatureName_IndirectFirstInstance',
    11: 'WGPUFeatureName_ShaderF16',
    12: 'WGPUFeatureName_RG11B10UfloatRenderable',
    13: 'WGPUFeatureName_BGRA8UnormStorage',
    14: 'WGPUFeatureName_Float32Filterable',
    15: 'WGPUFeatureName_Float32Blendable',
    16: 'WGPUFeatureName_ClipDistances',
    17: 'WGPUFeatureName_DualSourceBlending',
    18: 'WGPUFeatureName_Subgroups',
    19: 'WGPUFeatureName_TextureFormatsTier1',
    20: 'WGPUFeatureName_TextureFormatsTier2',
    21: 'WGPUFeatureName_PrimitiveIndex',
    22: 'WGPUFeatureName_TextureComponentSwizzle',
    327680: 'WGPUFeatureName_DawnInternalUsages',
    327681: 'WGPUFeatureName_DawnMultiPlanarFormats',
    327682: 'WGPUFeatureName_DawnNative',
    327683: 'WGPUFeatureName_ChromiumExperimentalTimestampQueryInsidePasses',
    327684: 'WGPUFeatureName_ImplicitDeviceSynchronization',
    327686: 'WGPUFeatureName_TransientAttachments',
    327687: 'WGPUFeatureName_MSAARenderToSingleSampled',
    327688: 'WGPUFeatureName_D3D11MultithreadProtected',
    327689: 'WGPUFeatureName_ANGLETextureSharing',
    327690: 'WGPUFeatureName_PixelLocalStorageCoherent',
    327691: 'WGPUFeatureName_PixelLocalStorageNonCoherent',
    327692: 'WGPUFeatureName_Unorm16TextureFormats',
    327693: 'WGPUFeatureName_MultiPlanarFormatExtendedUsages',
    327694: 'WGPUFeatureName_MultiPlanarFormatP010',
    327695: 'WGPUFeatureName_HostMappedPointer',
    327696: 'WGPUFeatureName_MultiPlanarRenderTargets',
    327697: 'WGPUFeatureName_MultiPlanarFormatNv12a',
    327698: 'WGPUFeatureName_FramebufferFetch',
    327699: 'WGPUFeatureName_BufferMapExtendedUsages',
    327700: 'WGPUFeatureName_AdapterPropertiesMemoryHeaps',
    327701: 'WGPUFeatureName_AdapterPropertiesD3D',
    327702: 'WGPUFeatureName_AdapterPropertiesVk',
    327703: 'WGPUFeatureName_R8UnormStorage',
    327704: 'WGPUFeatureName_DawnFormatCapabilities',
    327705: 'WGPUFeatureName_DawnDrmFormatCapabilities',
    327706: 'WGPUFeatureName_MultiPlanarFormatNv16',
    327707: 'WGPUFeatureName_MultiPlanarFormatNv24',
    327708: 'WGPUFeatureName_MultiPlanarFormatP210',
    327709: 'WGPUFeatureName_MultiPlanarFormatP410',
    327710: 'WGPUFeatureName_SharedTextureMemoryVkDedicatedAllocation',
    327711: 'WGPUFeatureName_SharedTextureMemoryAHardwareBuffer',
    327712: 'WGPUFeatureName_SharedTextureMemoryDmaBuf',
    327713: 'WGPUFeatureName_SharedTextureMemoryOpaqueFD',
    327714: 'WGPUFeatureName_SharedTextureMemoryZirconHandle',
    327715: 'WGPUFeatureName_SharedTextureMemoryDXGISharedHandle',
    327716: 'WGPUFeatureName_SharedTextureMemoryD3D11Texture2D',
    327717: 'WGPUFeatureName_SharedTextureMemoryIOSurface',
    327718: 'WGPUFeatureName_SharedTextureMemoryEGLImage',
    327719: 'WGPUFeatureName_SharedFenceVkSemaphoreOpaqueFD',
    327720: 'WGPUFeatureName_SharedFenceSyncFD',
    327721: 'WGPUFeatureName_SharedFenceVkSemaphoreZirconHandle',
    327722: 'WGPUFeatureName_SharedFenceDXGISharedHandle',
    327723: 'WGPUFeatureName_SharedFenceMTLSharedEvent',
    327724: 'WGPUFeatureName_SharedBufferMemoryD3D12Resource',
    327725: 'WGPUFeatureName_StaticSamplers',
    327726: 'WGPUFeatureName_YCbCrVulkanSamplers',
    327727: 'WGPUFeatureName_ShaderModuleCompilationOptions',
    327728: 'WGPUFeatureName_DawnLoadResolveTexture',
    327729: 'WGPUFeatureName_DawnPartialLoadResolveTexture',
    327730: 'WGPUFeatureName_MultiDrawIndirect',
    327731: 'WGPUFeatureName_DawnTexelCopyBufferRowAlignment',
    327732: 'WGPUFeatureName_FlexibleTextureViews',
    327733: 'WGPUFeatureName_ChromiumExperimentalSubgroupMatrix',
    327734: 'WGPUFeatureName_SharedFenceEGLSync',
    327735: 'WGPUFeatureName_DawnDeviceAllocatorControl',
    327736: 'WGPUFeatureName_ChromiumExperimentalBindless',
    327737: 'WGPUFeatureName_AdapterPropertiesWGPU',
    327738: 'WGPUFeatureName_SharedBufferMemoryD3D12SharedMemoryFileMappingHandle',
    327739: 'WGPUFeatureName_SharedTextureMemoryD3D12Resource',
    327740: 'WGPUFeatureName_ChromiumExperimentalSamplingResourceTable',
    2147483647: 'WGPUFeatureName_Force32',
}
WGPUFeatureName_CoreFeaturesAndLimits = 1
WGPUFeatureName_DepthClipControl = 2
WGPUFeatureName_Depth32FloatStencil8 = 3
WGPUFeatureName_TextureCompressionBC = 4
WGPUFeatureName_TextureCompressionBCSliced3D = 5
WGPUFeatureName_TextureCompressionETC2 = 6
WGPUFeatureName_TextureCompressionASTC = 7
WGPUFeatureName_TextureCompressionASTCSliced3D = 8
WGPUFeatureName_TimestampQuery = 9
WGPUFeatureName_IndirectFirstInstance = 10
WGPUFeatureName_ShaderF16 = 11
WGPUFeatureName_RG11B10UfloatRenderable = 12
WGPUFeatureName_BGRA8UnormStorage = 13
WGPUFeatureName_Float32Filterable = 14
WGPUFeatureName_Float32Blendable = 15
WGPUFeatureName_ClipDistances = 16
WGPUFeatureName_DualSourceBlending = 17
WGPUFeatureName_Subgroups = 18
WGPUFeatureName_TextureFormatsTier1 = 19
WGPUFeatureName_TextureFormatsTier2 = 20
WGPUFeatureName_PrimitiveIndex = 21
WGPUFeatureName_TextureComponentSwizzle = 22
WGPUFeatureName_DawnInternalUsages = 327680
WGPUFeatureName_DawnMultiPlanarFormats = 327681
WGPUFeatureName_DawnNative = 327682
WGPUFeatureName_ChromiumExperimentalTimestampQueryInsidePasses = 327683
WGPUFeatureName_ImplicitDeviceSynchronization = 327684
WGPUFeatureName_TransientAttachments = 327686
WGPUFeatureName_MSAARenderToSingleSampled = 327687
WGPUFeatureName_D3D11MultithreadProtected = 327688
WGPUFeatureName_ANGLETextureSharing = 327689
WGPUFeatureName_PixelLocalStorageCoherent = 327690
WGPUFeatureName_PixelLocalStorageNonCoherent = 327691
WGPUFeatureName_Unorm16TextureFormats = 327692
WGPUFeatureName_MultiPlanarFormatExtendedUsages = 327693
WGPUFeatureName_MultiPlanarFormatP010 = 327694
WGPUFeatureName_HostMappedPointer = 327695
WGPUFeatureName_MultiPlanarRenderTargets = 327696
WGPUFeatureName_MultiPlanarFormatNv12a = 327697
WGPUFeatureName_FramebufferFetch = 327698
WGPUFeatureName_BufferMapExtendedUsages = 327699
WGPUFeatureName_AdapterPropertiesMemoryHeaps = 327700
WGPUFeatureName_AdapterPropertiesD3D = 327701
WGPUFeatureName_AdapterPropertiesVk = 327702
WGPUFeatureName_R8UnormStorage = 327703
WGPUFeatureName_DawnFormatCapabilities = 327704
WGPUFeatureName_DawnDrmFormatCapabilities = 327705
WGPUFeatureName_MultiPlanarFormatNv16 = 327706
WGPUFeatureName_MultiPlanarFormatNv24 = 327707
WGPUFeatureName_MultiPlanarFormatP210 = 327708
WGPUFeatureName_MultiPlanarFormatP410 = 327709
WGPUFeatureName_SharedTextureMemoryVkDedicatedAllocation = 327710
WGPUFeatureName_SharedTextureMemoryAHardwareBuffer = 327711
WGPUFeatureName_SharedTextureMemoryDmaBuf = 327712
WGPUFeatureName_SharedTextureMemoryOpaqueFD = 327713
WGPUFeatureName_SharedTextureMemoryZirconHandle = 327714
WGPUFeatureName_SharedTextureMemoryDXGISharedHandle = 327715
WGPUFeatureName_SharedTextureMemoryD3D11Texture2D = 327716
WGPUFeatureName_SharedTextureMemoryIOSurface = 327717
WGPUFeatureName_SharedTextureMemoryEGLImage = 327718
WGPUFeatureName_SharedFenceVkSemaphoreOpaqueFD = 327719
WGPUFeatureName_SharedFenceSyncFD = 327720
WGPUFeatureName_SharedFenceVkSemaphoreZirconHandle = 327721
WGPUFeatureName_SharedFenceDXGISharedHandle = 327722
WGPUFeatureName_SharedFenceMTLSharedEvent = 327723
WGPUFeatureName_SharedBufferMemoryD3D12Resource = 327724
WGPUFeatureName_StaticSamplers = 327725
WGPUFeatureName_YCbCrVulkanSamplers = 327726
WGPUFeatureName_ShaderModuleCompilationOptions = 327727
WGPUFeatureName_DawnLoadResolveTexture = 327728
WGPUFeatureName_DawnPartialLoadResolveTexture = 327729
WGPUFeatureName_MultiDrawIndirect = 327730
WGPUFeatureName_DawnTexelCopyBufferRowAlignment = 327731
WGPUFeatureName_FlexibleTextureViews = 327732
WGPUFeatureName_ChromiumExperimentalSubgroupMatrix = 327733
WGPUFeatureName_SharedFenceEGLSync = 327734
WGPUFeatureName_DawnDeviceAllocatorControl = 327735
WGPUFeatureName_ChromiumExperimentalBindless = 327736
WGPUFeatureName_AdapterPropertiesWGPU = 327737
WGPUFeatureName_SharedBufferMemoryD3D12SharedMemoryFileMappingHandle = 327738
WGPUFeatureName_SharedTextureMemoryD3D12Resource = 327739
WGPUFeatureName_ChromiumExperimentalSamplingResourceTable = 327740
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

# values for enumeration 'WGPUInstanceFeatureName'
WGPUInstanceFeatureName__enumvalues = {
    1: 'WGPUInstanceFeatureName_TimedWaitAny',
    2: 'WGPUInstanceFeatureName_ShaderSourceSPIRV',
    3: 'WGPUInstanceFeatureName_MultipleDevicesPerAdapter',
    2147483647: 'WGPUInstanceFeatureName_Force32',
}
WGPUInstanceFeatureName_TimedWaitAny = 1
WGPUInstanceFeatureName_ShaderSourceSPIRV = 2
WGPUInstanceFeatureName_MultipleDevicesPerAdapter = 3
WGPUInstanceFeatureName_Force32 = 2147483647
WGPUInstanceFeatureName = ctypes.c_uint32 # enum

# values for enumeration 'WGPULoadOp'
WGPULoadOp__enumvalues = {
    0: 'WGPULoadOp_Undefined',
    1: 'WGPULoadOp_Load',
    2: 'WGPULoadOp_Clear',
    327683: 'WGPULoadOp_ExpandResolveTexture',
    2147483647: 'WGPULoadOp_Force32',
}
WGPULoadOp_Undefined = 0
WGPULoadOp_Load = 1
WGPULoadOp_Clear = 2
WGPULoadOp_ExpandResolveTexture = 327683
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
    1: 'WGPUMapAsyncStatus_Success',
    2: 'WGPUMapAsyncStatus_CallbackCancelled',
    3: 'WGPUMapAsyncStatus_Error',
    4: 'WGPUMapAsyncStatus_Aborted',
    2147483647: 'WGPUMapAsyncStatus_Force32',
}
WGPUMapAsyncStatus_Success = 1
WGPUMapAsyncStatus_CallbackCancelled = 2
WGPUMapAsyncStatus_Error = 3
WGPUMapAsyncStatus_Aborted = 4
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

# values for enumeration 'WGPUOptionalBool'
WGPUOptionalBool__enumvalues = {
    0: 'WGPUOptionalBool_False',
    1: 'WGPUOptionalBool_True',
    2: 'WGPUOptionalBool_Undefined',
    2147483647: 'WGPUOptionalBool_Force32',
}
WGPUOptionalBool_False = 0
WGPUOptionalBool_True = 1
WGPUOptionalBool_Undefined = 2
WGPUOptionalBool_Force32 = 2147483647
WGPUOptionalBool = ctypes.c_uint32 # enum

# values for enumeration 'WGPUPopErrorScopeStatus'
WGPUPopErrorScopeStatus__enumvalues = {
    1: 'WGPUPopErrorScopeStatus_Success',
    2: 'WGPUPopErrorScopeStatus_CallbackCancelled',
    3: 'WGPUPopErrorScopeStatus_Error',
    2147483647: 'WGPUPopErrorScopeStatus_Force32',
}
WGPUPopErrorScopeStatus_Success = 1
WGPUPopErrorScopeStatus_CallbackCancelled = 2
WGPUPopErrorScopeStatus_Error = 3
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

# values for enumeration 'WGPUPredefinedColorSpace'
WGPUPredefinedColorSpace__enumvalues = {
    1: 'WGPUPredefinedColorSpace_SRGB',
    2: 'WGPUPredefinedColorSpace_DisplayP3',
    2147483647: 'WGPUPredefinedColorSpace_Force32',
}
WGPUPredefinedColorSpace_SRGB = 1
WGPUPredefinedColorSpace_DisplayP3 = 2
WGPUPredefinedColorSpace_Force32 = 2147483647
WGPUPredefinedColorSpace = ctypes.c_uint32 # enum

# values for enumeration 'WGPUPresentMode'
WGPUPresentMode__enumvalues = {
    0: 'WGPUPresentMode_Undefined',
    1: 'WGPUPresentMode_Fifo',
    2: 'WGPUPresentMode_FifoRelaxed',
    3: 'WGPUPresentMode_Immediate',
    4: 'WGPUPresentMode_Mailbox',
    2147483647: 'WGPUPresentMode_Force32',
}
WGPUPresentMode_Undefined = 0
WGPUPresentMode_Fifo = 1
WGPUPresentMode_FifoRelaxed = 2
WGPUPresentMode_Immediate = 3
WGPUPresentMode_Mailbox = 4
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
    1: 'WGPUQueueWorkDoneStatus_Success',
    2: 'WGPUQueueWorkDoneStatus_CallbackCancelled',
    3: 'WGPUQueueWorkDoneStatus_Error',
    2147483647: 'WGPUQueueWorkDoneStatus_Force32',
}
WGPUQueueWorkDoneStatus_Success = 1
WGPUQueueWorkDoneStatus_CallbackCancelled = 2
WGPUQueueWorkDoneStatus_Error = 3
WGPUQueueWorkDoneStatus_Force32 = 2147483647
WGPUQueueWorkDoneStatus = ctypes.c_uint32 # enum

# values for enumeration 'WGPURequestAdapterStatus'
WGPURequestAdapterStatus__enumvalues = {
    1: 'WGPURequestAdapterStatus_Success',
    2: 'WGPURequestAdapterStatus_CallbackCancelled',
    3: 'WGPURequestAdapterStatus_Unavailable',
    4: 'WGPURequestAdapterStatus_Error',
    2147483647: 'WGPURequestAdapterStatus_Force32',
}
WGPURequestAdapterStatus_Success = 1
WGPURequestAdapterStatus_CallbackCancelled = 2
WGPURequestAdapterStatus_Unavailable = 3
WGPURequestAdapterStatus_Error = 4
WGPURequestAdapterStatus_Force32 = 2147483647
WGPURequestAdapterStatus = ctypes.c_uint32 # enum

# values for enumeration 'WGPURequestDeviceStatus'
WGPURequestDeviceStatus__enumvalues = {
    1: 'WGPURequestDeviceStatus_Success',
    2: 'WGPURequestDeviceStatus_CallbackCancelled',
    3: 'WGPURequestDeviceStatus_Error',
    2147483647: 'WGPURequestDeviceStatus_Force32',
}
WGPURequestDeviceStatus_Success = 1
WGPURequestDeviceStatus_CallbackCancelled = 2
WGPURequestDeviceStatus_Error = 3
WGPURequestDeviceStatus_Force32 = 2147483647
WGPURequestDeviceStatus = ctypes.c_uint32 # enum

# values for enumeration 'WGPUSamplerBindingType'
WGPUSamplerBindingType__enumvalues = {
    0: 'WGPUSamplerBindingType_BindingNotUsed',
    1: 'WGPUSamplerBindingType_Undefined',
    2: 'WGPUSamplerBindingType_Filtering',
    3: 'WGPUSamplerBindingType_NonFiltering',
    4: 'WGPUSamplerBindingType_Comparison',
    2147483647: 'WGPUSamplerBindingType_Force32',
}
WGPUSamplerBindingType_BindingNotUsed = 0
WGPUSamplerBindingType_Undefined = 1
WGPUSamplerBindingType_Filtering = 2
WGPUSamplerBindingType_NonFiltering = 3
WGPUSamplerBindingType_Comparison = 4
WGPUSamplerBindingType_Force32 = 2147483647
WGPUSamplerBindingType = ctypes.c_uint32 # enum

# values for enumeration 'WGPUSharedFenceType'
WGPUSharedFenceType__enumvalues = {
    1: 'WGPUSharedFenceType_VkSemaphoreOpaqueFD',
    2: 'WGPUSharedFenceType_SyncFD',
    3: 'WGPUSharedFenceType_VkSemaphoreZirconHandle',
    4: 'WGPUSharedFenceType_DXGISharedHandle',
    5: 'WGPUSharedFenceType_MTLSharedEvent',
    6: 'WGPUSharedFenceType_EGLSync',
    2147483647: 'WGPUSharedFenceType_Force32',
}
WGPUSharedFenceType_VkSemaphoreOpaqueFD = 1
WGPUSharedFenceType_SyncFD = 2
WGPUSharedFenceType_VkSemaphoreZirconHandle = 3
WGPUSharedFenceType_DXGISharedHandle = 4
WGPUSharedFenceType_MTLSharedEvent = 5
WGPUSharedFenceType_EGLSync = 6
WGPUSharedFenceType_Force32 = 2147483647
WGPUSharedFenceType = ctypes.c_uint32 # enum

# values for enumeration 'WGPUStatus'
WGPUStatus__enumvalues = {
    1: 'WGPUStatus_Success',
    2: 'WGPUStatus_Error',
    2147483647: 'WGPUStatus_Force32',
}
WGPUStatus_Success = 1
WGPUStatus_Error = 2
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
    0: 'WGPUStorageTextureAccess_BindingNotUsed',
    1: 'WGPUStorageTextureAccess_Undefined',
    2: 'WGPUStorageTextureAccess_WriteOnly',
    3: 'WGPUStorageTextureAccess_ReadOnly',
    4: 'WGPUStorageTextureAccess_ReadWrite',
    2147483647: 'WGPUStorageTextureAccess_Force32',
}
WGPUStorageTextureAccess_BindingNotUsed = 0
WGPUStorageTextureAccess_Undefined = 1
WGPUStorageTextureAccess_WriteOnly = 2
WGPUStorageTextureAccess_ReadOnly = 3
WGPUStorageTextureAccess_ReadWrite = 4
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

# values for enumeration 'WGPUSType'
WGPUSType__enumvalues = {
    1: 'WGPUSType_ShaderSourceSPIRV',
    2: 'WGPUSType_ShaderSourceWGSL',
    3: 'WGPUSType_RenderPassMaxDrawCount',
    4: 'WGPUSType_SurfaceSourceMetalLayer',
    5: 'WGPUSType_SurfaceSourceWindowsHWND',
    6: 'WGPUSType_SurfaceSourceXlibWindow',
    7: 'WGPUSType_SurfaceSourceWaylandSurface',
    8: 'WGPUSType_SurfaceSourceAndroidNativeWindow',
    9: 'WGPUSType_SurfaceSourceXCBWindow',
    10: 'WGPUSType_SurfaceColorManagement',
    11: 'WGPUSType_RequestAdapterWebXROptions',
    12: 'WGPUSType_TextureComponentSwizzleDescriptor',
    131072: 'WGPUSType_CompatibilityModeLimits',
    131073: 'WGPUSType_TextureBindingViewDimensionDescriptor',
    262144: 'WGPUSType_EmscriptenSurfaceSourceCanvasHTMLSelector',
    327680: 'WGPUSType_SurfaceDescriptorFromWindowsCoreWindow',
    327681: 'WGPUSType_ExternalTextureBindingEntry',
    327682: 'WGPUSType_ExternalTextureBindingLayout',
    327683: 'WGPUSType_SurfaceDescriptorFromWindowsUWPSwapChainPanel',
    327684: 'WGPUSType_DawnTextureInternalUsageDescriptor',
    327685: 'WGPUSType_DawnEncoderInternalUsageDescriptor',
    327686: 'WGPUSType_DawnInstanceDescriptor',
    327687: 'WGPUSType_DawnCacheDeviceDescriptor',
    327688: 'WGPUSType_DawnAdapterPropertiesPowerPreference',
    327689: 'WGPUSType_DawnBufferDescriptorErrorInfoFromWireClient',
    327690: 'WGPUSType_DawnTogglesDescriptor',
    327691: 'WGPUSType_DawnShaderModuleSPIRVOptionsDescriptor',
    327692: 'WGPUSType_RequestAdapterOptionsLUID',
    327693: 'WGPUSType_RequestAdapterOptionsGetGLProc',
    327694: 'WGPUSType_RequestAdapterOptionsD3D11Device',
    327695: 'WGPUSType_DawnRenderPassColorAttachmentRenderToSingleSampled',
    327696: 'WGPUSType_RenderPassPixelLocalStorage',
    327697: 'WGPUSType_PipelineLayoutPixelLocalStorage',
    327698: 'WGPUSType_BufferHostMappedPointer',
    327699: 'WGPUSType_AdapterPropertiesMemoryHeaps',
    327700: 'WGPUSType_AdapterPropertiesD3D',
    327701: 'WGPUSType_AdapterPropertiesVk',
    327702: 'WGPUSType_DawnWireWGSLControl',
    327703: 'WGPUSType_DawnWGSLBlocklist',
    327704: 'WGPUSType_DawnDrmFormatCapabilities',
    327705: 'WGPUSType_ShaderModuleCompilationOptions',
    327706: 'WGPUSType_ColorTargetStateExpandResolveTextureDawn',
    327707: 'WGPUSType_RenderPassDescriptorExpandResolveRect',
    327708: 'WGPUSType_SharedTextureMemoryVkDedicatedAllocationDescriptor',
    327709: 'WGPUSType_SharedTextureMemoryAHardwareBufferDescriptor',
    327710: 'WGPUSType_SharedTextureMemoryDmaBufDescriptor',
    327711: 'WGPUSType_SharedTextureMemoryOpaqueFDDescriptor',
    327712: 'WGPUSType_SharedTextureMemoryZirconHandleDescriptor',
    327713: 'WGPUSType_SharedTextureMemoryDXGISharedHandleDescriptor',
    327714: 'WGPUSType_SharedTextureMemoryD3D11Texture2DDescriptor',
    327715: 'WGPUSType_SharedTextureMemoryIOSurfaceDescriptor',
    327716: 'WGPUSType_SharedTextureMemoryEGLImageDescriptor',
    327717: 'WGPUSType_SharedTextureMemoryInitializedBeginState',
    327718: 'WGPUSType_SharedTextureMemoryInitializedEndState',
    327719: 'WGPUSType_SharedTextureMemoryVkImageLayoutBeginState',
    327720: 'WGPUSType_SharedTextureMemoryVkImageLayoutEndState',
    327721: 'WGPUSType_SharedTextureMemoryD3DSwapchainBeginState',
    327722: 'WGPUSType_SharedFenceVkSemaphoreOpaqueFDDescriptor',
    327723: 'WGPUSType_SharedFenceVkSemaphoreOpaqueFDExportInfo',
    327724: 'WGPUSType_SharedFenceSyncFDDescriptor',
    327725: 'WGPUSType_SharedFenceSyncFDExportInfo',
    327726: 'WGPUSType_SharedFenceVkSemaphoreZirconHandleDescriptor',
    327727: 'WGPUSType_SharedFenceVkSemaphoreZirconHandleExportInfo',
    327728: 'WGPUSType_SharedFenceDXGISharedHandleDescriptor',
    327729: 'WGPUSType_SharedFenceDXGISharedHandleExportInfo',
    327730: 'WGPUSType_SharedFenceMTLSharedEventDescriptor',
    327731: 'WGPUSType_SharedFenceMTLSharedEventExportInfo',
    327732: 'WGPUSType_SharedBufferMemoryD3D12ResourceDescriptor',
    327733: 'WGPUSType_StaticSamplerBindingLayout',
    327734: 'WGPUSType_YCbCrVkDescriptor',
    327735: 'WGPUSType_SharedTextureMemoryAHardwareBufferProperties',
    327736: 'WGPUSType_AHardwareBufferProperties',
    327738: 'WGPUSType_DawnTexelCopyBufferRowAlignmentLimits',
    327739: 'WGPUSType_AdapterPropertiesSubgroupMatrixConfigs',
    327740: 'WGPUSType_SharedFenceEGLSyncDescriptor',
    327741: 'WGPUSType_SharedFenceEGLSyncExportInfo',
    327742: 'WGPUSType_DawnInjectedInvalidSType',
    327743: 'WGPUSType_DawnCompilationMessageUtf16',
    327744: 'WGPUSType_DawnFakeBufferOOMForTesting',
    327745: 'WGPUSType_SurfaceDescriptorFromWindowsWinUISwapChainPanel',
    327746: 'WGPUSType_DawnDeviceAllocatorControl',
    327747: 'WGPUSType_DawnHostMappedPointerLimits',
    327748: 'WGPUSType_RenderPassDescriptorResolveRect',
    327749: 'WGPUSType_RequestAdapterWebGPUBackendOptions',
    327750: 'WGPUSType_DawnFakeDeviceInitializeErrorForTesting',
    327751: 'WGPUSType_SharedTextureMemoryD3D11BeginState',
    327752: 'WGPUSType_DawnConsumeAdapterDescriptor',
    327753: 'WGPUSType_BindGroupLayoutDynamicBindingArray',
    327754: 'WGPUSType_DynamicBindingArrayLimits',
    327755: 'WGPUSType_BindGroupDynamicBindingArray',
    327756: 'WGPUSType_TexelBufferBindingEntry',
    327757: 'WGPUSType_TexelBufferBindingLayout',
    327758: 'WGPUSType_SharedTextureMemoryMetalEndAccessState',
    327759: 'WGPUSType_AdapterPropertiesWGPU',
    327760: 'WGPUSType_SharedBufferMemoryD3D12SharedMemoryFileMappingHandleDescriptor',
    327761: 'WGPUSType_SharedTextureMemoryD3D12ResourceDescriptor',
    327762: 'WGPUSType_RequestAdapterOptionsAngleVirtualizationGroup',
    327763: 'WGPUSType_ResourceTableLimits',
    327764: 'WGPUSType_PipelineLayoutResourceTable',
    2147483647: 'WGPUSType_Force32',
}
WGPUSType_ShaderSourceSPIRV = 1
WGPUSType_ShaderSourceWGSL = 2
WGPUSType_RenderPassMaxDrawCount = 3
WGPUSType_SurfaceSourceMetalLayer = 4
WGPUSType_SurfaceSourceWindowsHWND = 5
WGPUSType_SurfaceSourceXlibWindow = 6
WGPUSType_SurfaceSourceWaylandSurface = 7
WGPUSType_SurfaceSourceAndroidNativeWindow = 8
WGPUSType_SurfaceSourceXCBWindow = 9
WGPUSType_SurfaceColorManagement = 10
WGPUSType_RequestAdapterWebXROptions = 11
WGPUSType_TextureComponentSwizzleDescriptor = 12
WGPUSType_CompatibilityModeLimits = 131072
WGPUSType_TextureBindingViewDimensionDescriptor = 131073
WGPUSType_EmscriptenSurfaceSourceCanvasHTMLSelector = 262144
WGPUSType_SurfaceDescriptorFromWindowsCoreWindow = 327680
WGPUSType_ExternalTextureBindingEntry = 327681
WGPUSType_ExternalTextureBindingLayout = 327682
WGPUSType_SurfaceDescriptorFromWindowsUWPSwapChainPanel = 327683
WGPUSType_DawnTextureInternalUsageDescriptor = 327684
WGPUSType_DawnEncoderInternalUsageDescriptor = 327685
WGPUSType_DawnInstanceDescriptor = 327686
WGPUSType_DawnCacheDeviceDescriptor = 327687
WGPUSType_DawnAdapterPropertiesPowerPreference = 327688
WGPUSType_DawnBufferDescriptorErrorInfoFromWireClient = 327689
WGPUSType_DawnTogglesDescriptor = 327690
WGPUSType_DawnShaderModuleSPIRVOptionsDescriptor = 327691
WGPUSType_RequestAdapterOptionsLUID = 327692
WGPUSType_RequestAdapterOptionsGetGLProc = 327693
WGPUSType_RequestAdapterOptionsD3D11Device = 327694
WGPUSType_DawnRenderPassColorAttachmentRenderToSingleSampled = 327695
WGPUSType_RenderPassPixelLocalStorage = 327696
WGPUSType_PipelineLayoutPixelLocalStorage = 327697
WGPUSType_BufferHostMappedPointer = 327698
WGPUSType_AdapterPropertiesMemoryHeaps = 327699
WGPUSType_AdapterPropertiesD3D = 327700
WGPUSType_AdapterPropertiesVk = 327701
WGPUSType_DawnWireWGSLControl = 327702
WGPUSType_DawnWGSLBlocklist = 327703
WGPUSType_DawnDrmFormatCapabilities = 327704
WGPUSType_ShaderModuleCompilationOptions = 327705
WGPUSType_ColorTargetStateExpandResolveTextureDawn = 327706
WGPUSType_RenderPassDescriptorExpandResolveRect = 327707
WGPUSType_SharedTextureMemoryVkDedicatedAllocationDescriptor = 327708
WGPUSType_SharedTextureMemoryAHardwareBufferDescriptor = 327709
WGPUSType_SharedTextureMemoryDmaBufDescriptor = 327710
WGPUSType_SharedTextureMemoryOpaqueFDDescriptor = 327711
WGPUSType_SharedTextureMemoryZirconHandleDescriptor = 327712
WGPUSType_SharedTextureMemoryDXGISharedHandleDescriptor = 327713
WGPUSType_SharedTextureMemoryD3D11Texture2DDescriptor = 327714
WGPUSType_SharedTextureMemoryIOSurfaceDescriptor = 327715
WGPUSType_SharedTextureMemoryEGLImageDescriptor = 327716
WGPUSType_SharedTextureMemoryInitializedBeginState = 327717
WGPUSType_SharedTextureMemoryInitializedEndState = 327718
WGPUSType_SharedTextureMemoryVkImageLayoutBeginState = 327719
WGPUSType_SharedTextureMemoryVkImageLayoutEndState = 327720
WGPUSType_SharedTextureMemoryD3DSwapchainBeginState = 327721
WGPUSType_SharedFenceVkSemaphoreOpaqueFDDescriptor = 327722
WGPUSType_SharedFenceVkSemaphoreOpaqueFDExportInfo = 327723
WGPUSType_SharedFenceSyncFDDescriptor = 327724
WGPUSType_SharedFenceSyncFDExportInfo = 327725
WGPUSType_SharedFenceVkSemaphoreZirconHandleDescriptor = 327726
WGPUSType_SharedFenceVkSemaphoreZirconHandleExportInfo = 327727
WGPUSType_SharedFenceDXGISharedHandleDescriptor = 327728
WGPUSType_SharedFenceDXGISharedHandleExportInfo = 327729
WGPUSType_SharedFenceMTLSharedEventDescriptor = 327730
WGPUSType_SharedFenceMTLSharedEventExportInfo = 327731
WGPUSType_SharedBufferMemoryD3D12ResourceDescriptor = 327732
WGPUSType_StaticSamplerBindingLayout = 327733
WGPUSType_YCbCrVkDescriptor = 327734
WGPUSType_SharedTextureMemoryAHardwareBufferProperties = 327735
WGPUSType_AHardwareBufferProperties = 327736
WGPUSType_DawnTexelCopyBufferRowAlignmentLimits = 327738
WGPUSType_AdapterPropertiesSubgroupMatrixConfigs = 327739
WGPUSType_SharedFenceEGLSyncDescriptor = 327740
WGPUSType_SharedFenceEGLSyncExportInfo = 327741
WGPUSType_DawnInjectedInvalidSType = 327742
WGPUSType_DawnCompilationMessageUtf16 = 327743
WGPUSType_DawnFakeBufferOOMForTesting = 327744
WGPUSType_SurfaceDescriptorFromWindowsWinUISwapChainPanel = 327745
WGPUSType_DawnDeviceAllocatorControl = 327746
WGPUSType_DawnHostMappedPointerLimits = 327747
WGPUSType_RenderPassDescriptorResolveRect = 327748
WGPUSType_RequestAdapterWebGPUBackendOptions = 327749
WGPUSType_DawnFakeDeviceInitializeErrorForTesting = 327750
WGPUSType_SharedTextureMemoryD3D11BeginState = 327751
WGPUSType_DawnConsumeAdapterDescriptor = 327752
WGPUSType_BindGroupLayoutDynamicBindingArray = 327753
WGPUSType_DynamicBindingArrayLimits = 327754
WGPUSType_BindGroupDynamicBindingArray = 327755
WGPUSType_TexelBufferBindingEntry = 327756
WGPUSType_TexelBufferBindingLayout = 327757
WGPUSType_SharedTextureMemoryMetalEndAccessState = 327758
WGPUSType_AdapterPropertiesWGPU = 327759
WGPUSType_SharedBufferMemoryD3D12SharedMemoryFileMappingHandleDescriptor = 327760
WGPUSType_SharedTextureMemoryD3D12ResourceDescriptor = 327761
WGPUSType_RequestAdapterOptionsAngleVirtualizationGroup = 327762
WGPUSType_ResourceTableLimits = 327763
WGPUSType_PipelineLayoutResourceTable = 327764
WGPUSType_Force32 = 2147483647
WGPUSType = ctypes.c_uint32 # enum

# values for enumeration 'WGPUSubgroupMatrixComponentType'
WGPUSubgroupMatrixComponentType__enumvalues = {
    1: 'WGPUSubgroupMatrixComponentType_F32',
    2: 'WGPUSubgroupMatrixComponentType_F16',
    3: 'WGPUSubgroupMatrixComponentType_U32',
    4: 'WGPUSubgroupMatrixComponentType_I32',
    5: 'WGPUSubgroupMatrixComponentType_U8',
    6: 'WGPUSubgroupMatrixComponentType_I8',
    2147483647: 'WGPUSubgroupMatrixComponentType_Force32',
}
WGPUSubgroupMatrixComponentType_F32 = 1
WGPUSubgroupMatrixComponentType_F16 = 2
WGPUSubgroupMatrixComponentType_U32 = 3
WGPUSubgroupMatrixComponentType_I32 = 4
WGPUSubgroupMatrixComponentType_U8 = 5
WGPUSubgroupMatrixComponentType_I8 = 6
WGPUSubgroupMatrixComponentType_Force32 = 2147483647
WGPUSubgroupMatrixComponentType = ctypes.c_uint32 # enum

# values for enumeration 'WGPUSurfaceGetCurrentTextureStatus'
WGPUSurfaceGetCurrentTextureStatus__enumvalues = {
    1: 'WGPUSurfaceGetCurrentTextureStatus_SuccessOptimal',
    2: 'WGPUSurfaceGetCurrentTextureStatus_SuccessSuboptimal',
    3: 'WGPUSurfaceGetCurrentTextureStatus_Timeout',
    4: 'WGPUSurfaceGetCurrentTextureStatus_Outdated',
    5: 'WGPUSurfaceGetCurrentTextureStatus_Lost',
    6: 'WGPUSurfaceGetCurrentTextureStatus_Error',
    2147483647: 'WGPUSurfaceGetCurrentTextureStatus_Force32',
}
WGPUSurfaceGetCurrentTextureStatus_SuccessOptimal = 1
WGPUSurfaceGetCurrentTextureStatus_SuccessSuboptimal = 2
WGPUSurfaceGetCurrentTextureStatus_Timeout = 3
WGPUSurfaceGetCurrentTextureStatus_Outdated = 4
WGPUSurfaceGetCurrentTextureStatus_Lost = 5
WGPUSurfaceGetCurrentTextureStatus_Error = 6
WGPUSurfaceGetCurrentTextureStatus_Force32 = 2147483647
WGPUSurfaceGetCurrentTextureStatus = ctypes.c_uint32 # enum

# values for enumeration 'WGPUTexelBufferAccess'
WGPUTexelBufferAccess__enumvalues = {
    0: 'WGPUTexelBufferAccess_Undefined',
    1: 'WGPUTexelBufferAccess_ReadOnly',
    2: 'WGPUTexelBufferAccess_ReadWrite',
    2147483647: 'WGPUTexelBufferAccess_Force32',
}
WGPUTexelBufferAccess_Undefined = 0
WGPUTexelBufferAccess_ReadOnly = 1
WGPUTexelBufferAccess_ReadWrite = 2
WGPUTexelBufferAccess_Force32 = 2147483647
WGPUTexelBufferAccess = ctypes.c_uint32 # enum

# values for enumeration 'WGPUTextureAspect'
WGPUTextureAspect__enumvalues = {
    0: 'WGPUTextureAspect_Undefined',
    1: 'WGPUTextureAspect_All',
    2: 'WGPUTextureAspect_StencilOnly',
    3: 'WGPUTextureAspect_DepthOnly',
    327680: 'WGPUTextureAspect_Plane0Only',
    327681: 'WGPUTextureAspect_Plane1Only',
    327682: 'WGPUTextureAspect_Plane2Only',
    2147483647: 'WGPUTextureAspect_Force32',
}
WGPUTextureAspect_Undefined = 0
WGPUTextureAspect_All = 1
WGPUTextureAspect_StencilOnly = 2
WGPUTextureAspect_DepthOnly = 3
WGPUTextureAspect_Plane0Only = 327680
WGPUTextureAspect_Plane1Only = 327681
WGPUTextureAspect_Plane2Only = 327682
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
    5: 'WGPUTextureFormat_R16Unorm',
    6: 'WGPUTextureFormat_R16Snorm',
    7: 'WGPUTextureFormat_R16Uint',
    8: 'WGPUTextureFormat_R16Sint',
    9: 'WGPUTextureFormat_R16Float',
    10: 'WGPUTextureFormat_RG8Unorm',
    11: 'WGPUTextureFormat_RG8Snorm',
    12: 'WGPUTextureFormat_RG8Uint',
    13: 'WGPUTextureFormat_RG8Sint',
    14: 'WGPUTextureFormat_R32Float',
    15: 'WGPUTextureFormat_R32Uint',
    16: 'WGPUTextureFormat_R32Sint',
    17: 'WGPUTextureFormat_RG16Unorm',
    18: 'WGPUTextureFormat_RG16Snorm',
    19: 'WGPUTextureFormat_RG16Uint',
    20: 'WGPUTextureFormat_RG16Sint',
    21: 'WGPUTextureFormat_RG16Float',
    22: 'WGPUTextureFormat_RGBA8Unorm',
    23: 'WGPUTextureFormat_RGBA8UnormSrgb',
    24: 'WGPUTextureFormat_RGBA8Snorm',
    25: 'WGPUTextureFormat_RGBA8Uint',
    26: 'WGPUTextureFormat_RGBA8Sint',
    27: 'WGPUTextureFormat_BGRA8Unorm',
    28: 'WGPUTextureFormat_BGRA8UnormSrgb',
    29: 'WGPUTextureFormat_RGB10A2Uint',
    30: 'WGPUTextureFormat_RGB10A2Unorm',
    31: 'WGPUTextureFormat_RG11B10Ufloat',
    32: 'WGPUTextureFormat_RGB9E5Ufloat',
    33: 'WGPUTextureFormat_RG32Float',
    34: 'WGPUTextureFormat_RG32Uint',
    35: 'WGPUTextureFormat_RG32Sint',
    36: 'WGPUTextureFormat_RGBA16Unorm',
    37: 'WGPUTextureFormat_RGBA16Snorm',
    38: 'WGPUTextureFormat_RGBA16Uint',
    39: 'WGPUTextureFormat_RGBA16Sint',
    40: 'WGPUTextureFormat_RGBA16Float',
    41: 'WGPUTextureFormat_RGBA32Float',
    42: 'WGPUTextureFormat_RGBA32Uint',
    43: 'WGPUTextureFormat_RGBA32Sint',
    44: 'WGPUTextureFormat_Stencil8',
    45: 'WGPUTextureFormat_Depth16Unorm',
    46: 'WGPUTextureFormat_Depth24Plus',
    47: 'WGPUTextureFormat_Depth24PlusStencil8',
    48: 'WGPUTextureFormat_Depth32Float',
    49: 'WGPUTextureFormat_Depth32FloatStencil8',
    50: 'WGPUTextureFormat_BC1RGBAUnorm',
    51: 'WGPUTextureFormat_BC1RGBAUnormSrgb',
    52: 'WGPUTextureFormat_BC2RGBAUnorm',
    53: 'WGPUTextureFormat_BC2RGBAUnormSrgb',
    54: 'WGPUTextureFormat_BC3RGBAUnorm',
    55: 'WGPUTextureFormat_BC3RGBAUnormSrgb',
    56: 'WGPUTextureFormat_BC4RUnorm',
    57: 'WGPUTextureFormat_BC4RSnorm',
    58: 'WGPUTextureFormat_BC5RGUnorm',
    59: 'WGPUTextureFormat_BC5RGSnorm',
    60: 'WGPUTextureFormat_BC6HRGBUfloat',
    61: 'WGPUTextureFormat_BC6HRGBFloat',
    62: 'WGPUTextureFormat_BC7RGBAUnorm',
    63: 'WGPUTextureFormat_BC7RGBAUnormSrgb',
    64: 'WGPUTextureFormat_ETC2RGB8Unorm',
    65: 'WGPUTextureFormat_ETC2RGB8UnormSrgb',
    66: 'WGPUTextureFormat_ETC2RGB8A1Unorm',
    67: 'WGPUTextureFormat_ETC2RGB8A1UnormSrgb',
    68: 'WGPUTextureFormat_ETC2RGBA8Unorm',
    69: 'WGPUTextureFormat_ETC2RGBA8UnormSrgb',
    70: 'WGPUTextureFormat_EACR11Unorm',
    71: 'WGPUTextureFormat_EACR11Snorm',
    72: 'WGPUTextureFormat_EACRG11Unorm',
    73: 'WGPUTextureFormat_EACRG11Snorm',
    74: 'WGPUTextureFormat_ASTC4x4Unorm',
    75: 'WGPUTextureFormat_ASTC4x4UnormSrgb',
    76: 'WGPUTextureFormat_ASTC5x4Unorm',
    77: 'WGPUTextureFormat_ASTC5x4UnormSrgb',
    78: 'WGPUTextureFormat_ASTC5x5Unorm',
    79: 'WGPUTextureFormat_ASTC5x5UnormSrgb',
    80: 'WGPUTextureFormat_ASTC6x5Unorm',
    81: 'WGPUTextureFormat_ASTC6x5UnormSrgb',
    82: 'WGPUTextureFormat_ASTC6x6Unorm',
    83: 'WGPUTextureFormat_ASTC6x6UnormSrgb',
    84: 'WGPUTextureFormat_ASTC8x5Unorm',
    85: 'WGPUTextureFormat_ASTC8x5UnormSrgb',
    86: 'WGPUTextureFormat_ASTC8x6Unorm',
    87: 'WGPUTextureFormat_ASTC8x6UnormSrgb',
    88: 'WGPUTextureFormat_ASTC8x8Unorm',
    89: 'WGPUTextureFormat_ASTC8x8UnormSrgb',
    90: 'WGPUTextureFormat_ASTC10x5Unorm',
    91: 'WGPUTextureFormat_ASTC10x5UnormSrgb',
    92: 'WGPUTextureFormat_ASTC10x6Unorm',
    93: 'WGPUTextureFormat_ASTC10x6UnormSrgb',
    94: 'WGPUTextureFormat_ASTC10x8Unorm',
    95: 'WGPUTextureFormat_ASTC10x8UnormSrgb',
    96: 'WGPUTextureFormat_ASTC10x10Unorm',
    97: 'WGPUTextureFormat_ASTC10x10UnormSrgb',
    98: 'WGPUTextureFormat_ASTC12x10Unorm',
    99: 'WGPUTextureFormat_ASTC12x10UnormSrgb',
    100: 'WGPUTextureFormat_ASTC12x12Unorm',
    101: 'WGPUTextureFormat_ASTC12x12UnormSrgb',
    327686: 'WGPUTextureFormat_R8BG8Biplanar420Unorm',
    327687: 'WGPUTextureFormat_R10X6BG10X6Biplanar420Unorm',
    327688: 'WGPUTextureFormat_R8BG8A8Triplanar420Unorm',
    327689: 'WGPUTextureFormat_R8BG8Biplanar422Unorm',
    327690: 'WGPUTextureFormat_R8BG8Biplanar444Unorm',
    327691: 'WGPUTextureFormat_R10X6BG10X6Biplanar422Unorm',
    327692: 'WGPUTextureFormat_R10X6BG10X6Biplanar444Unorm',
    327693: 'WGPUTextureFormat_External',
    2147483647: 'WGPUTextureFormat_Force32',
}
WGPUTextureFormat_Undefined = 0
WGPUTextureFormat_R8Unorm = 1
WGPUTextureFormat_R8Snorm = 2
WGPUTextureFormat_R8Uint = 3
WGPUTextureFormat_R8Sint = 4
WGPUTextureFormat_R16Unorm = 5
WGPUTextureFormat_R16Snorm = 6
WGPUTextureFormat_R16Uint = 7
WGPUTextureFormat_R16Sint = 8
WGPUTextureFormat_R16Float = 9
WGPUTextureFormat_RG8Unorm = 10
WGPUTextureFormat_RG8Snorm = 11
WGPUTextureFormat_RG8Uint = 12
WGPUTextureFormat_RG8Sint = 13
WGPUTextureFormat_R32Float = 14
WGPUTextureFormat_R32Uint = 15
WGPUTextureFormat_R32Sint = 16
WGPUTextureFormat_RG16Unorm = 17
WGPUTextureFormat_RG16Snorm = 18
WGPUTextureFormat_RG16Uint = 19
WGPUTextureFormat_RG16Sint = 20
WGPUTextureFormat_RG16Float = 21
WGPUTextureFormat_RGBA8Unorm = 22
WGPUTextureFormat_RGBA8UnormSrgb = 23
WGPUTextureFormat_RGBA8Snorm = 24
WGPUTextureFormat_RGBA8Uint = 25
WGPUTextureFormat_RGBA8Sint = 26
WGPUTextureFormat_BGRA8Unorm = 27
WGPUTextureFormat_BGRA8UnormSrgb = 28
WGPUTextureFormat_RGB10A2Uint = 29
WGPUTextureFormat_RGB10A2Unorm = 30
WGPUTextureFormat_RG11B10Ufloat = 31
WGPUTextureFormat_RGB9E5Ufloat = 32
WGPUTextureFormat_RG32Float = 33
WGPUTextureFormat_RG32Uint = 34
WGPUTextureFormat_RG32Sint = 35
WGPUTextureFormat_RGBA16Unorm = 36
WGPUTextureFormat_RGBA16Snorm = 37
WGPUTextureFormat_RGBA16Uint = 38
WGPUTextureFormat_RGBA16Sint = 39
WGPUTextureFormat_RGBA16Float = 40
WGPUTextureFormat_RGBA32Float = 41
WGPUTextureFormat_RGBA32Uint = 42
WGPUTextureFormat_RGBA32Sint = 43
WGPUTextureFormat_Stencil8 = 44
WGPUTextureFormat_Depth16Unorm = 45
WGPUTextureFormat_Depth24Plus = 46
WGPUTextureFormat_Depth24PlusStencil8 = 47
WGPUTextureFormat_Depth32Float = 48
WGPUTextureFormat_Depth32FloatStencil8 = 49
WGPUTextureFormat_BC1RGBAUnorm = 50
WGPUTextureFormat_BC1RGBAUnormSrgb = 51
WGPUTextureFormat_BC2RGBAUnorm = 52
WGPUTextureFormat_BC2RGBAUnormSrgb = 53
WGPUTextureFormat_BC3RGBAUnorm = 54
WGPUTextureFormat_BC3RGBAUnormSrgb = 55
WGPUTextureFormat_BC4RUnorm = 56
WGPUTextureFormat_BC4RSnorm = 57
WGPUTextureFormat_BC5RGUnorm = 58
WGPUTextureFormat_BC5RGSnorm = 59
WGPUTextureFormat_BC6HRGBUfloat = 60
WGPUTextureFormat_BC6HRGBFloat = 61
WGPUTextureFormat_BC7RGBAUnorm = 62
WGPUTextureFormat_BC7RGBAUnormSrgb = 63
WGPUTextureFormat_ETC2RGB8Unorm = 64
WGPUTextureFormat_ETC2RGB8UnormSrgb = 65
WGPUTextureFormat_ETC2RGB8A1Unorm = 66
WGPUTextureFormat_ETC2RGB8A1UnormSrgb = 67
WGPUTextureFormat_ETC2RGBA8Unorm = 68
WGPUTextureFormat_ETC2RGBA8UnormSrgb = 69
WGPUTextureFormat_EACR11Unorm = 70
WGPUTextureFormat_EACR11Snorm = 71
WGPUTextureFormat_EACRG11Unorm = 72
WGPUTextureFormat_EACRG11Snorm = 73
WGPUTextureFormat_ASTC4x4Unorm = 74
WGPUTextureFormat_ASTC4x4UnormSrgb = 75
WGPUTextureFormat_ASTC5x4Unorm = 76
WGPUTextureFormat_ASTC5x4UnormSrgb = 77
WGPUTextureFormat_ASTC5x5Unorm = 78
WGPUTextureFormat_ASTC5x5UnormSrgb = 79
WGPUTextureFormat_ASTC6x5Unorm = 80
WGPUTextureFormat_ASTC6x5UnormSrgb = 81
WGPUTextureFormat_ASTC6x6Unorm = 82
WGPUTextureFormat_ASTC6x6UnormSrgb = 83
WGPUTextureFormat_ASTC8x5Unorm = 84
WGPUTextureFormat_ASTC8x5UnormSrgb = 85
WGPUTextureFormat_ASTC8x6Unorm = 86
WGPUTextureFormat_ASTC8x6UnormSrgb = 87
WGPUTextureFormat_ASTC8x8Unorm = 88
WGPUTextureFormat_ASTC8x8UnormSrgb = 89
WGPUTextureFormat_ASTC10x5Unorm = 90
WGPUTextureFormat_ASTC10x5UnormSrgb = 91
WGPUTextureFormat_ASTC10x6Unorm = 92
WGPUTextureFormat_ASTC10x6UnormSrgb = 93
WGPUTextureFormat_ASTC10x8Unorm = 94
WGPUTextureFormat_ASTC10x8UnormSrgb = 95
WGPUTextureFormat_ASTC10x10Unorm = 96
WGPUTextureFormat_ASTC10x10UnormSrgb = 97
WGPUTextureFormat_ASTC12x10Unorm = 98
WGPUTextureFormat_ASTC12x10UnormSrgb = 99
WGPUTextureFormat_ASTC12x12Unorm = 100
WGPUTextureFormat_ASTC12x12UnormSrgb = 101
WGPUTextureFormat_R8BG8Biplanar420Unorm = 327686
WGPUTextureFormat_R10X6BG10X6Biplanar420Unorm = 327687
WGPUTextureFormat_R8BG8A8Triplanar420Unorm = 327688
WGPUTextureFormat_R8BG8Biplanar422Unorm = 327689
WGPUTextureFormat_R8BG8Biplanar444Unorm = 327690
WGPUTextureFormat_R10X6BG10X6Biplanar422Unorm = 327691
WGPUTextureFormat_R10X6BG10X6Biplanar444Unorm = 327692
WGPUTextureFormat_External = 327693
WGPUTextureFormat_Force32 = 2147483647
WGPUTextureFormat = ctypes.c_uint32 # enum

# values for enumeration 'WGPUTextureSampleType'
WGPUTextureSampleType__enumvalues = {
    0: 'WGPUTextureSampleType_BindingNotUsed',
    1: 'WGPUTextureSampleType_Undefined',
    2: 'WGPUTextureSampleType_Float',
    3: 'WGPUTextureSampleType_UnfilterableFloat',
    4: 'WGPUTextureSampleType_Depth',
    5: 'WGPUTextureSampleType_Sint',
    6: 'WGPUTextureSampleType_Uint',
    2147483647: 'WGPUTextureSampleType_Force32',
}
WGPUTextureSampleType_BindingNotUsed = 0
WGPUTextureSampleType_Undefined = 1
WGPUTextureSampleType_Float = 2
WGPUTextureSampleType_UnfilterableFloat = 3
WGPUTextureSampleType_Depth = 4
WGPUTextureSampleType_Sint = 5
WGPUTextureSampleType_Uint = 6
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

# values for enumeration 'WGPUToneMappingMode'
WGPUToneMappingMode__enumvalues = {
    1: 'WGPUToneMappingMode_Standard',
    2: 'WGPUToneMappingMode_Extended',
    2147483647: 'WGPUToneMappingMode_Force32',
}
WGPUToneMappingMode_Standard = 1
WGPUToneMappingMode_Extended = 2
WGPUToneMappingMode_Force32 = 2147483647
WGPUToneMappingMode = ctypes.c_uint32 # enum

# values for enumeration 'WGPUVertexFormat'
WGPUVertexFormat__enumvalues = {
    1: 'WGPUVertexFormat_Uint8',
    2: 'WGPUVertexFormat_Uint8x2',
    3: 'WGPUVertexFormat_Uint8x4',
    4: 'WGPUVertexFormat_Sint8',
    5: 'WGPUVertexFormat_Sint8x2',
    6: 'WGPUVertexFormat_Sint8x4',
    7: 'WGPUVertexFormat_Unorm8',
    8: 'WGPUVertexFormat_Unorm8x2',
    9: 'WGPUVertexFormat_Unorm8x4',
    10: 'WGPUVertexFormat_Snorm8',
    11: 'WGPUVertexFormat_Snorm8x2',
    12: 'WGPUVertexFormat_Snorm8x4',
    13: 'WGPUVertexFormat_Uint16',
    14: 'WGPUVertexFormat_Uint16x2',
    15: 'WGPUVertexFormat_Uint16x4',
    16: 'WGPUVertexFormat_Sint16',
    17: 'WGPUVertexFormat_Sint16x2',
    18: 'WGPUVertexFormat_Sint16x4',
    19: 'WGPUVertexFormat_Unorm16',
    20: 'WGPUVertexFormat_Unorm16x2',
    21: 'WGPUVertexFormat_Unorm16x4',
    22: 'WGPUVertexFormat_Snorm16',
    23: 'WGPUVertexFormat_Snorm16x2',
    24: 'WGPUVertexFormat_Snorm16x4',
    25: 'WGPUVertexFormat_Float16',
    26: 'WGPUVertexFormat_Float16x2',
    27: 'WGPUVertexFormat_Float16x4',
    28: 'WGPUVertexFormat_Float32',
    29: 'WGPUVertexFormat_Float32x2',
    30: 'WGPUVertexFormat_Float32x3',
    31: 'WGPUVertexFormat_Float32x4',
    32: 'WGPUVertexFormat_Uint32',
    33: 'WGPUVertexFormat_Uint32x2',
    34: 'WGPUVertexFormat_Uint32x3',
    35: 'WGPUVertexFormat_Uint32x4',
    36: 'WGPUVertexFormat_Sint32',
    37: 'WGPUVertexFormat_Sint32x2',
    38: 'WGPUVertexFormat_Sint32x3',
    39: 'WGPUVertexFormat_Sint32x4',
    40: 'WGPUVertexFormat_Unorm10_10_10_2',
    41: 'WGPUVertexFormat_Unorm8x4BGRA',
    2147483647: 'WGPUVertexFormat_Force32',
}
WGPUVertexFormat_Uint8 = 1
WGPUVertexFormat_Uint8x2 = 2
WGPUVertexFormat_Uint8x4 = 3
WGPUVertexFormat_Sint8 = 4
WGPUVertexFormat_Sint8x2 = 5
WGPUVertexFormat_Sint8x4 = 6
WGPUVertexFormat_Unorm8 = 7
WGPUVertexFormat_Unorm8x2 = 8
WGPUVertexFormat_Unorm8x4 = 9
WGPUVertexFormat_Snorm8 = 10
WGPUVertexFormat_Snorm8x2 = 11
WGPUVertexFormat_Snorm8x4 = 12
WGPUVertexFormat_Uint16 = 13
WGPUVertexFormat_Uint16x2 = 14
WGPUVertexFormat_Uint16x4 = 15
WGPUVertexFormat_Sint16 = 16
WGPUVertexFormat_Sint16x2 = 17
WGPUVertexFormat_Sint16x4 = 18
WGPUVertexFormat_Unorm16 = 19
WGPUVertexFormat_Unorm16x2 = 20
WGPUVertexFormat_Unorm16x4 = 21
WGPUVertexFormat_Snorm16 = 22
WGPUVertexFormat_Snorm16x2 = 23
WGPUVertexFormat_Snorm16x4 = 24
WGPUVertexFormat_Float16 = 25
WGPUVertexFormat_Float16x2 = 26
WGPUVertexFormat_Float16x4 = 27
WGPUVertexFormat_Float32 = 28
WGPUVertexFormat_Float32x2 = 29
WGPUVertexFormat_Float32x3 = 30
WGPUVertexFormat_Float32x4 = 31
WGPUVertexFormat_Uint32 = 32
WGPUVertexFormat_Uint32x2 = 33
WGPUVertexFormat_Uint32x3 = 34
WGPUVertexFormat_Uint32x4 = 35
WGPUVertexFormat_Sint32 = 36
WGPUVertexFormat_Sint32x2 = 37
WGPUVertexFormat_Sint32x3 = 38
WGPUVertexFormat_Sint32x4 = 39
WGPUVertexFormat_Unorm10_10_10_2 = 40
WGPUVertexFormat_Unorm8x4BGRA = 41
WGPUVertexFormat_Force32 = 2147483647
WGPUVertexFormat = ctypes.c_uint32 # enum

# values for enumeration 'WGPUVertexStepMode'
WGPUVertexStepMode__enumvalues = {
    0: 'WGPUVertexStepMode_Undefined',
    1: 'WGPUVertexStepMode_Vertex',
    2: 'WGPUVertexStepMode_Instance',
    2147483647: 'WGPUVertexStepMode_Force32',
}
WGPUVertexStepMode_Undefined = 0
WGPUVertexStepMode_Vertex = 1
WGPUVertexStepMode_Instance = 2
WGPUVertexStepMode_Force32 = 2147483647
WGPUVertexStepMode = ctypes.c_uint32 # enum

# values for enumeration 'WGPUWaitStatus'
WGPUWaitStatus__enumvalues = {
    1: 'WGPUWaitStatus_Success',
    2: 'WGPUWaitStatus_TimedOut',
    3: 'WGPUWaitStatus_Error',
    2147483647: 'WGPUWaitStatus_Force32',
}
WGPUWaitStatus_Success = 1
WGPUWaitStatus_TimedOut = 2
WGPUWaitStatus_Error = 3
WGPUWaitStatus_Force32 = 2147483647
WGPUWaitStatus = ctypes.c_uint32 # enum

# values for enumeration 'WGPUWGSLLanguageFeatureName'
WGPUWGSLLanguageFeatureName__enumvalues = {
    1: 'WGPUWGSLLanguageFeatureName_ReadonlyAndReadwriteStorageTextures',
    2: 'WGPUWGSLLanguageFeatureName_Packed4x8IntegerDotProduct',
    3: 'WGPUWGSLLanguageFeatureName_UnrestrictedPointerParameters',
    4: 'WGPUWGSLLanguageFeatureName_PointerCompositeAccess',
    5: 'WGPUWGSLLanguageFeatureName_UniformBufferStandardLayout',
    6: 'WGPUWGSLLanguageFeatureName_SubgroupId',
    327687: 'WGPUWGSLLanguageFeatureName_SizedBindingArray',
    327688: 'WGPUWGSLLanguageFeatureName_TexelBuffers',
    327689: 'WGPUWGSLLanguageFeatureName_ChromiumPrint',
    327690: 'WGPUWGSLLanguageFeatureName_FragmentDepth',
    327691: 'WGPUWGSLLanguageFeatureName_ImmediateAddressSpace',
    327692: 'WGPUWGSLLanguageFeatureName_SubgroupUniformity',
    327680: 'WGPUWGSLLanguageFeatureName_ChromiumTestingUnimplemented',
    327681: 'WGPUWGSLLanguageFeatureName_ChromiumTestingUnsafeExperimental',
    327682: 'WGPUWGSLLanguageFeatureName_ChromiumTestingExperimental',
    327683: 'WGPUWGSLLanguageFeatureName_ChromiumTestingShippedWithKillswitch',
    327684: 'WGPUWGSLLanguageFeatureName_ChromiumTestingShipped',
    2147483647: 'WGPUWGSLLanguageFeatureName_Force32',
}
WGPUWGSLLanguageFeatureName_ReadonlyAndReadwriteStorageTextures = 1
WGPUWGSLLanguageFeatureName_Packed4x8IntegerDotProduct = 2
WGPUWGSLLanguageFeatureName_UnrestrictedPointerParameters = 3
WGPUWGSLLanguageFeatureName_PointerCompositeAccess = 4
WGPUWGSLLanguageFeatureName_UniformBufferStandardLayout = 5
WGPUWGSLLanguageFeatureName_SubgroupId = 6
WGPUWGSLLanguageFeatureName_SizedBindingArray = 327687
WGPUWGSLLanguageFeatureName_TexelBuffers = 327688
WGPUWGSLLanguageFeatureName_ChromiumPrint = 327689
WGPUWGSLLanguageFeatureName_FragmentDepth = 327690
WGPUWGSLLanguageFeatureName_ImmediateAddressSpace = 327691
WGPUWGSLLanguageFeatureName_SubgroupUniformity = 327692
WGPUWGSLLanguageFeatureName_ChromiumTestingUnimplemented = 327680
WGPUWGSLLanguageFeatureName_ChromiumTestingUnsafeExperimental = 327681
WGPUWGSLLanguageFeatureName_ChromiumTestingExperimental = 327682
WGPUWGSLLanguageFeatureName_ChromiumTestingShippedWithKillswitch = 327683
WGPUWGSLLanguageFeatureName_ChromiumTestingShipped = 327684
WGPUWGSLLanguageFeatureName_Force32 = 2147483647
WGPUWGSLLanguageFeatureName = ctypes.c_uint32 # enum
WGPUBufferUsage = ctypes.c_uint64
WGPUBufferUsage_None = 0x0000000000000000 # Variable ctypes.c_uint64
WGPUBufferUsage_MapRead = 0x0000000000000001 # Variable ctypes.c_uint64
WGPUBufferUsage_MapWrite = 0x0000000000000002 # Variable ctypes.c_uint64
WGPUBufferUsage_CopySrc = 0x0000000000000004 # Variable ctypes.c_uint64
WGPUBufferUsage_CopyDst = 0x0000000000000008 # Variable ctypes.c_uint64
WGPUBufferUsage_Index = 0x0000000000000010 # Variable ctypes.c_uint64
WGPUBufferUsage_Vertex = 0x0000000000000020 # Variable ctypes.c_uint64
WGPUBufferUsage_Uniform = 0x0000000000000040 # Variable ctypes.c_uint64
WGPUBufferUsage_Storage = 0x0000000000000080 # Variable ctypes.c_uint64
WGPUBufferUsage_Indirect = 0x0000000000000100 # Variable ctypes.c_uint64
WGPUBufferUsage_QueryResolve = 0x0000000000000200 # Variable ctypes.c_uint64
WGPUBufferUsage_TexelBuffer = 0x0000000000000400 # Variable ctypes.c_uint64
WGPUColorWriteMask = ctypes.c_uint64
WGPUColorWriteMask_None = 0x0000000000000000 # Variable ctypes.c_uint64
WGPUColorWriteMask_Red = 0x0000000000000001 # Variable ctypes.c_uint64
WGPUColorWriteMask_Green = 0x0000000000000002 # Variable ctypes.c_uint64
WGPUColorWriteMask_Blue = 0x0000000000000004 # Variable ctypes.c_uint64
WGPUColorWriteMask_Alpha = 0x0000000000000008 # Variable ctypes.c_uint64
WGPUColorWriteMask_All = 0x000000000000000F # Variable ctypes.c_uint64
WGPUHeapProperty = ctypes.c_uint64
WGPUHeapProperty_None = 0x0000000000000000 # Variable ctypes.c_uint64
WGPUHeapProperty_DeviceLocal = 0x0000000000000001 # Variable ctypes.c_uint64
WGPUHeapProperty_HostVisible = 0x0000000000000002 # Variable ctypes.c_uint64
WGPUHeapProperty_HostCoherent = 0x0000000000000004 # Variable ctypes.c_uint64
WGPUHeapProperty_HostUncached = 0x0000000000000008 # Variable ctypes.c_uint64
WGPUHeapProperty_HostCached = 0x0000000000000010 # Variable ctypes.c_uint64
WGPUMapMode = ctypes.c_uint64
WGPUMapMode_None = 0x0000000000000000 # Variable ctypes.c_uint64
WGPUMapMode_Read = 0x0000000000000001 # Variable ctypes.c_uint64
WGPUMapMode_Write = 0x0000000000000002 # Variable ctypes.c_uint64
WGPUShaderStage = ctypes.c_uint64
WGPUShaderStage_None = 0x0000000000000000 # Variable ctypes.c_uint64
WGPUShaderStage_Vertex = 0x0000000000000001 # Variable ctypes.c_uint64
WGPUShaderStage_Fragment = 0x0000000000000002 # Variable ctypes.c_uint64
WGPUShaderStage_Compute = 0x0000000000000004 # Variable ctypes.c_uint64
WGPUTextureUsage = ctypes.c_uint64
WGPUTextureUsage_None = 0x0000000000000000 # Variable ctypes.c_uint64
WGPUTextureUsage_CopySrc = 0x0000000000000001 # Variable ctypes.c_uint64
WGPUTextureUsage_CopyDst = 0x0000000000000002 # Variable ctypes.c_uint64
WGPUTextureUsage_TextureBinding = 0x0000000000000004 # Variable ctypes.c_uint64
WGPUTextureUsage_StorageBinding = 0x0000000000000008 # Variable ctypes.c_uint64
WGPUTextureUsage_RenderAttachment = 0x0000000000000010 # Variable ctypes.c_uint64
WGPUTextureUsage_TransientAttachment = 0x0000000000000020 # Variable ctypes.c_uint64
WGPUTextureUsage_StorageAttachment = 0x0000000000000040 # Variable ctypes.c_uint64
WGPUCallback = ctypes.CFUNCTYPE(None, ctypes.POINTER(None))
WGPUDawnLoadCacheDataFunction = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.POINTER(None), ctypes.c_uint64, ctypes.POINTER(None), ctypes.c_uint64, ctypes.POINTER(None))
WGPUDawnStoreCacheDataFunction = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.c_uint64, ctypes.POINTER(None), ctypes.c_uint64, ctypes.POINTER(None))
WGPUProc = ctypes.CFUNCTYPE(None)
WGPUBufferMapCallback = ctypes.CFUNCTYPE(None, WGPUMapAsyncStatus, struct_WGPUStringView, ctypes.POINTER(None), ctypes.POINTER(None))
class struct_WGPUCompilationInfo(Structure):
    pass

WGPUCompilationInfoCallback = ctypes.CFUNCTYPE(None, WGPUCompilationInfoRequestStatus, ctypes.POINTER(struct_WGPUCompilationInfo), ctypes.POINTER(None), ctypes.POINTER(None))
WGPUCreateComputePipelineAsyncCallback = ctypes.CFUNCTYPE(None, WGPUCreatePipelineAsyncStatus, ctypes.POINTER(struct_WGPUComputePipelineImpl), struct_WGPUStringView, ctypes.POINTER(None), ctypes.POINTER(None))
WGPUCreateRenderPipelineAsyncCallback = ctypes.CFUNCTYPE(None, WGPUCreatePipelineAsyncStatus, ctypes.POINTER(struct_WGPURenderPipelineImpl), struct_WGPUStringView, ctypes.POINTER(None), ctypes.POINTER(None))
WGPUDeviceLostCallback = ctypes.CFUNCTYPE(None, ctypes.POINTER(ctypes.POINTER(struct_WGPUDeviceImpl)), WGPUDeviceLostReason, struct_WGPUStringView, ctypes.POINTER(None), ctypes.POINTER(None))
WGPULoggingCallback = ctypes.CFUNCTYPE(None, WGPULoggingType, struct_WGPUStringView, ctypes.POINTER(None), ctypes.POINTER(None))
WGPUPopErrorScopeCallback = ctypes.CFUNCTYPE(None, WGPUPopErrorScopeStatus, WGPUErrorType, struct_WGPUStringView, ctypes.POINTER(None), ctypes.POINTER(None))
WGPUQueueWorkDoneCallback = ctypes.CFUNCTYPE(None, WGPUQueueWorkDoneStatus, struct_WGPUStringView, ctypes.POINTER(None), ctypes.POINTER(None))
WGPURequestAdapterCallback = ctypes.CFUNCTYPE(None, WGPURequestAdapterStatus, ctypes.POINTER(struct_WGPUAdapterImpl), struct_WGPUStringView, ctypes.POINTER(None), ctypes.POINTER(None))
WGPURequestDeviceCallback = ctypes.CFUNCTYPE(None, WGPURequestDeviceStatus, ctypes.POINTER(struct_WGPUDeviceImpl), struct_WGPUStringView, ctypes.POINTER(None), ctypes.POINTER(None))
WGPUUncapturedErrorCallback = ctypes.CFUNCTYPE(None, ctypes.POINTER(ctypes.POINTER(struct_WGPUDeviceImpl)), WGPUErrorType, struct_WGPUStringView, ctypes.POINTER(None), ctypes.POINTER(None))
class struct_WGPUChainedStruct(Structure):
    pass

struct_WGPUChainedStruct._pack_ = 1 # source:False
struct_WGPUChainedStruct._fields_ = [
    ('next', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('sType', WGPUSType),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUChainedStruct = struct_WGPUChainedStruct
class struct_WGPUBufferMapCallbackInfo(Structure):
    pass

struct_WGPUBufferMapCallbackInfo._pack_ = 1 # source:False
struct_WGPUBufferMapCallbackInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, WGPUMapAsyncStatus, struct_WGPUStringView, ctypes.POINTER(None), ctypes.POINTER(None))),
    ('userdata1', ctypes.POINTER(None)),
    ('userdata2', ctypes.POINTER(None)),
]

WGPUBufferMapCallbackInfo = struct_WGPUBufferMapCallbackInfo
class struct_WGPUCompilationInfoCallbackInfo(Structure):
    pass

struct_WGPUCompilationInfoCallbackInfo._pack_ = 1 # source:False
struct_WGPUCompilationInfoCallbackInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, WGPUCompilationInfoRequestStatus, ctypes.POINTER(struct_WGPUCompilationInfo), ctypes.POINTER(None), ctypes.POINTER(None))),
    ('userdata1', ctypes.POINTER(None)),
    ('userdata2', ctypes.POINTER(None)),
]

WGPUCompilationInfoCallbackInfo = struct_WGPUCompilationInfoCallbackInfo
class struct_WGPUCreateComputePipelineAsyncCallbackInfo(Structure):
    pass

struct_WGPUCreateComputePipelineAsyncCallbackInfo._pack_ = 1 # source:False
struct_WGPUCreateComputePipelineAsyncCallbackInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, WGPUCreatePipelineAsyncStatus, ctypes.POINTER(struct_WGPUComputePipelineImpl), struct_WGPUStringView, ctypes.POINTER(None), ctypes.POINTER(None))),
    ('userdata1', ctypes.POINTER(None)),
    ('userdata2', ctypes.POINTER(None)),
]

WGPUCreateComputePipelineAsyncCallbackInfo = struct_WGPUCreateComputePipelineAsyncCallbackInfo
class struct_WGPUCreateRenderPipelineAsyncCallbackInfo(Structure):
    pass

struct_WGPUCreateRenderPipelineAsyncCallbackInfo._pack_ = 1 # source:False
struct_WGPUCreateRenderPipelineAsyncCallbackInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, WGPUCreatePipelineAsyncStatus, ctypes.POINTER(struct_WGPURenderPipelineImpl), struct_WGPUStringView, ctypes.POINTER(None), ctypes.POINTER(None))),
    ('userdata1', ctypes.POINTER(None)),
    ('userdata2', ctypes.POINTER(None)),
]

WGPUCreateRenderPipelineAsyncCallbackInfo = struct_WGPUCreateRenderPipelineAsyncCallbackInfo
class struct_WGPUDeviceLostCallbackInfo(Structure):
    pass

struct_WGPUDeviceLostCallbackInfo._pack_ = 1 # source:False
struct_WGPUDeviceLostCallbackInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, ctypes.POINTER(ctypes.POINTER(struct_WGPUDeviceImpl)), WGPUDeviceLostReason, struct_WGPUStringView, ctypes.POINTER(None), ctypes.POINTER(None))),
    ('userdata1', ctypes.POINTER(None)),
    ('userdata2', ctypes.POINTER(None)),
]

WGPUDeviceLostCallbackInfo = struct_WGPUDeviceLostCallbackInfo
class struct_WGPULoggingCallbackInfo(Structure):
    pass

struct_WGPULoggingCallbackInfo._pack_ = 1 # source:False
struct_WGPULoggingCallbackInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('callback', ctypes.CFUNCTYPE(None, WGPULoggingType, struct_WGPUStringView, ctypes.POINTER(None), ctypes.POINTER(None))),
    ('userdata1', ctypes.POINTER(None)),
    ('userdata2', ctypes.POINTER(None)),
]

WGPULoggingCallbackInfo = struct_WGPULoggingCallbackInfo
class struct_WGPUPopErrorScopeCallbackInfo(Structure):
    pass

struct_WGPUPopErrorScopeCallbackInfo._pack_ = 1 # source:False
struct_WGPUPopErrorScopeCallbackInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, WGPUPopErrorScopeStatus, WGPUErrorType, struct_WGPUStringView, ctypes.POINTER(None), ctypes.POINTER(None))),
    ('userdata1', ctypes.POINTER(None)),
    ('userdata2', ctypes.POINTER(None)),
]

WGPUPopErrorScopeCallbackInfo = struct_WGPUPopErrorScopeCallbackInfo
class struct_WGPUQueueWorkDoneCallbackInfo(Structure):
    pass

struct_WGPUQueueWorkDoneCallbackInfo._pack_ = 1 # source:False
struct_WGPUQueueWorkDoneCallbackInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, WGPUQueueWorkDoneStatus, struct_WGPUStringView, ctypes.POINTER(None), ctypes.POINTER(None))),
    ('userdata1', ctypes.POINTER(None)),
    ('userdata2', ctypes.POINTER(None)),
]

WGPUQueueWorkDoneCallbackInfo = struct_WGPUQueueWorkDoneCallbackInfo
class struct_WGPURequestAdapterCallbackInfo(Structure):
    pass

struct_WGPURequestAdapterCallbackInfo._pack_ = 1 # source:False
struct_WGPURequestAdapterCallbackInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, WGPURequestAdapterStatus, ctypes.POINTER(struct_WGPUAdapterImpl), struct_WGPUStringView, ctypes.POINTER(None), ctypes.POINTER(None))),
    ('userdata1', ctypes.POINTER(None)),
    ('userdata2', ctypes.POINTER(None)),
]

WGPURequestAdapterCallbackInfo = struct_WGPURequestAdapterCallbackInfo
class struct_WGPURequestDeviceCallbackInfo(Structure):
    pass

struct_WGPURequestDeviceCallbackInfo._pack_ = 1 # source:False
struct_WGPURequestDeviceCallbackInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('mode', WGPUCallbackMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('callback', ctypes.CFUNCTYPE(None, WGPURequestDeviceStatus, ctypes.POINTER(struct_WGPUDeviceImpl), struct_WGPUStringView, ctypes.POINTER(None), ctypes.POINTER(None))),
    ('userdata1', ctypes.POINTER(None)),
    ('userdata2', ctypes.POINTER(None)),
]

WGPURequestDeviceCallbackInfo = struct_WGPURequestDeviceCallbackInfo
class struct_WGPUUncapturedErrorCallbackInfo(Structure):
    pass

struct_WGPUUncapturedErrorCallbackInfo._pack_ = 1 # source:False
struct_WGPUUncapturedErrorCallbackInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('callback', ctypes.CFUNCTYPE(None, ctypes.POINTER(ctypes.POINTER(struct_WGPUDeviceImpl)), WGPUErrorType, struct_WGPUStringView, ctypes.POINTER(None), ctypes.POINTER(None))),
    ('userdata1', ctypes.POINTER(None)),
    ('userdata2', ctypes.POINTER(None)),
]

WGPUUncapturedErrorCallbackInfo = struct_WGPUUncapturedErrorCallbackInfo
class struct_WGPUAdapterPropertiesD3D(Structure):
    pass

struct_WGPUAdapterPropertiesD3D._pack_ = 1 # source:False
struct_WGPUAdapterPropertiesD3D._fields_ = [
    ('chain', WGPUChainedStruct),
    ('shaderModel', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUAdapterPropertiesD3D = struct_WGPUAdapterPropertiesD3D
class struct_WGPUAdapterPropertiesVk(Structure):
    pass

struct_WGPUAdapterPropertiesVk._pack_ = 1 # source:False
struct_WGPUAdapterPropertiesVk._fields_ = [
    ('chain', WGPUChainedStruct),
    ('driverVersion', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUAdapterPropertiesVk = struct_WGPUAdapterPropertiesVk
class struct_WGPUAdapterPropertiesWGPU(Structure):
    pass

struct_WGPUAdapterPropertiesWGPU._pack_ = 1 # source:False
struct_WGPUAdapterPropertiesWGPU._fields_ = [
    ('chain', WGPUChainedStruct),
    ('backendType', WGPUBackendType),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUAdapterPropertiesWGPU = struct_WGPUAdapterPropertiesWGPU
class struct_WGPUBindGroupDynamicBindingArray(Structure):
    pass

struct_WGPUBindGroupDynamicBindingArray._pack_ = 1 # source:False
struct_WGPUBindGroupDynamicBindingArray._fields_ = [
    ('chain', WGPUChainedStruct),
    ('dynamicArraySize', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUBindGroupDynamicBindingArray = struct_WGPUBindGroupDynamicBindingArray
class struct_WGPUBindGroupEntryContents(Structure):
    pass

struct_WGPUBindGroupEntryContents._pack_ = 1 # source:False
struct_WGPUBindGroupEntryContents._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('buffer', ctypes.POINTER(struct_WGPUBufferImpl)),
    ('offset', ctypes.c_uint64),
    ('size', ctypes.c_uint64),
    ('sampler', ctypes.POINTER(struct_WGPUSamplerImpl)),
    ('textureView', ctypes.POINTER(struct_WGPUTextureViewImpl)),
]

WGPUBindGroupEntryContents = struct_WGPUBindGroupEntryContents
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
    ('label', WGPUStringView),
]

WGPUCommandBufferDescriptor = struct_WGPUCommandBufferDescriptor
class struct_WGPUCompatibilityModeLimits(Structure):
    pass

struct_WGPUCompatibilityModeLimits._pack_ = 1 # source:False
struct_WGPUCompatibilityModeLimits._fields_ = [
    ('chain', WGPUChainedStruct),
    ('maxStorageBuffersInVertexStage', ctypes.c_uint32),
    ('maxStorageTexturesInVertexStage', ctypes.c_uint32),
    ('maxStorageBuffersInFragmentStage', ctypes.c_uint32),
    ('maxStorageTexturesInFragmentStage', ctypes.c_uint32),
]

WGPUCompatibilityModeLimits = struct_WGPUCompatibilityModeLimits
class struct_WGPUConstantEntry(Structure):
    pass

struct_WGPUConstantEntry._pack_ = 1 # source:False
struct_WGPUConstantEntry._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('key', WGPUStringView),
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
class struct_WGPUDawnAdapterPropertiesPowerPreference(Structure):
    pass

struct_WGPUDawnAdapterPropertiesPowerPreference._pack_ = 1 # source:False
struct_WGPUDawnAdapterPropertiesPowerPreference._fields_ = [
    ('chain', WGPUChainedStruct),
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
    ('isolationKey', WGPUStringView),
    ('loadDataFunction', ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.POINTER(None), ctypes.c_uint64, ctypes.POINTER(None), ctypes.c_uint64, ctypes.POINTER(None))),
    ('storeDataFunction', ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.c_uint64, ctypes.POINTER(None), ctypes.c_uint64, ctypes.POINTER(None))),
    ('functionUserdata', ctypes.POINTER(None)),
]

WGPUDawnCacheDeviceDescriptor = struct_WGPUDawnCacheDeviceDescriptor
class struct_WGPUDawnCompilationMessageUtf16(Structure):
    pass

struct_WGPUDawnCompilationMessageUtf16._pack_ = 1 # source:False
struct_WGPUDawnCompilationMessageUtf16._fields_ = [
    ('chain', WGPUChainedStruct),
    ('linePos', ctypes.c_uint64),
    ('offset', ctypes.c_uint64),
    ('length', ctypes.c_uint64),
]

WGPUDawnCompilationMessageUtf16 = struct_WGPUDawnCompilationMessageUtf16
class struct_WGPUDawnConsumeAdapterDescriptor(Structure):
    pass

struct_WGPUDawnConsumeAdapterDescriptor._pack_ = 1 # source:False
struct_WGPUDawnConsumeAdapterDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('consumeAdapter', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUDawnConsumeAdapterDescriptor = struct_WGPUDawnConsumeAdapterDescriptor
class struct_WGPUDawnDeviceAllocatorControl(Structure):
    pass

struct_WGPUDawnDeviceAllocatorControl._pack_ = 1 # source:False
struct_WGPUDawnDeviceAllocatorControl._fields_ = [
    ('chain', WGPUChainedStruct),
    ('allocatorHeapBlockSize', ctypes.c_uint64),
]

WGPUDawnDeviceAllocatorControl = struct_WGPUDawnDeviceAllocatorControl
class struct_WGPUDawnDrmFormatProperties(Structure):
    pass

struct_WGPUDawnDrmFormatProperties._pack_ = 1 # source:False
struct_WGPUDawnDrmFormatProperties._fields_ = [
    ('modifier', ctypes.c_uint64),
    ('modifierPlaneCount', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUDawnDrmFormatProperties = struct_WGPUDawnDrmFormatProperties
class struct_WGPUDawnEncoderInternalUsageDescriptor(Structure):
    pass

struct_WGPUDawnEncoderInternalUsageDescriptor._pack_ = 1 # source:False
struct_WGPUDawnEncoderInternalUsageDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('useInternalUsages', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUDawnEncoderInternalUsageDescriptor = struct_WGPUDawnEncoderInternalUsageDescriptor
class struct_WGPUDawnFakeBufferOOMForTesting(Structure):
    pass

struct_WGPUDawnFakeBufferOOMForTesting._pack_ = 1 # source:False
struct_WGPUDawnFakeBufferOOMForTesting._fields_ = [
    ('chain', WGPUChainedStruct),
    ('fakeOOMAtWireClientMap', ctypes.c_uint32),
    ('fakeOOMAtNativeMap', ctypes.c_uint32),
    ('fakeOOMAtDevice', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUDawnFakeBufferOOMForTesting = struct_WGPUDawnFakeBufferOOMForTesting
class struct_WGPUDawnFakeDeviceInitializeErrorForTesting(Structure):
    _pack_ = 1 # source:False
    _fields_ = [
    ('chain', WGPUChainedStruct),
     ]

WGPUDawnFakeDeviceInitializeErrorForTesting = struct_WGPUDawnFakeDeviceInitializeErrorForTesting
class struct_WGPUDawnHostMappedPointerLimits(Structure):
    pass

struct_WGPUDawnHostMappedPointerLimits._pack_ = 1 # source:False
struct_WGPUDawnHostMappedPointerLimits._fields_ = [
    ('chain', WGPUChainedStruct),
    ('hostMappedPointerAlignment', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUDawnHostMappedPointerLimits = struct_WGPUDawnHostMappedPointerLimits
class struct_WGPUDawnInjectedInvalidSType(Structure):
    pass

struct_WGPUDawnInjectedInvalidSType._pack_ = 1 # source:False
struct_WGPUDawnInjectedInvalidSType._fields_ = [
    ('chain', WGPUChainedStruct),
    ('invalidSType', WGPUSType),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUDawnInjectedInvalidSType = struct_WGPUDawnInjectedInvalidSType
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
class struct_WGPUDawnTexelCopyBufferRowAlignmentLimits(Structure):
    pass

struct_WGPUDawnTexelCopyBufferRowAlignmentLimits._pack_ = 1 # source:False
struct_WGPUDawnTexelCopyBufferRowAlignmentLimits._fields_ = [
    ('chain', WGPUChainedStruct),
    ('minTexelCopyBufferRowAlignment', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUDawnTexelCopyBufferRowAlignmentLimits = struct_WGPUDawnTexelCopyBufferRowAlignmentLimits
class struct_WGPUDawnTextureInternalUsageDescriptor(Structure):
    pass

struct_WGPUDawnTextureInternalUsageDescriptor._pack_ = 1 # source:False
struct_WGPUDawnTextureInternalUsageDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('internalUsage', ctypes.c_uint64),
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
class struct_WGPUDawnWGSLBlocklist(Structure):
    pass

struct_WGPUDawnWGSLBlocklist._pack_ = 1 # source:False
struct_WGPUDawnWGSLBlocklist._fields_ = [
    ('chain', WGPUChainedStruct),
    ('blocklistedFeatureCount', ctypes.c_uint64),
    ('blocklistedFeatures', ctypes.POINTER(ctypes.POINTER(ctypes.c_char))),
]

WGPUDawnWGSLBlocklist = struct_WGPUDawnWGSLBlocklist
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
class struct_WGPUDynamicBindingArrayLayout(Structure):
    pass

struct_WGPUDynamicBindingArrayLayout._pack_ = 1 # source:False
struct_WGPUDynamicBindingArrayLayout._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('start', ctypes.c_uint32),
    ('kind', WGPUDynamicBindingKind),
]

WGPUDynamicBindingArrayLayout = struct_WGPUDynamicBindingArrayLayout
class struct_WGPUDynamicBindingArrayLimits(Structure):
    pass

struct_WGPUDynamicBindingArrayLimits._pack_ = 1 # source:False
struct_WGPUDynamicBindingArrayLimits._fields_ = [
    ('chain', WGPUChainedStruct),
    ('maxDynamicBindingArraySize', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUDynamicBindingArrayLimits = struct_WGPUDynamicBindingArrayLimits
class struct_WGPUEmscriptenSurfaceSourceCanvasHTMLSelector(Structure):
    _pack_ = 1 # source:False
    _fields_ = [
    ('chain', WGPUChainedStruct),
    ('selector', WGPUStringView),
     ]

WGPUEmscriptenSurfaceSourceCanvasHTMLSelector = struct_WGPUEmscriptenSurfaceSourceCanvasHTMLSelector
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
class struct_WGPUFuture(Structure):
    pass

struct_WGPUFuture._pack_ = 1 # source:False
struct_WGPUFuture._fields_ = [
    ('id', ctypes.c_uint64),
]

WGPUFuture = struct_WGPUFuture
class struct_WGPUInstanceLimits(Structure):
    pass

struct_WGPUInstanceLimits._pack_ = 1 # source:False
struct_WGPUInstanceLimits._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('timedWaitAnyMaxCount', ctypes.c_uint64),
]

WGPUInstanceLimits = struct_WGPUInstanceLimits
class struct_WGPUINTERNAL_HAVE_EMDAWNWEBGPU_HEADER(Structure):
    pass

struct_WGPUINTERNAL_HAVE_EMDAWNWEBGPU_HEADER._pack_ = 1 # source:False
struct_WGPUINTERNAL_HAVE_EMDAWNWEBGPU_HEADER._fields_ = [
    ('unused', ctypes.c_uint32),
]

WGPUINTERNAL_HAVE_EMDAWNWEBGPU_HEADER = struct_WGPUINTERNAL_HAVE_EMDAWNWEBGPU_HEADER
class struct_WGPUMemoryHeapInfo(Structure):
    pass

struct_WGPUMemoryHeapInfo._pack_ = 1 # source:False
struct_WGPUMemoryHeapInfo._fields_ = [
    ('properties', ctypes.c_uint64),
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
class struct_WGPUPassTimestampWrites(Structure):
    pass

struct_WGPUPassTimestampWrites._pack_ = 1 # source:False
struct_WGPUPassTimestampWrites._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('querySet', ctypes.POINTER(struct_WGPUQuerySetImpl)),
    ('beginningOfPassWriteIndex', ctypes.c_uint32),
    ('endOfPassWriteIndex', ctypes.c_uint32),
]

WGPUPassTimestampWrites = struct_WGPUPassTimestampWrites
class struct_WGPUPipelineLayoutResourceTable(Structure):
    pass

struct_WGPUPipelineLayoutResourceTable._pack_ = 1 # source:False
struct_WGPUPipelineLayoutResourceTable._fields_ = [
    ('chain', WGPUChainedStruct),
    ('usesResourceTable', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUPipelineLayoutResourceTable = struct_WGPUPipelineLayoutResourceTable
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
class struct_WGPUPrimitiveState(Structure):
    pass

struct_WGPUPrimitiveState._pack_ = 1 # source:False
struct_WGPUPrimitiveState._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('topology', WGPUPrimitiveTopology),
    ('stripIndexFormat', WGPUIndexFormat),
    ('frontFace', WGPUFrontFace),
    ('cullMode', WGPUCullMode),
    ('unclippedDepth', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUPrimitiveState = struct_WGPUPrimitiveState
class struct_WGPUQuerySetDescriptor(Structure):
    pass

struct_WGPUQuerySetDescriptor._pack_ = 1 # source:False
struct_WGPUQuerySetDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', WGPUStringView),
    ('type', WGPUQueryType),
    ('count', ctypes.c_uint32),
]

WGPUQuerySetDescriptor = struct_WGPUQuerySetDescriptor
class struct_WGPUQueueDescriptor(Structure):
    pass

struct_WGPUQueueDescriptor._pack_ = 1 # source:False
struct_WGPUQueueDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', WGPUStringView),
]

WGPUQueueDescriptor = struct_WGPUQueueDescriptor
class struct_WGPURenderBundleDescriptor(Structure):
    pass

struct_WGPURenderBundleDescriptor._pack_ = 1 # source:False
struct_WGPURenderBundleDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', WGPUStringView),
]

WGPURenderBundleDescriptor = struct_WGPURenderBundleDescriptor
class struct_WGPURenderBundleEncoderDescriptor(Structure):
    pass

struct_WGPURenderBundleEncoderDescriptor._pack_ = 1 # source:False
struct_WGPURenderBundleEncoderDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', WGPUStringView),
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
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
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
class struct_WGPURenderPassDescriptorExpandResolveRect(Structure):
    pass

struct_WGPURenderPassDescriptorExpandResolveRect._pack_ = 1 # source:False
struct_WGPURenderPassDescriptorExpandResolveRect._fields_ = [
    ('chain', WGPUChainedStruct),
    ('x', ctypes.c_uint32),
    ('y', ctypes.c_uint32),
    ('width', ctypes.c_uint32),
    ('height', ctypes.c_uint32),
]

WGPURenderPassDescriptorExpandResolveRect = struct_WGPURenderPassDescriptorExpandResolveRect
class struct_WGPURenderPassDescriptorResolveRect(Structure):
    pass

struct_WGPURenderPassDescriptorResolveRect._pack_ = 1 # source:False
struct_WGPURenderPassDescriptorResolveRect._fields_ = [
    ('chain', WGPUChainedStruct),
    ('colorOffsetX', ctypes.c_uint32),
    ('colorOffsetY', ctypes.c_uint32),
    ('resolveOffsetX', ctypes.c_uint32),
    ('resolveOffsetY', ctypes.c_uint32),
    ('width', ctypes.c_uint32),
    ('height', ctypes.c_uint32),
]

WGPURenderPassDescriptorResolveRect = struct_WGPURenderPassDescriptorResolveRect
class struct_WGPURenderPassMaxDrawCount(Structure):
    pass

struct_WGPURenderPassMaxDrawCount._pack_ = 1 # source:False
struct_WGPURenderPassMaxDrawCount._fields_ = [
    ('chain', WGPUChainedStruct),
    ('maxDrawCount', ctypes.c_uint64),
]

WGPURenderPassMaxDrawCount = struct_WGPURenderPassMaxDrawCount
class struct_WGPURequestAdapterWebGPUBackendOptions(Structure):
    _pack_ = 1 # source:False
    _fields_ = [
    ('chain', WGPUChainedStruct),
     ]

WGPURequestAdapterWebGPUBackendOptions = struct_WGPURequestAdapterWebGPUBackendOptions
class struct_WGPURequestAdapterWebXROptions(Structure):
    pass

struct_WGPURequestAdapterWebXROptions._pack_ = 1 # source:False
struct_WGPURequestAdapterWebXROptions._fields_ = [
    ('chain', WGPUChainedStruct),
    ('xrCompatible', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPURequestAdapterWebXROptions = struct_WGPURequestAdapterWebXROptions
class struct_WGPUResourceTableDescriptor(Structure):
    pass

struct_WGPUResourceTableDescriptor._pack_ = 1 # source:False
struct_WGPUResourceTableDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', WGPUStringView),
    ('size', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUResourceTableDescriptor = struct_WGPUResourceTableDescriptor
class struct_WGPUResourceTableLimits(Structure):
    pass

struct_WGPUResourceTableLimits._pack_ = 1 # source:False
struct_WGPUResourceTableLimits._fields_ = [
    ('chain', WGPUChainedStruct),
    ('maxResourceTableSize', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUResourceTableLimits = struct_WGPUResourceTableLimits
class struct_WGPUSamplerBindingLayout(Structure):
    pass

struct_WGPUSamplerBindingLayout._pack_ = 1 # source:False
struct_WGPUSamplerBindingLayout._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('type', WGPUSamplerBindingType),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSamplerBindingLayout = struct_WGPUSamplerBindingLayout
class struct_WGPUShaderModuleCompilationOptions(Structure):
    pass

struct_WGPUShaderModuleCompilationOptions._pack_ = 1 # source:False
struct_WGPUShaderModuleCompilationOptions._fields_ = [
    ('chain', WGPUChainedStruct),
    ('strictMath', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUShaderModuleCompilationOptions = struct_WGPUShaderModuleCompilationOptions
class struct_WGPUShaderSourceSPIRV(Structure):
    pass

struct_WGPUShaderSourceSPIRV._pack_ = 1 # source:False
struct_WGPUShaderSourceSPIRV._fields_ = [
    ('chain', WGPUChainedStruct),
    ('codeSize', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('code', ctypes.POINTER(ctypes.c_uint32)),
]

WGPUShaderSourceSPIRV = struct_WGPUShaderSourceSPIRV
class struct_WGPUShaderSourceWGSL(Structure):
    _pack_ = 1 # source:False
    _fields_ = [
    ('chain', WGPUChainedStruct),
    ('code', WGPUStringView),
     ]

WGPUShaderSourceWGSL = struct_WGPUShaderSourceWGSL
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
    ('label', WGPUStringView),
]

WGPUSharedBufferMemoryDescriptor = struct_WGPUSharedBufferMemoryDescriptor
class struct_WGPUSharedBufferMemoryEndAccessState(Structure):
    pass

struct_WGPUSharedBufferMemoryEndAccessState._pack_ = 1 # source:False
struct_WGPUSharedBufferMemoryEndAccessState._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
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
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('usage', ctypes.c_uint64),
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
    ('chain', WGPUChainedStruct),
    ('handle', ctypes.POINTER(None)),
]

WGPUSharedFenceDXGISharedHandleExportInfo = struct_WGPUSharedFenceDXGISharedHandleExportInfo
class struct_WGPUSharedFenceEGLSyncDescriptor(Structure):
    pass

struct_WGPUSharedFenceEGLSyncDescriptor._pack_ = 1 # source:False
struct_WGPUSharedFenceEGLSyncDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('sync', ctypes.POINTER(None)),
]

WGPUSharedFenceEGLSyncDescriptor = struct_WGPUSharedFenceEGLSyncDescriptor
class struct_WGPUSharedFenceEGLSyncExportInfo(Structure):
    pass

struct_WGPUSharedFenceEGLSyncExportInfo._pack_ = 1 # source:False
struct_WGPUSharedFenceEGLSyncExportInfo._fields_ = [
    ('chain', WGPUChainedStruct),
    ('sync', ctypes.POINTER(None)),
]

WGPUSharedFenceEGLSyncExportInfo = struct_WGPUSharedFenceEGLSyncExportInfo
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
    ('chain', WGPUChainedStruct),
    ('sharedEvent', ctypes.POINTER(None)),
]

WGPUSharedFenceMTLSharedEventExportInfo = struct_WGPUSharedFenceMTLSharedEventExportInfo
class struct_WGPUSharedFenceSyncFDDescriptor(Structure):
    pass

struct_WGPUSharedFenceSyncFDDescriptor._pack_ = 1 # source:False
struct_WGPUSharedFenceSyncFDDescriptor._fields_ = [
    ('chain', WGPUChainedStruct),
    ('handle', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSharedFenceSyncFDDescriptor = struct_WGPUSharedFenceSyncFDDescriptor
class struct_WGPUSharedFenceSyncFDExportInfo(Structure):
    pass

struct_WGPUSharedFenceSyncFDExportInfo._pack_ = 1 # source:False
struct_WGPUSharedFenceSyncFDExportInfo._fields_ = [
    ('chain', WGPUChainedStruct),
    ('handle', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSharedFenceSyncFDExportInfo = struct_WGPUSharedFenceSyncFDExportInfo
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
    ('chain', WGPUChainedStruct),
    ('handle', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSharedFenceVkSemaphoreOpaqueFDExportInfo = struct_WGPUSharedFenceVkSemaphoreOpaqueFDExportInfo
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
    ('chain', WGPUChainedStruct),
    ('handle', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSharedFenceVkSemaphoreZirconHandleExportInfo = struct_WGPUSharedFenceVkSemaphoreZirconHandleExportInfo
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
class struct_WGPUSharedTextureMemoryD3D11BeginState(Structure):
    pass

struct_WGPUSharedTextureMemoryD3D11BeginState._pack_ = 1 # source:False
struct_WGPUSharedTextureMemoryD3D11BeginState._fields_ = [
    ('chain', WGPUChainedStruct),
    ('requiresEndAccessFence', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSharedTextureMemoryD3D11BeginState = struct_WGPUSharedTextureMemoryD3D11BeginState
class struct_WGPUSharedTextureMemoryD3DSwapchainBeginState(Structure):
    pass

struct_WGPUSharedTextureMemoryD3DSwapchainBeginState._pack_ = 1 # source:False
struct_WGPUSharedTextureMemoryD3DSwapchainBeginState._fields_ = [
    ('chain', WGPUChainedStruct),
    ('isSwapchain', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSharedTextureMemoryD3DSwapchainBeginState = struct_WGPUSharedTextureMemoryD3DSwapchainBeginState
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
    ('allowStorageBinding', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSharedTextureMemoryIOSurfaceDescriptor = struct_WGPUSharedTextureMemoryIOSurfaceDescriptor
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
    ('chain', WGPUChainedStruct),
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
    ('sampledTextureBinding', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
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
class struct_WGPUSubgroupMatrixConfig(Structure):
    pass

struct_WGPUSubgroupMatrixConfig._pack_ = 1 # source:False
struct_WGPUSubgroupMatrixConfig._fields_ = [
    ('componentType', WGPUSubgroupMatrixComponentType),
    ('resultComponentType', WGPUSubgroupMatrixComponentType),
    ('M', ctypes.c_uint32),
    ('N', ctypes.c_uint32),
    ('K', ctypes.c_uint32),
]

WGPUSubgroupMatrixConfig = struct_WGPUSubgroupMatrixConfig
class struct_WGPUSupportedFeatures(Structure):
    pass

struct_WGPUSupportedFeatures._pack_ = 1 # source:False
struct_WGPUSupportedFeatures._fields_ = [
    ('featureCount', ctypes.c_uint64),
    ('features', ctypes.POINTER(WGPUFeatureName)),
]

WGPUSupportedFeatures = struct_WGPUSupportedFeatures
class struct_WGPUSupportedInstanceFeatures(Structure):
    pass

struct_WGPUSupportedInstanceFeatures._pack_ = 1 # source:False
struct_WGPUSupportedInstanceFeatures._fields_ = [
    ('featureCount', ctypes.c_uint64),
    ('features', ctypes.POINTER(WGPUInstanceFeatureName)),
]

WGPUSupportedInstanceFeatures = struct_WGPUSupportedInstanceFeatures
class struct_WGPUSupportedWGSLLanguageFeatures(Structure):
    pass

struct_WGPUSupportedWGSLLanguageFeatures._pack_ = 1 # source:False
struct_WGPUSupportedWGSLLanguageFeatures._fields_ = [
    ('featureCount', ctypes.c_uint64),
    ('features', ctypes.POINTER(WGPUWGSLLanguageFeatureName)),
]

WGPUSupportedWGSLLanguageFeatures = struct_WGPUSupportedWGSLLanguageFeatures
class struct_WGPUSurfaceCapabilities(Structure):
    pass

struct_WGPUSurfaceCapabilities._pack_ = 1 # source:False
struct_WGPUSurfaceCapabilities._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('usages', ctypes.c_uint64),
    ('formatCount', ctypes.c_uint64),
    ('formats', ctypes.POINTER(WGPUTextureFormat)),
    ('presentModeCount', ctypes.c_uint64),
    ('presentModes', ctypes.POINTER(WGPUPresentMode)),
    ('alphaModeCount', ctypes.c_uint64),
    ('alphaModes', ctypes.POINTER(WGPUCompositeAlphaMode)),
]

WGPUSurfaceCapabilities = struct_WGPUSurfaceCapabilities
class struct_WGPUSurfaceColorManagement(Structure):
    _pack_ = 1 # source:False
    _fields_ = [
    ('chain', WGPUChainedStruct),
    ('colorSpace', WGPUPredefinedColorSpace),
    ('toneMappingMode', WGPUToneMappingMode),
     ]

WGPUSurfaceColorManagement = struct_WGPUSurfaceColorManagement
class struct_WGPUSurfaceConfiguration(Structure):
    pass

struct_WGPUSurfaceConfiguration._pack_ = 1 # source:False
struct_WGPUSurfaceConfiguration._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('device', ctypes.POINTER(struct_WGPUDeviceImpl)),
    ('format', WGPUTextureFormat),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('usage', ctypes.c_uint64),
    ('width', ctypes.c_uint32),
    ('height', ctypes.c_uint32),
    ('viewFormatCount', ctypes.c_uint64),
    ('viewFormats', ctypes.POINTER(WGPUTextureFormat)),
    ('alphaMode', WGPUCompositeAlphaMode),
    ('presentMode', WGPUPresentMode),
]

WGPUSurfaceConfiguration = struct_WGPUSurfaceConfiguration
class struct_WGPUSurfaceDescriptorFromWindowsCoreWindow(Structure):
    pass

struct_WGPUSurfaceDescriptorFromWindowsCoreWindow._pack_ = 1 # source:False
struct_WGPUSurfaceDescriptorFromWindowsCoreWindow._fields_ = [
    ('chain', WGPUChainedStruct),
    ('coreWindow', ctypes.POINTER(None)),
]

WGPUSurfaceDescriptorFromWindowsCoreWindow = struct_WGPUSurfaceDescriptorFromWindowsCoreWindow
class struct_WGPUSurfaceDescriptorFromWindowsUWPSwapChainPanel(Structure):
    pass

struct_WGPUSurfaceDescriptorFromWindowsUWPSwapChainPanel._pack_ = 1 # source:False
struct_WGPUSurfaceDescriptorFromWindowsUWPSwapChainPanel._fields_ = [
    ('chain', WGPUChainedStruct),
    ('swapChainPanel', ctypes.POINTER(None)),
]

WGPUSurfaceDescriptorFromWindowsUWPSwapChainPanel = struct_WGPUSurfaceDescriptorFromWindowsUWPSwapChainPanel
class struct_WGPUSurfaceDescriptorFromWindowsWinUISwapChainPanel(Structure):
    pass

struct_WGPUSurfaceDescriptorFromWindowsWinUISwapChainPanel._pack_ = 1 # source:False
struct_WGPUSurfaceDescriptorFromWindowsWinUISwapChainPanel._fields_ = [
    ('chain', WGPUChainedStruct),
    ('swapChainPanel', ctypes.POINTER(None)),
]

WGPUSurfaceDescriptorFromWindowsWinUISwapChainPanel = struct_WGPUSurfaceDescriptorFromWindowsWinUISwapChainPanel
class struct_WGPUSurfaceSourceAndroidNativeWindow(Structure):
    pass

struct_WGPUSurfaceSourceAndroidNativeWindow._pack_ = 1 # source:False
struct_WGPUSurfaceSourceAndroidNativeWindow._fields_ = [
    ('chain', WGPUChainedStruct),
    ('window', ctypes.POINTER(None)),
]

WGPUSurfaceSourceAndroidNativeWindow = struct_WGPUSurfaceSourceAndroidNativeWindow
class struct_WGPUSurfaceSourceMetalLayer(Structure):
    pass

struct_WGPUSurfaceSourceMetalLayer._pack_ = 1 # source:False
struct_WGPUSurfaceSourceMetalLayer._fields_ = [
    ('chain', WGPUChainedStruct),
    ('layer', ctypes.POINTER(None)),
]

WGPUSurfaceSourceMetalLayer = struct_WGPUSurfaceSourceMetalLayer
class struct_WGPUSurfaceSourceWaylandSurface(Structure):
    pass

struct_WGPUSurfaceSourceWaylandSurface._pack_ = 1 # source:False
struct_WGPUSurfaceSourceWaylandSurface._fields_ = [
    ('chain', WGPUChainedStruct),
    ('display', ctypes.POINTER(None)),
    ('surface', ctypes.POINTER(None)),
]

WGPUSurfaceSourceWaylandSurface = struct_WGPUSurfaceSourceWaylandSurface
class struct_WGPUSurfaceSourceWindowsHWND(Structure):
    pass

struct_WGPUSurfaceSourceWindowsHWND._pack_ = 1 # source:False
struct_WGPUSurfaceSourceWindowsHWND._fields_ = [
    ('chain', WGPUChainedStruct),
    ('hinstance', ctypes.POINTER(None)),
    ('hwnd', ctypes.POINTER(None)),
]

WGPUSurfaceSourceWindowsHWND = struct_WGPUSurfaceSourceWindowsHWND
class struct_WGPUSurfaceSourceXCBWindow(Structure):
    pass

struct_WGPUSurfaceSourceXCBWindow._pack_ = 1 # source:False
struct_WGPUSurfaceSourceXCBWindow._fields_ = [
    ('chain', WGPUChainedStruct),
    ('connection', ctypes.POINTER(None)),
    ('window', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSurfaceSourceXCBWindow = struct_WGPUSurfaceSourceXCBWindow
class struct_WGPUSurfaceSourceXlibWindow(Structure):
    pass

struct_WGPUSurfaceSourceXlibWindow._pack_ = 1 # source:False
struct_WGPUSurfaceSourceXlibWindow._fields_ = [
    ('chain', WGPUChainedStruct),
    ('display', ctypes.POINTER(None)),
    ('window', ctypes.c_uint64),
]

WGPUSurfaceSourceXlibWindow = struct_WGPUSurfaceSourceXlibWindow
class struct_WGPUSurfaceTexture(Structure):
    pass

struct_WGPUSurfaceTexture._pack_ = 1 # source:False
struct_WGPUSurfaceTexture._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('texture', ctypes.POINTER(struct_WGPUTextureImpl)),
    ('status', WGPUSurfaceGetCurrentTextureStatus),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSurfaceTexture = struct_WGPUSurfaceTexture
class struct_WGPUTexelBufferBindingEntry(Structure):
    pass

struct_WGPUTexelBufferBindingEntry._pack_ = 1 # source:False
struct_WGPUTexelBufferBindingEntry._fields_ = [
    ('chain', WGPUChainedStruct),
    ('texelBufferView', ctypes.POINTER(struct_WGPUTexelBufferViewImpl)),
]

WGPUTexelBufferBindingEntry = struct_WGPUTexelBufferBindingEntry
class struct_WGPUTexelBufferBindingLayout(Structure):
    _pack_ = 1 # source:False
    _fields_ = [
    ('chain', WGPUChainedStruct),
    ('access', WGPUTexelBufferAccess),
    ('format', WGPUTextureFormat),
     ]

WGPUTexelBufferBindingLayout = struct_WGPUTexelBufferBindingLayout
class struct_WGPUTexelBufferViewDescriptor(Structure):
    pass

struct_WGPUTexelBufferViewDescriptor._pack_ = 1 # source:False
struct_WGPUTexelBufferViewDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', WGPUStringView),
    ('format', WGPUTextureFormat),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('offset', ctypes.c_uint64),
    ('size', ctypes.c_uint64),
]

WGPUTexelBufferViewDescriptor = struct_WGPUTexelBufferViewDescriptor
class struct_WGPUTexelCopyBufferLayout(Structure):
    pass

struct_WGPUTexelCopyBufferLayout._pack_ = 1 # source:False
struct_WGPUTexelCopyBufferLayout._fields_ = [
    ('offset', ctypes.c_uint64),
    ('bytesPerRow', ctypes.c_uint32),
    ('rowsPerImage', ctypes.c_uint32),
]

WGPUTexelCopyBufferLayout = struct_WGPUTexelCopyBufferLayout
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
class struct_WGPUTextureComponentSwizzle(Structure):
    _pack_ = 1 # source:False
    _fields_ = [
    ('r', WGPUComponentSwizzle),
    ('g', WGPUComponentSwizzle),
    ('b', WGPUComponentSwizzle),
    ('a', WGPUComponentSwizzle),
     ]

WGPUTextureComponentSwizzle = struct_WGPUTextureComponentSwizzle
class struct_WGPUVertexAttribute(Structure):
    pass

struct_WGPUVertexAttribute._pack_ = 1 # source:False
struct_WGPUVertexAttribute._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
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
class struct_WGPUAdapterPropertiesMemoryHeaps(Structure):
    pass

struct_WGPUAdapterPropertiesMemoryHeaps._pack_ = 1 # source:False
struct_WGPUAdapterPropertiesMemoryHeaps._fields_ = [
    ('chain', WGPUChainedStruct),
    ('heapCount', ctypes.c_uint64),
    ('heapInfo', ctypes.POINTER(struct_WGPUMemoryHeapInfo)),
]

WGPUAdapterPropertiesMemoryHeaps = struct_WGPUAdapterPropertiesMemoryHeaps
class struct_WGPUAdapterPropertiesSubgroupMatrixConfigs(Structure):
    pass

struct_WGPUAdapterPropertiesSubgroupMatrixConfigs._pack_ = 1 # source:False
struct_WGPUAdapterPropertiesSubgroupMatrixConfigs._fields_ = [
    ('chain', WGPUChainedStruct),
    ('configCount', ctypes.c_uint64),
    ('configs', ctypes.POINTER(struct_WGPUSubgroupMatrixConfig)),
]

WGPUAdapterPropertiesSubgroupMatrixConfigs = struct_WGPUAdapterPropertiesSubgroupMatrixConfigs
class struct_WGPUAHardwareBufferProperties(Structure):
    _pack_ = 1 # source:False
    _fields_ = [
    ('yCbCrInfo', WGPUYCbCrVkDescriptor),
     ]

WGPUAHardwareBufferProperties = struct_WGPUAHardwareBufferProperties
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
class struct_WGPUBindGroupLayoutDynamicBindingArray(Structure):
    _pack_ = 1 # source:False
    _fields_ = [
    ('chain', WGPUChainedStruct),
    ('dynamicArray', WGPUDynamicBindingArrayLayout),
     ]

WGPUBindGroupLayoutDynamicBindingArray = struct_WGPUBindGroupLayoutDynamicBindingArray
class struct_WGPUBindGroupLayoutEntry(Structure):
    pass

struct_WGPUBindGroupLayoutEntry._pack_ = 1 # source:False
struct_WGPUBindGroupLayoutEntry._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('binding', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('visibility', ctypes.c_uint64),
    ('bindingArraySize', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
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
class struct_WGPUBufferDescriptor(Structure):
    pass

struct_WGPUBufferDescriptor._pack_ = 1 # source:False
struct_WGPUBufferDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', WGPUStringView),
    ('usage', ctypes.c_uint64),
    ('size', ctypes.c_uint64),
    ('mappedAtCreation', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUBufferDescriptor = struct_WGPUBufferDescriptor
class struct_WGPUCommandEncoderDescriptor(Structure):
    pass

struct_WGPUCommandEncoderDescriptor._pack_ = 1 # source:False
struct_WGPUCommandEncoderDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', WGPUStringView),
]

WGPUCommandEncoderDescriptor = struct_WGPUCommandEncoderDescriptor
class struct_WGPUCompilationMessage(Structure):
    pass

struct_WGPUCompilationMessage._pack_ = 1 # source:False
struct_WGPUCompilationMessage._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('message', WGPUStringView),
    ('type', WGPUCompilationMessageType),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('lineNum', ctypes.c_uint64),
    ('linePos', ctypes.c_uint64),
    ('offset', ctypes.c_uint64),
    ('length', ctypes.c_uint64),
]

WGPUCompilationMessage = struct_WGPUCompilationMessage
class struct_WGPUComputePassDescriptor(Structure):
    pass

struct_WGPUComputePassDescriptor._pack_ = 1 # source:False
struct_WGPUComputePassDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', WGPUStringView),
    ('timestampWrites', ctypes.POINTER(struct_WGPUPassTimestampWrites)),
]

WGPUComputePassDescriptor = struct_WGPUComputePassDescriptor
class struct_WGPUComputeState(Structure):
    pass

struct_WGPUComputeState._pack_ = 1 # source:False
struct_WGPUComputeState._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('module', ctypes.POINTER(struct_WGPUShaderModuleImpl)),
    ('entryPoint', WGPUStringView),
    ('constantCount', ctypes.c_uint64),
    ('constants', ctypes.POINTER(struct_WGPUConstantEntry)),
]

WGPUComputeState = struct_WGPUComputeState
class struct_WGPUDawnDrmFormatCapabilities(Structure):
    pass

struct_WGPUDawnDrmFormatCapabilities._pack_ = 1 # source:False
struct_WGPUDawnDrmFormatCapabilities._fields_ = [
    ('chain', WGPUChainedStruct),
    ('propertiesCount', ctypes.c_uint64),
    ('properties', ctypes.POINTER(struct_WGPUDawnDrmFormatProperties)),
]

WGPUDawnDrmFormatCapabilities = struct_WGPUDawnDrmFormatCapabilities
class struct_WGPUDepthStencilState(Structure):
    pass

struct_WGPUDepthStencilState._pack_ = 1 # source:False
struct_WGPUDepthStencilState._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('format', WGPUTextureFormat),
    ('depthWriteEnabled', WGPUOptionalBool),
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
class struct_WGPUExternalTextureDescriptor(Structure):
    pass

struct_WGPUExternalTextureDescriptor._pack_ = 1 # source:False
struct_WGPUExternalTextureDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', WGPUStringView),
    ('plane0', ctypes.POINTER(struct_WGPUTextureViewImpl)),
    ('plane1', ctypes.POINTER(struct_WGPUTextureViewImpl)),
    ('cropOrigin', WGPUOrigin2D),
    ('cropSize', WGPUExtent2D),
    ('apparentSize', WGPUExtent2D),
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
class struct_WGPUInstanceDescriptor(Structure):
    pass

struct_WGPUInstanceDescriptor._pack_ = 1 # source:False
struct_WGPUInstanceDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('requiredFeatureCount', ctypes.c_uint64),
    ('requiredFeatures', ctypes.POINTER(WGPUInstanceFeatureName)),
    ('requiredLimits', ctypes.POINTER(struct_WGPUInstanceLimits)),
]

WGPUInstanceDescriptor = struct_WGPUInstanceDescriptor
class struct_WGPULimits(Structure):
    pass

struct_WGPULimits._pack_ = 1 # source:False
struct_WGPULimits._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
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
    ('maxInterStageShaderVariables', ctypes.c_uint32),
    ('maxColorAttachments', ctypes.c_uint32),
    ('maxColorAttachmentBytesPerSample', ctypes.c_uint32),
    ('maxComputeWorkgroupStorageSize', ctypes.c_uint32),
    ('maxComputeInvocationsPerWorkgroup', ctypes.c_uint32),
    ('maxComputeWorkgroupSizeX', ctypes.c_uint32),
    ('maxComputeWorkgroupSizeY', ctypes.c_uint32),
    ('maxComputeWorkgroupSizeZ', ctypes.c_uint32),
    ('maxComputeWorkgroupsPerDimension', ctypes.c_uint32),
    ('maxImmediateSize', ctypes.c_uint32),
]

WGPULimits = struct_WGPULimits
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
class struct_WGPURequestAdapterOptions(Structure):
    pass

struct_WGPURequestAdapterOptions._pack_ = 1 # source:False
struct_WGPURequestAdapterOptions._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('featureLevel', WGPUFeatureLevel),
    ('powerPreference', WGPUPowerPreference),
    ('forceFallbackAdapter', ctypes.c_uint32),
    ('backendType', WGPUBackendType),
    ('compatibleSurface', ctypes.POINTER(struct_WGPUSurfaceImpl)),
]

WGPURequestAdapterOptions = struct_WGPURequestAdapterOptions
class struct_WGPUSamplerDescriptor(Structure):
    pass

struct_WGPUSamplerDescriptor._pack_ = 1 # source:False
struct_WGPUSamplerDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', WGPUStringView),
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
class struct_WGPUShaderModuleDescriptor(Structure):
    pass

struct_WGPUShaderModuleDescriptor._pack_ = 1 # source:False
struct_WGPUShaderModuleDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', WGPUStringView),
]

WGPUShaderModuleDescriptor = struct_WGPUShaderModuleDescriptor
class struct_WGPUSharedFenceDescriptor(Structure):
    pass

struct_WGPUSharedFenceDescriptor._pack_ = 1 # source:False
struct_WGPUSharedFenceDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', WGPUStringView),
]

WGPUSharedFenceDescriptor = struct_WGPUSharedFenceDescriptor
class struct_WGPUSharedFenceExportInfo(Structure):
    pass

struct_WGPUSharedFenceExportInfo._pack_ = 1 # source:False
struct_WGPUSharedFenceExportInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('type', WGPUSharedFenceType),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUSharedFenceExportInfo = struct_WGPUSharedFenceExportInfo
class struct_WGPUSharedTextureMemoryAHardwareBufferProperties(Structure):
    _pack_ = 1 # source:False
    _fields_ = [
    ('chain', WGPUChainedStruct),
    ('yCbCrInfo', WGPUYCbCrVkDescriptor),
     ]

WGPUSharedTextureMemoryAHardwareBufferProperties = struct_WGPUSharedTextureMemoryAHardwareBufferProperties
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
class struct_WGPUSharedTextureMemoryMetalEndAccessState(Structure):
    _pack_ = 1 # source:False
    _fields_ = [
    ('chain', WGPUChainedStruct),
    ('commandsScheduledFuture', WGPUFuture),
     ]

WGPUSharedTextureMemoryMetalEndAccessState = struct_WGPUSharedTextureMemoryMetalEndAccessState
class struct_WGPUSurfaceDescriptor(Structure):
    pass

struct_WGPUSurfaceDescriptor._pack_ = 1 # source:False
struct_WGPUSurfaceDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', WGPUStringView),
]

WGPUSurfaceDescriptor = struct_WGPUSurfaceDescriptor
class struct_WGPUTexelCopyBufferInfo(Structure):
    pass

struct_WGPUTexelCopyBufferInfo._pack_ = 1 # source:False
struct_WGPUTexelCopyBufferInfo._fields_ = [
    ('layout', WGPUTexelCopyBufferLayout),
    ('buffer', ctypes.POINTER(struct_WGPUBufferImpl)),
]

WGPUTexelCopyBufferInfo = struct_WGPUTexelCopyBufferInfo
class struct_WGPUTexelCopyTextureInfo(Structure):
    pass

struct_WGPUTexelCopyTextureInfo._pack_ = 1 # source:False
struct_WGPUTexelCopyTextureInfo._fields_ = [
    ('texture', ctypes.POINTER(struct_WGPUTextureImpl)),
    ('mipLevel', ctypes.c_uint32),
    ('origin', WGPUOrigin3D),
    ('aspect', WGPUTextureAspect),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUTexelCopyTextureInfo = struct_WGPUTexelCopyTextureInfo
class struct_WGPUTextureComponentSwizzleDescriptor(Structure):
    _pack_ = 1 # source:False
    _fields_ = [
    ('chain', WGPUChainedStruct),
    ('swizzle', WGPUTextureComponentSwizzle),
     ]

WGPUTextureComponentSwizzleDescriptor = struct_WGPUTextureComponentSwizzleDescriptor
class struct_WGPUTextureDescriptor(Structure):
    pass

struct_WGPUTextureDescriptor._pack_ = 1 # source:False
struct_WGPUTextureDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', WGPUStringView),
    ('usage', ctypes.c_uint64),
    ('dimension', WGPUTextureDimension),
    ('size', WGPUExtent3D),
    ('format', WGPUTextureFormat),
    ('mipLevelCount', ctypes.c_uint32),
    ('sampleCount', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('viewFormatCount', ctypes.c_uint64),
    ('viewFormats', ctypes.POINTER(WGPUTextureFormat)),
]

WGPUTextureDescriptor = struct_WGPUTextureDescriptor
class struct_WGPUVertexBufferLayout(Structure):
    pass

struct_WGPUVertexBufferLayout._pack_ = 1 # source:False
struct_WGPUVertexBufferLayout._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('stepMode', WGPUVertexStepMode),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('arrayStride', ctypes.c_uint64),
    ('attributeCount', ctypes.c_uint64),
    ('attributes', ctypes.POINTER(struct_WGPUVertexAttribute)),
]

WGPUVertexBufferLayout = struct_WGPUVertexBufferLayout
class struct_WGPUAdapterInfo(Structure):
    pass

struct_WGPUAdapterInfo._pack_ = 1 # source:False
struct_WGPUAdapterInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('vendor', WGPUStringView),
    ('architecture', WGPUStringView),
    ('device', WGPUStringView),
    ('description', WGPUStringView),
    ('backendType', WGPUBackendType),
    ('adapterType', WGPUAdapterType),
    ('vendorID', ctypes.c_uint32),
    ('deviceID', ctypes.c_uint32),
    ('subgroupMinSize', ctypes.c_uint32),
    ('subgroupMaxSize', ctypes.c_uint32),
]

WGPUAdapterInfo = struct_WGPUAdapterInfo
class struct_WGPUBindGroupDescriptor(Structure):
    pass

struct_WGPUBindGroupDescriptor._pack_ = 1 # source:False
struct_WGPUBindGroupDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', WGPUStringView),
    ('layout', ctypes.POINTER(struct_WGPUBindGroupLayoutImpl)),
    ('entryCount', ctypes.c_uint64),
    ('entries', ctypes.POINTER(struct_WGPUBindGroupEntry)),
]

WGPUBindGroupDescriptor = struct_WGPUBindGroupDescriptor
class struct_WGPUBindGroupLayoutDescriptor(Structure):
    pass

struct_WGPUBindGroupLayoutDescriptor._pack_ = 1 # source:False
struct_WGPUBindGroupLayoutDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', WGPUStringView),
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
    ('writeMask', ctypes.c_uint64),
]

WGPUColorTargetState = struct_WGPUColorTargetState
struct_WGPUCompilationInfo._pack_ = 1 # source:False
struct_WGPUCompilationInfo._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('messageCount', ctypes.c_uint64),
    ('messages', ctypes.POINTER(struct_WGPUCompilationMessage)),
]

WGPUCompilationInfo = struct_WGPUCompilationInfo
class struct_WGPUComputePipelineDescriptor(Structure):
    pass

struct_WGPUComputePipelineDescriptor._pack_ = 1 # source:False
struct_WGPUComputePipelineDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', WGPUStringView),
    ('layout', ctypes.POINTER(struct_WGPUPipelineLayoutImpl)),
    ('compute', WGPUComputeState),
]

WGPUComputePipelineDescriptor = struct_WGPUComputePipelineDescriptor
class struct_WGPUDawnFormatCapabilities(Structure):
    pass

struct_WGPUDawnFormatCapabilities._pack_ = 1 # source:False
struct_WGPUDawnFormatCapabilities._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
]

WGPUDawnFormatCapabilities = struct_WGPUDawnFormatCapabilities
class struct_WGPUDeviceDescriptor(Structure):
    pass

struct_WGPUDeviceDescriptor._pack_ = 1 # source:False
struct_WGPUDeviceDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', WGPUStringView),
    ('requiredFeatureCount', ctypes.c_uint64),
    ('requiredFeatures', ctypes.POINTER(WGPUFeatureName)),
    ('requiredLimits', ctypes.POINTER(struct_WGPULimits)),
    ('defaultQueue', WGPUQueueDescriptor),
    ('deviceLostCallbackInfo', WGPUDeviceLostCallbackInfo),
    ('uncapturedErrorCallbackInfo', WGPUUncapturedErrorCallbackInfo),
]

WGPUDeviceDescriptor = struct_WGPUDeviceDescriptor
class struct_WGPUPipelineLayoutDescriptor(Structure):
    pass

struct_WGPUPipelineLayoutDescriptor._pack_ = 1 # source:False
struct_WGPUPipelineLayoutDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', WGPUStringView),
    ('bindGroupLayoutCount', ctypes.c_uint64),
    ('bindGroupLayouts', ctypes.POINTER(ctypes.POINTER(struct_WGPUBindGroupLayoutImpl))),
    ('immediateSize', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
]

WGPUPipelineLayoutDescriptor = struct_WGPUPipelineLayoutDescriptor
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
class struct_WGPUSharedTextureMemoryDescriptor(Structure):
    pass

struct_WGPUSharedTextureMemoryDescriptor._pack_ = 1 # source:False
struct_WGPUSharedTextureMemoryDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', WGPUStringView),
]

WGPUSharedTextureMemoryDescriptor = struct_WGPUSharedTextureMemoryDescriptor
class struct_WGPUSharedTextureMemoryEndAccessState(Structure):
    pass

struct_WGPUSharedTextureMemoryEndAccessState._pack_ = 1 # source:False
struct_WGPUSharedTextureMemoryEndAccessState._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('initialized', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('fenceCount', ctypes.c_uint64),
    ('fences', ctypes.POINTER(ctypes.POINTER(struct_WGPUSharedFenceImpl))),
    ('signaledValues', ctypes.POINTER(ctypes.c_uint64)),
]

WGPUSharedTextureMemoryEndAccessState = struct_WGPUSharedTextureMemoryEndAccessState
class struct_WGPUSharedTextureMemoryProperties(Structure):
    pass

struct_WGPUSharedTextureMemoryProperties._pack_ = 1 # source:False
struct_WGPUSharedTextureMemoryProperties._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('usage', ctypes.c_uint64),
    ('size', WGPUExtent3D),
    ('format', WGPUTextureFormat),
]

WGPUSharedTextureMemoryProperties = struct_WGPUSharedTextureMemoryProperties
class struct_WGPUTextureViewDescriptor(Structure):
    pass

struct_WGPUTextureViewDescriptor._pack_ = 1 # source:False
struct_WGPUTextureViewDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', WGPUStringView),
    ('format', WGPUTextureFormat),
    ('dimension', WGPUTextureViewDimension),
    ('baseMipLevel', ctypes.c_uint32),
    ('mipLevelCount', ctypes.c_uint32),
    ('baseArrayLayer', ctypes.c_uint32),
    ('arrayLayerCount', ctypes.c_uint32),
    ('aspect', WGPUTextureAspect),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('usage', ctypes.c_uint64),
]

WGPUTextureViewDescriptor = struct_WGPUTextureViewDescriptor
class struct_WGPUVertexState(Structure):
    pass

struct_WGPUVertexState._pack_ = 1 # source:False
struct_WGPUVertexState._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('module', ctypes.POINTER(struct_WGPUShaderModuleImpl)),
    ('entryPoint', WGPUStringView),
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
    ('entryPoint', WGPUStringView),
    ('constantCount', ctypes.c_uint64),
    ('constants', ctypes.POINTER(struct_WGPUConstantEntry)),
    ('targetCount', ctypes.c_uint64),
    ('targets', ctypes.POINTER(struct_WGPUColorTargetState)),
]

WGPUFragmentState = struct_WGPUFragmentState
class struct_WGPURenderPassDescriptor(Structure):
    pass

struct_WGPURenderPassDescriptor._pack_ = 1 # source:False
struct_WGPURenderPassDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', WGPUStringView),
    ('colorAttachmentCount', ctypes.c_uint64),
    ('colorAttachments', ctypes.POINTER(struct_WGPURenderPassColorAttachment)),
    ('depthStencilAttachment', ctypes.POINTER(struct_WGPURenderPassDepthStencilAttachment)),
    ('occlusionQuerySet', ctypes.POINTER(struct_WGPUQuerySetImpl)),
    ('timestampWrites', ctypes.POINTER(struct_WGPUPassTimestampWrites)),
]

WGPURenderPassDescriptor = struct_WGPURenderPassDescriptor
class struct_WGPURenderPipelineDescriptor(Structure):
    pass

struct_WGPURenderPipelineDescriptor._pack_ = 1 # source:False
struct_WGPURenderPipelineDescriptor._fields_ = [
    ('nextInChain', ctypes.POINTER(struct_WGPUChainedStruct)),
    ('label', WGPUStringView),
    ('layout', ctypes.POINTER(struct_WGPUPipelineLayoutImpl)),
    ('vertex', WGPUVertexState),
    ('primitive', WGPUPrimitiveState),
    ('depthStencil', ctypes.POINTER(struct_WGPUDepthStencilState)),
    ('multisample', WGPUMultisampleState),
    ('fragment', ctypes.POINTER(struct_WGPUFragmentState)),
]

WGPURenderPipelineDescriptor = struct_WGPURenderPipelineDescriptor
try:
    emscripten_webgpu_get_device = _libraries['FIXME_STUB'].emscripten_webgpu_get_device
    emscripten_webgpu_get_device.restype = WGPUDevice
    emscripten_webgpu_get_device.argtypes = []
except AttributeError:
    pass
WGPUProcCreateInstance = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUInstanceImpl), ctypes.POINTER(struct_WGPUInstanceDescriptor))
WGPUProcGetInstanceFeatures = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSupportedInstanceFeatures))
WGPUProcGetInstanceLimits = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUInstanceLimits))
WGPUProcHasInstanceFeature = ctypes.CFUNCTYPE(ctypes.c_uint32, WGPUInstanceFeatureName)
WGPUProcGetProcAddress = ctypes.CFUNCTYPE(ctypes.CFUNCTYPE(None), struct_WGPUStringView)
WGPUProcAdapterCreateDevice = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUAdapterImpl), ctypes.POINTER(struct_WGPUDeviceDescriptor))
WGPUProcAdapterGetFeatures = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUAdapterImpl), ctypes.POINTER(struct_WGPUSupportedFeatures))
WGPUProcAdapterGetFormatCapabilities = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUAdapterImpl), WGPUTextureFormat, ctypes.POINTER(struct_WGPUDawnFormatCapabilities))
WGPUProcAdapterGetInfo = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUAdapterImpl), ctypes.POINTER(struct_WGPUAdapterInfo))
WGPUProcAdapterGetInstance = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUInstanceImpl), ctypes.POINTER(struct_WGPUAdapterImpl))
WGPUProcAdapterGetLimits = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUAdapterImpl), ctypes.POINTER(struct_WGPULimits))
WGPUProcAdapterHasFeature = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUAdapterImpl), WGPUFeatureName)
WGPUProcAdapterRequestDevice = ctypes.CFUNCTYPE(struct_WGPUFuture, ctypes.POINTER(struct_WGPUAdapterImpl), ctypes.POINTER(struct_WGPUDeviceDescriptor), struct_WGPURequestDeviceCallbackInfo)
WGPUProcAdapterAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUAdapterImpl))
WGPUProcAdapterRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUAdapterImpl))
WGPUProcAdapterInfoFreeMembers = ctypes.CFUNCTYPE(None, struct_WGPUAdapterInfo)
WGPUProcAdapterPropertiesMemoryHeapsFreeMembers = ctypes.CFUNCTYPE(None, struct_WGPUAdapterPropertiesMemoryHeaps)
WGPUProcAdapterPropertiesSubgroupMatrixConfigsFreeMembers = ctypes.CFUNCTYPE(None, struct_WGPUAdapterPropertiesSubgroupMatrixConfigs)
WGPUProcBindGroupDestroy = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUBindGroupImpl))
WGPUProcBindGroupInsertBinding = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUBindGroupImpl), ctypes.POINTER(struct_WGPUBindGroupEntryContents))
WGPUProcBindGroupRemoveBinding = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUBindGroupImpl), ctypes.c_uint32)
WGPUProcBindGroupSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUBindGroupImpl), struct_WGPUStringView)
WGPUProcBindGroupUpdate = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUBindGroupImpl), ctypes.POINTER(struct_WGPUBindGroupEntry))
WGPUProcBindGroupAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUBindGroupImpl))
WGPUProcBindGroupRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUBindGroupImpl))
WGPUProcBindGroupLayoutSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUBindGroupLayoutImpl), struct_WGPUStringView)
WGPUProcBindGroupLayoutAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUBindGroupLayoutImpl))
WGPUProcBindGroupLayoutRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUBindGroupLayoutImpl))
WGPUProcBufferCreateTexelView = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUTexelBufferViewImpl), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.POINTER(struct_WGPUTexelBufferViewDescriptor))
WGPUProcBufferDestroy = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUBufferImpl))
WGPUProcBufferGetConstMappedRange = ctypes.CFUNCTYPE(ctypes.POINTER(None), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64, ctypes.c_uint64)
WGPUProcBufferGetMappedRange = ctypes.CFUNCTYPE(ctypes.POINTER(None), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64, ctypes.c_uint64)
WGPUProcBufferGetMapState = ctypes.CFUNCTYPE(WGPUBufferMapState, ctypes.POINTER(struct_WGPUBufferImpl))
WGPUProcBufferGetSize = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.POINTER(struct_WGPUBufferImpl))
WGPUProcBufferGetUsage = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.POINTER(struct_WGPUBufferImpl))
WGPUProcBufferMapAsync = ctypes.CFUNCTYPE(struct_WGPUFuture, ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, struct_WGPUBufferMapCallbackInfo)
WGPUProcBufferReadMappedRange = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64, ctypes.POINTER(None), ctypes.c_uint64)
WGPUProcBufferSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUBufferImpl), struct_WGPUStringView)
WGPUProcBufferUnmap = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUBufferImpl))
WGPUProcBufferWriteMappedRange = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64, ctypes.POINTER(None), ctypes.c_uint64)
WGPUProcBufferAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUBufferImpl))
WGPUProcBufferRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUBufferImpl))
WGPUProcCommandBufferSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandBufferImpl), struct_WGPUStringView)
WGPUProcCommandBufferAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandBufferImpl))
WGPUProcCommandBufferRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandBufferImpl))
WGPUProcCommandEncoderBeginComputePass = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUComputePassEncoderImpl), ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(struct_WGPUComputePassDescriptor))
WGPUProcCommandEncoderBeginRenderPass = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(struct_WGPURenderPassDescriptor))
WGPUProcCommandEncoderClearBuffer = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64, ctypes.c_uint64)
WGPUProcCommandEncoderCopyBufferToBuffer = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64, ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64, ctypes.c_uint64)
WGPUProcCommandEncoderCopyBufferToTexture = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(struct_WGPUTexelCopyBufferInfo), ctypes.POINTER(struct_WGPUTexelCopyTextureInfo), ctypes.POINTER(struct_WGPUExtent3D))
WGPUProcCommandEncoderCopyTextureToBuffer = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(struct_WGPUTexelCopyTextureInfo), ctypes.POINTER(struct_WGPUTexelCopyBufferInfo), ctypes.POINTER(struct_WGPUExtent3D))
WGPUProcCommandEncoderCopyTextureToTexture = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(struct_WGPUTexelCopyTextureInfo), ctypes.POINTER(struct_WGPUTexelCopyTextureInfo), ctypes.POINTER(struct_WGPUExtent3D))
WGPUProcCommandEncoderFinish = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUCommandBufferImpl), ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(struct_WGPUCommandBufferDescriptor))
WGPUProcCommandEncoderInjectValidationError = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl), struct_WGPUStringView)
WGPUProcCommandEncoderInsertDebugMarker = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl), struct_WGPUStringView)
WGPUProcCommandEncoderPopDebugGroup = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl))
WGPUProcCommandEncoderPushDebugGroup = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl), struct_WGPUStringView)
WGPUProcCommandEncoderResolveQuerySet = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(struct_WGPUQuerySetImpl), ctypes.c_uint32, ctypes.c_uint32, ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64)
WGPUProcCommandEncoderSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl), struct_WGPUStringView)
WGPUProcCommandEncoderSetResourceTable = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(struct_WGPUResourceTableImpl))
WGPUProcCommandEncoderWriteBuffer = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_uint64)
WGPUProcCommandEncoderWriteTimestamp = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(struct_WGPUQuerySetImpl), ctypes.c_uint32)
WGPUProcCommandEncoderAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl))
WGPUProcCommandEncoderRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUCommandEncoderImpl))
WGPUProcComputePassEncoderDispatchWorkgroups = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePassEncoderImpl), ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32)
WGPUProcComputePassEncoderDispatchWorkgroupsIndirect = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePassEncoderImpl), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64)
WGPUProcComputePassEncoderEnd = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePassEncoderImpl))
WGPUProcComputePassEncoderInsertDebugMarker = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePassEncoderImpl), struct_WGPUStringView)
WGPUProcComputePassEncoderPopDebugGroup = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePassEncoderImpl))
WGPUProcComputePassEncoderPushDebugGroup = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePassEncoderImpl), struct_WGPUStringView)
WGPUProcComputePassEncoderSetBindGroup = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePassEncoderImpl), ctypes.c_uint32, ctypes.POINTER(struct_WGPUBindGroupImpl), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint32))
WGPUProcComputePassEncoderSetImmediates = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePassEncoderImpl), ctypes.c_uint32, ctypes.POINTER(None), ctypes.c_uint64)
WGPUProcComputePassEncoderSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePassEncoderImpl), struct_WGPUStringView)
WGPUProcComputePassEncoderSetPipeline = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePassEncoderImpl), ctypes.POINTER(struct_WGPUComputePipelineImpl))
WGPUProcComputePassEncoderWriteTimestamp = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePassEncoderImpl), ctypes.POINTER(struct_WGPUQuerySetImpl), ctypes.c_uint32)
WGPUProcComputePassEncoderAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePassEncoderImpl))
WGPUProcComputePassEncoderRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePassEncoderImpl))
WGPUProcComputePipelineGetBindGroupLayout = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUBindGroupLayoutImpl), ctypes.POINTER(struct_WGPUComputePipelineImpl), ctypes.c_uint32)
WGPUProcComputePipelineSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePipelineImpl), struct_WGPUStringView)
WGPUProcComputePipelineAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePipelineImpl))
WGPUProcComputePipelineRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUComputePipelineImpl))
WGPUProcDawnDrmFormatCapabilitiesFreeMembers = ctypes.CFUNCTYPE(None, struct_WGPUDawnDrmFormatCapabilities)
WGPUProcDeviceCreateBindGroup = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUBindGroupImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUBindGroupDescriptor))
WGPUProcDeviceCreateBindGroupLayout = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUBindGroupLayoutImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUBindGroupLayoutDescriptor))
WGPUProcDeviceCreateBuffer = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUBufferImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUBufferDescriptor))
WGPUProcDeviceCreateCommandEncoder = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUCommandEncoderImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUCommandEncoderDescriptor))
WGPUProcDeviceCreateComputePipeline = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUComputePipelineImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUComputePipelineDescriptor))
WGPUProcDeviceCreateComputePipelineAsync = ctypes.CFUNCTYPE(struct_WGPUFuture, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUComputePipelineDescriptor), struct_WGPUCreateComputePipelineAsyncCallbackInfo)
WGPUProcDeviceCreateErrorBuffer = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUBufferImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUBufferDescriptor))
WGPUProcDeviceCreateErrorExternalTexture = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUExternalTextureImpl), ctypes.POINTER(struct_WGPUDeviceImpl))
WGPUProcDeviceCreateErrorShaderModule = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUShaderModuleImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUShaderModuleDescriptor), struct_WGPUStringView)
WGPUProcDeviceCreateErrorTexture = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUTextureImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUTextureDescriptor))
WGPUProcDeviceCreateExternalTexture = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUExternalTextureImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUExternalTextureDescriptor))
WGPUProcDeviceCreatePipelineLayout = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUPipelineLayoutImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUPipelineLayoutDescriptor))
WGPUProcDeviceCreateQuerySet = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUQuerySetImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUQuerySetDescriptor))
WGPUProcDeviceCreateRenderBundleEncoder = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPURenderBundleEncoderImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPURenderBundleEncoderDescriptor))
WGPUProcDeviceCreateRenderPipeline = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPURenderPipelineImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPURenderPipelineDescriptor))
WGPUProcDeviceCreateRenderPipelineAsync = ctypes.CFUNCTYPE(struct_WGPUFuture, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPURenderPipelineDescriptor), struct_WGPUCreateRenderPipelineAsyncCallbackInfo)
WGPUProcDeviceCreateResourceTable = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUResourceTableImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUResourceTableDescriptor))
WGPUProcDeviceCreateSampler = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUSamplerImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUSamplerDescriptor))
WGPUProcDeviceCreateShaderModule = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUShaderModuleImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUShaderModuleDescriptor))
WGPUProcDeviceCreateTexture = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUTextureImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUTextureDescriptor))
WGPUProcDeviceDestroy = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl))
WGPUProcDeviceForceLoss = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl), WGPUDeviceLostReason, struct_WGPUStringView)
WGPUProcDeviceGetAdapter = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUAdapterImpl), ctypes.POINTER(struct_WGPUDeviceImpl))
WGPUProcDeviceGetAdapterInfo = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUAdapterInfo))
WGPUProcDeviceGetAHardwareBufferProperties = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(None), ctypes.POINTER(struct_WGPUAHardwareBufferProperties))
WGPUProcDeviceGetFeatures = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUSupportedFeatures))
WGPUProcDeviceGetLimits = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPULimits))
WGPUProcDeviceGetLostFuture = ctypes.CFUNCTYPE(struct_WGPUFuture, ctypes.POINTER(struct_WGPUDeviceImpl))
WGPUProcDeviceGetQueue = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUQueueImpl), ctypes.POINTER(struct_WGPUDeviceImpl))
WGPUProcDeviceHasFeature = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUDeviceImpl), WGPUFeatureName)
WGPUProcDeviceImportSharedBufferMemory = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUSharedBufferMemoryImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUSharedBufferMemoryDescriptor))
WGPUProcDeviceImportSharedFence = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUSharedFenceImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUSharedFenceDescriptor))
WGPUProcDeviceImportSharedTextureMemory = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUSharedTextureMemoryImpl), ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUSharedTextureMemoryDescriptor))
WGPUProcDeviceInjectError = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl), WGPUErrorType, struct_WGPUStringView)
WGPUProcDevicePopErrorScope = ctypes.CFUNCTYPE(struct_WGPUFuture, ctypes.POINTER(struct_WGPUDeviceImpl), struct_WGPUPopErrorScopeCallbackInfo)
WGPUProcDevicePushErrorScope = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl), WGPUErrorFilter)
WGPUProcDeviceSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl), struct_WGPUStringView)
WGPUProcDeviceSetLoggingCallback = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl), struct_WGPULoggingCallbackInfo)
WGPUProcDeviceTick = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl))
WGPUProcDeviceValidateTextureDescriptor = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl), ctypes.POINTER(struct_WGPUTextureDescriptor))
WGPUProcDeviceAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl))
WGPUProcDeviceRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUDeviceImpl))
WGPUProcExternalTextureDestroy = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUExternalTextureImpl))
WGPUProcExternalTextureExpire = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUExternalTextureImpl))
WGPUProcExternalTextureRefresh = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUExternalTextureImpl))
WGPUProcExternalTextureSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUExternalTextureImpl), struct_WGPUStringView)
WGPUProcExternalTextureAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUExternalTextureImpl))
WGPUProcExternalTextureRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUExternalTextureImpl))
WGPUProcInstanceCreateSurface = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUSurfaceImpl), ctypes.POINTER(struct_WGPUInstanceImpl), ctypes.POINTER(struct_WGPUSurfaceDescriptor))
WGPUProcInstanceGetWGSLLanguageFeatures = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUInstanceImpl), ctypes.POINTER(struct_WGPUSupportedWGSLLanguageFeatures))
WGPUProcInstanceHasWGSLLanguageFeature = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUInstanceImpl), WGPUWGSLLanguageFeatureName)
WGPUProcInstanceProcessEvents = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUInstanceImpl))
WGPUProcInstanceRequestAdapter = ctypes.CFUNCTYPE(struct_WGPUFuture, ctypes.POINTER(struct_WGPUInstanceImpl), ctypes.POINTER(struct_WGPURequestAdapterOptions), struct_WGPURequestAdapterCallbackInfo)
WGPUProcInstanceWaitAny = ctypes.CFUNCTYPE(WGPUWaitStatus, ctypes.POINTER(struct_WGPUInstanceImpl), ctypes.c_uint64, ctypes.POINTER(struct_WGPUFutureWaitInfo), ctypes.c_uint64)
WGPUProcInstanceAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUInstanceImpl))
WGPUProcInstanceRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUInstanceImpl))
WGPUProcPipelineLayoutSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUPipelineLayoutImpl), struct_WGPUStringView)
WGPUProcPipelineLayoutAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUPipelineLayoutImpl))
WGPUProcPipelineLayoutRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUPipelineLayoutImpl))
WGPUProcQuerySetDestroy = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUQuerySetImpl))
WGPUProcQuerySetGetCount = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUQuerySetImpl))
WGPUProcQuerySetGetType = ctypes.CFUNCTYPE(WGPUQueryType, ctypes.POINTER(struct_WGPUQuerySetImpl))
WGPUProcQuerySetSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUQuerySetImpl), struct_WGPUStringView)
WGPUProcQuerySetAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUQuerySetImpl))
WGPUProcQuerySetRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUQuerySetImpl))
WGPUProcQueueCopyExternalTextureForBrowser = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUQueueImpl), ctypes.POINTER(struct_WGPUImageCopyExternalTexture), ctypes.POINTER(struct_WGPUTexelCopyTextureInfo), ctypes.POINTER(struct_WGPUExtent3D), ctypes.POINTER(struct_WGPUCopyTextureForBrowserOptions))
WGPUProcQueueCopyTextureForBrowser = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUQueueImpl), ctypes.POINTER(struct_WGPUTexelCopyTextureInfo), ctypes.POINTER(struct_WGPUTexelCopyTextureInfo), ctypes.POINTER(struct_WGPUExtent3D), ctypes.POINTER(struct_WGPUCopyTextureForBrowserOptions))
WGPUProcQueueOnSubmittedWorkDone = ctypes.CFUNCTYPE(struct_WGPUFuture, ctypes.POINTER(struct_WGPUQueueImpl), struct_WGPUQueueWorkDoneCallbackInfo)
WGPUProcQueueSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUQueueImpl), struct_WGPUStringView)
WGPUProcQueueSubmit = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUQueueImpl), ctypes.c_uint64, ctypes.POINTER(ctypes.POINTER(struct_WGPUCommandBufferImpl)))
WGPUProcQueueWriteBuffer = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUQueueImpl), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64, ctypes.POINTER(None), ctypes.c_uint64)
WGPUProcQueueWriteTexture = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUQueueImpl), ctypes.POINTER(struct_WGPUTexelCopyTextureInfo), ctypes.POINTER(None), ctypes.c_uint64, ctypes.POINTER(struct_WGPUTexelCopyBufferLayout), ctypes.POINTER(struct_WGPUExtent3D))
WGPUProcQueueAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUQueueImpl))
WGPUProcQueueRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUQueueImpl))
WGPUProcRenderBundleSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleImpl), struct_WGPUStringView)
WGPUProcRenderBundleAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleImpl))
WGPUProcRenderBundleRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleImpl))
WGPUProcRenderBundleEncoderDraw = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleEncoderImpl), ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32)
WGPUProcRenderBundleEncoderDrawIndexed = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleEncoderImpl), ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_int32, ctypes.c_uint32)
WGPUProcRenderBundleEncoderDrawIndexedIndirect = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleEncoderImpl), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64)
WGPUProcRenderBundleEncoderDrawIndirect = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleEncoderImpl), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64)
WGPUProcRenderBundleEncoderFinish = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPURenderBundleImpl), ctypes.POINTER(struct_WGPURenderBundleEncoderImpl), ctypes.POINTER(struct_WGPURenderBundleDescriptor))
WGPUProcRenderBundleEncoderInsertDebugMarker = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleEncoderImpl), struct_WGPUStringView)
WGPUProcRenderBundleEncoderPopDebugGroup = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleEncoderImpl))
WGPUProcRenderBundleEncoderPushDebugGroup = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleEncoderImpl), struct_WGPUStringView)
WGPUProcRenderBundleEncoderSetBindGroup = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleEncoderImpl), ctypes.c_uint32, ctypes.POINTER(struct_WGPUBindGroupImpl), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint32))
WGPUProcRenderBundleEncoderSetImmediates = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleEncoderImpl), ctypes.c_uint32, ctypes.POINTER(None), ctypes.c_uint64)
WGPUProcRenderBundleEncoderSetIndexBuffer = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleEncoderImpl), ctypes.POINTER(struct_WGPUBufferImpl), WGPUIndexFormat, ctypes.c_uint64, ctypes.c_uint64)
WGPUProcRenderBundleEncoderSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderBundleEncoderImpl), struct_WGPUStringView)
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
WGPUProcRenderPassEncoderInsertDebugMarker = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), struct_WGPUStringView)
WGPUProcRenderPassEncoderMultiDrawIndexedIndirect = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64, ctypes.c_uint32, ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64)
WGPUProcRenderPassEncoderMultiDrawIndirect = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64, ctypes.c_uint32, ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64)
WGPUProcRenderPassEncoderPixelLocalStorageBarrier = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl))
WGPUProcRenderPassEncoderPopDebugGroup = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl))
WGPUProcRenderPassEncoderPushDebugGroup = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), struct_WGPUStringView)
WGPUProcRenderPassEncoderSetBindGroup = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.c_uint32, ctypes.POINTER(struct_WGPUBindGroupImpl), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint32))
WGPUProcRenderPassEncoderSetBlendConstant = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.POINTER(struct_WGPUColor))
WGPUProcRenderPassEncoderSetImmediates = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.c_uint32, ctypes.POINTER(None), ctypes.c_uint64)
WGPUProcRenderPassEncoderSetIndexBuffer = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.POINTER(struct_WGPUBufferImpl), WGPUIndexFormat, ctypes.c_uint64, ctypes.c_uint64)
WGPUProcRenderPassEncoderSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), struct_WGPUStringView)
WGPUProcRenderPassEncoderSetPipeline = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.POINTER(struct_WGPURenderPipelineImpl))
WGPUProcRenderPassEncoderSetScissorRect = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32)
WGPUProcRenderPassEncoderSetStencilReference = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.c_uint32)
WGPUProcRenderPassEncoderSetVertexBuffer = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.c_uint32, ctypes.POINTER(struct_WGPUBufferImpl), ctypes.c_uint64, ctypes.c_uint64)
WGPUProcRenderPassEncoderSetViewport = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float)
WGPUProcRenderPassEncoderWriteTimestamp = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl), ctypes.POINTER(struct_WGPUQuerySetImpl), ctypes.c_uint32)
WGPUProcRenderPassEncoderAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl))
WGPUProcRenderPassEncoderRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPassEncoderImpl))
WGPUProcRenderPipelineGetBindGroupLayout = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUBindGroupLayoutImpl), ctypes.POINTER(struct_WGPURenderPipelineImpl), ctypes.c_uint32)
WGPUProcRenderPipelineSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPipelineImpl), struct_WGPUStringView)
WGPUProcRenderPipelineAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPipelineImpl))
WGPUProcRenderPipelineRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPURenderPipelineImpl))
WGPUProcResourceTableDestroy = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUResourceTableImpl))
WGPUProcResourceTableAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUResourceTableImpl))
WGPUProcResourceTableRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUResourceTableImpl))
WGPUProcSamplerSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSamplerImpl), struct_WGPUStringView)
WGPUProcSamplerAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSamplerImpl))
WGPUProcSamplerRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSamplerImpl))
WGPUProcShaderModuleGetCompilationInfo = ctypes.CFUNCTYPE(struct_WGPUFuture, ctypes.POINTER(struct_WGPUShaderModuleImpl), struct_WGPUCompilationInfoCallbackInfo)
WGPUProcShaderModuleSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUShaderModuleImpl), struct_WGPUStringView)
WGPUProcShaderModuleAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUShaderModuleImpl))
WGPUProcShaderModuleRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUShaderModuleImpl))
WGPUProcSharedBufferMemoryBeginAccess = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUSharedBufferMemoryImpl), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.POINTER(struct_WGPUSharedBufferMemoryBeginAccessDescriptor))
WGPUProcSharedBufferMemoryCreateBuffer = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUBufferImpl), ctypes.POINTER(struct_WGPUSharedBufferMemoryImpl), ctypes.POINTER(struct_WGPUBufferDescriptor))
WGPUProcSharedBufferMemoryEndAccess = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUSharedBufferMemoryImpl), ctypes.POINTER(struct_WGPUBufferImpl), ctypes.POINTER(struct_WGPUSharedBufferMemoryEndAccessState))
WGPUProcSharedBufferMemoryGetProperties = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUSharedBufferMemoryImpl), ctypes.POINTER(struct_WGPUSharedBufferMemoryProperties))
WGPUProcSharedBufferMemoryIsDeviceLost = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUSharedBufferMemoryImpl))
WGPUProcSharedBufferMemorySetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSharedBufferMemoryImpl), struct_WGPUStringView)
WGPUProcSharedBufferMemoryAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSharedBufferMemoryImpl))
WGPUProcSharedBufferMemoryRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSharedBufferMemoryImpl))
WGPUProcSharedBufferMemoryEndAccessStateFreeMembers = ctypes.CFUNCTYPE(None, struct_WGPUSharedBufferMemoryEndAccessState)
WGPUProcSharedFenceExportInfo = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSharedFenceImpl), ctypes.POINTER(struct_WGPUSharedFenceExportInfo))
WGPUProcSharedFenceAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSharedFenceImpl))
WGPUProcSharedFenceRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSharedFenceImpl))
WGPUProcSharedTextureMemoryBeginAccess = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUSharedTextureMemoryImpl), ctypes.POINTER(struct_WGPUTextureImpl), ctypes.POINTER(struct_WGPUSharedTextureMemoryBeginAccessDescriptor))
WGPUProcSharedTextureMemoryCreateTexture = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUTextureImpl), ctypes.POINTER(struct_WGPUSharedTextureMemoryImpl), ctypes.POINTER(struct_WGPUTextureDescriptor))
WGPUProcSharedTextureMemoryEndAccess = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUSharedTextureMemoryImpl), ctypes.POINTER(struct_WGPUTextureImpl), ctypes.POINTER(struct_WGPUSharedTextureMemoryEndAccessState))
WGPUProcSharedTextureMemoryGetProperties = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUSharedTextureMemoryImpl), ctypes.POINTER(struct_WGPUSharedTextureMemoryProperties))
WGPUProcSharedTextureMemoryIsDeviceLost = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUSharedTextureMemoryImpl))
WGPUProcSharedTextureMemorySetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSharedTextureMemoryImpl), struct_WGPUStringView)
WGPUProcSharedTextureMemoryAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSharedTextureMemoryImpl))
WGPUProcSharedTextureMemoryRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSharedTextureMemoryImpl))
WGPUProcSharedTextureMemoryEndAccessStateFreeMembers = ctypes.CFUNCTYPE(None, struct_WGPUSharedTextureMemoryEndAccessState)
WGPUProcSupportedFeaturesFreeMembers = ctypes.CFUNCTYPE(None, struct_WGPUSupportedFeatures)
WGPUProcSupportedInstanceFeaturesFreeMembers = ctypes.CFUNCTYPE(None, struct_WGPUSupportedInstanceFeatures)
WGPUProcSupportedWGSLLanguageFeaturesFreeMembers = ctypes.CFUNCTYPE(None, struct_WGPUSupportedWGSLLanguageFeatures)
WGPUProcSurfaceConfigure = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSurfaceImpl), ctypes.POINTER(struct_WGPUSurfaceConfiguration))
WGPUProcSurfaceGetCapabilities = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUSurfaceImpl), ctypes.POINTER(struct_WGPUAdapterImpl), ctypes.POINTER(struct_WGPUSurfaceCapabilities))
WGPUProcSurfaceGetCurrentTexture = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSurfaceImpl), ctypes.POINTER(struct_WGPUSurfaceTexture))
WGPUProcSurfacePresent = ctypes.CFUNCTYPE(WGPUStatus, ctypes.POINTER(struct_WGPUSurfaceImpl))
WGPUProcSurfaceSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSurfaceImpl), struct_WGPUStringView)
WGPUProcSurfaceUnconfigure = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSurfaceImpl))
WGPUProcSurfaceAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSurfaceImpl))
WGPUProcSurfaceRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUSurfaceImpl))
WGPUProcSurfaceCapabilitiesFreeMembers = ctypes.CFUNCTYPE(None, struct_WGPUSurfaceCapabilities)
WGPUProcTexelBufferViewSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUTexelBufferViewImpl), struct_WGPUStringView)
WGPUProcTexelBufferViewAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUTexelBufferViewImpl))
WGPUProcTexelBufferViewRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUTexelBufferViewImpl))
WGPUProcTextureCreateErrorView = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUTextureViewImpl), ctypes.POINTER(struct_WGPUTextureImpl), ctypes.POINTER(struct_WGPUTextureViewDescriptor))
WGPUProcTextureCreateView = ctypes.CFUNCTYPE(ctypes.POINTER(struct_WGPUTextureViewImpl), ctypes.POINTER(struct_WGPUTextureImpl), ctypes.POINTER(struct_WGPUTextureViewDescriptor))
WGPUProcTextureDestroy = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUTextureImpl))
WGPUProcTextureGetDepthOrArrayLayers = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUTextureImpl))
WGPUProcTextureGetDimension = ctypes.CFUNCTYPE(WGPUTextureDimension, ctypes.POINTER(struct_WGPUTextureImpl))
WGPUProcTextureGetFormat = ctypes.CFUNCTYPE(WGPUTextureFormat, ctypes.POINTER(struct_WGPUTextureImpl))
WGPUProcTextureGetHeight = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUTextureImpl))
WGPUProcTextureGetMipLevelCount = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUTextureImpl))
WGPUProcTextureGetSampleCount = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUTextureImpl))
WGPUProcTextureGetUsage = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.POINTER(struct_WGPUTextureImpl))
WGPUProcTextureGetWidth = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(struct_WGPUTextureImpl))
WGPUProcTexturePin = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUTextureImpl), ctypes.c_uint64)
WGPUProcTextureSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUTextureImpl), struct_WGPUStringView)
WGPUProcTextureUnpin = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUTextureImpl))
WGPUProcTextureAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUTextureImpl))
WGPUProcTextureRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUTextureImpl))
WGPUProcTextureViewSetLabel = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUTextureViewImpl), struct_WGPUStringView)
WGPUProcTextureViewAddRef = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUTextureViewImpl))
WGPUProcTextureViewRelease = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_WGPUTextureViewImpl))
try:
    wgpuCreateInstance = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuCreateInstance
    wgpuCreateInstance.restype = WGPUInstance
    wgpuCreateInstance.argtypes = [ctypes.POINTER(struct_WGPUInstanceDescriptor)]
except AttributeError:
    pass
try:
    wgpuGetInstanceFeatures = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuGetInstanceFeatures
    wgpuGetInstanceFeatures.restype = None
    wgpuGetInstanceFeatures.argtypes = [ctypes.POINTER(struct_WGPUSupportedInstanceFeatures)]
except AttributeError:
    pass
try:
    wgpuGetInstanceLimits = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuGetInstanceLimits
    wgpuGetInstanceLimits.restype = WGPUStatus
    wgpuGetInstanceLimits.argtypes = [ctypes.POINTER(struct_WGPUInstanceLimits)]
except AttributeError:
    pass
try:
    wgpuHasInstanceFeature = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuHasInstanceFeature
    wgpuHasInstanceFeature.restype = WGPUBool
    wgpuHasInstanceFeature.argtypes = [WGPUInstanceFeatureName]
except AttributeError:
    pass
try:
    wgpuGetProcAddress = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuGetProcAddress
    wgpuGetProcAddress.restype = WGPUProc
    wgpuGetProcAddress.argtypes = [WGPUStringView]
except AttributeError:
    pass
try:
    wgpuAdapterCreateDevice = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuAdapterCreateDevice
    wgpuAdapterCreateDevice.restype = WGPUDevice
    wgpuAdapterCreateDevice.argtypes = [WGPUAdapter, ctypes.POINTER(struct_WGPUDeviceDescriptor)]
except AttributeError:
    pass
try:
    wgpuAdapterGetFeatures = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuAdapterGetFeatures
    wgpuAdapterGetFeatures.restype = None
    wgpuAdapterGetFeatures.argtypes = [WGPUAdapter, ctypes.POINTER(struct_WGPUSupportedFeatures)]
except AttributeError:
    pass
try:
    wgpuAdapterGetFormatCapabilities = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuAdapterGetFormatCapabilities
    wgpuAdapterGetFormatCapabilities.restype = WGPUStatus
    wgpuAdapterGetFormatCapabilities.argtypes = [WGPUAdapter, WGPUTextureFormat, ctypes.POINTER(struct_WGPUDawnFormatCapabilities)]
except AttributeError:
    pass
try:
    wgpuAdapterGetInfo = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuAdapterGetInfo
    wgpuAdapterGetInfo.restype = WGPUStatus
    wgpuAdapterGetInfo.argtypes = [WGPUAdapter, ctypes.POINTER(struct_WGPUAdapterInfo)]
except AttributeError:
    pass
try:
    wgpuAdapterGetInstance = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuAdapterGetInstance
    wgpuAdapterGetInstance.restype = WGPUInstance
    wgpuAdapterGetInstance.argtypes = [WGPUAdapter]
except AttributeError:
    pass
try:
    wgpuAdapterGetLimits = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuAdapterGetLimits
    wgpuAdapterGetLimits.restype = WGPUStatus
    wgpuAdapterGetLimits.argtypes = [WGPUAdapter, ctypes.POINTER(struct_WGPULimits)]
except AttributeError:
    pass
try:
    wgpuAdapterHasFeature = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuAdapterHasFeature
    wgpuAdapterHasFeature.restype = WGPUBool
    wgpuAdapterHasFeature.argtypes = [WGPUAdapter, WGPUFeatureName]
except AttributeError:
    pass
try:
    wgpuAdapterRequestDevice = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuAdapterRequestDevice
    wgpuAdapterRequestDevice.restype = WGPUFuture
    wgpuAdapterRequestDevice.argtypes = [WGPUAdapter, ctypes.POINTER(struct_WGPUDeviceDescriptor), WGPURequestDeviceCallbackInfo]
except AttributeError:
    pass
try:
    wgpuAdapterAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuAdapterAddRef
    wgpuAdapterAddRef.restype = None
    wgpuAdapterAddRef.argtypes = [WGPUAdapter]
except AttributeError:
    pass
try:
    wgpuAdapterRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuAdapterRelease
    wgpuAdapterRelease.restype = None
    wgpuAdapterRelease.argtypes = [WGPUAdapter]
except AttributeError:
    pass
try:
    wgpuAdapterInfoFreeMembers = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuAdapterInfoFreeMembers
    wgpuAdapterInfoFreeMembers.restype = None
    wgpuAdapterInfoFreeMembers.argtypes = [WGPUAdapterInfo]
except AttributeError:
    pass
try:
    wgpuAdapterPropertiesMemoryHeapsFreeMembers = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuAdapterPropertiesMemoryHeapsFreeMembers
    wgpuAdapterPropertiesMemoryHeapsFreeMembers.restype = None
    wgpuAdapterPropertiesMemoryHeapsFreeMembers.argtypes = [WGPUAdapterPropertiesMemoryHeaps]
except AttributeError:
    pass
try:
    wgpuAdapterPropertiesSubgroupMatrixConfigsFreeMembers = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuAdapterPropertiesSubgroupMatrixConfigsFreeMembers
    wgpuAdapterPropertiesSubgroupMatrixConfigsFreeMembers.restype = None
    wgpuAdapterPropertiesSubgroupMatrixConfigsFreeMembers.argtypes = [WGPUAdapterPropertiesSubgroupMatrixConfigs]
except AttributeError:
    pass
try:
    wgpuBindGroupDestroy = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuBindGroupDestroy
    wgpuBindGroupDestroy.restype = None
    wgpuBindGroupDestroy.argtypes = [WGPUBindGroup]
except AttributeError:
    pass
uint32_t = ctypes.c_uint32
try:
    wgpuBindGroupInsertBinding = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuBindGroupInsertBinding
    wgpuBindGroupInsertBinding.restype = uint32_t
    wgpuBindGroupInsertBinding.argtypes = [WGPUBindGroup, ctypes.POINTER(struct_WGPUBindGroupEntryContents)]
except AttributeError:
    pass
try:
    wgpuBindGroupRemoveBinding = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuBindGroupRemoveBinding
    wgpuBindGroupRemoveBinding.restype = WGPUStatus
    wgpuBindGroupRemoveBinding.argtypes = [WGPUBindGroup, uint32_t]
except AttributeError:
    pass
try:
    wgpuBindGroupSetLabel = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuBindGroupSetLabel
    wgpuBindGroupSetLabel.restype = None
    wgpuBindGroupSetLabel.argtypes = [WGPUBindGroup, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuBindGroupUpdate = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuBindGroupUpdate
    wgpuBindGroupUpdate.restype = WGPUStatus
    wgpuBindGroupUpdate.argtypes = [WGPUBindGroup, ctypes.POINTER(struct_WGPUBindGroupEntry)]
except AttributeError:
    pass
try:
    wgpuBindGroupAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuBindGroupAddRef
    wgpuBindGroupAddRef.restype = None
    wgpuBindGroupAddRef.argtypes = [WGPUBindGroup]
except AttributeError:
    pass
try:
    wgpuBindGroupRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuBindGroupRelease
    wgpuBindGroupRelease.restype = None
    wgpuBindGroupRelease.argtypes = [WGPUBindGroup]
except AttributeError:
    pass
try:
    wgpuBindGroupLayoutSetLabel = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuBindGroupLayoutSetLabel
    wgpuBindGroupLayoutSetLabel.restype = None
    wgpuBindGroupLayoutSetLabel.argtypes = [WGPUBindGroupLayout, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuBindGroupLayoutAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuBindGroupLayoutAddRef
    wgpuBindGroupLayoutAddRef.restype = None
    wgpuBindGroupLayoutAddRef.argtypes = [WGPUBindGroupLayout]
except AttributeError:
    pass
try:
    wgpuBindGroupLayoutRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuBindGroupLayoutRelease
    wgpuBindGroupLayoutRelease.restype = None
    wgpuBindGroupLayoutRelease.argtypes = [WGPUBindGroupLayout]
except AttributeError:
    pass
try:
    wgpuBufferCreateTexelView = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuBufferCreateTexelView
    wgpuBufferCreateTexelView.restype = WGPUTexelBufferView
    wgpuBufferCreateTexelView.argtypes = [WGPUBuffer, ctypes.POINTER(struct_WGPUTexelBufferViewDescriptor)]
except AttributeError:
    pass
try:
    wgpuBufferDestroy = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuBufferDestroy
    wgpuBufferDestroy.restype = None
    wgpuBufferDestroy.argtypes = [WGPUBuffer]
except AttributeError:
    pass
size_t = ctypes.c_uint64
try:
    wgpuBufferGetConstMappedRange = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuBufferGetConstMappedRange
    wgpuBufferGetConstMappedRange.restype = ctypes.POINTER(None)
    wgpuBufferGetConstMappedRange.argtypes = [WGPUBuffer, size_t, size_t]
except AttributeError:
    pass
try:
    wgpuBufferGetMappedRange = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuBufferGetMappedRange
    wgpuBufferGetMappedRange.restype = ctypes.POINTER(None)
    wgpuBufferGetMappedRange.argtypes = [WGPUBuffer, size_t, size_t]
except AttributeError:
    pass
try:
    wgpuBufferGetMapState = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuBufferGetMapState
    wgpuBufferGetMapState.restype = WGPUBufferMapState
    wgpuBufferGetMapState.argtypes = [WGPUBuffer]
except AttributeError:
    pass
uint64_t = ctypes.c_uint64
try:
    wgpuBufferGetSize = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuBufferGetSize
    wgpuBufferGetSize.restype = uint64_t
    wgpuBufferGetSize.argtypes = [WGPUBuffer]
except AttributeError:
    pass
try:
    wgpuBufferGetUsage = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuBufferGetUsage
    wgpuBufferGetUsage.restype = WGPUBufferUsage
    wgpuBufferGetUsage.argtypes = [WGPUBuffer]
except AttributeError:
    pass
try:
    wgpuBufferMapAsync = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuBufferMapAsync
    wgpuBufferMapAsync.restype = WGPUFuture
    wgpuBufferMapAsync.argtypes = [WGPUBuffer, WGPUMapMode, size_t, size_t, WGPUBufferMapCallbackInfo]
except AttributeError:
    pass
try:
    wgpuBufferReadMappedRange = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuBufferReadMappedRange
    wgpuBufferReadMappedRange.restype = WGPUStatus
    wgpuBufferReadMappedRange.argtypes = [WGPUBuffer, size_t, ctypes.POINTER(None), size_t]
except AttributeError:
    pass
try:
    wgpuBufferSetLabel = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuBufferSetLabel
    wgpuBufferSetLabel.restype = None
    wgpuBufferSetLabel.argtypes = [WGPUBuffer, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuBufferUnmap = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuBufferUnmap
    wgpuBufferUnmap.restype = None
    wgpuBufferUnmap.argtypes = [WGPUBuffer]
except AttributeError:
    pass
try:
    wgpuBufferWriteMappedRange = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuBufferWriteMappedRange
    wgpuBufferWriteMappedRange.restype = WGPUStatus
    wgpuBufferWriteMappedRange.argtypes = [WGPUBuffer, size_t, ctypes.POINTER(None), size_t]
except AttributeError:
    pass
try:
    wgpuBufferAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuBufferAddRef
    wgpuBufferAddRef.restype = None
    wgpuBufferAddRef.argtypes = [WGPUBuffer]
except AttributeError:
    pass
try:
    wgpuBufferRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuBufferRelease
    wgpuBufferRelease.restype = None
    wgpuBufferRelease.argtypes = [WGPUBuffer]
except AttributeError:
    pass
try:
    wgpuCommandBufferSetLabel = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuCommandBufferSetLabel
    wgpuCommandBufferSetLabel.restype = None
    wgpuCommandBufferSetLabel.argtypes = [WGPUCommandBuffer, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuCommandBufferAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuCommandBufferAddRef
    wgpuCommandBufferAddRef.restype = None
    wgpuCommandBufferAddRef.argtypes = [WGPUCommandBuffer]
except AttributeError:
    pass
try:
    wgpuCommandBufferRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuCommandBufferRelease
    wgpuCommandBufferRelease.restype = None
    wgpuCommandBufferRelease.argtypes = [WGPUCommandBuffer]
except AttributeError:
    pass
try:
    wgpuCommandEncoderBeginComputePass = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuCommandEncoderBeginComputePass
    wgpuCommandEncoderBeginComputePass.restype = WGPUComputePassEncoder
    wgpuCommandEncoderBeginComputePass.argtypes = [WGPUCommandEncoder, ctypes.POINTER(struct_WGPUComputePassDescriptor)]
except AttributeError:
    pass
try:
    wgpuCommandEncoderBeginRenderPass = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuCommandEncoderBeginRenderPass
    wgpuCommandEncoderBeginRenderPass.restype = WGPURenderPassEncoder
    wgpuCommandEncoderBeginRenderPass.argtypes = [WGPUCommandEncoder, ctypes.POINTER(struct_WGPURenderPassDescriptor)]
except AttributeError:
    pass
try:
    wgpuCommandEncoderClearBuffer = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuCommandEncoderClearBuffer
    wgpuCommandEncoderClearBuffer.restype = None
    wgpuCommandEncoderClearBuffer.argtypes = [WGPUCommandEncoder, WGPUBuffer, uint64_t, uint64_t]
except AttributeError:
    pass
try:
    wgpuCommandEncoderCopyBufferToBuffer = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuCommandEncoderCopyBufferToBuffer
    wgpuCommandEncoderCopyBufferToBuffer.restype = None
    wgpuCommandEncoderCopyBufferToBuffer.argtypes = [WGPUCommandEncoder, WGPUBuffer, uint64_t, WGPUBuffer, uint64_t, uint64_t]
except AttributeError:
    pass
try:
    wgpuCommandEncoderCopyBufferToTexture = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuCommandEncoderCopyBufferToTexture
    wgpuCommandEncoderCopyBufferToTexture.restype = None
    wgpuCommandEncoderCopyBufferToTexture.argtypes = [WGPUCommandEncoder, ctypes.POINTER(struct_WGPUTexelCopyBufferInfo), ctypes.POINTER(struct_WGPUTexelCopyTextureInfo), ctypes.POINTER(struct_WGPUExtent3D)]
except AttributeError:
    pass
try:
    wgpuCommandEncoderCopyTextureToBuffer = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuCommandEncoderCopyTextureToBuffer
    wgpuCommandEncoderCopyTextureToBuffer.restype = None
    wgpuCommandEncoderCopyTextureToBuffer.argtypes = [WGPUCommandEncoder, ctypes.POINTER(struct_WGPUTexelCopyTextureInfo), ctypes.POINTER(struct_WGPUTexelCopyBufferInfo), ctypes.POINTER(struct_WGPUExtent3D)]
except AttributeError:
    pass
try:
    wgpuCommandEncoderCopyTextureToTexture = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuCommandEncoderCopyTextureToTexture
    wgpuCommandEncoderCopyTextureToTexture.restype = None
    wgpuCommandEncoderCopyTextureToTexture.argtypes = [WGPUCommandEncoder, ctypes.POINTER(struct_WGPUTexelCopyTextureInfo), ctypes.POINTER(struct_WGPUTexelCopyTextureInfo), ctypes.POINTER(struct_WGPUExtent3D)]
except AttributeError:
    pass
try:
    wgpuCommandEncoderFinish = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuCommandEncoderFinish
    wgpuCommandEncoderFinish.restype = WGPUCommandBuffer
    wgpuCommandEncoderFinish.argtypes = [WGPUCommandEncoder, ctypes.POINTER(struct_WGPUCommandBufferDescriptor)]
except AttributeError:
    pass
try:
    wgpuCommandEncoderInjectValidationError = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuCommandEncoderInjectValidationError
    wgpuCommandEncoderInjectValidationError.restype = None
    wgpuCommandEncoderInjectValidationError.argtypes = [WGPUCommandEncoder, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuCommandEncoderInsertDebugMarker = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuCommandEncoderInsertDebugMarker
    wgpuCommandEncoderInsertDebugMarker.restype = None
    wgpuCommandEncoderInsertDebugMarker.argtypes = [WGPUCommandEncoder, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuCommandEncoderPopDebugGroup = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuCommandEncoderPopDebugGroup
    wgpuCommandEncoderPopDebugGroup.restype = None
    wgpuCommandEncoderPopDebugGroup.argtypes = [WGPUCommandEncoder]
except AttributeError:
    pass
try:
    wgpuCommandEncoderPushDebugGroup = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuCommandEncoderPushDebugGroup
    wgpuCommandEncoderPushDebugGroup.restype = None
    wgpuCommandEncoderPushDebugGroup.argtypes = [WGPUCommandEncoder, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuCommandEncoderResolveQuerySet = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuCommandEncoderResolveQuerySet
    wgpuCommandEncoderResolveQuerySet.restype = None
    wgpuCommandEncoderResolveQuerySet.argtypes = [WGPUCommandEncoder, WGPUQuerySet, uint32_t, uint32_t, WGPUBuffer, uint64_t]
except AttributeError:
    pass
try:
    wgpuCommandEncoderSetLabel = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuCommandEncoderSetLabel
    wgpuCommandEncoderSetLabel.restype = None
    wgpuCommandEncoderSetLabel.argtypes = [WGPUCommandEncoder, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuCommandEncoderSetResourceTable = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuCommandEncoderSetResourceTable
    wgpuCommandEncoderSetResourceTable.restype = None
    wgpuCommandEncoderSetResourceTable.argtypes = [WGPUCommandEncoder, WGPUResourceTable]
except AttributeError:
    pass
try:
    wgpuCommandEncoderWriteBuffer = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuCommandEncoderWriteBuffer
    wgpuCommandEncoderWriteBuffer.restype = None
    wgpuCommandEncoderWriteBuffer.argtypes = [WGPUCommandEncoder, WGPUBuffer, uint64_t, ctypes.POINTER(ctypes.c_ubyte), uint64_t]
except AttributeError:
    pass
try:
    wgpuCommandEncoderWriteTimestamp = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuCommandEncoderWriteTimestamp
    wgpuCommandEncoderWriteTimestamp.restype = None
    wgpuCommandEncoderWriteTimestamp.argtypes = [WGPUCommandEncoder, WGPUQuerySet, uint32_t]
except AttributeError:
    pass
try:
    wgpuCommandEncoderAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuCommandEncoderAddRef
    wgpuCommandEncoderAddRef.restype = None
    wgpuCommandEncoderAddRef.argtypes = [WGPUCommandEncoder]
except AttributeError:
    pass
try:
    wgpuCommandEncoderRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuCommandEncoderRelease
    wgpuCommandEncoderRelease.restype = None
    wgpuCommandEncoderRelease.argtypes = [WGPUCommandEncoder]
except AttributeError:
    pass
try:
    wgpuComputePassEncoderDispatchWorkgroups = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuComputePassEncoderDispatchWorkgroups
    wgpuComputePassEncoderDispatchWorkgroups.restype = None
    wgpuComputePassEncoderDispatchWorkgroups.argtypes = [WGPUComputePassEncoder, uint32_t, uint32_t, uint32_t]
except AttributeError:
    pass
try:
    wgpuComputePassEncoderDispatchWorkgroupsIndirect = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuComputePassEncoderDispatchWorkgroupsIndirect
    wgpuComputePassEncoderDispatchWorkgroupsIndirect.restype = None
    wgpuComputePassEncoderDispatchWorkgroupsIndirect.argtypes = [WGPUComputePassEncoder, WGPUBuffer, uint64_t]
except AttributeError:
    pass
try:
    wgpuComputePassEncoderEnd = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuComputePassEncoderEnd
    wgpuComputePassEncoderEnd.restype = None
    wgpuComputePassEncoderEnd.argtypes = [WGPUComputePassEncoder]
except AttributeError:
    pass
try:
    wgpuComputePassEncoderInsertDebugMarker = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuComputePassEncoderInsertDebugMarker
    wgpuComputePassEncoderInsertDebugMarker.restype = None
    wgpuComputePassEncoderInsertDebugMarker.argtypes = [WGPUComputePassEncoder, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuComputePassEncoderPopDebugGroup = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuComputePassEncoderPopDebugGroup
    wgpuComputePassEncoderPopDebugGroup.restype = None
    wgpuComputePassEncoderPopDebugGroup.argtypes = [WGPUComputePassEncoder]
except AttributeError:
    pass
try:
    wgpuComputePassEncoderPushDebugGroup = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuComputePassEncoderPushDebugGroup
    wgpuComputePassEncoderPushDebugGroup.restype = None
    wgpuComputePassEncoderPushDebugGroup.argtypes = [WGPUComputePassEncoder, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuComputePassEncoderSetBindGroup = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuComputePassEncoderSetBindGroup
    wgpuComputePassEncoderSetBindGroup.restype = None
    wgpuComputePassEncoderSetBindGroup.argtypes = [WGPUComputePassEncoder, uint32_t, WGPUBindGroup, size_t, ctypes.POINTER(ctypes.c_uint32)]
except AttributeError:
    pass
try:
    wgpuComputePassEncoderSetImmediates = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuComputePassEncoderSetImmediates
    wgpuComputePassEncoderSetImmediates.restype = None
    wgpuComputePassEncoderSetImmediates.argtypes = [WGPUComputePassEncoder, uint32_t, ctypes.POINTER(None), size_t]
except AttributeError:
    pass
try:
    wgpuComputePassEncoderSetLabel = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuComputePassEncoderSetLabel
    wgpuComputePassEncoderSetLabel.restype = None
    wgpuComputePassEncoderSetLabel.argtypes = [WGPUComputePassEncoder, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuComputePassEncoderSetPipeline = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuComputePassEncoderSetPipeline
    wgpuComputePassEncoderSetPipeline.restype = None
    wgpuComputePassEncoderSetPipeline.argtypes = [WGPUComputePassEncoder, WGPUComputePipeline]
except AttributeError:
    pass
try:
    wgpuComputePassEncoderWriteTimestamp = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuComputePassEncoderWriteTimestamp
    wgpuComputePassEncoderWriteTimestamp.restype = None
    wgpuComputePassEncoderWriteTimestamp.argtypes = [WGPUComputePassEncoder, WGPUQuerySet, uint32_t]
except AttributeError:
    pass
try:
    wgpuComputePassEncoderAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuComputePassEncoderAddRef
    wgpuComputePassEncoderAddRef.restype = None
    wgpuComputePassEncoderAddRef.argtypes = [WGPUComputePassEncoder]
except AttributeError:
    pass
try:
    wgpuComputePassEncoderRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuComputePassEncoderRelease
    wgpuComputePassEncoderRelease.restype = None
    wgpuComputePassEncoderRelease.argtypes = [WGPUComputePassEncoder]
except AttributeError:
    pass
try:
    wgpuComputePipelineGetBindGroupLayout = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuComputePipelineGetBindGroupLayout
    wgpuComputePipelineGetBindGroupLayout.restype = WGPUBindGroupLayout
    wgpuComputePipelineGetBindGroupLayout.argtypes = [WGPUComputePipeline, uint32_t]
except AttributeError:
    pass
try:
    wgpuComputePipelineSetLabel = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuComputePipelineSetLabel
    wgpuComputePipelineSetLabel.restype = None
    wgpuComputePipelineSetLabel.argtypes = [WGPUComputePipeline, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuComputePipelineAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuComputePipelineAddRef
    wgpuComputePipelineAddRef.restype = None
    wgpuComputePipelineAddRef.argtypes = [WGPUComputePipeline]
except AttributeError:
    pass
try:
    wgpuComputePipelineRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuComputePipelineRelease
    wgpuComputePipelineRelease.restype = None
    wgpuComputePipelineRelease.argtypes = [WGPUComputePipeline]
except AttributeError:
    pass
try:
    wgpuDawnDrmFormatCapabilitiesFreeMembers = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDawnDrmFormatCapabilitiesFreeMembers
    wgpuDawnDrmFormatCapabilitiesFreeMembers.restype = None
    wgpuDawnDrmFormatCapabilitiesFreeMembers.argtypes = [WGPUDawnDrmFormatCapabilities]
except AttributeError:
    pass
try:
    wgpuDeviceCreateBindGroup = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceCreateBindGroup
    wgpuDeviceCreateBindGroup.restype = WGPUBindGroup
    wgpuDeviceCreateBindGroup.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUBindGroupDescriptor)]
except AttributeError:
    pass
try:
    wgpuDeviceCreateBindGroupLayout = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceCreateBindGroupLayout
    wgpuDeviceCreateBindGroupLayout.restype = WGPUBindGroupLayout
    wgpuDeviceCreateBindGroupLayout.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUBindGroupLayoutDescriptor)]
except AttributeError:
    pass
try:
    wgpuDeviceCreateBuffer = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceCreateBuffer
    wgpuDeviceCreateBuffer.restype = WGPUBuffer
    wgpuDeviceCreateBuffer.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUBufferDescriptor)]
except AttributeError:
    pass
try:
    wgpuDeviceCreateCommandEncoder = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceCreateCommandEncoder
    wgpuDeviceCreateCommandEncoder.restype = WGPUCommandEncoder
    wgpuDeviceCreateCommandEncoder.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUCommandEncoderDescriptor)]
except AttributeError:
    pass
try:
    wgpuDeviceCreateComputePipeline = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceCreateComputePipeline
    wgpuDeviceCreateComputePipeline.restype = WGPUComputePipeline
    wgpuDeviceCreateComputePipeline.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUComputePipelineDescriptor)]
except AttributeError:
    pass
try:
    wgpuDeviceCreateComputePipelineAsync = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceCreateComputePipelineAsync
    wgpuDeviceCreateComputePipelineAsync.restype = WGPUFuture
    wgpuDeviceCreateComputePipelineAsync.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUComputePipelineDescriptor), WGPUCreateComputePipelineAsyncCallbackInfo]
except AttributeError:
    pass
try:
    wgpuDeviceCreateErrorBuffer = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceCreateErrorBuffer
    wgpuDeviceCreateErrorBuffer.restype = WGPUBuffer
    wgpuDeviceCreateErrorBuffer.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUBufferDescriptor)]
except AttributeError:
    pass
try:
    wgpuDeviceCreateErrorExternalTexture = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceCreateErrorExternalTexture
    wgpuDeviceCreateErrorExternalTexture.restype = WGPUExternalTexture
    wgpuDeviceCreateErrorExternalTexture.argtypes = [WGPUDevice]
except AttributeError:
    pass
try:
    wgpuDeviceCreateErrorShaderModule = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceCreateErrorShaderModule
    wgpuDeviceCreateErrorShaderModule.restype = WGPUShaderModule
    wgpuDeviceCreateErrorShaderModule.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUShaderModuleDescriptor), WGPUStringView]
except AttributeError:
    pass
try:
    wgpuDeviceCreateErrorTexture = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceCreateErrorTexture
    wgpuDeviceCreateErrorTexture.restype = WGPUTexture
    wgpuDeviceCreateErrorTexture.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUTextureDescriptor)]
except AttributeError:
    pass
try:
    wgpuDeviceCreateExternalTexture = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceCreateExternalTexture
    wgpuDeviceCreateExternalTexture.restype = WGPUExternalTexture
    wgpuDeviceCreateExternalTexture.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUExternalTextureDescriptor)]
except AttributeError:
    pass
try:
    wgpuDeviceCreatePipelineLayout = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceCreatePipelineLayout
    wgpuDeviceCreatePipelineLayout.restype = WGPUPipelineLayout
    wgpuDeviceCreatePipelineLayout.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUPipelineLayoutDescriptor)]
except AttributeError:
    pass
try:
    wgpuDeviceCreateQuerySet = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceCreateQuerySet
    wgpuDeviceCreateQuerySet.restype = WGPUQuerySet
    wgpuDeviceCreateQuerySet.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUQuerySetDescriptor)]
except AttributeError:
    pass
try:
    wgpuDeviceCreateRenderBundleEncoder = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceCreateRenderBundleEncoder
    wgpuDeviceCreateRenderBundleEncoder.restype = WGPURenderBundleEncoder
    wgpuDeviceCreateRenderBundleEncoder.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPURenderBundleEncoderDescriptor)]
except AttributeError:
    pass
try:
    wgpuDeviceCreateRenderPipeline = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceCreateRenderPipeline
    wgpuDeviceCreateRenderPipeline.restype = WGPURenderPipeline
    wgpuDeviceCreateRenderPipeline.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPURenderPipelineDescriptor)]
except AttributeError:
    pass
try:
    wgpuDeviceCreateRenderPipelineAsync = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceCreateRenderPipelineAsync
    wgpuDeviceCreateRenderPipelineAsync.restype = WGPUFuture
    wgpuDeviceCreateRenderPipelineAsync.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPURenderPipelineDescriptor), WGPUCreateRenderPipelineAsyncCallbackInfo]
except AttributeError:
    pass
try:
    wgpuDeviceCreateResourceTable = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceCreateResourceTable
    wgpuDeviceCreateResourceTable.restype = WGPUResourceTable
    wgpuDeviceCreateResourceTable.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUResourceTableDescriptor)]
except AttributeError:
    pass
try:
    wgpuDeviceCreateSampler = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceCreateSampler
    wgpuDeviceCreateSampler.restype = WGPUSampler
    wgpuDeviceCreateSampler.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUSamplerDescriptor)]
except AttributeError:
    pass
try:
    wgpuDeviceCreateShaderModule = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceCreateShaderModule
    wgpuDeviceCreateShaderModule.restype = WGPUShaderModule
    wgpuDeviceCreateShaderModule.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUShaderModuleDescriptor)]
except AttributeError:
    pass
try:
    wgpuDeviceCreateTexture = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceCreateTexture
    wgpuDeviceCreateTexture.restype = WGPUTexture
    wgpuDeviceCreateTexture.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUTextureDescriptor)]
except AttributeError:
    pass
try:
    wgpuDeviceDestroy = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceDestroy
    wgpuDeviceDestroy.restype = None
    wgpuDeviceDestroy.argtypes = [WGPUDevice]
except AttributeError:
    pass
try:
    wgpuDeviceForceLoss = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceForceLoss
    wgpuDeviceForceLoss.restype = None
    wgpuDeviceForceLoss.argtypes = [WGPUDevice, WGPUDeviceLostReason, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuDeviceGetAdapter = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceGetAdapter
    wgpuDeviceGetAdapter.restype = WGPUAdapter
    wgpuDeviceGetAdapter.argtypes = [WGPUDevice]
except AttributeError:
    pass
try:
    wgpuDeviceGetAdapterInfo = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceGetAdapterInfo
    wgpuDeviceGetAdapterInfo.restype = WGPUStatus
    wgpuDeviceGetAdapterInfo.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUAdapterInfo)]
except AttributeError:
    pass
try:
    wgpuDeviceGetAHardwareBufferProperties = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceGetAHardwareBufferProperties
    wgpuDeviceGetAHardwareBufferProperties.restype = WGPUStatus
    wgpuDeviceGetAHardwareBufferProperties.argtypes = [WGPUDevice, ctypes.POINTER(None), ctypes.POINTER(struct_WGPUAHardwareBufferProperties)]
except AttributeError:
    pass
try:
    wgpuDeviceGetFeatures = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceGetFeatures
    wgpuDeviceGetFeatures.restype = None
    wgpuDeviceGetFeatures.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUSupportedFeatures)]
except AttributeError:
    pass
try:
    wgpuDeviceGetLimits = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceGetLimits
    wgpuDeviceGetLimits.restype = WGPUStatus
    wgpuDeviceGetLimits.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPULimits)]
except AttributeError:
    pass
try:
    wgpuDeviceGetLostFuture = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceGetLostFuture
    wgpuDeviceGetLostFuture.restype = WGPUFuture
    wgpuDeviceGetLostFuture.argtypes = [WGPUDevice]
except AttributeError:
    pass
try:
    wgpuDeviceGetQueue = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceGetQueue
    wgpuDeviceGetQueue.restype = WGPUQueue
    wgpuDeviceGetQueue.argtypes = [WGPUDevice]
except AttributeError:
    pass
try:
    wgpuDeviceHasFeature = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceHasFeature
    wgpuDeviceHasFeature.restype = WGPUBool
    wgpuDeviceHasFeature.argtypes = [WGPUDevice, WGPUFeatureName]
except AttributeError:
    pass
try:
    wgpuDeviceImportSharedBufferMemory = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceImportSharedBufferMemory
    wgpuDeviceImportSharedBufferMemory.restype = WGPUSharedBufferMemory
    wgpuDeviceImportSharedBufferMemory.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUSharedBufferMemoryDescriptor)]
except AttributeError:
    pass
try:
    wgpuDeviceImportSharedFence = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceImportSharedFence
    wgpuDeviceImportSharedFence.restype = WGPUSharedFence
    wgpuDeviceImportSharedFence.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUSharedFenceDescriptor)]
except AttributeError:
    pass
try:
    wgpuDeviceImportSharedTextureMemory = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceImportSharedTextureMemory
    wgpuDeviceImportSharedTextureMemory.restype = WGPUSharedTextureMemory
    wgpuDeviceImportSharedTextureMemory.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUSharedTextureMemoryDescriptor)]
except AttributeError:
    pass
try:
    wgpuDeviceInjectError = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceInjectError
    wgpuDeviceInjectError.restype = None
    wgpuDeviceInjectError.argtypes = [WGPUDevice, WGPUErrorType, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuDevicePopErrorScope = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDevicePopErrorScope
    wgpuDevicePopErrorScope.restype = WGPUFuture
    wgpuDevicePopErrorScope.argtypes = [WGPUDevice, WGPUPopErrorScopeCallbackInfo]
except AttributeError:
    pass
try:
    wgpuDevicePushErrorScope = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDevicePushErrorScope
    wgpuDevicePushErrorScope.restype = None
    wgpuDevicePushErrorScope.argtypes = [WGPUDevice, WGPUErrorFilter]
except AttributeError:
    pass
try:
    wgpuDeviceSetLabel = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceSetLabel
    wgpuDeviceSetLabel.restype = None
    wgpuDeviceSetLabel.argtypes = [WGPUDevice, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuDeviceSetLoggingCallback = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceSetLoggingCallback
    wgpuDeviceSetLoggingCallback.restype = None
    wgpuDeviceSetLoggingCallback.argtypes = [WGPUDevice, WGPULoggingCallbackInfo]
except AttributeError:
    pass
try:
    wgpuDeviceTick = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceTick
    wgpuDeviceTick.restype = None
    wgpuDeviceTick.argtypes = [WGPUDevice]
except AttributeError:
    pass
try:
    wgpuDeviceValidateTextureDescriptor = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceValidateTextureDescriptor
    wgpuDeviceValidateTextureDescriptor.restype = None
    wgpuDeviceValidateTextureDescriptor.argtypes = [WGPUDevice, ctypes.POINTER(struct_WGPUTextureDescriptor)]
except AttributeError:
    pass
try:
    wgpuDeviceAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceAddRef
    wgpuDeviceAddRef.restype = None
    wgpuDeviceAddRef.argtypes = [WGPUDevice]
except AttributeError:
    pass
try:
    wgpuDeviceRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuDeviceRelease
    wgpuDeviceRelease.restype = None
    wgpuDeviceRelease.argtypes = [WGPUDevice]
except AttributeError:
    pass
try:
    wgpuExternalTextureDestroy = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuExternalTextureDestroy
    wgpuExternalTextureDestroy.restype = None
    wgpuExternalTextureDestroy.argtypes = [WGPUExternalTexture]
except AttributeError:
    pass
try:
    wgpuExternalTextureExpire = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuExternalTextureExpire
    wgpuExternalTextureExpire.restype = None
    wgpuExternalTextureExpire.argtypes = [WGPUExternalTexture]
except AttributeError:
    pass
try:
    wgpuExternalTextureRefresh = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuExternalTextureRefresh
    wgpuExternalTextureRefresh.restype = None
    wgpuExternalTextureRefresh.argtypes = [WGPUExternalTexture]
except AttributeError:
    pass
try:
    wgpuExternalTextureSetLabel = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuExternalTextureSetLabel
    wgpuExternalTextureSetLabel.restype = None
    wgpuExternalTextureSetLabel.argtypes = [WGPUExternalTexture, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuExternalTextureAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuExternalTextureAddRef
    wgpuExternalTextureAddRef.restype = None
    wgpuExternalTextureAddRef.argtypes = [WGPUExternalTexture]
except AttributeError:
    pass
try:
    wgpuExternalTextureRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuExternalTextureRelease
    wgpuExternalTextureRelease.restype = None
    wgpuExternalTextureRelease.argtypes = [WGPUExternalTexture]
except AttributeError:
    pass
try:
    wgpuInstanceCreateSurface = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuInstanceCreateSurface
    wgpuInstanceCreateSurface.restype = WGPUSurface
    wgpuInstanceCreateSurface.argtypes = [WGPUInstance, ctypes.POINTER(struct_WGPUSurfaceDescriptor)]
except AttributeError:
    pass
try:
    wgpuInstanceGetWGSLLanguageFeatures = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuInstanceGetWGSLLanguageFeatures
    wgpuInstanceGetWGSLLanguageFeatures.restype = None
    wgpuInstanceGetWGSLLanguageFeatures.argtypes = [WGPUInstance, ctypes.POINTER(struct_WGPUSupportedWGSLLanguageFeatures)]
except AttributeError:
    pass
try:
    wgpuInstanceHasWGSLLanguageFeature = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuInstanceHasWGSLLanguageFeature
    wgpuInstanceHasWGSLLanguageFeature.restype = WGPUBool
    wgpuInstanceHasWGSLLanguageFeature.argtypes = [WGPUInstance, WGPUWGSLLanguageFeatureName]
except AttributeError:
    pass
try:
    wgpuInstanceProcessEvents = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuInstanceProcessEvents
    wgpuInstanceProcessEvents.restype = None
    wgpuInstanceProcessEvents.argtypes = [WGPUInstance]
except AttributeError:
    pass
try:
    wgpuInstanceRequestAdapter = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuInstanceRequestAdapter
    wgpuInstanceRequestAdapter.restype = WGPUFuture
    wgpuInstanceRequestAdapter.argtypes = [WGPUInstance, ctypes.POINTER(struct_WGPURequestAdapterOptions), WGPURequestAdapterCallbackInfo]
except AttributeError:
    pass
try:
    wgpuInstanceWaitAny = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuInstanceWaitAny
    wgpuInstanceWaitAny.restype = WGPUWaitStatus
    wgpuInstanceWaitAny.argtypes = [WGPUInstance, size_t, ctypes.POINTER(struct_WGPUFutureWaitInfo), uint64_t]
except AttributeError:
    pass
try:
    wgpuInstanceAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuInstanceAddRef
    wgpuInstanceAddRef.restype = None
    wgpuInstanceAddRef.argtypes = [WGPUInstance]
except AttributeError:
    pass
try:
    wgpuInstanceRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuInstanceRelease
    wgpuInstanceRelease.restype = None
    wgpuInstanceRelease.argtypes = [WGPUInstance]
except AttributeError:
    pass
try:
    wgpuPipelineLayoutSetLabel = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuPipelineLayoutSetLabel
    wgpuPipelineLayoutSetLabel.restype = None
    wgpuPipelineLayoutSetLabel.argtypes = [WGPUPipelineLayout, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuPipelineLayoutAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuPipelineLayoutAddRef
    wgpuPipelineLayoutAddRef.restype = None
    wgpuPipelineLayoutAddRef.argtypes = [WGPUPipelineLayout]
except AttributeError:
    pass
try:
    wgpuPipelineLayoutRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuPipelineLayoutRelease
    wgpuPipelineLayoutRelease.restype = None
    wgpuPipelineLayoutRelease.argtypes = [WGPUPipelineLayout]
except AttributeError:
    pass
try:
    wgpuQuerySetDestroy = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuQuerySetDestroy
    wgpuQuerySetDestroy.restype = None
    wgpuQuerySetDestroy.argtypes = [WGPUQuerySet]
except AttributeError:
    pass
try:
    wgpuQuerySetGetCount = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuQuerySetGetCount
    wgpuQuerySetGetCount.restype = uint32_t
    wgpuQuerySetGetCount.argtypes = [WGPUQuerySet]
except AttributeError:
    pass
try:
    wgpuQuerySetGetType = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuQuerySetGetType
    wgpuQuerySetGetType.restype = WGPUQueryType
    wgpuQuerySetGetType.argtypes = [WGPUQuerySet]
except AttributeError:
    pass
try:
    wgpuQuerySetSetLabel = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuQuerySetSetLabel
    wgpuQuerySetSetLabel.restype = None
    wgpuQuerySetSetLabel.argtypes = [WGPUQuerySet, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuQuerySetAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuQuerySetAddRef
    wgpuQuerySetAddRef.restype = None
    wgpuQuerySetAddRef.argtypes = [WGPUQuerySet]
except AttributeError:
    pass
try:
    wgpuQuerySetRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuQuerySetRelease
    wgpuQuerySetRelease.restype = None
    wgpuQuerySetRelease.argtypes = [WGPUQuerySet]
except AttributeError:
    pass
try:
    wgpuQueueCopyExternalTextureForBrowser = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuQueueCopyExternalTextureForBrowser
    wgpuQueueCopyExternalTextureForBrowser.restype = None
    wgpuQueueCopyExternalTextureForBrowser.argtypes = [WGPUQueue, ctypes.POINTER(struct_WGPUImageCopyExternalTexture), ctypes.POINTER(struct_WGPUTexelCopyTextureInfo), ctypes.POINTER(struct_WGPUExtent3D), ctypes.POINTER(struct_WGPUCopyTextureForBrowserOptions)]
except AttributeError:
    pass
try:
    wgpuQueueCopyTextureForBrowser = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuQueueCopyTextureForBrowser
    wgpuQueueCopyTextureForBrowser.restype = None
    wgpuQueueCopyTextureForBrowser.argtypes = [WGPUQueue, ctypes.POINTER(struct_WGPUTexelCopyTextureInfo), ctypes.POINTER(struct_WGPUTexelCopyTextureInfo), ctypes.POINTER(struct_WGPUExtent3D), ctypes.POINTER(struct_WGPUCopyTextureForBrowserOptions)]
except AttributeError:
    pass
try:
    wgpuQueueOnSubmittedWorkDone = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuQueueOnSubmittedWorkDone
    wgpuQueueOnSubmittedWorkDone.restype = WGPUFuture
    wgpuQueueOnSubmittedWorkDone.argtypes = [WGPUQueue, WGPUQueueWorkDoneCallbackInfo]
except AttributeError:
    pass
try:
    wgpuQueueSetLabel = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuQueueSetLabel
    wgpuQueueSetLabel.restype = None
    wgpuQueueSetLabel.argtypes = [WGPUQueue, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuQueueSubmit = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuQueueSubmit
    wgpuQueueSubmit.restype = None
    wgpuQueueSubmit.argtypes = [WGPUQueue, size_t, ctypes.POINTER(ctypes.POINTER(struct_WGPUCommandBufferImpl))]
except AttributeError:
    pass
try:
    wgpuQueueWriteBuffer = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuQueueWriteBuffer
    wgpuQueueWriteBuffer.restype = None
    wgpuQueueWriteBuffer.argtypes = [WGPUQueue, WGPUBuffer, uint64_t, ctypes.POINTER(None), size_t]
except AttributeError:
    pass
try:
    wgpuQueueWriteTexture = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuQueueWriteTexture
    wgpuQueueWriteTexture.restype = None
    wgpuQueueWriteTexture.argtypes = [WGPUQueue, ctypes.POINTER(struct_WGPUTexelCopyTextureInfo), ctypes.POINTER(None), size_t, ctypes.POINTER(struct_WGPUTexelCopyBufferLayout), ctypes.POINTER(struct_WGPUExtent3D)]
except AttributeError:
    pass
try:
    wgpuQueueAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuQueueAddRef
    wgpuQueueAddRef.restype = None
    wgpuQueueAddRef.argtypes = [WGPUQueue]
except AttributeError:
    pass
try:
    wgpuQueueRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuQueueRelease
    wgpuQueueRelease.restype = None
    wgpuQueueRelease.argtypes = [WGPUQueue]
except AttributeError:
    pass
try:
    wgpuRenderBundleSetLabel = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderBundleSetLabel
    wgpuRenderBundleSetLabel.restype = None
    wgpuRenderBundleSetLabel.argtypes = [WGPURenderBundle, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuRenderBundleAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderBundleAddRef
    wgpuRenderBundleAddRef.restype = None
    wgpuRenderBundleAddRef.argtypes = [WGPURenderBundle]
except AttributeError:
    pass
try:
    wgpuRenderBundleRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderBundleRelease
    wgpuRenderBundleRelease.restype = None
    wgpuRenderBundleRelease.argtypes = [WGPURenderBundle]
except AttributeError:
    pass
try:
    wgpuRenderBundleEncoderDraw = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderBundleEncoderDraw
    wgpuRenderBundleEncoderDraw.restype = None
    wgpuRenderBundleEncoderDraw.argtypes = [WGPURenderBundleEncoder, uint32_t, uint32_t, uint32_t, uint32_t]
except AttributeError:
    pass
int32_t = ctypes.c_int32
try:
    wgpuRenderBundleEncoderDrawIndexed = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderBundleEncoderDrawIndexed
    wgpuRenderBundleEncoderDrawIndexed.restype = None
    wgpuRenderBundleEncoderDrawIndexed.argtypes = [WGPURenderBundleEncoder, uint32_t, uint32_t, uint32_t, int32_t, uint32_t]
except AttributeError:
    pass
try:
    wgpuRenderBundleEncoderDrawIndexedIndirect = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderBundleEncoderDrawIndexedIndirect
    wgpuRenderBundleEncoderDrawIndexedIndirect.restype = None
    wgpuRenderBundleEncoderDrawIndexedIndirect.argtypes = [WGPURenderBundleEncoder, WGPUBuffer, uint64_t]
except AttributeError:
    pass
try:
    wgpuRenderBundleEncoderDrawIndirect = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderBundleEncoderDrawIndirect
    wgpuRenderBundleEncoderDrawIndirect.restype = None
    wgpuRenderBundleEncoderDrawIndirect.argtypes = [WGPURenderBundleEncoder, WGPUBuffer, uint64_t]
except AttributeError:
    pass
try:
    wgpuRenderBundleEncoderFinish = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderBundleEncoderFinish
    wgpuRenderBundleEncoderFinish.restype = WGPURenderBundle
    wgpuRenderBundleEncoderFinish.argtypes = [WGPURenderBundleEncoder, ctypes.POINTER(struct_WGPURenderBundleDescriptor)]
except AttributeError:
    pass
try:
    wgpuRenderBundleEncoderInsertDebugMarker = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderBundleEncoderInsertDebugMarker
    wgpuRenderBundleEncoderInsertDebugMarker.restype = None
    wgpuRenderBundleEncoderInsertDebugMarker.argtypes = [WGPURenderBundleEncoder, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuRenderBundleEncoderPopDebugGroup = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderBundleEncoderPopDebugGroup
    wgpuRenderBundleEncoderPopDebugGroup.restype = None
    wgpuRenderBundleEncoderPopDebugGroup.argtypes = [WGPURenderBundleEncoder]
except AttributeError:
    pass
try:
    wgpuRenderBundleEncoderPushDebugGroup = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderBundleEncoderPushDebugGroup
    wgpuRenderBundleEncoderPushDebugGroup.restype = None
    wgpuRenderBundleEncoderPushDebugGroup.argtypes = [WGPURenderBundleEncoder, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuRenderBundleEncoderSetBindGroup = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderBundleEncoderSetBindGroup
    wgpuRenderBundleEncoderSetBindGroup.restype = None
    wgpuRenderBundleEncoderSetBindGroup.argtypes = [WGPURenderBundleEncoder, uint32_t, WGPUBindGroup, size_t, ctypes.POINTER(ctypes.c_uint32)]
except AttributeError:
    pass
try:
    wgpuRenderBundleEncoderSetImmediates = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderBundleEncoderSetImmediates
    wgpuRenderBundleEncoderSetImmediates.restype = None
    wgpuRenderBundleEncoderSetImmediates.argtypes = [WGPURenderBundleEncoder, uint32_t, ctypes.POINTER(None), size_t]
except AttributeError:
    pass
try:
    wgpuRenderBundleEncoderSetIndexBuffer = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderBundleEncoderSetIndexBuffer
    wgpuRenderBundleEncoderSetIndexBuffer.restype = None
    wgpuRenderBundleEncoderSetIndexBuffer.argtypes = [WGPURenderBundleEncoder, WGPUBuffer, WGPUIndexFormat, uint64_t, uint64_t]
except AttributeError:
    pass
try:
    wgpuRenderBundleEncoderSetLabel = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderBundleEncoderSetLabel
    wgpuRenderBundleEncoderSetLabel.restype = None
    wgpuRenderBundleEncoderSetLabel.argtypes = [WGPURenderBundleEncoder, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuRenderBundleEncoderSetPipeline = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderBundleEncoderSetPipeline
    wgpuRenderBundleEncoderSetPipeline.restype = None
    wgpuRenderBundleEncoderSetPipeline.argtypes = [WGPURenderBundleEncoder, WGPURenderPipeline]
except AttributeError:
    pass
try:
    wgpuRenderBundleEncoderSetVertexBuffer = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderBundleEncoderSetVertexBuffer
    wgpuRenderBundleEncoderSetVertexBuffer.restype = None
    wgpuRenderBundleEncoderSetVertexBuffer.argtypes = [WGPURenderBundleEncoder, uint32_t, WGPUBuffer, uint64_t, uint64_t]
except AttributeError:
    pass
try:
    wgpuRenderBundleEncoderAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderBundleEncoderAddRef
    wgpuRenderBundleEncoderAddRef.restype = None
    wgpuRenderBundleEncoderAddRef.argtypes = [WGPURenderBundleEncoder]
except AttributeError:
    pass
try:
    wgpuRenderBundleEncoderRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderBundleEncoderRelease
    wgpuRenderBundleEncoderRelease.restype = None
    wgpuRenderBundleEncoderRelease.argtypes = [WGPURenderBundleEncoder]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderBeginOcclusionQuery = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderBeginOcclusionQuery
    wgpuRenderPassEncoderBeginOcclusionQuery.restype = None
    wgpuRenderPassEncoderBeginOcclusionQuery.argtypes = [WGPURenderPassEncoder, uint32_t]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderDraw = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderDraw
    wgpuRenderPassEncoderDraw.restype = None
    wgpuRenderPassEncoderDraw.argtypes = [WGPURenderPassEncoder, uint32_t, uint32_t, uint32_t, uint32_t]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderDrawIndexed = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderDrawIndexed
    wgpuRenderPassEncoderDrawIndexed.restype = None
    wgpuRenderPassEncoderDrawIndexed.argtypes = [WGPURenderPassEncoder, uint32_t, uint32_t, uint32_t, int32_t, uint32_t]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderDrawIndexedIndirect = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderDrawIndexedIndirect
    wgpuRenderPassEncoderDrawIndexedIndirect.restype = None
    wgpuRenderPassEncoderDrawIndexedIndirect.argtypes = [WGPURenderPassEncoder, WGPUBuffer, uint64_t]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderDrawIndirect = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderDrawIndirect
    wgpuRenderPassEncoderDrawIndirect.restype = None
    wgpuRenderPassEncoderDrawIndirect.argtypes = [WGPURenderPassEncoder, WGPUBuffer, uint64_t]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderEnd = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderEnd
    wgpuRenderPassEncoderEnd.restype = None
    wgpuRenderPassEncoderEnd.argtypes = [WGPURenderPassEncoder]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderEndOcclusionQuery = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderEndOcclusionQuery
    wgpuRenderPassEncoderEndOcclusionQuery.restype = None
    wgpuRenderPassEncoderEndOcclusionQuery.argtypes = [WGPURenderPassEncoder]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderExecuteBundles = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderExecuteBundles
    wgpuRenderPassEncoderExecuteBundles.restype = None
    wgpuRenderPassEncoderExecuteBundles.argtypes = [WGPURenderPassEncoder, size_t, ctypes.POINTER(ctypes.POINTER(struct_WGPURenderBundleImpl))]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderInsertDebugMarker = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderInsertDebugMarker
    wgpuRenderPassEncoderInsertDebugMarker.restype = None
    wgpuRenderPassEncoderInsertDebugMarker.argtypes = [WGPURenderPassEncoder, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderMultiDrawIndexedIndirect = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderMultiDrawIndexedIndirect
    wgpuRenderPassEncoderMultiDrawIndexedIndirect.restype = None
    wgpuRenderPassEncoderMultiDrawIndexedIndirect.argtypes = [WGPURenderPassEncoder, WGPUBuffer, uint64_t, uint32_t, WGPUBuffer, uint64_t]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderMultiDrawIndirect = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderMultiDrawIndirect
    wgpuRenderPassEncoderMultiDrawIndirect.restype = None
    wgpuRenderPassEncoderMultiDrawIndirect.argtypes = [WGPURenderPassEncoder, WGPUBuffer, uint64_t, uint32_t, WGPUBuffer, uint64_t]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderPixelLocalStorageBarrier = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderPixelLocalStorageBarrier
    wgpuRenderPassEncoderPixelLocalStorageBarrier.restype = None
    wgpuRenderPassEncoderPixelLocalStorageBarrier.argtypes = [WGPURenderPassEncoder]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderPopDebugGroup = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderPopDebugGroup
    wgpuRenderPassEncoderPopDebugGroup.restype = None
    wgpuRenderPassEncoderPopDebugGroup.argtypes = [WGPURenderPassEncoder]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderPushDebugGroup = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderPushDebugGroup
    wgpuRenderPassEncoderPushDebugGroup.restype = None
    wgpuRenderPassEncoderPushDebugGroup.argtypes = [WGPURenderPassEncoder, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderSetBindGroup = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderSetBindGroup
    wgpuRenderPassEncoderSetBindGroup.restype = None
    wgpuRenderPassEncoderSetBindGroup.argtypes = [WGPURenderPassEncoder, uint32_t, WGPUBindGroup, size_t, ctypes.POINTER(ctypes.c_uint32)]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderSetBlendConstant = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderSetBlendConstant
    wgpuRenderPassEncoderSetBlendConstant.restype = None
    wgpuRenderPassEncoderSetBlendConstant.argtypes = [WGPURenderPassEncoder, ctypes.POINTER(struct_WGPUColor)]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderSetImmediates = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderSetImmediates
    wgpuRenderPassEncoderSetImmediates.restype = None
    wgpuRenderPassEncoderSetImmediates.argtypes = [WGPURenderPassEncoder, uint32_t, ctypes.POINTER(None), size_t]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderSetIndexBuffer = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderSetIndexBuffer
    wgpuRenderPassEncoderSetIndexBuffer.restype = None
    wgpuRenderPassEncoderSetIndexBuffer.argtypes = [WGPURenderPassEncoder, WGPUBuffer, WGPUIndexFormat, uint64_t, uint64_t]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderSetLabel = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderSetLabel
    wgpuRenderPassEncoderSetLabel.restype = None
    wgpuRenderPassEncoderSetLabel.argtypes = [WGPURenderPassEncoder, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderSetPipeline = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderSetPipeline
    wgpuRenderPassEncoderSetPipeline.restype = None
    wgpuRenderPassEncoderSetPipeline.argtypes = [WGPURenderPassEncoder, WGPURenderPipeline]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderSetScissorRect = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderSetScissorRect
    wgpuRenderPassEncoderSetScissorRect.restype = None
    wgpuRenderPassEncoderSetScissorRect.argtypes = [WGPURenderPassEncoder, uint32_t, uint32_t, uint32_t, uint32_t]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderSetStencilReference = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderSetStencilReference
    wgpuRenderPassEncoderSetStencilReference.restype = None
    wgpuRenderPassEncoderSetStencilReference.argtypes = [WGPURenderPassEncoder, uint32_t]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderSetVertexBuffer = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderSetVertexBuffer
    wgpuRenderPassEncoderSetVertexBuffer.restype = None
    wgpuRenderPassEncoderSetVertexBuffer.argtypes = [WGPURenderPassEncoder, uint32_t, WGPUBuffer, uint64_t, uint64_t]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderSetViewport = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderSetViewport
    wgpuRenderPassEncoderSetViewport.restype = None
    wgpuRenderPassEncoderSetViewport.argtypes = [WGPURenderPassEncoder, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderWriteTimestamp = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderWriteTimestamp
    wgpuRenderPassEncoderWriteTimestamp.restype = None
    wgpuRenderPassEncoderWriteTimestamp.argtypes = [WGPURenderPassEncoder, WGPUQuerySet, uint32_t]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderAddRef
    wgpuRenderPassEncoderAddRef.restype = None
    wgpuRenderPassEncoderAddRef.argtypes = [WGPURenderPassEncoder]
except AttributeError:
    pass
try:
    wgpuRenderPassEncoderRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPassEncoderRelease
    wgpuRenderPassEncoderRelease.restype = None
    wgpuRenderPassEncoderRelease.argtypes = [WGPURenderPassEncoder]
except AttributeError:
    pass
try:
    wgpuRenderPipelineGetBindGroupLayout = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPipelineGetBindGroupLayout
    wgpuRenderPipelineGetBindGroupLayout.restype = WGPUBindGroupLayout
    wgpuRenderPipelineGetBindGroupLayout.argtypes = [WGPURenderPipeline, uint32_t]
except AttributeError:
    pass
try:
    wgpuRenderPipelineSetLabel = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPipelineSetLabel
    wgpuRenderPipelineSetLabel.restype = None
    wgpuRenderPipelineSetLabel.argtypes = [WGPURenderPipeline, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuRenderPipelineAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPipelineAddRef
    wgpuRenderPipelineAddRef.restype = None
    wgpuRenderPipelineAddRef.argtypes = [WGPURenderPipeline]
except AttributeError:
    pass
try:
    wgpuRenderPipelineRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuRenderPipelineRelease
    wgpuRenderPipelineRelease.restype = None
    wgpuRenderPipelineRelease.argtypes = [WGPURenderPipeline]
except AttributeError:
    pass
try:
    wgpuResourceTableDestroy = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuResourceTableDestroy
    wgpuResourceTableDestroy.restype = None
    wgpuResourceTableDestroy.argtypes = [WGPUResourceTable]
except AttributeError:
    pass
try:
    wgpuResourceTableAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuResourceTableAddRef
    wgpuResourceTableAddRef.restype = None
    wgpuResourceTableAddRef.argtypes = [WGPUResourceTable]
except AttributeError:
    pass
try:
    wgpuResourceTableRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuResourceTableRelease
    wgpuResourceTableRelease.restype = None
    wgpuResourceTableRelease.argtypes = [WGPUResourceTable]
except AttributeError:
    pass
try:
    wgpuSamplerSetLabel = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSamplerSetLabel
    wgpuSamplerSetLabel.restype = None
    wgpuSamplerSetLabel.argtypes = [WGPUSampler, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuSamplerAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSamplerAddRef
    wgpuSamplerAddRef.restype = None
    wgpuSamplerAddRef.argtypes = [WGPUSampler]
except AttributeError:
    pass
try:
    wgpuSamplerRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSamplerRelease
    wgpuSamplerRelease.restype = None
    wgpuSamplerRelease.argtypes = [WGPUSampler]
except AttributeError:
    pass
try:
    wgpuShaderModuleGetCompilationInfo = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuShaderModuleGetCompilationInfo
    wgpuShaderModuleGetCompilationInfo.restype = WGPUFuture
    wgpuShaderModuleGetCompilationInfo.argtypes = [WGPUShaderModule, WGPUCompilationInfoCallbackInfo]
except AttributeError:
    pass
try:
    wgpuShaderModuleSetLabel = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuShaderModuleSetLabel
    wgpuShaderModuleSetLabel.restype = None
    wgpuShaderModuleSetLabel.argtypes = [WGPUShaderModule, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuShaderModuleAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuShaderModuleAddRef
    wgpuShaderModuleAddRef.restype = None
    wgpuShaderModuleAddRef.argtypes = [WGPUShaderModule]
except AttributeError:
    pass
try:
    wgpuShaderModuleRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuShaderModuleRelease
    wgpuShaderModuleRelease.restype = None
    wgpuShaderModuleRelease.argtypes = [WGPUShaderModule]
except AttributeError:
    pass
try:
    wgpuSharedBufferMemoryBeginAccess = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSharedBufferMemoryBeginAccess
    wgpuSharedBufferMemoryBeginAccess.restype = WGPUStatus
    wgpuSharedBufferMemoryBeginAccess.argtypes = [WGPUSharedBufferMemory, WGPUBuffer, ctypes.POINTER(struct_WGPUSharedBufferMemoryBeginAccessDescriptor)]
except AttributeError:
    pass
try:
    wgpuSharedBufferMemoryCreateBuffer = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSharedBufferMemoryCreateBuffer
    wgpuSharedBufferMemoryCreateBuffer.restype = WGPUBuffer
    wgpuSharedBufferMemoryCreateBuffer.argtypes = [WGPUSharedBufferMemory, ctypes.POINTER(struct_WGPUBufferDescriptor)]
except AttributeError:
    pass
try:
    wgpuSharedBufferMemoryEndAccess = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSharedBufferMemoryEndAccess
    wgpuSharedBufferMemoryEndAccess.restype = WGPUStatus
    wgpuSharedBufferMemoryEndAccess.argtypes = [WGPUSharedBufferMemory, WGPUBuffer, ctypes.POINTER(struct_WGPUSharedBufferMemoryEndAccessState)]
except AttributeError:
    pass
try:
    wgpuSharedBufferMemoryGetProperties = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSharedBufferMemoryGetProperties
    wgpuSharedBufferMemoryGetProperties.restype = WGPUStatus
    wgpuSharedBufferMemoryGetProperties.argtypes = [WGPUSharedBufferMemory, ctypes.POINTER(struct_WGPUSharedBufferMemoryProperties)]
except AttributeError:
    pass
try:
    wgpuSharedBufferMemoryIsDeviceLost = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSharedBufferMemoryIsDeviceLost
    wgpuSharedBufferMemoryIsDeviceLost.restype = WGPUBool
    wgpuSharedBufferMemoryIsDeviceLost.argtypes = [WGPUSharedBufferMemory]
except AttributeError:
    pass
try:
    wgpuSharedBufferMemorySetLabel = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSharedBufferMemorySetLabel
    wgpuSharedBufferMemorySetLabel.restype = None
    wgpuSharedBufferMemorySetLabel.argtypes = [WGPUSharedBufferMemory, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuSharedBufferMemoryAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSharedBufferMemoryAddRef
    wgpuSharedBufferMemoryAddRef.restype = None
    wgpuSharedBufferMemoryAddRef.argtypes = [WGPUSharedBufferMemory]
except AttributeError:
    pass
try:
    wgpuSharedBufferMemoryRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSharedBufferMemoryRelease
    wgpuSharedBufferMemoryRelease.restype = None
    wgpuSharedBufferMemoryRelease.argtypes = [WGPUSharedBufferMemory]
except AttributeError:
    pass
try:
    wgpuSharedBufferMemoryEndAccessStateFreeMembers = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSharedBufferMemoryEndAccessStateFreeMembers
    wgpuSharedBufferMemoryEndAccessStateFreeMembers.restype = None
    wgpuSharedBufferMemoryEndAccessStateFreeMembers.argtypes = [WGPUSharedBufferMemoryEndAccessState]
except AttributeError:
    pass
try:
    wgpuSharedFenceExportInfo = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSharedFenceExportInfo
    wgpuSharedFenceExportInfo.restype = None
    wgpuSharedFenceExportInfo.argtypes = [WGPUSharedFence, ctypes.POINTER(struct_WGPUSharedFenceExportInfo)]
except AttributeError:
    pass
try:
    wgpuSharedFenceAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSharedFenceAddRef
    wgpuSharedFenceAddRef.restype = None
    wgpuSharedFenceAddRef.argtypes = [WGPUSharedFence]
except AttributeError:
    pass
try:
    wgpuSharedFenceRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSharedFenceRelease
    wgpuSharedFenceRelease.restype = None
    wgpuSharedFenceRelease.argtypes = [WGPUSharedFence]
except AttributeError:
    pass
try:
    wgpuSharedTextureMemoryBeginAccess = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSharedTextureMemoryBeginAccess
    wgpuSharedTextureMemoryBeginAccess.restype = WGPUStatus
    wgpuSharedTextureMemoryBeginAccess.argtypes = [WGPUSharedTextureMemory, WGPUTexture, ctypes.POINTER(struct_WGPUSharedTextureMemoryBeginAccessDescriptor)]
except AttributeError:
    pass
try:
    wgpuSharedTextureMemoryCreateTexture = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSharedTextureMemoryCreateTexture
    wgpuSharedTextureMemoryCreateTexture.restype = WGPUTexture
    wgpuSharedTextureMemoryCreateTexture.argtypes = [WGPUSharedTextureMemory, ctypes.POINTER(struct_WGPUTextureDescriptor)]
except AttributeError:
    pass
try:
    wgpuSharedTextureMemoryEndAccess = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSharedTextureMemoryEndAccess
    wgpuSharedTextureMemoryEndAccess.restype = WGPUStatus
    wgpuSharedTextureMemoryEndAccess.argtypes = [WGPUSharedTextureMemory, WGPUTexture, ctypes.POINTER(struct_WGPUSharedTextureMemoryEndAccessState)]
except AttributeError:
    pass
try:
    wgpuSharedTextureMemoryGetProperties = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSharedTextureMemoryGetProperties
    wgpuSharedTextureMemoryGetProperties.restype = WGPUStatus
    wgpuSharedTextureMemoryGetProperties.argtypes = [WGPUSharedTextureMemory, ctypes.POINTER(struct_WGPUSharedTextureMemoryProperties)]
except AttributeError:
    pass
try:
    wgpuSharedTextureMemoryIsDeviceLost = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSharedTextureMemoryIsDeviceLost
    wgpuSharedTextureMemoryIsDeviceLost.restype = WGPUBool
    wgpuSharedTextureMemoryIsDeviceLost.argtypes = [WGPUSharedTextureMemory]
except AttributeError:
    pass
try:
    wgpuSharedTextureMemorySetLabel = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSharedTextureMemorySetLabel
    wgpuSharedTextureMemorySetLabel.restype = None
    wgpuSharedTextureMemorySetLabel.argtypes = [WGPUSharedTextureMemory, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuSharedTextureMemoryAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSharedTextureMemoryAddRef
    wgpuSharedTextureMemoryAddRef.restype = None
    wgpuSharedTextureMemoryAddRef.argtypes = [WGPUSharedTextureMemory]
except AttributeError:
    pass
try:
    wgpuSharedTextureMemoryRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSharedTextureMemoryRelease
    wgpuSharedTextureMemoryRelease.restype = None
    wgpuSharedTextureMemoryRelease.argtypes = [WGPUSharedTextureMemory]
except AttributeError:
    pass
try:
    wgpuSharedTextureMemoryEndAccessStateFreeMembers = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSharedTextureMemoryEndAccessStateFreeMembers
    wgpuSharedTextureMemoryEndAccessStateFreeMembers.restype = None
    wgpuSharedTextureMemoryEndAccessStateFreeMembers.argtypes = [WGPUSharedTextureMemoryEndAccessState]
except AttributeError:
    pass
try:
    wgpuSupportedFeaturesFreeMembers = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSupportedFeaturesFreeMembers
    wgpuSupportedFeaturesFreeMembers.restype = None
    wgpuSupportedFeaturesFreeMembers.argtypes = [WGPUSupportedFeatures]
except AttributeError:
    pass
try:
    wgpuSupportedInstanceFeaturesFreeMembers = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSupportedInstanceFeaturesFreeMembers
    wgpuSupportedInstanceFeaturesFreeMembers.restype = None
    wgpuSupportedInstanceFeaturesFreeMembers.argtypes = [WGPUSupportedInstanceFeatures]
except AttributeError:
    pass
try:
    wgpuSupportedWGSLLanguageFeaturesFreeMembers = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSupportedWGSLLanguageFeaturesFreeMembers
    wgpuSupportedWGSLLanguageFeaturesFreeMembers.restype = None
    wgpuSupportedWGSLLanguageFeaturesFreeMembers.argtypes = [WGPUSupportedWGSLLanguageFeatures]
except AttributeError:
    pass
try:
    wgpuSurfaceConfigure = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSurfaceConfigure
    wgpuSurfaceConfigure.restype = None
    wgpuSurfaceConfigure.argtypes = [WGPUSurface, ctypes.POINTER(struct_WGPUSurfaceConfiguration)]
except AttributeError:
    pass
try:
    wgpuSurfaceGetCapabilities = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSurfaceGetCapabilities
    wgpuSurfaceGetCapabilities.restype = WGPUStatus
    wgpuSurfaceGetCapabilities.argtypes = [WGPUSurface, WGPUAdapter, ctypes.POINTER(struct_WGPUSurfaceCapabilities)]
except AttributeError:
    pass
try:
    wgpuSurfaceGetCurrentTexture = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSurfaceGetCurrentTexture
    wgpuSurfaceGetCurrentTexture.restype = None
    wgpuSurfaceGetCurrentTexture.argtypes = [WGPUSurface, ctypes.POINTER(struct_WGPUSurfaceTexture)]
except AttributeError:
    pass
try:
    wgpuSurfacePresent = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSurfacePresent
    wgpuSurfacePresent.restype = WGPUStatus
    wgpuSurfacePresent.argtypes = [WGPUSurface]
except AttributeError:
    pass
try:
    wgpuSurfaceSetLabel = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSurfaceSetLabel
    wgpuSurfaceSetLabel.restype = None
    wgpuSurfaceSetLabel.argtypes = [WGPUSurface, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuSurfaceUnconfigure = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSurfaceUnconfigure
    wgpuSurfaceUnconfigure.restype = None
    wgpuSurfaceUnconfigure.argtypes = [WGPUSurface]
except AttributeError:
    pass
try:
    wgpuSurfaceAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSurfaceAddRef
    wgpuSurfaceAddRef.restype = None
    wgpuSurfaceAddRef.argtypes = [WGPUSurface]
except AttributeError:
    pass
try:
    wgpuSurfaceRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSurfaceRelease
    wgpuSurfaceRelease.restype = None
    wgpuSurfaceRelease.argtypes = [WGPUSurface]
except AttributeError:
    pass
try:
    wgpuSurfaceCapabilitiesFreeMembers = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuSurfaceCapabilitiesFreeMembers
    wgpuSurfaceCapabilitiesFreeMembers.restype = None
    wgpuSurfaceCapabilitiesFreeMembers.argtypes = [WGPUSurfaceCapabilities]
except AttributeError:
    pass
try:
    wgpuTexelBufferViewSetLabel = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuTexelBufferViewSetLabel
    wgpuTexelBufferViewSetLabel.restype = None
    wgpuTexelBufferViewSetLabel.argtypes = [WGPUTexelBufferView, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuTexelBufferViewAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuTexelBufferViewAddRef
    wgpuTexelBufferViewAddRef.restype = None
    wgpuTexelBufferViewAddRef.argtypes = [WGPUTexelBufferView]
except AttributeError:
    pass
try:
    wgpuTexelBufferViewRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuTexelBufferViewRelease
    wgpuTexelBufferViewRelease.restype = None
    wgpuTexelBufferViewRelease.argtypes = [WGPUTexelBufferView]
except AttributeError:
    pass
try:
    wgpuTextureCreateErrorView = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuTextureCreateErrorView
    wgpuTextureCreateErrorView.restype = WGPUTextureView
    wgpuTextureCreateErrorView.argtypes = [WGPUTexture, ctypes.POINTER(struct_WGPUTextureViewDescriptor)]
except AttributeError:
    pass
try:
    wgpuTextureCreateView = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuTextureCreateView
    wgpuTextureCreateView.restype = WGPUTextureView
    wgpuTextureCreateView.argtypes = [WGPUTexture, ctypes.POINTER(struct_WGPUTextureViewDescriptor)]
except AttributeError:
    pass
try:
    wgpuTextureDestroy = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuTextureDestroy
    wgpuTextureDestroy.restype = None
    wgpuTextureDestroy.argtypes = [WGPUTexture]
except AttributeError:
    pass
try:
    wgpuTextureGetDepthOrArrayLayers = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuTextureGetDepthOrArrayLayers
    wgpuTextureGetDepthOrArrayLayers.restype = uint32_t
    wgpuTextureGetDepthOrArrayLayers.argtypes = [WGPUTexture]
except AttributeError:
    pass
try:
    wgpuTextureGetDimension = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuTextureGetDimension
    wgpuTextureGetDimension.restype = WGPUTextureDimension
    wgpuTextureGetDimension.argtypes = [WGPUTexture]
except AttributeError:
    pass
try:
    wgpuTextureGetFormat = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuTextureGetFormat
    wgpuTextureGetFormat.restype = WGPUTextureFormat
    wgpuTextureGetFormat.argtypes = [WGPUTexture]
except AttributeError:
    pass
try:
    wgpuTextureGetHeight = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuTextureGetHeight
    wgpuTextureGetHeight.restype = uint32_t
    wgpuTextureGetHeight.argtypes = [WGPUTexture]
except AttributeError:
    pass
try:
    wgpuTextureGetMipLevelCount = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuTextureGetMipLevelCount
    wgpuTextureGetMipLevelCount.restype = uint32_t
    wgpuTextureGetMipLevelCount.argtypes = [WGPUTexture]
except AttributeError:
    pass
try:
    wgpuTextureGetSampleCount = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuTextureGetSampleCount
    wgpuTextureGetSampleCount.restype = uint32_t
    wgpuTextureGetSampleCount.argtypes = [WGPUTexture]
except AttributeError:
    pass
try:
    wgpuTextureGetUsage = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuTextureGetUsage
    wgpuTextureGetUsage.restype = WGPUTextureUsage
    wgpuTextureGetUsage.argtypes = [WGPUTexture]
except AttributeError:
    pass
try:
    wgpuTextureGetWidth = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuTextureGetWidth
    wgpuTextureGetWidth.restype = uint32_t
    wgpuTextureGetWidth.argtypes = [WGPUTexture]
except AttributeError:
    pass
try:
    wgpuTexturePin = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuTexturePin
    wgpuTexturePin.restype = None
    wgpuTexturePin.argtypes = [WGPUTexture, WGPUTextureUsage]
except AttributeError:
    pass
try:
    wgpuTextureSetLabel = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuTextureSetLabel
    wgpuTextureSetLabel.restype = None
    wgpuTextureSetLabel.argtypes = [WGPUTexture, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuTextureUnpin = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuTextureUnpin
    wgpuTextureUnpin.restype = None
    wgpuTextureUnpin.argtypes = [WGPUTexture]
except AttributeError:
    pass
try:
    wgpuTextureAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuTextureAddRef
    wgpuTextureAddRef.restype = None
    wgpuTextureAddRef.argtypes = [WGPUTexture]
except AttributeError:
    pass
try:
    wgpuTextureRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuTextureRelease
    wgpuTextureRelease.restype = None
    wgpuTextureRelease.argtypes = [WGPUTexture]
except AttributeError:
    pass
try:
    wgpuTextureViewSetLabel = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuTextureViewSetLabel
    wgpuTextureViewSetLabel.restype = None
    wgpuTextureViewSetLabel.argtypes = [WGPUTextureView, WGPUStringView]
except AttributeError:
    pass
try:
    wgpuTextureViewAddRef = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuTextureViewAddRef
    wgpuTextureViewAddRef.restype = None
    wgpuTextureViewAddRef.argtypes = [WGPUTextureView]
except AttributeError:
    pass
try:
    wgpuTextureViewRelease = _libraries['libwebgpu_dawn_subgroup_test.dylib'].wgpuTextureViewRelease
    wgpuTextureViewRelease.restype = None
    wgpuTextureViewRelease.argtypes = [WGPUTextureView]
except AttributeError:
    pass
__all__ = \
    ['WGPUAHardwareBufferProperties', 'WGPUAdapter',
    'WGPUAdapterInfo', 'WGPUAdapterPropertiesD3D',
    'WGPUAdapterPropertiesMemoryHeaps',
    'WGPUAdapterPropertiesSubgroupMatrixConfigs',
    'WGPUAdapterPropertiesVk', 'WGPUAdapterPropertiesWGPU',
    'WGPUAdapterType', 'WGPUAdapterType_CPU',
    'WGPUAdapterType_DiscreteGPU', 'WGPUAdapterType_Force32',
    'WGPUAdapterType_IntegratedGPU', 'WGPUAdapterType_Unknown',
    'WGPUAddressMode', 'WGPUAddressMode_ClampToEdge',
    'WGPUAddressMode_Force32', 'WGPUAddressMode_MirrorRepeat',
    'WGPUAddressMode_Repeat', 'WGPUAddressMode_Undefined',
    'WGPUAlphaMode', 'WGPUAlphaMode_Force32', 'WGPUAlphaMode_Opaque',
    'WGPUAlphaMode_Premultiplied', 'WGPUAlphaMode_Unpremultiplied',
    'WGPUBackendType', 'WGPUBackendType_D3D11',
    'WGPUBackendType_D3D12', 'WGPUBackendType_Force32',
    'WGPUBackendType_Metal', 'WGPUBackendType_Null',
    'WGPUBackendType_OpenGL', 'WGPUBackendType_OpenGLES',
    'WGPUBackendType_Undefined', 'WGPUBackendType_Vulkan',
    'WGPUBackendType_WebGPU', 'WGPUBindGroup',
    'WGPUBindGroupDescriptor', 'WGPUBindGroupDynamicBindingArray',
    'WGPUBindGroupEntry', 'WGPUBindGroupEntryContents',
    'WGPUBindGroupLayout', 'WGPUBindGroupLayoutDescriptor',
    'WGPUBindGroupLayoutDynamicBindingArray',
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
    'WGPUBufferBindingType_BindingNotUsed',
    'WGPUBufferBindingType_Force32',
    'WGPUBufferBindingType_ReadOnlyStorage',
    'WGPUBufferBindingType_Storage',
    'WGPUBufferBindingType_Undefined',
    'WGPUBufferBindingType_Uniform', 'WGPUBufferDescriptor',
    'WGPUBufferHostMappedPointer', 'WGPUBufferMapCallback',
    'WGPUBufferMapCallbackInfo', 'WGPUBufferMapState',
    'WGPUBufferMapState_Force32', 'WGPUBufferMapState_Mapped',
    'WGPUBufferMapState_Pending', 'WGPUBufferMapState_Unmapped',
    'WGPUBufferUsage', 'WGPUBufferUsage_CopyDst',
    'WGPUBufferUsage_CopySrc', 'WGPUBufferUsage_Index',
    'WGPUBufferUsage_Indirect', 'WGPUBufferUsage_MapRead',
    'WGPUBufferUsage_MapWrite', 'WGPUBufferUsage_None',
    'WGPUBufferUsage_QueryResolve', 'WGPUBufferUsage_Storage',
    'WGPUBufferUsage_TexelBuffer', 'WGPUBufferUsage_Uniform',
    'WGPUBufferUsage_Vertex', 'WGPUCallback', 'WGPUCallbackMode',
    'WGPUCallbackMode_AllowProcessEvents',
    'WGPUCallbackMode_AllowSpontaneous', 'WGPUCallbackMode_Force32',
    'WGPUCallbackMode_WaitAnyOnly', 'WGPUChainedStruct', 'WGPUColor',
    'WGPUColorTargetState',
    'WGPUColorTargetStateExpandResolveTextureDawn',
    'WGPUColorWriteMask', 'WGPUColorWriteMask_All',
    'WGPUColorWriteMask_Alpha', 'WGPUColorWriteMask_Blue',
    'WGPUColorWriteMask_Green', 'WGPUColorWriteMask_None',
    'WGPUColorWriteMask_Red', 'WGPUCommandBuffer',
    'WGPUCommandBufferDescriptor', 'WGPUCommandEncoder',
    'WGPUCommandEncoderDescriptor', 'WGPUCompareFunction',
    'WGPUCompareFunction_Always', 'WGPUCompareFunction_Equal',
    'WGPUCompareFunction_Force32', 'WGPUCompareFunction_Greater',
    'WGPUCompareFunction_GreaterEqual', 'WGPUCompareFunction_Less',
    'WGPUCompareFunction_LessEqual', 'WGPUCompareFunction_Never',
    'WGPUCompareFunction_NotEqual', 'WGPUCompareFunction_Undefined',
    'WGPUCompatibilityModeLimits', 'WGPUCompilationInfo',
    'WGPUCompilationInfoCallback', 'WGPUCompilationInfoCallbackInfo',
    'WGPUCompilationInfoRequestStatus',
    'WGPUCompilationInfoRequestStatus_CallbackCancelled',
    'WGPUCompilationInfoRequestStatus_Force32',
    'WGPUCompilationInfoRequestStatus_Success',
    'WGPUCompilationMessage', 'WGPUCompilationMessageType',
    'WGPUCompilationMessageType_Error',
    'WGPUCompilationMessageType_Force32',
    'WGPUCompilationMessageType_Info',
    'WGPUCompilationMessageType_Warning', 'WGPUComponentSwizzle',
    'WGPUComponentSwizzle_A', 'WGPUComponentSwizzle_B',
    'WGPUComponentSwizzle_Force32', 'WGPUComponentSwizzle_G',
    'WGPUComponentSwizzle_One', 'WGPUComponentSwizzle_R',
    'WGPUComponentSwizzle_Undefined', 'WGPUComponentSwizzle_Zero',
    'WGPUCompositeAlphaMode', 'WGPUCompositeAlphaMode_Auto',
    'WGPUCompositeAlphaMode_Force32',
    'WGPUCompositeAlphaMode_Inherit', 'WGPUCompositeAlphaMode_Opaque',
    'WGPUCompositeAlphaMode_Premultiplied',
    'WGPUCompositeAlphaMode_Unpremultiplied',
    'WGPUComputePassDescriptor', 'WGPUComputePassEncoder',
    'WGPUComputePipeline', 'WGPUComputePipelineDescriptor',
    'WGPUComputeState', 'WGPUConstantEntry',
    'WGPUCopyTextureForBrowserOptions',
    'WGPUCreateComputePipelineAsyncCallback',
    'WGPUCreateComputePipelineAsyncCallbackInfo',
    'WGPUCreatePipelineAsyncStatus',
    'WGPUCreatePipelineAsyncStatus_CallbackCancelled',
    'WGPUCreatePipelineAsyncStatus_Force32',
    'WGPUCreatePipelineAsyncStatus_InternalError',
    'WGPUCreatePipelineAsyncStatus_Success',
    'WGPUCreatePipelineAsyncStatus_ValidationError',
    'WGPUCreateRenderPipelineAsyncCallback',
    'WGPUCreateRenderPipelineAsyncCallbackInfo', 'WGPUCullMode',
    'WGPUCullMode_Back', 'WGPUCullMode_Force32', 'WGPUCullMode_Front',
    'WGPUCullMode_None', 'WGPUCullMode_Undefined',
    'WGPUDawnAdapterPropertiesPowerPreference',
    'WGPUDawnBufferDescriptorErrorInfoFromWireClient',
    'WGPUDawnCacheDeviceDescriptor',
    'WGPUDawnCompilationMessageUtf16',
    'WGPUDawnConsumeAdapterDescriptor',
    'WGPUDawnDeviceAllocatorControl', 'WGPUDawnDrmFormatCapabilities',
    'WGPUDawnDrmFormatProperties',
    'WGPUDawnEncoderInternalUsageDescriptor',
    'WGPUDawnFakeBufferOOMForTesting',
    'WGPUDawnFakeDeviceInitializeErrorForTesting',
    'WGPUDawnFormatCapabilities', 'WGPUDawnHostMappedPointerLimits',
    'WGPUDawnInjectedInvalidSType', 'WGPUDawnLoadCacheDataFunction',
    'WGPUDawnRenderPassColorAttachmentRenderToSingleSampled',
    'WGPUDawnShaderModuleSPIRVOptionsDescriptor',
    'WGPUDawnStoreCacheDataFunction',
    'WGPUDawnTexelCopyBufferRowAlignmentLimits',
    'WGPUDawnTextureInternalUsageDescriptor',
    'WGPUDawnTogglesDescriptor', 'WGPUDawnWGSLBlocklist',
    'WGPUDawnWireWGSLControl', 'WGPUDepthStencilState', 'WGPUDevice',
    'WGPUDeviceDescriptor', 'WGPUDeviceLostCallback',
    'WGPUDeviceLostCallbackInfo', 'WGPUDeviceLostReason',
    'WGPUDeviceLostReason_CallbackCancelled',
    'WGPUDeviceLostReason_Destroyed',
    'WGPUDeviceLostReason_FailedCreation',
    'WGPUDeviceLostReason_Force32', 'WGPUDeviceLostReason_Unknown',
    'WGPUDynamicBindingArrayLayout', 'WGPUDynamicBindingArrayLimits',
    'WGPUDynamicBindingKind', 'WGPUDynamicBindingKind_Force32',
    'WGPUDynamicBindingKind_SampledTexture',
    'WGPUDynamicBindingKind_Undefined',
    'WGPUEmscriptenSurfaceSourceCanvasHTMLSelector',
    'WGPUErrorFilter', 'WGPUErrorFilter_Force32',
    'WGPUErrorFilter_Internal', 'WGPUErrorFilter_OutOfMemory',
    'WGPUErrorFilter_Validation', 'WGPUErrorType',
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
    'WGPUExternalTextureRotation_Rotate90Degrees', 'WGPUFeatureLevel',
    'WGPUFeatureLevel_Compatibility', 'WGPUFeatureLevel_Core',
    'WGPUFeatureLevel_Force32', 'WGPUFeatureLevel_Undefined',
    'WGPUFeatureName', 'WGPUFeatureName_ANGLETextureSharing',
    'WGPUFeatureName_AdapterPropertiesD3D',
    'WGPUFeatureName_AdapterPropertiesMemoryHeaps',
    'WGPUFeatureName_AdapterPropertiesVk',
    'WGPUFeatureName_AdapterPropertiesWGPU',
    'WGPUFeatureName_BGRA8UnormStorage',
    'WGPUFeatureName_BufferMapExtendedUsages',
    'WGPUFeatureName_ChromiumExperimentalBindless',
    'WGPUFeatureName_ChromiumExperimentalSamplingResourceTable',
    'WGPUFeatureName_ChromiumExperimentalSubgroupMatrix',
    'WGPUFeatureName_ChromiumExperimentalTimestampQueryInsidePasses',
    'WGPUFeatureName_ClipDistances',
    'WGPUFeatureName_CoreFeaturesAndLimits',
    'WGPUFeatureName_D3D11MultithreadProtected',
    'WGPUFeatureName_DawnDeviceAllocatorControl',
    'WGPUFeatureName_DawnDrmFormatCapabilities',
    'WGPUFeatureName_DawnFormatCapabilities',
    'WGPUFeatureName_DawnInternalUsages',
    'WGPUFeatureName_DawnLoadResolveTexture',
    'WGPUFeatureName_DawnMultiPlanarFormats',
    'WGPUFeatureName_DawnNative',
    'WGPUFeatureName_DawnPartialLoadResolveTexture',
    'WGPUFeatureName_DawnTexelCopyBufferRowAlignment',
    'WGPUFeatureName_Depth32FloatStencil8',
    'WGPUFeatureName_DepthClipControl',
    'WGPUFeatureName_DualSourceBlending',
    'WGPUFeatureName_FlexibleTextureViews',
    'WGPUFeatureName_Float32Blendable',
    'WGPUFeatureName_Float32Filterable', 'WGPUFeatureName_Force32',
    'WGPUFeatureName_FramebufferFetch',
    'WGPUFeatureName_HostMappedPointer',
    'WGPUFeatureName_ImplicitDeviceSynchronization',
    'WGPUFeatureName_IndirectFirstInstance',
    'WGPUFeatureName_MSAARenderToSingleSampled',
    'WGPUFeatureName_MultiDrawIndirect',
    'WGPUFeatureName_MultiPlanarFormatExtendedUsages',
    'WGPUFeatureName_MultiPlanarFormatNv12a',
    'WGPUFeatureName_MultiPlanarFormatNv16',
    'WGPUFeatureName_MultiPlanarFormatNv24',
    'WGPUFeatureName_MultiPlanarFormatP010',
    'WGPUFeatureName_MultiPlanarFormatP210',
    'WGPUFeatureName_MultiPlanarFormatP410',
    'WGPUFeatureName_MultiPlanarRenderTargets',
    'WGPUFeatureName_PixelLocalStorageCoherent',
    'WGPUFeatureName_PixelLocalStorageNonCoherent',
    'WGPUFeatureName_PrimitiveIndex',
    'WGPUFeatureName_R8UnormStorage',
    'WGPUFeatureName_RG11B10UfloatRenderable',
    'WGPUFeatureName_ShaderF16',
    'WGPUFeatureName_ShaderModuleCompilationOptions',
    'WGPUFeatureName_SharedBufferMemoryD3D12Resource',
    'WGPUFeatureName_SharedBufferMemoryD3D12SharedMemoryFileMappingHandle',
    'WGPUFeatureName_SharedFenceDXGISharedHandle',
    'WGPUFeatureName_SharedFenceEGLSync',
    'WGPUFeatureName_SharedFenceMTLSharedEvent',
    'WGPUFeatureName_SharedFenceSyncFD',
    'WGPUFeatureName_SharedFenceVkSemaphoreOpaqueFD',
    'WGPUFeatureName_SharedFenceVkSemaphoreZirconHandle',
    'WGPUFeatureName_SharedTextureMemoryAHardwareBuffer',
    'WGPUFeatureName_SharedTextureMemoryD3D11Texture2D',
    'WGPUFeatureName_SharedTextureMemoryD3D12Resource',
    'WGPUFeatureName_SharedTextureMemoryDXGISharedHandle',
    'WGPUFeatureName_SharedTextureMemoryDmaBuf',
    'WGPUFeatureName_SharedTextureMemoryEGLImage',
    'WGPUFeatureName_SharedTextureMemoryIOSurface',
    'WGPUFeatureName_SharedTextureMemoryOpaqueFD',
    'WGPUFeatureName_SharedTextureMemoryVkDedicatedAllocation',
    'WGPUFeatureName_SharedTextureMemoryZirconHandle',
    'WGPUFeatureName_StaticSamplers', 'WGPUFeatureName_Subgroups',
    'WGPUFeatureName_TextureComponentSwizzle',
    'WGPUFeatureName_TextureCompressionASTC',
    'WGPUFeatureName_TextureCompressionASTCSliced3D',
    'WGPUFeatureName_TextureCompressionBC',
    'WGPUFeatureName_TextureCompressionBCSliced3D',
    'WGPUFeatureName_TextureCompressionETC2',
    'WGPUFeatureName_TextureFormatsTier1',
    'WGPUFeatureName_TextureFormatsTier2',
    'WGPUFeatureName_TimestampQuery',
    'WGPUFeatureName_TransientAttachments',
    'WGPUFeatureName_Unorm16TextureFormats',
    'WGPUFeatureName_YCbCrVulkanSamplers', 'WGPUFilterMode',
    'WGPUFilterMode_Force32', 'WGPUFilterMode_Linear',
    'WGPUFilterMode_Nearest', 'WGPUFilterMode_Undefined', 'WGPUFlags',
    'WGPUFragmentState', 'WGPUFrontFace', 'WGPUFrontFace_CCW',
    'WGPUFrontFace_CW', 'WGPUFrontFace_Force32',
    'WGPUFrontFace_Undefined', 'WGPUFuture', 'WGPUFutureWaitInfo',
    'WGPUHeapProperty', 'WGPUHeapProperty_DeviceLocal',
    'WGPUHeapProperty_HostCached', 'WGPUHeapProperty_HostCoherent',
    'WGPUHeapProperty_HostUncached', 'WGPUHeapProperty_HostVisible',
    'WGPUHeapProperty_None', 'WGPUINTERNAL_HAVE_EMDAWNWEBGPU_HEADER',
    'WGPUImageCopyExternalTexture', 'WGPUIndexFormat',
    'WGPUIndexFormat_Force32', 'WGPUIndexFormat_Uint16',
    'WGPUIndexFormat_Uint32', 'WGPUIndexFormat_Undefined',
    'WGPUInstance', 'WGPUInstanceDescriptor',
    'WGPUInstanceFeatureName', 'WGPUInstanceFeatureName_Force32',
    'WGPUInstanceFeatureName_MultipleDevicesPerAdapter',
    'WGPUInstanceFeatureName_ShaderSourceSPIRV',
    'WGPUInstanceFeatureName_TimedWaitAny', 'WGPUInstanceLimits',
    'WGPULimits', 'WGPULoadOp', 'WGPULoadOp_Clear',
    'WGPULoadOp_ExpandResolveTexture', 'WGPULoadOp_Force32',
    'WGPULoadOp_Load', 'WGPULoadOp_Undefined', 'WGPULoggingCallback',
    'WGPULoggingCallbackInfo', 'WGPULoggingType',
    'WGPULoggingType_Error', 'WGPULoggingType_Force32',
    'WGPULoggingType_Info', 'WGPULoggingType_Verbose',
    'WGPULoggingType_Warning', 'WGPUMapAsyncStatus',
    'WGPUMapAsyncStatus_Aborted',
    'WGPUMapAsyncStatus_CallbackCancelled',
    'WGPUMapAsyncStatus_Error', 'WGPUMapAsyncStatus_Force32',
    'WGPUMapAsyncStatus_Success', 'WGPUMapMode', 'WGPUMapMode_None',
    'WGPUMapMode_Read', 'WGPUMapMode_Write', 'WGPUMemoryHeapInfo',
    'WGPUMipmapFilterMode', 'WGPUMipmapFilterMode_Force32',
    'WGPUMipmapFilterMode_Linear', 'WGPUMipmapFilterMode_Nearest',
    'WGPUMipmapFilterMode_Undefined', 'WGPUMultisampleState',
    'WGPUOptionalBool', 'WGPUOptionalBool_False',
    'WGPUOptionalBool_Force32', 'WGPUOptionalBool_True',
    'WGPUOptionalBool_Undefined', 'WGPUOrigin2D', 'WGPUOrigin3D',
    'WGPUPassTimestampWrites', 'WGPUPipelineLayout',
    'WGPUPipelineLayoutDescriptor',
    'WGPUPipelineLayoutPixelLocalStorage',
    'WGPUPipelineLayoutResourceTable',
    'WGPUPipelineLayoutStorageAttachment',
    'WGPUPopErrorScopeCallback', 'WGPUPopErrorScopeCallbackInfo',
    'WGPUPopErrorScopeStatus',
    'WGPUPopErrorScopeStatus_CallbackCancelled',
    'WGPUPopErrorScopeStatus_Error',
    'WGPUPopErrorScopeStatus_Force32',
    'WGPUPopErrorScopeStatus_Success', 'WGPUPowerPreference',
    'WGPUPowerPreference_Force32',
    'WGPUPowerPreference_HighPerformance',
    'WGPUPowerPreference_LowPower', 'WGPUPowerPreference_Undefined',
    'WGPUPredefinedColorSpace', 'WGPUPredefinedColorSpace_DisplayP3',
    'WGPUPredefinedColorSpace_Force32',
    'WGPUPredefinedColorSpace_SRGB', 'WGPUPresentMode',
    'WGPUPresentMode_Fifo', 'WGPUPresentMode_FifoRelaxed',
    'WGPUPresentMode_Force32', 'WGPUPresentMode_Immediate',
    'WGPUPresentMode_Mailbox', 'WGPUPresentMode_Undefined',
    'WGPUPrimitiveState', 'WGPUPrimitiveTopology',
    'WGPUPrimitiveTopology_Force32', 'WGPUPrimitiveTopology_LineList',
    'WGPUPrimitiveTopology_LineStrip',
    'WGPUPrimitiveTopology_PointList',
    'WGPUPrimitiveTopology_TriangleList',
    'WGPUPrimitiveTopology_TriangleStrip',
    'WGPUPrimitiveTopology_Undefined', 'WGPUProc',
    'WGPUProcAdapterAddRef', 'WGPUProcAdapterCreateDevice',
    'WGPUProcAdapterGetFeatures',
    'WGPUProcAdapterGetFormatCapabilities', 'WGPUProcAdapterGetInfo',
    'WGPUProcAdapterGetInstance', 'WGPUProcAdapterGetLimits',
    'WGPUProcAdapterHasFeature', 'WGPUProcAdapterInfoFreeMembers',
    'WGPUProcAdapterPropertiesMemoryHeapsFreeMembers',
    'WGPUProcAdapterPropertiesSubgroupMatrixConfigsFreeMembers',
    'WGPUProcAdapterRelease', 'WGPUProcAdapterRequestDevice',
    'WGPUProcBindGroupAddRef', 'WGPUProcBindGroupDestroy',
    'WGPUProcBindGroupInsertBinding', 'WGPUProcBindGroupLayoutAddRef',
    'WGPUProcBindGroupLayoutRelease',
    'WGPUProcBindGroupLayoutSetLabel', 'WGPUProcBindGroupRelease',
    'WGPUProcBindGroupRemoveBinding', 'WGPUProcBindGroupSetLabel',
    'WGPUProcBindGroupUpdate', 'WGPUProcBufferAddRef',
    'WGPUProcBufferCreateTexelView', 'WGPUProcBufferDestroy',
    'WGPUProcBufferGetConstMappedRange', 'WGPUProcBufferGetMapState',
    'WGPUProcBufferGetMappedRange', 'WGPUProcBufferGetSize',
    'WGPUProcBufferGetUsage', 'WGPUProcBufferMapAsync',
    'WGPUProcBufferReadMappedRange', 'WGPUProcBufferRelease',
    'WGPUProcBufferSetLabel', 'WGPUProcBufferUnmap',
    'WGPUProcBufferWriteMappedRange', 'WGPUProcCommandBufferAddRef',
    'WGPUProcCommandBufferRelease', 'WGPUProcCommandBufferSetLabel',
    'WGPUProcCommandEncoderAddRef',
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
    'WGPUProcCommandEncoderSetResourceTable',
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
    'WGPUProcComputePassEncoderSetImmediates',
    'WGPUProcComputePassEncoderSetLabel',
    'WGPUProcComputePassEncoderSetPipeline',
    'WGPUProcComputePassEncoderWriteTimestamp',
    'WGPUProcComputePipelineAddRef',
    'WGPUProcComputePipelineGetBindGroupLayout',
    'WGPUProcComputePipelineRelease',
    'WGPUProcComputePipelineSetLabel', 'WGPUProcCreateInstance',
    'WGPUProcDawnDrmFormatCapabilitiesFreeMembers',
    'WGPUProcDeviceAddRef', 'WGPUProcDeviceCreateBindGroup',
    'WGPUProcDeviceCreateBindGroupLayout',
    'WGPUProcDeviceCreateBuffer',
    'WGPUProcDeviceCreateCommandEncoder',
    'WGPUProcDeviceCreateComputePipeline',
    'WGPUProcDeviceCreateComputePipelineAsync',
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
    'WGPUProcDeviceCreateResourceTable',
    'WGPUProcDeviceCreateSampler', 'WGPUProcDeviceCreateShaderModule',
    'WGPUProcDeviceCreateTexture', 'WGPUProcDeviceDestroy',
    'WGPUProcDeviceForceLoss',
    'WGPUProcDeviceGetAHardwareBufferProperties',
    'WGPUProcDeviceGetAdapter', 'WGPUProcDeviceGetAdapterInfo',
    'WGPUProcDeviceGetFeatures', 'WGPUProcDeviceGetLimits',
    'WGPUProcDeviceGetLostFuture', 'WGPUProcDeviceGetQueue',
    'WGPUProcDeviceHasFeature',
    'WGPUProcDeviceImportSharedBufferMemory',
    'WGPUProcDeviceImportSharedFence',
    'WGPUProcDeviceImportSharedTextureMemory',
    'WGPUProcDeviceInjectError', 'WGPUProcDevicePopErrorScope',
    'WGPUProcDevicePushErrorScope', 'WGPUProcDeviceRelease',
    'WGPUProcDeviceSetLabel', 'WGPUProcDeviceSetLoggingCallback',
    'WGPUProcDeviceTick', 'WGPUProcDeviceValidateTextureDescriptor',
    'WGPUProcExternalTextureAddRef', 'WGPUProcExternalTextureDestroy',
    'WGPUProcExternalTextureExpire', 'WGPUProcExternalTextureRefresh',
    'WGPUProcExternalTextureRelease',
    'WGPUProcExternalTextureSetLabel', 'WGPUProcGetInstanceFeatures',
    'WGPUProcGetInstanceLimits', 'WGPUProcGetProcAddress',
    'WGPUProcHasInstanceFeature', 'WGPUProcInstanceAddRef',
    'WGPUProcInstanceCreateSurface',
    'WGPUProcInstanceGetWGSLLanguageFeatures',
    'WGPUProcInstanceHasWGSLLanguageFeature',
    'WGPUProcInstanceProcessEvents', 'WGPUProcInstanceRelease',
    'WGPUProcInstanceRequestAdapter', 'WGPUProcInstanceWaitAny',
    'WGPUProcPipelineLayoutAddRef', 'WGPUProcPipelineLayoutRelease',
    'WGPUProcPipelineLayoutSetLabel', 'WGPUProcQuerySetAddRef',
    'WGPUProcQuerySetDestroy', 'WGPUProcQuerySetGetCount',
    'WGPUProcQuerySetGetType', 'WGPUProcQuerySetRelease',
    'WGPUProcQuerySetSetLabel', 'WGPUProcQueueAddRef',
    'WGPUProcQueueCopyExternalTextureForBrowser',
    'WGPUProcQueueCopyTextureForBrowser',
    'WGPUProcQueueOnSubmittedWorkDone', 'WGPUProcQueueRelease',
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
    'WGPUProcRenderBundleEncoderSetImmediates',
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
    'WGPUProcRenderPassEncoderMultiDrawIndexedIndirect',
    'WGPUProcRenderPassEncoderMultiDrawIndirect',
    'WGPUProcRenderPassEncoderPixelLocalStorageBarrier',
    'WGPUProcRenderPassEncoderPopDebugGroup',
    'WGPUProcRenderPassEncoderPushDebugGroup',
    'WGPUProcRenderPassEncoderRelease',
    'WGPUProcRenderPassEncoderSetBindGroup',
    'WGPUProcRenderPassEncoderSetBlendConstant',
    'WGPUProcRenderPassEncoderSetImmediates',
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
    'WGPUProcResourceTableAddRef', 'WGPUProcResourceTableDestroy',
    'WGPUProcResourceTableRelease', 'WGPUProcSamplerAddRef',
    'WGPUProcSamplerRelease', 'WGPUProcSamplerSetLabel',
    'WGPUProcShaderModuleAddRef',
    'WGPUProcShaderModuleGetCompilationInfo',
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
    'WGPUProcSharedTextureMemorySetLabel',
    'WGPUProcSupportedFeaturesFreeMembers',
    'WGPUProcSupportedInstanceFeaturesFreeMembers',
    'WGPUProcSupportedWGSLLanguageFeaturesFreeMembers',
    'WGPUProcSurfaceAddRef', 'WGPUProcSurfaceCapabilitiesFreeMembers',
    'WGPUProcSurfaceConfigure', 'WGPUProcSurfaceGetCapabilities',
    'WGPUProcSurfaceGetCurrentTexture', 'WGPUProcSurfacePresent',
    'WGPUProcSurfaceRelease', 'WGPUProcSurfaceSetLabel',
    'WGPUProcSurfaceUnconfigure', 'WGPUProcTexelBufferViewAddRef',
    'WGPUProcTexelBufferViewRelease',
    'WGPUProcTexelBufferViewSetLabel', 'WGPUProcTextureAddRef',
    'WGPUProcTextureCreateErrorView', 'WGPUProcTextureCreateView',
    'WGPUProcTextureDestroy', 'WGPUProcTextureGetDepthOrArrayLayers',
    'WGPUProcTextureGetDimension', 'WGPUProcTextureGetFormat',
    'WGPUProcTextureGetHeight', 'WGPUProcTextureGetMipLevelCount',
    'WGPUProcTextureGetSampleCount', 'WGPUProcTextureGetUsage',
    'WGPUProcTextureGetWidth', 'WGPUProcTexturePin',
    'WGPUProcTextureRelease', 'WGPUProcTextureSetLabel',
    'WGPUProcTextureUnpin', 'WGPUProcTextureViewAddRef',
    'WGPUProcTextureViewRelease', 'WGPUProcTextureViewSetLabel',
    'WGPUQuerySet', 'WGPUQuerySetDescriptor', 'WGPUQueryType',
    'WGPUQueryType_Force32', 'WGPUQueryType_Occlusion',
    'WGPUQueryType_Timestamp', 'WGPUQueue', 'WGPUQueueDescriptor',
    'WGPUQueueWorkDoneCallback', 'WGPUQueueWorkDoneCallbackInfo',
    'WGPUQueueWorkDoneStatus',
    'WGPUQueueWorkDoneStatus_CallbackCancelled',
    'WGPUQueueWorkDoneStatus_Error',
    'WGPUQueueWorkDoneStatus_Force32',
    'WGPUQueueWorkDoneStatus_Success', 'WGPURenderBundle',
    'WGPURenderBundleDescriptor', 'WGPURenderBundleEncoder',
    'WGPURenderBundleEncoderDescriptor',
    'WGPURenderPassColorAttachment',
    'WGPURenderPassDepthStencilAttachment',
    'WGPURenderPassDescriptor',
    'WGPURenderPassDescriptorExpandResolveRect',
    'WGPURenderPassDescriptorResolveRect', 'WGPURenderPassEncoder',
    'WGPURenderPassMaxDrawCount', 'WGPURenderPassPixelLocalStorage',
    'WGPURenderPassStorageAttachment', 'WGPURenderPipeline',
    'WGPURenderPipelineDescriptor', 'WGPURequestAdapterCallback',
    'WGPURequestAdapterCallbackInfo', 'WGPURequestAdapterOptions',
    'WGPURequestAdapterStatus',
    'WGPURequestAdapterStatus_CallbackCancelled',
    'WGPURequestAdapterStatus_Error',
    'WGPURequestAdapterStatus_Force32',
    'WGPURequestAdapterStatus_Success',
    'WGPURequestAdapterStatus_Unavailable',
    'WGPURequestAdapterWebGPUBackendOptions',
    'WGPURequestAdapterWebXROptions', 'WGPURequestDeviceCallback',
    'WGPURequestDeviceCallbackInfo', 'WGPURequestDeviceStatus',
    'WGPURequestDeviceStatus_CallbackCancelled',
    'WGPURequestDeviceStatus_Error',
    'WGPURequestDeviceStatus_Force32',
    'WGPURequestDeviceStatus_Success', 'WGPUResourceTable',
    'WGPUResourceTableDescriptor', 'WGPUResourceTableLimits',
    'WGPUSType', 'WGPUSType_AHardwareBufferProperties',
    'WGPUSType_AdapterPropertiesD3D',
    'WGPUSType_AdapterPropertiesMemoryHeaps',
    'WGPUSType_AdapterPropertiesSubgroupMatrixConfigs',
    'WGPUSType_AdapterPropertiesVk',
    'WGPUSType_AdapterPropertiesWGPU',
    'WGPUSType_BindGroupDynamicBindingArray',
    'WGPUSType_BindGroupLayoutDynamicBindingArray',
    'WGPUSType_BufferHostMappedPointer',
    'WGPUSType_ColorTargetStateExpandResolveTextureDawn',
    'WGPUSType_CompatibilityModeLimits',
    'WGPUSType_DawnAdapterPropertiesPowerPreference',
    'WGPUSType_DawnBufferDescriptorErrorInfoFromWireClient',
    'WGPUSType_DawnCacheDeviceDescriptor',
    'WGPUSType_DawnCompilationMessageUtf16',
    'WGPUSType_DawnConsumeAdapterDescriptor',
    'WGPUSType_DawnDeviceAllocatorControl',
    'WGPUSType_DawnDrmFormatCapabilities',
    'WGPUSType_DawnEncoderInternalUsageDescriptor',
    'WGPUSType_DawnFakeBufferOOMForTesting',
    'WGPUSType_DawnFakeDeviceInitializeErrorForTesting',
    'WGPUSType_DawnHostMappedPointerLimits',
    'WGPUSType_DawnInjectedInvalidSType',
    'WGPUSType_DawnInstanceDescriptor',
    'WGPUSType_DawnRenderPassColorAttachmentRenderToSingleSampled',
    'WGPUSType_DawnShaderModuleSPIRVOptionsDescriptor',
    'WGPUSType_DawnTexelCopyBufferRowAlignmentLimits',
    'WGPUSType_DawnTextureInternalUsageDescriptor',
    'WGPUSType_DawnTogglesDescriptor', 'WGPUSType_DawnWGSLBlocklist',
    'WGPUSType_DawnWireWGSLControl',
    'WGPUSType_DynamicBindingArrayLimits',
    'WGPUSType_EmscriptenSurfaceSourceCanvasHTMLSelector',
    'WGPUSType_ExternalTextureBindingEntry',
    'WGPUSType_ExternalTextureBindingLayout', 'WGPUSType_Force32',
    'WGPUSType_PipelineLayoutPixelLocalStorage',
    'WGPUSType_PipelineLayoutResourceTable',
    'WGPUSType_RenderPassDescriptorExpandResolveRect',
    'WGPUSType_RenderPassDescriptorResolveRect',
    'WGPUSType_RenderPassMaxDrawCount',
    'WGPUSType_RenderPassPixelLocalStorage',
    'WGPUSType_RequestAdapterOptionsAngleVirtualizationGroup',
    'WGPUSType_RequestAdapterOptionsD3D11Device',
    'WGPUSType_RequestAdapterOptionsGetGLProc',
    'WGPUSType_RequestAdapterOptionsLUID',
    'WGPUSType_RequestAdapterWebGPUBackendOptions',
    'WGPUSType_RequestAdapterWebXROptions',
    'WGPUSType_ResourceTableLimits',
    'WGPUSType_ShaderModuleCompilationOptions',
    'WGPUSType_ShaderSourceSPIRV', 'WGPUSType_ShaderSourceWGSL',
    'WGPUSType_SharedBufferMemoryD3D12ResourceDescriptor',
    'WGPUSType_SharedBufferMemoryD3D12SharedMemoryFileMappingHandleDescriptor',
    'WGPUSType_SharedFenceDXGISharedHandleDescriptor',
    'WGPUSType_SharedFenceDXGISharedHandleExportInfo',
    'WGPUSType_SharedFenceEGLSyncDescriptor',
    'WGPUSType_SharedFenceEGLSyncExportInfo',
    'WGPUSType_SharedFenceMTLSharedEventDescriptor',
    'WGPUSType_SharedFenceMTLSharedEventExportInfo',
    'WGPUSType_SharedFenceSyncFDDescriptor',
    'WGPUSType_SharedFenceSyncFDExportInfo',
    'WGPUSType_SharedFenceVkSemaphoreOpaqueFDDescriptor',
    'WGPUSType_SharedFenceVkSemaphoreOpaqueFDExportInfo',
    'WGPUSType_SharedFenceVkSemaphoreZirconHandleDescriptor',
    'WGPUSType_SharedFenceVkSemaphoreZirconHandleExportInfo',
    'WGPUSType_SharedTextureMemoryAHardwareBufferDescriptor',
    'WGPUSType_SharedTextureMemoryAHardwareBufferProperties',
    'WGPUSType_SharedTextureMemoryD3D11BeginState',
    'WGPUSType_SharedTextureMemoryD3D11Texture2DDescriptor',
    'WGPUSType_SharedTextureMemoryD3D12ResourceDescriptor',
    'WGPUSType_SharedTextureMemoryD3DSwapchainBeginState',
    'WGPUSType_SharedTextureMemoryDXGISharedHandleDescriptor',
    'WGPUSType_SharedTextureMemoryDmaBufDescriptor',
    'WGPUSType_SharedTextureMemoryEGLImageDescriptor',
    'WGPUSType_SharedTextureMemoryIOSurfaceDescriptor',
    'WGPUSType_SharedTextureMemoryInitializedBeginState',
    'WGPUSType_SharedTextureMemoryInitializedEndState',
    'WGPUSType_SharedTextureMemoryMetalEndAccessState',
    'WGPUSType_SharedTextureMemoryOpaqueFDDescriptor',
    'WGPUSType_SharedTextureMemoryVkDedicatedAllocationDescriptor',
    'WGPUSType_SharedTextureMemoryVkImageLayoutBeginState',
    'WGPUSType_SharedTextureMemoryVkImageLayoutEndState',
    'WGPUSType_SharedTextureMemoryZirconHandleDescriptor',
    'WGPUSType_StaticSamplerBindingLayout',
    'WGPUSType_SurfaceColorManagement',
    'WGPUSType_SurfaceDescriptorFromWindowsCoreWindow',
    'WGPUSType_SurfaceDescriptorFromWindowsUWPSwapChainPanel',
    'WGPUSType_SurfaceDescriptorFromWindowsWinUISwapChainPanel',
    'WGPUSType_SurfaceSourceAndroidNativeWindow',
    'WGPUSType_SurfaceSourceMetalLayer',
    'WGPUSType_SurfaceSourceWaylandSurface',
    'WGPUSType_SurfaceSourceWindowsHWND',
    'WGPUSType_SurfaceSourceXCBWindow',
    'WGPUSType_SurfaceSourceXlibWindow',
    'WGPUSType_TexelBufferBindingEntry',
    'WGPUSType_TexelBufferBindingLayout',
    'WGPUSType_TextureBindingViewDimensionDescriptor',
    'WGPUSType_TextureComponentSwizzleDescriptor',
    'WGPUSType_YCbCrVkDescriptor', 'WGPUSampler',
    'WGPUSamplerBindingLayout', 'WGPUSamplerBindingType',
    'WGPUSamplerBindingType_BindingNotUsed',
    'WGPUSamplerBindingType_Comparison',
    'WGPUSamplerBindingType_Filtering',
    'WGPUSamplerBindingType_Force32',
    'WGPUSamplerBindingType_NonFiltering',
    'WGPUSamplerBindingType_Undefined', 'WGPUSamplerDescriptor',
    'WGPUShaderModule', 'WGPUShaderModuleCompilationOptions',
    'WGPUShaderModuleDescriptor', 'WGPUShaderSourceSPIRV',
    'WGPUShaderSourceWGSL', 'WGPUShaderStage',
    'WGPUShaderStage_Compute', 'WGPUShaderStage_Fragment',
    'WGPUShaderStage_None', 'WGPUShaderStage_Vertex',
    'WGPUSharedBufferMemory',
    'WGPUSharedBufferMemoryBeginAccessDescriptor',
    'WGPUSharedBufferMemoryDescriptor',
    'WGPUSharedBufferMemoryEndAccessState',
    'WGPUSharedBufferMemoryProperties', 'WGPUSharedFence',
    'WGPUSharedFenceDXGISharedHandleDescriptor',
    'WGPUSharedFenceDXGISharedHandleExportInfo',
    'WGPUSharedFenceDescriptor', 'WGPUSharedFenceEGLSyncDescriptor',
    'WGPUSharedFenceEGLSyncExportInfo', 'WGPUSharedFenceExportInfo',
    'WGPUSharedFenceMTLSharedEventDescriptor',
    'WGPUSharedFenceMTLSharedEventExportInfo',
    'WGPUSharedFenceSyncFDDescriptor',
    'WGPUSharedFenceSyncFDExportInfo', 'WGPUSharedFenceType',
    'WGPUSharedFenceType_DXGISharedHandle',
    'WGPUSharedFenceType_EGLSync', 'WGPUSharedFenceType_Force32',
    'WGPUSharedFenceType_MTLSharedEvent',
    'WGPUSharedFenceType_SyncFD',
    'WGPUSharedFenceType_VkSemaphoreOpaqueFD',
    'WGPUSharedFenceType_VkSemaphoreZirconHandle',
    'WGPUSharedFenceVkSemaphoreOpaqueFDDescriptor',
    'WGPUSharedFenceVkSemaphoreOpaqueFDExportInfo',
    'WGPUSharedFenceVkSemaphoreZirconHandleDescriptor',
    'WGPUSharedFenceVkSemaphoreZirconHandleExportInfo',
    'WGPUSharedTextureMemory',
    'WGPUSharedTextureMemoryAHardwareBufferDescriptor',
    'WGPUSharedTextureMemoryAHardwareBufferProperties',
    'WGPUSharedTextureMemoryBeginAccessDescriptor',
    'WGPUSharedTextureMemoryD3D11BeginState',
    'WGPUSharedTextureMemoryD3DSwapchainBeginState',
    'WGPUSharedTextureMemoryDXGISharedHandleDescriptor',
    'WGPUSharedTextureMemoryDescriptor',
    'WGPUSharedTextureMemoryDmaBufDescriptor',
    'WGPUSharedTextureMemoryDmaBufPlane',
    'WGPUSharedTextureMemoryEGLImageDescriptor',
    'WGPUSharedTextureMemoryEndAccessState',
    'WGPUSharedTextureMemoryIOSurfaceDescriptor',
    'WGPUSharedTextureMemoryMetalEndAccessState',
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
    'WGPUStorageTextureAccess_BindingNotUsed',
    'WGPUStorageTextureAccess_Force32',
    'WGPUStorageTextureAccess_ReadOnly',
    'WGPUStorageTextureAccess_ReadWrite',
    'WGPUStorageTextureAccess_Undefined',
    'WGPUStorageTextureAccess_WriteOnly',
    'WGPUStorageTextureBindingLayout', 'WGPUStoreOp',
    'WGPUStoreOp_Discard', 'WGPUStoreOp_Force32', 'WGPUStoreOp_Store',
    'WGPUStoreOp_Undefined', 'WGPUStringView',
    'WGPUSubgroupMatrixComponentType',
    'WGPUSubgroupMatrixComponentType_F16',
    'WGPUSubgroupMatrixComponentType_F32',
    'WGPUSubgroupMatrixComponentType_Force32',
    'WGPUSubgroupMatrixComponentType_I32',
    'WGPUSubgroupMatrixComponentType_I8',
    'WGPUSubgroupMatrixComponentType_U32',
    'WGPUSubgroupMatrixComponentType_U8', 'WGPUSubgroupMatrixConfig',
    'WGPUSupportedFeatures', 'WGPUSupportedInstanceFeatures',
    'WGPUSupportedWGSLLanguageFeatures', 'WGPUSurface',
    'WGPUSurfaceCapabilities', 'WGPUSurfaceColorManagement',
    'WGPUSurfaceConfiguration', 'WGPUSurfaceDescriptor',
    'WGPUSurfaceDescriptorFromWindowsCoreWindow',
    'WGPUSurfaceDescriptorFromWindowsUWPSwapChainPanel',
    'WGPUSurfaceDescriptorFromWindowsWinUISwapChainPanel',
    'WGPUSurfaceGetCurrentTextureStatus',
    'WGPUSurfaceGetCurrentTextureStatus_Error',
    'WGPUSurfaceGetCurrentTextureStatus_Force32',
    'WGPUSurfaceGetCurrentTextureStatus_Lost',
    'WGPUSurfaceGetCurrentTextureStatus_Outdated',
    'WGPUSurfaceGetCurrentTextureStatus_SuccessOptimal',
    'WGPUSurfaceGetCurrentTextureStatus_SuccessSuboptimal',
    'WGPUSurfaceGetCurrentTextureStatus_Timeout',
    'WGPUSurfaceSourceAndroidNativeWindow',
    'WGPUSurfaceSourceMetalLayer', 'WGPUSurfaceSourceWaylandSurface',
    'WGPUSurfaceSourceWindowsHWND', 'WGPUSurfaceSourceXCBWindow',
    'WGPUSurfaceSourceXlibWindow', 'WGPUSurfaceTexture',
    'WGPUTexelBufferAccess', 'WGPUTexelBufferAccess_Force32',
    'WGPUTexelBufferAccess_ReadOnly',
    'WGPUTexelBufferAccess_ReadWrite',
    'WGPUTexelBufferAccess_Undefined', 'WGPUTexelBufferBindingEntry',
    'WGPUTexelBufferBindingLayout', 'WGPUTexelBufferView',
    'WGPUTexelBufferViewDescriptor', 'WGPUTexelCopyBufferInfo',
    'WGPUTexelCopyBufferLayout', 'WGPUTexelCopyTextureInfo',
    'WGPUTexture', 'WGPUTextureAspect', 'WGPUTextureAspect_All',
    'WGPUTextureAspect_DepthOnly', 'WGPUTextureAspect_Force32',
    'WGPUTextureAspect_Plane0Only', 'WGPUTextureAspect_Plane1Only',
    'WGPUTextureAspect_Plane2Only', 'WGPUTextureAspect_StencilOnly',
    'WGPUTextureAspect_Undefined', 'WGPUTextureBindingLayout',
    'WGPUTextureBindingViewDimensionDescriptor',
    'WGPUTextureComponentSwizzle',
    'WGPUTextureComponentSwizzleDescriptor', 'WGPUTextureDescriptor',
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
    'WGPUTextureSampleType_BindingNotUsed',
    'WGPUTextureSampleType_Depth', 'WGPUTextureSampleType_Float',
    'WGPUTextureSampleType_Force32', 'WGPUTextureSampleType_Sint',
    'WGPUTextureSampleType_Uint', 'WGPUTextureSampleType_Undefined',
    'WGPUTextureSampleType_UnfilterableFloat', 'WGPUTextureUsage',
    'WGPUTextureUsage_CopyDst', 'WGPUTextureUsage_CopySrc',
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
    'WGPUTextureViewDimension_Undefined', 'WGPUToneMappingMode',
    'WGPUToneMappingMode_Extended', 'WGPUToneMappingMode_Force32',
    'WGPUToneMappingMode_Standard', 'WGPUUncapturedErrorCallback',
    'WGPUUncapturedErrorCallbackInfo', 'WGPUVertexAttribute',
    'WGPUVertexBufferLayout', 'WGPUVertexFormat',
    'WGPUVertexFormat_Float16', 'WGPUVertexFormat_Float16x2',
    'WGPUVertexFormat_Float16x4', 'WGPUVertexFormat_Float32',
    'WGPUVertexFormat_Float32x2', 'WGPUVertexFormat_Float32x3',
    'WGPUVertexFormat_Float32x4', 'WGPUVertexFormat_Force32',
    'WGPUVertexFormat_Sint16', 'WGPUVertexFormat_Sint16x2',
    'WGPUVertexFormat_Sint16x4', 'WGPUVertexFormat_Sint32',
    'WGPUVertexFormat_Sint32x2', 'WGPUVertexFormat_Sint32x3',
    'WGPUVertexFormat_Sint32x4', 'WGPUVertexFormat_Sint8',
    'WGPUVertexFormat_Sint8x2', 'WGPUVertexFormat_Sint8x4',
    'WGPUVertexFormat_Snorm16', 'WGPUVertexFormat_Snorm16x2',
    'WGPUVertexFormat_Snorm16x4', 'WGPUVertexFormat_Snorm8',
    'WGPUVertexFormat_Snorm8x2', 'WGPUVertexFormat_Snorm8x4',
    'WGPUVertexFormat_Uint16', 'WGPUVertexFormat_Uint16x2',
    'WGPUVertexFormat_Uint16x4', 'WGPUVertexFormat_Uint32',
    'WGPUVertexFormat_Uint32x2', 'WGPUVertexFormat_Uint32x3',
    'WGPUVertexFormat_Uint32x4', 'WGPUVertexFormat_Uint8',
    'WGPUVertexFormat_Uint8x2', 'WGPUVertexFormat_Uint8x4',
    'WGPUVertexFormat_Unorm10_10_10_2', 'WGPUVertexFormat_Unorm16',
    'WGPUVertexFormat_Unorm16x2', 'WGPUVertexFormat_Unorm16x4',
    'WGPUVertexFormat_Unorm8', 'WGPUVertexFormat_Unorm8x2',
    'WGPUVertexFormat_Unorm8x4', 'WGPUVertexFormat_Unorm8x4BGRA',
    'WGPUVertexState', 'WGPUVertexStepMode',
    'WGPUVertexStepMode_Force32', 'WGPUVertexStepMode_Instance',
    'WGPUVertexStepMode_Undefined', 'WGPUVertexStepMode_Vertex',
    'WGPUWGSLLanguageFeatureName',
    'WGPUWGSLLanguageFeatureName_ChromiumPrint',
    'WGPUWGSLLanguageFeatureName_ChromiumTestingExperimental',
    'WGPUWGSLLanguageFeatureName_ChromiumTestingShipped',
    'WGPUWGSLLanguageFeatureName_ChromiumTestingShippedWithKillswitch',
    'WGPUWGSLLanguageFeatureName_ChromiumTestingUnimplemented',
    'WGPUWGSLLanguageFeatureName_ChromiumTestingUnsafeExperimental',
    'WGPUWGSLLanguageFeatureName_Force32',
    'WGPUWGSLLanguageFeatureName_FragmentDepth',
    'WGPUWGSLLanguageFeatureName_ImmediateAddressSpace',
    'WGPUWGSLLanguageFeatureName_Packed4x8IntegerDotProduct',
    'WGPUWGSLLanguageFeatureName_PointerCompositeAccess',
    'WGPUWGSLLanguageFeatureName_ReadonlyAndReadwriteStorageTextures',
    'WGPUWGSLLanguageFeatureName_SizedBindingArray',
    'WGPUWGSLLanguageFeatureName_SubgroupId',
    'WGPUWGSLLanguageFeatureName_SubgroupUniformity',
    'WGPUWGSLLanguageFeatureName_TexelBuffers',
    'WGPUWGSLLanguageFeatureName_UniformBufferStandardLayout',
    'WGPUWGSLLanguageFeatureName_UnrestrictedPointerParameters',
    'WGPUWaitStatus', 'WGPUWaitStatus_Error',
    'WGPUWaitStatus_Force32', 'WGPUWaitStatus_Success',
    'WGPUWaitStatus_TimedOut', 'WGPUYCbCrVkDescriptor',
    'emscripten_webgpu_get_device', 'int32_t', 'size_t',
    'struct_WGPUAHardwareBufferProperties', 'struct_WGPUAdapterImpl',
    'struct_WGPUAdapterInfo', 'struct_WGPUAdapterPropertiesD3D',
    'struct_WGPUAdapterPropertiesMemoryHeaps',
    'struct_WGPUAdapterPropertiesSubgroupMatrixConfigs',
    'struct_WGPUAdapterPropertiesVk',
    'struct_WGPUAdapterPropertiesWGPU',
    'struct_WGPUBindGroupDescriptor',
    'struct_WGPUBindGroupDynamicBindingArray',
    'struct_WGPUBindGroupEntry', 'struct_WGPUBindGroupEntryContents',
    'struct_WGPUBindGroupImpl',
    'struct_WGPUBindGroupLayoutDescriptor',
    'struct_WGPUBindGroupLayoutDynamicBindingArray',
    'struct_WGPUBindGroupLayoutEntry',
    'struct_WGPUBindGroupLayoutImpl', 'struct_WGPUBlendComponent',
    'struct_WGPUBlendState', 'struct_WGPUBufferBindingLayout',
    'struct_WGPUBufferDescriptor',
    'struct_WGPUBufferHostMappedPointer', 'struct_WGPUBufferImpl',
    'struct_WGPUBufferMapCallbackInfo', 'struct_WGPUChainedStruct',
    'struct_WGPUColor', 'struct_WGPUColorTargetState',
    'struct_WGPUColorTargetStateExpandResolveTextureDawn',
    'struct_WGPUCommandBufferDescriptor',
    'struct_WGPUCommandBufferImpl',
    'struct_WGPUCommandEncoderDescriptor',
    'struct_WGPUCommandEncoderImpl',
    'struct_WGPUCompatibilityModeLimits',
    'struct_WGPUCompilationInfo',
    'struct_WGPUCompilationInfoCallbackInfo',
    'struct_WGPUCompilationMessage',
    'struct_WGPUComputePassDescriptor',
    'struct_WGPUComputePassEncoderImpl',
    'struct_WGPUComputePipelineDescriptor',
    'struct_WGPUComputePipelineImpl', 'struct_WGPUComputeState',
    'struct_WGPUConstantEntry',
    'struct_WGPUCopyTextureForBrowserOptions',
    'struct_WGPUCreateComputePipelineAsyncCallbackInfo',
    'struct_WGPUCreateRenderPipelineAsyncCallbackInfo',
    'struct_WGPUDawnAdapterPropertiesPowerPreference',
    'struct_WGPUDawnBufferDescriptorErrorInfoFromWireClient',
    'struct_WGPUDawnCacheDeviceDescriptor',
    'struct_WGPUDawnCompilationMessageUtf16',
    'struct_WGPUDawnConsumeAdapterDescriptor',
    'struct_WGPUDawnDeviceAllocatorControl',
    'struct_WGPUDawnDrmFormatCapabilities',
    'struct_WGPUDawnDrmFormatProperties',
    'struct_WGPUDawnEncoderInternalUsageDescriptor',
    'struct_WGPUDawnFakeBufferOOMForTesting',
    'struct_WGPUDawnFakeDeviceInitializeErrorForTesting',
    'struct_WGPUDawnFormatCapabilities',
    'struct_WGPUDawnHostMappedPointerLimits',
    'struct_WGPUDawnInjectedInvalidSType',
    'struct_WGPUDawnRenderPassColorAttachmentRenderToSingleSampled',
    'struct_WGPUDawnShaderModuleSPIRVOptionsDescriptor',
    'struct_WGPUDawnTexelCopyBufferRowAlignmentLimits',
    'struct_WGPUDawnTextureInternalUsageDescriptor',
    'struct_WGPUDawnTogglesDescriptor',
    'struct_WGPUDawnWGSLBlocklist', 'struct_WGPUDawnWireWGSLControl',
    'struct_WGPUDepthStencilState', 'struct_WGPUDeviceDescriptor',
    'struct_WGPUDeviceImpl', 'struct_WGPUDeviceLostCallbackInfo',
    'struct_WGPUDynamicBindingArrayLayout',
    'struct_WGPUDynamicBindingArrayLimits',
    'struct_WGPUEmscriptenSurfaceSourceCanvasHTMLSelector',
    'struct_WGPUExtent2D', 'struct_WGPUExtent3D',
    'struct_WGPUExternalTextureBindingEntry',
    'struct_WGPUExternalTextureBindingLayout',
    'struct_WGPUExternalTextureDescriptor',
    'struct_WGPUExternalTextureImpl', 'struct_WGPUFragmentState',
    'struct_WGPUFuture', 'struct_WGPUFutureWaitInfo',
    'struct_WGPUINTERNAL_HAVE_EMDAWNWEBGPU_HEADER',
    'struct_WGPUImageCopyExternalTexture',
    'struct_WGPUInstanceDescriptor', 'struct_WGPUInstanceImpl',
    'struct_WGPUInstanceLimits', 'struct_WGPULimits',
    'struct_WGPULoggingCallbackInfo', 'struct_WGPUMemoryHeapInfo',
    'struct_WGPUMultisampleState', 'struct_WGPUOrigin2D',
    'struct_WGPUOrigin3D', 'struct_WGPUPassTimestampWrites',
    'struct_WGPUPipelineLayoutDescriptor',
    'struct_WGPUPipelineLayoutImpl',
    'struct_WGPUPipelineLayoutPixelLocalStorage',
    'struct_WGPUPipelineLayoutResourceTable',
    'struct_WGPUPipelineLayoutStorageAttachment',
    'struct_WGPUPopErrorScopeCallbackInfo',
    'struct_WGPUPrimitiveState', 'struct_WGPUQuerySetDescriptor',
    'struct_WGPUQuerySetImpl', 'struct_WGPUQueueDescriptor',
    'struct_WGPUQueueImpl', 'struct_WGPUQueueWorkDoneCallbackInfo',
    'struct_WGPURenderBundleDescriptor',
    'struct_WGPURenderBundleEncoderDescriptor',
    'struct_WGPURenderBundleEncoderImpl',
    'struct_WGPURenderBundleImpl',
    'struct_WGPURenderPassColorAttachment',
    'struct_WGPURenderPassDepthStencilAttachment',
    'struct_WGPURenderPassDescriptor',
    'struct_WGPURenderPassDescriptorExpandResolveRect',
    'struct_WGPURenderPassDescriptorResolveRect',
    'struct_WGPURenderPassEncoderImpl',
    'struct_WGPURenderPassMaxDrawCount',
    'struct_WGPURenderPassPixelLocalStorage',
    'struct_WGPURenderPassStorageAttachment',
    'struct_WGPURenderPipelineDescriptor',
    'struct_WGPURenderPipelineImpl',
    'struct_WGPURequestAdapterCallbackInfo',
    'struct_WGPURequestAdapterOptions',
    'struct_WGPURequestAdapterWebGPUBackendOptions',
    'struct_WGPURequestAdapterWebXROptions',
    'struct_WGPURequestDeviceCallbackInfo',
    'struct_WGPUResourceTableDescriptor',
    'struct_WGPUResourceTableImpl', 'struct_WGPUResourceTableLimits',
    'struct_WGPUSamplerBindingLayout', 'struct_WGPUSamplerDescriptor',
    'struct_WGPUSamplerImpl',
    'struct_WGPUShaderModuleCompilationOptions',
    'struct_WGPUShaderModuleDescriptor',
    'struct_WGPUShaderModuleImpl', 'struct_WGPUShaderSourceSPIRV',
    'struct_WGPUShaderSourceWGSL',
    'struct_WGPUSharedBufferMemoryBeginAccessDescriptor',
    'struct_WGPUSharedBufferMemoryDescriptor',
    'struct_WGPUSharedBufferMemoryEndAccessState',
    'struct_WGPUSharedBufferMemoryImpl',
    'struct_WGPUSharedBufferMemoryProperties',
    'struct_WGPUSharedFenceDXGISharedHandleDescriptor',
    'struct_WGPUSharedFenceDXGISharedHandleExportInfo',
    'struct_WGPUSharedFenceDescriptor',
    'struct_WGPUSharedFenceEGLSyncDescriptor',
    'struct_WGPUSharedFenceEGLSyncExportInfo',
    'struct_WGPUSharedFenceExportInfo', 'struct_WGPUSharedFenceImpl',
    'struct_WGPUSharedFenceMTLSharedEventDescriptor',
    'struct_WGPUSharedFenceMTLSharedEventExportInfo',
    'struct_WGPUSharedFenceSyncFDDescriptor',
    'struct_WGPUSharedFenceSyncFDExportInfo',
    'struct_WGPUSharedFenceVkSemaphoreOpaqueFDDescriptor',
    'struct_WGPUSharedFenceVkSemaphoreOpaqueFDExportInfo',
    'struct_WGPUSharedFenceVkSemaphoreZirconHandleDescriptor',
    'struct_WGPUSharedFenceVkSemaphoreZirconHandleExportInfo',
    'struct_WGPUSharedTextureMemoryAHardwareBufferDescriptor',
    'struct_WGPUSharedTextureMemoryAHardwareBufferProperties',
    'struct_WGPUSharedTextureMemoryBeginAccessDescriptor',
    'struct_WGPUSharedTextureMemoryD3D11BeginState',
    'struct_WGPUSharedTextureMemoryD3DSwapchainBeginState',
    'struct_WGPUSharedTextureMemoryDXGISharedHandleDescriptor',
    'struct_WGPUSharedTextureMemoryDescriptor',
    'struct_WGPUSharedTextureMemoryDmaBufDescriptor',
    'struct_WGPUSharedTextureMemoryDmaBufPlane',
    'struct_WGPUSharedTextureMemoryEGLImageDescriptor',
    'struct_WGPUSharedTextureMemoryEndAccessState',
    'struct_WGPUSharedTextureMemoryIOSurfaceDescriptor',
    'struct_WGPUSharedTextureMemoryImpl',
    'struct_WGPUSharedTextureMemoryMetalEndAccessState',
    'struct_WGPUSharedTextureMemoryOpaqueFDDescriptor',
    'struct_WGPUSharedTextureMemoryProperties',
    'struct_WGPUSharedTextureMemoryVkDedicatedAllocationDescriptor',
    'struct_WGPUSharedTextureMemoryVkImageLayoutBeginState',
    'struct_WGPUSharedTextureMemoryVkImageLayoutEndState',
    'struct_WGPUSharedTextureMemoryZirconHandleDescriptor',
    'struct_WGPUStaticSamplerBindingLayout',
    'struct_WGPUStencilFaceState',
    'struct_WGPUStorageTextureBindingLayout', 'struct_WGPUStringView',
    'struct_WGPUSubgroupMatrixConfig', 'struct_WGPUSupportedFeatures',
    'struct_WGPUSupportedInstanceFeatures',
    'struct_WGPUSupportedWGSLLanguageFeatures',
    'struct_WGPUSurfaceCapabilities',
    'struct_WGPUSurfaceColorManagement',
    'struct_WGPUSurfaceConfiguration', 'struct_WGPUSurfaceDescriptor',
    'struct_WGPUSurfaceDescriptorFromWindowsCoreWindow',
    'struct_WGPUSurfaceDescriptorFromWindowsUWPSwapChainPanel',
    'struct_WGPUSurfaceDescriptorFromWindowsWinUISwapChainPanel',
    'struct_WGPUSurfaceImpl',
    'struct_WGPUSurfaceSourceAndroidNativeWindow',
    'struct_WGPUSurfaceSourceMetalLayer',
    'struct_WGPUSurfaceSourceWaylandSurface',
    'struct_WGPUSurfaceSourceWindowsHWND',
    'struct_WGPUSurfaceSourceXCBWindow',
    'struct_WGPUSurfaceSourceXlibWindow', 'struct_WGPUSurfaceTexture',
    'struct_WGPUTexelBufferBindingEntry',
    'struct_WGPUTexelBufferBindingLayout',
    'struct_WGPUTexelBufferViewDescriptor',
    'struct_WGPUTexelBufferViewImpl',
    'struct_WGPUTexelCopyBufferInfo',
    'struct_WGPUTexelCopyBufferLayout',
    'struct_WGPUTexelCopyTextureInfo',
    'struct_WGPUTextureBindingLayout',
    'struct_WGPUTextureBindingViewDimensionDescriptor',
    'struct_WGPUTextureComponentSwizzle',
    'struct_WGPUTextureComponentSwizzleDescriptor',
    'struct_WGPUTextureDescriptor', 'struct_WGPUTextureImpl',
    'struct_WGPUTextureViewDescriptor', 'struct_WGPUTextureViewImpl',
    'struct_WGPUUncapturedErrorCallbackInfo',
    'struct_WGPUVertexAttribute', 'struct_WGPUVertexBufferLayout',
    'struct_WGPUVertexState', 'struct_WGPUYCbCrVkDescriptor',
    'uint32_t', 'uint64_t', 'wgpuAdapterAddRef',
    'wgpuAdapterCreateDevice', 'wgpuAdapterGetFeatures',
    'wgpuAdapterGetFormatCapabilities', 'wgpuAdapterGetInfo',
    'wgpuAdapterGetInstance', 'wgpuAdapterGetLimits',
    'wgpuAdapterHasFeature', 'wgpuAdapterInfoFreeMembers',
    'wgpuAdapterPropertiesMemoryHeapsFreeMembers',
    'wgpuAdapterPropertiesSubgroupMatrixConfigsFreeMembers',
    'wgpuAdapterRelease', 'wgpuAdapterRequestDevice',
    'wgpuBindGroupAddRef', 'wgpuBindGroupDestroy',
    'wgpuBindGroupInsertBinding', 'wgpuBindGroupLayoutAddRef',
    'wgpuBindGroupLayoutRelease', 'wgpuBindGroupLayoutSetLabel',
    'wgpuBindGroupRelease', 'wgpuBindGroupRemoveBinding',
    'wgpuBindGroupSetLabel', 'wgpuBindGroupUpdate',
    'wgpuBufferAddRef', 'wgpuBufferCreateTexelView',
    'wgpuBufferDestroy', 'wgpuBufferGetConstMappedRange',
    'wgpuBufferGetMapState', 'wgpuBufferGetMappedRange',
    'wgpuBufferGetSize', 'wgpuBufferGetUsage', 'wgpuBufferMapAsync',
    'wgpuBufferReadMappedRange', 'wgpuBufferRelease',
    'wgpuBufferSetLabel', 'wgpuBufferUnmap',
    'wgpuBufferWriteMappedRange', 'wgpuCommandBufferAddRef',
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
    'wgpuCommandEncoderSetResourceTable',
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
    'wgpuComputePassEncoderSetImmediates',
    'wgpuComputePassEncoderSetLabel',
    'wgpuComputePassEncoderSetPipeline',
    'wgpuComputePassEncoderWriteTimestamp',
    'wgpuComputePipelineAddRef',
    'wgpuComputePipelineGetBindGroupLayout',
    'wgpuComputePipelineRelease', 'wgpuComputePipelineSetLabel',
    'wgpuCreateInstance', 'wgpuDawnDrmFormatCapabilitiesFreeMembers',
    'wgpuDeviceAddRef', 'wgpuDeviceCreateBindGroup',
    'wgpuDeviceCreateBindGroupLayout', 'wgpuDeviceCreateBuffer',
    'wgpuDeviceCreateCommandEncoder',
    'wgpuDeviceCreateComputePipeline',
    'wgpuDeviceCreateComputePipelineAsync',
    'wgpuDeviceCreateErrorBuffer',
    'wgpuDeviceCreateErrorExternalTexture',
    'wgpuDeviceCreateErrorShaderModule',
    'wgpuDeviceCreateErrorTexture', 'wgpuDeviceCreateExternalTexture',
    'wgpuDeviceCreatePipelineLayout', 'wgpuDeviceCreateQuerySet',
    'wgpuDeviceCreateRenderBundleEncoder',
    'wgpuDeviceCreateRenderPipeline',
    'wgpuDeviceCreateRenderPipelineAsync',
    'wgpuDeviceCreateResourceTable', 'wgpuDeviceCreateSampler',
    'wgpuDeviceCreateShaderModule', 'wgpuDeviceCreateTexture',
    'wgpuDeviceDestroy', 'wgpuDeviceForceLoss',
    'wgpuDeviceGetAHardwareBufferProperties', 'wgpuDeviceGetAdapter',
    'wgpuDeviceGetAdapterInfo', 'wgpuDeviceGetFeatures',
    'wgpuDeviceGetLimits', 'wgpuDeviceGetLostFuture',
    'wgpuDeviceGetQueue', 'wgpuDeviceHasFeature',
    'wgpuDeviceImportSharedBufferMemory',
    'wgpuDeviceImportSharedFence',
    'wgpuDeviceImportSharedTextureMemory', 'wgpuDeviceInjectError',
    'wgpuDevicePopErrorScope', 'wgpuDevicePushErrorScope',
    'wgpuDeviceRelease', 'wgpuDeviceSetLabel',
    'wgpuDeviceSetLoggingCallback', 'wgpuDeviceTick',
    'wgpuDeviceValidateTextureDescriptor',
    'wgpuExternalTextureAddRef', 'wgpuExternalTextureDestroy',
    'wgpuExternalTextureExpire', 'wgpuExternalTextureRefresh',
    'wgpuExternalTextureRelease', 'wgpuExternalTextureSetLabel',
    'wgpuGetInstanceFeatures', 'wgpuGetInstanceLimits',
    'wgpuGetProcAddress', 'wgpuHasInstanceFeature',
    'wgpuInstanceAddRef', 'wgpuInstanceCreateSurface',
    'wgpuInstanceGetWGSLLanguageFeatures',
    'wgpuInstanceHasWGSLLanguageFeature', 'wgpuInstanceProcessEvents',
    'wgpuInstanceRelease', 'wgpuInstanceRequestAdapter',
    'wgpuInstanceWaitAny', 'wgpuPipelineLayoutAddRef',
    'wgpuPipelineLayoutRelease', 'wgpuPipelineLayoutSetLabel',
    'wgpuQuerySetAddRef', 'wgpuQuerySetDestroy',
    'wgpuQuerySetGetCount', 'wgpuQuerySetGetType',
    'wgpuQuerySetRelease', 'wgpuQuerySetSetLabel', 'wgpuQueueAddRef',
    'wgpuQueueCopyExternalTextureForBrowser',
    'wgpuQueueCopyTextureForBrowser', 'wgpuQueueOnSubmittedWorkDone',
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
    'wgpuRenderBundleEncoderSetImmediates',
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
    'wgpuRenderPassEncoderMultiDrawIndexedIndirect',
    'wgpuRenderPassEncoderMultiDrawIndirect',
    'wgpuRenderPassEncoderPixelLocalStorageBarrier',
    'wgpuRenderPassEncoderPopDebugGroup',
    'wgpuRenderPassEncoderPushDebugGroup',
    'wgpuRenderPassEncoderRelease',
    'wgpuRenderPassEncoderSetBindGroup',
    'wgpuRenderPassEncoderSetBlendConstant',
    'wgpuRenderPassEncoderSetImmediates',
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
    'wgpuResourceTableAddRef', 'wgpuResourceTableDestroy',
    'wgpuResourceTableRelease', 'wgpuSamplerAddRef',
    'wgpuSamplerRelease', 'wgpuSamplerSetLabel',
    'wgpuShaderModuleAddRef', 'wgpuShaderModuleGetCompilationInfo',
    'wgpuShaderModuleRelease', 'wgpuShaderModuleSetLabel',
    'wgpuSharedBufferMemoryAddRef',
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
    'wgpuSharedTextureMemorySetLabel',
    'wgpuSupportedFeaturesFreeMembers',
    'wgpuSupportedInstanceFeaturesFreeMembers',
    'wgpuSupportedWGSLLanguageFeaturesFreeMembers',
    'wgpuSurfaceAddRef', 'wgpuSurfaceCapabilitiesFreeMembers',
    'wgpuSurfaceConfigure', 'wgpuSurfaceGetCapabilities',
    'wgpuSurfaceGetCurrentTexture', 'wgpuSurfacePresent',
    'wgpuSurfaceRelease', 'wgpuSurfaceSetLabel',
    'wgpuSurfaceUnconfigure', 'wgpuTexelBufferViewAddRef',
    'wgpuTexelBufferViewRelease', 'wgpuTexelBufferViewSetLabel',
    'wgpuTextureAddRef', 'wgpuTextureCreateErrorView',
    'wgpuTextureCreateView', 'wgpuTextureDestroy',
    'wgpuTextureGetDepthOrArrayLayers', 'wgpuTextureGetDimension',
    'wgpuTextureGetFormat', 'wgpuTextureGetHeight',
    'wgpuTextureGetMipLevelCount', 'wgpuTextureGetSampleCount',
    'wgpuTextureGetUsage', 'wgpuTextureGetWidth', 'wgpuTexturePin',
    'wgpuTextureRelease', 'wgpuTextureSetLabel', 'wgpuTextureUnpin',
    'wgpuTextureViewAddRef', 'wgpuTextureViewRelease',
    'wgpuTextureViewSetLabel']
