// -------------------------------------------------------- SCENE
var scene = new THREE.Scene();

// -------------------------------------------------------- CAMERA
var camera = new THREE.PerspectiveCamera( 
  75, window.innerWidth/window.innerHeight, 0.1, 100 
  );
  
camera.position.z = 3;

// -------------------------------------------------------- LIGHTS


const color = 0xFFFFFF;
const intensity = 1.0;
const light = new THREE.DirectionalLight(color, intensity);

light.position.set(7, 30, 0);
light.target.position.set(-10, 0, -100);
scene.add(light);
scene.add(light.target);

// -------------------------------------------------------- RENDERER

var texture = new THREE.TextureLoader().load( 'https://i.ibb.co/QD8w2W6/Watercolor-geographical-map-of-the-world-Physical-map-of-the-world-Realistic-image-Isolated-on-white.jpg' );
var geometry = new THREE.SphereGeometry( 1, 180, 90);
var material = new THREE.MeshLambertMaterial({ map: texture });
var mesh = new THREE.Mesh(geometry, material);
scene.add( mesh );

var renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
renderer.setSize( 600, 300);
var canvas = document.getElementById('earth-container');
canvas.appendChild( renderer.domElement );

function resize() {
  renderer.setSize(w, h);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
}; 

window.addEventListener("resize", resize);

// -------------------------------------------------------- ANIMATION

var animate = function () {
	requestAnimationFrame(animate);
	mesh.rotation.y += 0.015;
  renderer.render(scene, camera);
};

animate();