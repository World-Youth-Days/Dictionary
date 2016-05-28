<?php
require_once('PHPMailer-master/class.phpmailer.php');
$email = new PHPMailer();
$email->From      = $_POST['mail'];
$email->FromName  = $_POST['author'];
$email->Subject   = 'Words addition';
$email->Body      = $_POST['author']." wants to add records to the dictionary. Language: ".$_POST['from']."=>".$_POST['to'].". The level is ".$_POST['default_level']." His PIN is correct.";

$name = date('m-d')."-".$_POST['author'].".";
if (isset($_FILES['file_src']) && $_FILES['file_src']['error'] == UPLOAD_ERR_OK) {
    $email->AddAttachment($_FILES['file_src']['tmp_name'], $name.pathinfo($_FILES['file_src']['name'], PATHINFO_EXTENSION));
} else {
    echo "Brak załączika!";
}

$inf = "";
$inf .= $_POST['author']."/n";
$inf .= $_POST['from']."/n";
$inf .= $_POST['to']."/n";
$inf .= $_POST['level']."/n";

for ($i = 0; $<count($_POST["common_tag_name"]); $i++) {
    $inf .= $_POST["common_tag_name"][$i] . "<r>" . $_POST["common_readable"][i] . "</r><d>" . $_POST["common_description"][$i] . "</d>";
}

$email->addStringAttachment($inf, $name.'.inf');
$email->AddAddress( 'test@localhost' );
return $email->Send();
?>