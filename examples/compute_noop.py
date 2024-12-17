from pydawn import utils, webgpu
import numpy as np

if __name__ == "__main__":
    pd_utils = utils.PyDawnUtils()

    # Creating an adapter
    adapter = pd_utils.request_adapter_sync(power_preference=webgpu.WGPUPowerPreference_HighPerformance)

    # Creating a device
    dev = pd_utils.request_device_sync(adapter, [webgpu.WGPUFeatureName_ShaderF16])

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
    shader_module = pd_utils.create_shader_module(shader_source)
    buffer1 = pd_utils.create_buffer(dev, 16, webgpu.WGPUBufferUsage_Storage | webgpu.WGPUBufferUsage_CopyDst)

    # Pass-in test data
    half_float_array = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0], dtype=np.float16)
    pd_utils.write_buffer(buffer1, 0, bytearray(half_float_array.tobytes()))

    buffer2 = pd_utils.create_buffer(dev, 16, webgpu.WGPUBufferUsage_Storage | webgpu.WGPUBufferUsage_CopySrc)

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
    bind_group_layout = pd_utils.create_bind_group_layout(entries=binding_layouts)
    pipeline_layout = pd_utils.create_pipeline_layout(bind_group_layouts=[bind_group_layout])
    bind_group = pd_utils.create_bind_group(layout=bind_group_layout, entries=bindings)

    # Create and run the pipeline
    compute_pipeline = pd_utils.create_compute_pipeline(
        layout=pipeline_layout,
        compute={"module": shader_module, "entry_point": "main"},
    )

    command_encoder = pd_utils.create_command_encoder()
    compute_pass = pd_utils.begin_compute_pass(command_encoder)

    pd_utils.set_pipeline(compute_pass, compute_pipeline)
    pd_utils.set_bind_group(compute_pass, bind_group)
    pd_utils.dispatch_workgroups(compute_pass, 8, 1, 1)
    pd_utils.end_compute_pass(compute_pass)
    cb_buffer = pd_utils.command_encoder_finish(command_encoder)
    pd_utils.submit([cb_buffer])
    byte_array = pd_utils.read_buffer(buffer2)

    half_float_array = np.frombuffer(byte_array, dtype=np.float16)
    print(half_float_array)