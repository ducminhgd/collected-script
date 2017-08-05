<?php
// fetch private key from file and ready it
$pkeyid = openssl_pkey_get_private("private_key.pem");

$data = 'PHP';

// compute signature
$success = openssl_sign($data, $signature, $pkeyid);
if ($success) {
    echo 'Sign success';
} else {
    echo 'Sign failed'
}

// free the key from memory
openssl_free_key($pkeyid);

$pubkeyid = openssl_pkey_get_public("public_key.pem");

// state whether signature is okay or not
$ok = openssl_verify($data, $signature, $pubkeyid);
if ($ok == 1) {
    echo "good";
} elseif ($ok == 0) {
    echo "bad";
} else {
    echo "ugly, error checking signature";
}
// free the key from memory
openssl_free_key($pubkeyid);
