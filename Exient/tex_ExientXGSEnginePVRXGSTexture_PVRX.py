#By LolHacksRule
#UNTESTED IN FIRST TOUCH GAMES

#Please tell me if a format that is listed isn't decoded properly
from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("Exient XGS Engine PVR Texture", ".pvrx")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadRGBA(handle, noepyLoadRGBA)
    noesis.logPopup()
    return 1

def noepyCheckType(data):
    bs = NoeBitStream(data)
    if (bs.readInt() != 64): return 0
    return 1
    
def noepyLoadRGBA(data, texList):
    bs = NoeBitStream(data)
    hdrSize = bs.readInt()
    imgWidth = bs.readInt()
    imgHeight = bs.readInt()
    numMips = bs.readInt()
    imgFmt = bs.readByte()
    flag1 = bs.readByte()
    flag2 = bs.readByte()
    flag3 = bs.readByte()
    print(hex(imgFmt)+ ": format")
    dataSize = bs.readInt()
    bpp = bs.readInt();
    red = bs.readInt();
    green = bs.readInt();
    blue = bs.readInt();
    alpha = bs.readInt();
    PVRId = bs.readInt();
    PVRSurfaces = bs.readInt()
    unknown = bs.readInt();
    unknown2 = bs.readInt();
    unknown3 = bs.readInt();
    data = bs.readBytes(dataSize)
    if dataSize == 0:
        print("Texture is empty!")
        return 1
    if flag1 == -125 or flag1 == -126:
        print("Swizzled!")
        data = rapi.imageFromMortonOrder(data, imgWidth, imgHeight) # PSVita specific swizzling, thanks Acewell
    #RGBA4444
    if imgFmt == 0x0 or imgFmt == 0x10:
        print("RGBA4444")
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "a4 b4 g4 r4")
        #data = rapi.imageFlipRGBA32(data, imgWidth, imgHeight, 0, 0)
        texFmt = noesis.NOESISTEX_RGBA32
    #RGB565
    elif imgFmt == 0x04:
        print("RGB888")
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "a0 b8 g8 r8")
        texFmt = noesis.NOESISTEX_RGBA32
    elif imgFmt == 0x11:
        print("ARGB1555")
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "a1 b5 g5 r5")
        texFmt = noesis.NOESISTEX_RGBA32
    elif imgFmt == 0x12:
        print("ARGB8888\nWIP!")
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r8 g8 b8 a8")
        texFmt = noesis.NOESISTEX_RGBA32
    elif imgFmt == 0x13:
        print("RGB565")
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r5 g6 b5 a8")
        texFmt = noesis.NOESISTEX_RGBA32
    elif imgFmt == 0x18:
        print("PVRTC_2BPP_RGBA")
        data = rapi.imageDecodePVRTC(data, imgWidth, imgHeight, 2)
        texFmt = noesis.NOESISTEX_RGBA32
    elif imgFmt == 0x19:
        print("PVRTC_4BPP_RGBA")
        data = rapi.imageDecodePVRTC(data, imgWidth, imgHeight, 4)
        texFmt = noesis.NOESISTEX_RGBA32
    elif imgFmt == 0x36:
        data = rapi.callExtensionMethod("etc_decoderaw32", data, imgWidth, imgHeight, "rgb")
        texFmt = noesis.NOESISTEX_RGBA32
    texList.append(NoeTexture(rapi.getInputName(), imgWidth, imgHeight, data, texFmt))
    return 1