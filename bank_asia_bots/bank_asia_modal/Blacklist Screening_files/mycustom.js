// $('#P90_CUSTOMER_ID_lov_btn').click(function(){
// 	$('body').after('<div id="pushModal" style="width: 100%; display:none; height: 100%;" class="u-DisplayNone u-Overlay--glass"></div><div id="ui-datepicker-div" class="ui-datepicker ui-widget ui-widget-content ui-helper-clearfix ui-corner-all" tabindex="-1"></div><div tabindex="-1" role="dialog" class="ui-dialog ui-corner-all ui-widget ui-widget-content ui-front ui-dialog--apex ui-dialog—popuplov ui-draggable" aria-describedby="apex_dialog_2" aria-labelledby="ui-id-2" style="position: fixed; height: auto; width: 500px; top: 138px; left: 433px; max-width: 100%;"><div class="ui-dialog-titlebar ui-corner-all ui-widget-header ui-helper-clearfix ui-draggable-handle"><span id="ui-id-2" class="ui-dialog-title">Search Dialog</span><button type="button" class="ui-button ui-corner-all ui-widget ui-button-icon-only ui-dialog-titlebar-close" title="Close"><span class="ui-button-icon ui-icon ui-icon-closethick"></span><span class="ui-button-icon-space"> </span>Close</button></div><div id="apex_dialog_2" class="ui-dialog-content ui-widget-content" style="width: auto; min-height: 0px; max-height: none; height: 451px;"><iframe src="./Blacklist Screeningsearch_files/wwv_flow.html" title="Search Dialog" width="100%" height="100%" style="min-width: 95%;height:100%;" scrolling="auto"></iframe></div></div>');
// })


// $('button[title="Close"]').click(function(){
// 	alert('hello');
// 	$('div[role="dialog"]').css('display', 'none');
// })


// hide modal at page load
$(document).ready(function(){
	var mymodal = $('#mymodal')
	var modalObj = $('div[role="dialog"]')
	var modalAppearObj = $('#P90_CUSTOMER_ID_lov_btn')
	var modalCloseObj;
	

	mymodal.css('display', 'none');
	// modalObj.css('display', 'none');
	// show modal at the click of the button

	modalAppearObj.click(function(){
		mymodal.css('display', 'block');
	})


	if(modalObj.css('display') === 'block'){
		// $('myclosebtn').click(function(){
		// 	alert('hello');
		// 	// $('div[role="dialog"]').css('display', 'none');
		// })
		mymodal.click(function(){
			// alert('hello');
			$(this).css('display', 'none');
		})
	}
})



