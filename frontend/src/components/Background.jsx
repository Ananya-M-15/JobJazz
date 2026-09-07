import React, { useMemo } from "react"

function Background() {
    // Generate fine stardust particle specs for the AI Powered orb
    const stardustParticles = useMemo(() => {
        return [
            { x: 28, y: 30, size: 1.8, opacity: 0.8, delay: 0 },
            { x: 38, y: 18, size: 1.2, opacity: 0.6, delay: 1.2 },
            { x: 55, y: 26, size: 2.0, opacity: 0.9, delay: 0.5 },
            { x: 68, y: 20, size: 1.0, opacity: 0.5, delay: 2.1 },
            { x: 78, y: 32, size: 1.5, opacity: 0.75, delay: 1.7 },
            { x: 22, y: 42, size: 1.2, opacity: 0.65, delay: 0.8 },
            { x: 34, y: 48, size: 1.8, opacity: 0.85, delay: 2.4 },
            { x: 48, y: 38, size: 1.0, opacity: 0.5, delay: 1.1 },
            { x: 64, y: 44, size: 1.6, opacity: 0.8, delay: 0.3 },
            { x: 76, y: 48, size: 1.2, opacity: 0.6, delay: 1.9 },
            { x: 26, y: 56, size: 1.5, opacity: 0.8, delay: 2.7 },
            { x: 44, y: 58, size: 2.0, opacity: 0.95, delay: 0.9 },
            { x: 58, y: 52, size: 1.3, opacity: 0.7, delay: 1.4 },
            { x: 70, y: 56, size: 1.8, opacity: 0.85, delay: 2.0 },
            { x: 82, y: 54, size: 1.4, opacity: 0.7, delay: 0.4 },
            { x: 30, y: 64, size: 2.2, opacity: 0.95, delay: 1.6 },
            { x: 50, y: 66, size: 2.5, opacity: 1.0, delay: 0.2 },
            { x: 66, y: 65, size: 2.0, opacity: 0.9, delay: 2.3 },
            { x: 18, y: 34, size: 1.0, opacity: 0.45, delay: 1.8 },
            { x: 84, y: 38, size: 1.2, opacity: 0.6, delay: 0.7 },
        ]
    }, [])

    return (
        <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none" aria-hidden="true">
            {/* Base Obsidian Void */}
            <div className="absolute inset-0 bg-[#08060f]" />

            {/* Diamond / Isometric Mesh Grid in Top-Left */}
            <div className="jj-diamond-grid" />

            {/* Subtle atmospheric glow in top-left */}
            <div className="jj-radiation-top-left" />

            {/* =======================================================
          CONCENTRIC 3D RINGS & AI POWERED ORB
          Epicenter positioned with clearance from bottom and right
          ======================================================= */}
            <div
                className="absolute"
                style={{
                    right: "clamp(120px, 13vw, 220px)",
                    bottom: "clamp(130px, 18vh, 220px)",
                    width: 0,
                    height: 0,
                }}
            >
                {/* Atmospheric purple radiation glow behind the rings */}
                <div
                    className="absolute pointer-events-none -translate-x-1/2 -translate-y-1/2"
                    style={{
                        width: "1400px",
                        height: "1400px",
                        borderRadius: "50%",
                        background:
                            "radial-gradient(circle, rgba(139, 92, 246, 0.4) 0%, rgba(109, 40, 217, 0.26) 30%, rgba(67, 24, 150, 0.12) 55%, transparent 75%)",
                        filter: "blur(80px)",
                    }}
                />

                {/* SVG Concentric 3D Rings */}
                <svg
                    className="absolute pointer-events-none -translate-x-1/2 -translate-y-1/2"
                    style={{
                        width: "1900px",
                        height: "1900px",
                        overflow: "visible",
                    }}
                    viewBox="0 0 1900 1900"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <defs>
                        {/* Ring Shading Gradients (Light from top-left, deep shadow at bottom-right) */}
                        <linearGradient id="ringGrad1" x1="450" y1="450" x2="1450" y2="1450" gradientUnits="userSpaceOnUse">
                            <stop offset="0%" stopColor="#673ebf" />
                            <stop offset="30%" stopColor="#4e289c" />
                            <stop offset="65%" stopColor="#240f52" />
                            <stop offset="100%" stopColor="#0f0624" />
                        </linearGradient>

                        <linearGradient id="ringGrad2" x1="380" y1="380" x2="1520" y2="1520" gradientUnits="userSpaceOnUse">
                            <stop offset="0%" stopColor="#6037b5" />
                            <stop offset="32%" stopColor="#45228c" />
                            <stop offset="68%" stopColor="#200d47" />
                            <stop offset="100%" stopColor="#0c051d" />
                        </linearGradient>

                        <linearGradient id="ringGrad3" x1="300" y1="300" x2="1600" y2="1600" gradientUnits="userSpaceOnUse">
                            <stop offset="0%" stopColor="#572fad" />
                            <stop offset="35%" stopColor="#3d1d80" />
                            <stop offset="70%" stopColor="#1c0a3e" />
                            <stop offset="100%" stopColor="#090417" />
                        </linearGradient>

                        <linearGradient id="ringGrad4" x1="200" y1="200" x2="1700" y2="1700" gradientUnits="userSpaceOnUse">
                            <stop offset="0%" stopColor="#4c269a" />
                            <stop offset="35%" stopColor="#341672" />
                            <stop offset="72%" stopColor="#160733" />
                            <stop offset="100%" stopColor="#070211" />
                        </linearGradient>

                        <linearGradient id="ringGrad5" x1="100" y1="100" x2="1800" y2="1800" gradientUnits="userSpaceOnUse">
                            <stop offset="0%" stopColor="#411d88" stopOpacity="0.8" />
                            <stop offset="40%" stopColor="#280f5a" stopOpacity="0.55" />
                            <stop offset="75%" stopColor="#120429" stopOpacity="0.28" />
                            <stop offset="100%" stopColor="#05010c" stopOpacity="0" />
                        </linearGradient>

                        {/* Specular Bevel Rim Highlight along upper-left curve */}
                        <linearGradient id="rimHighlight" x1="450" y1="450" x2="1450" y2="1450" gradientUnits="userSpaceOnUse">
                            <stop offset="0%" stopColor="#ebd5ff" stopOpacity="0.75" />
                            <stop offset="22%" stopColor="#c084fc" stopOpacity="0.55" />
                            <stop offset="50%" stopColor="#8b5cf6" stopOpacity="0.25" />
                            <stop offset="80%" stopColor="#4c1d95" stopOpacity="0.05" />
                            <stop offset="100%" stopColor="transparent" />
                        </linearGradient>

                        {/* Step Shadow filter for 3D stadium relief */}
                        <filter id="ringShadow" x="-20%" y="-20%" width="150%" height="150%">
                            <feDropShadow dx="-8" dy="-8" stdDeviation="15" floodColor="#000000" floodOpacity="0.92" />
                        </filter>
                    </defs>

                    {/* Ring 5: Outermost ambient ripple */}
                    <circle
                        cx="950"
                        cy="950"
                        r="800"
                        stroke="url(#ringGrad5)"
                        strokeWidth="180"
                    />
                    <circle
                        cx="950"
                        cy="950"
                        r="891"
                        stroke="url(#rimHighlight)"
                        strokeWidth="1.6"
                        opacity="0.35"
                    />

                    {/* Ring 4: Large Outer Stadium Band */}
                    <circle
                        cx="950"
                        cy="950"
                        r="580"
                        stroke="url(#ringGrad4)"
                        strokeWidth="140"
                        filter="url(#ringShadow)"
                    />
                    {/* Ring 4 outer specular bevel */}
                    <circle
                        cx="950"
                        cy="950"
                        r="651"
                        stroke="url(#rimHighlight)"
                        strokeWidth="1.9"
                        opacity="0.65"
                    />
                    {/* Ring 4 inner trench groove */}
                    <circle
                        cx="950"
                        cy="950"
                        r="509"
                        stroke="#06020e"
                        strokeWidth="2.5"
                    />

                    {/* Ring 3: Mid Outer Band */}
                    <circle
                        cx="950"
                        cy="950"
                        r="405"
                        stroke="url(#ringGrad3)"
                        strokeWidth="110"
                        filter="url(#ringShadow)"
                    />
                    {/* Ring 3 outer specular bevel */}
                    <circle
                        cx="950"
                        cy="950"
                        r="461"
                        stroke="url(#rimHighlight)"
                        strokeWidth="2.1"
                        opacity="0.75"
                    />
                    {/* Ring 3 inner trench groove */}
                    <circle
                        cx="950"
                        cy="950"
                        r="349"
                        stroke="#06020e"
                        strokeWidth="2.5"
                    />

                    {/* Ring 2: Mid Inner Band */}
                    <circle
                        cx="950"
                        cy="950"
                        r="270"
                        stroke="url(#ringGrad2)"
                        strokeWidth="80"
                        filter="url(#ringShadow)"
                    />
                    {/* Ring 2 outer specular bevel */}
                    <circle
                        cx="950"
                        cy="950"
                        r="311"
                        stroke="url(#rimHighlight)"
                        strokeWidth="2.3"
                        opacity="0.85"
                    />
                    {/* Ring 2 inner trench groove */}
                    <circle
                        cx="950"
                        cy="950"
                        r="229"
                        stroke="#06020e"
                        strokeWidth="2.5"
                    />

                    {/* Ring 1: Innermost Band (framing the central orb) */}
                    <circle
                        cx="950"
                        cy="950"
                        r="170"
                        stroke="url(#ringGrad1)"
                        strokeWidth="60"
                        filter="url(#ringShadow)"
                    />
                    {/* Ring 1 outer specular bevel */}
                    <circle
                        cx="950"
                        cy="950"
                        r="201"
                        stroke="url(#rimHighlight)"
                        strokeWidth="2.5"
                        opacity="0.95"
                    />
                    {/* Ring 1 inner shadow socket for the orb */}
                    <circle
                        cx="950"
                        cy="950"
                        r="139"
                        stroke="#05020c"
                        strokeWidth="3.5"
                    />
                </svg>

                {/* =======================================================
            GLOWING "AI POWERED" COSMIC ORB
            Locked right at the epicenter
            ======================================================= */}
                <div
                    className="absolute pointer-events-auto -translate-x-1/2 -translate-y-1/2 cursor-pointer"
                    style={{
                        width: "240px",
                        height: "240px",
                    }}
                >
                    <div className="jj-orb-container w-full h-full">
                        {/* Stardust particles inside orb */}
                        {stardustParticles.map((pt, idx) => (
                            <span
                                key={idx}
                                className="jj-stardust animate-twinkle"
                                style={{
                                    left: `${pt.x}%`,
                                    top: `${pt.y}%`,
                                    width: `${pt.size}px`,
                                    height: `${pt.size}px`,
                                    opacity: pt.opacity,
                                    animationDelay: `${pt.delay}s`,
                                }}
                            />
                        ))}

                        {/* Radiant Aurora at the bottom inside orb */}
                        <div className="jj-orb-aurora">
                            {/* Left hot magenta/pink flare */}
                            <div className="jj-aurora-glow-left" />

                            {/* Right electric cyan/sky flare */}
                            <div className="jj-aurora-glow-right" />

                            {/* Center bright white merge flare */}
                            <div className="jj-aurora-glow-center" />

                            {/* Horizon bright glowing line */}
                            <div className="jj-orb-horizon-line" />
                        </div>

                        {/* Glass rim specular highlight */}
                        <div className="jj-orb-rim-highlight" />

                        {/* "AI Powered" Centered Text */}
                        <div className="absolute inset-0 flex items-center justify-center pointer-events-none pb-7">
                            <span className="text-white text-[15px] font-medium tracking-[0.03em] drop-shadow-[0_2px_8px_rgba(0,0,0,0.85)] select-none">
                                AI Powered
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Background