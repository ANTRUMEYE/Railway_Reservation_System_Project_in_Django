 var app=angular.module("Myapp",[])
                        .controller("MyController",function($scope,$http){
     $scope.tr=[];
     $scope.submitreq=function(){
     var u1="https://api.railwayapi.com/v2/between/source/";
     var u2="/dest/";
     var u3="/date/";
     var u4="/apikey/6j2lxp5khs";
     $scope.api="/apikey/6j2lxp5khs";
     var url=u1+$scope.src+u2+$scope.dest+u3+$scope.dt+u4;
     document.getElementById('table1').style.display="none";
    document.getElementById('table2').style.display="none";	
    console.log(url);
     $http.get(url).then(function(response)
     {
     	var ob=response.data;
     	console.log(ob);
     	var tr=[];

     	
     	for(x in ob['trains'])
     	{	
     		tr.push({'nb':ob.trains[x].number,'nm':ob.trains[x].name,'dtime':ob.trains[x].src_departure_time,'atime':ob.trains[x].dest_arrival_time});
     	}
     	$scope.tr=tr;
     	
     	document.getElementById('table2').style.display="block";	
     	
     });

 
	
	}
	$scope.getseat=function(no,cls){
		var v1="https://api.railwayapi.com/v2/check-seat/train/"+no+"/source/"+$scope.src+"/dest/"+$scope.dest+"/date/"+$scope.dt+"/pref/"+cls+"/quota/"+$scope.qta+"/"+$scope.api;
		$scope.disp=[];
		document.getElementById('table1').style.display="none";
		document.getElementById('Res').innerHTML="";
		$http.get(v1).then(function(response)
		{	
			var z=response.data;
			var y=z.availability;
			console.log(z);
			console.log(v1);
			if(z.response_code==200)
			{$scope.disp=y;
				$scope.ctr=no;
				document.getElementById('table1').style.display="block";}
			else
			{
				document.getElementById('Res').innerHTML="This class is not available";
			}



		});
	};
});
					
                
				
             