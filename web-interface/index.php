﻿<!DOCTYPE html>
<html>
    <head>
        <title>WYD Dictionary</title>
        <meta name="description" content="WYD Dictionary - the best dictionary for the World Youth Day!" />
        <meta property="og:title" content="WYD Dictionary" />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="http://wyd-dict.tk/" />
        <meta property="og:image" content="http://wyd-dict.tk/img/fb.png" />
        <meta property="og:description" content="WYD Dictionary - the best dictionary for the World Youth Day!" />
        
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script type="text/javascript" src="jquery-1.12.2.min.js"></script>
        <script type="text/javascript" src="main.js"></script>
        <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
        <link rel="stylesheet" href="https://code.getmdl.io/1.1.3/material.blue-orange.min.css" />
        <script defer src="https://code.getmdl.io/1.1.3/material.min.js"></script>
        <link rel="stylesheet" href="main.css" />
        <?php
        require 'langs/en.php';
        function t($string) {
            global $translations;
            if (isset($translations[$string])) {
                echo $translations[$string];
            } else {
                echo "---";
            }
        }
        ?>
        <script>
            (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
            (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
            m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
            })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

            ga('create', 'UA-79048505-1', 'auto');
            ga('send', 'pageview');

        </script>
    </head>
    <?php
    class MyDB extends SQLite3
    {
       function __construct()
       {
          $this->open('dictionary.db');
       }
    }
    
    $db = new MyDB();
    
    if(!$db){
       echo $db->lastErrorMsg();
    } else {
       #echo "Opened database successfully\n";
    }
    ?>
    <body>
        <div id="header" class="mdl-shadow--2dp">
            <div id="logo">
                <img src="/img/logo-top.png" alt="WYD Dictionary" >
            </div>
            <div id="nav">
                <a href="/"><div class="nav-elem active" id="nav-mainPage"><?php t("mainPage") ?></div></a>
                <a href="#contribute"><div class="nav-elem" id="nav-contribute"><?php t("contribute") ?></div></a>
                <a href="#about"><div class="nav-elem" id="nav-about"><?php t("about") ?></div></a>
            </div>
        </div>
        <div id="content">
            <div class="mdl-grid">
                <div class="mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet">
                    <div id="filters" class="mdl-card mdl-shadow--2dp">
                        <div class="mdl-card__title">
                            <h2 class="mdl-card__title-text"><?php t("Search") ?></h2>
                        </div>
                        <div id="search_box">
                            <div id="search_input">
                                <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                                    <input class="mdl-textfield__input" type="text" id="search_input_value">
                                    <label class="mdl-textfield__label" for="sample3"><?php t("SearchForWordDefLabel") ?></label>
                                </div>
                            </div>
                            <div id="search_button">
                                <button class="mdl-button mdl-js-button mdl-button--fab mdl-button--mini-fab mdl-js-ripple-effect" id="search_button_click">
                                    <i class="material-icons">search</i>
                                </button>
                            </div>
                        </div>
                        <div class="mdl-card__title">
                            <h2 class="mdl-card__title-text"><?php t("Languages") ?></h2>
                        </div>
                        <div id="language-box">
                            <div class="language-chooser">
                                <button id="language-from" class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect">
                                    <span class="radio-text">--</span> <i class="material-icons">keyboard_arrow_down</i>
                                </button>
                                <ul class="mdl-menu mdl-js-menu" for="language-from">
                                    <?php
                                        $sql = "SELECT * FROM tags WHERE flag = 'from'";
                                        $ret = $db->query($sql);
                                        while ($row = $ret->fetchArray(SQLITE3_ASSOC)) {
                                    ?>
                                        <li class="mdl-menu__item">
                                            <label class="mdl-radio mdl-js-radio mdl-js-ripple-effect" for="<?php echo $row['tag_name'] ?>">
                                                <input type="radio" id="<?php echo $row['tag_name'] ?>" class="mdl-radio__button from-radio" name="options-from" value="<?php echo $row['tag_name'] ?>">
                                                <span class="mdl-radio__label"><?php echo substr($row['tag_name'],5) ?></span>
                                            </label>
                                        </li>
                                    <?php } ?>
                                </ul>
                            </div>
                            <div id="language-arrow">
                                <button class="mdl-button mdl-js-button mdl-button--icon">
                                    <i class="material-icons">trending_flat</i>
                                </button>
                            </div>
                            <div class="language-chooser">
                                <button id="language-to" class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect">
                                    <span class="radio-text">--</span> <i class="material-icons">keyboard_arrow_down</i>
                                </button>
                                <ul class="mdl-menu mdl-js-menu" id="language-to-ul" for="language-to">
                                    <?php
                                        $sql = "SELECT * FROM tags WHERE flag = 'to'";
                                        $ret = $db->query($sql);
                                        while ($row = $ret->fetchArray(SQLITE3_ASSOC)) {
                                    ?>
                                        <li class="mdl-menu__item">
                                            <label class="mdl-radio mdl-js-radio mdl-js-ripple-effect" for="<?php echo $row['tag_name'] ?>">
                                                <input type="radio" id="<?php echo $row['tag_name'] ?>" class="mdl-radio__button to-radio" name="options-to" value="<?php echo $row['tag_name'] ?>">
                                                <span class="mdl-radio__label"><?php echo substr($row['tag_name'],3) ?></span>
                                            </label>
                                        </li>
                                    <?php } ?>
                                </ul>
                            </div>
                        </div>
                        <div class="mdl-card__title">
                            <h2 class="mdl-card__title-text"><?php t("Tags") ?></h2>
                        </div>
                        <div class="card-content" id="tag-container">
                            <?php
                            $sql = "SELECT * FROM 'tags' WHERE flag = 'live'";
                            $ret = $db->query($sql);
                            while ($row = $ret->fetchArray(SQLITE3_ASSOC)) {
                                $tag_name = ($row['readable']!="" ? $row['readable'] : $row['tag_name']);
                            ?>
                            <label class="mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect" for="checkbox-<?php echo $row['tag_name'] ?>" style="display: none;" id="label-for-<?php echo $row['tag_name'] ?>">
                                <input type="checkbox" id="checkbox-<?php echo $row['tag_name'] ?>" class="mdl-checkbox__input tag-checkbox">
                                <span class="mdl-checkbox__label"><?php echo $tag_name ?></span>
                            </label>
                            <?php if ($row['description']!="") { ?>
                            <div class="mdl-tooltip mdl-tooltip--large" for="label-for-<?php echo $row['tag_name'] ?>">
                                <?php echo $row['description'] ?>
                            </div>
                            <?php } ?>
                            <?php } ?>
                            <div id="tags-instruction"><?php t("firstChooseTheLanguages") ?></div>
                        </div>
                        <div class="mdl-card__title">
                            <h2 class="mdl-card__title-text"><?php t("Level") ?></h2>
                        </div>
                        <div class="hardness-container">
                            <div class="hardness-des" id="hardness-des-min">Min</div>
                            <div class="hardness-slider">
                                <input class="mdl-slider mdl-js-slider" type="range" min="1" max="8" value="1" id="hardness-min">
                            </div>
                            <div class="hardness-val" id="hardness-val-min">0</div>
                        </div>
                        <div class="hardness-container">
                            <div class="hardness-des" id="hardness-des-min">Max</div>
                            <div class="hardness-slider">
                                <input class="mdl-slider mdl-js-slider" type="range" min="1" max="8" value="8" id="hardness-max">
                            </div>
                            <div class="hardness-val" id="hardness-val-max">8</div>
                        </div>
                    </div>
                </div>
                <div id="word-container" class="mdl-cell mdl-cell--8-col mdl-card mdl-shadow--2dp">
                    <div id="loading" class="mdl-progress mdl-js-progress mdl-progress__indeterminate"></div>
                    <table class="mdl-data-table mdl-js-data-table" id="words-table">
                        <thead>
                            <td class="mdl-data-table__cell--non-numeric"><?php t("Word") ?></td>
                            <td class="mdl-data-table__cell--non-numeric"><?php t("Translation") ?></td>
                            <td class="mdl-data-table__cell--non-numeric mdl-cell--hide-phone mdl-cell--hide-tablet"><?php t("Definition") ?></td>
                            <td class="mdl-data-table__cell--non-numeric"><?php t("Author") ?></td>
                            <td class="mdl-cell--hide-phone"><?php t("Level") ?></td>
                        </thead>
                        <tbody id="words-table-body">
                            
                        </tbody>
                    </table>
                    <div id="communication">
                        <div id="communication-welcome" class="communication">
                            <img src="img/logo-self.png" id="welcome-logo" class="mdl-cell--hide-phone" alt="logo">
                            <h2><?php t("welcome") ?></h2>
                            <p><?php t("welcomeContent") ?></p>
                            <div id="chooseLanguage"></div>
                        </div>
                        <div id="communication-nothing-found" class="communication">
                            <h2><?php t("nothingFound") ?></h2>
                            <p><?php t("nothingFoundTroubleshooting") ?></p>
                        </div>
                        <div id="communication-choose-tags" class="communication">
                            <h2><?php t("noWords") ?></h2>
                            <p><?php t("noWordsTroubleshooting") ?></p>
                        </div>
                        <div id="communication-additional" class="communication">
                            
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div id="footer">
            Project by Jakub Dranczewski (<a href="https://github.com/z-gora" target=_blank>@ZGora</a>) and Hubert Bereś (<a href="https://github.com/Ddedalus" target=_blank>@Dedalus</a>).<br>
            <a href="https://github.com/World-Youth-Days/Dictionary" target=_blank>We <i class="material-icons">favorite</i> Open Source, so it's all on GitHub!</a><br>
            If you want to use the data, ask us first!
        </div>
        <?php $db->close(); unset($db); ?>
    </body>
</html>
