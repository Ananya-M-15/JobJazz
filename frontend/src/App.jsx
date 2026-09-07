import React from "react"
import Background from "./components/Background"
import Navbar from "./components/Navbar"

function App() {
  return (
    <main className="relative min-h-screen overflow-hidden text-white select-none">
      {/* Untouched Navbar */}
      <Navbar />

      {/* Background with Diamond Grid, Color Radiations, 3D Rings & Glowing Orb */}
      <Background />

      {/* Hero Section */}
      <section className="relative z-10 mx-auto flex min-h-screen max-w-7xl flex-col justify-center px-6 sm:px-12 lg:px-16 pt-28 pb-20">
        <div className="max-w-2xl lg:max-w-3xl">

          {/* Heading */}
          <h1 className="jj-display text-[2.75rem] sm:text-[4rem] lg:text-[4.5rem] font-bold tracking-[-0.038em] text-white leading-[1.08]">
            Scale Your Productivity
            <br />
            Beyond Boundaries
          </h1>

          {/* Description */}
          <p className="mt-6 max-w-xl text-base sm:text-[1.0625rem] leading-[1.68] text-[#938ea9]">
            Launch faster with everything you need out of the box.
            PostgreSQL database, auth, file storage, serverless functions, real-time
            updates, vector support — all open source and built for scale.
          </p>

          {/* Partner / Integration Logos */}
          <div className="mt-10 flex flex-wrap items-center gap-x-6 sm:gap-x-7 gap-y-3">
            {/* Loom */}
            <div className="jj-partner-badge">
              <svg className="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="currentColor">
                <circle cx="12" cy="12" r="3.2" />
                <path
                  d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.28 5.28l2.12 2.12M16.6 16.6l2.12 2.12M5.28 18.72l2.12-2.12M16.6 7.4l2.12-2.12"
                  stroke="currentColor"
                  strokeWidth="2.4"
                  strokeLinecap="round"
                />
              </svg>
              <span>Loom</span>
            </div>

            {/* Calendly */}
            <div className="jj-partner-badge">
              <svg
                className="w-4 h-4 shrink-0"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.3"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <circle cx="12" cy="12" r="9.5" />
                <path d="M15 8.8a4.5 4.5 0 1 0 0 6.4" />
              </svg>
              <span>Calendly</span>
            </div>

            {/* Zapier */}
            <div className="jj-partner-badge">
              <svg className="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2a1 1 0 0 1 1 1v7.5l5.3-5.3a1 1 0 0 1 1.4 1.4L14.4 12l5.3 5.3a1 1 0 0 1-1.4 1.4L13 13.4V21a1 1 0 1 1-2 0v-7.6l-5.3 5.3a1 1 0 0 1-1.4-1.4L9.6 12 4.3 6.7a1 1 0 0 1 1.4-1.4L11 10.5V3a1 1 0 0 1 1-1z" />
              </svg>
              <span>Zapier</span>
            </div>

            {/* OpenAI */}
            <div className="jj-partner-badge">
              <svg
                className="w-4 h-4 shrink-0"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.9"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M19.5 10c.3.6.5 1.3.5 2 0 2.8-2.2 5-5 5h-1v2a3 3 0 0 1-3 3c-.8 0-1.5-.3-2.1-.8M4.5 14c-.3-.6-.5-1.3-.5-2 0-2.8 2.2-5 5-5h1V5a3 3 0 0 1 3-3c.8 0 1.5.3 2.1.8" />
                <circle cx="12" cy="12" r="3" />
              </svg>
              <span>Open AI</span>
            </div>

            {/* Notion */}
            <div className="jj-partner-badge">
              <svg className="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="currentColor">
                <path d="M4 4.5A2.5 2.5 0 0 1 6.5 2h11A2.5 2.5 0 0 1 20 4.5v15a2.5 2.5 0 0 1-2.5 2.5h-11A2.5 2.5 0 0 1 4 19.5v-15zM7.5 7v10h2.2l4.8-7v7h2V7h-2.2L9.5 14V7h-2z" />
              </svg>
              <span>Notion</span>
            </div>

            {/* Figma */}
            <div className="jj-partner-badge">
              <svg className="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="currentColor">
                <path d="M8 2h4v5H8a2.5 2.5 0 1 1 0-5zm4 0h4a2.5 2.5 0 0 1 0 5h-4V2zm0 5h4a2.5 2.5 0 0 1 0 5h-4V7zm-4 0h4v5H8a2.5 2.5 0 0 1 0-5zm0 5h4v4.5A2.5 2.5 0 0 1 8 19a2.5 2.5 0 0 1 0-5z" />
              </svg>
              <span>Figma</span>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="mt-11 flex items-center gap-5">
            <button className="jj-btn-primary">
              Get Started
            </button>

            <button className="jj-btn-secondary">
              Request a demo
            </button>
          </div>

        </div>
      </section>
    </main>
  )
}

export default App