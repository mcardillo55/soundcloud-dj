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
	function($scope, $http) {
		$scope.url = "";
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
			$scope.songList.push({"id":0, "url":$scope.url});
			$http.post("http://127.0.0.1:5000/api/playlist", data)
		};
	}
]);