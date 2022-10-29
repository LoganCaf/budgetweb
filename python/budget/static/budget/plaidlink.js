(async ($) => {
  // Grab a Link token to initialize Link
  const createLinkToken = async () => {
    const res = await fetch("http://localhost:8080/api/create_link_token");
    const data = await res.json();
    const linkToken = data.link_token;
    localStorage.setItem("link_token", linkToken);
    return linkToken;
  };
  // Initialize Link
  const handler = Plaid.create({
    token: await createLinkToken(),
    onSuccess: async (publicToken, metadata) => {
      await fetch("http://localhost:8080/api/exchange_public_token", {
        method: "POST",
        body: JSON.stringify({ public_token: publicToken }),
        headers: {
          "Content-Type": "application/json",
        },
      });
      await getBalance();
    },
    onEvent: (eventName, metadata) => {
      console.log("Event:", eventName);
      console.log("Metadata:", metadata);
    },
    onExit: (error, metadata) => {
      console.log(error, metadata);
    },
  });

  // Start Link when button is clicked
  const linkAccountButton = document.getElementById("link-account");
  linkAccountButton.addEventListener("click", (event) => {
    handler.open();
  });
})(jQuery);

// Retrieves balance information
const getBalance = async function () {
  console.log("---------------1---------------");
  const response = await fetch("http://localhost:8080/api/data", {
    method: "GET",
  });
  console.log("----------------2--------------");
  const data = await response.json();
  
  //Render response data
  const pre = document.getElementById("response");
  pre.textContent = JSON.stringify(data, null, 2);
};

// Check whether account is connected
const getStatus = async function () {
  const account = await fetch("http://localhost:8080/api/is_account_connected");
  const connected = await account.json();
  if (connected.status == true) {
    getBalance();
    console.log("Account is connected");
    document.write(getBalance());
  }
};

getStatus().then(function () {
  console.log("Promise Resolved1");
}).catch(function () {
  console.log("Promise Rejected1");
});
getBalance().then(function () {
  console.log("Promise Resolved2");
}).catch(function () {
  console.log("Promise Rejected2");
});