<?php

if (isset($_POST['name']) && isset($_POST['desc'])) {
    $name = $_POST['name'];

    $sanitized_name = preg_replace("/[^a-z]/i","",$name);

    $file_data = file_get_contents("pets/" . $sanitized_name);
    $data = json_decode($file_data);

    $data->desc = $_POST['desc'];

    file_put_contents("pets/" . $data->name, json_encode($data));

    echo "Successfully updated " . $data->name;
}

?>