// Scroll to top on page refresh
$(window).unload(function() {
    $('body').scrollTop(0);
    $(document).scrollTop(0);
});

$(document).ready(function() {

    // Scroll to job post
    setTimeout(function() {
        if(window.location.hash) {
            $('html, body').delay(1000).animate({scrollTop: $('.job-postings').offset().top - 225}, 'slow');

            $('.current').removeClass('current');
            var hash = $('#job-' + window.location.hash.substring(1)); //Puts hash in variable, and removes the # character
            var targetClass = hash.attr("class");
            $(hash).addClass('current');
            $('.' + targetClass).addClass('current');

            return false;
        }
    }, 1);

    $('.hero article').delay(400).animate({'margin-top': -40, opacity: 1}, 500);

    // Mobile menu
    $('#menu-button').on('click', function(e) {
        $('#menu').slideToggle(250);
        e.preventDefault();
    });

    // Login menu
    $('#login-button').on('click', function(e) {
        if ($(window).width()<972) {
            $('#menu').slideToggle(250);
            $('.login-panel, .login-black').fadeIn(250, function () {
                document.forms['login-form'].elements['login-email'].focus();
            });
        } else if ($(window).width()>=972) {
            $('.login-panel').slideToggle(250, function () {
                document.forms['login-form'].elements['login-email'].focus();
            });
        }
        e.preventDefault();
    });

    $('.login-black').on('click', function() {
        $('.login-black, .login-panel').fadeOut(250);
    });


    // Show job posts
    $('.list-of-jobs li').on('click', function() {
        $('.current').removeClass('current');
        var clickedClass = $(this).attr("class");
        $('.' + clickedClass).addClass('current');
    });

    var pathname = window.location.pathname;
    var currentLocation = pathname.substring(pathname.lastIndexOf('/') + 1);

    // Navigation highlighting
    $('nav a').each(function() {
        if ($(this).attr('href') === currentLocation) {
            $(this).addClass('current');
        }
    });

    // Scroll to buttons
    function scrollToAnchor(aid) {
        var aTag = $("a[name='" + aid + "']");
        $('html, body').animate({scrollTop: aTag.offset().top - 280}, 'slow');
    }

    // Scrolling buttons
    $('.scrolling').on('click', function(e) {
        var target = $(this).attr('id');
        var scrolling = $('#scrolling-' + target); //Puts hash in variable, and removes the # character
        $('html, body').delay(200).animate({scrollTop: scrolling.offset().top - 100}, 'slow');
        e.preventDefault();
    });

    // Show different fields on 'support' selection
    $('#contact-purpose').on('change',function(){
        if( $(this).val()==="Support"){
            $(".contact-support").show();
            $(".contact-reg").hide();
        } else{
            $(".contact-support").hide();
            $(".contact-reg").show();
        }
    });

    // Disable form options
    $("option[value='Purpose of Contact *'], option[value='What product were you using?'], option[value='How do you feel?']").attr("disabled", "disabled");

    // Location of the close quote
    var quotePos = $('.rquote').parent().width()-150;
    $('.rquote').css('right', quotePos * -1);

    // Do not scroll hero on mobile
    var isMobile = {
    Android: function() {
        return navigator.userAgent.match(/Android/i) ? true : false;
    },
    BlackBerry: function() {
        return navigator.userAgent.match(/BlackBerry/i) ? true : false;
    },
    iOS: function() {
        return navigator.userAgent.match(/iPhone|iPad|iPod/i) ? true : false;
    },
    Windows: function() {
        return navigator.userAgent.match(/IEMobile/i) ? true : false;
    },
    any: function() {
        return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Windows());
    }
    };

    $(function(){
        if(! isMobile.any()){
            // Fading hero text on scroll
            $(window).scroll(function() {
                var height = $(this).height();
                var scrollTop = $(this).scrollTop();
                var opacity = 1;

                if (scrollTop < 300 && scrollTop > 30) {
                    opacity = 1 - Math.floor(scrollTop) / 180 + 0.15;
                } else if (scrollTop <= 30) {
                    opacity = 1;
                } else {
                    opacity = 0;
                }
                $('.hero article, .shade').css('opacity', opacity);
            });
        }
    });
});


