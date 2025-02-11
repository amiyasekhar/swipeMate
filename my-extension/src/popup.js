// Retrieve the token from Chrome storage
chrome.storage.local.get("tinderAuthToken", async (result) => {
  const authToken = result.tinderAuthToken;
  console.log("RES = ", result);
  console.log("AUTH TOKEN ", authToken);
});
document.getElementById("pay-now").addEventListener("click", async () => {
  const renderBackend = "https://swipemate.onrender.com";

  // Retrieve the token from Chrome storage
  chrome.storage.local.get("tinderAuthToken", async (result) => {
    const authToken = result.tinderAuthToken;
    //console.log("RES = ", json.stringify(result));
    console.log("AUTH TOKEN ", authToken);
    if (!authToken) {
      console.error("Auth token not found in storage.");
      alert(
        "Authentication token not available. Please make sure you are logged into Tinder."
      );
      return;
    }

    console.log("Using auth token:", authToken);

    try {
      const response = await fetch(`${renderBackend}/create-checkout-session`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ authToken: authToken }), // Use the retrieved token
      });

      if (!response.ok) {
        throw new Error("Failed to create checkout session");
      }

      const session = await response.json();
      console.log("Checkout session created:", session);

      // Open the checkout URL in a new tab
      chrome.tabs.create({ url: session.url });
    } catch (error) {
      console.error("Error during payment:", error);
      alert("An error occurred during payment. Please try again.");
    }
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("auth-status");

  // Function to update the UI
  const renderUI = (authTokenFound) => {
    if (authTokenFound) {
      container.innerHTML = `
      <h1 class="title">Auth Token Found</h1>
      <p class="step-text">Your authentication token was found. You can now proceed.</p>
      <button id="pay-now" class="cta-btn">Pay Now</button>
    `;
    } else {
      container.innerHTML = `
      <h1 class="title">Auth Token Not Found</h1>
      <p class="step-text">Please open Tinder, log in, and try again.</p>
      <button id="retry" class="cta-btn">Retry</button>
    `;
    }

    // Add event listener to the Retry button
    document.getElementById("retry").addEventListener("click", () => {
      checkAuthToken(); // Retry the check
    });
  };

  // Function to check auth token status
  const checkAuthToken = () => {
    chrome.runtime.sendMessage({ action: "checkAuthToken" }, (response) => {
      const authTokenFound = response?.authTokenFound || false;
      renderUI(authTokenFound);
    });
  };

  // Initial check
  checkAuthToken();
});
