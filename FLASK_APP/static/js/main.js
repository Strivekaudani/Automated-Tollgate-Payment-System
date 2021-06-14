 AOS.init({
 	duration: 800,
 	easing: 'slide'
 });


 function setCSSVariablesForWindowDimensions() {

	const elem = document.documentElement;
	const winWidth = window.innerWidth + 'px';
	const winHeight = window.innerHeight + 'px';

	elem.style.setProperty('--window-height', winHeight);
	elem.style.setProperty('--window-width', winWidth);

}

const divLoading = document.createElement('div');
divLoading.style.display = 'none';
divLoading.style.top = 0
divLoading.style.bottom = 0;
divLoading.style.left = 0;
divLoading.style.right = 0;
divLoading.style.position = 'fixed';
divLoading.style.zIndex = 2000;
divLoading.style.alignItems = 'center';
divLoading.style.background = 'white';

const div = document.createElement('div');
div.setAttribute('role', 'status');
div.classList.add('spinner-grow');
div.style.marginLeft = 'calc(var(--window-width) / 2)'

const span = document.createElement('span');
span.classList.add('visually-hidden');

div.append(span);
divLoading.append(div);
document.body.append(divLoading);

function showLoading() {
	divLoading.style.display = 'flex';
}

function hideLoading() {
	divLoading.style.display = 'none';
}

// add axios
const script = document.createElement('script');

script.onload = function() {

	const hideLoadingAfterResponseIsReceived = function(response) {
		hideLoading();
		return response;
	}

	const showLoadingBeforeSendingRequest = function(config) {
		showLoading();
		return config;
	}

	const hideLoadingWhenAnErrorOccurs = function(err) {
		hideLoading();
		throw err;	
	}

	axios.interceptors.request.use(showLoadingBeforeSendingRequest);
	axios.interceptors.response.use(hideLoadingAfterResponseIsReceived, hideLoadingWhenAnErrorOccurs);

}
script.src ='/static/js/axios.min.js';

document.body.append(script);



window.addEventListener('resize', setCSSVariablesForWindowDimensions);
setCSSVariablesForWindowDimensions();


// functions

function getRequestErrorMessage(error) {
	const { response } = error;
	return response.data.toString() || response.statusText || 'Something went wrong!!'
}

/* ==============================================================
	# API FUNCTIONS
============================================================== */

async function openGateTemporarily() {

	try {
		await axios.post('/api/open-gate-command');
	} catch (err) {
		const error_msg = getRequestErrorMessage(err);
		alert(error_msg);
	}
}

async function scanCarPlates() {

	try {
		await axios.get('/api/scanned-plates');
	} catch (err) {
		const error_msg = getRequestErrorMessage(err);
		alert(error_msg);
	} 
}

// function getNumberPlate(elem) {

// 	let number_plate = elem.getAttribute('data-number-plate');

// 	while (number_plate === null && elem.tagName !== 'BODY') {
// 		elem = elem.parentNode;
// 		number_plate = elem.getAttribute('data-number-plate')
// 	}

// 	return number_plate;
// }

// async function payForThisCar(elem) {
	
// 	const number_plate = getNumberPlate(elem);

// 	try {
// 		await axios.post(`/api/cars/${number_plate}/payment`);

// 		elem.innerHTML = 'PAID';
// 		elem.disabled = true;

// 		hFunds = document.getElementById('funds');
// 		funds = parseFloat(hFunds.innerHTML.trim().substr(1)) - 10;
// 		hFunds.innerHTML = '$' + funds.toFixed(2)

// 	} catch (err) {
// 		const error_msg = getRequestErrorMessage(err)
// 		alert(error_msg);
// 	}

// }


// /* ==============================================================
// 	# LINK MANAGEMENT
// ============================================================== */

// (function() {

// 	function addLink(path, display) {
// 		const a = document.createElement('a');
// 		a.href = path;
// 		a.innerHTML = display
// 		a.classList.add('nav-link');

// 		const li = document.createElement('li');
// 		li.classList.add('nav-item');
// 		li.append(a)

// 		if (path === window.location.pathname)
// 			li.classList.add('active');

// 		navUl.append(li);
// 	}

// 	const navUl = document.querySelector('nav ul');

