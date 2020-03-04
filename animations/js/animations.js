
// DISCUSS: font.setAttribute("font", "src", "fonts/Cinzel_Bold.json")

function setBounce(words, color, fontID)
	{
			words.setAttribute("material", "color", color);

			words.setAttribute("animation__bounce", "autoplay", "true");

			let a = 0 + " " + 0 + " " + 0;
			let b = 0 + " " + 1 + " " + 0;			

			words.setAttribute("animation__bounce", {
			"property": "position",
			"from": b,
			"to": a,
			"loop": true,
			"dur": 500,
			"dir": "alternate"
			});			

		words.setAttribute("text-geometry", "font", fontID);

		let obj = words.getObject3D('mesh');
		let box = new THREE.Box3().setFromObject(obj);
		let offset = ((box.min.x - box.max.x)/2);
		obj.position.set(offset, 0, 0);
		
	};

function setFloat(words, color, fontID)
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

			words.setAttribute("text-geometry", "font", fontID);

			let obj = words.getObject3D('mesh');
			let box = new THREE.Box3().setFromObject(obj);
			let offset = ((box.min.x - box.max.x)/2);
			obj.position.set(offset, 0, 0);

	};

function setRotate(words, color, fontID)
	{
		let x = 0 + " " + 360 + " " + 0;
		let dur = 5000;

		//rotation="0 0 0"
		words.setAttribute("material", "color", color);


		words.setAttribute("animation", {
			"property": "rotation",
			"easing": "easeInOutQuint",
			"to": x,
			"loop": true,
			"dur": dur,
		});

		words.setAttribute("text-geometry", "font", fontID);
		
		if (words.getObject3D('mesh').position.x == 0) {
			let obj = words.getObject3D('mesh');
			let box = new THREE.Box3().setFromObject(obj);
			let offset = ((box.min.x - box.max.x)/2);
			obj.position.set(offset, 0, 0);
		};

		//Credit to: https://stackoverflow.com/questions/54892378/aframe-text-geometry-component-rotation-from-center

	};

function setTilt(words, color, fontID)
	{
		let a = 0 + " " + 0 + " " + 45;
		let b = 0 + " " + 0 + " " + -45;
		let dur = 10000;

		//rotation="0 0 0"
		words.setAttribute("material", "color", color);

		words.setAttribute("animation", "autoplay", "true");

		words.setAttribute("animation", {
			"property": "rotation",
			"from": b,
			"to": a,
			"loop": true,
			"dur": dur,
			"dir": "alternate"
		});

		words.setAttribute("text-geometry", "font", fontID);
		//words.setAttribute("text-geometry", "align", "center");
		//words.setAttribute("text-geometry", "xOffset", 100)


		let obj = words.getObject3D('mesh');
		let box = new THREE.Box3().setFromObject(obj);
		let offset = ((box.min.x - box.max.x)/2);
		obj.position.set(offset, 0, 0);

		//Credit to: https://stackoverflow.com/questions/54892378/aframe-text-geometry-component-rotation-from-center

	};

function setFlash(words, color, fontID)
	{
		words.setAttribute("material", "color", color);

		words.setAttribute("animation", {
				 "property": "material.opacity",
				 "dur": 500,
				 "from": 1.0,
				 "to": 0.0,
				 "loop": true,
				 "dir": "alternate"
					});

		words.setAttribute("text-geometry", "font", fontID);

		let obj = words.getObject3D('mesh');
		let box = new THREE.Box3().setFromObject(obj);
		let offset = ((box.min.x - box.max.x)/2);
		obj.position.set(offset, 0, 0);

	};

console.log("animations.js");