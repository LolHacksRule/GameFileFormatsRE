#Mod by LolHacksRule, Acewell for original script https://www.zenhax.com/download/file.php?id=8466
#Added support for RGB565, RGBA4444, PVRTC4BPP, ETC2_RGB
#Added support for AB Star Wars Wii palletized textures (credits to Allen for original code [https://raw.githubusercontent.com/leeao/Noesis-Plugins/master/Textures/tex_AngryBirdsStarWars_Wii_xgt.py])
#It's not possible to detect Wii U textures rightaway so I commented sections that are moddable
#Add console checks to ensure decoding works properly
#Added conversion of r channel in LA88 (https://zenhax.com/viewtopic.php?t=7573)
#Fixed bugs with decoding X360 RGB565 and RGBA8888 textures
#Add WinPhone detection
#Add iOS and old iOS detection
#Fixed wrong channel order for WinPhone textures

#Please tell me if a format that is listed isn't decoded properly
from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("Exient XGS Engine Texture", ".xgt_dxt;.xgt;.xgt_etc;.xgt_pvr")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadRGBA(handle, noepyLoadRGBA)
    noesis.logPopup()
    return 1

def noepyCheckType(data):
    bs = NoeBitStream(data)
    if noeStrFromBytes(bs.readBytes(4)) != "XGST": return 0
    return 1
    
