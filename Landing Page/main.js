
function getJsonFromUrl() {
  var query = location.search.substr(1);
  var result = {};
  query.split('&').forEach(function(part) {
    var item = part.split('=');
    result[item[0]] = decodeURIComponent(item[1]);
  });
  return result;
}

var decoded = getJsonFromUrl();

// background setup
var backgroundColor = decoded.backgroundColor || '000';
document.getElementById('particles-js').style.backgroundColor =
  '#' + backgroundColor;
