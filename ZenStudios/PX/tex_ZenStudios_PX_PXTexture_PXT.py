from inc_noesis import *

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
    texData = texData[0x18:] #Do this so we read textures at 0x18
    #RGBA8888 texture
    if texFmt == 0x16:    
        print("RGBA8888")
        texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "r8 g8 b8 a8")
        texFmt = noesis.NOESISTEX_RGBA32
    #DXT?
    elif texFmt == 0x40:    
        print("Possibly DXT, TODO!")
        #texData = rapi.imageDecodeDXT(texData, texWidth, texHeight, "r8 g8 b8 a8")
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x8A:    
        print("ETC") #this byte is inconsistent
        texData = rapi.callExtensionMethod("etc_decoderaw32", texData, texWidth, texHeight, "rgb")
        texFmt = noesis.NOESISTEX_RGBA32
    else:
        print("UNKNOWN TEXTURE FORMAT DETECTED!")
        return None
    texList.append(NoeTexture(rapi.getInputName(), texWidth, texHeight, texData, texFmt))
    return 1