def noepyLoadRGBA(data, texList):
    bs = NoeBitStream(data)
    bs.seek(0x4)
    dataOffset = bs.readByte()
    platform = bs.readByte()
    headerSZ = bs.readUShort()
    numMips = bs.readUByte()
    flag1 = bs.readByte()
    flag2 = bs.readByte()
    flag3 = bs.readByte()
    imgFmt = bs.readUShort()
    print(hex(imgFmt)+ ": format")
    numColors = bs.readShort()
    imgWidth = bs.readUShort()
    imgHeight = bs.readUShort()
    imgWidth2 = bs.readUShort()
    imgHeight2 = bs.readUShort()
    paletteSize = bs.readInt()
    dataSize = bs.readInt()
    if dataSize == 0:
        print("Texture is empty!")
        return 1
    #if headerSZ == 26:
        #print("WARNING: Width may be inaccurate! If it is, uncommenting the below can temporarily help but break other textures.")
    #data = bs.readBytes(dataSize)
    if platform == 0x00:
        print("Platform: Android/Win32 [how]");
    if platform == 0x01:
        print("Platform: PlayStation 3");
    if platform == 0x02:
        print("Platform: iOS");
    if platform == 0x03:
        print("Platform: Revolution/Nintendo Wii");
    if platform == 0x04:
        print("Platform: Xenon/Xbox 360");
    if platform == 0x05:
        print("Platform: iOS_OLD");
    if platform == 0x06:
        print("Platform: CTR/Nintendo 3DS");
    if platform == 0x09:
        print("Platform: Android_OLD");
    if platform == 0x0B:
        print("Platform: caFe/Nintendo Wii U");
    if platform == 0x0E:
        print("Platform: Orbis/PlayStation 4");
    if platform == 0x10:
        print("Platform: WinPhone");
    #RGB565_ABSW_WII
    if imgFmt == 0x0:
        print("RGB565_Swizzled (WIP!)")
        if platform == 0x03:
            data = bs.readBytes(dataSize)
            #data = untile(bs.readBytes(dataSize),imgWidth,imgHeight,1,4,16) #Attempt to deswizzle ({1,0},{2,0},{0,1},{0,2})
            print("Cannot deswizzle currently!")
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "b5 g6 r5")
            texFmt = noesis.NOESISTEX_RGBA32
        elif platform == 0x04:
            data = bs.readBytes(dataSize)
            imgWidth = imgWidth + 1 #fix for textures with odd width sizes
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "b5 g6 r5")
            texFmt = noesis.NOESISTEX_RGBA32
        elif platform == 0x06:
            data = bs.readBytes(dataSize)
            #data = untile(bs.readBytes(dataSize),imgWidth,imgHeight,1,4,16) #Attempt to deswizzle ({1,0},{0,1},{2,0},{0,2},{4,0},{0,4})
            print("Cannot deswizzle currently!")
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "b5 g6 r5")
            texFmt = noesis.NOESISTEX_RGBA32
        else:
            data = bs.readBytes(dataSize)
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "b5 g6 r5")
            texFmt = noesis.NOESISTEX_RGBA32
    elif imgFmt == 0x1:
        data = bs.readBytes(dataSize)
        print("RGB565")
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "b5 g6 r5")
        texFmt = noesis.NOESISTEX_RGBA32
    #RGB565
    elif imgFmt == 0x2:
        if platform == 0x06:
            data = bs.readBytes(dataSize)
            data = untile(bs.readBytes(dataSize),imgWidth,imgHeight,8,8,16) #Attempt to deswizzle ({1,0},{0,1},{2,0},{0,2},{4,0},{0,4})
            print("Deswizzling is WIP!\nComment the above to see the swizzled image.")
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "a4 b4 g4 r4")
            texFmt = noesis.NOESISTEX_RGBA32
        if platform == 0x04:
            data = bs.readBytes(dataSize)
            print("RGBA4444")
            imgWidth = imgWidth + 1 #fix for textures with odd width sizes
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "b4 g4 r4 a4")
            texFmt = noesis.NOESISTEX_RGBA32
        else:
            data = bs.readBytes(dataSize)
            print("RGBA4444")
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "a4 b4 g4 r4")
            texFmt = noesis.NOESISTEX_RGBA32
    #RGBA4444_OR_RGBA8888
    elif imgFmt == 0x3:
        if platform == 0x00:
            data = bs.readBytes(dataSize)
            print("RGBA8888\nIt's not possible to detect the format for this platform.\nComment the below and replace with the other function to force RGBA4444.")
            #data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r4 g4 b4 a4")
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "a4 b4 g4 r4")
            texFmt = noesis.NOESISTEX_RGBA32
        elif platform == 0x01:
            print("RGBA8888\nIf it doesn't look right, look at the below comment!")
            data = bs.readBytes(dataSize)
            #data = untile(bs.readBytes(dataSize),imgWidth,imgHeight,1,4,16) #Attempt to deswizzle ({1,0},{0,1},{2,0},{0,2},{4,0},{0,4})
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "a8 r8 g8 b8")
            texFmt = noesis.NOESISTEX_RGBA32
        elif platform == 0x02:
            print("RGBA4444")
            data = bs.readBytes(dataSize)
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "a4 b4 g4 r4")
            texFmt = noesis.NOESISTEX_RGBA32
        elif platform == 0x03: #LA88 32BPP Wii texture
            data = bs.readBytes(dataSize)
            data = read32RGBA(data, imgWidth, imgHeight, 4,4)
            texFmt = noesis.NOESISTEX_RGBA32
        elif platform == 0x05:
            data = bs.readBytes(dataSize)
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r8 g8 b8 a8")
            texFmt = noesis.NOESISTEX_RGBA32
        elif platform == 0x06:
            print("RGBA8888")
            data = bs.readBytes(dataSize)
            #data = untile(bs.readBytes(dataSize),imgWidth,imgHeight,1,4,16) #Attempt to deswizzle ({1,0},{0,1},{2,0},{0,2},{4,0},{0,4})
            print("Deswizzling is WIP!\nComment the above to see the swizzled image.")
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "a8 b8 g8 r8")
            texFmt = noesis.NOESISTEX_RGBA32
        elif platform == 0x09:
            data = bs.readBytes(dataSize)
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "a8 b8 g8 r8")
            texFmt = noesis.NOESISTEX_RGBA32
        elif platform == 0x0B: #RGBA8888 Wii U
            data = bs.readBytes(dataSize)
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r8 g8 b8 a8")
            texFmt = noesis.NOESISTEX_RGBA32
        elif platform == 0x0E or platform == 0x04 or platform == 0x10: #ARGB8888 PS4/X360
            data = bs.readBytes(dataSize)
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "b8 g8 r8 a8")
            texFmt = noesis.NOESISTEX_RGBA32
    #RGBA8888
    elif imgFmt == 0x4:
        data = bs.readBytes(dataSize)
        print("RGBA8888")    
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r8 g8 b8 a8")
        texFmt = noesis.NOESISTEX_RGBA32
    elif imgFmt == 0x5:    
        print("RGBA8888 Paletized")
        palettes = readPalette(2,paletteSize,bs)
        data = untile(bs.readBytes(dataSize),imgWidth,imgHeight,8,4,8)
        textureData = convert8to32(data,palettes,imgWidth,imgHeight)
        texList.append(NoeTexture(rapi.getInputName(), imgWidth, imgHeight, textureData, noesis.NOESISTEX_RGBA32))
        return 1
    #LA88
    elif imgFmt == 0x8:
        if platform == 0x00 or platform == 0x02: #Android
            print("LA88")
            data = bs.readBytes(dataSize)
            #add to convert
            In = bytearray(data)
            Out = bytearray(2*len(data))
            for i in range(3): Out[i::4] = In[0::2]
            Out[3::4] = In[1::2]
            data = Out
            Out = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r8 a8") #TODO#
            texFmt = noesis.NOESISTEX_RGBA32
        elif platform == 0x0B or platform == 0x01 or platform == 0x04 or platform == 0x10: #DXT1 Wii U/PS3/WinPhone
            print("DXT1")
            data = bs.readBytes(dataSize)
            Out = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r8 g8 b8 a8")
            texFmt = noesis.NOESISTEX_DXT1
        else:
            data = bs.readBytes(dataSize)
            print("L8A8 OR DXT1 (WIP!)\nIf it doesn't look right, look at the below comment!")
            Out = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "l8 a8") #COMMENT THIS AND THE BELOW LINE AND REPLACE THE BELOW WITH "texFmt = noesis.NOESISTEX_DXT1" (No quotes) TO WORK WITH WII U TEXTURES#
            texFmt = noesis.NOESISTEX_RGBA32
    elif imgFmt == 0x10:
        data = bs.readBytes(dataSize)
        print("PVRTC4BPP_RGB 2")    
        data = rapi.imageDecodePVRTC(data, imgWidth, imgHeight, 4)
        texFmt = noesis.NOESISTEX_RGBA32
    #DXT5
    elif imgFmt == 0x0a:
        data = bs.readBytes(dataSize)
        print("DXT5")
        #data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r8 g8 b8 a8")
        texFmt = noesis.NOESISTEX_DXT5
    elif imgFmt == 0x0d:
        data = bs.readBytes(dataSize)
        print("AL88")
        #add to convert
        In = bytearray(data)
        Out = bytearray(2*len(data))
        for i in range(3): Out[i::4] = In[0::2]
        Out[3::4] = In[1::2]
        data = Out
        if platform == 0x03:
            Out = untile(bs.readBytes(dataSize),imgWidth,imgHeight,8,4,8)
        elif platform == 0x01:
            #data = untile(bs.readBytes(dataSize),imgWidth,imgHeight,8,8,8)
            Out = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "a8 r8") #TODO#
        else:
            Out = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r8 a8") #TODO#
        texFmt = noesis.NOESISTEX_RGBA32
    elif imgFmt == 0x0f:
        data = bs.readBytes(dataSize)
        print("PVRTC2BPP_RGB (WIP!)")
        data = rapi.imageDecodePVRTC(data, imgWidth, imgHeight, 2)
        texFmt = noesis.NOESISTEX_RGBA32
    elif imgFmt == 0x11:
        data = bs.readBytes(dataSize)
        print("PVRTC4BPP_RGB (WIP!)")
        data = rapi.imageDecodePVRTC(data, imgWidth, imgHeight, 4)
        texFmt = noesis.NOESISTEX_RGBA32
    #DXT1
    elif imgFmt == 0x18:
        data = bs.readBytes(dataSize)
        print("DXT1")
        texFmt = noesis.NOESISTEX_DXT1
    #LA44
    elif imgFmt == 0x19:
        data = bs.readBytes(dataSize)
        print("LA44")
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r4 a4")
        texFmt = noesis.NOESISTEX_RGBA32
    #DXT5
    elif imgFmt == 0x1a:
        data = bs.readBytes(dataSize)
        print("DXT5")
        texFmt = noesis.NOESISTEX_DXT5
    #PVRTC_4BPP_RGB_v3
    elif imgFmt == 0x1e:    
        data = bs.readBytes(dataSize)
        print("PVRTC4BPP_RGB (WIP!)")
        data = rapi.imageDecodePVRTC(data, imgWidth, imgHeight, 4)
        texFmt = noesis.NOESISTEX_RGBA32
    elif imgFmt == 0x1f:
        data = bs.readBytes(dataSize)
        print("PVRTC4BPP_RGBA (WIP!)")
        data = rapi.imageDecodePVRTC(data, imgWidth, imgHeight, 4)
        texFmt = noesis.NOESISTEX_RGBA32
    #ETC RGB
    elif imgFmt == 0x23:
        data = bs.readBytes(dataSize)
        data = rapi.callExtensionMethod("etc_decoderaw32", data, imgWidth, imgHeight, "rgb")
        texFmt = noesis.NOESISTEX_RGBA32
        print("ETC")
    elif imgFmt == 0xFC:
        data = bs.readBytes(dataSize)
        data = rapi.callExtensionMethod("etc_decoderaw32", data, imgWidth, imgHeight, "rgba")
        texFmt = noesis.NOESISTEX_RGBA32
        print("ETC2_RGB")
    elif imgFmt == 0xFD: #3ds only?
        data = bs.readBytes(dataSize)
        data = rapi.callExtensionMethod("etc_decoderaw32", data, imgWidth, imgHeight, "rgba")
        texFmt = noesis.NOESISTEX_RGBA32
        print("ETC1_RGB_SPLITALPHA\nWIP")
    texList.append(NoeTexture(rapi.getInputName(), imgWidth, imgHeight, data, texFmt))
    return 1
    
