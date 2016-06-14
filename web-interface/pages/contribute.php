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
    <h2><?php t("contribute") ?></h2>
    <p><?php t("contributeHi") ?></p>
    <hr>
    <form action="contribute.php" method="post" target="_blank" enctype="multipart/form-data">
        <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
            <input class="mdl-textfield__input" type="text" id="author" name="author">
            <label class="mdl-textfield__label" for="author"><?php t("name") ?></label>
        </div>
        <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
            <input class="mdl-textfield__input" type="password" id="pin" pattern="-?[0-9]*(\.[0-9]+)?" name="pin">
            <label class="mdl-textfield__label" for="pin"><?php t("pin") ?></label>
            <span class="mdl-textfield__error"><?php t("notANumber") ?></span>
        </div>
        <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
            <input class="mdl-textfield__input" type="text" id="mail" name="mail">
            <label class="mdl-textfield__label" for="mail"><?php t("mail") ?></label>
        </div>
        <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
            <input class="mdl-textfield__input" type="text" id="default_level" name="default_level" pattern="-?[0-9]*(\.[0-9]+)?">
            <label class="mdl-textfield__label" for="default_level"><?php t("defaultLevel") ?></label>
            <span class="mdl-textfield__error"><?php t("notANumber") ?></span>
        </div>
        <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
            <input class="mdl-textfield__input" type="text" id="from" name="from">
            <label class="mdl-textfield__label" for="from"><?php t("fromLanguage") ?></label>
        </div>
        <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
            <input class="mdl-textfield__input" type="text" id="to" name="to">
            <label class="mdl-textfield__label" for="to"><?php t("toLanguage") ?></label>
        </div>
        <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
            <input class="mdl-textfield__input" type="text" id="separator" name="separator" value=",">
            <label class="mdl-textfield__label" for="to"><?php t("columnSeparator") ?></label>
        </div>
        <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
            <input class="mdl-textfield__input" type="text" id="row_delimiter" name="row_delimiter" value="\n">
            <label class="mdl-textfield__label" for="row_delimiter"><?php t("lineSeparator") ?></label>
        </div><br>
        <span style="font-size: 15px"><?php t("separatorsExplanation") ?></span>
        <hr>
        
        <p><?php t("commonTags") ?></p>
        <div class="common-tags common-ones">
            <div class="common-tags-container">
                <div class="common-tag-example common-tag hidden">
                    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                        <input class="mdl-textfield__input" type="text" name="common_tag_name[]">
                    </div>
                    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                        <input class="mdl-textfield__input" type="text" name="common_readable[]">
                    </div>
                    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                        <input class="mdl-textfield__input" type="text" name="common_description[]">
                    </div>
                    <button class="mdl-button mdl-js-button mdl-button--icon delete">
                        <i class="material-icons">delete</i>
                    </button>
                </div>              
                <div class="common-tag">
                    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                        <input class="mdl-textfield__input" type="text" id="common_tag_name" name="common_tag_name[]">
                        <label class="mdl-textfield__label" for="common_tag_name"><?php t("tagName") ?></label>
                    </div>
                    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                        <input class="mdl-textfield__input" type="text" id="common_readable" name="common_readable[]">
                        <label class="mdl-textfield__label" dor="common_readable"><?php t("tagReadable") ?></label>
                    </div>
                    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                        <input class="mdl-textfield__input" type="text" id="common_description" name="common_description[]">
                        <label class="mdl-textfield__label" for="common_description"><?php t("tagDescription") ?></label>
                    </div>
                    <button class="mdl-button mdl-js-button mdl-button--icon delete-disabled" disabled>
                        
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
                        <input class="mdl-textfield__input" type="text" name="special_tag_name[]">
                    </div>
                    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                        <input class="mdl-textfield__input" type="text" name="special_readable[]">
                    </div>
                    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                        <input class="mdl-textfield__input" type="text" name="special_description[]">
                    </div>
                    <button class="mdl-button mdl-js-button mdl-button--icon delete">
                        <i class="material-icons">delete</i>
                    </button>
                </div>
                <div class="common-tag">
                    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                        <input class="mdl-textfield__input" type="text" id="special_tag_name" name="special_tag_name[]">
                        <label class="mdl-textfield__label" for="special_tag_name"><?php t("tagName") ?></label>
                    </div>
                    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                        <input class="mdl-textfield__input" type="text" id="special_readable" name="special_readable[]">
                        <label class="mdl-textfield__label" for="special_readable"><?php t("tagReadable") ?></label>
                    </div>
                    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                        <input class="mdl-textfield__input" type="text" id="special_description" name="special_description[]">
                        <label class="mdl-textfield__label" for="special_description"><?php t("tagDescription") ?></label>
                    </div>
                    <button class="mdl-button mdl-js-button mdl-button--icon delete-disabled" disabled>
                        
                    </button>
                </div>
            </div>
            <button class="mdl-button mdl-js-button mdl-button--primary mdl-js-ripple-effect addTag">
                <?php t("addTag") ?>
            </button>
        </div>
        <hr>
        
        <p><?php t("fileTransfer") ?></p>
        <input type="file" name="file_src">
        <hr>
        <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label user-input">
            <textarea class="mdl-textfield__input" type="text" id="user-input" name="user-input"></textarea>
            <label class="mdl-textfield__label" for="user-input"><?php t("userInput") ?></label>
        </div>
        <hr>
        <p>
            <?php t("readyToGo") ?>
            <button class="mdl-button mdl-js-button mdl-button--raised mdl-button--colored">
                <?php t("send"); ?>
            </button>
        </p>
    </form>
</div>

<script type="text/javascript">
    $(".common-tags .delete").click(function(event) {
        event.preventDefault();
        $(this).parent().remove();
    })
    $(".common-ones .addTag").click(function(event) {
        event.preventDefault();
        $(this).parent().children(".common-tags-container").children(".common-tag-example").each(function() {
            $(this).removeClass("hidden");
            $(this).clone().removeClass("common-tag-example").appendTo(".common-ones .common-tags-container");
            $(this).addClass("hidden");
        });
        $(".common-tags .delete").click(function(event) {
            event.preventDefault();
            $(this).parent().remove();
        })
    })
    $(".special-ones .addTag").click(function(event) {
        event.preventDefault();
        $(this).parent().children(".common-tags-container").children(".common-tag-example").each(function() {
            $(this).removeClass("hidden");
            $(this).clone().removeClass("common-tag-example").appendTo(".special-ones .common-tags-container");
            $(this).addClass("hidden");
        });
        $(".common-tags .delete").click(function(event) {
            event.preventDefault();
            $(this).parent().remove();
        })
    })
</script>