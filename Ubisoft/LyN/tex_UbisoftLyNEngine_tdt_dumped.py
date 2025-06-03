#Mod by LHR to support all formats for all platforms

from inc_noesis import *
import lib_zq_nintendo_tex as nintexture
    
def registerNoesisTypes():
    handle = noesis.register("LyN Engine Dumped Texture Data", ".tdt") #For data dumped from the TDT splitter. https://reshax.com/files/file/1183-tex_justdance4_wii_tdtzip/
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadRGBA(handle, noepyLoadRGBA)
    return 1

def noepyCheckType(data):
    return 1
   
#TODO: There's no way to detect what swizzle is used, so set this to the given platform if it looks weird, only Wii is done, I haven't checked the others aside from Wii U iirc it doesn't use swizzle but icbw.
platformSwizzle = 0 #1: Wii, 2: X360, 3: PS3

def noepyLoadRGBA(data, texList):
    dataSize = len(data) - 0x10         
    bs = NoeBitStream(data)
    bs.setEndian(NOE_LITTLEENDIAN)
    bs.seek(0x08, NOESEEK_ABS)  
    texPixelFmt = bs.readUByte()
    bs.seek(0x0C, NOESEEK_ABS)         
    imgWidth = bs.readUShort()         
    imgHeight = bs.readUShort()         
    data = bs.readBytes(dataSize)
    if texPixelFmt == 0x00: 
        if platformSwizzle == 1:
            print("ARGB8888 (WIP)")
            data = nintexture.convert(data, imgWidth, imgHeight, nintexture.NINTEX_RGBA32)
        else:
            print("RGBA8888")
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r8 g8 b8 a8")
            texFmt = noesis.NOESISTEX_RGBA32
    #elif texPixelFmt == 0x2:
        #print("R16F") #not in RGH.
        #texFmt = noesis.NOESISTEX_RGBA32;
    #elif texPixelFmt == 0x3:
        #print("RG16F") #not in RGH.
        #texFmt = noesis.NOESISTEX_RGBA32;
    #elif texPixelFmt == 0x4:
        #print("ABGR16F") #not in RGH.
        #texFmt = noesis.NOESISTEX_RGBA32;
    elif texPixelFmt == 0x5:
        print("R32F (WIP)") #not in RGH.
        if platformSwizzle == 1:
            data = nintexture.convert(data, imgWidth, imgHeight, nintexture.NINTEX_RGBA32)
        else:
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r32")
            texFmt = noesis.NOESISTEX_RGBA32;
    elif texPixelFmt == 0x6:
        print("GR32F") #not in RGH.
        if platformSwizzle == 1:
            data = nintexture.convert(data, imgWidth, imgHeight, nintexture.NINTEX_RGBA32)
        else:
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r32 g32")
            texFmt = noesis.NOESISTEX_RGBA32;
    elif texPixelFmt == 0x6:
        print("ABGR32F") #not in RGH.
        if platformSwizzle == 1:
            data = nintexture.convert(data, imgWidth, imgHeight, nintexture.NINTEX_RGBA32)
        else:
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r32 g32, b32, a32")
            texFmt = noesis.NOESISTEX_RGBA32;
    #elif texPixelFmt == 0x7:
        #print("D16")
        #texFmt = noesis.NOESISTEX_RGBA32;
    #elif texPixelFmt == 0x8:
        #print("D24S8")
        #texFmt = noesis.NOESISTEX_RGBA32;
    elif texPixelFmt == 0x09:
        if (platformSwizzle == 1):
            print("CMPR (Wii)")
            data = nintexture.convert(data, imgWidth, imgHeight, nintexture.NINTEX_CMPR)
        else:
            print("DXT1")
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r8 g8 b8 a8")
            texFmt = noesis.NOESISTEX_DXT1;
    elif texPixelFmt == 0x0A:
        print("DXT3") #not in RGH.
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r8 g8 b8 a8")
        texFmt = noesis.NOESISTEX_DXT3;
    elif texPixelFmt == 0x0B:
        print("DXT5") #not in RGH.
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r8 g8 b8 a8")
        texFmt = noesis.NOESISTEX_DXT5;
    #elif texPixelFmt == 0xC:
        #print("D16Tex")
        #texFmt = noesis.NOESISTEX_RGBA32;
    #elif texPixelFmt == 0xD:
        #print("D24S8Tex")
        #texFmt = noesis.NOESISTEX_RGBA32;
    elif texPixelFmt == 0x0E:
        print("RGB565")
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r5 g6 b5 a8")
        texFmt = noesis.NOESISTEX_RGBA32
    elif texPixelFmt == 0xF:
        print("A2RGB10")
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "a8")
        texFmt = noesis.NOESISTEX_RGBA32;
    elif texPixelFmt == 0x10:
        print("XRGB8888")
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r8 g8 b8 x8")
        texFmt = noesis.NOESISTEX_RGBA32;
    elif texPixelFmt == 0x11:
        print("A8")
        if (platformSwizzle == 1):
            data = nintexture.convert(data, imgWidth, imgHeight, nintexture.NINTEX_I8)
        else:
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "a8")
            texFmt = noesis.NOESISTEX_RGBA32;
    elif texPixelFmt == 0x12:
        print("L8 (WIP)")
        if (platformSwizzle == 1):
            data = nintexture.convert(data, imgWidth, imgHeight, nintexture.NINTEX_I8)
        else:
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "l8")
            texFmt = noesis.NOESISTEX_RGBA32;
    elif texPixelFmt == 0x13:
        print("AL88")
        #add to convert
        In = bytearray(data)
        Out = bytearray(2*len(data))
        for i in range(3): Out[i::4] = In[0::2]
        Out[3::4] = In[1::2]
        data = Out
        if (platformSwizzle == 1):
            data = nintexture.convert(data, imgWidth, imgHeight, nintexture.NINTEX_I4)
        else:
            Out = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r8 a8")
            texFmt = noesis.NOESISTEX_RGBA32;
    elif texPixelFmt == 0x14: 
        print("RGBA4444") #not in rgh
        #if (platformSwizzle == 1)
            #untiled = untile(data,imgWidth,imgHeight,4,4,16)
        #else
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r4 g4 b4 a4")
        texFmt = noesis.NOESISTEX_RGBA32
    elif texPixelFmt == 0x15:
        print("AL44") #not in rgh
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "a4 r4")
        texFmt = noesis.NOESISTEX_RGBA32;
    #0x16/22 is none
    #elif texPixelFmt == 0x17:
        #print("RawDepth")
        #texFmt = noesis.NOESISTEX_RGBA32;
    #elif texPixelFmt == 0x18:
        #print("ABGR16")
        #texFmt = noesis.NOESISTEX_RGB24;
    #elif texPixelFmt == 0x19:
        #print("L16")
        #texFmt = noesis.NOESISTEX_RGB24;
    #elif texPixelFmt == 0x1A:
        #print("GR16")
            #data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r8 g8 b8 a8")
        #texFmt = noesis.NOESISTEX_RGB24;
    elif texPixelFmt == 0x1B:
        if (platformSwizzle == 1):
            print("ACPR (CMPR)")
            data = nintexture.convert(data, imgWidth, imgHeight, 14)
        else:
            print("ACPR (DXT1)")
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r8 g8 b8 a8")
            texFmt = noesis.NOESISTEX_DXT1;
    else:
        print("TEXTURE FORMAT", texFmt, "IS AN UNKNOWN/UNSUPPORTED TEXTURE FORMAT!");
        return None
    #Todo implement flip without breaking DXT
    #data = rapi.imageFlipRGBA32(data, imgWidth, imgHeight, 0, 1)
    if platformSwizzle == 1:
        texList.append(data)
    else:
        texList.append(NoeTexture(rapi.getInputName(), imgWidth, imgHeight, data, texFmt))
    return 1