function formata_data(caracter)
    {
    var nTecla = 0;
	if (document.all) {
		nTecla = caracter.keyCode;
    }
	else
	{
     	nTecla = caracter.which;
    }
    if( nTecla == 8 ){
        return true;
    }
    else{
    switch (document.form.dataCert.value.length) {
        case 2:
                document.form.dataCert.value = document.form.dataCert.value + "/";
                break;
        case 5:
                document.form.dataCert.value = document.form.dataCert.value + "/";
                break;
}
}
}

function Apenas_Numeros(caracter)
{
	var nTecla = 0;
	if (document.all) {
		nTecla = caracter.keyCode;
    }
	else
	{
     	nTecla = caracter.which;
    }
	if ((nTecla> 47 && nTecla <58)
    || nTecla == 8 || nTecla == 127
    || nTecla == 0 || nTecla == 9  // 0 == Tab
    || nTecla == 13) { // 13 == Enter
		return true;
    }
	else
	{
    	return false;
    }
}
