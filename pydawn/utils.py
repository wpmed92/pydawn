from pydawn import webgpu
import ctypes
import os
import sys

class ResultContainer:
    def __init__(self):
        self.msg = None
        self.status = None
        self.value = None

instDesc = webgpu.WGPUInstanceDescriptor()
instDesc.features.timedWaitAnyEnable = True
instance = webgpu.wgpuCreateInstance(instDesc)
supported_backends = { "Metal": webgpu.WGPUBackendType_Metal, "Vulkan": webgpu.WGPUBackendType_Vulkan,
"DirectX11": webgpu.WGPUBackendType_D3D11,  "DirectX12": webgpu.WGPUBackendType_D3D12 }

def to_c_string(str):
    return ctypes.create_string_buffer(str.encode('utf-8'))

def from_wgpu_str(string_view):
    return ctypes.string_at(string_view.data, string_view.length).decode("utf-8")

def to_wgpu_str(str):
    buffer = to_c_string(str)
    view = webgpu.WGPUStringView()
    view.data = ctypes.cast(ctypes.pointer(buffer), ctypes.POINTER(ctypes.c_char))
    view.length = len(str)
    return view

def wait(future):
    info = webgpu.WGPUFutureWaitInfo()
    info.future = future
    status = webgpu.wgpuInstanceWaitAny(instance, 1, info, 2**64 - 1)
    assert status == webgpu.WGPUWaitStatus_Success, "Future failed"

def request_adapter_sync(power_preference):
    cb_info = webgpu.WGPURequestAdapterCallbackInfo()
    cb_info.nextInChain = None
    cb_info.mode = webgpu.WGPUCallbackMode_WaitAnyOnly
    result = ResultContainer()

    def cb(status, adapter, msg, _):
        result.status = status
        result.value = adapter
        result.msg = from_wgpu_str(msg)

    cb_info.callback = webgpu.WGPURequestAdapterCallback(cb)
    adapterOptions = webgpu.WGPURequestAdapterOptions()
    adapterOptions.powerPreference = power_preference

    force_backend = os.getenv("BACKEND_TYPE", "").strip()

    if force_backend:
        if force_backend not in supported_backends:
            raise RuntimeError(f"Unsupported backend: {force_backend}")
        adapterOptions.backendType = supported_backends[force_backend]

    wait(webgpu.wgpuInstanceRequestAdapterF(instance, adapterOptions, cb_info))

    if result.status != webgpu.WGPURequestAdapterStatus_Success:
        raise RuntimeError(f"Error requesting adapter: [{webgpu.WGPURequestAdapterStatus__enumvalues[result.status]}] {result.msg}")

    return result.value

def request_device_sync(adapter, required_features = []):
    assert adapter is not None, "adapter should not be none"
    device_desc = webgpu.WGPUDeviceDescriptor()

    toggles = [b"allow_unsafe_apis"]
    if sys.platform == "win32":
        # NOTE(irwin): this obscure toggle instructs d3d12 implementation of webgpu in dawn to
        # use dxc instead of fxc. fxc doesn't support fp16, while dxc does - depending on
        # hardware support. @ShadersF16_On_Windows
        toggles.append(b"use_dxc")

    string_buffers = [ctypes.create_string_buffer(t) for t in toggles]
    string_buffer_pointers = [ctypes.cast(sb, ctypes.POINTER(ctypes.c_char)) for sb in string_buffers]

    toggles_count = len(toggles)

    # Create array of char* (pointer-to-char) with toggles_count elements
    enabled_toggles_array = (ctypes.POINTER(ctypes.c_char) * toggles_count)(*string_buffer_pointers)

    # Disable "timestamp_quantization" for nanosecond precision: https://developer.chrome.com/blog/new-in-webgpu-120
    toggle_desc = webgpu.WGPUDawnTogglesDescriptor()
    toggle_desc.chain.sType = webgpu.WGPUSType_DawnTogglesDescriptor
    toggle_desc.enabledToggleCount = toggles_count
    toggle_desc.enabledToggles = enabled_toggles_array
    toggle_desc.disabledToggleCount = 1
    ts_quant = ctypes.cast(ctypes.pointer(to_c_string("timestamp_quantization")), ctypes.POINTER(ctypes.c_char))
    toggle_desc.disabledToggles = ctypes.pointer(ts_quant)
    device_desc.nextInChain = ctypes.cast(ctypes.pointer(toggle_desc), ctypes.POINTER(webgpu.struct_WGPUChainedStruct))

    # Populate required features
    feature_array_type = webgpu.WGPUFeatureName * len(required_features)
    feature_array = feature_array_type(*required_features)
    device_desc.requiredFeatureCount = len(required_features)
    device_desc.requiredFeatures = ctypes.cast(feature_array, ctypes.POINTER(webgpu.WGPUFeatureName))

    # Limits
    supported_limits = webgpu.WGPUSupportedLimits()
    webgpu.wgpuAdapterGetLimits(adapter, ctypes.cast(ctypes.pointer(supported_limits),ctypes.POINTER(webgpu.struct_WGPUSupportedLimits)))
    limits = webgpu.WGPURequiredLimits()
    limits.limits = supported_limits.limits
    device_desc.requiredLimits = ctypes.cast(ctypes.pointer(limits),ctypes.POINTER(webgpu.struct_WGPURequiredLimits))

    # Request device
    cb_info = webgpu.WGPURequestDeviceCallbackInfo()
    cb_info.nextInChain = None
    cb_info.mode = webgpu.WGPUCallbackMode_WaitAnyOnly
    result = ResultContainer()

    def cb(status, device_impl, msg, _):
        result.status = status
        result.value = device_impl
        result.msg = from_wgpu_str(msg)

    cb_info.callback = webgpu.WGPURequestDeviceCallback(cb)
    wait(webgpu.wgpuAdapterRequestDeviceF(adapter, device_desc, cb_info))

    if result.status != webgpu.WGPURequestDeviceStatus_Success:
        raise RuntimeError(f"Failed to request device: [{webgpu.WGPURequestDeviceStatus__enumvalues[result.status]}] {result.msg}")

    return result.value

