from inc_noesis import *
from addrlib import *

def registerNoesisTypes():
    handle = noesis.register("Zen Studios PX Texture", ".pxt")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadRGBA(handle, noepyLoadRGBA)
    noesis.logPopup()
    return 1

def noepyCheckType(texData):
    bs = NoeBitStream(texData)
    #Check for PXT header
    
    if noeStrFromBytes(bs.readBytes(2)) != "PX": return 0
    return 1
    
def noepyLoadRGBA(texData, texList):
    bs = NoeBitStream(texData)
    bs.seek(0x8)
    #ver = bs.readByte() #Afaik I only found 01
    texFmt = bs.readInt()
    texWidth = bs.readInt()
    texHeight = bs.readInt()
    mips = bs.readInt()
    print(texWidth, "x", texHeight)
    if texFmt != 0xE1 and texFmt != 0xF0:
        texData = texData[0x18:] #Do this so we read textures at 0x18
    else:
        WiiUTex_dataSz = bs.readInt();
        WiiUTex_unk = bs.readInt();
        texData = bs.readBytes(WiiUTex_dataSz)
        #bpp = surfaceGetBitsPerPixel(texFmt)
        
        #texData = texData[0x20:]
    #RGBA8888 texture
    if texFmt == 0x14: #Mobile
        print("RGB888")
        texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "r8 g8 b8")
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x16:    
        print("RGBA8888") #Mobile
        texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "r8 g8 b8 a8")
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x17:    
        print("RGBA8888 other one")
        texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "a8 r8 g8 b8")
        texFmt = noesis.NOESISTEX_RGBA32
    #DXT?
    elif texFmt == 0x40:    
        print("Possibly DXT, TODO!")
        #texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "r8 g8 b8 a8")
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x44:    
        print("Possibly BC4 DXT, TODO!")
        texData = rapi.imageDecodeDXT(texData, texWidth, texHeight, noesis.FOURCC_BC4)
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x54:    
        print("Xbox 360 DXT Tiled\nUNKNOWN")
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x82:    
        print("PVRTC4, TODO!")
        texData = rapi.imageDecodePVRTC(texData, texWidth, texHeight, 4)
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x83:    
        print("PVRTC4A, TODO!")
        texData = rapi.imageDecodePVRTC(texData, texWidth, texHeight, 4)
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x84:    
        print("Xbox 360 DXT Tiled\nUNKNOWN")
        #texData = rapi.imageDecodePVRTC(texData, texWidth, texHeight, 4)
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0xC0:    
        print("PS Vita Swizzled RGBA8888\nDeswizzling is WIP!")
        texData = rapi.imageFromMortonOrder(texData, texWidth, texHeight)
        texData = rapi.imageFlipRGBA32(texData, texWidth, texHeight, 1, 0)
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x8A:    
        print("ETC") #this byte is inconsistent
        texData = rapi.callExtensionMethod("etc_decoderaw32", texData, texWidth, texHeight, "rgb")
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0xE1:    
        #texData = deswizzle(texWidth, texHeight, 1, texFmt, 0, 1, 4, 4, 256, 32, 0, 0, texData)
        print("WiiU Swizzled RGBA8888\nCannot deswizzle currently!")
        texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "r8 g8 b8 a8")
        texFmt = noesis.NOESISTEX_RGBA32
    else:
        print(texFmt)
        print("UNKNOWN TEXTURE FORMAT DETECTED!")
        return 1
    texList.append(NoeTexture(rapi.getInputName(), texWidth, texHeight, texData, texFmt))
    return 1