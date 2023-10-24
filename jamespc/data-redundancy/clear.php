<?php
$files = glob('pets/*'); // get all file names
foreach($files as $file){ // iterate files
  if(is_file($file)) {
    unlink($file); // delete file
  }
}
?>

<p>Pets Cleared!</p>
<a href="/">Go back</a>