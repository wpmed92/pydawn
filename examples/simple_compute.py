from pydawn import utils, webgpu
import numpy as np

if __name__ == "__main__":
    # Creating an adapter
    adapter = utils.request_adapter_sync(power_preference=webgpu.WGPUPowerPreference_HighPerformance)

    # Creating a device
    dev = utils.request_device_sync(adapter, [webgpu.WGPUFeatureName_ShaderF16])

    # Creating a shader module
    shader_source = """
        enable f16;
        @group(0) @binding(0)
        var<storage,read> data1: array<f16>;

        @group(0) @binding(1)
        var<storage,read_write> data2: array<f16>;

        @compute
        @workgroup_size(1)
        fn main(@builtin(global_invocation_id) index: vec3<u32>) {
            let i: u32 = index.x;
            data2[i] = data1[i]*2;
        }
    """
    shader_module = utils.create_shader_module(dev, shader_source)
    buffer1 = utils.create_buffer(dev, 16, webgpu.WGPUBufferUsage_Storage | webgpu.WGPUBufferUsage_CopyDst)

    # Pass-in test data
    half_float_array = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0], dtype=np.float16)
    utils.write_buffer(dev, buffer1, 0, bytearray(half_float_array.tobytes()))

    buffer2 = utils.create_buffer(dev, 16, webgpu.WGPUBufferUsage_Storage | webgpu.WGPUBufferUsage_CopySrc)

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
            "resource": {"buffer": buffer1, "offset": 0, "size": 16},
        },
        {
            "binding": 1,
            "resource": {"buffer": buffer2, "offset": 0, "size": 16},
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
    utils.dispatch_workgroups(compute_pass, 8, 1, 1)
    utils.end_compute_pass(compute_pass)
    cb_buffer = utils.command_encoder_finish(command_encoder)
    utils.submit(dev, [cb_buffer])
    byte_array = utils.read_buffer(dev, buffer2)

    half_float_array = np.frombuffer(byte_array, dtype=np.float16)
    print(half_float_array)