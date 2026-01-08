from pydawn.experimental import utils, webgpu
import numpy as np

if __name__ == "__main__":
    rows, cols = 1024, 1024
    A = np.random.rand(rows, cols).astype(np.float32)
    B = np.random.rand(rows, cols).astype(np.float32)

    # Creating an adapter
    adapter = utils.request_adapter_sync(power_preference=webgpu.WGPUPowerPreference_HighPerformance)

    # Creating a device
    # Request ChromiumExperimentalSubgroupMatrix features
    dev = utils.request_device_sync(adapter, [webgpu.WGPUFeatureName_ChromiumExperimentalSubgroupMatrix, webgpu.WGPUFeatureName_Subgroups])

    # Print out the types of subgroup matrix configurations supported by the adapter
    utils.get_adapter_info(dev)

    # Creating a shader module
    shader_source = """
        // enable the subgroup_matrix feature in wgsl
        enable chromium_experimental_subgroup_matrix;
        enable subgroups;
        requires subgroup_id;

        // define the output buffer where we will store our subgroup matrix
        @group(0) @binding(0)
        var<storage,read> mat_a: array<f32>;

        @group(0) @binding(1)
        var<storage,read> mat_b: array<f32>;

        @group(0) @binding(2)
        var<storage,read_write> output: array<f32>;

        // exactly one 8x8 subgroup
        @compute
        @workgroup_size(64)
        fn main(@builtin(workgroup_id) wid: vec3<u32>,
                @builtin(subgroup_id) subgroup_id : u32) {
            var acc: subgroup_matrix_result<f32, 8, 8> = subgroup_matrix_result<f32, 8, 8>(0.0);
            for (var k = 0u; k < 1024u; k+= 8u) {
                var lhs_offset = (wid.y * 8u * 1024) + k;
                var rhs_offset = k * 1024 + (wid.x * 8);
                let stride = 1024u;
                var lhs = subgroupMatrixLoad<subgroup_matrix_left<f32, 8, 8>>(&mat_a, lhs_offset, false, stride);
                var rhs = subgroupMatrixLoad<subgroup_matrix_right<f32, 8, 8>>(&mat_b, rhs_offset, false, stride);
                acc = subgroupMatrixMultiplyAccumulate(lhs, rhs, acc);
            }

            var storeOffset = (wid.y * 8u * 1024u) + (wid.x * 8u);
            subgroupMatrixStore(&output, storeOffset, acc, false, 1024);
        }
    """
    shader_module = utils.create_shader_module(dev, shader_source)
    matrix_buffer_size = rows*cols*4

    # A
    mat_a = utils.create_buffer(dev, matrix_buffer_size, webgpu.WGPUBufferUsage_Storage | webgpu.WGPUBufferUsage_CopyDst)
    utils.write_buffer(dev, mat_a, 0, bytearray(A.tobytes()))

    # B
    mat_b = utils.create_buffer(dev, matrix_buffer_size, webgpu.WGPUBufferUsage_Storage | webgpu.WGPUBufferUsage_CopyDst)
    utils.write_buffer(dev, mat_b, 0, bytearray(B.tobytes()))

    # C
    output = utils.create_buffer(dev, matrix_buffer_size, webgpu.WGPUBufferUsage_Storage | webgpu.WGPUBufferUsage_CopySrc)


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
                "type": webgpu.WGPUBufferBindingType_ReadOnlyStorage,
            },
        },
        {
            "binding": 2,
            "visibility": webgpu.WGPUShaderStage_Compute,
            "buffer": {
                "type": webgpu.WGPUBufferBindingType_Storage,
            },
        }
    ]
    bindings = [
        {
            "binding": 0,
            "resource": {"buffer": mat_a, "offset": 0, "size": matrix_buffer_size},
        },
        {
            "binding": 1,
            "resource": {"buffer": mat_b, "offset": 0, "size": matrix_buffer_size},
        },
        {
            "binding": 2,
            "resource": {"buffer": output, "offset": 0, "size": matrix_buffer_size},
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
    utils.dispatch_workgroups(compute_pass, rows//8, cols//8, 1)
    utils.end_compute_pass(compute_pass)
    cb_buffer = utils.command_encoder_finish(command_encoder)
    utils.submit(dev, [cb_buffer])
    byte_array = utils.read_buffer(dev, output)

    matmul_output = np.frombuffer(byte_array, dtype=np.float32)
    print(matmul_output)
    np.testing.assert_allclose(matmul_output.reshape(1024,1024), A @ B, atol=1e-5)
