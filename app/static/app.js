var app;
app = angular.module("app", [])
.config(function($interpolateProvider) {
  /* $interpolateProvider 
   * we need replace {{ }} with  [[ ]]
   * */
  $interpolateProvider.startSymbol("[[");
  $interpolateProvider.endSymbol("]]");
})

app.controller('djController', [
	"$scope",
	"$http",
	"$sce",
	function($scope, $http, $sce) {
		$scope.url = "";
		$scope.songEmbed = $sce.trustAsHtml('<iframe width="420" height="450" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https://soundcloud.com/nokturnalist/lee-foss-mk-live-the-mixmag-dj-lab-2013-06-07&amp;auto_play=true&amp;hide_related=false&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false&amp;visual=true"></iframe>');
		$http.get("http://127.0.0.1:5000/api/playlist")
		.success(function (response) {
			$scope.songList = response.songList;
			console.log("success");
		})
		/*for (var song in $scope.songList) {
			console.log(song.url);
		}*/
		$scope.addSong = function () {
			data = {
				"url": $scope.url
			};
			$scope.songList.push({"id":$scope.songList.length+1, "url":$scope.url});
			$http.post("http://127.0.0.1:5000/api/playlist", data)
		};

		$scope.changeSong = function (songId) {
			var newSong =  $scope.songList[songId - 1];
			$scope.songEmbed = $sce.trustAsHtml('<iframe width=“420” height="450" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=' + newSong.url + '&amp;auto_play=true&amp;hide_related=false&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false&amp;visual=true"></iframe>');
		};
	}
]);