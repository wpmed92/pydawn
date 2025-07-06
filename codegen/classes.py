
class GPUSupportedLimits:
  pass

class GPUSupportedFeatures:
  pass

class WGSLLanguageFeatures:
  pass

class GPUAdapterInfo:
  pass

class GPU:
  def requestAdapter(self, options):
    pass
  def getPreferredCanvasFormat(self):
    pass

class GPUAdapter:
  def requestDevice(self, descriptor):
    pass

class GPUDevice:
  def destroy(self):
    pass
  def createBuffer(self, descriptor):
    pass
  def createTexture(self, descriptor):
    pass
  def createSampler(self, descriptor):
    pass
  def importExternalTexture(self, descriptor):
    pass
  def createBindGroupLayout(self, descriptor):
    pass
  def createPipelineLayout(self, descriptor):
    pass
  def createBindGroup(self, descriptor):
    pass
  def createShaderModule(self, descriptor):
    pass
  def createComputePipeline(self, descriptor):
    pass
  def createRenderPipeline(self, descriptor):
    pass
  def createComputePipelineAsync(self, descriptor):
    pass
  def createRenderPipelineAsync(self, descriptor):
    pass
  def createCommandEncoder(self, descriptor):
    pass
  def createRenderBundleEncoder(self, descriptor):
    pass
  def createQuerySet(self, descriptor):
    pass

class GPUBuffer:
  def mapAsync(self, mode, offset, size):
    pass
  def getMappedRange(self, offset, size):
    pass
  def unmap(self):
    pass
  def destroy(self):
    pass

class GPUTexture:
  def createView(self, descriptor):
    pass
  def destroy(self):
    pass

class GPUTextureView:
  pass

class GPUExternalTexture:
  pass

class GPUSampler:
  pass

class GPUBindGroupLayout:
  pass

class GPUBindGroup:
  pass

class GPUPipelineLayout:
  pass

class GPUShaderModule:
  def getCompilationInfo(self):
    pass

class GPUCompilationMessage:
  pass

class GPUCompilationInfo:
  pass

class GPUPipelineError:
  def __init__(self,message,options):
      self.message = message
      self.options = options

class GPUComputePipeline:
  pass

class GPURenderPipeline:
  pass

class GPUCommandBuffer:
  pass

class GPUCommandEncoder:
  def beginRenderPass(self, descriptor):
    pass
  def beginComputePass(self, descriptor):
    pass
  def copyBufferToBuffer(self, source, destination, size):
    pass
  def copyBufferToBuffer(self, source, sourceOffset, destination, destinationOffset, size):
    pass
  def copyBufferToTexture(self, source, destination, copySize):
    pass
  def copyTextureToBuffer(self, source, destination, copySize):
    pass
  def copyTextureToTexture(self, source, destination, copySize):
    pass
  def clearBuffer(self, buffer, offset, size):
    pass
  def resolveQuerySet(self, querySet, firstQuery, queryCount, destination, destinationOffset):
    pass
  def finish(self, descriptor):
    pass

class GPUComputePassEncoder:
  def setPipeline(self, pipeline):
    pass
  def dispatchWorkgroups(self, workgroupCountX, workgroupCountY, workgroupCountZ):
    pass
  def dispatchWorkgroupsIndirect(self, indirectBuffer, indirectOffset):
    pass
  def end(self):
    pass

class GPURenderPassEncoder:
  def setViewport(self, x, y, width, height, minDepth, maxDepth):
    pass
  def setScissorRect(self, x, y, width, height):
    pass
  def setBlendConstant(self, color):
    pass
  def setStencilReference(self, reference):
    pass
  def beginOcclusionQuery(self, queryIndex):
    pass
  def endOcclusionQuery(self):
    pass
  def executeBundles(self, bundles):
    pass
  def end(self):
    pass

class GPURenderBundle:
  pass

class GPURenderBundleEncoder:
  def finish(self, descriptor):
    pass

class GPUQueue:
  def submit(self, commandBuffers):
    pass
  def onSubmittedWorkDone(self):
    pass
  def writeBuffer(self, buffer, bufferOffset, data, dataOffset, size):
    pass
  def writeTexture(self, destination, data, dataLayout, size):
    pass
  def copyExternalImageToTexture(self, source, destination, copySize):
    pass

class GPUQuerySet:
  def destroy(self):
    pass

class GPUCanvasContext:
  def configure(self, configuration):
    pass
  def unconfigure(self):
    pass
  def getConfiguration(self):
    pass
  def getCurrentTexture(self):
    pass

class GPUDeviceLostInfo:
  pass

class GPUDevice:
  pass

class GPUError:
  pass

class GPUValidationError:
  def __init__(self,message):
      self.message = message

class GPUOutOfMemoryError:
  def __init__(self,message):
      self.message = message

class GPUInternalError:
  def __init__(self,message):
      self.message = message

class GPUDevice:
  def pushErrorScope(self, filter):
    pass
  def popErrorScope(self):
    pass

class GPUUncapturedErrorEvent:
  def __init__(self,type,gpuUncapturedErrorEventInitDict):
      self.type = type
      self.gpuUncapturedErrorEventInitDict = gpuUncapturedErrorEventInitDict

class GPUDevice:
  pass
