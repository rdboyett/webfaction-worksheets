import os
ROOT_PATH = os.path.dirname(__file__)

import subprocess
import errno
import json
import logging
import httplib2
from datetime import date

from django.shortcuts import render_to_response, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from myproject.googleapi.models import *
from django.core.exceptions import ObjectDoesNotExist
#from myproject.googleapi.forms import *
from django.utils import simplejson
from django.contrib.auth.models import *
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required

from apiclient.discovery import build
from django.core.urlresolvers import reverse
from myproject import settings
from oauth2client import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage

from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow

from apiclient import errors

#import PythonMagick
#from PythonMagick import Image
from pyPdf import PdfFileReader, PdfFileWriter
from tempfile import NamedTemporaryFile

import zipfile
import StringIO


#Test where the settings file is located (in home computer or on the server)
testPath = ROOT_PATH.split(os.sep)
if 'C:' in testPath:
    bOnServer = False
else:
    bOnServer = True


# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
if bOnServer:
    CLIENT_SECRETS = '/home/rdboyett/webapps/static_media/client_secrets.json'
else:
    CLIENT_SECRETS = 'c:/webfactionProject/client_secrets.json'

SCOPES = [
    'https://www.googleapis.com/auth/drive.install',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    # Add other requested scopes.
]

if bOnServer:
    FLOW = flow_from_clientsecrets(
        CLIENT_SECRETS,
        scope= ' '.join(SCOPES),
        redirect_uri='http://rdboyett.webfactional.com/oauth2callback')
else:
    FLOW = flow_from_clientsecrets(
        CLIENT_SECRETS,
        scope= ' '.join(SCOPES),
        redirect_uri='http://127.0.0.1:8000/oauth2callback')




def testLoad(request):
    return HttpResponse("Hello, You're in!")



def get_user_info(credentials):
  """Send a request to the UserInfo API to retrieve the user's information.

  Args:
    credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                 request.
  Returns:
    User information as a dict.
  """
  user_info_service = build(
      serviceName='oauth2', version='v2',
      http=credentials.authorize(httplib2.Http()))
  user_info = None
  try:
    user_info = user_info_service.userinfo().get().execute()
  except errors.HttpError, e:
    logging.error('An error occurred: %s', e)
  if user_info and user_info.get('id'):
    return user_info
  else:
    raise NoUserIdException()



def index(request):
    credential = None
    
    if credential is None or credential.invalid == True:
        FLOW.params['access_type'] = 'offline'
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                       request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)

def auth_return(request):
    if not xsrfutil.validate_token(settings.SECRET_KEY, request.REQUEST['state'],
                                   request.user):
      return  HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.REQUEST)
    
    user_info = get_user_info(credential)
    google_email = user_info.get('email')
    firstName = user_info.get('given_name')
    lastName = user_info.get('family_name')
    avatar = user_info.get('picture')
    
    if User.objects.filter(username=google_email):
        # Make sure that the e-mail is unique.
        user = User.objects.get(username=google_email)
        #userInfo = UserInfo.objects.get(user=user)
    else:
        user = User.objects.create(
            username = google_email,
            first_name = firstName,
            last_name = lastName,
            email = google_email,
            password = 'password',
        )
        
        userInfo = UserInfo.objects.create(
            user = user,
            avatar = avatar,
            createOrOpen = '/getFile/',
        )
    
    
    if user:
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
    
    userInfo = UserInfo.objects.get(user=user)
    
    storage = Storage(CredentialsModel, 'id', user, 'credential')
    storage.put(credential)
    return HttpResponseRedirect(userInfo.createOrOpen)



def getUserInfo(request):
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    
    if credential is None or credential.invalid == True:
        return HttpResponseRedirect("/login/")
    
    else:
        user_info = get_user_info(credential)
        google_email = user_info.get('email')
        firstName = user_info.get('given_name')
        lastName = user_info.get('family_name')
        avatar = user_info.get('picture')
        
    
    return render_to_response('user_info.html', {
        'google_email':google_email,
        'firstName':firstName,
        'lastName':lastName,
        'avatar':avatar,
        })
    
    

def driveList(request):
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    
    if credential is None or credential.invalid == True:
        return HttpResponseRedirect("/login/")
    
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        drive_service = build("drive", "v2", http=http)
        
        result = retrieve_all_files(drive_service)
        
        return render_to_response('list_files.html', {
        'userName': request.user.first_name,
        })
    
