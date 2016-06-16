/*!
 * cookie-monster - a simple cookie library
 * v0.3.0
 * https://github.com/jgallen23/cookie-monster
 * copyright Greg Allen 2014
 * MIT License
*/
var monster={set:function(a,b,c,d,e){var f=new Date,g="",h=typeof b,i="",j="";if(d=d||"/",c&&(f.setTime(f.getTime()+24*c*60*60*1e3),g="; expires="+f.toUTCString()),"object"===h&&"undefined"!==h){if(!("JSON"in window))throw"Bummer, your browser doesn't support JSON parsing.";i=encodeURIComponent(JSON.stringify({v:b}))}else i=encodeURIComponent(b);e&&(j="; secure"),document.cookie=a+"="+i+g+"; path="+d+j},get:function(a){for(var b=a+"=",c=document.cookie.split(";"),d="",e="",f={},g=0;g<c.length;g++){for(var h=c[g];" "==h.charAt(0);)h=h.substring(1,h.length);if(0===h.indexOf(b)){if(d=decodeURIComponent(h.substring(b.length,h.length)),e=d.substring(0,1),"{"==e)try{if(f=JSON.parse(d),"v"in f)return f.v}catch(i){return d}return"undefined"==d?void 0:d}}return null},remove:function(a){this.set(a,"",-1)},increment:function(a,b){var c=this.get(a)||0;this.set(a,parseInt(c,10)+1,b)},decrement:function(a,b){var c=this.get(a)||0;this.set(a,parseInt(c,10)-1,b)}};

