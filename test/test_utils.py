import unittest
from pydawn import utils, webgpu

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.adapter = utils.request_adapter_sync(power_preference=webgpu.WGPUPowerPreference_HighPerformance)
        self.assertIsNotNone(self.adapter, "adapter should not be None")
        self.device = utils.request_device_sync(self.adapter, [webgpu.WGPUFeatureName_ShaderF16])
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
        self.assertEqual(list(out), test_src, f"buffer mismatch: (actual) {test_src} != (expected) {out}")

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
            utils.request_adapter_sync(webgpu.WGPUPowerPreference_HighPerformance, webgpu.WGPUBackendType_Vulkan)

        self.assertIn("No supported adapters", str(ctx.exception))

    def test_request_device_error(self):
        with self.assertRaises(RuntimeError) as ctx:
            utils.request_device_sync(self.adapter, [webgpu.WGPUFeatureName_D3D11MultithreadProtected])

        self.assertIn("Invalid feature required", str(ctx.exception))

    def test_map_buffer_error(self):
        with self.assertRaises(RuntimeError) as ctx:
            buf = utils.create_buffer(self.device, 4, webgpu.WGPUBufferUsage_Storage | webgpu.WGPUBufferUsage_MapRead | webgpu.WGPUBufferUsage_MapWrite)
            utils.map_buffer(buf, 4)

        self.assertIn("Failed to map buffer", str(ctx.exception))

if __name__ == "__main__":
    unittest.main()
