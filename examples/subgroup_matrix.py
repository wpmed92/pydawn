from pydawn import utils, webgpu
import numpy as np

if __name__ == "__main__":
    # Creating an adapter
    adapter = utils.request_adapter_sync(power_preference=webgpu.WGPUPowerPreference_HighPerformance)

    # Creating a device
    dev = utils.request_device_sync(adapter, [webgpu.WGPUFeatureName_ChromiumExperimentalSubgroupMatrix])

    print(utils.supported_features(adapter))
    utils.get_adapter_info(dev)
    # Creating a shader module
    shader_source = """
        enable chromium_experimental_subgroup_matrix;
        @group(0) @binding(0)
        var<storage,read> data1: array<f32>;

        @group(0) @binding(1)
        var<storage,read_write> data2: array<f32>;

        
        var<workgroup> arg_0 : array<f32, 64>;
        @compute
        @workgroup_size(64)
        fn main(@builtin(global_invocation_id) index: vec3<u32>) {
            var a = subgroup_matrix_left<f32, 8, 8>(2.12);
            var b = subgroup_matrix_right<f32, 8, 8>(4.12);
            var res: subgroup_matrix_result<f32,8,8> = subgroupMatrixMultiply<f32>(a,b);
            subgroupMatrixStore(&data2, 0, res, false, 8);
        }
    """
    shader_module = utils.create_shader_module(dev, shader_source)
    buffer1 = utils.create_buffer(dev, 64*4, webgpu.WGPUBufferUsage_Storage | webgpu.WGPUBufferUsage_CopyDst)

    # Pass-in test data
    float_array = np.array([1.0]*64, dtype=np.float32)
    utils.write_buffer(dev, buffer1, 0, bytearray(float_array.tobytes()))

    buffer2 = utils.create_buffer(dev, 64*4, webgpu.WGPUBufferUsage_Storage | webgpu.WGPUBufferUsage_CopySrc)
    print(buffer2)

    # Setup layout and bindings
    binding_layouts = [
        {
            "binding": 0,
            "visibility": webgpu.WGPUShaderStage_Compute,
            "buffer": {
                "type": webgpu.WGPUBufferBindingType_ReadOnlyStorage,
            },
        },
        {
            "binding": 1,
            "visibility": webgpu.WGPUShaderStage_Compute,
            "buffer": {
                "type": webgpu.WGPUBufferBindingType_Storage,
            },
        },
    ]
    bindings = [
        {
            "binding": 0,
            "resource": {"buffer": buffer1, "offset": 0, "size": 64*4},
        },
        {
            "binding": 1,
            "resource": {"buffer": buffer2, "offset": 0, "size": 64*4},
        },
    ]

    # Creating bind group layout
    bind_group_layout = utils.create_bind_group_layout(device=dev, entries=binding_layouts)
    pipeline_layout = utils.create_pipeline_layout(device=dev, bind_group_layouts=[bind_group_layout])
    bind_group = utils.create_bind_group(device=dev, layout=bind_group_layout, entries=bindings)

    # Create and run the pipeline
    compute_pipeline = utils.create_compute_pipeline(
        device=dev,
        layout=pipeline_layout,
        compute={"module": shader_module, "entry_point": "main"},
    )

    command_encoder = utils.create_command_encoder(dev)
    compute_pass = utils.begin_compute_pass(command_encoder)

    utils.set_pipeline(compute_pass, compute_pipeline)
    utils.set_bind_group(compute_pass, bind_group)
    utils.dispatch_workgroups(compute_pass, 1, 1, 1)
    utils.end_compute_pass(compute_pass)
    cb_buffer = utils.command_encoder_finish(command_encoder)
    utils.submit(dev, [cb_buffer])
    byte_array = utils.read_buffer(dev, buffer2)

    half_float_array = np.frombuffer(byte_array, dtype=np.float32)
    print(half_float_array)
