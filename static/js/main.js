window.onload = function() {
  let inputs = document.getElementsByTagName("input")
  for (i = 0; i < inputs.length; i++) {
    inputs[i].addEventListener("input", function(e) {
      console.log(e)
      e.target.classList.remove("input-error")
    })
}
}