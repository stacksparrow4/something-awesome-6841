<?php

$prevpage = '/index.php';
if(isset($_GET['prevpage'])) {
    $prevpage = $_GET['prevpage'];
}

$prevpage = htmlspecialchars($prevpage);

?>

<p>An unexpected error occurred. Perhaps you do not have the authorisation to access this page?</p>

<a href='<?= $prevpage ?>'>Go back to previous page</a>
