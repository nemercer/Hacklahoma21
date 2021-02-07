  (function() {
    function replaceTwitterWord() {
      var tweetContent = document.querySelectorAll("div[lang]");
  
        // if 0 (hate speech) replace with redacted
        // if 1 (offensive language) replace offensive word with non offensive word

      [].slice.call(tweetContent).forEach(function(el){
        var newContent = el.innerHTML.replace(/.*/s,"justin");
        if (newContent != el.innerHTML) {
          el.innerHTML = newContent;
        }
      });
    }
  
    // Replace words every 5000 ticks
    function tick() {
        // If it determines hate speech of offensive language (0/1)

        replaceTwitterWord();
        window.setTimeout(tick, 5000);
    }
  
    tick();
  })();