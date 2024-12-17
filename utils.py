import webgpu as pydawn
import ctypes

def get_wgpu_string(string_view):
    return ctypes.string_at(string_view.data, string_view.length).decode("utf-8")

def to_wgpu_str(byte_string):
    buffer = ctypes.create_string_buffer(byte_string)
    view = pydawn.WGPUStringView()
    view.data = ctypes.cast(ctypes.pointer(buffer), ctypes.POINTER(ctypes.c_char))
    view.length = len(byte_string)
    return view

class PyDawnUtils:
    def __init__(self):
        instDesc = pydawn.WGPUInstanceDescriptor()
        instDesc.features.timedWaitAnyEnable = True
        self.instance = pydawn.wgpuCreateInstance(instDesc)
        self.adapter = None
        self.device = None
        self.pipeline = None
        self.command_encoder = None
    
    def wait(self, future):
        info = pydawn.WGPUFutureWaitInfo()
        info.future = future
        status = pydawn.wgpuInstanceWaitAny(self.instance, 1, info, 2**64 - 1)
        assert status == pydawn.WGPUWaitStatus_Success, f"Future failed"

    def request_adapter_sync(self, power_preference):
        cbInfo = pydawn.WGPURequestAdapterCallbackInfo()
        cbInfo.nextInChain = None
        cbInfo.mode = pydawn.WGPUCallbackMode_WaitAnyOnly

        def reqAdapterCb(status, adapter, string, _):
            self.adapter = adapter

        cb = pydawn.WGPURequestAdapterCallback(reqAdapterCb)
        cbInfo.callback = cb
        adapterOptions = pydawn.WGPURequestAdapterOptions()
        adapterOptions.powerPreference = power_preference
        self.wait(pydawn.wgpuInstanceRequestAdapterF(self.instance, adapterOptions, cbInfo))
        return self.adapter
        
    def request_device_sync(self, adapter, required_features):
        deviceDesc = pydawn.WGPUDeviceDescriptor()
        feature_array_type = pydawn.WGPUFeatureName * len(required_features)
        feature_array = feature_array_type(*required_features) 
        deviceDesc.requiredFeatureCount = len(required_features)
        deviceDesc.requiredFeatures = ctypes.cast(feature_array, ctypes.POINTER(pydawn.WGPUFeatureName))
        print(feature_array[0])

        cbInfo = pydawn.WGPURequestDeviceCallbackInfo()
        cbInfo.nextInChain = None
        cbInfo.mode = pydawn.WGPUCallbackMode_WaitAnyOnly

        def reqDeviceCb(status, deviceImpl, i1, i2):
            print(f"status={status}")
            self.device = deviceImpl
        
        cbInfo.callback = pydawn.WGPURequestDeviceCallback(reqDeviceCb)
        self.wait(pydawn.wgpuAdapterRequestDeviceF(adapter, deviceDesc, cbInfo))

        return self.device

    def create_buffer(self, device, size, usage):
        buffer_desc = pydawn.WGPUBufferDescriptor()
        buffer_desc.size = size
        buffer_desc.usage = usage
        return pydawn.wgpuDeviceCreateBuffer(device, buffer_desc)
    
    def write_buffer(self, device, buf, offset, src):
        queue = pydawn.wgpuDeviceGetQueue(device)
        src_pointer = (ctypes.c_uint8 * len(src)).from_buffer(src)
        pydawn.wgpuQueueWriteBuffer(queue, buf, offset, ctypes.cast(src_pointer, ctypes.POINTER(ctypes.c_void_p)), len(src))

    def read_buffer(self, buf):
        cbInfo = pydawn.WGPUBufferMapCallbackInfo2()
        cbInfo.nextInChain = None
        cbInfo.mode = pydawn.WGPUCallbackMode_WaitAnyOnly

        def mapAsyncCb(status, str, i1, i2):
            print(status)
            print(f"msg={get_wgpu_string(str)}")

        cbInfo.callback = pydawn.WGPUBufferMapCallback2(mapAsyncCb)
        size = pydawn.wgpuBufferGetSize(buf)
        void_ptr = pydawn.wgpuBufferGetMappedRange(buf, 0, size)
        print(void_ptr)
        ctype_array_type = ctypes.c_uint8 * size
        buffer = ctype_array_type.from_address(void_ptr)
        return buffer[:size]
    
    def get_compilation_info(self, shader_module):
        cb_info = pydawn.WGPUCompilationInfoCallbackInfo2()
        cb_info.nextInChain = None
        cb_info.mode = pydawn.WGPUCallbackMode_WaitAnyOnly

        def compilationInfoCb(status, info, u1, u2):
            print(info.messageCount)
            assert status == pydawn.WGPUCompilationInfoRequestStatus_Success, "Failed to create shader module"

        cb_info.callback = pydawn.WGPUCompilationInfoCallback2(compilationInfoCb)
        self.wait(pydawn.wgpuShaderModuleGetCompilationInfo2(shader_module, cb_info, None))
    
    def create_shader_module(self, source):
        shader = pydawn.WGPUShaderModuleWGSLDescriptor()
        shader.code = to_wgpu_str(source)
        shader.chain.next = None
        shader.chain.sType = pydawn.WGPUSType_ShaderSourceWGSL
        module = pydawn.WGPUShaderModuleDescriptor()
        module.nextInChain = ctypes.cast(ctypes.pointer(shader), ctypes.POINTER(pydawn.struct_WGPUChainedStruct))
        shader_module = pydawn.wgpuDeviceCreateShaderModule(self.device, module)
        cb_info = pydawn.WGPUCompilationInfoCallbackInfo2()
        cb_info.nextInChain = None
        cb_info.mode = pydawn.WGPUCallbackMode_WaitAnyOnly

        def compilationInfoCb(status, info, u1, u2):
            assert status == pydawn.WGPUCompilationInfoRequestStatus_Success, "Failed to create shader module"

        cb_info.callback = pydawn.WGPUCompilationInfoCallback2(compilationInfoCb)
        self.wait(pydawn.wgpuShaderModuleGetCompilationInfo2(shader_module, cb_info, None))
        return shader_module
    
    def create_bind_group_layout(self, entries):
        pydawnEntries = []
        for entry in entries:
            pydawnEntry = pydawn.WGPUBindGroupLayoutEntry()
            pydawnEntry.binding = entry["binding"]
            pydawnEntry.visibility = entry["visibility"]
            bufferBindingLayout = pydawn.WGPUBufferBindingLayout()
            bufferBindingLayout.type = entry["buffer"]["type"]
            pydawnEntry.buffer = bufferBindingLayout
            pydawnEntries.append(pydawnEntry)

        entries_array_type = pydawn.WGPUBindGroupLayoutEntry * len(pydawnEntries)
        entries_array = entries_array_type(*pydawnEntries) 

        desc = pydawn.WGPUBindGroupLayoutDescriptor()
        desc.entryCount = len(pydawnEntries)
        desc.entries = ctypes.cast(entries_array, ctypes.POINTER(pydawn.WGPUBindGroupLayoutEntry))

        return pydawn.wgpuDeviceCreateBindGroupLayout(self.device, desc)
    
    def create_pipeline_layout(self, bind_group_layouts):
        pipeline_layout_desc = pydawn.WGPUPipelineLayoutDescriptor()
        pipeline_layout_desc.bindGroupLayoutCount = len(bind_group_layouts)
        bind_group_array_type = pydawn.WGPUBindGroupLayout * len(bind_group_layouts)
        bind_groups_ctype = bind_group_array_type(*bind_group_layouts)
        
        pipeline_layout_desc.bindGroupLayouts = bind_groups_ctype

        return pydawn.wgpuDeviceCreatePipelineLayout(self.device, pipeline_layout_desc)
    
    def create_bind_group(self, layout, entries):
        bind_group_desc = pydawn.WGPUBindGroupDescriptor()
        bind_group_desc.layout = layout
        bind_group_desc.entryCount = len(entries)

        pydawnEntries = []
        for entry in entries:
            pydawnEntry = pydawn.WGPUBindGroupEntry()
            pydawnEntry.binding = entry["binding"]
            pydawnEntry.buffer = entry["resource"]["buffer"]
            pydawnEntry.offset = entry["resource"]["offset"]
            pydawnEntry.size = entry["resource"]["size"]
            pydawnEntries.append(pydawnEntry)

        entries_array_type = pydawn.WGPUBindGroupEntry * len(pydawnEntries)
        entries_array = entries_array_type(*pydawnEntries) 
        bind_group_desc.entries = entries_array
        
        return pydawn.wgpuDeviceCreateBindGroup(self.device, bind_group_desc)

    def create_compute_pipeline(self, layout, compute):
        compute_desc = pydawn.WGPUComputePipelineDescriptor()
        compute_desc.layout = layout

        dawnCompute = pydawn.WGPUComputeState()
        dawnCompute.module = compute["module"]
        dawnCompute.entryPoint = to_wgpu_str(compute["entry_point"])
        compute_desc.compute = dawnCompute

        cb_info = pydawn.WGPUCreateComputePipelineAsyncCallbackInfo2()
        cb_info.nextInChain = None
        cb_info.mode = pydawn.WGPUCallbackMode_WaitAnyOnly

        def cb(status, compute_pipeline_impl, msg, i1, i2):
            if status != pydawn.WGPUCreatePipelineAsyncStatus_Success:
                print(f"error={get_wgpu_string(msg)}")
            assert status == pydawn.WGPUCreatePipelineAsyncStatus_Success, "Validation error"
            self.pipeline = compute_pipeline_impl

        cb_info.callback = pydawn.WGPUCreateComputePipelineAsyncCallback2(cb)
        self.wait(pydawn.wgpuDeviceCreateComputePipelineAsync2(self.device, compute_desc, cb_info))
        return self.pipeline
    
    def create_command_encoder(self):
        encoder_desc = pydawn.WGPUCommandEncoderDescriptor()
        self.command_encoder = pydawn.wgpuDeviceCreateCommandEncoder(self.device, encoder_desc)
        return self.command_encoder
    
    def supported_features(self):
        supported_features = pydawn.WGPUSupportedFeatures()
        pydawn.wgpuAdapterGetFeatures(self.adapter, supported_features)
        features = []
        for i in range(supported_features.featureCount):
            features.append(pydawn.WGPUFeatureName__enumvalues[supported_features.features[i]])

        return features
    
    def begin_compute_pass(self):
        desc = pydawn.WGPUComputePassDescriptor()
        return pydawn.wgpuCommandEncoderBeginComputePass(self.command_encoder, desc)
    
    def set_pipeline(self, compute_encoder, pipeline):
        pydawn.wgpuComputePassEncoderSetPipeline(compute_encoder, pipeline)

    def set_bind_group(self, compute_encoder, bind_group):
        pydawn.wgpuComputePassEncoderSetBindGroup(compute_encoder, 0, bind_group, 0, None)
    
    def dispatch_workgroups(self, compute_encoder,x,y,z):
        pydawn.wgpuComputePassEncoderDispatchWorkgroups(compute_encoder,x,y,z)

    def end_compute_pass(self, compute_encoder):
        pydawn.wgpuComputePassEncoderEnd(compute_encoder)

    def command_encoder_finish(self):
        desc = pydawn.WGPUCommandBufferDescriptor()
        return pydawn.wgpuCommandEncoderFinish(self.command_encoder, desc)

    def submit(self, command_buffers):
        cb_buffers_array_type = pydawn.WGPUCommandBuffer * len(command_buffers)
        cb_buffers_array = cb_buffers_array_type(*command_buffers) 
        pydawn.wgpuQueueSubmit(pydawn.wgpuDeviceGetQueue(self.device), len(command_buffers), cb_buffers_array)
