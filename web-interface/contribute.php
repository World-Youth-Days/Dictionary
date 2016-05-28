<?php
require_once('PHPMailer-master/class.phpmailer.php');

$check = TRUE;

if ($check) {
    if (isset($_FILES['file_src']) && $_FILES['file_src']['error'] == UPLOAD_ERR_OK) {
        if (isset($_POST['author']) && isset($_POST['pin']) && isset($_POST['mail']) && isset($_POST['default_level']) && isset($_POST['from']) && isset($_POST['to']) && isset($_POST['separator']) && isset($_POST['row_delimiter'])) {
            $email = new PHPMailer();
            $email->From      = $_POST['mail'];
            $email->FromName  = $_POST['author'];
            $email->Subject   = 'Words addition';
            $email->Body      = $_POST['author']." wants to add records to the dictionary. Language: ".$_POST['from']."=>".$_POST['to'].". The level is ".$_POST['default_level'].". His PIN is correct.";

            $name = date('m-d')."-".$_POST['author'].".".pathinfo($_FILES['file_src']['name'], PATHINFO_EXTENSION);
            $email->AddAttachment($_FILES['file_src']['tmp_name'], $name);

            $inf = "";
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
            $email->AddAddress( 'aaaaaa.hberes@gmail.com' );
            if (!$email->send()) {
                echo "Mailer Error: " . $mail->ErrorInfo;
            } else {
                echo "Message sent!";
            }
        } else {
            echo "You didn't fill out all of the fields! Close this window and try again.";
        }
    } else {
        echo "You didn't add the attachment or the attachment is to big! Close this window and try again.";
    }
} else {
    echo "User's name and the PIN don't match. Close this window and try again.";
}
?>