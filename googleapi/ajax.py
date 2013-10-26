from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from myproject.googleapi.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import *
from django.contrib.auth.decorators import login_required



@dajaxice_register
def test(request, userInfo, project_id, pageNumber, inputNumber, left, top, width, height):
    if Project.objects.filter(id=project_id):
        project = Project.objects.get(id=project_id)
        if project.formInputs.all():
            oldFormInputs = project.formInputs.all().order_by("-questionNumber")
            lastNumber = oldFormInputs[0].questionNumber
        else:
            lastNumber = 0
        newFormInput = FormInput.objects.create(
            pageNumber = int(pageNumber),
            inputType = 'text',
            left = float(left),
            top = float(top),
            width = float(width),
            height = float(height),
            questionNumber = lastNumber+1,
        )
        project.formInputs.add(newFormInput)
    
    
    return simplejson.dumps({'inputNumber': newFormInput.id, 'questionNumber': newFormInput.questionNumber, 'left': left,'top':top,'width':width,'height':height})
