var app;
var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
	//needed for client to recieve server messages
    socket.emit('connect');
});

app = angular.module("app", [])
.config(function($interpolateProvider) {
  // replaces {{ }} with [[ ]] to differentiate from jinja
  $interpolateProvider.startSymbol("[[");
  $interpolateProvider.endSymbol("]]");
})

app.controller('djController', [
	"$scope",
	"$http",
	"$sce",
	"$timeout",
	function($scope, $http, $sce, $timeout) {
		$scope.url = "";
		$scope.flash = "";

		socket.on('new-song', function (data) {
    		$scope.songList.unshift(data);
    		$scope.$apply();
		});

		angular.element(document).ready(function () {
			$scope.SCWidget = SC.Widget(SCPlayer);
			$scope.SCWidget.bind(SC.Widget.Events.FINISH, 
				function() { 
					rand = Math.floor(Math.random() * $scope.songList.length);
					$scope.changeSong($scope.songList[rand].id);
					$scope.$apply();
			});
			$scope.YTWidget = new YT.Player('YTPlayer').addEventListener('onStateChange', function(event){
				if (event.data == YT.PlayerState.ENDED) {
					rand = Math.floor(Math.random() * $scope.songList.length);
					$scope.changeSong($scope.songList[rand].id);
					$scope.$apply();
				}
			});
			console.log("players enabled");
		});


		$http.get(host + "/api/playlist")
		.success(function (response) {
			$scope.responseLength = response.songList.length;
			$scope.songList = response.songList;
			//if list is populated, start playing first track
			if($scope.songList.length > 0) {
				rand = Math.floor(Math.random() * $scope.songList.length);
				$scope.changeSong($scope.songList[rand].id);
			}
		})

		$scope.loadSongs = function () {
			last = $scope.songList[$scope.songList.length-1];
			$http.get(host + "/api/playlist/" + last.id)
			.success(function (response) {
				$scope.responseLength = response.songList.length;
				$scope.songList = $scope.songList.concat(response.songList);
			})
		};

		$scope.addSong = function () {
			newUrl = $scope.url;
			data = {
				"url": $scope.url,
			};
			$http.post(host + "/api/playlist", data)
			.success(function (response) {
				if (response.success == true) {
					$scope.songList.push({"id":response.data.id, "url":response.data.url, "title": response.data.title});
				} else {
					$scope.flashMessage(response.message);
					console.log("invalid url");
				}
			})
		};

		$scope.changeSong = function (songId) {
			for (index = 0; index < $scope.songList.length; index++){
				if ($scope.songList[index].id == songId) {
					newSong =  $scope.songList[index];
					break;
				}
			}
			if (newSong.url.indexOf("soundcloud") > -1) {
				YTPlayer.style.display="none";
				SCPlayer.style.display="block";
				if ($scope.YTWidget) {
					$scope.YTWidget.pauseVideo();
				}
				$scope.SCUrl = $sce.trustAsResourceUrl('https://w.soundcloud.com/player/?url=' + newSong.url + '&auto_play=true&visual=true');
			} else if (newSong.url.indexOf("youtube") > -1) {
				SCPlayer.style.display="none";
				YTPlayer.style.display="block";
				if ($scope.SCWidget) {
					$scope.SCWidget.pause();
				}
				$scope.YTUrl = $sce.trustAsResourceUrl(newSong.url + "?enablejsapi=1&autoplay=1&origin=" + host);
			}
			$scope.curSong = newSong;
		};

		$scope.flashMessage = function (message) {
			console.log("message set to" + message);
			$scope.flash = message;
			$timeout(function () {
				$scope.flash = null;
			}, 5000);
		}
	}
]);


