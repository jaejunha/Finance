var count, divide, probability, win, loss, ret;

function cal(){
	if (document.getElementById("count").value != null)
		count = Number(document.getElementById("count").value);
	
	if (document.getElementById("divide").value != null)
		divide = Number(document.getElementById("divide").value);

	if (document.getElementById("probability").value != null)
		probability = Number(document.getElementById("probability").value);
	if (document.getElementById("win").value != null)
		win = Number(document.getElementById("win").value);
				
	if (document.getElementById("loss").value != null)
		loss = Number(document.getElementById("loss").value);
	
	if (document.querySelector('input[name="simple"]:checked').value == "s")
		ret = (probability / 100.0 * (win - 0.3) / divide + (100 - probability) / 100.0 * (loss - 0.3) / divide) * divide * count;
	else
		ret = (Math.pow( Math.pow( 1 + (win - 0.3) / 100.0 / divide, probability / 100.0 ) * Math.pow( 1 + (loss - 0.3) / 100.0 / divide, (100 - probability) / 100.0 ), divide * count) - 1) * 100.0;
	document.getElementById("result").innerText = "결과(총 " + count * divide + "회 매매): " + ret + " %";
}
setInterval("cal()", 1000);