/* Placeholders.js v2.1.0 */
!function(a){"use strict";function b(a,b,c){return a.addEventListener?a.addEventListener(b,c,!1):a.attachEvent?a.attachEvent("on"+b,c):void 0}function c(a,b){var c,d;for(c=0,d=a.length;d>c;c++)if(a[c]===b)return!0;return!1}function d(a,b){var c;a.createTextRange?(c=a.createTextRange(),c.move("character",b),c.select()):a.selectionStart&&(a.focus(),a.setSelectionRange(b,b))}function e(a,b){try{return a.type=b,!0}catch(c){return!1}}a.Placeholders={Utils:{addEventListener:b,inArray:c,moveCaret:d,changeType:e}}}(this),function(a){"use strict";function b(){}function c(a){var b;return a.value===a.getAttribute(G)&&"true"===a.getAttribute(H)?(a.setAttribute(H,"false"),a.value="",a.className=a.className.replace(F,""),b=a.getAttribute(I),b&&(a.type=b),!0):!1}function d(a){var b,c=a.getAttribute(G);return""===a.value&&c?(a.setAttribute(H,"true"),a.value=c,a.className+=" "+E,b=a.getAttribute(I),b?a.type="text":"password"===a.type&&R.changeType(a,"text")&&a.setAttribute(I,"password"),!0):!1}function e(a,b){var c,d,e,f,g;if(a&&a.getAttribute(G))b(a);else for(c=a?a.getElementsByTagName("input"):o,d=a?a.getElementsByTagName("textarea"):p,g=0,f=c.length+d.length;f>g;g++)e=g<c.length?c[g]:d[g-c.length],b(e)}function f(a){e(a,c)}function g(a){e(a,d)}function h(a){return function(){q&&a.value===a.getAttribute(G)&&"true"===a.getAttribute(H)?R.moveCaret(a,0):c(a)}}function i(a){return function(){d(a)}}function j(a){return function(b){return s=a.value,"true"===a.getAttribute(H)&&s===a.getAttribute(G)&&R.inArray(C,b.keyCode)?(b.preventDefault&&b.preventDefault(),!1):void 0}}function k(a){return function(){var b;"true"===a.getAttribute(H)&&a.value!==s&&(a.className=a.className.replace(F,""),a.value=a.value.replace(a.getAttribute(G),""),a.setAttribute(H,!1),b=a.getAttribute(I),b&&(a.type=b)),""===a.value&&(a.blur(),R.moveCaret(a,0))}}function l(a){return function(){a===document.activeElement&&a.value===a.getAttribute(G)&&"true"===a.getAttribute(H)&&R.moveCaret(a,0)}}function m(a){return function(){f(a)}}function n(a){a.form&&(x=a.form,x.getAttribute(J)||(R.addEventListener(x,"submit",m(x)),x.setAttribute(J,"true"))),R.addEventListener(a,"focus",h(a)),R.addEventListener(a,"blur",i(a)),q&&(R.addEventListener(a,"keydown",j(a)),R.addEventListener(a,"keyup",k(a)),R.addEventListener(a,"click",l(a))),a.setAttribute(K,"true"),a.setAttribute(G,v),d(a)}var o,p,q,r,s,t,u,v,w,x,y,z,A,B=["text","search","url","tel","email","password","number","textarea"],C=[27,33,34,35,36,37,38,39,40,8,46],D="#ccc",E="placeholdersjs",F=new RegExp("(?:^|\\s)"+E+"(?!\\S)"),G="data-placeholder-value",H="data-placeholder-active",I="data-placeholder-type",J="data-placeholder-submit",K="data-placeholder-bound",L="data-placeholder-focus",M="data-placeholder-live",N=document.createElement("input"),O=document.getElementsByTagName("head")[0],P=document.documentElement,Q=a.Placeholders,R=Q.Utils;if(Q.nativeSupport=void 0!==N.placeholder,!Q.nativeSupport){for(o=document.getElementsByTagName("input"),p=document.getElementsByTagName("textarea"),q="false"===P.getAttribute(L),r="false"!==P.getAttribute(M),t=document.createElement("style"),t.type="text/css",u=document.createTextNode("."+E+" { color:"+D+"; }"),t.styleSheet?t.styleSheet.cssText=u.nodeValue:t.appendChild(u),O.insertBefore(t,O.firstChild),A=0,z=o.length+p.length;z>A;A++)y=A<o.length?o[A]:p[A-o.length],v=y.attributes.placeholder,v&&(v=v.nodeValue,v&&R.inArray(B,y.type)&&n(y));w=setInterval(function(){for(A=0,z=o.length+p.length;z>A;A++)y=A<o.length?o[A]:p[A-o.length],v=y.attributes.placeholder,v&&(v=v.nodeValue,v&&R.inArray(B,y.type)&&(y.getAttribute(K)||n(y),(v!==y.getAttribute(G)||"password"===y.type&&!y.getAttribute(I))&&("password"===y.type&&!y.getAttribute(I)&&R.changeType(y,"text")&&y.setAttribute(I,"password"),y.value===y.getAttribute(G)&&(y.value=v),y.setAttribute(G,v))));r||clearInterval(w)},100)}Q.disable=Q.nativeSupport?b:f,Q.enable=Q.nativeSupport?b:g}(this);

    $(window).resize(function () {
        if ($(window).width()<972) {
            // console.log($(window).width());
            if($('.login-panel').is(':visible')) {
                $('#menu').hide(250);
                $('.login-black').show();
            }
        } else if ($(window).width()>=972) {
            $('#menu').show();
            $('.login-black').hide();
        }
    });
