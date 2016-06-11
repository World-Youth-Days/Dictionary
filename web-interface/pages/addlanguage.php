 <?php
if (!isset($_COOKIE["language"])) {
    $lang = substr($_SERVER['HTTP_ACCEPT_LANGUAGE'], 0, 2);

} else {
    $lang = substr($_COOKIE["language"], 0, 2);
}
if (!file_exists("../langs/".$lang.".php")) $lang = "en";
$_COOKIE["language"] = $lang;
require '../langs/'.$lang.'.php';

function t($string) {
    global $translations;
    if (isset($translations[$string])) {
        echo $translations[$string];
    } else {
        echo "---";
    }
}
?>
<div id="page">
    <h2><?php t("addLanguageHeader") ?></h2>
    <p><?php t("addLanguageContent") ?></p>
</div>

<script type="text/javascript">
    $(".common-tags .delete").click(function(e) {
        event.preventDefault();
        $(this).parent().remove();
    })
    $(".common-ones .addTag").click(function(e) {
        event.preventDefault();
        $(this).parent().children(".common-tags-container").children(".common-tag-example").each(function() {
            $(this).removeClass("hidden");
            $(this).clone().removeClass("common-tag-example").appendTo(".common-ones .common-tags-container");
            $(this).addClass("hidden");
        });
        $(".common-tags .delete").click(function(e) {
            event.preventDefault();
            $(this).parent().remove();
        })
    })
    $(".special-ones .addTag").click(function(e) {
        event.preventDefault();
        $(this).parent().children(".common-tags-container").children(".common-tag-example").each(function() {
            $(this).removeClass("hidden");
            $(this).clone().removeClass("common-tag-example").appendTo(".special-ones .common-tags-container");
            $(this).addClass("hidden");
        });
        $(".common-tags .delete").click(function(e) {
            event.preventDefault();
            $(this).parent().remove();
        })
    })
</script>