def startCreate(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    elif UserInfo.objects.filter(user=request.user):
        userInfo = UserInfo.objects.get(user=request.user)
        userInfo.createOrOpen = '/getFile/'
        userInfo.save()
    return HttpResponseRedirect("/login/")

def getFile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    return render_to_response('list_files.html', {
        })


def display_path(path):
    return path.replace("\\", "/")


def showFile(request, fileId=False):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    userInfo = UserInfo.objects.get(user=request.user)
    userInfo.createOrOpen = '/showFile/'
    if fileId:
        userInfo.fileID = fileId
    else:
        fileId = userInfo.fileID
    
    userInfo.save()
        
    today = datetime.datetime.now().strftime("%Y%m%d%H%M")
    
    if not fileId:
        return redirect('/getFile/')
    else:
        storage = Storage(CredentialsModel, 'id', request.user, 'credential')
        credential = storage.get()
        
        if credential is None or credential.invalid == True:
            return HttpResponseRedirect("/login/")
        
        else:
            http = httplib2.Http()
            http = credential.authorize(http)
            drive_service = build("drive", "v2", http=http)
        
        try:
            file = drive_service.files().get(fileId=fileId).execute()
            
            
            #get the download url for the file
            try:
                download_url = file['exportLinks']['application/pdf']
            except Exception:
                download_url = file.get('downloadUrl')
            
            if download_url:
                #Download the file's content and store as a PDF file-------------------------------------------------
              resp, content = drive_service._http.request(download_url)
              if resp.status == 200:
                title = 'worksheet'
                baseFilePath = os.path.join(settings.ROOT_PATH,'media', request.user.first_name+request.user.last_name+str(request.user.id))
                make_sure_path_exists(baseFilePath)
                pdfPath = os.path.join(baseFilePath,title + ".pdf")
                f = open(pdfPath, 'wb')
                f.write(content)
                f.close()
                
                #count the number of pages and delete if too many:---------------------------------------------------
                pdfFile = open(pdfPath, "rb")
                reader = PdfFileReader(pdfFile)
                counter = 0
                for page_num in xrange(reader.getNumPages()):
                    counter += 1
                if counter > 5:
                    bTooManyPages = True
                    pdfFile.close()
                    os.remove(pdfPath)
                else:
                    bTooManyPages = False
                
                
                
                if not bTooManyPages:
                    #Convert pages to images:-------------------------------------------------------------------------
                    bItConverted = covertPDFtoImage(pdfPath, os.path.join(baseFilePath, title+ '.jpg'))
                    if bItConverted:
                        pdfFile.close()
                        #os.remove(pdfPath)
                        
                    
                    #store file paths----------------------------------------------------------------------------------
                    filenames = []
                    for pageNumber in range(0,counter):
                        filenames.append(os.path.join(baseFilePath,title + '-' + str(pageNumber) + '.jpg'))
                        
                        
                    
                    #create a project-----------------------------------------------------------------------------------
                    newProject = Project.objects.create(
                        title = title,
                    )
                    userInfo.projects.add(newProject)
                    
                    
                    #create background images for the project----------------------------------------------------------
                    pageNum = 0
                    for filename in filenames:
                        pageNum += 1
                        fileComponentsList = filename.split(os.sep)
                        newList = []
                        if bOnServer:
                            for number in range(7,10):
                                newList.append(fileComponentsList[number])
                        else:
                            for number in range(4,7):
                                newList.append(fileComponentsList[number])
                        lastFileName = os.path.join('/',*newList)
                        newFilename = display_path(lastFileName)
                        
                        newBackImage = BackImage.objects.create(
                            imagePath = newFilename,
                            pageNumber = pageNum
                        )
                        newProject.backgroundImages.add(newBackImage)
                    
                    '''
                    #Create a json file to store all file information---------------------------------------------------
                    projectData = {
                        'userInfo_id':userInfo.id,
                        'project_id':newProject.id,
                    }
                    jsonFilePath = makeJsonFile(request.user, projectData, title)
                    filenames.append(jsonFilePath)
                    
                    
                    
                    #Zip the file and upload to Drive---------------------------------------------------------------------
                    myZipFile = zipFile(filenames, title, baseFilePath)
                    if myZipFile:
                        bMyUploadToDrive = driveUpload(request.user, os.path.join(baseFilePath,title + '.sst'))
                        if bMyUploadToDrive:
                            os.remove(os.path.join(baseFilePath,title + '.sst'))
                    '''
                    
                else:
                    return HttpResponse("Sorry you are limited to 5 pages for your worksheet")
              else:
                content = None
            else:
              # The file doesn't have any content stored on Drive.
              content = None
                
            title = file['title']
            mimeType = file['mimeType']
            
            return render_to_response('show_file.html', {
              'userInfo': userInfo,
              'newProject':newProject,
              'pageNumber':1,
              'totalPages': pageNum,
              'formInputs':False,
              })
        except errors.HttpError, error:
          return HttpResponseRedirect("/login/")   

def showNextPage(request, projectID=False, pageNumber=False, totalPages=False):
    if not projectID or not pageNumber:
        return HttpResponseRedirect("/login/")
    userInfo = UserInfo.objects.get(user=request.user)
    if Project.objects.filter(id=projectID):
        newProject = Project.objects.get(id=projectID)
        if newProject.formInputs.all():
            formInputs = newProject.formInputs.all().order_by('pageNumber', 'questionNumber')
        else:
            formInputs = False
        return render_to_response('show_file.html', {
              'userInfo': userInfo,
              'newProject':newProject,
              'pageNumber':int(pageNumber),
              'totalPages':int(totalPages),
              'formInputs':formInputs,
              })
    else:
        return HttpResponseRedirect("/login/")


def testMedia(request):
    return render_to_response('test2.html', {
              })


def covertPDFtoImage(input, output, quality=None, density=None):
    params = []
    #params += ["-unsharp", "0x0.4+0.6+0.008"]
    params += ["-density", str(250)]
    if bOnServer:
        subprocess.check_call(["convert"] + params + [input] + [output], 
                                    shell=False)
    else:
        subprocess.check_call(["convert"] + params + [input] + [output], 
                                    shell=True)
        
    return True



def imageConvert(request):
    cmd = ['convert', os.path.join(os.path.join(settings.ROOT_PATH,'media', request.user.first_name+request.user.last_name+str(request.user.id)),'test.pdf'), os.path.join(os.path.join(settings.ROOT_PATH,'media', request.user.first_name+request.user.last_name+str(request.user.id)),'imageOut.png')]
    subprocess.check_call(cmd, 
                shell=False)
    #os.remove(pathToFolder)
    return HttpResponse("Done")

def countPages(request):
    reader = PdfFileReader(open(os.path.join(baseFilePath,'test.pdf'), "rb"))
    counter = 0
    for page_num in xrange(reader.getNumPages()):
        counter += 1
    return HttpResponse("The number of pages: " + str(counter))


def zipFile(filenames, zipFileName, baseFilePath):
    # Files (local path) to put in the .zip
    # FIXME: Change this (get paths from DB etc)
    #filenames = [os.path.join(baseFilePath,'test-1.jpg'), os.path.join(baseFilePath,'test-2.jpg')]
    
    # Folder name in ZIP archive which contains the above files
    # E.g [thearchive.zip]/somefiles/file2.txt
    # FIXME: Set this to something better
    zip_subdir = "simplesheets"
    zip_filename = "%s.zip" % zip_subdir

    # Open StringIO to grab in-memory ZIP contents
    myZipPath = os.path.join(baseFilePath,zipFileName+'.sst')

    # The zip compressor
    zf = zipfile.ZipFile(myZipPath, "w")

    for fpath in filenames:
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)

        # Add file, at correct path
        zf.write(fpath, zip_path)
        os.remove(fpath)
        

    # Must close zip for all contents to be written
    zf.close()
    
    return True



