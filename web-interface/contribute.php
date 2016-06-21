<?php
require_once('PHPMailer-master/class.phpmailer.php');

class MyDB extends SQLite3
{
   function __construct()
   {
      $this->open('users.db');
   }
}

$db = new MyDB();

if(!$db){
   echo $db->lastErrorMsg();
} else {
   #echo "Opened database successfully\n";
}


if (isset($_FILES['file_src']) && $_FILES['file_src']['error'] == UPLOAD_ERR_OK) {
    if (isset($_POST['author']) && isset($_POST['pin']) && isset($_POST['mail']) && isset($_POST['default_level']) && isset($_POST['from']) && isset($_POST['to']) && isset($_POST['separator']) && isset($_POST['row_delimiter'])) {
        
        //Account managment
        $accErr = 0;
        $PIN_hash = md5($_POST['pin']);
        //Check, whether there's already an account with this email
        $sql = "SELECT * FROM users WHERE mail = '".$_POST['mail']."'";
        $stmt = $db->prepare($sql);
        $stmt->bindValue(':id', 1, SQLITE3_INTEGER);
        $result = $stmt->execute();
        $checkMail = 0;
        while($row = $result->fetchArray(SQLITE3_ASSOC)) {
            $checkMail += 1;
        }
        if ($checkMail) {
            $sql = "SELECT * FROM users WHERE mail = '".$_POST['mail']."' AND PIN_hash = '".$PIN_hash."'";
            $stmt = $db->prepare($sql);
            $stmt->bindValue(':id', 1, SQLITE3_INTEGER);
            $result = $stmt->execute();
            $checkPIN = 0;
            while($row = $result->fetchArray(SQLITE3_ASSOC)) {
                $checkPIN += 1;
            }
            if ($checkPIN) {
                echo "PIN correct!<br>";
            } else {
                echo "PIN incorrect! Close this window and try again!<br>";
                $accErr += 1;
            }
        } else {
            echo "We haven't seen you before (well, your email adress precisely), nice to meet you!<br>";
            $sql = "INSERT INTO `users`(`ID`,`author`,`mail`,`PIN_hash`) VALUES (NULL,'".$_POST['author']."','".$_POST['mail']."','".$PIN_hash."');";
            $stmt = $db->prepare($sql);
            $stmt->execute();
            echo "We've created an account for you, and we're sending you an email with all the data...<br>";
            $data = new PHPMailer();
            $data->From      = "dict.wyd@gmail.com";
            $data->FromName  = "WYD Dictionary";
            $data->Subject   = 'Your account at the World Youth Day Dictionary';
            $data->Body      = "Congratulations! Now you're a dictionary editor! Here is your data, remember it and if you want to change something, reply to this email:\n\nName: ".$_POST['author']."\nPIN: ".$_POST['pin']."\n\nThanks for your input, we're hoping for a great cooperation in the future ;)\nThe WYD-Dict Team";
            $data->AddAddress( $_POST['mail'] );
            if (!$data->send()) {
                echo "Mailer Error: " . $data->ErrorInfo;
            } else {
                echo "The details were sent!<br>";
            }
        }
        
        if (!$accErr) {
            $email = new PHPMailer();
            $email->From      = $_POST['mail'];
            $email->FromName  = $_POST['author'];
            $email->Subject   = 'Words addition';
            $email->Body      = $_POST['author']." wants to add records to the dictionary. Language: ".$_POST['from']."=>".$_POST['to'].". The level is ".$_POST['default_level'].". Their PIN is correct.\n\nTheir additional notes:\n".$_POST['user-input'];

            $name = date('m-d-H-i')."-".$_FILES['file_src']['name'];
            $email->AddAttachment($_FILES['file_src']['tmp_name'], $name);

            $inf = "";
            $inf .= $_POST['row_delimiter']."\n";
            $inf .= $_POST['separator']."\n";
            $inf .= $_POST['author']."\n";
            $inf .= $_POST['from']."\n";
            $inf .= $_POST['to']."\n";
            $inf .= $_POST['default_level']."\n";

            for ($i = 1; $i <count($_POST["common_tag_name"]); $i++) {
                $inf .= $_POST["common_tag_name"][$i] . "<r>" . $_POST["common_readable"][$i] . "</r><d>" . $_POST["common_description"][$i] . "</d>\n";
            }
            $inf .= "\n";
            for ($i = 1; $i < count($_POST["special_tag_name"]); $i++) {
                $inf .= $_POST["special_tag_name"][$i] . "<r>" . $_POST["special_readable"][$i] . "</r><d>" . $_POST["special_description"][$i] . "</d>\n";
            }

            $email->addStringAttachment($inf, $name.'.inf');
            $email->AddAddress( 'dict.wyd@gmail.com' );
            if (!$email->send()) {
                echo "Mailer Error: " . $email->ErrorInfo;
            } else {
                echo "The file was sent and now it will be processed by us. Thank you!";
            }
        }
    } else {
        echo "You didn't fill out all of the fields! Close this window and try again.";
    }
} else {
    echo "You didn't add the attachment or the attachment is to big! Close this window and try again.";
}
$db->close(); unset($db);
?>
