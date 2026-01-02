from pydawn import utils, webgpu
import numpy as np

def compute_with_max_buffer_size(max_buffer_size: int) -> np.array:
    # Creating an adapter
    adapter = utils.request_adapter_sync(power_preference=webgpu.WGPUPowerPreference_HighPerformance)

    # Creating a device
    dev = utils.request_device_sync(adapter, [])

    # Creating a shader module
    shader_source = """
        @group(0) @binding(0)
        var<storage,read_write> data1: array<f32>;

        @compute
        @workgroup_size(1)
        fn main(@builtin(global_invocation_id) index: vec3<u32>) {
            var idx = index.y*32768+index.x;
            if (idx < arrayLength(&data1)) {
            data1[idx] = 1.0f;
            }
        }
    """
    shader_module = utils.create_shader_module(dev, shader_source)

    buffer1 = utils.create_buffer(dev, max_buffer_size, webgpu.WGPUBufferUsage_Storage | webgpu.WGPUBufferUsage_CopySrc)

    # Setup layout and bindings
    binding_layouts = [
        {
            "binding": 0,
            "visibility": webgpu.WGPUShaderStage_Compute,
            "buffer": {
                "type": webgpu.WGPUBufferBindingType_Storage,
            },
        },
    ]
    bindings = [
        {
            "binding": 0,
            "resource": {"buffer": buffer1, "offset": 0, "size": max_buffer_size},
        }
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
    utils.dispatch_workgroups(compute_pass, 32768, 32768, 1)
    utils.end_compute_pass(compute_pass)
    cb_buffer = utils.command_encoder_finish(command_encoder)
    utils.submit(dev, [cb_buffer])
    byte_array = utils.read_buffer(dev, buffer1)
    out_array = np.frombuffer(byte_array, dtype=np.float32)
    webgpu.wgpuBufferRelease(buffer1)
    webgpu.wgpuBufferDestroy(buffer1)
    return out_array

if __name__ == "__main__":
    _4gigs = 1024*1024*1024*4
    # Just below 4 gigabytes
    out1 = compute_with_max_buffer_size(_4gigs-4)
    # Passes
    assert np.all(out1 == 1.0), "Incorrect output buffer"
    print(f"out1 ok for {_4gigs-4} bytes")

    # Exactly 4 gigabytes
    out2 = compute_with_max_buffer_size(_4gigs)
    # Fails
    assert np.all(out2 == 1.0), "Incorrect output buffer"
