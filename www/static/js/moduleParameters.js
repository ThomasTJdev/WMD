
$( function() {
    $( "#dialog" ).dialog({
        autoOpen: false,
        show: {
          effect: "blind",
          duration: 500
        },
        hide: {
          effect: "slideUp",
          duration: 500
        },
        position: { my: 'top', at: 'top+100' },
        minWidth: 370
    });
});

function startDialog(elem) {
    var modulename = elem.id
    loadModuleParameters(modulename);
}

function loadModuleParameters(modulename) {
    $( "#dialog" ).dialog({
        title: modulename
    });
    $('.ui-dialog .ui-dialog-buttonpane').hide()
    $.ajaxSetup ({
        cache: false
    });
    var ajax_load = "<img src='http://automobiles.honda.com/images/current-offers/small-loading.gif' alt='loading...' />";
    var loadUrl = '/start?module=' + modulename;

    $( "#dialog" ).dialog( "open" );

    $( "#dialog" ).html(ajax_load).load(loadUrl);

    $( "#dialog" ).dialog({
        buttons: {
            Ok: function() {
                $( this ).dialog( "close" );
            }
        }
    });
};
