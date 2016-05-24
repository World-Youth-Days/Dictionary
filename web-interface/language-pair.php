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
    
        $from = $_GET['from'];
        $base_query = "SELECT * FROM 'words' WHERE (";
        $return = "";
        
        $stmt = $db->prepare("SELECT * FROM '".$from."'");
        $stmt->bindValue(':id', 1, SQLITE3_INTEGER);
        $result = $stmt->execute();
        while($row = $result->fetchArray(SQLITE3_ASSOC)) {
            $base_query .= "id=".$row['word_id']." OR ";
        }
        $base_query = substr($base_query, 0, -4);
        $base_query .= ") AND (";
        #echo $base_query."<br>";
        #We've got the first condition
        
        $sql = "SELECT * FROM 'tags' WHERE flag = 'to'";
        $ret = $db->query($sql);
        while ($row = $ret->fetchArray(SQLITE3_ASSOC)) {
            #Now for every language combination with the specified FROM we check whether there are any words
            $temp_query = $base_query;
            $stmt = $db->prepare("SELECT * FROM '".$row['tag_name']."'");
            $stmt->bindValue(':id', 1, SQLITE3_INTEGER);
            $result = $stmt->execute();
            while($row2 = $result->fetchArray(SQLITE3_ASSOC)) {
                $temp_query .= "id=".$row2['word_id']." OR ";
            }
            $temp_query = substr($temp_query, 0, -4);
            $temp_query .= ")";
            #echo $row['tag_name']."<br>";
            #echo $temp_query."<br>";
            #checking the number of words for language pair
            $count = 0;
            $retForCount = $db->query($temp_query);
            while ($rowForCount = $retForCount->fetchArray(SQLITE3_ASSOC)) {$count += 1;}
            #echo $count;
            if ($count) {
                $return .= $row['tag_name'].";";
            }
        }
        echo $return;
    } else {
        echo "";
    }
?>
