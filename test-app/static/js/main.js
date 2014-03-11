

function validateOnCreate(){
	if (document.createform.long.value == '') {
		alert ("Long path is a required field. Please try again");
	        return false;
	}
	else{
		longstr = document.createform.long.value
		var re = /http:+\S+\.com+/;
		if (!re.test(longstr)){
		 		alert("Please enter correct long URL in the format http://...com");
		 	return false;
		 }
	}
	

    if (document.createform.short.value == '') {
       var x=confirm("You have not entered short path. Do you want it to be automatically created?");
		if (x ==true){
			// document.createform.short.value = getShortValue();
			// alert ("Short path created ",document.createform.short.value);
			return true;
		}	
		else{
			return false;
		}
        
    }
    else{
		shortstr = document.createform.short.value;
		var re = /^[A-Za-z]+$/;
		 if (!re.test(shortstr)){
		 	alert ("Short path can only take alphabets. Please try again");
		 	return false;
		 }
	}
    return true;

}

function getShortValue() {
	var chars = "ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz";
	var string_length = 5;
	var randomstring = '';
	for (var i=0; i<string_length; i++) {
		var rnum = Math.floor(Math.random() * chars.length);
		randomstring += chars.substring(rnum,rnum+1);
	}
	return randomstring;
}

function validateOnDelete(){

  if (document.deleteform.short1.value == '') {
		alert ("Short URL is a required field. Please try again");
	    return false;
	}
return true

}

