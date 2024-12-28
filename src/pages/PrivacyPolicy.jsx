import React from 'react';

const PrivacyPolicy = () => {
    return (
        <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
            <h1>Privacy Policy</h1>
            <p>
                Our Chrome extension is committed to maintaining user privacy. Below is a summary of our privacy practices:
            </p>
            <ul>
                <li>
                    <strong>No External Data Collection:</strong> We do not collect, process, or store personal data on external servers.
                </li>
                <li>
                    <strong>Local Storage Only:</strong> The extension uses local storage within the Chrome browser solely for functionality purposes, such as securely storing the authentication token.
                </li>
                <li>
                    <strong>Limited Data Transmission:</strong> The extension does not share or transmit user data to external servers, except for necessary interactions with our Flask-based AI model to provide core functionality.
                </li>
            </ul>
            <p>
                By using our extension, you can rest assured that your data remains private and is handled securely.
            </p>
        </div>
    );
};

export default PrivacyPolicy;
