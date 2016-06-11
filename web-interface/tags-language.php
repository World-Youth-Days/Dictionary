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
    
    if ($_GET['from']!="undefined" && $_GET['to']!="undefined"){
        #echo "Start";
        $from = $_GET['from'];
        $to = $_GET['to'];
        $fromIds = array();
        $toIds = array();
        $return = "";
        
        $stmtFromIds = $db->prepare("SELECT * FROM '".$from."'");
        $stmtFromIds->bindValue(':id', 1, SQLITE3_INTEGER);
        $resultFromIds = $stmtFromIds->execute();
        while($row = $resultFromIds->fetchArray(SQLITE3_ASSOC)) {
            $fromIds[] = $row['word_id'];
        }
//        foreach ($fromIds as $value) {
//            echo $value;
//        }
//        echo "<br>";
        #We've got the first (from) condition
        
        $stmtToIds = $db->prepare("SELECT * FROM '".$to."'");
        $stmtToIds->bindValue(':id', 1, SQLITE3_INTEGER);
        $resultToIds = $stmtToIds->execute();
        while($row = $resultToIds->fetchArray(SQLITE3_ASSOC)) {
            $toIds[] = $row['word_id'];
        }
//        foreach ($toIds as $value) {
//            echo $value;
//        }
//        echo "<br>";
        
        $stmtLiveTags = "SELECT * FROM tags WHERE flag = 'live'";
        $returnLiveTags = $db->query($stmtLiveTags);
        while ($row = $returnLiveTags->fetchArray(SQLITE3_ASSOC)) {
            #Now for every language combination with the specified FROM we check whether there are any words
            $liveIds = array();
            $stmtLiveIds = $db->prepare("SELECT * FROM ".$row['tag_name']."");
            $stmtLiveIds->bindValue(':id', 1, SQLITE3_INTEGER);
            $resultLiveIds = $stmtLiveIds->execute();
            while($row2 = $resultLiveIds->fetchArray(SQLITE3_ASSOC)) {
               $liveIds[] = $row2['word_id'];
            }
            #checking the number of words for language pair
            $count = count(array_intersect($toIds, $fromIds, $liveIds));
            #echo $count."Count<br>";
            if ($count) {
                $return .= $row['tag_name'].";";
            }
        }
        echo $return;
        if ($return == "") echo "//ABC//";
    } else {
        echo "//ABC//";
    }
    $db->close(); unset($db);
?>