def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise



def download_file(service, drive_file):
  """Download a file's content.

  Args:
    service: Drive API service instance.
    drive_file: Drive File instance.

  Returns:
    File's content if successful, None otherwise.
  """
  download_url = drive_file.get('downloadUrl')
  if download_url:
    resp, content = service._http.request(download_url)
    if resp.status == 200:
      #print 'Status: %s' % resp
      return content
    else:
      #print 'An error occurred: %s' % resp
      return None
  else:
    # The file doesn't have any content stored on Drive.
    return None



def retrieve_all_files(service):
  """Retrieve a list of File resources.

  Args:
    service: Drive API service instance.
  Returns:
    List of File resources.
  """
  result = []
  page_token = None
  while True:
    try:
      param = {}
      if page_token:
        param['pageToken'] = page_token
      files = service.files().list(**param).execute()

      result.extend(files['items'])
      page_token = files.get('nextPageToken')
      if not page_token:
        break
    except errors.HttpError, error:
      print 'An error occurred: %s' % error
      break
  return result




def driveUpload(user, FILENAME):
    storage = Storage(CredentialsModel, 'id', user, 'credential')
    credential = storage.get()
    
    if credential is None or credential.invalid == True:
        return HttpResponseRedirect("/login/")
    
    else:
        # Path to the file to upload
        #FILENAME = filePath
        
        fdir, fname = os.path.split(FILENAME)
    
        http = httplib2.Http()
        http = credential.authorize(http)
        drive_service = build("drive", "v2", http=http)
    
        # Insert a file
        media_body = MediaFileUpload(FILENAME, mimetype='application/sst', resumable=True)
        body = {
          'title': fname,
          'mimeType': 'application/sst'
        }
        
        file = drive_service.files().insert(body=body, media_body=media_body).execute()
          
        return True




def driveDownload(request):
    download_url = drive_file.get('downloadUrl')
    if download_url:
      resp, content = service._http.request(download_url)
      if resp.status == 200:
        print 'Status: %s' % resp
        return content
      else:
        print 'An error occurred: %s' % resp
        return None
    else:
      # The file doesn't have any content stored on Drive.
      return None 





def readJsonFile(user):
    basePath = os.path.join(settings.ROOT_PATH,'media', user.first_name+user.last_name+str(user.id))
    make_sure_path_exists(basePath)
        
    #This is what you use to open and load the data from the file
    with open(os.path.join(basePath,'projectData.json'), 'r') as json_file:
        data = json.load(json_file)
    
    return data
    
    
    
def makeJsonFile(user, data ,title):
    basePath = os.path.join(settings.ROOT_PATH,'media', user.first_name+user.last_name+str(user.id))
    make_sure_path_exists(basePath)
    
    '''
    #This is how you create new data
    data = {
        'userID': '1234',
        'ProjectID': '1234',
    }
    '''
    
    with open(os.path.join(basePath,title + '.json'), 'w') as json_file:
        json.dump(data, json_file)
        
    return os.path.join(basePath,title + '.json') 






