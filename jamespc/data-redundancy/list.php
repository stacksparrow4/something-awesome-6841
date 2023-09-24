<!DOCTYPE html>

<html>
<head>
    <title>Pet designer!</title>
</head>

<body>
    
<?php

$pet_dir = dirname(__FILE__) . "/pets";
$dir = new DirectoryIterator($pet_dir);
foreach ($dir as $fileinfo) {
    if (!$fileinfo->isDot()) {
        $fname = $fileinfo->getFilename();
        
        $file_data = file_get_contents("pets/" . $fname);
        $data = json_decode($file_data);

        echo "<p>\n";
        echo 'PET "' . $data->name . '" with description "' . $data->desc . '" and age "' . $data->age . '"';
        echo "\n";

        echo '<!-- <a href="pets/' . $fname . '"> DEBUG ' . $fname . '</a> --> <button onclick="edit(\'' . $fname . '\')">EDIT ' . $fname . '</button><br>';
        echo "\n</p>\n";
    }
}
?>

<script>
async function edit(fname) {
    const newDesc = prompt('Enter new description for ' + fname);
    
    alert(
        await fetch(
            'update.php',
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: 'name=' + encodeURIComponent(fname) + '&desc=' + encodeURIComponent(newDesc)
            }
        ).then(resp => resp.text())
    );

    location.reload();
}
</script>

</body>

</html>