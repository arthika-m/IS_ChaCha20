
function showStatus(message, success = true) {
    const status = document.getElementById("status");
    status.textContent = message;
    status.className = success ? "success" : "error";
}


// ENCRYPTION

async function encryptMessage() {
    const message = document.getElementById("message").value;

    if (!message) {
        showStatus("Please enter a plaintext message.", false);
        return;
    }

    try {
        const response = await fetch("/encrypt", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error);
        }

        document.getElementById("encKey").value = data.key;
        document.getElementById("encNonce").value = data.nonce;
        document.getElementById("encCipher").value = data.ciphertext;

        showStatus("Encryption successful! Copy the key, nonce and ciphertext for manual decryption.");

    } catch (error) {
        showStatus(error.message, false);
    }
}


// COPY SECRET KEY

async function copyKey() {
    await copyValue("encKey", "Secret key copied!");
}


// COPY NONCE

async function copyNonce() {
    await copyValue("encNonce", "Nonce copied!");
}


// COPY CIPHERTEXT

async function copyCipher() {
    await copyValue("encCipher", "Ciphertext copied!");
}


async function copyValue(id, message) {
    const value = document.getElementById(id).value;

    if (!value) {
        showStatus("Generate encryption details first.", false);
        return;
    }

    try {
        await navigator.clipboard.writeText(value);
        showStatus(message);
    } catch {
        showStatus("Copy failed. Please copy manually.", false);
    }
}


// MANUAL DECRYPTION

async function decryptMessage() {
    const ciphertext =
        document.getElementById("decCipher").value.trim();

    const key =
        document.getElementById("decKey").value.trim();

    const nonce =
        document.getElementById("decNonce").value.trim();

    if (!ciphertext || !key || !nonce) {
        showStatus("Please enter ciphertext, secret key and nonce.", false);
        return;
    }

    try {
        const response = await fetch("/decrypt", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                ciphertext: ciphertext,
                key: key,
                nonce: nonce
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error);
        }

        document.getElementById("decrypted").value =
            data.decrypted;

        showStatus("Decryption successful! Original message recovered.");

    } catch (error) {
        document.getElementById("decrypted").value = "";
        showStatus(error.message, false);
    }
}


// CLEAR DECRYPTION SECTION

function clearDecryption() {
    document.getElementById("decCipher").value = "";
    document.getElementById("decKey").value = "";
    document.getElementById("decNonce").value = "";
    document.getElementById("decrypted").value = "";

    showStatus("Decryption fields cleared.");
}
