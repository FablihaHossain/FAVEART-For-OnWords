
// DISCUSS: font.setAttribute("font", "src", "fonts/Cinzel_Bold.json")

function setBounce(words, color, time, font)
	{
			words.setAttribute("material", "color", color);

			let x = 0;
			let y = Math.sin(time / 850);
			let z = 0;
			let s = x + " " + y + " " + z;

			//words.setAttribute("animation__bounce", "autoplay", "true");
			words.setAttribute("position", s);

			// let a = 0 + " " + 0 + " " + 0;
			// let b = 0 + " " + 2 + " " + 0;			

			// words.setAttribute("animation__bounce", {
			// 	"position": s,
			// 	"elasticity": 3000,
			// 	"loop": true
			// 	});

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
		//words.setAttribute("text-geometry", "align", "center");
		words.setAttribute("text-geometry", "xOffset", 100)

	};

function setTilt(words, color, font)
	{
		let a = 0 + " " + 0 + " " + 45;
		let b = 0 + " " + 0 + " " + -45;
		let dur = 10000;

		//rotation="0 0 0"
		words.setAttribute("material", "color", color);

		words.setAttribute("animation", "autoplay", "false");

		words.setAttribute("animation", {
			"property": "rotation",
			"from": b,
			"to": a,
			"loop": true,
			"dur": dur
		});

		words.setAttribute("text-geometry", "font", font);
		//words.setAttribute("text-geometry", "align", "center");
		words.setAttribute("text-geometry", "xOffset", 100)

	};

console.log("animations.js");