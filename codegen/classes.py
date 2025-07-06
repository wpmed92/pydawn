
class GPUSupportedLimits:
  @property
  def maxTextureDimension1D(self):
    pass
  @property
  def maxTextureDimension2D(self):
    pass
  @property
  def maxTextureDimension3D(self):
    pass
  @property
  def maxTextureArrayLayers(self):
    pass
  @property
  def maxBindGroups(self):
    pass
  @property
  def maxBindGroupsPlusVertexBuffers(self):
    pass
  @property
  def maxBindingsPerBindGroup(self):
    pass
  @property
  def maxDynamicUniformBuffersPerPipelineLayout(self):
    pass
  @property
  def maxDynamicStorageBuffersPerPipelineLayout(self):
    pass
  @property
  def maxSampledTexturesPerShaderStage(self):
    pass
  @property
  def maxSamplersPerShaderStage(self):
    pass
  @property
  def maxStorageBuffersPerShaderStage(self):
    pass
  @property
  def maxStorageTexturesPerShaderStage(self):
    pass
  @property
  def maxUniformBuffersPerShaderStage(self):
    pass
  @property
  def maxUniformBufferBindingSize(self):
    pass
  @property
  def maxStorageBufferBindingSize(self):
    pass
  @property
  def minUniformBufferOffsetAlignment(self):
    pass
  @property
  def minStorageBufferOffsetAlignment(self):
    pass
  @property
  def maxVertexBuffers(self):
    pass
  @property
  def maxBufferSize(self):
    pass
  @property
  def maxVertexAttributes(self):
    pass
  @property
  def maxVertexBufferArrayStride(self):
    pass
  @property
  def maxInterStageShaderVariables(self):
    pass
  @property
  def maxColorAttachments(self):
    pass
  @property
  def maxColorAttachmentBytesPerSample(self):
    pass
  @property
  def maxComputeWorkgroupStorageSize(self):
    pass
  @property
  def maxComputeInvocationsPerWorkgroup(self):
    pass
  @property
  def maxComputeWorkgroupSizeX(self):
    pass
  @property
  def maxComputeWorkgroupSizeY(self):
    pass
  @property
  def maxComputeWorkgroupSizeZ(self):
    pass
  @property
  def maxComputeWorkgroupsPerDimension(self):
    pass

class GPUSupportedFeatures:
  pass

class WGSLLanguageFeatures:
  pass

class GPUAdapterInfo:
  @property
  def vendor(self):
    pass
  @property
  def architecture(self):
    pass
  @property
  def device(self):
    pass
  @property
  def description(self):
    pass
  @property
  def subgroupMinSize(self):
    pass
  @property
  def subgroupMaxSize(self):
    pass
  @property
  def isFallbackAdapter(self):
    pass

class GPU:
  def requestAdapter(self, options):
    pass
  def getPreferredCanvasFormat(self):
    pass
  @property
  def wgslLanguageFeatures(self):
    pass

class GPUAdapter:
  @property
  def features(self):
    pass
  @property
  def limits(self):
    pass
  @property
  def info(self):
    pass
  def requestDevice(self, descriptor):
    pass

class GPUDevice:
  @property
  def features(self):
    pass
  @property
  def limits(self):
    pass
  @property
  def adapterInfo(self):
    pass
  @property
  def queue(self):
    pass
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
  @property
  def size(self):
    pass
  @property
  def usage(self):
    pass
  @property
  def mapState(self):
    pass
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
  @property
  def width(self):
    pass
  @property
  def height(self):
    pass
  @property
  def depthOrArrayLayers(self):
    pass
  @property
  def mipLevelCount(self):
    pass
  @property
  def sampleCount(self):
    pass
  @property
  def dimension(self):
    pass
  @property
  def format(self):
    pass
  @property
  def usage(self):
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
  @property
  def message(self):
    pass
  @property
  def type(self):
    pass
  @property
  def lineNum(self):
    pass
  @property
  def linePos(self):
    pass
  @property
  def offset(self):
    pass
  @property
  def length(self):
    pass

class GPUCompilationInfo:
  @property
  def messages(self):
    pass

class GPUPipelineError:
  def __init__(self,message,options):
      self.message = message
      self.options = options
  @property
  def reason(self):
    pass

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
  @property
  def type(self):
    pass
  @property
  def count(self):
    pass

class GPUCanvasContext:
  @property
  def canvas(self):
    pass
  def configure(self, configuration):
    pass
  def unconfigure(self):
    pass
  def getConfiguration(self):
    pass
  def getCurrentTexture(self):
    pass

class GPUDeviceLostInfo:
  @property
  def reason(self):
    pass
  @property
  def message(self):
    pass

class GPUDevice:
  @property
  def lost(self):
    pass

class GPUError:
  @property
  def message(self):
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
  @property
  def error(self):
    pass

class GPUDevice:
  @property
  def onuncapturederror(self):
    pass
