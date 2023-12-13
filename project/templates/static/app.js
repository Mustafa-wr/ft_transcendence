let autoBtn = document.querySelector(".auto-btn");

function authorize() {
  var authorizationUrl =
    "https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-8156fc58fc2005216ad58258e48c1a311ceb0c4b4bd45451aba59272720501f4&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fcallback&response_type=code"; // Замените на ваш URL

  window.location.href = authorizationUrl;
}

autoBtn.addEventListener("click", authorize);
