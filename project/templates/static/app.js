let autoBtn = document.querySelector(".auto-btn");

function authorize() {
  var authorizationUrl =
    "https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-53a3167e09d6ecdd47402154ef121f68ea10b4ec95f2cb099cf3d92e56a0c822&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fcallback&response_type=code"; // Замените на ваш URL

  window.location.href = authorizationUrl;
}

autoBtn.addEventListener("click", authorize); 
