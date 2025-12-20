# Subgroup matrix dawn

Before:

```python
instDesc = webgpu.WGPUInstanceDescriptor()
instDesc.features.timedWaitAnyEnable = True
```

After:
```python
instDesc = webgpu.WGPUInstanceDescriptor()
required_inst_features = [webgpu.WGPUInstanceFeatureName_TimedWaitAny]
feature_array_type = webgpu.WGPUFeatureName * len(required_inst_features)
feature_array = feature_array_type(*required_inst_features)
instDesc.requiredFeatureCount = len(required_inst_features)
instDesc.requiredFeatures = ctypes.cast(feature_array, ctypes.POINTER(webgpu.WGPUFeatureName))
```


Before:

```python
wait(webgpu.wgpuInstanceRequestAdapterF(instance, adapterOptions, cb_info))
```

After:

A future by default, without the F suffix
```python3
wait(webgpu.wgpuInstanceRequestAdapter(instance, adapterOptions, cb_info))
```


Before:

```python3
def cb(status, adapter, msg, _):
    result.status = status
    result.value = adapter
    result.msg = from_wgpu_str(msg)
cb_info.callback = webgpu.WGPURequestAdapterCallback(cb)
```

After:

```python
 def cb(status, adapter, msg, i1, i2):
    result.status = status
    result.value = adapter
    result.msg = from_wgpu_str(msg)

cb_info.callback = webgpu.WGPURequestAdapterCallback(cb)
```

## No `webgpu.WGPUSupportedLimits()`

Instead,  just use `webgpu.WGPULimits()

No WGPURequiredLimits either, to apply your limits on `device_desc.requiredLimits`, just apply the `WGPULimits` directly