#added palette code and modified

def read32RGBA(pixel,width,height,tile_w,tile_h):
    real_width,real_height = getRealWH(width,height,tile_w,tile_h)
    tileSize = tile_w * tile_h * 4
    numTW = real_width // tile_w
    numTH = real_height // tile_h
    textureData = bytearray(real_width * real_height * 4)
    for y in range(0,real_height,tile_h):            
        for x in range(0,real_width,tile_w):                
            tileY_ID = y // tile_h
            tileX_ID = x // tile_w                
            dataPtr = tileY_ID * numTW * tileSize + tileSize * tileX_ID
            for ty in range(tile_h):
                for tx in range(tile_w):
                    dstIndex = (y + ty) * real_width*4 + (x + tx) * 4   
                    srcIndex = dataPtr + ty * tile_w * 2 + tx * 2
                    srcIndex2 = dataPtr + 32 + ty * tile_w * 2 + tx * 2
                    textureData[dstIndex]   = pixel[srcIndex+1]     #R
                    textureData[dstIndex+1] = pixel[srcIndex2]      #G
                    textureData[dstIndex+2] = pixel[srcIndex2+1]    #B
                    textureData[dstIndex+3] = pixel[srcIndex]       #A
    cropData = crop(textureData,real_width,real_height,width,height,32)
    return cropData

