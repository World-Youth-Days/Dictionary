$(document).ready(function() {
    
    update();
    
    $(".tag-checkbox").change(function() {
        $("#search_input_value").val("");
        $("#search_input div").removeClass("is-dirty");
        tags = "";
        $(".tag-checkbox:checked").each(function() {
            tags+=$("label[for='"+$(this).attr('id')+"'] .mdl-checkbox__label").text()+";";
        });
        tags = tags.substring(0, tags.length-1);
        location.hash = $("#hardness-min").val()+";"+$("#hardness-max").val()+";"+"tags;"+tags;
    });
    $("#search_button_click").click(function() {
        $(".tag-checkbox").each(function() {
            $(this).parent().removeClass("is-checked");
            $(this).prop('checked', false);
        });
        query = $("#search_input_value").val();
        location.hash = $("#hardness-min").val()+";"+$("#hardness-max").val()+";"+"search;"+query;
    });
    $("#search_input_value").keyup(function(e){
        if(e.keyCode == 13) {
            $(".tag-checkbox").each(function() {
                $(this).parent().removeClass("is-checked");
                $(this).prop('checked', false);
            });
            query = $("#search_input_value").val();
            location.hash = $("#hardness-min").val()+";"+$("#hardness-max").val()+";"+"search;"+query;
        }
    });
    $("#hardness-min").on("input", function() {
        $("#hardness-val-min").text($(this).val());
        data = location.hash.split(";");
        data[0] = data[0].substring(1, data[0].length);
        data[0] = $(this).val();
        location.hash = data.join(";");
    });
    $("#hardness-max").on("input", function() {
        $("#hardness-val-max").text($(this).val());
        data = location.hash.split(";");
        data[0] = data[0].substring(1, data[0].length);
        data[1] = $(this).val();
        location.hash = data.join(";");
    });
    
    function hideAll() {
        $(".communication").hide();
    }
    
    $(window).on('hashchange',function(){ 
        update();
    });
    
    function update() {
        data = location.hash.split(";");
        mode = data[2];
        data[0] = data[0].substring(1, data[0].length);
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
            tags = tags.substring(0, tags.length-1);
            $.get("query.php?tag="+tags+"&lmin="+data[0]+"&lmax="+data[1], function(data) {
                if (data == "//ABC//") {
                    $("#words-table-body").html("");
                    $("#communication-choose-tags").show();
                } else {
                    $("#words-table-body").html(data);
                }
            });
        } else if (mode=="search") {
            hideAll();
            $.get("search.php?search="+data[3]+"&lmin="+data[0]+"&lmax="+data[1], function(data) {
                if (data == "//ABC//") {
                    $("#words-table-body").html("");
                    $("#communication-nothing-found").show();
                } else {
                    $("#words-table-body").html(data);
                }
            });
        }
    }
});