from pydawn.experimental import utils, webgpu
import numpy as np

if __name__ == "__main__":
    # Creating an adapter
    adapter = utils.request_adapter_sync(power_preference=webgpu.WGPUPowerPreference_HighPerformance)

    # Creating a device
    # Request ChromiumExperimentalSubgroupMatrix features
    dev = utils.request_device_sync(adapter, [webgpu.WGPUFeatureName_ChromiumExperimentalSubgroupMatrix])

    # Print out the types of subgroup matrix configurations supported by the adapter
    utils.get_adapter_info(dev)

    # Creating a shader module
    shader_source = """
        // enable the subgroup_matrix feature in wgsl
        enable chromium_experimental_subgroup_matrix;

        // define the output buffer where we will store our subgroup matrix
        @group(0) @binding(0)
        var<storage,read_write> output: array<f32>;

        @compute
        @workgroup_size(32)
        fn main(@builtin(global_invocation_id) index: vec3<u32>) {
            // In WebGPU there are 3 types when dealing with subgroup matrices:
            // -> subgroup_matrix_left
            // -> subgroup_matrix_right
            // -> subgroup_matrix_result
            var lhs = subgroup_matrix_left<f32, 8, 8>(2.12);
            var rhs = subgroup_matrix_right<f32, 8, 8>(4.12);

            // Performs lhs@rhs
            var res: subgroup_matrix_result<f32,8,8> = subgroupMatrixMultiply<f32>(lhs, rhs);

            // Stores the subgroup matrix in the output buffer
            subgroupMatrixStore(&output, 0, res, false, 8);
        }
    """
    shader_module = utils.create_shader_module(dev, shader_source)
    output_size = 64*4
    output = utils.create_buffer(dev, output_size, webgpu.WGPUBufferUsage_Storage | webgpu.WGPUBufferUsage_CopySrc)


    # Setup layout and bindings
    binding_layouts = [
        {
            "binding": 0,
            "visibility": webgpu.WGPUShaderStage_Compute,
            "buffer": {
                "type": webgpu.WGPUBufferBindingType_Storage,
            },
        }
    ]
    bindings = [
        {
            "binding": 0,
            "resource": {"buffer": output, "offset": 0, "size": output_size},
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
    byte_array = utils.read_buffer(dev, output)

    matmul_output = np.frombuffer(byte_array, dtype=np.float32)
    print(matmul_output)
    expected = (np.full((8, 8), 2.12) @ np.full((8, 8), 4.12)).reshape(64)
    np.testing.assert_allclose(matmul_output, expected, atol=1e-5)
