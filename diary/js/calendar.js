var sel_year = $("#year");
var sel_month = $("#month");
var sel_day = $("#day");

for (var i = 2020; i < 2050; ++i)
	sel_year.append("<option value='" + i + "'>" + i + "</option>");
for (var i = 1; i <= 12; ++i)
	sel_month.append("<option value='" + i + "'>" + i + "</option>");
			
var today = new Date();   
sel_year.val(today.getFullYear()).attr("selected", "selected");
sel_month.val(today.getMonth() + 1).attr("selected", "selected");

setDay();
if (today.getDay() == 0){
	today.setDate(today.getDate() - 2);
}
else if (today.getDay() == 6){
	today.setDate(today.getDate() - 1);
}

sel_year.val(today.getFullYear()).attr("selected", "selected");
sel_month.val(today.getMonth() + 1).attr("selected", "selected");
sel_day.val(today.getDate()).attr("selected", "selected");

function setDay(){
	var year = $("#year option:selected").val();
	var month = $("#month option:selected").val();
	var last_day = new Date(year, month, 0).getDate();
	var week;

	$("#day option").remove();
	for (var i = 1; i <= last_day; ++i){
		week = new Date(year, month, i).getDay();
		if (week == 0 || week == 6)
			continue;
		sel_day.append("<option value='" + i + "'>" + i + "</option>");
	}
}


