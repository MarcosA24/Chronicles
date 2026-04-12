from PIL import Image
import cv2
import numpy as np
#https://dev.to/natamacm/turn-photos-into-pixel-art-with-python-32pc#:~:text=Make%20your%20photos%20looks%20like%20pixel%20art%20using,can%20use%20the%20module%20pixelate%20to%20do%20that.
#  R'D:\RPG_games\Ilgmar\Test1\img\faces\Actor1.png'
imageName= (R'E:/CharsIcons/albedo.jpg',R'C:\Users\user\Pictures\safescreen\kieran.jpg')

def cv_image_from_PIL_image(pil_img):
    cv2_img = np.array(pil_img)
    cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_RGB2BGR)
    return cv2_img


def pixelate(input_file_path, output_file_path, pixel_size):
    image = Image.open(input_file_path)
    image = image.resize((image.size[0] // pixel_size, image.size[1] // pixel_size),Image.NEAREST)
    image = image.resize((image.size[0] * pixel_size, image.size[1] * pixel_size),Image.NEAREST)
    image.save(output_file_path)
    return image

def click_ev(ev,x,y,flags,param):
    cut= art.copy()
    if ev == cv2.EVENT_LBUTTONDOWN:
        print(x,' ',y)
        cv2.circle(cut, (x,y), radius=2, color=(0, 0, 255), thickness=4)
        cv2.imshow(window,cut)
        
    if ev == cv2.EVENT_RBUTTONDOWN:
        print(x,' ',y)
        size= (144,144)     #size of the rectangle fixed
        sq= [(x-size[0],y-size[0]),(x+size[0],y+size[0])]
        print(sq[0],sq[1])
        if x-size[0]/2>0 and x+size[0]<cut.shape[0] and y-size[1]/2>0 and y+size[1]<cut.shape[1]:
            cv2.rectangle(cut,sq[0],sq[1],(0,255,255),1)
            cv2.imshow(window,cut)
        else:
            print('Cut out of bounds')

    
def resize_scale(num=1):
    cv2.setTrackbarMax('Scale',window,25)
    cv2.setTrackbarMin('Scale',window,-25)
    num= cv2.getTrackbarPos('Scale',window)
    def scale(num):
        if num==0: pass
        if num>0: return num
        elif num<0: return -1/num
    effect= cv2.resize(img, (int(img.shape[1]*scale(num)), int(img.shape[0]*scale(num))))
    print('scale and shape:',scale(num),effect.shape)
    cv2.imshow('Effect',effect)
    
    if cv2.waitKey(0)== ord('s'): return effect
    elif cv2.waitKey(0) != ord('k'): cv2.destroyAllWindows()

def resize(img,window,shape=None,divisor=1,pixelartFace=None):
    print(shape, divisor, pixelartFace)
    #-- Resize the image ----------------------------------------------------
    if divisor!=1:
        rsz= cv2.resize(img, (int(img.shape[1]/divisor), int(img.shape[0]/divisor)))
        return rsz
    
    elif pixelartFace!=None:
        #here, we reduce the size of the image to (144,144), a measure fixated for pixelart faces in RPG maker. 
        #we divide the shape to a closer size, to later on crop the image where we exactly want, to make it square from the center that we want.
        pixelart_shape=(144,144)
        divx, divy= img.shape[0]/144, img.shape[1]/144
        print('scales',divx,' <>',divy)
        if divx>divy: 
            divisor= int(divy)-1
            rsz= cv2.resize(img, (int(img.shape[1]/divisor), int(img.shape[0]/divisor)))
            return rsz
        elif divx<divy or divx==divy: 
            divisor= int(divx)-1
            rsz= cv2.resize(img, (int(img.shape[1]/divisor), int(img.shape[0]/divisor)))
            return rsz
    elif shape!=None:
        print('shape')
        rsz= cv2.resize(img, shape)
        print(rsz.shape)
        return rsz
    else:
        cv2.imshow(window,img)
        cv2.createTrackbar('Scale', window, 1, 50, resize_scale)
        #cv2.imwrite(name+'.png',effect)#s
        
def cropSquare(img,center='',pixels=144):
    newimg= img[sq]
    return newimg
    
# --Main CODE **********************
if __name__ == '__main__':
    window='art'
    #for imN in imageName:
    name= imageName[0].split('.')[0]
    pix= pixelate(imageName[0],'pixelart.jpg',16)
    img = cv2.imread(imageName[0])
    #Only visualize the possible scale of the product.
    #art= resize(img,window)
    
    #go with the definitive slice
    #art= resize(img,window,divisor=1)
    #print(art.shape)
    cv2.imshow(window,cv_image_from_PIL_image(pix))
    #cv2.setMouseCallback(window,click_ev)
    cv2.waitKey(0)
    #print('Cut for',sq)
    #slice= cropSquare(art,sq)
    #cv2.waitKey(0)
        