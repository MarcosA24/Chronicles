# coding= UTF-8
import sys
import numpy as np
import pandas as pd
import warnings
import Omni
from Mementos_au import ExcelExport, ExcelOpen

#supress Future warning messages in cmd. For the pandas pd.mask 
warnings.simplefilter(action='ignore', category=FutureWarning)

workspace= R'C:\Users\Documents\0_simbologia'

def reformulacio(df, reformulacio, common_field, method):
    new_formulacio= pd.merge(df, reformulacio, on=common_field, how=method)
    #print('EPIGRAFS_JOIN:\n', new_formulacio.shape)
    select_old= new_formulacio.loc[new_formulacio['EPI_DGN_NOU'].isnull()]
    select_new= new_formulacio.loc[new_formulacio['EPI_DGN_NOU'].notnull()]
    #print(' Antics EPIGRAFS\n', select_old.shape)
    #print(' NOUS EPIGRAFS:\n', select_new.shape)
    
    #create a new column where the ANTIC and the NOU are mixed
    new_formulacio['EPI_DGN_ACTUAL']= np.where(new_formulacio['EPI_DGN_NOU'].notnull, new_formulacio['EPI_DGN_NOU'],new_formulacio['EPI_DGN_ANTIC'])    # update values from column where is not null in the original
    new_formulacio['EPI_DGN_ACTUAL'].mask(pd.isnull, new_formulacio['EPI_DGN_ANTIC'], inplace=True)                                                     # where the new column is null, take values of another column
    updated= new_formulacio
    #print('UPDATED:\n',updated.columns)
    return updated

def MetaMorfismes_prefix(xl_pdf):
            # rename the prefix of the morphisms in the EPI_PDF column
            morfismes= xl_pdf['EPI_ACTUAL'][xl_pdf['EPI_ACTUAL'].str.startswith('M')==True]   #filter the morphisms and use the blank spaces to split the codes
            morph= morfismes.str.split(pat=' ', n=-1, expand=True)                             #split the codes using blankspaces
            morph['EPI_ACTUAL']= morfismes
            
            split3= morph.loc[morph[2].notnull()]                                             
            pref3= split3[0]+split3[1].str.strip('M')                   # CODIS of 3 splits   MC MRac Oz -> mcrac_Oz 
            morph['CODI_morf']= pref3.str.lower()+'_'+morph[2]

            split2= morph.loc[morph[1].notnull()]                       # CODIS of 2 splits   MR Gnl  -> gmr_Gnlg
            pref2= split2[0].str.lower()
            morph['CODI_morf'].mask(pd.isnull, pref2+'_'+split2[1],inplace=True)   

            split1= morph.loc[morph[1].isnull()]                       # CODIS of 1 split   M  -> M
            morph['CODI_morf'].mask(pd.isnull, split1[0], inplace=True)
            codi_morfismes= morph[['EPI_ACTUAL','CODI_morf']]

            # update the new morphism CODIS
            mp= pd.merge(xl_pdf,codi_morfismes,how='left',on='EPI_ACTUAL')
            select_m= mp.loc[mp['CODI_morf'].notnull()]
            #print('metaMORFISMES:', select_m.shape)
            mp['EPI_ACTUAL']= np.where(mp['CODI_morf'].notnull(), mp['CODI_morf'],mp['EPI_ACTUAL'])    
            return mp

if __name__ == "__main__":

    Step0 = True        # STEP 0 ----------------open all the files that are to be inspected
    Step1= True         # STEP 1 ----------------change the codification of the EPIGRAFS according to the new EPI_DGN_NOU from the reformulacio dataframe
    Step2= True         # STEP 2 ----------------prepare comparison between pdf and xlsx and lyrx. apply changes of EPIGRAFS and join all the CMYK codes in 1 field, separated by blankSpace.
    Step3= True        # STEP 3 ----------------filter codes of ArcGis Layer. 853 rows to compare
    Step4= True        # STEP 4 ----------------compare between xlsx and pdf color codes. 
    Step5= True        # STEP 5 ----------------compare the result mix of Step4 with ArcGis lyrx
    Step6= False        # STEP 6 ----------------extract Result with definitive UPDATED COLORS 

