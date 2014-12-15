var app = angular.module('acb_photo', ['ngRoute', 'ngAnimate']);

var nav_links = [
	{ page: 'Selected',  title: 'Selected Works', template: 'gallery' },
	{ page: 'Portrait',  title: 'Portraits',      template: 'gallery' },
	{ page: 'Street',    title: 'Street',         template: 'gallery' },
	{ page: 'Landscape', title: 'Landscapes',     template: 'gallery' },
	{ page: 'About',     title: 'About',          template: 'about'   },
	{ page: 'Contact',   title: 'Contact',        template: 'contact' },
];
app.constant('navLinks', nav_links);


function createCachedDataFunction($q, $http, resource_url) {
	var cached_resource;
	var cached = false;
	return function() {
		var defered=$q.defer();
		if( cached ) {
			defered.resolve(cached_resource);
		} else {
			$http.get(resource_url).
				success(function(data, status, headers, config) {
					cached_resource=data;
					cached = true;
					defered.resolve(data)
				}).
				error(function(data, status, headers, conig) {
					defered.reject('Unable to fetch ' + resource_url);
				});
			}
		return defered.promise;
	};
}


app.factory('DataService', ['$q', '$http', function($q, $http) {
	var service={};
	service.get_gallery_contents=createCachedDataFunction($q, $http, '/gallery/files.json');
	return service;
}]);


var LEFT_KEY = 37;
var RIGHT_KEY = 39;
function createGalleryControler(gallery_section) {
	return function($scope, $rootScope, $location, DataService) {

		DataService.get_gallery_contents().then(function(data) {
			$scope.images = _.map(data[gallery_section], function(img) {
				return {
					img: img,
					large: '/gallery/' + img,
					thumb: '/gallery/thumbs/' + img,
				}
			});
			 setTimeout(function(){ resize(); }, 10);
		});


		$scope.selected_image = 0;
		$scope.isCurrentImage = function(index) {
			return index == $scope.selected_image;
		};

		$scope.prevImage = function() {
			if( $scope.selected_image > 0 )
				$scope.selected_image--;
			else
				$scope.selected_image = $scope.images.length - 1;
		}

		$scope.nextImage = function() {
			if( $scope.selected_image < $scope.images.length - 1 )
				$scope.selected_image++;
			else
				$scope.selected_image = 0;
		}

		$scope.$on('key_down_event', function (event, data) {
			if( data.key == LEFT_KEY ) {
				$scope.prevImage();
			}
			if( data.key == RIGHT_KEY ) {
				$scope.nextImage();
			}
		});

		$scope.$watch('selected_image', function() {
			resize();
		});
	};
}


_.each(nav_links, function(nav_link) {
	var ctrl_name = nav_link.page + 'Ctrl';
	var gallery_section = nav_link.page.toLowerCase();
	app.controller(ctrl_name, ['$scope', '$rootScope', '$location', 'DataService',
		createGalleryControler(gallery_section)]);
});


app.controller('AboutCtrl', ['$scope', function($scope) {
}]);


app.controller('ContactCtrl', ['$scope', function($scope) {
}]);


app.controller('MainCtrl', ['$scope', function($scope) {
	$scope.handle_key_down = function(ev) {
		$scope.$broadcast('key_down_event', {key: ev.which});
	};
}]);


app.config(['$routeProvider', 'navLinks', function($routeProvider, navLinks) {
	_.each(navLinks, function(nav_link) {
		$routeProvider.when('/' + nav_link.page, {
			templateUrl: 'partials/' + nav_link.template + '.html',
			controller: nav_link.page + 'Ctrl'
		});
	});
	$routeProvider.otherwise({
		redirectTo: '/Selected'
	});
}]);


app.run(['$rootScope', '$location', 'navLinks', function($rootScope, $location, navLinks) {
	$rootScope.navLinks = navLinks;
	$rootScope.$on('$viewContentLoaded', function() {
		var screenName = location.pathname + location.search + location.hash;
		ga('send', 'screenview', {
			'screenName': screenName
		});
	});
	$rootScope.isActiveRoute = function(route) {
		return route == $location.path();
	};
}]);


window.onresize = window.onload = function() {
	resize();
}


function resize() {
	var visible_height = $(window).height() - $("nav.navbar").height();
	$("div.slide img").each(function() {  
		var image_height = visible_height - 100;
		this.style.maxHeight = image_height + 'px';
	});  
}
