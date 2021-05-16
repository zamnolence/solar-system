/* Get data from NASA API */
function searchNASA() {
  q = document.getElementById('planet-select').value
  $.ajax({
    url: 'https://images-api.nasa.gov/search?q='+q,
    error: function (jqXHR, textStatus, errorThrown) {
      console.log(textStatus); /* Write status to console if error */
    },
    success: function(img) {
    document.getElementById("planet-image").innerHTML = "<img class='planet-image center-block' src='"+img.collection.items[0].links[0].href+"'/>";
  }
})};
$(function(){
  $('#planet-select').change(function(){
      var selected = $(this).find(':selected').text();
      $(".desc").hide();
      $('#' + selected).show();
  }).change()
});


/* Progress bar as we scroll */
window.onscroll = function () { progbarFunc() };
function progbarFunc() {
  /* scrollTop measures distance from element's top to its topmost visible content */
  var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
  /* Calculate height from height of document - viewable (client) height*/
  var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  /* Calculate percentage height we've already scrolled */
  var scrolled = (winScroll / height) * 100;
  /* Change the width of the progress bar */
  document.getElementById("progbar").style.width = scrolled + "%";
}




// var selectPlanet = document.getElementById('planet-select')

// selectPlanet.addEventListener("change", ()=>{
//   console.log("planet selected!")
//   sendAPIRequest()
// })

// async function sendAPIRequest() {
//   let API_KEY = "bPSbdUIbdNajjsknz4RdQyVZywGoHyJk0kuMbabW" /* NASA API KEY */
//   let response = await fetch(`https://api.nasa.gov/planetary/apod?api_key=${ API_KEY }`);
//   let data = await response.json()
//   console.log("data is here!")
//   searchNASAimage(data);
// }

// function searchNASAimage(data) {
//   document.getElementById("planet-image").innerHTML = `<img src="${data.url}">`
//   console.log("img found!")
// }