# STEP 0 ----------------open all the files that are to be inspected
    if Step0==True:
    #--------------------------- Open excel files
    # xl_univers contains the reformulation that occured from the old_codes to the new_codes
        #old_codes are shown in the pdf, or .txt 
        # new-codes are shown in the .lyrx, which are currently in use for the visor
        # the difference is that the news include the eonotema era of geological layers, and they have an added sufix.
        
        xl_reformulacio= ExcelOpen(R'C:\Users\becari.alex.marcos\OneDrive - Institut Cartogràfic i Geològic de Catalunya\visor_geologia\CONSULTA_UNIVERS_v3.xlsx',sheet='TBL_REFORMULACIO')[0]
        xl_estil= ExcelOpen(R'C:\Users\becari.alex.marcos\OneDrive - Institut Cartogràfic i Geològic de Catalunya\visor_geologia\MGC_TBL_ESTIL_POL.xlsx',sheet='GT1_pol')[0]
        xl_est_pol= xl_estil[['EPIGRAF (EPI_BASE)','C','M','Y','K','Codi pattern','COMENTARIS']]
        print('REFORMULACIO.xlsx, MGC_TBL_ESTIL_POL.xlsx\n',xl_reformulacio.shape, xl_est_pol.shape)

        #read the xlsx with arcgis colors codification
        #xl_basam= ExcelOpen(R'C:\Users\becari.alex.marcos\OneDrive - Institut Cartogràfic i Geològic de Catalunya\visor_geologia\arcgisCMYK.xlsx',sheet='colors')[0]
        xl_basam= ExcelOpen(R'C:\Users\becari.alex.marcos\OneDrive - Institut Cartogràfic i Geològic de Catalunya\visor_geologia\ArcGis_CMYK_quat.xlsx',sheet='ArcGis_CMYK')[0]
        print('arcgisCMYK\n',xl_basam.shape)
        # 853 codigos a revisar. hay que comparar con los codigos del excel y los del pdf, y contrastar los CMYK

        #read the xlsx from the pdf
        xl_pdf= ExcelOpen(R'C:\Users\becari.alex.marcos\OneDrive - Institut Cartogràfic i Geològic de Catalunya\visor_geologia\pdf_codes.xlsx',sheet='CD_TOT')[0]
        #xl_pdf2= ExcelOpen(R'C:\Users\becari.alex.marcos\OneDrive - Institut Cartogràfic i Geològic de Catalunya\visor_geologia\pdf_codes.xlsx',sheet='cd2')[0]
        
        #filter all rows where check == 1 
        xl_pdf= xl_pdf[xl_pdf['check'] == 1].iloc[:,:7]
        #print('$----- pdf_[:50]\n',xl_pdf.head(5))
        print('pdf\n', xl_pdf.shape)

    if Step1==True:
        print('----------pdf: BEFORE ', xl_pdf.shape)
        xl_pdf= reformulacio(xl_pdf,xl_reformulacio,common_field='EPI_DGN_ANTIC',method='left')
        xl_pdf.rename(columns={'EPI_DGN_ANTIC':'EPI_PDF', 'EPI_DGN_ACTUAL':'EPI_ACTUAL'},inplace=True)
        print('pdf: UPDATED ', xl_pdf.shape)
        
        print('----------xl_est_pol: BEFORE ', xl_est_pol.shape)
        xl_est_pol.rename(columns={'EPIGRAF (EPI_BASE)':'EPI_DGN_ANTIC'},inplace=True)   #renombrar columna per tal de referir-nos al camp comú
        xl_est_pol= reformulacio(xl_est_pol,xl_reformulacio,common_field='EPI_DGN_ANTIC',method='left')
        xl_est_pol.rename(columns={'EPI_DGN_ANTIC':'EPIGRAF (EPI_BASE)', 'EPI_DGN_ACTUAL':'EPI_ACTUAL'},inplace=True)
        print('xl_est_pol: UPDATED ', xl_est_pol.shape)

        print('----------xl_basam: BEFORE ', xl_basam.shape)
        xl_basam.rename(columns={'_attr_value':'EPI_DGN_ANTIC'},inplace=True)   #renombrar columna per tal de referir-nos al camp comú
        xl_basam= reformulacio(xl_basam,xl_reformulacio,common_field='EPI_DGN_ANTIC',method='left')
        xl_basam.rename(columns={'EPI_DGN_ANTIC':'_attr_value', 'EPI_DGN_ACTUAL':'EPI_ACTUAL'},inplace=True)
        print('xl_basam: UPDATED ', xl_basam.shape)

        #second part of renaming the columns, following the FME process. rename the CODIS. only for the pdf  
        xl_pdf['EPI_ACTUAL']= xl_pdf['EPI_ACTUAL'].str.replace(' (', '_')     # change 'codi (*)' for codi_*
        xl_pdf['EPI_ACTUAL']= xl_pdf['EPI_ACTUAL'].str.replace(')', '')

        xl_pdf_ref= MetaMorfismes_prefix(xl_pdf)

    if Step2==True:
        #column 'color' in the xl_basam is the merge of the 4 columns: C,M,Y,K        
        for index,row in xl_basam.iterrows():
            color= '%d %d %d %d' %(xl_basam.loc[index]['_attr_valueC'],xl_basam.loc[index]['_attr_valueM'],xl_basam.loc[index]['_attr_valueY'],xl_basam.loc[index]['_attr_valueK'])
            xl_basam.loc[index,'color']= color
        #colorCMYK is the merge column for the xl_estils
        for index,row in xl_est_pol.iterrows():
            color= '%s %s %s %s' %(xl_est_pol.loc[index]['C'],xl_est_pol.loc[index]['M'],xl_est_pol.loc[index]['Y'],xl_est_pol.loc[index]['K'])
            xl_est_pol.loc[index,'colorCMYK']= color
        xl_est_pol['colorCMYK']= xl_est_pol['colorCMYK'].str.replace('.0','')

        #split the CMYK of the xl_pdf in 4 columns C,M,Y,K
        splitCMYK1= xl_pdf_ref['colorFondo'].str.split(pat=' ', n=-1, expand=True)[[0,1,2,3]]

        for index,row in xl_pdf_ref.iterrows():
            xl_pdf_ref.loc[index,'C']= int(splitCMYK1.loc[index,0])
            xl_pdf_ref.loc[index,'M']= int(splitCMYK1.loc[index,1])
            xl_pdf_ref.loc[index,'Y']= int(splitCMYK1.loc[index,2])
            xl_pdf_ref.loc[index,'K']= int(splitCMYK1.loc[index,3])


    if Step3==True:  
        arc_basam= xl_basam.drop_duplicates(subset=['EPI_ACTUAL'],keep='first')
        print('Arc_basam:',arc_basam.shape)
        arc_pdf= xl_pdf_ref.merge(xl_basam,how='inner', on='EPI_ACTUAL')[['id1','EPI_PDF','colorFondo','colorTrama','EPI_ACTUAL',
                                                                            'C','M','Y','K','id']]
        print('Arc_pdf:',arc_pdf.shape)      

        arc_estils= xl_est_pol.merge(xl_basam,how='right', on='EPI_ACTUAL')[['EPIGRAF (EPI_BASE)','C','M','Y','K','colorCMYK','EPI_ACTUAL',
                                                                            'id','COMENTARIS']]
        #eliminar duplicates of EPIS, to make the excel have exactly 853 rows, instead of 969.  116 duplicates values
        arc_estils= arc_estils.drop_duplicates(subset=['EPI_ACTUAL'],keep='first')
        print('Arc_estils:\n',arc_estils.shape)

    if Step4==True:
        mix_colors= pd.merge(arc_pdf,arc_estils,how='right',on='EPI_ACTUAL')
        #select= mix_colors[mix_colors['colorFondo'].notnull()]        #select the colorsPDF if there is or not. to see how many of each source is inherited.
        mix_colors['CMYK_check']= np.where(mix_colors['colorFondo'].notnull(),mix_colors['colorFondo'],mix_colors['colorCMYK'])
        mix_colors['origen']= np.where(mix_colors['colorFondo'].notnull(),'pdf','xlsx')
        mix_colors['origen'].mask(mix_colors['CMYK_check'].isnull(), 'arcGis', inplace=True) 
        
        selectex= mix_colors[mix_colors['origen']=='xlsx']
        selectpd= mix_colors[mix_colors['origen']=='pdf']
        select_null= mix_colors[mix_colors['CMYK_check'].isnull()]
        print('Heredar del pdf y excel:',selectex.shape, selectpd.shape, select_null.shape)

        #print('\nestils:\n',selectex, '\nPDF:\n',selectpd, '\nArcGis nuevos:\n',select_null)

    if Step5==True:
        arc_definitive= pd.merge(arc_basam,mix_colors,how='left',on='EPI_ACTUAL')[['_attr_value','EPI_ACTUAL','color','EPI_PDF','colorFondo','colorTrama','EPIGRAF (EPI_BASE)','colorCMYK','CMYK_check','origen']]
        arc_definitive['CMYK_final'] = np.where(arc_definitive['CMYK_check'].notnull(), arc_definitive['CMYK_check'], arc_definitive['color'])
        #arc_definitive.rename(columns={'color':'col_arcgis','colorFondo':'col_PDF','colorCMYK':'col_excel'}, inplace=True)
        #select= arc_definitive[arc_definitive['CMYK_final']==arc_definitive['color']]        #select the colorsPDF if there is or not. to see how many of each source is inherited.
    
        splitCMYK= arc_definitive['CMYK_final'].str.split(pat=' ', n=-1, expand=True)[[0,1,2,3]]
        for index,row in arc_definitive.iterrows():
            arc_definitive.loc[index,'C']= int(splitCMYK.loc[index,0])
            arc_definitive.loc[index,'M']= int(splitCMYK.loc[index,1])
            arc_definitive.loc[index,'Y']= int(splitCMYK.loc[index,2])
            arc_definitive.loc[index,'K']= int(splitCMYK.loc[index,3])
        arc_definitive= arc_definitive.drop_duplicates(subset=['EPI_ACTUAL'], keep='first')
        s= arc_definitive[arc_definitive['color']!=arc_definitive['CMYK_final']]
        
        ExcelExport(arc_definitive,R'C:\Users\becari.alex.marcos\Documents\Alex\py_carto\geologia_visor\ArcDefinitive_quat.xlsx',hoja='actualizado')

    if Step6==True:
        pass

       
        
