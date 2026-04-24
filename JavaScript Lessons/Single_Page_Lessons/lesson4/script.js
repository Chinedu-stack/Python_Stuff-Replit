function showSection(id) {
      var sections = document.querySelectorAll('.section');
      sections.forEach(function(s) { s.style.display = 'none'; });

      var buttons = document.querySelectorAll('nav button');
      buttons.forEach(function(b) { b.classList.remove('active'); });

      document.getElementById(id).style.display = 'block';
      document.getElementById('btn-' + id).classList.add('active');
    }

    document.getElementById('btn-home').classList.add('active');
    document.getElementById('home').style.display = 'block';