
// CRYPTOSOLARTECH ROI CALCULATOR

$(function () {

        // DATOS DEL PROYECTO
        var CantidadMaxima = 100000;
        var PreIco = 72;    						
        var FaseUno = 60;    						
        var FaseDos = 52;    						
        var FaseTres = 45;    						
        var FaseCuatro = 36;    					
       
        var NumYears = 1;                           

        $("#range").ionRangeSlider({
            hide_min_max: false,
            keyboard: true,
            min: 500,
            max: CantidadMaxima,
            from: 3000,
            to: CantidadMaxima,
            type: 'single',
            step: 50,
            prefix: "€",
            grid: true,
            onStart: function (data) {

            	// INVERTIR AHORA
               	$("#total").html(data.from);
                //Pre-ICO
                $("#roipreico").html((PreIco/100*data.from) + data.from);
                $("#roipreicototal").val(PreIco/100*data.from);
                //Fase 1
                $("#roifaseuno").html((FaseUno/100*data.from) + data.from);
                $("#roifaseunototal").val(FaseUno/100*data.from);
                //Fase 2
                $("#roifasedos").html((FaseDos/100*data.from) + data.from);
                $("#roifasedostotal").val(FaseDos/100*data.from);
                //Fase 3
                $("#roifasetres").html((FaseTres/100*data.from) + data.from);
                $("#roifasetrestotal").val(FaseTres/100*data.from);
                //Fase 4
                $("#roifasecuatro").html((FaseCuatro/100*data.from) + data.from);
                $("#roifasecuatrototal").val(FaseCuatro/100*data.from);
               
            },
            onChange: function (data) {
               	
               	// INVERTIR AHORA
               	$("#total").html(data.from);
                //Pre-ICO
                $("#roipreico").html((PreIco/100*data.from) + data.from);
                $("#roipreicototal").val(PreIco/100*data.from);
                //Fase 1
                $("#roifaseuno").html((FaseUno/100*data.from) + data.from);
                $("#roifaseunototal").val(FaseUno/100*data.from);
                //Fase 2
                $("#roifasedos").html((FaseDos/100*data.from) + data.from);
                $("#roifasedostotal").val(FaseDos/100*data.from);
                //Fase 3
                $("#roifasetres").html((FaseTres/100*data.from) + data.from);
                $("#roifasetrestotal").val(FaseTres/100*data.from);
                //Fase 4
                $("#roifasecuatro").html((FaseCuatro/100*data.from) + data.from);
                $("#roifasecuatrototal").val(FaseCuatro/100*data.from);
            }
        });

    });