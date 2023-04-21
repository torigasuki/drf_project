window.onload = () => {
    const payload = localStorage.getItem('payload')
    const payload_json = JSON.parse(payload)
    const intro = document.getElementById('intro')
    var text = payload_json.email
    intro.innerText = text
}
