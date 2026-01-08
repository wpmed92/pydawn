from pydawn.experimental import utils, webgpu
import numpy as np

if __name__ == "__main__":
    rows, cols = 1024, 1024
    tile_dim = 8
    # replace with np.float16 for mixed-precision matmul
    dtype = np.float32
    shader_dtype = 'f16' if dtype == np.float16 else 'f32'
    A = np.random.rand(rows, cols).astype(dtype)
    B = np.random.rand(rows, cols).astype(dtype)

    # Creating an adapter
    adapter = utils.request_adapter_sync(power_preference=webgpu.WGPUPowerPreference_HighPerformance)

    # Creating a device
    # Request ChromiumExperimentalSubgroupMatrix features
    features = [webgpu.WGPUFeatureName_ChromiumExperimentalSubgroupMatrix, webgpu.WGPUFeatureName_Subgroups]
    if dtype == np.float16: features += [webgpu.WGPUFeatureName_ShaderF16]
    dev = utils.request_device_sync(adapter, features)

    # Print out the types of subgroup matrix configurations supported by the adapter
    utils.get_adapter_info(dev)

    # Creating a shader module
    shader_source = f"""
        // If f16 is used, we need to enable the feature
        {'enable f16;' if dtype == np.float16 else ''}
        enable chromium_experimental_subgroup_matrix;
        enable subgroups;
        requires subgroup_id;

        @group(0) @binding(0)
        var<storage,read> mat_a: array<{shader_dtype}>;

        @group(0) @binding(1)
        var<storage,read> mat_b: array<{shader_dtype}>;

        @group(0) @binding(2)
        var<storage,read_write> output: array<f32>;
        
        @compute
        @workgroup_size(64)
        fn main(@builtin(workgroup_id) wid: vec3<u32>,
                @builtin(subgroup_id) subgroup_id : u32) {{
            var acc: subgroup_matrix_result<f32, 8, 8> = subgroup_matrix_result<f32, 8, 8>(0.0);
            let stride = {cols}u;
            for (var k = 0u; k < {cols}u; k+= {tile_dim}u) {{
                let lhs_offset = (wid.y * {tile_dim}u * {cols}u) + k;
                let rhs_offset = k * {cols}u + (wid.x * {tile_dim}u);
                let lhs = subgroupMatrixLoad<subgroup_matrix_left<{shader_dtype}, 8, 8>>(&mat_a, lhs_offset, false, stride);
                let rhs = subgroupMatrixLoad<subgroup_matrix_right<{shader_dtype}, 8, 8>>(&mat_b, rhs_offset, false, stride);
                acc = subgroupMatrixMultiplyAccumulate(lhs, rhs, acc);
            }}

            var storeOffset = (wid.y * {tile_dim}u * {cols}u) + (wid.x * {tile_dim}u);
            subgroupMatrixStore(&output, storeOffset, acc, false, stride);
        }}
    """
    shader_module = utils.create_shader_module(dev, shader_source)
    matrix_buffer_size = rows*cols*(4 if dtype == np.float32 else 2)
    output_buffer_size = rows*cols*4
    # A
    mat_a = utils.create_buffer(dev, matrix_buffer_size, webgpu.WGPUBufferUsage_Storage | webgpu.WGPUBufferUsage_CopyDst)
    utils.write_buffer(dev, mat_a, 0, bytearray(A.tobytes()))

    # B
    mat_b = utils.create_buffer(dev, matrix_buffer_size, webgpu.WGPUBufferUsage_Storage | webgpu.WGPUBufferUsage_CopyDst)
    utils.write_buffer(dev, mat_b, 0, bytearray(B.tobytes()))

    # C
    output = utils.create_buffer(dev, output_buffer_size, webgpu.WGPUBufferUsage_Storage | webgpu.WGPUBufferUsage_CopySrc)


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
            "resource": {"buffer": output, "offset": 0, "size": output_buffer_size},
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
    utils.dispatch_workgroups(compute_pass, rows//tile_dim, cols//tile_dim, 1)
    utils.end_compute_pass(compute_pass)
    cb_buffer = utils.command_encoder_finish(command_encoder)
    utils.submit(dev, [cb_buffer])
    byte_array = utils.read_buffer(dev, output)

    matmul_output = np.frombuffer(byte_array, dtype=np.float32)
    print(matmul_output)
    np.testing.assert_allclose(matmul_output.reshape(1024,1024), A @ B, atol=1e-2, rtol=1e-3)
