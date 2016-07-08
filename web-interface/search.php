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
    
    error_reporting(0);
    register_shutdown_function( "fatal_handler" );
    function fatal_handler() {
        $error = error_get_last();
        if ($error['type'] === E_ERROR) {
            echo "//ABC//";
        }
    }
    
    function my_case($string) {
        return mb_strtolower($string);
    }
    $db->createFunction('my_case', 'my_case');
    $search = my_case($_GET['search']);
    #echo $search;
    $ids = "SELECT * FROM 'words' WHERE ";
    
    
    $strQuery = "SELECT * FROM words WHERE (my_case(base) LIKE '%".$search."%' OR my_case(author) LIKE '%".$search."%' OR my_case(trans) LIKE '%".$search."%' OR my_case(level) LIKE '%".$search."%' OR my_case(mono) LIKE '%".$search."%') AND (";
    $levelsArray = explode(",", $_GET['levels']);
    for ($i = 0; $i<count($levelsArray); $i++) {
        $strQuery .= "level=".$levelsArray[$i]." OR ";
    }
    $strQuery = substr($strQuery, 0, strlen($strQuery)-4);
    $strQuery .= ") ORDER BY id";
    #echo $strQuery;
    $stmt = $db->prepare($strQuery);
    $stmt->bindValue(':id', 1, SQLITE3_INTEGER);
    $result = $stmt->execute();
    $count = 0;
    while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
        $count += 1;
?>
        <tr>
            <td class="mdl-data-table__cell--non-numeric base"><?php echo str_replace("\n", "<br>", $row['base']) ?></td>
            <td class="mdl-data-table__cell--non-numeric trans"><?php echo str_replace("\n", "<br>", $row['trans']) ?></td>
            <td class="mdl-data-table__cell--non-numeric mono mdl-cell--hide-phone mdl-cell--hide-tablet"><?php echo str_replace("\n", "<br>", $row['mono']) ?></td>
            <td class="mdl-data-table__cell--non-numeric author"><?php echo str_replace("\n", "<br>", $row['author']) ?></td>
            <td class="level mdl-cell--hide-phone"><?php echo $row['level'] ?></td>
        </tr>
<?php
    }
    if (!$count) {
        echo "//ABC//";
    }
    $db->close(); unset($db);
?>
