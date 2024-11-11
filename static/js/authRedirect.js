// Create the main myMSALObj instance
// configuration parameters are located at authConfig.js
const myMSALObj = new msal.PublicClientApplication(msalConfig);

let username = "";

/**
 * A promise handler needs to be registered for handling the
 * response returned from redirect flow. For more information, visit:
 * https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-browser/docs/acquire-token.md
 */
myMSALObj.handleRedirectPromise()
    .then(handleResponse)
    .catch((error) => {
        console.error(error);
    });

function selectAccount () {

    /**
     * See here for more info on account retrieval: 
     * https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-common/docs/Accounts.md
     */

    const currentAccounts = myMSALObj.getAllAccounts();

    if (currentAccounts.length === 0) {
        return;
    } else {
        username = currentAccounts[0].username;
    }
}

function handleResponse(response) {
    if (response !== null) {
        username = response.account.username;
        loginUserBackend()
    } else {
        selectAccount();
    }
}

function signIn() {

    /**
     * You can pass a custom request object below. This will override the initial configuration. For more information, visit:
     * https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-browser/docs/request-response-object.md#request
     */

    myMSALObj.loginRedirect(loginRequest);
}

function signOut() {

    /**
     * You can pass a custom request object below. This will override the initial configuration. For more information, visit:
     * https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-browser/docs/request-response-object.md#request
     */
    console.log(location.origin + "/singlelogout");
    const logoutRequest = {
        account: myMSALObj.getAccountByUsername(username),
        postLogoutRedirectUri: location.origin + "/singlelogout",
    };
    if(myMSALObj.getAllAccounts().length > 0) {
        myMSALObj.logoutRedirect(logoutRequest);
    }
    else {
        window.location.href = location.origin + "/singlelogout";
    }
}

function getTokenRedirect(request) {
    /**
     * See here for more info on account retrieval: 
     * https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-common/docs/Accounts.md
     */
    request.account = myMSALObj.getAccountByUsername(username);

    return myMSALObj.acquireTokenSilent(request)
        .catch(error => {
            console.warn("silent token acquisition fails. acquiring token using redirect");
            if (error instanceof msal.InteractionRequiredAuthError) {
                // fallback to interaction when silent call fails
                return myMSALObj.acquireTokenRedirect(request);
            } else {
                console.warn(error);   
            }
        });
}

function seeProfile() {
    getTokenRedirect(loginRequest)
        .then(response => {
            callMSGraph(graphConfig.graphMeEndpoint, response.accessToken, null);
        }).catch(error => {
            console.error(error);
        });
}

function loginUserBackend() {
    var account = myMSALObj.getAllAccounts()[0];
        document.getElementById("loadingBG").hidden = false;
    fetch(location.origin + "/singlelogin/", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: account.username,
          password: account.localAccountId,
          name: account.name
        })
      })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            document.getElementById("loadingBG").hidden = true;
            if(data["message"] == "logged in successfully") {
                console.log("logged in successfully");
                location.reload();
            }
            else if(data["message"] == "only amb allowed on site") {
                alert("Only AMB Students are allowed on this site");
                signOut();
            }
            else if(data["message"] == "user created successfully complete student setup") {
                showLoginPopup('finishsetupstudent', true);
                document.getElementsByClassName('popupBG')[0].hidden = false;
            }
            else if(data["message"] == "faculty created successfully") {
                location.href = location.origin
            }
            
        })
        .catch(error => console.error('Error:', error));
}