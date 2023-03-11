from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("PopCap Games iOS Texture (Legacy)", ".tex;.txz")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadRGBA(handle, noepyLoadRGBA)
    noesis.logPopup()
    return 1

def noepyCheckType(texData):
    return 1
    
def noepyLoadRGBA(texData, texList):
    bs = NoeBitStream(texData)
    bs.seek(0x2)
    texWidth = bs.readShort()
    texHeight = bs.readShort()
    texFmt = bs.readShort()
    compChk = bs.readByte()
    bs.seek(0x8, NOESEEK_ABS)
    texData = texData[0x8:] #Do this so we read textures at 0x10
    
    if compChk == 0x78: #Decomp Zlib
        decompSzTmp = rapi.getInflatedSize(texData);
        decompTex=rapi.decompInflate(texData,decompSzTmp);
        texData = decompTex

    if texFmt == 0x1:
        print("ARGB8888")
        texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "r8g8b8a8")
    elif texFmt == 0x2:
        print("RGBA4444")
        texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "a4b4g4r4")
    elif texFmt == 0x3:
        print("RGBA5551")
        texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "a1b5g5r5")
    elif texFmt == 0x4:
        print("RGB565")
        texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "r5g6b5")
    texFmt = noesis.NOESISTEX_RGBA32
    texList.append(NoeTexture(rapi.getInputName(), texWidth, texHeight, texData, texFmt))
    return 1
