var longvalid = false;
var shortvalid = true;

//Validate long URL
var validatelong = function(){
	if ($('#long').val() === ''){
			longvalid= false;
			$('button[name="createbutton"]')[0].disabled = true;
			return;

		}
		else{
			longstr = $('#long').val();
			var re = /http:+\S+/;
			if (!re.test(longstr)){
			 	$("#longerror").text("long URL format should be http://...com");
			 	longvalid = false;
			 	$('button[name="createbutton"]')[0].disabled = true;
			 	return;
			 }		
		};

		$("#longerror").text("");
		longvalid = true;
		if (longvalid == true && shortvalid ==true){
			$('button[name="createbutton"]')[0].disabled = false ;
		}
}

// Validate Shortpath for Creation
var validateshort = function(){
	if ($('#short').val() != ''){
		shortstr = $('#short').val();
		var re = /^[A-Za-z]+$/;
		 if (!re.test(shortstr)){
		 	$("#shorterror").text("Shortpath can only take alphabets");
		 	$('button[name="createbutton"]')[0].disabled = true;
		 	shortvalid = false;
		 	return ;
		 }
	}
	$("#shorterror").text("");
	shortvalid = true;
	if (longvalid == true && shortvalid ==true){
		$('button[name="createbutton"]')[0].disabled = false ;
	}

}

// validate shortpath for Deletion
var validateshortdelete = function(){

	if ($('#shortdelete').val() === ""){
			$('button[name="deletebutton"]')[0].disabled = true;
		 	return ;

		};

		$("#shortdelerror").text("");
		$('button[name="deletebutton"]')[0].disabled = false;

};

$(function(){
	$('#long').focusout(validatelong);
	$('#short').focusout(validateshort);
	$('#shortdelete').focusout(validateshortdelete);
})


//Ask the user if he/she wants shortpath to be created automatically
function validateOnCreate(){

    if (document.createform.short.value === '') {
       var x=confirm("You have not entered short path. Do you want it to be automatically created?");
		if (x ==true){
			return true;
		}	
		else{
			return false;
		}
        
    }
    return true;

}
