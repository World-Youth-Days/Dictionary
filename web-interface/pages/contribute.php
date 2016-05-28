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
    <h2><?php t("contribute") ?></h2>
    <p><?php t("contributeHi") ?></p>
    <form action="contribute.php" method="post" target="_blank">
        <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
            <input class="mdl-textfield__input" type="text" id="author">
            <label class="mdl-textfield__label" for="sample3"><?php t("name") ?></label>
        </div>
        <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
            <input class="mdl-textfield__input" type="password" id="pin" pattern="-?[0-9]*(\.[0-9]+)?">
            <label class="mdl-textfield__label" for="sample3"><?php t("pin") ?></label>
            <span class="mdl-textfield__error"><?php t("notANumber") ?></span>
        </div>
        <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
            <input class="mdl-textfield__input" type="text" id="mail">
            <label class="mdl-textfield__label" for="sample3"><?php t("mail") ?></label>
        </div>
        <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
            <input class="mdl-textfield__input" type="text" id="default_level" pattern="-?[0-9]*(\.[0-9]+)?">
            <label class="mdl-textfield__label" for="sample3"><?php t("defaultLevel") ?></label>
            <span class="mdl-textfield__error"><?php t("notANumber") ?></span>
        </div>
        <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
            <input class="mdl-textfield__input" type="text" id="from">
            <label class="mdl-textfield__label" for="sample3"><?php t("fromLanguage") ?></label>
        </div>
        <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
            <input class="mdl-textfield__input" type="text" id="to">
            <label class="mdl-textfield__label" for="sample3"><?php t("toLanguage") ?></label>
        </div><br><br>
        <p><?php t("commonTags") ?></p>
        <div class="common-tags common-ones">
            <div class="common-tags-container">
                <div class="common-tag-example common-tag hidden">
                    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                        <input class="mdl-textfield__input" type="text" name="common_tag_name">
                    </div>
                    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                        <input class="mdl-textfield__input" type="text" name="common_readable">
                    </div>
                    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                        <input class="mdl-textfield__input" type="text" name="common_description">
                    </div>
                    <button class="mdl-button mdl-js-button mdl-button--icon delete">
                        <i class="material-icons">delete</i>
                    </button>
                </div>              
                <div class="common-tag">
                    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                        <input class="mdl-textfield__input" type="text" id="common_tag_name" name="common_tag_name">
                        <label class="mdl-textfield__label" for="common_tag_name"><?php t("tagName") ?></label>
                    </div>
                    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                        <input class="mdl-textfield__input" type="text" id="common_readable" name="common_readable">
                        <label class="mdl-textfield__label" dor="common_readable"><?php t("tagReadable") ?></label>
                    </div>
                    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                        <input class="mdl-textfield__input" type="text" id="common_description" name="common_description">
                        <label class="mdl-textfield__label" for="common_description"><?php t("tagDescription") ?></label>
                    </div>
                    <button class="mdl-button mdl-js-button mdl-button--icon">
                        
                    </button>
                </div>
            </div>
            <button class="mdl-button mdl-js-button mdl-button--primary mdl-js-ripple-effect addTag">
                <?php t("addTag") ?>
            </button>
        </div>
        <p><?php t("specialTags") ?></p>
        <div class="common-tags special-ones">
            <div class="common-tags-container">
                <div class="common-tag-example common-tag hidden">
                    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                        <input class="mdl-textfield__input" type="text" name="special_tag_name">
                    </div>
                    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                        <input class="mdl-textfield__input" type="text" name="special_readable">
                    </div>
                    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                        <input class="mdl-textfield__input" type="text" name="special_description">
                    </div>
                    <button class="mdl-button mdl-js-button mdl-button--icon delete">
                        <i class="material-icons">delete</i>
                    </button>
                </div>
                <div class="common-tag">
                    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                        <input class="mdl-textfield__input" type="text" id="special_tag_name" name="special_tag_name">
                        <label class="mdl-textfield__label" for="special_tag_name"><?php t("tagName") ?></label>
                    </div>
                    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                        <input class="mdl-textfield__input" type="text" id="special_readable" name="special_readable">
                        <label class="mdl-textfield__label" for="special_readable"><?php t("tagReadable") ?></label>
                    </div>
                    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                        <input class="mdl-textfield__input" type="text" id="special_description" name="special_description">
                        <label class="mdl-textfield__label" for="special_description"><?php t("tagDescription") ?></label>
                    </div>
                    <button class="mdl-button mdl-js-button mdl-button--icon">
                        
                    </button>
                </div>
            </div>
            <button class="mdl-button mdl-js-button mdl-button--primary mdl-js-ripple-effect addTag">
                <?php t("addTag") ?>
            </button>
        </div>
        <p><?php t("fileTransfer") ?></p>
        <input type="file" name="file">
        <p>
            <?php t("readyToGo") ?>
            <button class="mdl-button mdl-js-button mdl-button--raised mdl-button--colored">
                <?php t("send"); ?>
            </button>
        </p>
    </form>
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