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
    
    if ($_GET['tag']!=''){
    
        $tags = explode(";", $_GET['tag']);
        $ids = "SELECT * FROM 'words' WHERE (";

        for ($i = 0; $i<count($tags); $i++) {
            $stmt = $db->prepare("SELECT * FROM '".$tags[$i]."'");
            $stmt->bindValue(':id', 1, SQLITE3_INTEGER);
            $result = $stmt->execute();
            while($row = $result->fetchArray(SQLITE3_ASSOC)) {
                $ids .= "id=".$row['word_id']." OR ";
            }
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
            <td class="mdl-data-table__cell--non-numeric mono"><?php echo $row['mono'] ?></td>
            <td class="mdl-data-table__cell--non-numeric author"><?php echo $row['author'] ?></td>
            <td class="level"><?php echo $row['level'] ?></td>
        </tr>
<?php
        }
        if (!$count) {
            echo "//ABC//";
        }
    } else {
        echo "//ABC//";
    }
?>
