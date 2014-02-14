# coding=utf-8

__author__ = 'nacho'



import glob
import os
from MyListbox import MyListbox
from Tkinter import *
from bCore import bCore

class Interfaz(Frame):
    """
    Interfaz Gráfico
    """
    def __init__(self, parent,parametros):
        """
        Constructor
        """
        Frame.__init__(self, parent, background="white")
        self.FrameActiva=None
        self.parent = parent
        self.parametros=parametros

        # Mantienen los tipos y num de cada elemento
        self.noticias=[]
        self.documentos=[]
        self.eventos=[]
        self.reflexiones=[]

        self.core=bCore(parametros)
        self.titulo="Gesbol "+self.parametros.version
        self.initUI(self.titulo)

    def setFileTitulo(self,file):
        self.parent.title(self.titulo+' - '+file)

        #OjO
        #self.HerrCopiara()
        #self.editUI()
        #self.formNuevoBoletin()

    def initUI(self,version):
        """
        Ventana Inicial. Establece título y menú
        """
        self.parent.geometry("260x250")
        self.parent.title(self.titulo)

        MenuBar=Menu(self.parent)
        self.parent.config(menu=MenuBar)

        FileMenu=Menu(MenuBar,tearoff=0)
        FileMenu.add_command(label="Nuevo",command=self.ArchivoNuevo)
        FileMenu.add_command(label="Abrir",command=self.ArchivoAbrir)
        MenuBar.add_cascade(label="Archivo",menu=FileMenu)
        self.HerrMenu=Menu(MenuBar,tearoff=0)
        self.HerrMenu.add_command(label="Copiar a",command=self.HerrCopiara)
        MenuBar.add_cascade(label="Herramientas",menu=self.HerrMenu)
        self.HerrMenu.entryconfigure(0,state=DISABLED)
        self.pack(fill=BOTH, expand=1)

    def editUI(self):
        """
        Dibuja el formulario de edicion de items
        """
        self.borra()
        self.parent.geometry("900x600")
        self.itemUI()
        self.editItemFrame.grid(row=0,column=0)
        self.FrameActiva=self.editItemFrame
        self.ListBoxNot.fill(self.noticias)
        self.ListBoxDoc.fill(self.documentos)
        self.ListBoxEve.fill(self.eventos)
        self.ListBoxRef.fill(self.reflexiones)

    def borra(self):
        if self.FrameActiva:
            self.FrameActiva.grid_forget()


    def itemUI(self):
        """
        Define el formulario de edición de item
        """
        self.editItemFrame=Frame(self,width=1480, height=585)

        self.itemFrame = Frame(self.editItemFrame, width=480, height=585)

        # Si no se modifica el labelNum se asume que es elemento nuevo
        self.LabelNum=-1
        self.L1=Label(self.itemFrame,text="TituloES")
        self.L1.grid(row=0,column=0,sticky=W)
        self.TitESv=StringVar()
        self.TitES=Entry(self.itemFrame,textvariable=self.TitESv,width=48)
        self.TitES.grid(row=1,column=0)

        self.L2=Label(self.itemFrame,text="TituloEN")
        self.L2.grid(row=2,column=0,sticky=W)
        self.TitENv=StringVar()
        self.TitEN=Entry(self.itemFrame,textvariable=self.TitENv,width=48)
        self.TitEN.grid(row=3,column=0)

        self.L3=Label(self.itemFrame,text="TextoES")
        self.L3.grid(row=4,column=0,sticky=W)
        self.TextES=Text(self.itemFrame,highlightbackground='gray',width=61,height=8)
        self.TextES.grid(row=5,column=0)

        self.L4=Label(self.itemFrame,text="TextoEN")
        self.L4.grid(row=6,column=0,sticky=W)
        self.TextEN=Text(self.itemFrame,highlightbackground='gray',width=61,height=8)
        self.TextEN.grid(row=7,column=0)

        self.L6=Label(self.itemFrame,text="LinkES")
        self.L6.grid(row=8,column=0,sticky=W)
        self.LinkESv=StringVar()
        self.LinkES=Entry(self.itemFrame,textvariable=self.LinkESv,width=48)
        self.LinkES.grid(row=9,column=0)

        self.L5=Label(self.itemFrame,text="LinkEN")
        self.L5.grid(row=10,column=0,sticky=W)
        self.LinkENv=StringVar()
        self.LinkEN=Entry(self.itemFrame,textvariable=self.LinkENv,width=48)
        self.LinkEN.grid(row=11,column=0)

        self.L7=Label(self.itemFrame,text="Tags")
        self.L7.grid(row=12,column=0,sticky=W)
        self.Tagsv=StringVar()
        self.Tags=Entry(self.itemFrame,textvariable=self.Tagsv,width=48)
        self.Tags.grid(row=13,column=0)

        self.Tipov=StringVar()
        self.Tipov.set("noticia")
        self.Tipo=OptionMenu(self.itemFrame,self.Tipov,"noticia","documento","evento","reflexion")
        self.Tipo.grid(row=14,column=0,sticky=W)

        self.butFrame = Frame(self.editItemFrame, width=100, height=585);
        self.ButNew=Button(self.butFrame,text="Nuevo")
        self.ButNew.configure(command=self.newItem)
        self.ButNew.grid(row=0,column=0)

        self.ButOK=Button(self.butFrame,text="OK")
        self.ButOK.configure(command=self.updateItem)
        self.ButOK.grid(row=1,column=0)

        self.ButTerminar=Button(self.butFrame,text="Terminar")
        self.ButTerminar.configure(command=self.updateFiles)
        self.ButTerminar.grid(row=2,column=0)

        self.listframe=Frame(self.editItemFrame, width=320, height=500, background="black");
        self.ListBoxNot=MyListbox(parent=self.listframe,title="Noticias",ancho=30,alto=7,elementos=self.noticias,dobleclick=self.accion_Noticias)
        self.ListBoxDoc=MyListbox(parent=self.listframe,title="Documentos",ancho=30,alto=7,elementos=self.documentos,dobleclick=self.accion_Documentos)
        self.ListBoxEve=MyListbox(parent=self.listframe,title="Eventos",ancho=30,alto=7,elementos=self.eventos,dobleclick=self.accion_Eventos)
        self.ListBoxRef=MyListbox(parent=self.listframe,title="Reflexiones",ancho=30,alto=3,elementos=self.reflexiones,dobleclick=self.accion_Reflexiones)
        self.ListBoxNot.grid(row=0,column=0)
        self.ListBoxDoc.grid(row=1,column=0)
        self.ListBoxEve.grid(row=2,column=0)
        self.ListBoxRef.grid(row=3,column=0)

        self.itemFrame.grid(row=0,column=0)
        self.butFrame.grid(row=0,column=1)
        self.listframe.grid(row=0,column=2)


    def puebla_item(self,itemEN,itemES,num):
        #LabelNum contiene el num del elemento cargado
        self.LabelNum=num
        self.TitENv.set(itemEN.find('titulo').text)
        self.TextEN.delete("1.0",END)
        self.TextEN.insert(END,itemEN.find('texto').text)
        self.LinkENv.set(itemEN.find('link').text)
        self.Tagsv.set(itemEN.find('tag').text)
        self.Tipov.set(itemEN.find('tipo').text)

        self.TitESv.set(itemES.find('titulo').text)
        self.TextES.delete("1.0",END)
        self.TextES.insert(END,itemES.find('texto').text)
        self.LinkESv.set(itemES.find('link').text)

    def BorraEditUI(self):
        """
        Inicializa el formulario de edición de item
        """
        self.LabelNum=-1
        self.TitESv.set("")
        self.TextES.delete("1.0",END)
        self.LinkESv.set("")
        self.TitENv.set("")
        self.TextEN.delete("1.0",END)
        self.LinkENv.set("")
        self.Tipov.set("noticia")
        self.Tagsv.set("")


    def ArchivoNuevo(self):
        """
        Formulario de creación de nuevo boletín
        """
        self.borra()
        self.parent.geometry("270x200")
        self.NuevoBoletinFrame1 = Frame(self, width=100, height=400)
        self.FrameActiva=self.NuevoBoletinFrame1

        L1=Label(self.NuevoBoletinFrame1,text="Número").grid(row=0)
        L2=Label(self.NuevoBoletinFrame1,text="Día (d)").grid(row=1)
        L3=Label(self.NuevoBoletinFrame1,text="Mes (m)").grid(row=2)
        L4=Label(self.NuevoBoletinFrame1,text="Año (aaaa)").grid(row=3)

        self.IdV=StringVar()
        self.Id=Entry(self.NuevoBoletinFrame1,textvariable=self.IdV,width=10).grid(row=0,column=1)
        self.DiaV=StringVar()
        self.Dia=Entry(self.NuevoBoletinFrame1,textvariable=self.DiaV,width=10).grid(row=1,column=1)
        self.MesV=StringVar()
        self.Mes=Entry(self.NuevoBoletinFrame1,textvariable=self.MesV,width=10).grid(row=2,column=1)
        self.AnioV=StringVar()
        self.Anio=Entry(self.NuevoBoletinFrame1,textvariable=self.AnioV,width=10).grid(row=3,column=1)

        ButOK=Button(self.NuevoBoletinFrame1,text="Ok")
        ButOK.grid(row=0,column=2)
        ButOK.configure(command=self.NuevoBol)
        ButCancel=Button(self.NuevoBoletinFrame1,text="Cancelar")
        ButCancel.grid(row=1,column=2)
        ButCancel.configure(command=self.formNuevoBoletinSalir)

        self.setFileTitulo("boletin-"+str(self.Id))

        self.NuevoBoletinFrame1.grid()

    def formNuevoBoletinSalir(self):
        """
        Borra el formulario de nuevo boletín
        """
        self.NuevoBoletinFrame1.forget()

    def NuevoBol(self):
        """
        Establece los datos del nuevo boletín en core y pasa a la edición de items
        """
        datos={'id':self.IdV.get(),'dia':self.DiaV.get(),'mes':self.MesV.get(),'anio':self.AnioV.get()}
        self.core.nuevoBol(datos)
        self.formNuevoBoletinSalir()
        self.editUI()
        self.editItemFrame.pack()


    def ArchivoAbrir(self):
        """
        Formulario de apertura de archivo
        """
        self.borra()
        self.ArchivoAbrirFrame=Frame(self, width=320, height=500)
        self.FrameActiva=self.ArchivoAbrirFrame

        self.scrollbar1=Scrollbar(self.ArchivoAbrirFrame)
        self.scrollbar1.grid(row=0,column=1,sticky=N+S)
        self.ListBoxAbrirArchivo=Listbox(self.ArchivoAbrirFrame,yscrollcommand=self.scrollbar1.set)

        self.ListBoxAbrirArchivo.grid(row=0,column=0,sticky=N)
        self.scrollbar1.config(command=self.ListBoxAbrirArchivo.yview)

        l=self.ListaArchivos()
        for i in l:
            self.ListBoxAbrirArchivo.insert(END,i)

        self.ButOKAbrirArchivo=Button(self.ArchivoAbrirFrame,text="Abrir")
        self.ButOKAbrirArchivo.configure(command=lambda: self.AbrirBoletin(l[int(self.ListBoxAbrirArchivo.curselection()[0])]))
        self.ButOKAbrirArchivo.grid(row=0,column=2)

        self.ArchivoAbrirFrame.grid()
        self.HerrMenu.entryconfigure(0,state='normal')

    def HideListaArchivos(self):
        """
        Borra el ListBox de los archivos
        """
        self.scrollbar1.grid_forget()
        self.ListBoxAbrirArchivo.grid_forget()
        self.ButOKAbrirArchivo.grid_forget()

    def ListaArchivos(self):
        dir=self.parametros.dirxml
        p=os.path.join(dir,"*-en.xml")
        archs=glob.glob(p)
        l=[]
        for a in archs:
            e=re.match('.*\/(.*)\-en\.xml',a,re.M|re.I)
            l.append(e.group(1))
        return l

    def AbrirBoletin(self,nombre):
        """
        Callback desde Menu Archivo->Abrir.
        """
        self.core.cargaBoletines(nombre)
        self.setFileTitulo(nombre)
        self.listaItems()
        self.HideListaArchivos()
        self.editUI()

    def listaItems(self):
        """
        Mantiene una lista con todos los titulos, nums y tipos de los elementos XML
        """

        del self.documentos[:]
        del self.reflexiones[:]
        del self.eventos[:]
        del self.noticias[:]

        noti=[]
        docu=[]
        refl=[]
        even=[]

        indice=0
        for i in self.core.elementos:
            item=i['itemEN']
            titulo=item.findtext("titulo")
            pos=int(item.findtext("pos"))
            tipo=item.findtext("tipo")
            if tipo=='noticia':
                noti.append({'titulo':titulo,'pos':pos})
            elif tipo=='documento':
                docu.append({'titulo':titulo,'pos':pos})
            elif tipo=='evento':
                even.append({'titulo':titulo,'pos':pos})
            else:
                refl.append({'titulo':titulo,'pos':pos})

        self.noticias=[i['titulo'] for i in sorted(noti,key=lambda k: k['pos'])]
        self.documentos=[i['titulo'] for i in sorted(docu,key=lambda k: k['pos'])]
        self.eventos=[i['titulo'] for i in sorted(even,key=lambda k: k['pos'])]
        self.reflexiones=[i['titulo'] for i in sorted(refl,key=lambda k: k['pos'])]

    def newItem(self):
        """
        Callback del botón Nuevo item.
        Tan sólo borra el contenido del formulario del item.
        """
        self.BorraEditUI()


    def updateItem(self):
        """
        Callback del botón OK item.
        Actualiza el item en el XML a partir de los valores en los widgets
        """
        titulo=self.TitENv.get()
        texto=self.TextEN.get("1.0",END)
        link=self.LinkENv.get()
        tag=self.Tagsv.get()
        tipo=self.Tipov.get()

        num=self.LabelNum
        if num<0: # el item no tiene num => es nuevo
            nuevo=True
        else:
            nuevo=False
        itemEN={'titulo':titulo,'texto':texto,'link':link,'tag':tag,'tipo':tipo}
        titulo=self.TitESv.get()
        texto=self.TextES.get("1.0",END)
        link=self.LinkESv.get()
        itemES={'titulo':titulo,'texto':texto,'link':link,'tag':tag,'tipo':tipo}
        if (nuevo):
            self.core.nuevoItem(itemEN,itemES)
        else:
            self.core.updateItem(itemEN,itemES,num)
        self.BorraEditUI()
        self.listaItems()
        if (tipo=="noticia"):
            self.ListBoxNot.fill(self.noticias)
        elif (tipo=="documento"):
            self.ListBoxDoc.fill(self.documentos)
        elif (tipo=="evento"):
            self.ListBoxEve.fill(self.eventos)
        else:
            self.ListBoxRef.fill(self.reflexiones)

        #self.cargaItemsListBox()
        # Manera muy poco eficiente de hacer backup
        # Si funciona como debe podrían quitarse estas dos llamadas
        # OjO
        pos=self.setPosiciones()
        self.core.updateFiles(pos)

    def updateFiles(self):
        """
        Sale de la edición de items y actualiza los archivos XML
        """
        pos=self.setPosiciones()
        # self.itemFrame.forget()
        # self.butFrame.forget()
        # self.listframe.forget()
        self.editItemFrame.grid_forget()
        self.parent.geometry("250x450")
        self.core.updateFiles(pos)


    def setPosiciones(self):
        """
        A partir de las listas usadas para poblar los listbox
        Creo una lista que tenga elementos (num,pos)
        Esa lista se la paso al core para que actualice el XML
        """
        a=self.calcPos(self.documentos)
        b=self.calcPos(self.noticias)
        c=self.calcPos(self.eventos)
        d=self.calcPos(self.reflexiones)
        return a+b+c+d

    def calcPos(self,lista):
        posiciones=[]
        p=1
        for i in lista:
            item={}
            n=self.numByTit(i)
            item['pos']=p
            item['num']=n
            p+=1
            posiciones.append(item)
        return posiciones

    def numByTit(self,titulo):
        n=0
        for i in self.core.elementos:
            it=i['itemEN']
            tit=it.findtext('titulo')
            if titulo==tit:
                return n
            else:
                n+=1


    def accion_Noticias(self,e):
        """
        Callback del doble click en la Listbox de noticias
        """
        # Obtiene el indice de la linea seleccionada en la lista
        i=self.ListBoxNot.seleccion()
        titulo=self.noticias[i]
        item=self.core.item(titulo)
        self.puebla_item(item[0],item[1],item[2])

    def accion_Documentos(self,e):
        """
        Callback del doble click en la Listbox de documentos
        """
        # Obtiene el indice de la linea seleccionada en la lista
        i=self.ListBoxDoc.seleccion()
        titulo=self.documentos[i]
        item=self.core.item(titulo)
        self.puebla_item(item[0],item[1],item[2])

    def accion_Reflexiones(self,e):
        """
        Callback del doble click en la Listbox de reflexiones
        """
        # Obtiene el indice de la linea seleccionada en la lista
        i=self.ListBoxRef.seleccion()
        titulo=self.reflexiones[i]
        item=self.core.item(titulo)
        self.puebla_item(item[0],item[1],item[2])


    def accion_Eventos(self,e):
        """
        Callback del doble click en la Listbox de eventos
        """
        # Obtiene el indice de la linea seleccionada en la lista
        i=self.ListBoxEve.seleccion()
        titulo=self.eventos[i]
        item=self.core.item(titulo)
        self.puebla_item(item[0],item[1],item[2])

    def HerrCopiara(self):
        self.borra()
        altura=650
        self.parent.geometry("500x650")
        CopiarFrame=Frame(self, width=840, height=altura)

        itemsFrame=Frame(CopiarFrame,width=440,height=altura)

        L1=Label(itemsFrame,text="Noticias")
        L1.grid(row=0,column=0,sticky=W)
        scrollbar1=Scrollbar(itemsFrame)
        scrollbar1.grid(row=1,column=1,sticky=N+S)
        self.ListBoxNoticias=Listbox(itemsFrame,yscrollcommand=scrollbar1.set,selectmode=MULTIPLE,exportselection=False)
        self.ListBoxNoticias.grid(row=1,column=0)
        for item in self.noticias:
            self.ListBoxNoticias.insert(END, item)

        L2=Label(itemsFrame,text="Eventos")
        L2.grid(row=2,column=0,sticky=W)
        scrollbar2=Scrollbar(itemsFrame)
        scrollbar2.grid(row=3,column=1,sticky=N+S)
        self.ListBoxEventos=Listbox(itemsFrame,yscrollcommand=scrollbar2.set,selectmode=MULTIPLE,exportselection=False)
        self.ListBoxEventos.grid(row=3,column=0)
        for item in self.eventos:
            self.ListBoxEventos.insert(END, item)

        L3=Label(itemsFrame,text="Documentos")
        L3.grid(row=4,column=0,sticky=W)
        scrollbar3=Scrollbar(itemsFrame)
        scrollbar3.grid(row=5,column=1,sticky=N+S)
        self.ListBoxDocumentos=Listbox(itemsFrame,yscrollcommand=scrollbar3.set,selectmode=MULTIPLE,height=5,exportselection=False)
        self.ListBoxDocumentos.grid(row=5,column=0)
        for item in self.eventos:
            self.ListBoxDocumentos.insert(END, item)

        L4=Label(itemsFrame,text="Reflexiones")
        L4.grid(row=6,column=0,sticky=W)
        scrollbar4=Scrollbar(itemsFrame)
        scrollbar4.grid(row=7,column=1,sticky=N+S)
        self.ListBoxReflexiones=Listbox(itemsFrame,yscrollcommand=scrollbar4.set,selectmode=MULTIPLE,height=5,exportselection=False)
        self.ListBoxReflexiones.grid(row=7,column=0)
        for item in self.reflexiones:
            self.ListBoxReflexiones.insert(END, item)

        BotonFrame=Frame(CopiarFrame,width=100,height=altura)
        ButSend=Button(BotonFrame,text=">")
        ButSend.grid(row=0,column=0)
        ButSend.configure(command=self.DoCopiara)

        # ButTerminar=Button(BotonFrame,text="Terminar")
        # ButTerminar.grid(row=1,column=0)
        # ButTerminar.configure(command=self.DoTerminar)

        ArchFrame=Frame(CopiarFrame,width=400,height=altura)

        scrollbar5=Scrollbar(ArchFrame)
        scrollbar5.grid(row=0,column=1,sticky=N+S)
        self.ListBoxArchivos=Listbox(ArchFrame,yscrollcommand=scrollbar5.set)
        self.ListBoxArchivos.grid(row=0,column=0)

        l=self.ListaArchivos()
        for i in l:
            self.ListBoxArchivos.insert(END,i)

        itemsFrame.grid(row=0,column=0)
        BotonFrame.grid(row=0,column=1)
        ArchFrame.grid(row=0,column=2)
        CopiarFrame.grid()
        self.FrameActiva=CopiarFrame

    def DoCopiara(self):

        l=self.ListaArchivos()
        i=int(self.ListBoxArchivos.curselection()[0])
        boletin=l[i]

        tits=[]
        n=self.ListBoxNoticias.curselection()
        for i in n:
            tits.append(self.noticias[int(i)])
        n=self.ListBoxDocumentos.curselection()
        for i in n:
            tits.append(self.documentos[int(i)])
        n=self.ListBoxEventos.curselection()
        for i in n:
            tits.append(self.eventos[int(i)])
        n=self.ListBoxReflexiones.curselection()
        for i in n:
            tits.append(self.reflexiones[int(i)])
        ns=[]
        for i in tits:
            ns.append(self.numByTit(i))

        elementos=[]
        for i in ns:
            elementos.append(self.core.elementos[i])

        self.AbrirBoletin(boletin)

        for i in elementos:
            en={}
            en['titulo']=i['itemEN'].findtext('titulo')
            en['texto']=i['itemEN'].findtext('texto')
            en['link']=i['itemEN'].findtext('link')
            en['tipo']=i['itemEN'].findtext('tipo')
            en['tag']=i['itemEN'].findtext('tag')
            es={}
            es['titulo']=i['itemES'].find('titulo').text
            es['texto']=i['itemES'].find('texto').text
            es['link']=i['itemES'].find('link').text
            es['tipo']=i['itemES'].find('tipo').text
            es['tag']=i['itemES'].find('tag').text
            self.core.nuevoItem(en,es)
        self.listaItems()
        pos=self.setPosiciones()
        self.core.updateFiles(pos)

        self.ListBoxNot.fill(self.noticias)
        self.ListBoxDoc.fill(self.documentos)
        self.ListBoxEve.fill(self.eventos)
        self.ListBoxRef.fill(self.reflexiones)


    def DoTerminar(self):
	"""
	test
	"""
        pass
