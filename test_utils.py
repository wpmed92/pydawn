from utils import PyDawnUtils, pydawn
import array

if __name__ == "__main__":
    utils = PyDawnUtils()
    # Creating an adapter
    adapter = utils.request_adapter_sync(power_preference=pydawn.WGPUPowerPreference_HighPerformance)

    # Creating a device

    # List all the supported features by this adapter
    # features = utils.supported_features()
    # print(features)
    dev = utils.request_device_sync(adapter, [pydawn.WGPUFeatureName_ShaderF16])

    # Creating a shader module
    shader_source = b"""
        enable f16;
        @group(0) @binding(0)
        var<storage,read> data1: array<f16>;

        @group(0) @binding(1)
        var<storage,read_write> data2: array<f16>;

        @compute
        @workgroup_size(1)
        fn main(@builtin(global_invocation_id) index: vec3<u32>) {
            let i: u32 = index.x;
            data2[i] = data1[i];
        }
        """
    shader_module = utils.create_shader_module(shader_source)

    print(f"module={shader_module}")

    buffer1 = utils.create_buffer(dev, 16, pydawn.WGPUBufferUsage_Storage)
    buffer2 = utils.create_buffer(dev, 16, pydawn.WGPUBufferUsage_Storage | pydawn.WGPUBufferUsage_CopySrc)

    # Setup layout and bindings
    binding_layouts = [
        {
            "binding": 0,
            "visibility": pydawn.WGPUShaderStage_Compute,
            "buffer": {
                "type": pydawn.WGPUBufferBindingType_ReadOnlyStorage,
            },
        },
        {
            "binding": 1,
            "visibility": pydawn.WGPUShaderStage_Compute,
            "buffer": {
                "type": pydawn.WGPUBufferBindingType_Storage,
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
    bind_group_layout = utils.create_bind_group_layout(entries=binding_layouts)
    pipeline_layout = utils.create_pipeline_layout(bind_group_layouts=[bind_group_layout])
    bind_group = utils.create_bind_group(layout=bind_group_layout, entries=bindings)

    # Create and run the pipeline
    compute_pipeline = utils.create_compute_pipeline(
        layout=pipeline_layout,
        compute={"module": shader_module, "entry_point": b"main"},
    )

    print(f"compute_pipeline={compute_pipeline}")
    command_encoder = utils.create_command_encoder()
    compute_pass = utils.begin_compute_pass()
    print(f"compute_pass={compute_pass}")

    utils.set_pipeline(compute_pass, compute_pipeline)
    utils.set_bind_group(compute_pass, bind_group)
    utils.dispatch_workgroups(compute_pass, 4, 1, 1)
    utils.end_compute_pass(compute_pass)
    cb_buffer = utils.command_encoder_finish()
    print(cb_buffer)
    utils.submit([cb_buffer])




    