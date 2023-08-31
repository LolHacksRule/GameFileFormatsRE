#TYSM https://forums.gameex.com/forums/topic/23953-pinball-fx2-audio-tables-missing/ for WIP DXT fixes

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
    bs.seek(0x4)
    dataType = bs.readUInt()
    texFmt = bs.readUInt()
    texWidth = bs.readUInt()
    texHeight = bs.readUInt()
    if dataType != 0x12 and dataType != 0x18:
        mips = bs.readUInt()
    
        #apply DXT hackery
        if texFmt == 0x40 or texFmt == 0x42 or texFmt == 0x44 or texFmt == 0x48 or texFmt == 0x50 or texFmt == 0x52 or texFmt == 0x54 or texFmt == 0xF0 or texFmt == 0xF4 or texFmt == 0x140:
            nr_blocks_first = (texWidth * texHeight) >> 4
            print(str(nr_blocks_first))
            
            vblocks1 = bytearray(nr_blocks_first*4)
            pblocks1 = bytearray(nr_blocks_first*4)
            ablocks1 = bytearray(nr_blocks_first*8)
            ablocks2 = bytearray(nr_blocks_first*8)
            
            if texFmt == 0x40 or texFmt == 0x50 or texFmt == 0xF0 or texFmt == 0x140: #DXT1
                vblocks1 = bs.readBytes(nr_blocks_first*4)
                skipmips(bs, nr_blocks_first, mips, 4)
                pblocks1 = bs.readBytes(nr_blocks_first*4)
                skipmips(bs, nr_blocks_first, mips, 4)
        
            if texFmt == 0x42 or texFmt == 0x44 or texFmt == 0x54 or texFmt == 0xF4: #DXT3
                ablocks1 = bs.readBytes(nr_blocks_first*8)
                skipmips(bs, nr_blocks_first, mips, 8)
                vblocks1 = bs.readBytes(nr_blocks_first*4)
                skipmips(bs, nr_blocks_first, mips, 4)
                pblocks1 = bs.readBytes(nr_blocks_first*4)
                skipmips(bs, nr_blocks_first, mips, 4)
        
            if texFmt == 0x48 or texFmt == 0x52 or texFmt == 0x64: #DXT5
                ablocks1 = bs.readBytes(nr_blocks_first*8)
                skipmips(bs, nr_blocks_first, mips, 8)
                ablocks2 = bs.readBytes(nr_blocks_first*8)
                skipmips(bs, nr_blocks_first, mips, 8)
        
            texData = bytearray(nr_blocks_first*16)
        
            for blk in range(0, nr_blocks_first):
                if texFmt == 0x40 or texFmt == 0x50 or texFmt == 0xF0 or texFmt == 0x140: #DXT1
                    bsize = 8
                    texData[blk*bsize+0] = vblocks1[blk*4+0]
                    texData[blk*bsize+1] = vblocks1[blk*4+1]
                    texData[blk*bsize+2] = vblocks1[blk*4+2]
                    texData[blk*bsize+3] = vblocks1[blk*4+3]
                    texData[blk*bsize+4] = pblocks1[blk*4+0]
                    texData[blk*bsize+5] = pblocks1[blk*4+1]
                    texData[blk*bsize+6] = pblocks1[blk*4+2]
                    texData[blk*bsize+7] = pblocks1[blk*4+3]
                if texFmt == 0x42 or texFmt == 0x44 or texFmt == 0x54 or texFmt == 0xF4: #DXT3
                    bsize = 16
                    texData[blk*bsize+0] = ablocks1[blk*8+0]
                    texData[blk*bsize+1] = ablocks1[blk*8+1]
                    texData[blk*bsize+2] = ablocks1[blk*8+2]
                    texData[blk*bsize+3] = ablocks1[blk*8+3]
                    texData[blk*bsize+4] = ablocks1[blk*8+4]
                    texData[blk*bsize+5] = ablocks1[blk*8+5]
                    texData[blk*bsize+6] = ablocks1[blk*8+6]
                    texData[blk*bsize+7] = ablocks1[blk*8+7]
                    texData[blk*bsize+8] = vblocks1[blk*4+0]
                    texData[blk*bsize+9] = vblocks1[blk*4+1]
                    texData[blk*bsize+10] = vblocks1[blk*4+2]
                    texData[blk*bsize+11] = vblocks1[blk*4+3]
                    texData[blk*bsize+12] = pblocks1[blk*4+0]
                    texData[blk*bsize+13] = pblocks1[blk*4+1]
                    texData[blk*bsize+14] = pblocks1[blk*4+2]
                    texData[blk*bsize+15] = pblocks1[blk*4+3]
                if texFmt == 0x48 or texFmt == 0x52: #DXT5
                    bsize = 16
                    for a in range(0, 8):
                        texData[blk*bsize+a] = -ablocks1[blk*8+a] + 128 & 0xFF
                    for a in range(0, 8):
                        texData[blk*bsize+a+8] = ablocks2[blk*8+a] + 128 & 0xFF
        
            #           texData[blk*bsize+0] = ablocks1[blk*8+0]
            #           texData[blk*bsize+1] = ablocks1[blk*8+1]
            #           texData[blk*bsize+2] = ablocks1[blk*8+2]
            #           texData[blk*bsize+3] = ablocks1[blk*8+3]
            #           texData[blk*bsize+4] = ablocks1[blk*8+4]
            #           texData[blk*bsize+5] = ablocks1[blk*8+5]
            #           texData[blk*bsize+6] = ablocks1[blk*8+6]
            #           texData[blk*bsize+7] = ablocks1[blk*8+7]
            #           texData[blk*bsize+8] = ablocks2[blk*8+0]
            #           texData[blk*bsize+9] = ablocks2[blk*8+1]
            #           texData[blk*bsize+10] = ablocks2[blk*8+7]
            #           texData[blk*bsize+11] = ablocks2[blk*8+6]
            #           texData[blk*bsize+12] = ablocks2[blk*8+5]
            #           texData[blk*bsize+13] = ablocks2[blk*8+4]
            #           texData[blk*bsize+14] = ablocks2[blk*8+3]
            #           texData[blk*bsize+15] = ablocks2[blk*8+2]
            
            
        elif texFmt != 0xE1 and texFmt != 0xF0 and texFmt != 352 and texFmt != 353 and texFmt != 368 and texFmt != 370:
            texData = texData[0x18:] #Do this so we read textures at 0x18
        else:
            NinTex_dataSz = bs.readUInt();
            if texFmt == 0xE1 or texFmt == 0xF0 or texFmt == 0xF4:
                align = bs.readUInt(); #If we read this, the tex off is at 0x20, else 0x1C
                #texData = texData[0x20:] #Do this so we read textures at 0x18
            texData = bs.readBytes(NinTex_dataSz)
    else:
        print("Cubemap textures are WIP!")
        texData = texData[0x14:]
    #bpp = surfaceGetBitsPerPixel(texFmt)
        
    #texData = texData[0x20:]
    

    print(texWidth, "x", texHeight)
    
    #RGBA8888 texture
    if texFmt == 0x14 or texFmt == 0x18: #Mobile
        print("RGB888")
        texFmt = noesis.NOESISTEX_RGB24
    elif texFmt == 0x16:
        print("RGBA8888") #Mobile
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x17:
        print("RGBA8888 other one")
        texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "a8 r8 g8 b8")
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x40 or texFmt == 0x140:  
        print("DXT1\nWIP")
        #texData = rapi.imageUntile360DXT(texData, texWidth, texHeight, 8) #Keeping this here
        texFmt = noesis.NOESISTEX_DXT1
    elif texFmt == 0x42:
        print("DXT2\nWIP")
        texFmt = noesis.NOESISTEX_DXT3
    elif texFmt == 0x42:
        print("DXT3\nWIP")
        texFmt = noesis.NOESISTEX_DXT3
    elif texFmt == 0x44:
        print("DXT4\nWIP")
        #texData = rapi.imageDecodeDXT(texData, texWidth, texHeight, noesis.FOURCC_BC3)
        texFmt = noesis.NOESISTEX_DXT5
    elif texFmt == 0x50:
        print("Xbox 360 DXT1 Tiled\nWIP")
        texData = rapi.swapEndianArray(texData, 2)
        texFmt = noesis.NOESISTEX_DXT1
    elif texFmt == 0x52:
        print("Xbox 360 UNK Tiled\nWIP")
        texData = rapi.swapEndianArray(texData, 2)
        texFmt = noesis.NOESISTEX_DXT5
    elif texFmt == 0x54:
        print("Xbox 360 DXT4 Tiled\nWIP")
        texData = rapi.swapEndianArray(texData, 2)
        texData = rapi.imageDecodeDXT(texData, texWidth, texHeight, noesis.FOURCC_BC3)
        texFmt = noesis.NOESISTEX_RGBA32
    #todo formats 0x60 and 0x64, seen in Vita
    elif texFmt == 0x80 or texFmt == 0x82:
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
    elif texFmt == 0x90:
        print("CTR Swizzled RGB888\nCannot deswizzle currently!")
        #texData = unswizzleCTR(texData, texWidth, texHeight, 16, 8, 4, 2)
        #texData = rapi.imageFlipRGBA32(texData, texWidth, texHeight, 0, 1)
        texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "r8 g8 b8")
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x91:
        print("CTR Swizzled RGBA8888")
        texData = unswizzleCTR(texData, texWidth, texHeight, 32, 8, 4, 2)
        texData = rapi.imageFlipRGBA32(texData, texWidth, texHeight, 0, 1)
        texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "a8 r8 g8 b8")
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x92:
        print("CTR Swizzled ETC1")
        #texData = unswizzleCTR(texData, texWidth, texHeight, 32, 8, 4, 4)
        texData = rapi.imageDecodePICA200ETC1(texData, texWidth, texHeight, 0)
        texData = rapi.imageFlipRGBA32(texData, texWidth, texHeight, 0, 1)
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x93:
        print("CTR Swizzled ETC1A4")
        texData = rapi.imageDecodePICA200ETC1(texData, texWidth, texHeight, 1)
        texData = rapi.imageFlipRGBA32(texData, texWidth, texHeight, 0, 1)
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
    elif texFmt == 0x8D:
        print("ETC1A4")
        texData = rapi.imageDecodeETC(texData, texWidth, texHeight, "RGB")
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0xE0:
        print("WiiU Swizzled RGBX8888\WIP!")
        texData = deswizzle(texWidth, texHeight, 1, texFmt, 0, 1, 4, 4, texWidth, 32, 0, 0, texData)
        texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "r8 g8 b8 x8")
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0xE1:
        print("WiiU Swizzled RGBA8888")
        texData = deswizzle(texWidth, texHeight, 1, texFmt, 0, 1, 4, 4, texWidth, 32, 0, 0, texData)
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0xF0:
        print("WiiU Swizzled BC1\nCannot deswizzle currently!")
        #texData = deswizzle(texWidth, texHeight, 1, texFmt, 0, 1, 4, 4, texWidth, 32, 0, 0, texData)
        texFmt = noesis.NOESISTEX_DXT1
    elif texFmt == 0xF4:
        #def deswizzle(width, height, depth, format_, aa, use, tileMode, swizzle_, pitch, bpp, slice, sample, data):
        print("WiiU Swizzled BC3\nCannot deswizzle currently!")
        #texData = deswizzle(texWidth, texHeight, 1, texFmt, 0, 1, 1, 1, texWidth, 32, 0, 0, texData)
        texData = rapi.imageDecodeDXT(texData, texWidth, texHeight, noesis.FOURCC_BC3)
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x0148:
        print("BC5S\nCannot deswizzle currently!")
        #texData = rapi.callExtensionMethod("untile_1dthin", texData, texWidth, texHeight, 8, 1)
        texData = rapi.imageDecodeDXT(texData, texWidth, texHeight, noesis.FOURCC_ATI2, 0.0, 2) #Reads BC5S
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x0160:
        print("NX Swizzled RGBA8888 SRGB\nCannot deswizzle currently!")
        texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "b8 g8 r8 a8")
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x0161:
        print("NX Swizzled RGBA8888\nCannot deswizzle currently!")
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x0170:
        print("NX Swizzled DXT1\nCannot deswizzle currently!")
        texFmt = noesis.NOESISTEX_DXT1
    elif texFmt == 0x0171:
        print("NX Swizzled DXT3\nCannot deswizzle currently!")
        texFmt = noesis.NOESISTEX_DXT3
    elif texFmt == 0x0172:
        print("NX Swizzled DXT5\nCannot deswizzle currently!")
        texFmt = noesis.NOESISTEX_DXT5
    elif texFmt == 0x0178:
        texData = rapi.imageDecodeDXT(texData, texWidth, texHeight, noesis.FOURCC_ATI2, 0.0, 2)
        print("NX Swizzled BC5S\nCannot decode currently!")
        texFmt = noesis.NOESISTEX_RGBA32
        #return 1
    else:
        print(texFmt)
        print("UNKNOWN TEXTURE FORMAT DETECTED!")
        return 1
    texList.append(NoeTexture(rapi.getInputName(), texWidth, texHeight, texData, texFmt))
    return 1

def unswizzleCTR(buffer, width, height, bpp, l, m, s):
    stripSize = bpp * s // 8

    result = bytearray(width * height * bpp // 8)
    ptr = 0

    for y in range(0, height, l):
        for x in range(0, width, l):
            for y1 in range(0, l, m):
                for x1 in range(0, l, m):
                    for y2 in range(0, m, s):
                        for x2 in range(0, m, s):
                            for y3 in range(s):
                                idx = (((y + y1 + y2 + y3) * width) + x + x1 + x2) * bpp // 8
                                result[idx : idx+stripSize] = buffer[ptr : ptr+stripSize]
                                ptr += stripSize

    return result

#add fixes for DXT
def skipmips(bsi, nr_blocks, mips, bsize):
    for m in range(mips-1):
        nr_blocks = nr_blocks >> 2
        if nr_blocks <= 1:
            nr_blocks = 1
        bsi.seek(nr_blocks*bsize, NOESEEK_REL)
    return 1