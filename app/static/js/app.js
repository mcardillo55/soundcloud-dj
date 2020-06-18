var app;
var socket = io.connect('http://' + document.domain + ':' + location.port);

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
				if (response.success == false) {
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
				$scope.playerUrl = $sce.trustAsResourceUrl('https://w.soundcloud.com/player/?url=' + newSong.url + '&auto_play=true&visual=true');
				//temporary? hack to bind soundcloud listener after DOM update
				$timeout(function() { 
					SC.Widget(myPlayer).bind(SC.Widget.Events.FINISH, 
						function() { 
							rand = Math.floor(Math.random() * $scope.songList.length);
							$scope.changeSong($scope.songList[rand].id);
							$scope.$apply();
						})
					}, 1000);
			} else if (newSong.url.indexOf("youtube") > -1) {
				$scope.playerUrl = $sce.trustAsResourceUrl(newSong.url + "?enablejsapi=1&autoplay=1&origin=" + host);
				//temporary? hack to bind youtube listener after DOM update
				$timeout(function() {
					new YT.Player('myPlayer').addEventListener('onStateChange', function(event){
						if (event.data == YT.PlayerState.ENDED) {
							rand = Math.floor(Math.random() * $scope.songList.length);
							$scope.changeSong($scope.songList[rand].id);
							$scope.$apply();
						}
					});
				}, 1000);
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


