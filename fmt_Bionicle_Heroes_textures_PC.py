from inc_noesis import *
import noesis
import rapi

def registerNoesisTypes():
   handle = noesis.register("Bionicle Heroes textures", ".nup")
   noesis.setHandlerTypeCheck(handle, noepyCheckType)
   noesis.setHandlerLoadRGBA(handle, BioHLoadRGBA)
   handle = noesis.register("Bionicle Heroes textures", ".hgp")
   noesis.setHandlerTypeCheck(handle, noepyCheckType)
   noesis.setHandlerLoadRGBA(handle, BioHLoadRGBA)

   noesis.logPopup()
   return 1

def noepyCheckType(data):
	return 1

def getFormat(dxtInfo):
	if dxtInfo == 0x33545844:
		dxtFormat = noesis.NOESISTEX_DXT3
		print ("DXT3")
	else:
		dxtFormat = noesis.NOESISTEX_DXT5
		print ("DXT5")
	return dxtFormat

def BioHLoadRGBA(data, texList):
	texCount = 0
	bs = NoeBitStream(data)
	filesize = bs.getSize()
	filesizeDiv4 = filesize//4
	for i in range(0, filesizeDiv4-1):
		Temp = bs.readInt()

		if (Temp == 0x0020534444):
		    texCount += 1
		    print(texCount)
		    offset = bs.tell()
		    print ("Found Texture header at: " + hex(offset - 0x04))
		    bs.seek(0x08, NOESEEK_REL)
		    height = bs.readInt()
		    width = bs.readInt()

		    print ("Height: " + str(height))
		    print ("Width: " + str(width))

		    bs.seek(0x08, NOESEEK_REL)
		    mipCount = bs.readInt()
		    print ("MipMaps: " + str(mipCount))
		    bs.seek(0x34, NOESEEK_REL)
		    dxtHeader = bs.readInt()

		    bs.seek(0x28, NOESEEK_REL)
		    dataStart = bs.tell()
		    print ("Texture data start at: " + hex(dataStart))
		    img = rapi.imageDecodeDXT(bs.readBytes(width*height), width, height, getFormat(dxtHeader))
		    texList.append(NoeTexture(str(i), width, height, img, noesis.NOESISTEX_RGBA32))
	return 1
