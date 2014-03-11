
 
// jQuery $('document').ready(); function
$('document').ready(function(){

    // Calling LayerSlider on your selected element after the document loaded
   	$('#layerslider').layerSlider({autoStart: false});
   	$('#layerslider').hide();

	$('#startbutton').click(function(){
		$.ajax({
			  url: "/startcall",
			}).done(function() {
				$('#layerslider').show();

			 $('#layerslider').layerSlider({
		 
		    autoStart               : true,
		    responsive              : true,
		    responsiveUnder         : 0,
		    sublayerContainer       : 0,
		    firstLayer              : 1,
		    twoWaySlideshow         : false,
		    randomSlideshow         : false,
		    keybNav                 : true,
		    touchNav                : true,
		    imgPreload              : true,
		    navPrevNext             : true,
		    navStartStop            : true,
		    navButtons              : true,
		    thumbnailNavigation     : 'hover',
		    tnWidth                 : 100,
		    tnHeight                : 60,
		    tnContainerWidth        : '60%',
		    tnActiveOpacity         : 35,
		    tnInactiveOpacity       : 100,
		    hoverPrevNext           : true,
		    hoverBottomNav          : false,
		    skin                    : 'default',
		    skinsPath               : '/layerslider/skins/',
		    pauseOnHover            : true,
		    globalBGColor           : 'transparent',
		    globalBGImage           : false,
		    animateFirstLayer       : false,
		    yourLogo                : false,
		    yourLogoStyle           : 'position: absolute; z-index: 1001; left: 10px; top: 10px;',
		    yourLogoLink            : false,
		    yourLogoTarget          : '_blank',
		    loops                   : 0,
		    forceLoopNum            : true,
		    autoPlayVideos          : true,
		    autoPauseSlideshow      : 'auto',
		    youtubePreview          : 'maxresdefault.jpg',
		    showBarTimer        : false,
		    showCircleTimer     : true,
		 
		    // you can change this settings separately by layers or sublayers with using html style attribute
		 
		    slideDirection          : 'right',
		    slideDelay              : 4000,
		    durationIn              : 1000,
		    durationOut             : 1000,
		    easingIn                : 'easeInOutQuint',
		    easingOut               : 'easeInOutQuint',
		    delayIn                 : 0,
		    delayOut                : 0

			});

			$('#startbutton').hide();

		});


	})
    
	

});
