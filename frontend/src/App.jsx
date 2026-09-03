function App() {
  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <section className="mx-auto flex min-h-screen max-w-6xl flex-col items-center justify-center px-6 text-center">

        <p className="mb-4 text-sm font-medium uppercase tracking-[0.3em] text-slate-400">
          JobJazz
        </p>

        <h1 className="text-5xl font-bold tracking-tight md:text-7xl">
          Your career,
          <span className="block text-slate-300">
            in tune.
          </span>
        </h1>

        <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-400">
          Understand your job fit, discover skill gaps, and tune your
          career profile for the opportunities that matter.
        </p>

        <div className="mt-10 flex flex-col gap-4 sm:flex-row">

          <button className="rounded-xl bg-white px-6 py-3 font-semibold text-slate-950 transition hover:bg-slate-200">
            Analyze My Resume
          </button>

          <button className="rounded-xl border border-slate-700 px-6 py-3 font-semibold text-white transition hover:bg-slate-900">
            Explore Job Market
          </button>

        </div>

      </section>
    </main>
  )
}

export default App