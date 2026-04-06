# coding= UTF-8
import sys, os, cv2, img2pdf
import matplotlib.pyplot as mpt
import numpy as np
import pandas as pd
from PIL import Image

def pdfPlotter(img_path, pdf_path): #convert image file to pdf
    im= Image.open(img_path)
    pdf_bytes= img2pdf.convert(im.filename)
    file= open(pdf_path,"wb")
    file.write(pdf_bytes)
    im.close()
    file.close()
    
    
#display coordinates of points clicked on image
def click_ev(ev,x,y,flags,param,img):
    #check left mouse click occurs
    if ev == cv2.EVENT_LBUTTONDOWN:
        #display on shell
        print(x,' ',y)
        #diisplay on image window
        cord= cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,str(x)+','+str(y),(x,y),cord,1,(255,0,0),2)
        cv2.imshow('left',img)
    #checking right click
    if ev == cv2.EVENT_RBUTTONDOWN:
        print(x,' ',y)
        cord= cv2.FONT_HERSHEY_SIMPLEX
        b=img[y,x,0]
        g=img[y,x,1]
        r=img[y,x,2]
        cv2.putText(img,str(b) +','+str(g)+','+str(r),(x,y),cord,1,(255,255,0),2)
        cv2.imshow('right',img)

#sir = cv2.imread('C:\Users\Usuario\Documents\Artworks\Volo_color2.jpg')
def displayImage(sir):
    mpt.imshow(sir)
    mpt.show()

#cam= cv2.VideoCapture(0)
def videoRealT(cam):
    if not cam.isOpened():
        print('noVid')
        exit(0)
    
    while True:
        ret, frame = cam.read()
        if not ret:
            print('noframe')
            break
        cv2.imshow('videoC',frame)
        if cv2.waitkey(1) == ord('q'):
            break

