<!DOCTYPE html>
<html>
    <head>
        <title>WYD Dictionary</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script type="text/javascript" src="jquery-1.12.2.min.js"></script>
        <script type="text/javascript" src="main.js"></script>
        <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
        <link rel="stylesheet" href="https://code.getmdl.io/1.1.3/material.blue-amber.min.css" />
        <script defer src="https://code.getmdl.io/1.1.3/material.min.js"></script>
        <link rel="stylesheet" href="main.css" />
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
        </div>
        <div id="content">
            <div class="mdl-grid">
                <div class="mdl-cell mdl-cell--4-col">
                    <div id="filters" class="mdl-card mdl-shadow--2dp">
                        <div class="mdl-card__title">
                            <h2 class="mdl-card__title-text">Szukaj</h2>
                        </div>
                        <div id="search_box">
                            <div id="search_input">
                                <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                                    <input class="mdl-textfield__input" type="text" id="search_input_value">
                                    <label class="mdl-textfield__label" for="sample3">Szukaj słowa, definicji, autora...</label>
                                </div>
                            </div>
                            <div id="search_button">
                                <button class="mdl-button mdl-js-button mdl-button--fab mdl-button--mini-fab mdl-js-ripple-effect" id="search_button_click">
                                    <i class="material-icons">search</i>
                                </button>
                            </div>
                        </div>
                        <div class="mdl-card__title">
                            <h2 class="mdl-card__title-text">Słowniki</h2>
                        </div>
                        <div class="card-content">
                            <?php
                            $sql = "SELECT * FROM 'tags'";
                            $ret = $db->query($sql);
                            while ($row = $ret->fetchArray(SQLITE3_ASSOC)) {
                            ?>
                            <label class="mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect" for="checkbox-<?php echo $row['tag_name'] ?>">
                                <input type="checkbox" id="checkbox-<?php echo $row['tag_name'] ?>" class="mdl-checkbox__input tag-checkbox">
                                <span class="mdl-checkbox__label"><?php echo $row['tag_name'] ?></span>
                            </label>
                            <?php } ?>
                        </div>
                        <div class="mdl-card__title">
                            <h2 class="mdl-card__title-text">Poziom trudności</h2>
                        </div>
                        <div class="hardness-container">
                            <div class="hardness-des" id="hardness-des-min">Min</div>
                            <div class="hardness-slider">
                                <input class="mdl-slider mdl-js-slider" type="range" min="1" max="10" value="1" id="hardness-min">
                            </div>
                            <div class="hardness-val" id="hardness-val-min">0</div>
                        </div>
                        <div class="hardness-container">
                            <div class="hardness-des" id="hardness-des-min">Max</div>
                            <div class="hardness-slider">
                                <input class="mdl-slider mdl-js-slider" type="range" min="1" max="10" value="10" id="hardness-max">
                            </div>
                            <div class="hardness-val" id="hardness-val-max">10</div>
                        </div>
                    </div>
                </div>
                <div id="word-container" class="mdl-cell mdl-cell--8-col mdl-card mdl-shadow--2dp">
                    <div id="loading" class="mdl-progress mdl-js-progress mdl-progress__indeterminate"></div>
                    <table class="mdl-data-table mdl-js-data-table" id="words-table">
                        <thead>
                            <td class="mdl-data-table__cell--non-numeric">Słowo</td>
                            <td class="mdl-data-table__cell--non-numeric">Tłumaczenie</td>
                            <td class="mdl-data-table__cell--non-numeric">Opis</td>
                            <td class="mdl-data-table__cell--non-numeric">Autor</td>
                            <td>Poziom</td>
                        </thead>
                        <tbody id="words-table-body">
                            
                        </tbody>
                    </table>
                    <div id="communication">
                        <div id="communication-language" class="communication">
                            
                        </div>
                        <div id="communication-nothing-found" class="communication">
                            <h2>Nic nie znaleziono!</h2>
                            <p>Wybierz inne hasło do wyszukiwania.<br>A może poziomy trudności są źle ustawione?</p>
                        </div>
                        <div id="communication-choose-tags" class="communication">
                            <h2>Nic tu nie ma!</h2>
                            <p>Wybierz jeden ze słowników z menu po lewej.<br>A może poziomy trudności są źle ustawione?</p>
                        </div>
                        <div id="communication-additional" class="communication">
                            
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <?php $db->close(); ?>
    </body>
</html>
