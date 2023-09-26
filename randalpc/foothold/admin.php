<?php

if ($_COOKIE['admin_token'] !== 'bfdbjknsdnfbjaefanefgueaigahneg') {
    header('Location: /error.php?prevpage=index.php');
    die();
}

if($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = json_decode(file_get_contents('php://input'));
    echo "Uploading file to directory: " . $data->fileDir . "\n";
    echo "Uploading file name: " . $data->fileName . "\n";

    if (preg_match("/\.php$/i", $data->fileName)) {
        echo "Bad file name! Exiting...\n";
        die();
    }

    mkdir("./files");

    $dirpath = "./files/" . $data->fileDir;

    mkdir($dirpath);

    $realpath = realpath($dirpath);

    echo "Created directory " . $realpath . "\n";

    $fpath = $realpath . "/" . $data->fileName;

    file_put_contents($fpath, $data->fileContent);

    echo "Successfully written data to " . $fpath . "!\n";

    die();
}

?>

<h1>Admin page</h1>

<p>Welcome to the secret admin page!</p>

<p>Here you can upload your files for safe storage:</p>

<input type="file" id="fileupload">

<pre id="output"></pre>

<script>
const getHash = () => Math.floor(Math.random() * 100000000000000000).toString();

fileupload.onchange = () => {
    output.innerHTML = '';
    const reader = new FileReader();
    reader.onload = () => {
        const fHash = getHash();
        const fName = fileupload.files[0].name;
        fetch('admin.php', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                fileDir: fHash,
                fileName: fName,
                fileContent: reader.result
            })
        }).then((res) => {
            output.innerHTML = `Success! Your file can be found here: <a href="files/${fHash}/${fName}">link</a>`;
        }).catch((e) => {
            output.innerHTML = 'An unexpected error occurred!';
        });
    }
    reader.readAsText(fileupload.files[0]);
}
</script>