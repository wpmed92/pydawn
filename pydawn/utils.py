from pydawn import webgpu
import ctypes

def get_wgpu_string(string_view):
    return ctypes.string_at(string_view.data, string_view.length).decode("utf-8")

def to_wgpu_str(str):
    byte_str = str.encode("utf-8")
    buffer = ctypes.create_string_buffer(byte_str)
    view = webgpu.WGPUStringView()
    view.data = ctypes.cast(ctypes.pointer(buffer), ctypes.POINTER(ctypes.c_char))
    view.length = len(byte_str)
    return view

class PyDawnUtils:
    def __init__(self):
        instDesc = webgpu.WGPUInstanceDescriptor()
        instDesc.features.timedWaitAnyEnable = True
        self.instance = webgpu.wgpuCreateInstance(instDesc)
        self.adapter = None
        self.device = None
        self.queue = None
        self.pipeline = None

    def wait(self, future):
        info = webgpu.WGPUFutureWaitInfo()
        info.future = future
        status = webgpu.wgpuInstanceWaitAny(self.instance, 1, info, 2**64 - 1)
        assert status == webgpu.WGPUWaitStatus_Success, f"Future failed"

    def request_adapter_sync(self, power_preference):
        cbInfo = webgpu.WGPURequestAdapterCallbackInfo()
        cbInfo.nextInChain = None
        cbInfo.mode = webgpu.WGPUCallbackMode_WaitAnyOnly

        def reqAdapterCb(status, adapter, string, _):
            self.adapter = adapter

        cb = webgpu.WGPURequestAdapterCallback(reqAdapterCb)
        cbInfo.callback = cb
        adapterOptions = webgpu.WGPURequestAdapterOptions()
        adapterOptions.powerPreference = power_preference
        self.wait(webgpu.wgpuInstanceRequestAdapterF(self.instance, adapterOptions, cbInfo))
        return self.adapter

    def request_device_sync(self, adapter, required_features):
        deviceDesc = webgpu.WGPUDeviceDescriptor()
        feature_array_type = webgpu.WGPUFeatureName * len(required_features)
        feature_array = feature_array_type(*required_features) 
        deviceDesc.requiredFeatureCount = len(required_features)
        deviceDesc.requiredFeatures = ctypes.cast(feature_array, ctypes.POINTER(webgpu.WGPUFeatureName))

        cbInfo = webgpu.WGPURequestDeviceCallbackInfo()
        cbInfo.nextInChain = None
        cbInfo.mode = webgpu.WGPUCallbackMode_WaitAnyOnly

        def reqDeviceCb(status, deviceImpl, i1, i2):
            assert status == webgpu.WGPURequestDeviceStatus_Success, f"Failed to request device={webgpu.WGPURequestDeviceStatus__enumvalues[status]}"
            self.device = deviceImpl
        
        cbInfo.callback = webgpu.WGPURequestDeviceCallback(reqDeviceCb)
        self.wait(webgpu.wgpuAdapterRequestDeviceF(adapter, deviceDesc, cbInfo))

        self.queue = webgpu.wgpuDeviceGetQueue(self.device)
        return self.device

    def create_buffer(self, device, size, usage):
        buffer_desc = webgpu.WGPUBufferDescriptor()
        buffer_desc.size = size
        buffer_desc.usage = usage
        buffer_desc.mappedAtCreation = False
        return webgpu.wgpuDeviceCreateBuffer(device, buffer_desc)

    def write_buffer(self, buf, offset, src):
        src_pointer = (ctypes.c_uint8 * len(src)).from_buffer(src)
        webgpu.wgpuQueueWriteBuffer(self.queue, buf, offset, src_pointer, len(src))

    def map(self, buf, size):
        cb_info = webgpu.WGPUBufferMapCallbackInfo2()
        cb_info.nextInChain = None
        cb_info.mode = webgpu.WGPUCallbackMode_AllowProcessEvents

        def map_async_cb(status, str, i1, i2):
            assert status == webgpu.WGPUBufferMapAsyncStatus_Success, f"Failed to map buffer: {webgpu.WGPUBufferMapAsyncStatus__enumvalues[status]}"
            if status != webgpu.WGPUBufferMapAsyncStatus_Success:
                print(f"msg={get_wgpu_string(str)}")

        cb_info.callback = webgpu.WGPUBufferMapCallback2(map_async_cb)
        self.wait(webgpu.wgpuBufferMapAsync2(buf, webgpu.WGPUMapMode_Read, 0, size, cb_info))

    def copy_buffer_to_buffer(self, cmd_encoder, src, src_offset, dst, dst_offset, size):
        webgpu.wgpuCommandEncoderCopyBufferToBuffer(cmd_encoder, src, src_offset, dst, dst_offset, size)

    def read_buffer(self, buf):
        size = webgpu.wgpuBufferGetSize(buf)
        tmp_usage =  webgpu.WGPUBufferUsage_CopyDst | webgpu.WGPUBufferUsage_MapRead
        tmp_buffer = self.create_buffer(self.device, size, tmp_usage)

        encoder = self.create_command_encoder()
        self.copy_buffer_to_buffer(encoder, buf, 0, tmp_buffer, 0, size)
        cb = self.command_encoder_finish(encoder)
        self.submit([cb])

        self.map(tmp_buffer, size)
        ptr = webgpu.wgpuBufferGetConstMappedRange(tmp_buffer, 0, size)

        void_ptr = ctypes.cast(ptr, ctypes.c_void_p)
        byte_array = (ctypes.c_byte * size).from_address(void_ptr.value)
        return byte_array

    def free(self, buf):
        webgpu.wgpuBufferDestroy(buf)

    def create_shader_module(self, source):
        shader = webgpu.WGPUShaderModuleWGSLDescriptor()
        shader.code = to_wgpu_str(source)
        shader.chain.next = None
        shader.chain.sType = webgpu.WGPUSType_ShaderSourceWGSL
        module = webgpu.WGPUShaderModuleDescriptor()
        module.nextInChain = ctypes.cast(ctypes.pointer(shader), ctypes.POINTER(webgpu.struct_WGPUChainedStruct))
        shader_module = webgpu.wgpuDeviceCreateShaderModule(self.device, module)
        cb_info = webgpu.WGPUCompilationInfoCallbackInfo2()
        cb_info.nextInChain = None
        cb_info.mode = webgpu.WGPUCallbackMode_WaitAnyOnly

        def compilationInfoCb(status, info, u1, u2):
            assert status == webgpu.WGPUCompilationInfoRequestStatus_Success, "Failed to create shader module"

        cb_info.callback = webgpu.WGPUCompilationInfoCallback2(compilationInfoCb)
        self.wait(webgpu.wgpuShaderModuleGetCompilationInfo2(shader_module, cb_info, None))
        return shader_module

    def create_bind_group_layout(self, entries):
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

        return webgpu.wgpuDeviceCreateBindGroupLayout(self.device, desc)
    
    def create_pipeline_layout(self, bind_group_layouts):
        pipeline_layout_desc = webgpu.WGPUPipelineLayoutDescriptor()
        pipeline_layout_desc.bindGroupLayoutCount = len(bind_group_layouts)
        bind_group_array_type = webgpu.WGPUBindGroupLayout * len(bind_group_layouts)
        bind_groups_ctype = bind_group_array_type(*bind_group_layouts)
        pipeline_layout_desc.bindGroupLayouts = bind_groups_ctype
        return webgpu.wgpuDeviceCreatePipelineLayout(self.device, pipeline_layout_desc)

    def create_bind_group(self, layout, entries):
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
        
        return webgpu.wgpuDeviceCreateBindGroup(self.device, bind_group_desc)

    def create_compute_pipeline(self, layout, compute):
        compute_desc = webgpu.WGPUComputePipelineDescriptor()
        compute_desc.layout = layout

        dawnCompute = webgpu.WGPUComputeState()
        dawnCompute.module = compute["module"]
        dawnCompute.entryPoint = to_wgpu_str(compute["entry_point"])
        compute_desc.compute = dawnCompute

        cb_info = webgpu.WGPUCreateComputePipelineAsyncCallbackInfo2()
        cb_info.nextInChain = None
        cb_info.mode = webgpu.WGPUCallbackMode_WaitAnyOnly

        def cb(status, compute_pipeline_impl, msg, i1, i2):
            if status != webgpu.WGPUCreatePipelineAsyncStatus_Success:
                print(f"error={get_wgpu_string(msg)}")
            assert status == webgpu.WGPUCreatePipelineAsyncStatus_Success, "Validation error"
            self.pipeline = compute_pipeline_impl

        cb_info.callback = webgpu.WGPUCreateComputePipelineAsyncCallback2(cb)
        self.wait(webgpu.wgpuDeviceCreateComputePipelineAsync2(self.device, compute_desc, cb_info))
        return self.pipeline

    def create_command_encoder(self):
        encoder_desc = webgpu.WGPUCommandEncoderDescriptor()
        command_encoder = webgpu.wgpuDeviceCreateCommandEncoder(self.device, encoder_desc)
        return command_encoder

    def supported_features(self):
        supported_features = webgpu.WGPUSupportedFeatures()
        webgpu.wgpuAdapterGetFeatures(self.adapter, supported_features)
        features = []

        for i in range(supported_features.featureCount):
            features.append(webgpu.WGPUFeatureName__enumvalues[supported_features.features[i]])

        return features
    
    def begin_compute_pass(self, command_encoder):
        return webgpu.wgpuCommandEncoderBeginComputePass(command_encoder, webgpu.WGPUComputePassDescriptor())
    
    def set_pipeline(self, compute_encoder, pipeline):
        webgpu.wgpuComputePassEncoderSetPipeline(compute_encoder, pipeline)

    def set_bind_group(self, compute_encoder, bind_group):
        webgpu.wgpuComputePassEncoderSetBindGroup(compute_encoder, 0, bind_group, 0, None)
    
    def dispatch_workgroups(self, compute_encoder,x,y,z):
        webgpu.wgpuComputePassEncoderDispatchWorkgroups(compute_encoder,x,y,z)

    def end_compute_pass(self, compute_encoder):
        webgpu.wgpuComputePassEncoderEnd(compute_encoder)

    def command_encoder_finish(self, command_encoder):
        return webgpu.wgpuCommandEncoderFinish(command_encoder, webgpu.WGPUCommandBufferDescriptor())

    def submit(self, command_buffers):
        cb_buffers_array_type = webgpu.WGPUCommandBuffer * len(command_buffers)
        cb_buffers_array = cb_buffers_array_type(*command_buffers)
        webgpu.wgpuQueueSubmit(self.queue, len(command_buffers), cb_buffers_array)

        cb_info = webgpu.WGPUQueueWorkDoneCallbackInfo2()
        cb_info.nextInChain = None
        cb_info.mode = webgpu.WGPUCallbackMode_WaitAnyOnly

        def cb(status, i1, i2):
            assert status == webgpu.WGPUQueueWorkDoneStatus_Success, f"Submitted work failed: {webgpu.WGPUQueueWorkDoneStatus__enumvalues[status]}"

        cb_info.callback = webgpu.WGPUQueueWorkDoneCallback2(cb)
        self.wait(webgpu.wgpuQueueOnSubmittedWorkDone2(self.queue, cb_info))
