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
