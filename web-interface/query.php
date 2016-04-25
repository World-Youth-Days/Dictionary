<?php
    class MyDB extends SQLite3
    {
       function __construct()
       {
          $this->open('factbook.db');
       }
    }
    
    $db = new MyDB();
    
    if(!$db){
       echo $db->lastErrorMsg();
    } else {
       #echo "Opened database successfully\n";
    }
    
    $tags = explode(";", $_GET['tag']);
    $ids = "SELECT * FROM 'words' WHERE ";
    
    for ($i = 0; $i<count($tags); $i++) {
        $stmt = $db->prepare("SELECT * FROM '".$tags[$i]."'");
        $stmt->bindValue(':id', 1, SQLITE3_INTEGER);
        $result = $stmt->execute();
        while($row = $result->fetchArray(SQLITE3_ASSOC)) {
            $ids .= "id=".$row['word_id']." OR ";
        }
    }
    $ids = substr($ids, 0, -4);
    #echo $ids;
    
    $result = $db->query($ids);
    while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
?>
        <tr>
            <td class="mdl-data-table__cell--non-numeric"><?php echo $row['base'] ?></td>
            <td class="mdl-data-table__cell--non-numeric"><?php echo $row['trans'] ?></td>
            <td class="mdl-data-table__cell--non-numeric"><?php echo $row['mono'] ?></td>
            <td class="mdl-data-table__cell--non-numeric"><?php echo $row['author'] ?></td>
        </tr>
<?php } ?>
