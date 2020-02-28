function setBounce(words, myColor, time, font)
	{
			let color = myColor;
			words.setAttribute("material", "color", color);

			let x = 0;
			let y = Math.sin(time / 850);
			let z = 0;
			let s = x + " " + y + " " + z;
			words.setAttribute("position", s);

			words.setAttribute("text-geometry", "font", font);

	};

function setFloat(words, color, font)
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

			words.setAttribute("text-geometry", "font", font);
	};

function setRotate(words, color, font)
	{
		let x = 0 + " " + 360 + " " + 0;
		let dur = 10000;

		//rotation="0 0 0"
		words.setAttribute("material", "color", color);


		words.setAttribute("animation", {
			"property": "rotation",
			"to": x,
			"loop": true,
			"dur": dur
		});

		words.setAttribute("text-geometry", "font", font);

	};

console.log("animations.js");