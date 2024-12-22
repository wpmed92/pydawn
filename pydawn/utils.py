from pydawn import webgpu
import ctypes

class ResultContainer:
    def __init__(self):
        self.value = None

instDesc = webgpu.WGPUInstanceDescriptor()
instDesc.features.timedWaitAnyEnable = True
instance = webgpu.wgpuCreateInstance(instDesc)

def get_wgpu_string(string_view):
    return ctypes.string_at(string_view.data, string_view.length).decode("utf-8")

def to_wgpu_str(str):
    byte_str = str.encode("utf-8")
    buffer = ctypes.create_string_buffer(byte_str)
    view = webgpu.WGPUStringView()
    view.data = ctypes.cast(ctypes.pointer(buffer), ctypes.POINTER(ctypes.c_char))
    view.length = len(byte_str)
    return view

def wait(future):
    info = webgpu.WGPUFutureWaitInfo()
    info.future = future
    status = webgpu.wgpuInstanceWaitAny(instance, 1, info, 2**64 - 1)
    assert status == webgpu.WGPUWaitStatus_Success, f"Future failed"

def request_adapter_sync(power_preference):
    cbInfo = webgpu.WGPURequestAdapterCallbackInfo()
    cbInfo.nextInChain = None
    cbInfo.mode = webgpu.WGPUCallbackMode_WaitAnyOnly
    container = ResultContainer()

    def reqAdapterCb(status, adapter, string, _):
        container.value = adapter

    cb = webgpu.WGPURequestAdapterCallback(reqAdapterCb)
    cbInfo.callback = cb
    adapterOptions = webgpu.WGPURequestAdapterOptions()
    adapterOptions.powerPreference = power_preference
    wait(webgpu.wgpuInstanceRequestAdapterF(instance, adapterOptions, cbInfo))
    return container.value

def request_device_sync(adapter, required_features):
    deviceDesc = webgpu.WGPUDeviceDescriptor()
    feature_array_type = webgpu.WGPUFeatureName * len(required_features)
    feature_array = feature_array_type(*required_features)
    deviceDesc.requiredFeatureCount = len(required_features)
    deviceDesc.requiredFeatures = ctypes.cast(feature_array, ctypes.POINTER(webgpu.WGPUFeatureName))
    supported_limits = webgpu.WGPUSupportedLimits()
    webgpu.wgpuAdapterGetLimits(adapter, ctypes.cast(ctypes.pointer(supported_limits),ctypes.POINTER(webgpu.struct_WGPUSupportedLimits)))
    limits = webgpu.WGPURequiredLimits()
    limits.limits = supported_limits.limits
    deviceDesc.requiredLimits = ctypes.cast(ctypes.pointer(limits),ctypes.POINTER(webgpu.struct_WGPURequiredLimits))
    cbInfo = webgpu.WGPURequestDeviceCallbackInfo()
    cbInfo.nextInChain = None
    cbInfo.mode = webgpu.WGPUCallbackMode_WaitAnyOnly
    result = ResultContainer()

    def reqDeviceCb(status, deviceImpl, i1, i2):
        assert status == webgpu.WGPURequestDeviceStatus_Success, f"Failed to request device={webgpu.WGPURequestDeviceStatus__enumvalues[status]}"
        result.value = deviceImpl
    
    cbInfo.callback = webgpu.WGPURequestDeviceCallback(reqDeviceCb)
    wait(webgpu.wgpuAdapterRequestDeviceF(adapter, deviceDesc, cbInfo))

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

    def map_async_cb(status, str, i1, i2):
        assert status == webgpu.WGPUBufferMapAsyncStatus_Success, f"Failed to map buffer: {webgpu.WGPUBufferMapAsyncStatus__enumvalues[status]}"
        if status != webgpu.WGPUBufferMapAsyncStatus_Success:
            print(f"msg={get_wgpu_string(str)}")

    cb_info.callback = webgpu.WGPUBufferMapCallback2(map_async_cb)
    wait(webgpu.wgpuBufferMapAsync2(buf, webgpu.WGPUMapMode_Read, 0, size, cb_info))

def copy_buffer_to_buffer(cmd_encoder, src, src_offset, dst, dst_offset, size):
    webgpu.wgpuCommandEncoderCopyBufferToBuffer(cmd_encoder, src, src_offset, dst, dst_offset, size)

def read_buffer(dev, buf):
    size = webgpu.wgpuBufferGetSize(buf)
    tmp_usage = webgpu.WGPUBufferUsage_CopyDst | webgpu.WGPUBufferUsage_MapRead
    tmp_buffer = create_buffer(dev, size, tmp_usage)
    encoder = create_command_encoder(dev)
    copy_buffer_to_buffer(encoder, buf, 0, tmp_buffer, 0, size)
    cb = command_encoder_finish(encoder)
    submit(dev, [cb])
    sync(dev)
    map_buffer(tmp_buffer, size)
    ptr = webgpu.wgpuBufferGetConstMappedRange(tmp_buffer, 0, size)
    void_ptr = ctypes.cast(ptr, ctypes.c_void_p)
    byte_array = (ctypes.c_uint8 * size).from_address(void_ptr.value)
    result = bytearray(byte_array)
    webgpu.wgpuBufferUnmap(tmp_buffer)
    free_buffer(tmp_buffer)
    return memoryview(result).cast("B")

