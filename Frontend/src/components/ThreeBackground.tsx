import { Canvas, useFrame } from '@react-three/fiber';
import { useRef, useMemo } from 'react';
import * as THREE from 'three';

function FloatingParticles() {
    const meshRef = useRef<THREE.Points>(null);
    const count = 500;

    const positions = useMemo(() => {
        const pos = new Float32Array(count * 3);
        for (let i = 0; i < count; i++) {
            pos[i * 3] = (Math.random() - 0.5) * 20;
            pos[i * 3 + 1] = (Math.random() - 0.5) * 20;
            pos[i * 3 + 2] = (Math.random() - 0.5) * 20;
        }
        return pos;
    }, []);

    useFrame((state) => {
        if (meshRef.current) {
            meshRef.current.rotation.y = state.clock.elapsedTime * 0.05;
            meshRef.current.rotation.x = state.clock.elapsedTime * 0.03;
        }
    });

    return (
        <points ref={meshRef}>
            <bufferGeometry>
                <bufferAttribute
                    attach="attributes-position"
                    count={count}
                    array={positions}
                    itemSize={3}
                />
            </bufferGeometry>
            <pointsMaterial
                size={0.05}
                color="#8b5cf6"
                transparent
                opacity={0.6}
                sizeAttenuation
            />
        </points>
    );
}

function GlowingOrb() {
    const meshRef = useRef<THREE.Mesh>(null);

    useFrame((state) => {
        if (meshRef.current) {
            meshRef.current.position.y = Math.sin(state.clock.elapsedTime * 0.5) * 0.3;
            meshRef.current.rotation.y = state.clock.elapsedTime * 0.2;
        }
    });

    return (
        <mesh ref={meshRef} position={[0, 0, -5]}>
            <sphereGeometry args={[2, 32, 32]} />
            <meshStandardMaterial
                color="#7c3aed"
                emissive="#4c1d95"
                emissiveIntensity={0.5}
                transparent
                opacity={0.3}
            />
        </mesh>
    );
}

export function ThreeBackground() {
    return (
        <div className="fixed inset-0 -z-10">
            <Canvas camera={{ position: [0, 0, 5], fov: 75 }}>
                <ambientLight intensity={0.5} />
                <pointLight position={[10, 10, 10]} intensity={1} />
                <FloatingParticles />
                <GlowingOrb />
            </Canvas>
            <div className="absolute inset-0 bg-gradient-to-br from-slate-900/90 via-purple-900/50 to-slate-900/90" />
        </div>
    );
}
