# coding=utf-8
__author__ = 'nacho'


import re
import os
import shutil
from lxml import etree
from django.template import Template, Context
from django.conf import settings
from datetime import date

class bCore:
    def __init__(self,parametros):

        self.maxnum=0
        # Almacenan los items importados del XML
        self.itemsES=[]
        self.itemsEN=[]
        # Lista de diccionarios
        #
        # 'itemES' 'itemEN' 'pos'
        self.elementos=[]
        self.anio=-1
        self.dia=-1
        self.mes=-1
        self.parametros=parametros

        self.posNot=0
        self.posDoc=0
        self.posEve=0
        self.posRef=0

        settings.configure()


    def cargaBoletines(self,nombre):

        del self.elementos[:]
        path=self.parametros.dirxml
        self.nombreEs=os.path.join(path,nombre+'.xml')
        self.nombreEn=os.path.join(path,nombre+'-en.xml')

        # Esto tiene que ver con el pretty_print
        parser = etree.XMLParser(remove_blank_text=True)

        self.xmlDataEs=etree.parse(self.nombreEs,parser)
        self.xmlDataEn=etree.parse(self.nombreEn,parser)

        self.itemsES=self.xmlDataEs.findall("//item")
        self.itemsEN=self.xmlDataEn.findall("//item")

        for es,en in zip(self.itemsES,self.itemsEN):
            self.appendItem(es,en)

        fecha=self.xmlDataEn.findtext('fecha')
        e=re.match('(.+) (\d+)\, (\d+)',fecha,re.M|re.I)
        self.anio=e.group(3)
        self.dia=e.group(2)
        self.id=self.xmlDataEn.findtext('id')
        m=e.group(1)
        mesEN=('January','February','March','April','May','June','July','August','September','October','November','December')
        i=0
        for i in range(12):
            if (mesEN[i]==m):
                self.mes=i+1
                break

    def appendItem(self,en,es):
        e={}
        tipo=en.find('tipo').text
        if tipo=='noticia':
            pos=self.posNot
            self.posNot+=1
        elif tipo=='documento':
            pos=self.posDoc
            self.posDoc+=1
        elif tipo=='evento':
            pos=self.posEve
            self.posEve+=1
        else: # tipo=='reflexion'
            pos=self.posRef
            self.posRef+=1
            en.find('titulo').text="Reflexion "+str(self.posRef)

        posi=es.findtext('pos')
        if (posi==None):
            text="<pos>"+str(pos)+"</pos>"
            en.append(etree.fromstring(text))
            es.append(etree.fromstring(text))
        e['itemES']=es
        e['itemEN']=en
        self.elementos.append(e)

    def nuevoBol(self,datos):
        mesES=('enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre')
        mesEN=('January','February','March','April','May','June','July','August','September','October','November','December')

        self.posNot=0
        self.posDoc=0
        self.posEve=0
        self.posRef=0

        self.id=datos['id']
        self.dia=datos['dia']
        self.mes=datos['mes']
        self.stringMesES=mesES[int(datos['mes'])-1]
        self.stringMesEN=mesEN[int(datos['mes'])-1]
        self.anio=datos['anio']
        stringFechaES=self.dia+" de "+self.stringMesES+" de "+self.anio
        stringFechaEN=self.stringMesEN+" "+self.dia+", "+self.anio

        path=self.parametros.dirxml
        nombre="boletin"+self.id
        self.nombreEs=os.path.join(path,nombre+'.xml')
        self.nombreEn=os.path.join(path,nombre+'-en.xml')

        rootES=etree.Element("boletin")
        ident=etree.SubElement(rootES,"id")
        ident.text=self.id
        fecha=etree.SubElement(rootES,"fecha")
        fecha.text=stringFechaES

        rootEN=etree.Element("boletin")
        ident=etree.SubElement(rootEN,"id")
        ident.text=self.id
        fecha=etree.SubElement(rootEN,"fecha")
        fecha.text=stringFechaEN

        s=etree.tostring(rootES,pretty_print=True)
        fp=file(self.nombreEs,'w')
        fp.write(s)
        fp.close()
        s=etree.tostring(rootEN,pretty_print=True)
        fp=file(self.nombreEn,'w')
        fp.write(s)
        fp.close()

        self.cargaBoletines(nombre)

    def item(self,titulo):
        """ recibe el titulo  del elemento
            retorna 2-tupla con el elemento EN y el ES
        """
        EN=[]
        ES=[]
        num=0
        for item in self.elementos:
            t=item['itemEN'].find('titulo').text
            if (titulo==t):
                numBuscado=num
                break
            num+=1

        EN=self.elementos[num]['itemEN']
        ES=self.elementos[num]['itemES']
        return [EN,ES,num]

    def nuevoItem(self,itemEN,itemES):
        num=len(self.elementos)

        tipo=itemEN['tipo']
        if tipo=='noticia':
            pos=self.posNot
            self.posNot+=1
        elif tipo=='documento':
            pos=self.posDoc
            self.posDoc+=1
        elif tipo=='evento':
            pos=self.posEve
            self.posEve+=1
        else: # tipo=='reflexion'
            pos=self.posRef
            self.posRef+=1

        elementoEN=etree.Element("item")
        ident=etree.SubElement(elementoEN,"titulo")
        ident.text=itemEN['titulo']
        ident=etree.SubElement(elementoEN,"texto")
        ident.text=itemEN['texto']
        ident=etree.SubElement(elementoEN,"link")
        ident.text=itemEN['link']
        ident=etree.SubElement(elementoEN,"tag")
        ident.text=itemEN['tag']
        ident=etree.SubElement(elementoEN,"tipo")
        ident.text=itemEN['tipo']
        ident=etree.SubElement(elementoEN,"pos")
        ident.text=str(pos)
        self.xmlDataEn.getroot().insert(num+2,elementoEN)

        elementoES=etree.Element("item")
        ident=etree.SubElement(elementoES,"titulo")
        ident.text=itemES['titulo']
        ident=etree.SubElement(elementoES,"texto")
        ident.text=itemES['texto']
        ident=etree.SubElement(elementoES,"link")
        ident.text=itemES['link']
        ident=etree.SubElement(elementoES,"tag")
        ident.text=itemES['tag']
        ident=etree.SubElement(elementoES,"tipo")
        ident.text=itemES['tipo']
        ident=etree.SubElement(elementoES,"pos")
        ident.text=str(pos)
        self.xmlDataEs.getroot().insert(num+2,elementoES)

        self.itemsES=self.xmlDataEs.findall("//item")
        self.itemsEN=self.xmlDataEn.findall("//item")

        self.appendItem(elementoEN,elementoES)

    def updateItem(self,itemEN,itemES,num):
        """ actualiza los XML de un item
        """
        item=self.elementos[num]['itemEN']
        item.find('tipo').text=itemEN['tipo']
        #item.find('pos').text=itemEN['pos']
        item.find('texto').text=itemEN['texto']
        if (itemEN['tipo']<>"reflexion"):
            item.find('titulo').text=itemEN['titulo']
            item.find('tag').text=itemEN['tag']
            item.find('link').text=itemEN['link']
        item=self.elementos[num]['itemES']
        item.find('tipo').text=itemES['tipo']
        #item.find('pos').text=itemES['pos']
        item.find('texto').text=itemES['texto']
        if (itemES['tipo']<>"reflexion"):
            item.find('titulo').text=itemES['titulo']
            item.find('tag').text=itemES['tag']
            item.find('link').text=itemES['link']



    def updateFiles(self,posiciones):
        """
        Espera una lista con items ('num','pos')
        Incorpora el campo pos a cada elemento
        """
        path=self.parametros.dirxml
        nombre="boletin"+self.id
        self.nombreEs=os.path.join(path,nombre+'.xml')

        nombreorig=os.path.join(path,nombre+'.xml')
        nombredest=os.path.join(path,nombre+'.bak')
        shutil.copy(nombreorig,nombredest)

        nombreorig=os.path.join(path,nombre+'-en.xml')
        nombredest=os.path.join(path,nombre+'-en.bak')
        shutil.copy(nombreorig,nombredest)

        copia_pos=list(posiciones)
        num=0
        for item in self.itemsEN:
            for i in posiciones:
                if (i['num']==num):
                    p=i['pos']
                    #pos=item.findtext('pos')
                    for x in item:
                        if x.tag=='pos':
                            #item.find('pos').text=p
                            x.text=str(p)
                            break
                    else:
                        text="<pos>"+str(p)+"</pos>"
                        item.append(etree.fromstring(text))
                    posiciones.remove(i)
                    break
            num+=1
        posiciones=copia_pos
        num=0
        for item in self.itemsES:
            for i in posiciones:
                if (i['num']==num):
                    p=i['pos']
                    #pos=item.findtext('pos')
                    for x in item:
                        if x.tag=='pos':
                            #item.find('pos').text=p
                            x.text=str(p)
                            break
                    else:
                        text="<pos>"+str(p)+"</pos>"
                        item.append(etree.fromstring(text))
                    posiciones.remove(i)
                    break
            num+=1


        s=etree.tostring(self.xmlDataEs.getroot(),pretty_print=True)
        fp=file(self.nombreEs,'w')
        fp.write(s)
        fp.close()
        s=etree.tostring(self.xmlDataEn.getroot(),pretty_print=True)
        fp=file(self.nombreEn,'w')
        fp.write(s)
        fp.close()

        self.renderHTML('EN')
        self.renderHTML('ES')


    def renderHTML(self,idioma):

        noticias=[]
        documentos=[]
        eventos=[]
        reflexiones=[]

        items=[]
        i={}

        path=self.parametros.dirconf
        d=date(int(self.anio),int(self.mes),int(self.dia))
        filedate=d.strftime('%Y%m%d')

        if (idioma=='EN'):
            self.tag_enlace="Link"
            self.plantilla=os.path.join(path,self.parametros.plantillaen)
            self.fecha=self.xmlDataEn.findtext('fecha')
            self.id=self.xmlDataEn.findtext('id')
            self.output="Boletin-"+filedate+"-en.html"
        else:
            self.tag_enlace="Enlace"
            self.plantilla=os.path.join(path,self.parametros.plantillaes)
            self.fecha=self.xmlDataEs.findtext('fecha')
            self.id=self.xmlDataEs.findtext('id')
            self.output="Boletin-"+filedate+".html"

        for o in self.elementos:
            if idioma=='EN':
                j=o['itemEN']
            else:
                j=o['itemES']

            i={}
            i['titulo']=j.findtext('titulo')
            i['texto']=j.findtext('texto')
            i['link']=j.findtext('link')
            i['tipo']=j.findtext('tipo').lower()
            i['pos']=int(j.findtext('pos'))

            tipo=i['tipo']

            if tipo == "noticia":
                noticias.append(i)
            elif tipo == "documento":
                documentos.append(i)
            elif tipo == "evento":
                eventos.append(i)
            elif tipo == "reflexion":
                reflexiones.append(i)
        noti=[i for i in sorted(noticias,key=lambda k: k['pos'])]
        docu=[i for i in sorted(documentos,key=lambda k: k['pos'])]
        refl=[i for i in sorted(reflexiones,key=lambda k: k['pos'])]
        even=[i for i in sorted(eventos,key=lambda k: k['pos'])]

        Tnoticias=self.procElems(noti)
        Tdocumentos=self.procElems(docu)
        Teventos=self.procElems(even)
        Treflexiones=self.procElems(refl)

        fp=open(self.plantilla)
        t=Template(fp.read())
        fp.close()
        html=t.render(Context({
            "FECHA" : self.fecha,
            "NUMERO" : self.id,
            "NOTICIAS" : Tnoticias,
            "DOCUMENTOS" : Tdocumentos,
            "EVENTOS" : Teventos,
            "REFLEXIONES" : Treflexiones
            },autoescape=False))
        #fp=open('./Boletin.html','w')
        fp=open(self.output,'w')
        fp.write(html.encode('utf-8'))
        fp.close()


    def procElems(self,lista):
        t=""
        a=""
        for l in lista:
            if (l['tipo']=='reflexion'):
                a=self.procReflexion(l)
            else:
                a=self.procItem(l)
            t=t+a
        return t

    def procItem(self,item):
        template = """
<div>
    <strong>{{ titulo }}</strong></div>
<div> {{ texto }} </div>
<div>
    <a href=" {{ link }} " target="_self">{{ tagenlace }}</a></div>
<div>
&nbsp;</div>
"""

        titulo=item["titulo"]
        texto=item["texto"]
        link=item["link"]

        t=Template(template)
        c=Context({"titulo" : titulo,
                "texto" : texto,
                "link" : link,
                "tagenlace" : self.tag_enlace}, autoescape=False)
        return t.render(c)

    def procReflexion(self,item):
        template = """
<li> {{ texto }} </li>
        """

        titulo=item["titulo"]
        texto=item["texto"]
        link=item["link"]

        t=Template(template)
        c=Context({"titulo" : titulo,
                        "texto" : texto,
                        "link" : link}, autoescape=False)
        return t.render(c)
