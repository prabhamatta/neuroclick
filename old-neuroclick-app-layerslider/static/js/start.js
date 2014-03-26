$('document').ready(function(){

$('#startbutton').click(function(){
	console.log("before calling...")
		$.ajax({
			  url: "/startcall",

			}).done(function() {
			console.log("here")
})
	})

})