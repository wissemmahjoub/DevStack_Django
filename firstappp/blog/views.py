from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime


from .forms import ContactForm
from .forms import ImageeForm
from .forms import ImggForm
from .forms import GetVolumeForm
from .forms import VolumeForm
from django.core.files.storage import FileSystemStorage
import os.path
from .models import Document
from subprocess import call
def home(request):
    """ Exemple de page HTML, non valide pour que l'exemple soit concis """
    text = """<h1>Bienvenue sur Horizon modifie </h1>
              <p>Cette page va etre amelioree pour pouvoir creer des instances a travers openstack API !</p>"""
    return HttpResponse(text)

def date_actuelle(request):
    date = datetime.now()
    aa = "heloo"
    return render(request,'blog/date.html',locals())

def addition(request,nombre1,nombre2):
    total=int(nombre1)+int(nombre2)
    return  render(request,'blog/addition.html',locals())


#*******************************************************************************************
#****[Toeken] By wissem mahjoub**************************************************************
#*******************************************************************************************

def token(request) :
    # Generat Token --------------------------

    # la commande qui permet de stocker le fichier JSON qui contient le Token
    os.system('curl -s -X POST http://127.0.0.1:5000/v2.0/tokens \
                        -H "Content-Type: application/json" \
                        -d \'{"auth": {"tenantName": "admin", "passwordCredentials": {"username": "'"admin"'", "password": "'"esprit"'"}}}\' \
                        | python -m json.tool > token')

    # ici on va netoyer le fichier JSON par l'extraction de la valeur exacte du Token par la commande jq
    # et l'enregistrer dans le fichier "TOKEN_ID"
    os.system('jq \'.access.token.id\' token > f')
    os.system('sed \'s/\"//\' f > x |  sed \'s/\"//\' x > TOKEN_ID')
    # ici on va lire le contenu du fichier TOKEN_ID et l'affecter dans la variable "res"
    with open("TOKEN_ID", "r") as resul:
        res = str(resul.read())

    return  render(request,'blog/token.html',locals())


#*******************************************************************************************
#****[Add Volume] By Wissem Mahjoub*********************************************************
#*******************************************************************************************
def addvolume(request):
    form = VolumeForm(request.POST or None)
    size="1"
    name="null0"
    description="null0"
    ress="NULL0"
    os.system('echo "null" > COCO ')
    if form.is_valid():
        name = form.cleaned_data['name']
        description = form.cleaned_data['description']
        size = form.cleaned_data['size']
        envoi = True


     # ici on va lire le contenu du fichier TOKEN_ID et l'affecter dans la variable "ress"
        with open ("TOKEN_ID", "r") as resul:
            ress=str(resul.read())
    #cleaning Token
    taille = len(ress)
    tokenOK = ress[0:taille - 1]
    os.system('curl -i http://127.0.0.1:8776/v3/380e1127b76741ff99b156fce88cf09e/volumes -X POST -H "Content-Type: application/json" -H "Accept: application/json" -H "X-Auth-Token: '+tokenOK+' " -d \'{"volume": { "size": ' + size + ', "display_name": "' + name + '"}}\' > COCO')

    with open("COCO", "r") as resul:
        rr = str(resul.read())
    name=""
    OK=""
    if rr is "null" :
        OK="ERROR"

    return render(request, 'blog/addvolume.html', locals())

#*******************************************************************************************
#****[ListVolume] By wissem mahjoub*********************************************************
#*******************************************************************************************
def listevolume(request):
    form = GetVolumeForm(request.POST or None)

     # ici on va lire le contenu du fichier TOKEN_ID et l'affecter dans la variable "res"
    with open ("TOKEN_ID", "r") as resul:
        res=str(resul.read())

    #Afficher Volumes ----------------------
    commandeAffichevolume='curl -H "X-Auth-Token:'+res+'" -H "Content-Type: application/json" http://127.0.0.1:8776/v3/380e1127b76741ff99b156fce88cf09e/volumes/detail  > vol'
    os.system(commandeAffichevolume)
    with open ("vol", "r") as resultat:
        volumes=resultat.read()
    volumename = os.popen("jq '.volumes[].name' vol").readline()
    volumestatus = os.popen("jq '.volumes[].status' vol").readline()
    volumedescription = os.popen("jq '.volumes[].description' vol").readline()
    volumesize = os.popen("jq '.volumes[].size' vol").readline()
    volumedate = os.popen("jq '.volumes[].created_at' vol").readline()



    return render(request, 'blog/listevolume.html', locals())


