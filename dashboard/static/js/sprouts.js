$(function() {

	var pageHeight = $(window).height(),
		pageWidth = $(window).width();

	setHeight();

	$(window).resize(function() {
		setHeight();
	});

	function setHeight() {
		if (pageWidth > 480) {
			$('img.app_store').css({'margin-top':(pageHeight*1/4)+'px'});
			$('.team .well').css({'min-height':((pageHeight-164)+'px')});
			$('.about .well').css({'min-height':((pageHeight-164)+'px')});
			// $('.well').css({'min-height':((pageHeight-164)+'px')});
		}
		$('.home').css({'min-height':(pageHeight-62)+'px'});
	}

	Parse.initialize("rbVL4eTEwdq7DQ3UxDgnBp4G394L9cejopymUPhl", "tsHq7ypXeAxrEr0TW72yhteFrYwXPzZPV9d19uzV");

	$('#beta').submit(function(event) {
		var BetaUser = Parse.Object.extend("BetaUser"),
			betaUser = new BetaUser();

		betaUser.save( {
			email: $('#inputEmail').val(),
			udid: udid = $('#inputUDID').val()
		}, {
			success: function(betaUser) {
				console.log('info saved');
			},
			error: function(betaUser, error) {
				console.log('unable to save');
			}
		});
		
		return false;
	});

	$('#submit_button').click(function() {
		$('#beta').addClass('hidden');
		$('#thanks').removeClass('hidden');
	});

});