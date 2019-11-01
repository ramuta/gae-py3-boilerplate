// reusable function to find a cookie by its name (key)
function getCookie(n) {
    let a = `; ${document.cookie}`.match(`;\\s*${n}=([^;]+)`);
    return a ? a[1] : '';
}

// reusable function to create a cookie
function createCookie(name, value, days) {
  let expires;
  if (days) {
    let date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    expires = '; expires=' + date.toGMTString();
  } else {
    expires = '';
  }
  document.cookie = name + '=' + value + expires + '; path=/';
};

// find cookie for web app language
let webAppLanguage = getCookie("web-app-lang");

// if cookie exists, set it as the dropdown title
if(webAppLanguage) {
    document.getElementById("navbarDropdownLang").textContent = webAppLanguage;
}

// function for selecting language via dropdown
function selectLang(language) {
    createCookie("web-app-lang", language);
    location.reload();
}