$(document).ready(function() {
    
    update();
    
    //Cookies
    $("#okConsent").click(function() {
        monster.set("consent", "true", 365);
        $("#consent").animate({height:0, padding:0}, "slow", function() {
            $(this).remove();
        })
    })
    
    //Scroll on mobile
    $(".scroll").click(function() {
        if ($( window ).width()<826) {
            toppy = {scrollTop: $("#word-container").offset().top-8};
            $("html, body").animate(toppy, "slow", "swing")
        }
    })
    
    //Interface language chooser
    $("#nav-language-picker-menu li").click(function() {
        if($(this)[0].id == "nav-language-picker-add") {
            location.hash = "addlanguage";
        } else {
            monster.set("language", $(this).text().toLowerCase())
            location.reload()
        }
    })
    
    //Languages input events
    /*if($("input[name='options-from']:checked").val()!=undefined && $("input[name='options-to']:checked").val()!=undefined) {
        $.get("tags-language.php?from="+$("input[name='options-from']:checked").val()+"&to="+$("input[name='options-to']:checked").val(), function(data) {
            if (data!="//ABC//") {
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
    }*/
    
    $(".from-radio").change(function() {
        $("#language-from .radio-text").text($(this).val().substr(5));
        if($("input[name='options-to']:checked")[0] != undefined) {
            data = location.hash;
            data = data.split(";");
            data[3] = $("input[name='options-from']:checked").val();
            location.hash = "tags;"+selectedLevels()+";"+$("input[name='options-from']:checked").val()+";"+$("input[name='options-to']:checked").val();
        }
    });
    $(".to-radio").change(function() {
        $("#language-to .radio-text").text($(this).val().substr(3));
        if($("input[name='options-from']:checked")[0] != undefined) {
            data = location.hash;
            data = data.split(";");
            data[4] = $("input[name='options-to']:checked").val();
            location.hash = "tags;"+selectedLevels()+";"+$("input[name='options-from']:checked").val()+";"+$("input[name='options-to']:checked").val();
        }
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
        location.hash = "tags;"+selectedLevels()+";"+$("input[name='options-from']:checked").val()+";"+$("input[name='options-to']:checked").val()+";"+tags;
    });
    
    //Search input events
    $("#search_button_click").click(function() {
        query = $("#search_input_value").val();
        location.hash = "search;"+selectedLevels()+";"+query;
    });
    $("#search_input_value").keyup(function(e){
        if(e.keyCode == 13) {
            query = $("#search_input_value").val();
            location.hash = "search;"+selectedLevels()+";"+query;
        }
    });
    
    //Level input events
    $(".hardness-toggle-input").change(function() {
        data = location.hash.split(";");
        data[1] = selectedLevels();
        location.hash = data.join(";");
    })
    function selectedLevels() {
        selected = "";
        $(".hardness-toggle-input:checked").each(function() {
            selected += $(this).next().text()+",";
        });
        return selected.substr(0,selected.length-1);
    }
    
    //Some misc functions
    function hideAll() {
        $(".communication").hide();
    }
    $(window).on('hashchange',function(){ 
        update();
    });
    
    //Main update function
    var prev = "tags";
    function update() {
        ga('send', 'pageview', {
            'page': location.pathname + location.search  + location.hash
        });
        $("#loading").stop();
        $("#loading").fadeIn("slow");
        data = location.hash.split(";");
        data[0] = data[0].substring(1, data[0].length);
        mode = data[0];
        if (mode != prev) {
            $(".active").removeClass("active");
            activate = (mode == "" || mode=="search" || mode=="tags" ? "mainPage" : mode);
            $("#nav-"+activate).addClass("active");
        }
        //Tags mode
        if (mode == "") {
            hideAll();
            $("#words-table").hide();
            $("#tag-container label").hide();
            $("#tags-instruction").show();
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
            $("#communication-welcome").show();
            $("#loading").stop();
            $("#loading").fadeOut("slow");
        } else if (mode=="tags") {
            hideAll();
            $("#words-table").show();
            
            tags="";
            $.get("tags-language.php?from="+data[2]+"&to="+data[3], function(tag_data) {
                $("#tag-container label").hide();
                if (tag_data!="//ABC//") {
                    tag_data = tag_data.split(";");
                    for (i=0; i<tag_data.length; i++) {
                        $("#checkbox-"+tag_data[i]).parent().show();
                    }
                    $("#tags-instruction").hide();
                } else {
                    $("#tags-instruction").show();
                }
                $(".tag-checkbox").prop('checked', false);
                for (i=4; i<data.length; i++) {
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
                $("#"+data[2]).prop("checked", true);
                $("#language-from .radio-text").text(data[2].substr(5));
                $("#"+data[3]).prop("checked", true);
                $("#language-to .radio-text").text(data[3].substr(3));
                levels = data[1].split(",");
                $(".hardness-toggle-input").prop('checked', false);
                for (i=0; i<levels.length; i++) {
                    $("#hardness-toggle-"+levels[i]).prop("checked", true);
                }
                $(".hardness-toggle-input").each(function() {
                    if($(this).prop('checked')) {
                        $(this).parent().addClass("is-checked");
                    } else {
                        $(this).parent().removeClass("is-checked");
                    }
                });

                tags = tags.substring(0, tags.length-1);
                $.get("query.php?tag="+tags+"&levels="+data[1]+"&from="+data[2]+"&to="+data[3], function(data) {
                    if (data == "//ABC//") {
                        $("#words-table-body").html("");
                        $("#communication-choose-tags").show();
                    } else {
                        $("#words-table-body").html(data);
                    }
                    $("#loading").stop();
                    $("#loading").fadeOut("slow");
                });
            });
            
        //Search mode
        } else if (mode=="search") {
            hideAll();
            $("#words-table").show();
            $("#tag-container label").hide();
            $("#tags-instruction").show();
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
            
            $.get("search.php?search="+data[2]+"&levels="+data[1], function(data) {
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
            $("#words-table").hide();
            $("#tag-container label").hide();
            $("#tags-instruction").show();
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
            $.get("pages/"+mode+".php", function(data) {
                $("#communication-additional").html(data);
                $("#words-table").hide();
                $("#communication-additional").show();
                $("#loading").stop();
                $("#loading").fadeOut("slow");
                componentHandler.upgradeAllRegistered();
            });
        }
    }
});