<?php

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['name']) && isset($_POST['desc']) && isset($_POST['age'])) {
        $myObj = new stdClass();
        $myObj->name = $_POST['name'];
        $myObj->desc = $_POST['desc'];
        $myObj->age = $_POST['age'];

        $sanitized_name = preg_replace("/[^a-z]/i","",$_POST['name']);

        $fpath = "pets/" . $sanitized_name;

        file_put_contents($fpath, json_encode($myObj));

        echo "Success! View your pet here: <a href='" . $fpath . "'>" . $fpath . "</a>";

        exit();
    } else {
        die("Bad request data");
    }
}

?>

<!DOCTYPE html>

<html>
<head>
    <title>Pet designer!</title>
</head>

<body>
    <a href="/">Home</a>

    <form method="POST">
        <p>
            Pet name:
            <input name="name">
        </p>
        <p>
            Pet description:
            <input name="desc">
        </p>
        <p>
            Pet age:
            <input name="age">
        </p>

        <input type="submit">
    </form>
</body>

</html>