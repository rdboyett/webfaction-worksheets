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




@dajaxice_register
def updateInputType(request, inputNumber, newInputType):
    if FormInput.objects.filter(id=inputNumber):
        formInput = FormInput.objects.get(id=inputNumber)
        formInput.inputType = str(newInputType)
        formInput.save()
    return simplejson.dumps({'inputNumber': inputNumber, 'newQuestionNumber': formInput.questionNumber, 'newInputType': newInputType, 'points': formInput.points})





@dajaxice_register
def updateQuestionNumber(request, inputNumber, newQuestionNumber):
    if FormInput.objects.filter(id=inputNumber):
        formInput = FormInput.objects.get(id=inputNumber)
        formInput.questionNumber = newQuestionNumber
        formInput.save()
    return simplejson.dumps({'inputNumber': inputNumber, 'newQuestionNumber': newQuestionNumber, 'inputType': formInput.inputType, 'points': formInput.points})



@dajaxice_register
def updateCorrectAnswer(request, inputNumber, newCorrectAnswer):
    if FormInput.objects.filter(id=int(inputNumber)):
        formInput = FormInput.objects.get(id=int(inputNumber))
        formInput.correctAnswer = newCorrectAnswer.strip()
        formInput.save()
    
    return simplejson.dumps({'inputNumber': inputNumber, 'newCorrectAnswer': newCorrectAnswer})



@dajaxice_register
def updatePoints(request, inputNumber, newPoints):
    if FormInput.objects.filter(id=int(inputNumber)):
        formInput = FormInput.objects.get(id=int(inputNumber))
        formInput.points = int(newPoints)
        formInput.save()
    
    return simplejson.dumps({'inputNumber': inputNumber, 'points': newPoints})





@dajaxice_register
def updateHelpText(request, inputNumber, newHelpText):
    if FormInput.objects.filter(id=int(inputNumber)):
        formInput = FormInput.objects.get(id=int(inputNumber))
        formInput.helpText = str(newHelpText)
        formInput.save()
    
    return simplejson.dumps({'inputNumber': inputNumber, 'helpText': newHelpText})




@dajaxice_register
def updateHelpLink(request, inputNumber, newHelpLink):
    if FormInput.objects.filter(id=int(inputNumber)):
        formInput = FormInput.objects.get(id=int(inputNumber))
        formInput.helpLink = str(newHelpLink)
        formInput.save()
    
    return simplejson.dumps({'inputNumber': inputNumber, 'helpLink': newHelpLink})



@dajaxice_register
def updateKeyword(request, inputNumber, optionIDNumber, newKeyword):
    newKeyword = newKeyword.strip()
    newKeyword = newKeyword.lower()
    if FormInput.objects.filter(id=int(inputNumber)):
        formInput = FormInput.objects.get(id=int(inputNumber))
        if optionIDNumber == 1:
            formInput.option1 = newKeyword
        elif optionIDNumber == 2:
            formInput.option2 = newKeyword
        elif optionIDNumber == 3:
            formInput.option3 = newKeyword
        else:
            formInput.option4 = newKeyword
            
        formInput.save()
    
    return simplejson.dumps({'inputNumber': inputNumber, 'optionNumber': formInput.id})



@dajaxice_register
def updateChoice(request, inputNumber, optionIDNumber, newChoice):
    newChoice = newChoice.strip()
    newChoice = newChoice.lower()
    if FormInput.objects.filter(id=int(inputNumber)):
        formInput = FormInput.objects.get(id=int(inputNumber))
        if optionIDNumber == 1:
            formInput.option1 = newChoice
        elif optionIDNumber == 2:
            formInput.option2 = newChoice
        elif optionIDNumber == 3:
            formInput.option3 = newChoice
        elif optionIDNumber == 4:
            formInput.option4 = newChoice
        else:
            formInput.option5 = newChoice
            
        formInput.save()
    
    return simplejson.dumps({'inputNumber': inputNumber, 'newChoice': newChoice})




