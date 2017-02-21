$(function(){

	// Define function to add transactions/update money
	function logTransaction(){
    
	};



  function abortTransaction() {
    if ($started === true) {
      switchRow();
      // delete text
      var $listItem = document.getElementById($itemCount);
      // $listItem.value = '';
      delete $listItem;
      return;
    }
    else {
      return;
    }
  }


	// Call function when enter key is pressed
	$(document).on('keypress', function(e){
		if(e.which == 13) {
      if ($started == true) {
		    logText();
      }
      else
        logTransaction();
		}
	});


  $(document).keyup(function(e) {
    if(e.keyCode == 27) {
        abortTransaction();
    }
  });

});