#*******************************************************************************************
#********* Upload Image , By Chems *********************************************************
#*******************************************************************************************

def simple_upload(request):
    if request.method == 'POST':
        form = ImageeForm(request.POST, request.FILES)
        if form.is_valid():
            filee = form.cleaned_data["document"]
            myfile = request.FILES['document']
            fichier = request.FILES['document'].name

            fs = FileSystemStorage()

            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            ashh = fs.location
            ggg = ashh + "/" + fichier
            with open("TOKEN_ID", "r") as resul:
                tokenfor_img = str(resul.read())
            with open("images", "r") as r:
                imgs = r.read()
            os.system('jq \'.access.status.id\' images > imgOK')
            os.system('sed \'s/\"//\' imgOK > y |  sed \'s/\"//\' y > imgOKK')
            with open("imgOKK", "r") as r:
                imgID = r.read()

            commandeAddImage = 'curl -i -X PUT -H "X-Auth-Token: '+'gAAAAABZFo4CouSl71EHdkCuiqYF1014-axrv-RaMhSesDm18hApteLXsy2rVwaDFhxeOc60v4kH43iTnGbnXenZNT2Hc-nXGFZQ-eV7c1fJ-tz3xlFcSwmbn-NsG-xiucjr7wOQjVybg8pgUzPcp6TfzGOrpJL_8THw8owfkgfw-ShmGf0ctME'+'"  -H "Content-Type: application/octet-stream" -d '+ggg+'  http://192.168.1.16:9292/v2/images/4cafff0f-be40-4cb5-9044-28c2ad0d0fa1/file > final'
            os.system(commandeAddImage)
            with open("final", "r") as r:
                final = r.read()

    return render(request, 'blog/upload.html', locals())

#*******************************************************************************************
#********* Create Image , By Chems *********************************************************
#*******************************************************************************************

def createImg(request):
    form =ImggForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data["name"]
        container = form.cleaned_data["container"]
        disk = form.cleaned_data["disk"]
        visibility = form.cleaned_data["visibility"]

        with open("TOKEN_ID", "r") as resul:
            tokenfor_img = str(resul.read())

        jsonImg='\'{"name": "'+name+'", "container_format":"'+container+'", "disk_format":"'+disk+'", "visibility":"'+visibility+'", "tags": ["cirrosSapi", "14.04", "trusty"]}\''
        #commandeAddImage = 'curl -i -X POST -H "X-Auth-Token: '+'gAAAAABZFn_MSma6j_odMmj3RA7jGbGxey4WouXlGHLEZv6uorioFS8odmiOF8l1PyCwhPuwVPF_MUKemU-4CkH3dnZxXCvDWVKMOdy3jaRhWhOelXMSzLxFJF5Hip_mkuBAA0Q7kRyX75N-e9evChYg4_Tk9ncpUEBoWW0wR8BUN1I212_V2o0'+'"  -H "Content-Type: application/json" -d '+jsonImg+'  http://192.168.1.16:9292/v2/images > images'
        commandeAddImage = 'curl -i -X POST -H "X-Auth-Token: '+tokenfor_img+'"  -H "Content-Type: application/json" -d '+jsonImg+'  http://192.168.1.16:9292/v2/images > images'

        os.system(commandeAddImage)
        with open("images", "r") as r:
            imgs = r.read()

    return render(request, 'blog/createImg.html', locals())
