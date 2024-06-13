from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("Tramsmension SexyAppFramework Texture", ".tex")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadRGBA(handle, noepyLoadRGBA)
    noesis.logPopup()
    return 1

def noepyCheckType(texData):
    #Let's not mess up other scripts with TEX
    return 1
    
def noepyLoadRGBA(texData, texList):
    bs = NoeBitStream(texData)
    bs.seek(0x7)
    dummy = bs.readUInt()
    dummy2 = bs.readByte()
    texWidth = bs.readUInt()
    texHeight = bs.readUInt()
    texFmt = bs.readUInt()
    dummy3 = bs.readUInt()
    dummy4 = bs.readUInt()
    compTexSize = bs.readUInt()
    dummy5 = bs.readUInt()
    dummy6 = bs.readUInt()
    dummy7 = bs.readUInt()
    decompTex = bytearray()
    compTexToDecomp = bs.readBytes(compTexSize)
    compTexDecompSize = rapi.getInflatedSize(compTexToDecomp)
    decompTex += rapi.decompInflate(compTexToDecomp, compTexDecompSize)
    print(texWidth, texHeight, texFmt)
    #RGBA8888 texture
    if texFmt == 0x2:
        print("RGBA8888: format detected")
        texData = rapi.imageDecodeRaw(decompTex, texWidth, texHeight, "b8 g8 r8 a8")
        texFmt = noesis.NOESISTEX_RGBA32
    #RGBA4444 texture
    elif texFmt == 0x3:
        print("RGBA4444: format detected")
        texData = rapi.imageDecodeRaw(decompTex, texWidth, texHeight, "b4 g4 r4 a4")
        texFmt = noesis.NOESISTEX_RGBA32
    else:
        print("UNKNOWN TEXTURE FORMAT DETECTED!")
        return None
    texList.append(NoeTexture(rapi.getInputName(), texWidth, texHeight, texData, texFmt))
    return 1