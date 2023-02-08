from inc_noesis import *
from addrlib import *

def registerNoesisTypes():
    handle = noesis.register("Zen Studios PX Font", ".pxfont")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadRGBA(handle, noepyLoadRGBA)
    noesis.logPopup()
    return 1

def noepyCheckType(texData):
    bs = NoeBitStream(texData)
    return 1
    
def noepyLoadRGBA(texData, texList):
    bs = NoeBitStream(texData)
    texFmt = bs.readUShort()
    texWidth = bs.readUShort()
    texHeight = bs.readUShort()

    print(texWidth, "x", texHeight)
    
    texData = texData[0x06:]
    #RGBA8888 texture
    if texFmt == 0x00:    
        print("?\n")
        #texData = rapi.imageDecodeDXT(texData, texWidth, texHeight, noesis.FOURCC_BC3)
        #texData = rapi.imageUntile360Raw(texData, texWidth, texHeight, 16)
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x01:
        print("CTR Swizzled ETC1A4\nCannot deswizzle currently!")
        #texData = unswizzleCTR(texData, texWidth, texHeight, 32, 8, 4, 2)
        texData = rapi.imageDecodeETC(texData, texWidth, texHeight, "RGBA1")
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x02:    
        print("RGBA8888") #Mobile
        texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "r8 g8 b8 a8")
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x05:
        #texData = deswizzle(texWidth, texHeight, 1, texFmt, 0, 1, 4, 4, 0, 32, 0, 0, texData)
        print("WiiU Swizzled DXT5\nCannot deswizzle currently!")
        texData = rapi.imageDecodeDXT(texData, texWidth, texHeight, noesis.NOESISTEX_DXT5)
        texFmt = noesis.NOESISTEX_RGBA32
    else:
        print(texFmt)
        print("UNKNOWN TEXTURE FORMAT DETECTED!")
        return 1
    texList.append(NoeTexture(rapi.getInputName(), texWidth, texHeight, texData, texFmt))
    return 1