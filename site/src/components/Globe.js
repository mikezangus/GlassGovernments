import React, { useEffect, useRef } from "react"
import * as THREE from "three"
import { GeoJsonGeometry } from 'three-geojson-geometry';
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls"
import * as d3 from "d3-geo"

const Globe = () => {
    const refDiv = useRef(null)

    useEffect(() => {
        const globeScene = new THREE.Scene()
        const light =  new THREE.AmbientLight(0xffffff)
        globeScene.add(light)
        const width = refDiv.current.clientWidth
        const height = refDiv.current.clientHeight

        const renderer = new THREE.WebGLRenderer()
        renderer.setSize(width, height)
        refDiv.current.appendChild(renderer.domElement)

        const camera = new THREE.PerspectiveCamera(60, width / height, 1, 1000)
        camera.position.z = 500

        new OrbitControls(camera, renderer.domElement)

        fetch("/us_states.geojson")
            .then((response) => response.json())
            .then((geojson) => {
                const projection = d3.geoOrthographic().fitSize([width, height], geojson)
                const mesh = new THREE.Mesh(
                    new GeoJsonGeometry(geojson, 10, projection),
                    new THREE.MeshBasicMaterial({ color: 0xffffff, wireframe: true })
                )
                globeScene.add(mesh)
            })
            .catch((error) => console.error("Error loading GeoJSON data:", error))
        const animate = () => {
            requestAnimationFrame(animate)
            renderer.render(globeScene, camera)
        }
        animate()
    }, [])
    return <div ref={refDiv} style={{ width: "100%", height: "100%" }}/>
}

export default Globe