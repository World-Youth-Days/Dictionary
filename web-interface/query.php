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
    
    if ($_GET['from']!="undefined" && $_GET['to']!="undefined") {
        $ids = "SELECT * FROM words WHERE (";
        if ($_GET['tag'] != ""){
            $tags = explode(";", $_GET['tag']);

            for ($i = 0; $i<count($tags); $i++) {
                $stmt = $db->prepare("SELECT * FROM '".$tags[$i]."'");
                $stmt->bindValue(':id', 1, SQLITE3_INTEGER);
                $result = $stmt->execute();
                while($row = $result->fetchArray(SQLITE3_ASSOC)) {
                    $ids .= "id=".$row['word_id']." OR ";
                }
            }
            $ids = substr($ids, 0, -4).") AND (";
        }

        $stmt = $db->prepare("SELECT * FROM '".$_GET['from']."'");
        $stmt->bindValue(':id', 1, SQLITE3_INTEGER);
        $result = $stmt->execute();
        while($row = $result->fetchArray(SQLITE3_ASSOC)) {
            $ids .= "id=".$row['word_id']." OR ";
        }
        $ids = substr($ids, 0, -4).") AND (";

        $stmt = $db->prepare("SELECT * FROM '".$_GET['to']."'");
        $stmt->bindValue(':id', 1, SQLITE3_INTEGER);
        $result = $stmt->execute();
        while($row = $result->fetchArray(SQLITE3_ASSOC)) {
            $ids .= "id=".$row['word_id']." OR ";
        }
        $ids = substr($ids, 0, -4).") AND level>=".$_GET['lmin']." AND level<=".$_GET['lmax']." ORDER BY base";
        #echo $ids;

        $result = $db->query($ids);
        $count = 0;
        while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
            $count+=1;
    ?>
        <tr>
            <td class="mdl-data-table__cell--non-numeric base"><?php echo $row['base'] ?></td>
            <td class="mdl-data-table__cell--non-numeric trans"><?php echo $row['trans'] ?></td>
            <td class="mdl-data-table__cell--non-numeric mono mdl-cell--hide-phone mdl-cell--hide-tablet"><?php echo $row['mono'] ?></td>
            <td class="mdl-data-table__cell--non-numeric author"><?php echo $row['author'] ?></td>
            <td class="level mdl-cell--hide-phone"><?php echo $row['level'] ?></td>
        </tr>
    <?php
        }
        if (!$count) {
            echo "//ABC//";
        }
    } else {
        echo "//ABC//";
    }
    $db->close(); unset($db);
?>
