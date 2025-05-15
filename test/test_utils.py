import unittest
from pydawn import utils, webgpu
import os

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.adapter = utils.request_adapter_sync(power_preference=webgpu.WGPUPowerPreference_HighPerformance)
        self.assertIsNotNone(self.adapter, "adapter should not be None")
        self.device = utils.request_device_sync(self.adapter)
        self.assertIsNotNone(self.device, "device should not be None")

    def test_create_buffer(self):
        size = 16
        usage = webgpu.WGPUBufferUsage_Storage
        buf = utils.create_buffer(self.device, size, usage)
        actual_size = webgpu.wgpuBufferGetSize(buf)
        actual_usage = webgpu.wgpuBufferGetUsage(buf)
        self.assertEqual(actual_size, size, f"unexpected buffer size: (actual) {actual_size} != (expected) {size}")
        self.assertEqual(actual_usage, usage, f"unexpected buffer usage: (actual) {actual_usage} != (expected) {usage}")

    def test_buffer_read_write(self):
        buf = utils.create_buffer(self.device, 4, webgpu.WGPUBufferUsage_Storage | webgpu.WGPUBufferUsage_CopySrc | webgpu.WGPUBufferUsage_CopyDst)
        test_src = [1, 2, 3, 4]
        utils.write_buffer(self.device, buf, 0, test_src)
        out = utils.read_buffer(self.device, buf)
        self.assertEqual(list(out), test_src, f"buffer mismatch: (actual) {test_src} != (expected) {list(out)}")

    def test_copy_buffer_to_buffer(self):
        src = utils.create_buffer(self.device, 4, webgpu.WGPUBufferUsage_Storage | webgpu.WGPUBufferUsage_CopySrc | webgpu.WGPUBufferUsage_CopyDst)
        dst = utils.create_buffer(self.device, 4, webgpu.WGPUBufferUsage_Storage | webgpu.WGPUBufferUsage_CopySrc | webgpu.WGPUBufferUsage_CopyDst)
        test_src = [4, 8, 16, 32]
        utils.write_buffer(self.device, src, 0, test_src)
        utils.copy_buffer_to_buffer(self.device, src, 0, dst, 0, 4)
        dst_out = utils.read_buffer(self.device, dst)
        self.assertEqual(list(dst_out), test_src, f"buffer mismatch: (actual) {test_src} != (expected) {list(dst_out)}")

    def test_create_shader_module(self):
        shader_source = """
            @group(0) @binding(0)
            var<storage,read> data1: array<f32>;

            @group(0) @binding(1)
            var<storage,read_write> data2: array<f32>;

            @compute
            @workgroup_size(1)
            fn main(@builtin(global_invocation_id) index: vec3<u32>) {
                let i: u32 = index.x;
                data2[i] = data1[i];
            }
        """
        shader_module = utils.create_shader_module(self.device, shader_source)
        self.assertIsNotNone(shader_module, "shader_module should not be None")

    def test_compiler_error(self):
        with self.assertRaises(RuntimeError) as ctx:
            error_shader_source = """
                @group(0) @binding(0)
                var<storage,read> data1: array<f15>;

                @compute
                @workgroup_size(1)
                fn main(@builtin(global_invocation_id) index: vec3<u32>) {
                    let i: u32 = index.x;
                    data2[i] = data1[i];
                }
            """
            utils.create_shader_module(self.device, error_shader_source)
        self.assertIn("unresolved type 'f15'", str(ctx.exception))

    def test_request_adapter_error(self):
        with self.assertRaises(RuntimeError) as ctx:
            os.environ['BACKEND_TYPE'] = "D3D11"
            try:
                utils.request_adapter_sync(webgpu.WGPUPowerPreference_HighPerformance)
            finally:
                del os.environ['BACKEND_TYPE']

        self.assertIn("Unsupported backend", str(ctx.exception))

    def test_request_device_error(self):
        with self.assertRaises(RuntimeError) as ctx:
            utils.request_device_sync(self.adapter, [webgpu.WGPUFeatureName_D3D11MultithreadProtected])

        self.assertIn("Invalid feature required", str(ctx.exception))

    def test_map_buffer_error(self):
        with self.assertRaises(RuntimeError) as ctx:
            buf = utils.create_buffer(self.device, 4, webgpu.WGPUBufferUsage_Storage | webgpu.WGPUBufferUsage_MapRead | webgpu.WGPUBufferUsage_MapWrite)
            utils.map_buffer(buf, 4)

        self.assertIn("Failed to map buffer", str(ctx.exception))

    def test_create_bind_group_layout_error(self):
        with self.assertRaises(RuntimeError) as ctx:
            num_bufs = 11
            bind_group_layouts = [{
                    "binding": i,
                    "visibility": webgpu.WGPUShaderStage_Compute,
                    "buffer": {"type": webgpu.WGPUBufferBindingType_Storage},
                } for i in range(num_bufs)]
            utils.create_bind_group_layout(self.device, bind_group_layouts)

        self.assertIn(f"The number of storage buffers ({num_bufs}) in the Compute stage exceeds the maximum per-stage limit", str(ctx.exception))

    def test_create_pipeline_layout_error(self):
        with self.assertRaises(RuntimeError) as ctx:
            bind_group_layouts = [{
                    "binding": i,
                    "visibility": webgpu.WGPUShaderStage_Fragment,
                    "buffer": {"type": webgpu.WGPUBufferBindingType_Storage},
                } for i in range(11)]
            # Disable validation when creating bind group layout to catch the error later
            bind_group_layout = utils.create_bind_group_layout(self.device, bind_group_layouts, validate=False)
            utils.create_pipeline_layout(self.device, [bind_group_layout])

        self.assertIn(f"Error creating pipeline layout: [Invalid BindGroupLayout (unlabeled)] is invalid.", str(ctx.exception))

if __name__ == "__main__":
    unittest.main()
