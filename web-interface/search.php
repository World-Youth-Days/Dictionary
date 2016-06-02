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
    
    $search = $_GET['search'];
    $ids = "SELECT * FROM 'words' WHERE ";
    
    $strQuery = "SELECT * FROM words WHERE (base LIKE '%".$search."%' OR author LIKE '%".$search."%' OR trans LIKE '%".$search."%' OR level LIKE '%".$search."%' OR mono LIKE '%".$search."%') AND level>=".$_GET['lmin']." AND level<=".$_GET['lmax']." ORDER BY base";
    $stmt = $db->prepare($strQuery);
    #echo $strQuery;
    $stmt->bindValue(':id', 1, SQLITE3_INTEGER);
    $result = $stmt->execute();
    $count = 0;
    while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
        $count += 1;
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
    $db->close(); unset($db);
?>