def create_buffer(device, size, usage):
    buffer_desc = webgpu.WGPUBufferDescriptor()
    buffer_desc.size = size
    buffer_desc.usage = usage
    buffer_desc.mappedAtCreation = False
    return webgpu.wgpuDeviceCreateBuffer(device, buffer_desc)

def write_buffer(device, buf, offset, src):
    src = bytearray(src)
    src_pointer = (ctypes.c_uint8 * len(src)).from_buffer(src)
    webgpu.wgpuQueueWriteBuffer(webgpu.wgpuDeviceGetQueue(device), buf, offset, src_pointer, len(src))

def map_buffer(buf, size):
    cb_info = webgpu.WGPUBufferMapCallbackInfo2()
    cb_info.nextInChain = None
    cb_info.mode = webgpu.WGPUCallbackMode_WaitAnyOnly
    result = ResultContainer()

    def cb(status, msg, u1, u2):
        result.status = status
        result.msg = from_wgpu_str(msg)

    cb_info.callback = webgpu.WGPUBufferMapCallback2(cb)
    wait(webgpu.wgpuBufferMapAsync2(buf, webgpu.WGPUMapMode_Read, 0, size, cb_info))

    if result.status != webgpu.WGPUBufferMapAsyncStatus_Success:
        raise RuntimeError(f"Failed to map buffer: [{webgpu.WGPUBufferMapAsyncStatus__enumvalues[result.status]}] {result.msg}")

def copy_buffer_to_buffer(device, src, src_offset, dst, dst_offset, size):
    encoder = create_command_encoder(device)
    webgpu.wgpuCommandEncoderCopyBufferToBuffer(encoder, src, src_offset, dst, dst_offset, size)
    cb = command_encoder_finish(encoder)
    submit(device, [cb])
    webgpu.wgpuCommandBufferRelease(cb)
    webgpu.wgpuCommandEncoderRelease(encoder)

def read_buffer(dev, buf):
    size = webgpu.wgpuBufferGetSize(buf)
    tmp_usage = webgpu.WGPUBufferUsage_CopyDst | webgpu.WGPUBufferUsage_MapRead
    tmp_buffer = create_buffer(dev, size, tmp_usage)
    copy_buffer_to_buffer(dev, buf, 0, tmp_buffer, 0, size)
    sync(dev)
    map_buffer(tmp_buffer, size)
    ptr = webgpu.wgpuBufferGetConstMappedRange(tmp_buffer, 0, size)
    void_ptr = ctypes.cast(ptr, ctypes.c_void_p)
    byte_array = (ctypes.c_uint8 * size).from_address(void_ptr.value)
    result = bytearray(byte_array)
    webgpu.wgpuBufferUnmap(tmp_buffer)
    webgpu.wgpuBufferDestroy(tmp_buffer)
    return memoryview(result).cast("B")

def create_shader_module(device, source):
    shader = webgpu.WGPUShaderModuleWGSLDescriptor()
    shader.code = to_wgpu_str(source)
    shader.chain.next = None
    shader.chain.sType = webgpu.WGPUSType_ShaderSourceWGSL
    module = webgpu.WGPUShaderModuleDescriptor()
    module.nextInChain = ctypes.cast(ctypes.pointer(shader), ctypes.POINTER(webgpu.struct_WGPUChainedStruct))

    # Check compiler error
    webgpu.wgpuDevicePushErrorScope(device, webgpu.WGPUErrorFilter_Validation)
    shader_module = webgpu.wgpuDeviceCreateShaderModule(device, module)
    compiler_error = pop_error(device)

    if compiler_error:
        raise RuntimeError(f"Shader compilation failed: {compiler_error}")

    return shader_module

