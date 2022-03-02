
function fetch_status() {
  fetch('{{ request.scheme }}://{{ request.get_host }}/stream-frame/status_{{ channel.id }}.json?ts=' + Date.now())
    .then(response => response.json())
    .then((data) => {
      if (data.status == 'live') {
        document.querySelector("#stream-frame").innerHTML = data.embed;
      } else{
        setTimeout(fetch_status, 10000);
      }
    })
    .catch(e => alert('Error fetching stream status'));
}

fetch_status()
