import React from 'react';
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import brain from './brain.glb'


class Brain extends React.Component {
  constructor(props) {
    super(props)
    this.start = this.start.bind(this)
    this.stop = this.stop.bind(this)
    this.animate = this.animate.bind(this)
  }

  componentDidMount() {
    const width = this.mount.clientWidth
    const height = this.mount.clientHeight
    const scene = new THREE.Scene()

    // var raycaster = new THREE.Raycaster();
    // var mouse = new THREE.Vector2();
    // this.raycaster = raycaster
    // this.mouse = mouse

    var _this = this
    var loader = new GLTFLoader()

    loader.load(brain, function (gltf) {
      var mesh = gltf.scene.children[0]
      var material = new THREE.MeshPhongMaterial( { color: 'black', specular: 'white', shininess: 20} );
      mesh.material = material;
      scene.add(mesh)

      const camera = new THREE.PerspectiveCamera(
        65,
        width / height,
        0.1,
        1000
      )
      const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
      camera.position.z = 4
      var light = new THREE.DirectionalLight('white', 1.5);
      light.position.x = 3
      light.position.y = 4
      light.position.z = 4
      scene.add(light);
      // renderer.setClearColor('black')
      renderer.setSize(width, height)

      _this.scene = scene
      _this.camera = camera
      _this.renderer = renderer
      _this.mesh = mesh
      _this.mount.appendChild(_this.renderer.domElement)
      _this.start()
    }, undefined, function (error) {
      console.error(error);
    });
  }
  
  componentWillUnmount() {
    this.stop()
    this.mount.removeChild(this.renderer.domElement)
  }

  // shouldComponentUpdate(nextProps, nextState) {
  //   return false;
  // }

  start() {
    if (!this.frameId) {
      this.frameId = requestAnimationFrame(this.animate)
    }
  }

  stop() {
    cancelAnimationFrame(this.frameId)
  }

  animate() {
    this.mesh.rotation.y += -0.003
    this.renderScene()
    this.frameId = window.requestAnimationFrame(this.animate)
  }

  renderScene() {
    // var INTERSECTED
    // this.raycaster.setFromCamera(this.mouse, this.camera);
    // var intersects = this.raycaster.intersectObjects(this.scene.children);
    // for ( var i = 0; i < intersects.length; i++ ) {
    //   intersects[ i ].object.material.color.set( 0xff0000 );
    //   console.log('intersection!')
    // }
      // if (intersects.length > 0) {
      //   if (INTERSECTED != intersects[0].object) {
      //     if (INTERSECTED)
      //       INTERSECTED.material.emissive.setHex( INTERSECTED.currentHex );
      //     INTERSECTED = intersects[0].object;
      //     INTERSECTED.currentHex = INTERSECTED.material.emissive.getHex();
      //     INTERSECTED.material.emissive.setHex( 0xff0000 );
      //     console.log('intersected brain');
      //   }
      // } else {
      //   if (INTERSECTED)
      //     INTERSECTED.material.emissive.setHex( INTERSECTED.currentHex );
      //   INTERSECTED = null;
      //   console.log('nope')
      // }

    this.renderer.render(this.scene, this.camera);
  }

  render() {
    // var _this = this

    // function onMouseMove(event) {
    //   console.log(event)
    //   _this.mouse.x = (event.clientX / _this.innerWidth) * 2 - 1;
    //   _this.mouse.y = - (event.clientY / _this.innerHeight) * 2 + 1;
    // }

    // window.addEventListener('mousemove', onMouseMove, false);

    return (
      <div
        style={{ width: '400px', height: '200px' }}
        ref={(mount) => { this.mount = mount }}
      />
    )
  }
}

export default Brain;
