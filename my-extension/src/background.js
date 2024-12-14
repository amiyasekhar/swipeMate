let tinderToken = null;

// Function to check all open tabs for Tinder
function checkTinderTab() {
  chrome.tabs.query({}, (tabs) => {
    let tinderTabFound = false;
    for (let tab of tabs) {
      if (tab.url && tab.url.includes("tinder.com")) {
        console.log("Tinder is open in tab:", tab.id);
        tinderTabFound = true;
        monitorNetworkRequests();
        return;
      }
    }
    if (!tinderTabFound) {
      console.log("No Tinder tab found.");
    }
  });
}

// Function to monitor network requests to Tinder's API
function monitorNetworkRequests() {
  if (tinderToken) {
    console.log("Token already captured:", tinderToken);
    return;
  }

  console.log("Monitoring network requests for Tinder...");

  // Listen for outgoing network requests
  chrome.webRequest.onBeforeSendHeaders.addListener(
    (details) => {
      const headers = details.requestHeaders;

      console.log("Request details:", details); // Debug: Log request details

      // Iterate through headers to find X-Auth-Token
      for (let header of headers) {
        if (header.name.toLowerCase() === "x-auth-token") {
          tinderToken = header.value;
          console.log("Captured X-Auth-Token:", tinderToken);

          // Display token to the user
          //alert("Tinder Auth Token: " + tinderToken);

          // Save token to local storage for persistence
          chrome.storage.local.set({ tinderAuthToken: tinderToken }, () => {
            console.log("Auth token saved to local storage.");
          });

          // Stop monitoring further requests after capturing the token
          chrome.webRequest.onBeforeSendHeaders.removeListener(
            arguments.callee
          );
          return;
        }
      }
    },
    { urls: ["*://api.gotinder.com/*"] }, // Filter for Tinder API requests
    ["requestHeaders"]
  );
}

// Run when the extension is installed or updated
chrome.runtime.onInstalled.addListener(() => {
  console.log("Extension installed. Searching for Tinder...");
  checkTinderTab();
});

// Listen for the extension's action button being clicked
chrome.action.onClicked.addListener(() => {
  console.log("Extension clicked. Checking for Tinder tab...");
  checkTinderTab();
});

// Debug: Log when the extension starts running
console.log("SwipeMate background script initialized.");
monitorNetworkRequests(); // Start monitoring immediately
