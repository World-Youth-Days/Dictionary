$(document).ready(function() {
    
    update();
    
    if($("input[name='options-from']:checked").val()!=undefined && $("input[name='options-to']:checked").val()!=undefined) {
        $.get("tags-language.php?from="+$("input[name='options-from']:checked").val()+"&to="+$("input[name='options-to']:checked").val(), function(data) {
            if (data!="\\ABC\\") {
                data = data.split(";");
                for (i=0; i<data.length; i++) {
                    $("#checkbox-"+data[i]).parent().show();
                }
                $(".tag-checkbox").each(function() {
                    $(this).parent().removeClass("is-checked");
                    $(this).prop('checked', false);
                });
                $("#tags-instruction").hide();
            } else {
                $("#tags-instruction").show();
            }
        });
    }
    
    //Languages input events
    $(".from-radio").change(function() {
        $("#language-from .radio-text").text($(this).val().substr(5));
        if($("input[name='options-to']:checked").val() != undefined) {
            $.get("tags-language.php?from="+$("input[name='options-from']:checked").val()+"&to="+$("input[name='options-to']:checked").val(), function(data) {
                if (data!="\\ABC\\") {
                    data = data.split(";");
                    $("#tag-container label").hide();
                    for (i=0; i<data.length; i++) {
                        $("#checkbox-"+data[i]).parent().show();
                    }
                    $(".tag-checkbox").each(function() {
                        $(this).parent().removeClass("is-checked");
                        $(this).prop('checked', false);
                    });
                    $("#tags-instruction").hide();
                } else {
                    $("#tags-instruction").show();
                }
            });
        }
        data = location.hash;
        data = data.split(";");
        data[3] = $("input[name='options-from']:checked").val();
        location.hash = "tags;"+$("#hardness-min").val()+";"+$("#hardness-max").val()+";"+$("input[name='options-from']:checked").val()+";"+$("input[name='options-to']:checked").val()
    });
    $(".to-radio").change(function() {
        $("#language-to .radio-text").text($(this).val().substr(3));
        if($("input[name='options-from']:checked").val() != undefined) {
            $.get("tags-language.php?from="+$("input[name='options-from']:checked").val()+"&to="+$("input[name='options-to']:checked").val(), function(data) {
                if (data!="\\ABC\\") {
                    data = data.split(";");
                    for (i=0; i<data.length; i++) {
                        $("#checkbox-"+data[i]).parent().show();
                    }
                    $(".tag-checkbox").each(function() {
                        $(this).parent().removeClass("is-checked");
                        $(this).prop('checked', false);
                    });
                    $("#tags-instruction").hide();
                } else {
                    $("#tags-instruction").show();
                }
            });
        }
        data = location.hash;
        data = data.split(";");
        data[4] = $("input[name='options-to']:checked").val();
        location.hash = "tags;"+$("#hardness-min").val()+";"+$("#hardness-max").val()+";"+$("input[name='options-from']:checked").val()+";"+$("input[name='options-to']:checked").val()
    });
    
    //Checkboxes for tags
    $(".tag-checkbox").change(function() {
        $("#search_input_value").val("");
        $("#search_input div").removeClass("is-dirty");
        tags = "";
        $(".tag-checkbox:checked").each(function() {
            tags+=$(this).attr("id").substr(9)+";";
        });
        tags = tags.substring(0, tags.length-1);
        location.hash = "tags;"+$("#hardness-min").val()+";"+$("#hardness-max").val()+";"+$("input[name='options-from']:checked").val()+";"+$("input[name='options-to']:checked").val()+";"+tags;
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
    $("#hardness-min").change(function() {
        $("#hardness-val-min").text($(this).val());
        data = location.hash.split(";");
        data[1] = $(this).val();
        location.hash = data.join(";");
    });
    $("#hardness-max").change(function() {
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
            $("#words-table").show();
            tags="";
            $(".tag-checkbox").prop('checked', false);
            for (i=5; i<data.length; i++) {
                tags += data[i] + ";";
                $("#checkbox-"+data[i]).prop('checked', true);
            }
            $(".tag-checkbox").each(function() {
                if($(this).prop('checked')) {
                    $(this).parent().addClass("is-checked");
                } else {
                    $(this).parent().removeClass("is-checked");
                }
            });
            $("#"+data[3]).prop("checked", true);
            $("#language-from .radio-text").text(data[3].substr(5));
            $("#"+data[4]).prop("checked", true);
            $("#language-to .radio-text").text(data[4].substr(3));
            
            $("#hardness-min").val(data[1]);
            $("#hardness-val-min").text(data[1]);
            $("#hardness-max").val(data[2]);
            $("#hardness-val-max").text(data[2]);
            
            tags = tags.substring(0, tags.length-1);
            $.get("query.php?tag="+tags+"&lmin="+data[1]+"&lmax="+data[2]+"&from="+data[3]+"&to="+data[4], function(data) {
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
            $("#words-table").show();
            $(".tag-checkbox").each(function() {
                $(this).parent().removeClass("is-checked");
                $(this).prop('checked', false);
            });
            $("#language-box input").each(function() {
                $(this).removeAttr("checked");
                $(this).parent().removeClass("is-checked");
            });
            $("#language-from .radio-text").text("--");
            $("#language-to .radio-text").text("--");
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
        } else {
            hideAll();
            $.get("pages/"+mode+".php", function(data) {
                $("#communication-additional").html(data);
                $("#words-table").hide();
                $("#communication-additional").show();
                $("#loading").stop();
                $("#loading").fadeOut("slow");
            })
        }
    }
});