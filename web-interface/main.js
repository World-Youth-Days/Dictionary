$(document).ready(function() {
    $(".tag-checkbox").change(function() {
        tags = "";
        $(".tag-checkbox:checked").each(function() {
            tags+=$("label[for='"+$(this).attr('id')+"'] .mdl-checkbox__label").text()+";";
        });
        tags = tags.substring(0, tags.length-1);
        $.get("query.php?tag="+tags, function(data) {
            $("#words-table-body").html(data);
        });
    });
});