def free_buffer(buf):
    webgpu.wgpuBufferRelease(buf)

def create_shader_module(device, source):
    shader = webgpu.WGPUShaderModuleWGSLDescriptor()
    shader.code = to_wgpu_str(source)
    shader.chain.next = None
    shader.chain.sType = webgpu.WGPUSType_ShaderSourceWGSL
    module = webgpu.WGPUShaderModuleDescriptor()
    module.nextInChain = ctypes.cast(ctypes.pointer(shader), ctypes.POINTER(webgpu.struct_WGPUChainedStruct))
    shader_module = webgpu.wgpuDeviceCreateShaderModule(device, module)
    cb_info = webgpu.WGPUCompilationInfoCallbackInfo2()
    cb_info.nextInChain = None
    cb_info.mode = webgpu.WGPUCallbackMode_WaitAnyOnly

    def compilationInfoCb(status, info, u1, u2):
        assert status == webgpu.WGPUCompilationInfoRequestStatus_Success, "Failed to create shader module"

    cb_info.callback = webgpu.WGPUCompilationInfoCallback2(compilationInfoCb)
    wait(webgpu.wgpuShaderModuleGetCompilationInfo2(shader_module, cb_info, None))
    return shader_module

def create_bind_group_layout(device, entries):
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

    return webgpu.wgpuDeviceCreateBindGroupLayout(device, desc)
    
def create_pipeline_layout(device, bind_group_layouts):
    pipeline_layout_desc = webgpu.WGPUPipelineLayoutDescriptor()
    pipeline_layout_desc.bindGroupLayoutCount = len(bind_group_layouts)
    bind_group_array_type = webgpu.WGPUBindGroupLayout * len(bind_group_layouts)
    bind_groups_ctype = bind_group_array_type(*bind_group_layouts)
    pipeline_layout_desc.bindGroupLayouts = bind_groups_ctype
    return webgpu.wgpuDeviceCreatePipelineLayout(device, pipeline_layout_desc)

def create_bind_group(device, layout, entries):
    bind_group_desc = webgpu.WGPUBindGroupDescriptor()
    bind_group_desc.layout = layout
    bind_group_desc.entryCount = len(entries)
    webgpuEntries = []

    for entry in entries:
        webgpuEntry = webgpu.WGPUBindGroupEntry()
        webgpuEntry.binding = entry["binding"]
        webgpuEntry.buffer = entry["resource"]["buffer"]
        webgpuEntry.offset = entry["resource"]["offset"]
        webgpuEntry.size = entry["resource"]["size"]
        webgpuEntries.append(webgpuEntry)

    entries_array_type = webgpu.WGPUBindGroupEntry * len(webgpuEntries)
    entries_array = entries_array_type(*webgpuEntries)
    bind_group_desc.entries = entries_array
    
    return webgpu.wgpuDeviceCreateBindGroup(device, bind_group_desc)

def create_compute_pipeline(device, layout, compute):
    compute_desc = webgpu.WGPUComputePipelineDescriptor()
    compute_desc.layout = layout
    dawnCompute = webgpu.WGPUComputeState()
    dawnCompute.module = compute["module"]
    dawnCompute.entryPoint = to_wgpu_str(compute["entry_point"])
    compute_desc.compute = dawnCompute

    cb_info = webgpu.WGPUCreateComputePipelineAsyncCallbackInfo2()
    cb_info.nextInChain = None
    cb_info.mode = webgpu.WGPUCallbackMode_WaitAnyOnly
    result_container = ResultContainer()
    def cb(status, compute_pipeline_impl, msg, i1, i2):
        if status != webgpu.WGPUCreatePipelineAsyncStatus_Success:
            print(f"error={get_wgpu_string(msg)}")
        assert status == webgpu.WGPUCreatePipelineAsyncStatus_Success, f"Validation error={webgpu.WGPUCreatePipelineAsyncStatus__enumvalues[status]}"
        result_container.value = compute_pipeline_impl

    cb_info.callback = webgpu.WGPUCreateComputePipelineAsyncCallback2(cb)

    webgpu.wgpuDevicePushErrorScope(device, webgpu.WGPUErrorFilter_Validation)
    wait(webgpu.wgpuDeviceCreateComputePipelineAsync2(device, compute_desc, cb_info))
    get_error(device)
    return result_container.value

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
    if writes != None:
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

    def cb(status, i1, i2):
        assert status == webgpu.WGPUQueueWorkDoneStatus_Success, f"Submitted work failed: {webgpu.WGPUQueueWorkDoneStatus__enumvalues[status]}"

    cb_info.callback = webgpu.WGPUQueueWorkDoneCallback2(cb)
    wait(webgpu.wgpuQueueOnSubmittedWorkDone2(webgpu.wgpuDeviceGetQueue(device), cb_info))

def get_error(device):
    cb_info = webgpu.WGPUPopErrorScopeCallbackInfo()
    cb_info.nextInChain = None
    cb_info.mode = webgpu.WGPUCallbackMode_WaitAnyOnly

    def cb(status, type, str, i2):
        if (get_wgpu_string(str) != ""):
            print(f"error={get_wgpu_string(str)}")

    cb_info.callback = webgpu.WGPUPopErrorScopeCallback(cb)
    wait(webgpu.wgpuDevicePopErrorScopeF(device, cb_info))
