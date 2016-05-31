 <?php
require '../langs/en.php';
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
</div>