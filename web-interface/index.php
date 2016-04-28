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
                <div id="filters" class="mdl-cell mdl-cell--4-col mdl-card mdl-shadow--2dp">
                    <div class="mdl-card__title">
                        <h2 class="mdl-card__title-text">Filtry</h2>
                    </div>
                    <div class="card-content">
                        Wybierz obszary słownika, które chcesz wyświetlić w oknie po prawej:
                    </div>
                    <div class="card-content">
                        <?php
                        $sql = "SELECT * FROM 'tags'";
                        $ret = $db->query($sql);
                        while ($row = $ret->fetchArray(SQLITE3_ASSOC)) {
                        ?>
                        <label class="mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect" for="checkbox-<?php echo $row["id"] ?>">
                            <input type="checkbox" id="checkbox-<?php echo $row["id"] ?>" class="mdl-checkbox__input">
                            <span class="mdl-checkbox__label"><?php echo $row["tag_name"] ?></span>
                        </label>
                        <?php } ?>
                    </div>
                </div>
                <div id="word-container" class="mdl-cell mdl-cell--8-col mdl-card mdl-shadow--2dp">
                    
                </div>
            </div>
        </div>
        <?php $db->close(); ?>
    </body>
</html>
