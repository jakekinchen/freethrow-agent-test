"""
Test case for GeometryAgent
"""

import os
import json
from unittest.mock import MagicMock
from geometry_agent import GeometryAgent

class MockLLMService:
    def __init__(self, sample_response=None):
        self.sample_response = sample_response or """
// Create a group for the water molecule
const molecule = new THREE.Group();
window.molecule = molecule;

// Create materials for atoms
const oxygenMaterial = new THREE.MeshPhongMaterial({ color: 0xff0000 });
const hydrogenMaterial = new THREE.MeshPhongMaterial({ color: 0xffffff });
const bondMaterial = new THREE.MeshPhongMaterial({ color: 0xcccccc });

// Create geometries
const oxygenGeometry = new THREE.SphereGeometry(0.8, 32, 32);
const hydrogenGeometry = new THREE.SphereGeometry(0.4, 32, 32);
const bondGeometry = new THREE.CylinderGeometry(0.1, 0.1, 1.2, 8);

// Create atoms
const oxygen = new THREE.Mesh(oxygenGeometry, oxygenMaterial);
oxygen.position.set(0, 0, 0);

const hydrogen1 = new THREE.Mesh(hydrogenGeometry, hydrogenMaterial);
hydrogen1.position.set(-0.8, 0.6, 0);

const hydrogen2 = new THREE.Mesh(hydrogenGeometry, hydrogenMaterial);
hydrogen2.position.set(0.8, 0.6, 0);

// Create bonds
function createBond(start, end) {
    const direction = new THREE.Vector3().subVectors(end, start);
    const length = direction.length();
    
    const bondGeom = new THREE.CylinderGeometry(0.1, 0.1, length, 8);
    const bond = new THREE.Mesh(bondGeom, bondMaterial);
    
    // Position the bond
    bond.position.copy(start);
    bond.position.lerp(end, 0.5);
    
    // Orient the bond
    bond.quaternion.setFromUnitVectors(
        new THREE.Vector3(0, 1, 0),
        direction.clone().normalize()
    );
    
    return bond;
}

const bond1 = createBond(oxygen.position, hydrogen1.position);
const bond2 = createBond(oxygen.position, hydrogen2.position);

// Add everything to the molecule group
molecule.add(oxygen, hydrogen1, hydrogen2, bond1, bond2);

// Add the molecule to the scene
scene.add(molecule);
"""

    def generate(self, prompt):
        # Return the predefined sample response
        return self.sample_response

def test_geometry_agent():
    # Create mock LLM service
    mock_llm = MockLLMService()
    
    # Create the geometry agent
    agent = GeometryAgent(mock_llm)
    
    # Test with a sample prompt
    prompt = "Create a water molecule"
    result = agent.get_geometry_snippet(prompt)
    
    # Print the result
    print("Generated code:")
    print(result)
    
    # Create HTML test file
    html_content = generate_test_html(result)
    
    # Save the HTML to a file
    with open("test_geometry.html", "w") as f:
        f.write(html_content)
    
    print(f"Test HTML file created: {os.path.abspath('test_geometry.html')}")

def generate_test_html(geometry_code):
    """Generate an HTML file with Three.js that includes the geometry code."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Geometry Agent Test</title>
    <style>
        body {{ margin: 0; overflow: hidden; }}
        canvas {{ width: 100%; height: 100%; display: block; }}
    </style>
</head>
<body>
    <!-- Main Three.js library -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <!-- OrbitControls add-on - must be loaded after the main Three.js library -->
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    
    <script>
        // Set up scene, camera and renderer
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x222222);
        
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 5;
        
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);
        
        // Add lights
        const ambientLight = new THREE.AmbientLight(0x404040);
        scene.add(ambientLight);
        
        const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
        directionalLight.position.set(1, 1, 1).normalize();
        scene.add(directionalLight);
        
        // Add geometry from GeometryAgent
        {geometry_code}
        
        // Add orbit controls - using the OrbitControls add-on
        // Make sure orbit controls are created after the Three.js library and controls script are loaded
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.25;
        
        // Animation loop
        function animate() {{
            requestAnimationFrame(animate);
            
            // Rotate the molecule if it exists
            if (window.molecule) {{
                window.molecule.rotation.y += 0.005;
            }}
            
            controls.update();
            renderer.render(scene, camera);
        }}
        
        // Handle window resize
        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});
        
        // Run animation
        animate();
    </script>
</body>
</html>"""

if __name__ == "__main__":
    test_geometry_agent()