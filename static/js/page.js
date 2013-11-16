
    
    $( document ).ready(function() {
        resizeElements();
    });
    $( window ).resize(function() {
        resizeElements();
      });
    
    function resizeElements() {
        var screenWidth = $( '#wrapper' ).width();
        var fontPixels = (screenWidth/1267)*22;
        var fontPixels2 = (screenWidth/1267)*18;
        //$("input").attr('style','font-size:'+fontPixels+'px;line-height:'+fontPixels+'px;');
        //$("input").css('font-size', fontPixels+'px', 'line-height', fontPixels+'px');
        $("input").css({
                'font-size': fontPixels+'px',
                'line-height': fontPixels+'px' 
        });
	$("textarea").css({
                'font-size': fontPixels+'px',
                'line-height': fontPixels+'px' 
        });
	$("select").css({
                'font-size': fontPixels+'px',
                'line-height': fontPixels+'px' 
        });
	if (fontPixels2 < 14) {
	    fontPixels2 = 14
	}
	$(".menuItem").css({
                'font-size': fontPixels2+'px',
                'line-height': fontPixels2+'px' 
        });
	$("#questionType").css({
                'font-size': (fontPixels2-2)+'px',
                'line-height': (fontPixels2-2)+'px' 
        });
	
        var top = $('#questionMenu').offset().top - $(window).scrollTop();
	var bottom = $('#questionMenu').outerHeight(false);
	var topOfPane = top + bottom;
        $('.typePane').css({
                'top': topOfPane,
        });
        
        
    }
    
    /* Dajaxice Calls------------------------------------------------------------------------
     */
    /*$('#wrapper img').click(function(){
        Dajaxice.myproject.googleapi.test(test_callback, {'test_id':'it worked'});
    });*/
    
    var leftPercentage = 0;
    var topPercentage = 0;
    var widthPercentage = 0;
    var heightPercentage = 0;
    
    $('#wrapper img').imgAreaSelect({
        fadeSpeed: false,
        handles: true,
        onSelectEnd: function(img, selection){
            if (!selection.width || !selection.height){
                return;
            }
            $('.imgareaselect-selection').attr( 'id', 'enter_area');
            var imageWidth = $( '#wrapper' ).width();
            leftPercentage = (selection.x1/imageWidth)*100;
            var imageHeight = $( '#wrapper' ).height();
            topPercentage = (selection.y1/imageHeight)*100;
            widthPercentage = (selection.width/imageWidth)*100;
            heightPercentage = (selection.height/imageHeight)*100;
            
            
            //alert('left: ' + leftPercentage + '%, top: '+ topPercentage+ '%, width: ' + widthPercentage + '%, height: ' + heightPercentage + '%...');
            
        }
    });
    
    $(document).keydown(function (e) {
        if (e.keyCode == 13){
            e.preventDefault();
            if ($('#enter_area').is(":visible")) {
                //alert('selection is visible');
                runSelection();
            }
        }
    });
    
    $( document ).dblclick(function() {
            if ($('#enter_area').is(":visible")) {
                //alert('selection is visible');
                runSelection();
            }
        //alert('left: ' + leftPercentage + '%, top: '+ topPercentage+ '%, width: ' + widthPercentage + '%, height: ' + heightPercentage + '%...');
    });
    
    function runSelection() {
        $('.imgareaselect-outer').css('background-color','rgb(152,128,5)');
        $('#wrapper img').imgAreaSelect({
            fadeSpeed: 1000,
            hide: true,
            onSelectStart: doThisNext,
        });
        $('#wrapper img').imgAreaSelect({
            fadeSpeed: false,
        });
        var inputNumber = ($("form input").length)+1;
        Dajaxice.myproject.googleapi.test(test_callback, {'userInfo': '{{ userInfo.id }}', 'project_id':'{{ newProject.id }}', 'pageNumber': '{{ pageNumber }}', 'inputNumber': inputNumber, 'left': leftPercentage,'top':topPercentage,'width':widthPercentage,'height':heightPercentage});
        
    }
    
    function doThisNext(callback) {
        $('#wrapper img').imgAreaSelect({
            fadeSpeed: false,
        }); 
        $('.imgareaselect-outer').css('background-color','rgb(0,0,0)');
        
        //callback();
    }
    
    
    
    //Dajaxice.myproject.teacherTools.setQuickLink(setQuickLink_callback, {'list_id':listId, 'link_id':parseInt(linkID), 'user_id':parseInt(userID), 'sort_number':parseInt(sortNumber)});
    /*--------------------for dajaxice callbacks------------------------------------*/
	
    function test_callback(data){
        //alert('left: ' + data.left + '%, top: '+ data.top+ '%, width: ' + data.width + '%, height: ' + data.height + '%...');

        $( "#default_form" ).append( "<input id='input"+ data.inputNumber +"' class='answers highlight' data-options='' type='text' title='answer...' name=''>" );
        $("#input"+ data.inputNumber).css({
                'position': 'absolute',
                'z-index': '1000',
                'left': data.left + '%',
                'top': data.top+ '%',
                'width': data.width + '%',
                'height': data.height + '%'
        });
        $("#input"+ data.inputNumber).attr('data-options', '{"answer_id":"'+ data.inputNumber + '", "question_number":"'+ data.questionNumber + '", "input_type":"text"}');
        resizeElements();
    }
    
    /*****************************Put Answer info**************************************************/
    $('#default_form').on('focus', '.answers', function () {
        //alert('here');
        $('.typePane').hide();
        var elementID = $(this).attr('id');
        var IDnum = elementID.match(/\d+/g);
        $('#'+elementID).css('z-index','1002');
        $('#questionMenu').css('display','block');
	var answerID = $('#'+elementID).data("options").answer_id;
	$('#questionNumber').attr('data-options', '{"answer_id":"'+ answerID + '"}');
	$('#questionNumber').data("options").answer_id = answerID;
	$('#questionType').val($('#'+elementID).attr('type'));
	var question_type = $('#'+elementID).data("options").input_type;
	$( "#questionType" ).val(question_type);
	console.log(question_type);
        $('#questionNumber').val($('#'+elementID).data("options").question_number);
        resizeElements();
        setTimeout(function() {
            var dInput = $('#'+elementID).val();
            //console.log(dInput);
	    if (question_type == 'select') {
		$('#multipleChoicePane').slideDown( "slow");
	    }
	    else if (question_type == 'checkbox') {
		$('#checkboxPane').slideDown( "slow");
	    }
	    else if (question_type == 'textarea') {
		$('#textareaPane').slideDown( "slow");
	    }
	    else{$('#textPane').slideDown( "slow");}
            $('#correctAnswer').text(dInput);
        }, 500);
    });
    
    
    
    $('#backgroundImage').click(function(){
        //alert('background');
        $('.answers').blur();
        var elementID = $(this).attr('id');
        var IDnum = elementID.match(/\d+/g);
        $('#'+elementID).css('z-index','1000');
        $('#questionMenu').hide("slow");
        $('.typePane').hide("slow");
    });


    $("#default_form").on('keydown', '.answers', function() {
        //Interrupt the execution thread to allow input to update
        var elementID = $(this).attr('id');
        setTimeout(function() {
            var dInput = $('#'+elementID).val();
            //console.log(dInput);
            $('#correctAnswer').text(dInput);
        }, 0);
    });
    
    /******************CHECK IF QUESTION NUMBER CHANGES****************************/
    
    $('#questionNumber').change(function () {
	var inputNumber_id = $('#questionNumber').data("options").answer_id;
	var newQuestionNumber = $('#questionNumber').val();
	//alert(inputNumber_id);
	Dajaxice.myproject.googleapi.updateQuestionNumber(updateQuestionNumber_callback, {'inputNumber': inputNumber_id, 'newQuestionNumber': newQuestionNumber});
	
    });
    
    function updateQuestionNumber_callback(data){
	$("#input"+ data.inputNumber).data("options").question_number = data.newQuestionNumber;
	$("#input"+ data.inputNumber).attr('data-options', '{"answer_id":"'+ data.inputNumber + '", "question_number":"'+ data.newQuestionNumber + '"}');
	//alert(data.inputNumber);
    }
    
    /******************Enter Correct Answer****************************/
    
    $("#default_form").on('change', '.answers', function () {
        setTimeout(function() {
            var dInput = $('#'+elementID).val();
            //console.log(dInput);
            $('#correctAnswer').text(dInput);
        }, 1);
        var elementID = $(this).attr('id');
        var inputNumber_id = elementID.match(/\d+/g);
	var newCorrectAnswer = $('#'+elementID).val();
	if (document.getElementById(elementID).checked == true) {
	    $('#showCheckbox').prop("checked", true);
	}
	else{$('#showCheckbox').prop("checked", false);}
	//alert(inputNumber_id);
	Dajaxice.myproject.googleapi.updateCorrectAnswer(updateCorrectAnswer_callback, {'inputNumber': parseInt(inputNumber_id), 'newCorrectAnswer': (newCorrectAnswer).toString()});
    });
    
    function updateCorrectAnswer_callback(data){
	//alert(data.inputNumber);
    }
    
    /******************Change question Type****************************/
    $( "#questionType" ).change(function() {
	var inputNumber_id = $('#questionNumber').data("options").answer_id;
	var inputType = $( "#questionType" ).val();
	var oldInputType = $('#input'+inputNumber_id).data("options").input_type;
	
	Dajaxice.myproject.googleapi.updateInputType(updateInputType_callback, {'inputNumber': parseInt(inputNumber_id), 'newInputType': (inputType).toString()});
	//alert(inputNumber_id);
	if (inputType == 'textarea') {
	    createTextarea('input'+inputNumber_id);
	}
	else if (inputType == 'select') {
	    createSelect('input'+inputNumber_id);
	}
	else if (inputType == 'work') {
	    createWork('input'+inputNumber_id);
	}
	else if ((inputType == 'text' || inputType == 'number' || inputType == 'checkbox') && (oldInputType == 'textarea' || oldInputType == 'select' || oldInputType == 'work')) {
	    //Re-create the default input type
	    createDefaultInput('input'+inputNumber_id, inputType);
	    $('#input'+inputNumber_id).data("options").input_type = inputType;
	    $('#input'+inputNumber_id).attr('data-options', '{"answer_id":"'+ data.answer_id + '", "question_number":"'+ data.question_number + '", "input_type":"'+inputType+'"}');
	}
	else{
	    $('#input'+inputNumber_id).get(0).type = inputType;
	    var data = $('#input'+inputNumber_id).data("options");
	    $('#input'+inputNumber_id).data("options").input_type = inputType;
	    $('#input'+inputNumber_id).attr('data-options', '{"answer_id":"'+ data.answer_id + '", "question_number":"'+ data.question_number + '", "input_type":"'+inputType+'"}');
	}
	$('#input'+inputNumber_id).focus();
    });
    
    function updateInputType_callback() {
	//code
    }
    
    
    /*****************************Synchronize Checkboxes*************************/
    $('#showCheckbox').click(function(){
	var inputNumber_id = $('#questionNumber').data("options").answer_id;
	if (document.getElementById('showCheckbox').checked == true) {
	    $('#input'+inputNumber_id).prop("checked", true);
	}
	else{$('#input'+inputNumber_id).prop("checked", false);}
    });
    
    /****************************Create Inputs Area*********************************/
    function createTextarea(elementID) {
	//get the important parts of element
	var testStyle = $('#'+elementID).attr('style');
	var data = $('#'+elementID).data("options");
	//make the old input disappear
	$('#'+elementID).remove();
	//$('#'+elementID).css("display","none");
	//$('#'+elementID).attr('id','noShow');
	
	//Now, create the textarea
	$( "#default_form" ).append( "<textarea id='"+ elementID +"' class='answers highlight img-rounded' readonly='readonly' data-options=''>Place keywords to search in order to help with grading later.</textarea>" );
        $('#'+elementID).attr('style',testStyle);
        //$('#'+elementID).attr('data-options', '{"answer_id":"'+ options.answer_id + '", "question_number":"'+ options.question_number + '"}');
	
	$('#'+elementID).attr('data-options', '{"answer_id":"'+ data.answer_id + '", "question_number":"'+ data.question_number + '", "input_type":"textarea"}');
	
	$('#'+elementID).focus();
        resizeElements();
        
	
	//console.log(style);
	//style="position: absolute;z-index: 1000;left: {{ input.left }}%;top: {{ input.top }}%;width: {{ input.width }}%; height: {{ input.height }}%"
    }
    
    
    function createSelect(elementID) {
	//get the important parts of element
	var testStyle = $('#'+elementID).attr('style');
	var data = $('#'+elementID).data("options");
	//make the old input disappear
	$('#'+elementID).remove();
	
	//Now, create the textarea
	$( "#default_form" ).append( "<select id='"+ elementID +"' class='answers highlight img-rounded' data-options=''><option id='option0' value='none'>Select One...</option></select>" );
        $('#'+elementID).attr('style',testStyle);
	
	$('#'+elementID).attr('data-options', '{"answer_id":"'+ data.answer_id + '", "question_number":"'+ data.question_number + '", "input_type":"select"}');
	
	$('#'+elementID).focus();
        resizeElements();
    }
    function createWork(elementID) {
	//get the important parts of element
	var testStyle = $('#'+elementID).attr('style');
	var data = $('#'+elementID).data("options");
	//make the old input disappear
	$('#'+elementID).remove();
	
	//Now, create the textarea
	$( "#default_form" ).append( "<textarea id='"+ elementID +"' class='answers highlight img-rounded' readonly='readonly' data-options=''>Work Area will be activated for student use...</textarea>" );
        $('#'+elementID).attr('style',testStyle);
        //$('#'+elementID).attr('data-options', '{"answer_id":"'+ options.answer_id + '", "question_number":"'+ options.question_number + '"}');
	
	$('#'+elementID).attr('data-options', '{"answer_id":"'+ data.answer_id + '", "question_number":"'+ data.question_number + '", "input_type":"work"}');
	
	$('#'+elementID).focus();
        resizeElements();
        
    }
    
    
    function createDefaultInput(elementID, inputType) {
	//get the important parts of element
	var testStyle = $('#'+elementID).attr('style');
	var data = $('#'+elementID).data("options");
	//make the old input disappear
	$('#'+elementID).remove();
	//$('#'+elementID).css("display","none");
	//$('#'+elementID).attr('id','noShow');
	
	//Now, create the textarea
	$( "#default_form" ).append( "<input id='"+ elementID +"' class='answers highlight' data-options='' type='"+inputType+"' title='answer...' name=''>" );
        $('#'+elementID).attr('style',testStyle);
        //$('#'+elementID).attr('data-options', '{"answer_id":"'+ options.answer_id + '", "question_number":"'+ options.question_number + '"}');
	
	$('#'+elementID).attr('data-options', '{"answer_id":"'+ data.answer_id + '", "question_number":"'+ data.question_number + '", "input_type":"'+inputType+'"}');
	
	$('#'+elementID).focus();
	
        resizeElements();
        
	
	//console.log(style);
	//style="position: absolute;z-index: 1000;left: {{ input.left }}%;top: {{ input.top }}%;width: {{ input.width }}%; height: {{ input.height }}%"
    }