// 	window.navLinks.forEach(link => {
// 		const { path, caption } = links;
// 		addLink(path, caption);
// 	})
	
// })()


(function($) {

	"use strict";

	var isMobile = {
		Android: function() {
			return navigator.userAgent.match(/Android/i);
		},
			BlackBerry: function() {
			return navigator.userAgent.match(/BlackBerry/i);
		},
			iOS: function() {
			return navigator.userAgent.match(/iPhone|iPad|iPod/i);
		},
			Opera: function() {
			return navigator.userAgent.match(/Opera Mini/i);
		},
			Windows: function() {
			return navigator.userAgent.match(/IEMobile/i);
		},
			any: function() {
			return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
		}
	};


	$(window).stellar({
    responsive: true,
    parallaxBackgrounds: true,
    parallaxElements: true,
    horizontalScrolling: false,
    hideDistantElements: false,
    scrollProperty: 'scroll'
  });


	var fullHeight = function() {

		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function(){
			$('.js-fullheight').css('height', $(window).height());
		});

	};
	fullHeight();

	// loader
	var loader = function() {
		setTimeout(function() { 
			if($('#ftco-loader').length > 0) {
				$('#ftco-loader').removeClass('show');
			}
		}, 1);
	};
	loader();

	// Scrollax
   $.Scrollax();

	var carousel = function() {
		$('.home-slider').owlCarousel({
	    loop:true,
	    autoplay: true,
	    margin:0,
	    animateOut: 'fadeOut',
	    animateIn: 'fadeIn',
	    nav:false,
	    autoplayHoverPause: false,
	    items: 1,
	    navText : ["<span class='ion-md-arrow-back'></span>","<span class='ion-chevron-right'></span>"],
	    responsive:{
	      0:{
	        items:1
	      },
	      600:{
	        items:1
	      },
	      1000:{
	        items:1
	      }
	    }
		});
		$('.carousel-testimony').owlCarousel({
			autoplay: true,
			autoHeight: true,
			center: true,
			loop: true,
			items:1,
			margin: 30,
			stagePadding: 0,
			nav: false,
			dots: true,
			navText: ['<span class="ion-ios-arrow-back">', '<span class="ion-ios-arrow-forward">'],
			responsive:{
				0:{
					items: 1
				},
				600:{
					items: 1
				},
				1000:{
					items: 1
				}
			}
		});
		$('.carousel-team').owlCarousel({
			autoplay: true,
			autoHeight: true,
			items:1,
			margin: 30,
			stagePadding: 0,
			nav: false,
			dots: true,
			navText: ['<span class="ion-ios-arrow-back">', '<span class="ion-ios-arrow-forward">'],
			responsive:{
				0:{
					items: 1
				},
				600:{
					items: 3
				},
				1000:{
					items: 4
				}
			}
		});
	};
	carousel();

	$('nav .dropdown').hover(function(){
		var $this = $(this);
		// 	 timer;
		// clearTimeout(timer);
		$this.addClass('show');
		$this.find('> a').attr('aria-expanded', true);
		// $this.find('.dropdown-menu').addClass('animated-fast fadeInUp show');
		$this.find('.dropdown-menu').addClass('show');
	}, function(){
		var $this = $(this);
			// timer;
		// timer = setTimeout(function(){
			$this.removeClass('show');
			$this.find('> a').attr('aria-expanded', false);
			// $this.find('.dropdown-menu').removeClass('animated-fast fadeInUp show');
			$this.find('.dropdown-menu').removeClass('show');
		// }, 100);
	});


	$('#dropdown04').on('show.bs.dropdown', function () {
	  console.log('show');
	});

	// scroll
	var scrollWindow = function() {
		$(window).scroll(function(){
			var $w = $(this),
					st = $w.scrollTop(),
					navbar = $('.ftco_navbar'),
					sd = $('.js-scroll-wrap');

			if (st > 150) {
				if ( !navbar.hasClass('scrolled') ) {
					navbar.addClass('scrolled');	
				}
			} 
			if (st < 150) {
				if ( navbar.hasClass('scrolled') ) {
					navbar.removeClass('scrolled sleep');
				}
			} 
			if ( st > 350 ) {
				if ( !navbar.hasClass('awake') ) {
					navbar.addClass('awake');	
				}
				
				if(sd.length > 0) {
					sd.addClass('sleep');
				}
			}
			if ( st < 350 ) {
				if ( navbar.hasClass('awake') ) {
					navbar.removeClass('awake');
					navbar.addClass('sleep');
				}
				if(sd.length > 0) {
					sd.removeClass('sleep');
				}
			}
		});
	};
	scrollWindow();

	var isMobile = {
		Android: function() {
			return navigator.userAgent.match(/Android/i);
		},
			BlackBerry: function() {
			return navigator.userAgent.match(/BlackBerry/i);
		},
			iOS: function() {
			return navigator.userAgent.match(/iPhone|iPad|iPod/i);
		},
			Opera: function() {
			return navigator.userAgent.match(/Opera Mini/i);
		},
			Windows: function() {
			return navigator.userAgent.match(/IEMobile/i);
		},
			any: function() {
			return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
		}
	};

	var counter = function() {
		
		$('#section-counter, .hero-wrap, .ftco-counter, .ftco-volunteer').waypoint( function( direction ) {

			if( direction === 'down' && !$(this.element).hasClass('ftco-animated') ) {

				var comma_separator_number_step = $.animateNumber.numberStepFactories.separator(',')
				$('.number').each(function(){
					var $this = $(this),
						num = $this.data('number');
						console.log(num);
					$this.animateNumber(
					  {
					    number: num,
					    numberStep: comma_separator_number_step
					  }, 7000
					);
				});
				
			}

		} , { offset: '95%' } );

	}
	counter();


	var contentWayPoint = function() {
		var i = 0;
		$('.ftco-animate').waypoint( function( direction ) {

			if( direction === 'down' && !$(this.element).hasClass('ftco-animated') ) {
				
				i++;

				$(this.element).addClass('item-animate');
				setTimeout(function(){

					$('body .ftco-animate.item-animate').each(function(k){
						var el = $(this);
						setTimeout( function () {
							var effect = el.data('animate-effect');
							if ( effect === 'fadeIn') {
								el.addClass('fadeIn ftco-animated');
							} else if ( effect === 'fadeInLeft') {
								el.addClass('fadeInLeft ftco-animated');
							} else if ( effect === 'fadeInRight') {
								el.addClass('fadeInRight ftco-animated');
							} else {
								el.addClass('fadeInUp ftco-animated');
							}
							el.removeClass('item-animate');
						},  k * 50, 'easeInOutExpo' );
					});
					
				}, 100);
				
			}

		} , { offset: '95%' } );
	};
	contentWayPoint();


	// navigation
	var OnePageNav = function() {
		$(".smoothscroll[href^='#'], #ftco-nav ul li a[href^='#']").on('click', function(e) {
		 	e.preventDefault();

		 	var hash = this.hash,
		 			navToggler = $('.navbar-toggler');
		 	$('html, body').animate({
		    scrollTop: $(hash).offset().top
		  }, 700, 'easeInOutExpo', function(){
		    window.location.hash = hash;
		  });


		  if ( navToggler.is(':visible') ) {
		  	navToggler.click();
		  }
		});
		$('body').on('activate.bs.scrollspy', function () {
		  console.log('nice');
		})
	};
	OnePageNav();


	// magnific popup
	$('.image-popup').magnificPopup({
    type: 'image',
    closeOnContentClick: true,
    closeBtnInside: false,
    fixedContentPos: true,
    mainClass: 'mfp-no-margins mfp-with-zoom', // class to remove default margin from left and right side
     gallery: {
      enabled: true,
      navigateByImgClick: true,
      preload: [0,1] // Will preload 0 - before current, and 1 after the current image
    },
    image: {
      verticalFit: true
    },
    zoom: {
      enabled: true,
      duration: 300 // don't foget to change the duration also in CSS
    }
  });

  $('.popup-youtube, .popup-vimeo, .popup-gmaps').magnificPopup({
    disableOn: 700,
    type: 'iframe',
    mainClass: 'mfp-fade',
    removalDelay: 160,
    preloader: false,

    fixedContentPos: false
  });

  $('.appointment_date').datepicker({
	  'format': 'm/d/yyyy',
	  'autoclose': true
	});

	$('.appointment_time').timepicker();


})(jQuery);
