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
    
    if ($_GET['from']!=''){
        #echo "Start";
        $from = $_GET['from'];
        $fromIds = array();
        $return = "";
        
        $stmtFromIds = $db->prepare("SELECT * FROM ".$from."");
        $stmtFromIds->bindValue(':id', 1, SQLITE3_INTEGER);
        $resultFromIds = $stmtFromIds->execute();
        while($row = $resultFromIds->fetchArray(SQLITE3_ASSOC)) {
            $fromIds[] = $row['word_id'];
        }
        #We've got the first condition
        
        $stmtToTags = "SELECT * FROM tags WHERE flag = 'to'";
        $returnToTags = $db->query($stmtToTags);
        while ($row = $returnToTags->fetchArray(SQLITE3_ASSOC)) {
            #Now for every language combination with the specified FROM we check whether there are any words
            $toIds = array();
            $stmtToIds = $db->prepare("SELECT * FROM ".$row['tag_name']."");
            $stmtToIds->bindValue(':id', 1, SQLITE3_INTEGER);
            $resultToIds = $stmtToIds->execute();
            while($row2 = $resultToIds->fetchArray(SQLITE3_ASSOC)) {
               $toIds[] = $row2['word_id'];
            }
            #checking the number of words for language pair
            $count = count(array_intersect($toIds, $fromIds));
            #echo $count."Count<br>";
            if ($count) {
                $return .= $row['tag_name'].";";
            }
        }
        echo $return;
    } else {
        echo "";
    }
?>
