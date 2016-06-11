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
    <h2><?php t("about") ?></h2>
    <?php t("aboutContent") ?>
    <span class="mini"><?php t("code") ?> translation by <?php t("transAuthor") ?></span>
</div>