def create_bind_group_layout(device, entries, validate=True):
    webgpuEntries = []

    for entry in entries:
        webgpuEntry = webgpu.WGPUBindGroupLayoutEntry()
        webgpuEntry.binding = entry["binding"]
        webgpuEntry.visibility = entry["visibility"]
        bufferBindingLayout = webgpu.WGPUBufferBindingLayout()
        bufferBindingLayout.type = entry["buffer"]["type"]
        webgpuEntry.buffer = bufferBindingLayout
        webgpuEntries.append(webgpuEntry)

    entries_array_type = webgpu.WGPUBindGroupLayoutEntry * len(webgpuEntries)
    entries_array = entries_array_type(*webgpuEntries)

    desc = webgpu.WGPUBindGroupLayoutDescriptor()
    desc.entryCount = len(webgpuEntries)
    desc.entries = ctypes.cast(entries_array, ctypes.POINTER(webgpu.WGPUBindGroupLayoutEntry))

    webgpu.wgpuDevicePushErrorScope(device, webgpu.WGPUErrorFilter_Validation)
    ret = webgpu.wgpuDeviceCreateBindGroupLayout(device, desc)
    layout_error = pop_error(device)

    if layout_error and validate:
        raise RuntimeError(f"Error creating bind group layout: {layout_error}")

    return ret

def create_pipeline_layout(device, bind_group_layouts, validate=True):
    pipeline_layout_desc = webgpu.WGPUPipelineLayoutDescriptor()
    pipeline_layout_desc.bindGroupLayoutCount = len(bind_group_layouts)
    bind_group_array_type = webgpu.WGPUBindGroupLayout * len(bind_group_layouts)
    bind_groups_ctype = bind_group_array_type(*bind_group_layouts)
    pipeline_layout_desc.bindGroupLayouts = bind_groups_ctype

    webgpu.wgpuDevicePushErrorScope(device, webgpu.WGPUErrorFilter_Validation)
    ret = webgpu.wgpuDeviceCreatePipelineLayout(device, pipeline_layout_desc)
    layout_error = pop_error(device)

    if layout_error and validate:
        raise RuntimeError(f"Error creating pipeline layout: {layout_error}")

    return ret

def create_bind_group(device, layout, entries, validate=True):
    bind_group_desc = webgpu.WGPUBindGroupDescriptor()
    bind_group_desc.layout = layout
    bind_group_desc.entryCount = len(entries)
    webgpu_entries = []

    for entry in entries:
        webgpuEntry = webgpu.WGPUBindGroupEntry()
        webgpuEntry.binding = entry["binding"]
        webgpuEntry.buffer = entry["resource"]["buffer"]
        webgpuEntry.offset = entry["resource"]["offset"]
        webgpuEntry.size = entry["resource"]["size"]
        webgpu_entries.append(webgpuEntry)

    entries_array_type = webgpu.WGPUBindGroupEntry * len(webgpu_entries)
    entries_array = entries_array_type(*webgpu_entries)
    bind_group_desc.entries = entries_array

    webgpu.wgpuDevicePushErrorScope(device, webgpu.WGPUErrorFilter_Validation)
    ret = webgpu.wgpuDeviceCreateBindGroup(device, bind_group_desc)
    bind_group_error = pop_error(device)

    if bind_group_error and validate:
        raise RuntimeError(f"Error creating bind group: {bind_group_error}")

    return ret

def create_compute_pipeline(device, layout, compute):
    compute_desc = webgpu.WGPUComputePipelineDescriptor()
    compute_desc.layout = layout
    dawn_compute = webgpu.WGPUComputeState()
    dawn_compute.module = compute["module"]
    dawn_compute.entryPoint = to_wgpu_str(compute["entry_point"])
    compute_desc.compute = dawn_compute

    cb_info = webgpu.WGPUCreateComputePipelineAsyncCallbackInfo2()
    cb_info.nextInChain = None
    cb_info.mode = webgpu.WGPUCallbackMode_WaitAnyOnly
    result = ResultContainer()

    def cb(status, compute_pipeline_impl, msg, u1, u2):
        result.status = status
        result.msg = from_wgpu_str(msg)
        result.value = compute_pipeline_impl

    cb_info.callback = webgpu.WGPUCreateComputePipelineAsyncCallback2(cb)

    webgpu.wgpuDevicePushErrorScope(device, webgpu.WGPUErrorFilter_Validation)
    wait(webgpu.wgpuDeviceCreateComputePipelineAsync2(device, compute_desc, cb_info))
    maybe_error = pop_error(device)

    if result.status != webgpu.WGPUCreatePipelineAsyncStatus_Success:
        raise RuntimeError(f"Error creating pipeline: [{webgpu.WGPUCreatePipelineAsyncStatus__enumvalues[result.status]}] {result.msg}, {maybe_error}")

    return result.value

