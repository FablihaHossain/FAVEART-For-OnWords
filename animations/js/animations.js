function useBounce(myColor)
	{
			let color = myColor;
			this.el.setAttribute("material", "color", color);

			let x = 0;
			let y = Math.sin(time / 850);
			let z = 0;
			let s = x + " " + y + " " + z;
			this.el.setAttribute("position", s);
	};

function setFloat(words, color)
		{
			words.setAttribute("animation__rise", "autoplay", "true");
			words.setAttribute("animation__fade", "autoplay", "true");
			  
			let x = 0 + " " + 0 + " " + 0;
			let y = 0 + " " + 2 + " " + 0;
			let mySpeed = 5000;

			words.setAttribute("material", "color", color);
	   
			words.setAttribute("animation__rise", {
				"property": "position",
				"from": x,
				"to": y,            
				"dur": mySpeed,
				"easing": "linear",
				"dir": "normal",
				"loop": true
			});

			words.setAttribute("animation__fade", {
				 "property": "material.opacity",
				 "dur": 4000,
				 "from": 1.0,
				 "to": 0.0,
				 "loop": true,
				 "delay": 1000
					});

		};