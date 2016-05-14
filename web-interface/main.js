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
        query = $("#search_input_value").val();
        location.hash = $("#hardness-min").val()+";"+$("#hardness-max").val()+";"+"search;"+query;
    });
    $("#search_input_value").keyup(function(e){
        if(e.keyCode == 13) {
            query = $("#search_input_value").val();
            location.hash = $("#hardness-min").val()+";"+$("#hardness-max").val()+";"+"search;"+query;
        }
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
        if (mode=="tags") {
            hideAll();
            tags="";
            for (i=3; i<data.length; i++) {
                tags += data[i] + ";"
            }
            tags = tags.substring(0, tags.length-1);
            $.get("query.php?tag="+tags, function(data) {
                if (data == "//ABC//") {
                    $("#words-table-body").html("");
                    $("#communication-choose-tags").show();
                } else {
                    $("#words-table-body").html(data);
                }
            });
        } else if (mode=="search") {
            hideAll();
            $.get("search.php?search="+data[3], function(data) {
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