def readPalette(palFormat,palSize,bs):
    numColor = palSize // 2
    if palFormat == 0:
        palette = [ia8(bs.readUShort()) for i in range(numColor)]
    elif palFormat == 1:
        palette = [rgb565(bs.readUShort()) for i in range(numColor)]
    elif palFormat == 2:
        palette = [rgb5a3(bs.readUShort()) for i in range(numColor)]
    elif palFormat == -1:
        return 0
    else:
        print("unsupport palette format: ",palFormat)
        return 0
    return palette

def convert4to32(c4pixel,palette,width,height):
    c8pixel = bytearray(width*height)
    for i in range(width*height//2):
        index = c4pixel[i]
        id1 = (index >> 4) & 0xf
        id2 = index & 0xf
        c8pixel[i*2] = id1
        c8pixel[i*2+1] = id2  
    RGBA32Data = bytearray(width * height * 4)
    for i in range(width * height):
        RGBA32Data[i * 4:(i + 1) * 4] = palette[c8pixel[i]]         
    return RGBA32Data

def convert8to32(c8pixel,palette,width,height):
    RGBA32Data = bytearray(width * height * 4)
    for i in range(width * height):
        RGBA32Data[i * 4:(i + 1) * 4] = palette[c8pixel[i]]         
    return RGBA32Data

def convert4to8(c4pixel,real_width,real_height):
    c8pixel = bytearray(real_width*real_height)
    for i in range(real_width*real_height//2):
        index = c4pixel[i]
        id1 = (index >> 4) & 0xf
        id2 = index & 0xf
        c8pixel[i*2] = id1
        c8pixel[i*2+1] = id2
    return c8pixel

def untile(pixel,width,height,tile_w,tile_h,bpp):
    #bpp is bits per pixel
    #tile_w is tile width
    #tile_h is tile height
    real_width,real_height = getRealWH(width,height,tile_w,tile_h)
    numTileW = real_width // tile_w
    numTileH = real_height // tile_h
    lineSize = tile_w * bpp // 8
    tileSize = tile_w * tile_h * bpp // 8
    untileData = bytearray(real_width * real_height * bpp // 8)
    for y in range(numTileH):            
        for x in range(numTileW):                            
            dataPtr = y * numTileW * tileSize + tileSize * x
            for ty in range(tile_h):
                curHeight = y * tile_h + ty
                curWidth = x * tile_w
                dstIndex = (curHeight * real_width + curWidth) * bpp // 8   
                srcIndex = dataPtr + ty * lineSize
                untileData[dstIndex:dstIndex+lineSize] = pixel[srcIndex:srcIndex+lineSize]    
    cropData = crop(untileData,real_width,real_height,width,height,bpp)
    return cropData   

def crop(pixel,real_width,real_height,cropWidth,cropHeight,bpp):
    #Note: this function can't apply to 4bpp
    #for 4bpp: first convert 4bpp to 8bpp then run this function
    #Because some 4bpp array sizes are not integers.
    if real_width == cropWidth and real_height == cropHeight:
        return pixel
    minWidth = min(real_width,cropWidth)
    minHeight = min(real_height,cropHeight)
    length = cropWidth * cropHeight * bpp // 8 
    outPixel = bytearray(length)    
    dstLineSize = minWidth * bpp // 8
    srcLineSize = real_width * bpp // 8

    for y in range(minHeight):        
        dstIndex = y * dstLineSize
        srcIndex = y * srcLineSize
        outPixel[dstIndex:dstIndex+dstLineSize] = pixel[srcIndex:srcIndex+dstLineSize]
    return outPixel

def getRealWH(width,height,tile_w,tile_h):
    real_width = width
    real_height = height
    if (width%tile_w):
        real_width = (width-(width%tile_w))+tile_w            
    if (height%tile_h) :
        real_height = (height-(height%tile_h))+tile_h
    return real_width,real_height

def ia8(rawPixel):
    t = bytearray(4)
    t[0] = rawPixel & 0xFF
    t[1] = rawPixel & 0xFF
    t[2] = rawPixel & 0xFF
    t[3] = rawPixel >> 8
    return t    

def rgb565(rawPixel):
    t = bytearray(4)
    t[0] = (((rawPixel >> 11) & 0x1F) * 0xFF // 0x1F)
    t[1] = (((rawPixel >> 5)  & 0x3F) * 0xFF // 0x3F)
    t[2] = (((rawPixel >> 0)  & 0x1F) * 0xFF // 0x1F)
    t[3] = 0xFF
    return t       

def rgb5a3(rawPixel):
    t = bytearray(4)
    if (rawPixel & 0x8000) :  # r5g5b5
        t[0] = (((rawPixel >> 10) & 0x1F) * 0xFF // 0x1F)
        t[1] = (((rawPixel >> 5)  & 0x1F) * 0xFF // 0x1F)
        t[2] = (((rawPixel >> 0)  & 0x1F) * 0xFF // 0x1F)
        t[3] = 0xFF
    else:  # r4g4b4a3
        t[0] = (((rawPixel >> 8)  & 0x0F) * 0xFF // 0x0F)
        t[1] = (((rawPixel >> 4)  & 0x0F) * 0xFF // 0x0F)
        t[2] = (((rawPixel >> 0)  & 0x0F) * 0xFF // 0x0F)
        t[3] = (((rawPixel >> 12) & 0x07) * 0xFF // 0x07)
    return t    
#end