def create_command_encoder(device):
    encoder_desc = webgpu.WGPUCommandEncoderDescriptor()
    command_encoder = webgpu.wgpuDeviceCreateCommandEncoder(device, encoder_desc)
    return command_encoder

def create_query_set(device, type, count):
    desc = webgpu.WGPUQuerySetDescriptor()
    desc.type = type
    desc.count = count
    return webgpu.wgpuDeviceCreateQuerySet(device, desc)

def resolve_query_set(command_encoder, query_set, first_query, query_count, destination, destination_offset):
    webgpu.wgpuCommandEncoderResolveQuerySet(command_encoder, query_set, first_query, query_count, destination, destination_offset)

def supported_features(adapter):
    supported_features = webgpu.WGPUSupportedFeatures()
    webgpu.wgpuAdapterGetFeatures(adapter, supported_features)
    features = []

    for i in range(supported_features.featureCount):
        features.append(webgpu.WGPUFeatureName__enumvalues[supported_features.features[i]])

    return features

def begin_compute_pass(command_encoder, writes = None):
    desc = webgpu.WGPUComputePassDescriptor()
    desc.nextInChain = None
    if writes is not None:
        timestamp_writes = webgpu.WGPUComputePassTimestampWrites()
        timestamp_writes.querySet = writes["query_set"]
        timestamp_writes.beginningOfPassWriteIndex = writes["beginning_of_pass_write_index"]
        timestamp_writes.endOfPassWriteIndex = writes["end_of_pass_write_index"]
        desc.timestampWrites = ctypes.pointer(timestamp_writes)
    return webgpu.wgpuCommandEncoderBeginComputePass(command_encoder, desc)

def set_pipeline(compute_encoder, pipeline):
    webgpu.wgpuComputePassEncoderSetPipeline(compute_encoder, pipeline)

def set_bind_group(compute_encoder, bind_group):
    webgpu.wgpuComputePassEncoderSetBindGroup(compute_encoder, 0, bind_group, 0, None)

def dispatch_workgroups(compute_encoder, x, y, z):
    webgpu.wgpuComputePassEncoderDispatchWorkgroups(compute_encoder, x, y, z)

def end_compute_pass(compute_encoder):
    webgpu.wgpuComputePassEncoderEnd(compute_encoder)

def command_encoder_finish(command_encoder):
    return webgpu.wgpuCommandEncoderFinish(command_encoder, webgpu.WGPUCommandBufferDescriptor())

def submit(device, command_buffers):
    cb_buffers_array_type = webgpu.WGPUCommandBuffer * len(command_buffers)
    cb_buffers_array = cb_buffers_array_type(*command_buffers)
    webgpu.wgpuQueueSubmit(webgpu.wgpuDeviceGetQueue(device), len(command_buffers), cb_buffers_array)

def sync(device):
    cb_info = webgpu.WGPUQueueWorkDoneCallbackInfo2()
    cb_info.nextInChain = None
    cb_info.mode = webgpu.WGPUCallbackMode_WaitAnyOnly
    result = ResultContainer()

    def cb(status, u1, u2):
        result.status = status

    cb_info.callback = webgpu.WGPUQueueWorkDoneCallback2(cb)
    wait(webgpu.wgpuQueueOnSubmittedWorkDone2(webgpu.wgpuDeviceGetQueue(device), cb_info))

    if result.status != webgpu.WGPUQueueWorkDoneStatus_Success:
        raise RuntimeError(f"Submitted work failed: [{webgpu.WGPUQueueWorkDoneStatus__enumvalues[result.status]}]")

def pop_error(device):
    cb_info = webgpu.WGPUPopErrorScopeCallbackInfo()
    cb_info.nextInChain = None
    cb_info.mode = webgpu.WGPUCallbackMode_WaitAnyOnly
    result_container = ResultContainer()

    def cb(status, type, str, i2):
        if type != webgpu.WGPUErrorType_NoError:
            result_container.value = from_wgpu_str(str)

    cb_info.callback = webgpu.WGPUPopErrorScopeCallback(cb)
    wait(webgpu.wgpuDevicePopErrorScopeF(device, cb_info))
    return result_container.value