def resizeimage(img):
    amplada, altura, canals= img.shape
    pop = len(img.shape)
    if pop ==3:
        amplada,altura,canals
    else: 
        amplada,altura= img.shape   
    imr= cv2.resize(img,(altura//6,amplada//6))

def FiltColour(img):
    b, g, r= cv2.split(img)
    ired0= [[[0,0,255%j]for j in i]for i in r]
    ired= [[[255%j,255%j,j]for j in i]for i in r]
    dt = np.dtype('f8')
    ired0= np.array(ired,dtype=dt)
    ired= np.array(ired0,dtype=dt)
    cv2.imwrite('red0',ired0)

def wordIns(file, word):  #checks if the words is in the .txt 
    with open(file, 'r') as ori:
        for horn in ori.readlines():            
            horn=horn.replace(',','',-1)
            hornL=horn.split()
            head= hornL[0]
            for c in horn:       
                if head == word:
                    if len(hornL) <2:
                        head = (word,'No Index')
                        break
                    elif len(hornL) >=2: 
                        zane = int(hornL[2])
                        Kel= '%4d' %(zane)
                        return Kel
                else: 
                    break

def csvIns(file,word):
    with open(file, 'r') as ori:
        for horn in ori.readlines():        
            hornL=horn.split()
            head= hornL[0]
            if head == word:
                if len(hornL) == 2: 
                    zane = float(hornL[1])
                    Kel= '%4d' %(zane)
                    return Kel
                else: 
                    return (word,'No Index')
                    


def neighbours(matrix='',central='',image=''): #it gets the neighbouring pixels of the chosen one, that works as the central pixel.
        #els valors de matrix és depenent de quant vols que sigui la matriu de veïns..
        #només esta fet per 3: 3x3 i 9: 9x9.
        #central és una tupla de (row,columns), maracat el pixel central
        ND=[]
        pos=[]
        for l in range(0,matrix):
            cLin=central[1]+(-1+l)
            for c in range(0,3):
                cCol=central[0]+(c-1)
                pos+=[(cLin,cCol)]
    #ND posicions veïnes 'matrix'x'matrix'
        placeC=[x[0] for x in pos]
        placeL=[x[1] for x in pos]
        for d in range(0,len(pos)): 
            Level= image[placeL[d],placeC[d]]
            ND+=[Level]
        return ND   

def selectRGB(nchannels='',ig=''): #it extracts the RGB channels of an image, to make it visible
    img = ig.copy()
    img = img.astype(dtype=np.float32)
    for c in range(nchannels-3,nchannels):
        minim= img[c].min()
        maxim= img[c].max()
        img[c]= (img[c]-minim)/(maxim-minim)
        #cv2.imshow('channels',img[c])
        #cv2.waitKey(0)
    b = np.array(img[0])
    g= np.array(img[1])
    r = np.array(img[2])
    newRGB = cv2.merge((b,g,r))
    return newRGB

def editHSV(ig='',sat='',value=30): #it adjusts the image via HSV channels to make it more visible
    ig = ig
    imghsv = cv2.cvtColor(ig, cv2.COLOR_BGR2HSV).astype(dtype=np.float32)
    h,s,v = cv2.split((imghsv))
    #changing saturation
    adjust= sat/100
    s = s*adjust
    s = np.clip(s,0,255)
    #changing value, or brightness
    #lim = 255 - value
    #v[v > lim] = 255
    #v[v <= lim] += value
    final_hsv = cv2.merge((h, s, v)).astype(dtype=np.uint8)
    enhanced_ig = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return enhanced_ig

def doHisto(ig='',size=''): #plot histograms related to the image. Nivells digitals, npixels
    #the size parameter is the shape of the image.we will use those for later
    #definir els histogrames abans del bucle de les 3 bandes
    histo=cv2.calcHist([ig],[0],None,[256],[0,256])
    histo= [int(i) for i in histo]
    fig,ax= plt.subplots(1,3,figsize=(12,4))
    #paleta de colors per cambiar els gràfics
    raoul= ['blue','green','red','blue','gray','purple']

    for b in range(size[2]):
        histo[b]= cv2.calcHist([ig[b]],[0],None,[256],[0,256])
        x= [int(i) for i in range(256)]
        sea= b

        x_data= np.reshape(x,(len(histo[b]),))
        y_data= np.reshape(histo[b],(len(histo[b]),))
        
        ax[sea].bar(x_data,y_data,color= raoul[b])
        ax[sea].set_title('band'+str(b+1))

def combinator3channels(canals):
    combos = np.zeros(canals*(canals-1),canals)
    for c in range(canals-2):
        for j in range(c+1,canals):
            for i in range(j+1,canals):
                np.append(combos,(c,i,j),3)

def OpenBighorn(imatge_spectral,headers):
    horn= open(headers)
    horn= horn.readlines()
    '''
    def wordIns(file, word):
        with open(file, 'r') as ori:
            for horn in ori.readlines():            
                horn=horn.replace(',','',-1)
                hornL=horn.split()
                head= hornL[0]
                for c in horn:       
                    if head == word:
                        if len(hornL) <2:
                            head = (word,'No Index')
                            break
                        elif len(hornL) >=2: 
                            zane = int(hornL[2])
                            Kel= '%4d' %(zane)
                            return Kel
                    else: 
                        break
            '''
    #assignació de caracterí stiques de la imatge llegint els headers. 
    ncols= int(wordIns(headers,word='samples'))
    rows = int(wordIns(headers,word='lines'))
    bands = int(wordIns(headers,word='bands')) 
    #rb, llegir numeros com a binari
    f = open(imatge_spectral,'rb')
    ig = np.fromfile(f,dtype=np.uint8, count=ncols*rows*bands)
    f.close()
    ig= ig.reshape((bands,rows,ncols))
    measures= (bands, rows, ncols)
    return ig

#open any kind of file with pandas
def opSesame(route,separator='',sheet='',head=''):
    if route.endswith('.txt') or route.endswith('.ASC') or route.endswith('.csv'):
        estadillo= pd.read_csv(route,sep=separator,header=[0],index_col=None)
        estadillo= estadillo.replace(',','.', regex=True)
        return estadillo
    elif route.endswith('.xlsx'):
        if not sheet:
            sheet= input('Sheet_Name: ')
        if not head:
            head= int(input('Nºlines of headers(int)'))
        headers=[]
        for r in range(head):
            headers.append(r)
        estadillo= pd.read_excel(route,sheet_name=sheet,header=headers,names=None)
        estadillo= estadillo.replace(',','.', regex=True)
        return estadillo
    else:
        print('File type does not exist')


#Pandas tutorials:
#pandas create dataframe from zero


#pandas indexing
    #row indexing: estadillo.loc[0])  
    #col indexing:estadillo[['Estacion','PuntoVisado']]) 
    #print(trigEst.loc[0]['Slope']) 
    
#print the first 10 rows and 10 cols
    #df.iloc[:,:10].head(10))
#Pandas iterate over rows. -> 
            #for index, row in df.iterrows():
                #print(row['c1'], row['c2'])
                #print(dex.loc[index]['c1'])
                #print(row.to_frame().T)  # print horizontally
#Pandas iterate over columns:| 
            #for column in dLect.columns:
                #print(dLect[column])
#pandas to numpy array specific column:
#column_to_numpy = df['col1'].to_numpy()
#pandas change type of a column(2 options):
    #estadillo= estadillo.astype({'ESPALDA':float,'FRENTE':float})
    #estadillo[['ESPALDA', 'FRENTE']] = estadillo[['ESPALDA', 'FRENTE']].apply(pd.to_numeric)
#pandas export df to excel:
    #with pd.ExcelWriter('C:/Users/Usuario/Documents/Crossroads/AjustesRed/Nivel_pr.xlsx') as writer:
        #nivEst.to_excel(writer)
    #df.to_excel()
#pandas dataframe sort:
    #df.sort_values(by=['column'], ascending='True/False' , na_position= 'first'/'last')
    #natural sort with the key argument ; key =lambda x: np.argsort(index_natsorted(df['column']))
#pandas replace values:
    # for column
        #df['column'] = df['column'].replace(np.nan, 0)
    # for whole dataframe
        #df = df.replace('','') # replaces only the cells that completely match the character
        #df = df.replace('','', regex=True)  # replaces all characters of dataframe, also substring of a cell
    # inplace
        #df.replace(np.nan, 0, inplace=True)
    # using a loop, row by row and with loc to assign a value for only a column of the row. 
        #for index,row in ages.iterrows():
            #row['coln']= 1
            #df.loc[index, 'coln']= row['coln']
#pandas insert new rows:
    #df.loc['col'] = pd.Series({'c1':1, 'c2':5, 'c3':2})
#pandas get unique values of a whole dataframe, specifying each column: 
    #tp= pd.Series({c: df[c].unique() for c in df})
    
#pandas where clause SQL:
        #select= df[xdf['col_name'] == 1]

#pandas search for string values for each row
    #for index, row in panda.iterrows():
     #       if 'Vulcanisme' in row['line']:
      #          print(index,row['line'])
