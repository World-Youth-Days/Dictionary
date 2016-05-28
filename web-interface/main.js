$(document).ready(function() {
    
    update();
    
    //Languages input events
    $(".from-radio").change(function() {
        $("#language-from .radio-text").text($(this).val().substr(5));
        $.get("language-pair.php?from="+$(this).val(), function(data) {
            $("#language-to-ul li").hide();
            if (data == "") {
                $("#to-none-li").show();
            }
            data = data.split(";");
            for (i=0; i<data.length; i++) {
                $("#"+data[i]+"-li").show();
            }
            $("#language-to").prop("disabled", false);
        })
    })
    $(".to-radio").change(function() {
        $("#language-to .radio-text").text($(this).val().substr(3));
    })
    
    //Checkboxes for tags
    $(".tag-checkbox").change(function() {
        $("#search_input_value").val("");
        $("#search_input div").removeClass("is-dirty");
        tags = "";
        $(".tag-checkbox:checked").each(function() {
            tags+=$("label[for='"+$(this).attr('id')+"'] .mdl-checkbox__label").text()+";";
        });
        tags = tags.substring(0, tags.length-1);
        location.hash = "tags;"+$("#hardness-min").val()+";"+$("#hardness-max").val()+";"+tags;
    });
    
    //Search input events
    $("#search_button_click").click(function() {
        query = $("#search_input_value").val();
        location.hash = "search;"+$("#hardness-min").val()+";"+$("#hardness-max").val()+";"+query;
    });
    $("#search_input_value").keyup(function(e){
        if(e.keyCode == 13) {
            query = $("#search_input_value").val();
            location.hash = "search;"+$("#hardness-min").val()+";"+$("#hardness-max").val()+";"+query;
        }
    });
    
    //Level input events
    $("#hardness-min").on("input", function() {
        $("#hardness-val-min").text($(this).val());
        data = location.hash.split(";");
        data[1] = $(this).val();
        location.hash = data.join(";");
    });
    $("#hardness-max").on("input", function() {
        $("#hardness-val-max").text($(this).val());
        data = location.hash.split(";");
        data[2] = $(this).val();
        location.hash = data.join(";");
    });
    
    //Some misc functions
    function hideAll() {
        $(".communication").hide();
    }
    $(window).on('hashchange',function(){ 
        update();
    });
    
    //Main update function
    function update() {
        $("#loading").stop();
        $("#loading").fadeIn("slow");
        data = location.hash.split(";");
        data[0] = data[0].substring(1, data[0].length);
        mode = data[0];
        //Tags mode
        if (mode=="tags") {
            hideAll();
            tags="";
            $(".tag-checkbox").prop('checked', false);
            for (i=3; i<data.length; i++) {
                tags += data[i] + ";"
                $("#checkbox-"+data[i]).prop('checked', true);
            }
            $(".tag-checkbox").each(function() {
                if($(this).prop('checked')) {
                    $(this).parent().addClass("is-checked");
                } else {
                    $(this).parent().removeClass("is-checked");
                }
            });
            $("#hardness-min").val(data[1]);
            $("#hardness-val-min").text(data[1]);
            $("#hardness-max").val(data[2]);
            $("#hardness-val-max").text(data[2]);
            tags = tags.substring(0, tags.length-1);
            $.get("query.php?tag="+tags+"&lmin="+data[1]+"&lmax="+data[2], function(data) {
                if (data == "//ABC//") {
                    $("#words-table-body").html("");
                    $("#communication-choose-tags").show();
                } else {
                    $("#words-table-body").html(data);
                }
                $("#loading").stop();
                $("#loading").fadeOut("slow");
            });
        //Search mode
        } else if (mode=="search") {
            hideAll();
            $(".tag-checkbox").each(function() {
                $(this).parent().removeClass("is-checked");
                $(this).prop('checked', false);
            });
            $.get("search.php?search="+data[3]+"&lmin="+data[1]+"&lmax="+data[2], function(data) {
                if (data == "//ABC//") {
                    $("#words-table-body").html("");
                    $("#communication-nothing-found").show();
                } else {
                    $("#words-table-body").html(data);
                }
                $("#loading").stop();
                $("#loading").fadeOut("slow");
            });
        }
    }
});