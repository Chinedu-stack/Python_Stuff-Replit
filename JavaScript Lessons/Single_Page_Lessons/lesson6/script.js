const content = {
    home: "<h2>Home</h2><p>Welcome!</p>",
    football: "<h2>Football</h2><p>Train hard.</p>",
    school: "<h2>School</h2><p>Stay focused.</p>"
}


function init() {
    document.getElementById('btn-home').classList.add('active');
    document.getElementById('home').style.display = 'block';
    document.getElementById('home').innerHTML = content['home'];
}

function showSection(id) {
      const sections = document.querySelectorAll('.section');
      sections.forEach(function(s) { s.style.display = 'none'; });

      const buttons = document.querySelectorAll('nav button');
      buttons.forEach(function(b) { b.classList.remove('active'); });

      document.getElementById(id).style.display = 'block';
      document.getElementById(id).innerHTML = content[id]
      document.getElementById('btn-' + id).classList.add('active');
    }
    
init()
