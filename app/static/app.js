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
	function($scope, $http, $sce) {
		$scope.url = "";
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
			if (newUrl.indexOf("soundcloud") > -1 || newUrl.indexOf("youtube") > -1) {
				data = {
					"url": $scope.url,
				};
				$http.post("http://127.0.0.1:5000/api/playlist", data)
				.success(function (response) {
					$scope.songList.push({"id":response.data.id, "url":response.data.url, "title": response.data.title});
				})
			}
		};

		$scope.changeSong = function (songId) {
			newSong =  $scope.songList[songId - 1];
			if (newSong.url.indexOf("soundcloud") > -1) {
				$scope.playerUrl = $sce.trustAsResourceUrl('https://w.soundcloud.com/player/?url=' + newSong.url + '&amp;auto_play=true&amp;hide_related=false&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false&amp;visual=true');
			} else if (newSong.url.indexOf("youtube") > -1) {
				$scope.playerUrl = $sce.trustAsResourceUrl(newSong.url + "?autoplay=1");
				console.log($scope.playerUrl);
			}
		};
	}
]);