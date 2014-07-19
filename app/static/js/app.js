var app;
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

		$http.get("http://127.0.0.1:5000/api/playlist")
		.success(function (response) {
			$scope.songList = response.songList;
			//if list is populated, start playing first track
			if($scope.songList.length > 0) {
				$scope.changeSong($scope.songList[0].id);
			}
		})

		$scope.addSong = function () {
			newUrl = $scope.url;
			data = {
				"url": $scope.url,
			};
			$http.post("http://127.0.0.1:5000/api/playlist", data)
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
			newSong =  $scope.songList[songId - 1];
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
				$scope.playerUrl = $sce.trustAsResourceUrl(newSong.url + "?enablejsapi=1&autoplay=1&origin=http://127.0.0.1:5000");
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
			$scope.curSongId = songId;
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


