$(function () {

    $("#tabs").tabs();

});

/**********Drug Search Search********/
var drugSearchTerm = null;
function search_drug(value) {
    if (drugSearchTerm != null) drugSearchTerm.abort();
    if (value.length >= 3) {
        $("#intialDrugList").dataTable().fnClearTable(true);
        drugSearchTerm = $.ajax({
            url: '',
            data: {'search_term': value},
            success: function (data) {
                resultTable = "";
                $.map(data, function (obj, i) {
                    var _href = obj ? "prescribe-drug" : "prescribe-drug";
                    var link = "<a href='"+_href+".html?drugid="+obj.id+"'>prescribe drug</a>";
                    var name = "<a href='"+_href+".html?drugid="+obj.id+"'>"+obj.name+"</a>";
                    $("#intialDrugList").dataTable().fnAddData([name, link]);
                });
            }
        });
    } else {
        $("#intialDrugList").dataTable().fnClearTable(true);
    }
}
/**********End Drug Search********/