import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  Rocket, Sparkles, Brain, Award, Zap, Flame, Shield, ArrowRight,
  CheckCircle2, Terminal, Code, Cpu
} from 'lucide-react';

export default function LandingPage() {
  const subjects = [
    { name: 'DBMS', icon: '🗄️', desc: 'Relational model, indexing, normalization, and ACID.', color: 'from-cyan-500/20 to-blue-500/10' },
    { name: 'OOPS', icon: '🧩', desc: 'Object-oriented paradigms, dynamic dispatch, and SOLID.', color: 'from-purple-500/20 to-pink-500/10' },
    { name: 'OS', icon: '⚙️', desc: 'Concurrency, deadlocks, virtual memory, and kernel internals.', color: 'from-pink-500/20 to-rose-500/10' },
    { name: 'DS', icon: '🌳', desc: 'Asymptotic analysis, trees, graphs, heaps, and DP.', color: 'from-emerald-500/20 to-teal-500/10' },
    { name: 'ML', icon: '🧠', desc: 'Supervised learning, classification, clustering, and metrics.', color: 'from-amber-500/20 to-orange-500/10' },
    { name: 'CN', icon: '🌐', desc: 'OSI 7 layers, TCP/IP flow control, subnetting, and routing.', color: 'from-blue-500/20 to-indigo-500/10' },
  ];

  return (
    <div className="min-h-screen bg-[#080414] text-slate-100 flex flex-col relative overflow-hidden">
      {/* Ambient background glows */}
      <div className="fixed top-0 left-1/4 w-[600px] h-[600px] rounded-full bg-purple-900/15 blur-[140px] pointer-events-none" />
      <div className="fixed top-1/3 right-10 w-[500px] h-[500px] rounded-full bg-cyan-900/15 blur-[150px] pointer-events-none" />

      {/* Top Navigation */}
      <header className="h-20 border-b border-purple-500/15 flex items-center justify-between px-6 lg:px-12 backdrop-blur-md relative z-10">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-purple-600 via-indigo-500 to-cyan-400 p-[1.5px] shadow-lg shadow-purple-600/30">
            <div className="w-full h-full bg-[#0d081f] rounded-[10px] flex items-center justify-center">
              <span className="text-xl">🪐</span>
            </div>
          </div>
          <span className="text-xl font-extrabold tracking-tight bg-gradient-to-r from-white via-purple-100 to-cyan-300 bg-clip-text text-transparent">
            CodeOrbit
          </span>
        </div>

        <div className="flex items-center gap-3">
          <NavLink
            to="/login"
            className="px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold text-slate-300 hover:text-white transition-colors"
          >
            Sign In
          </NavLink>
          <NavLink
            to="/register"
            className="px-5 py-2.5 rounded-xl text-xs sm:text-sm font-bold bg-gradient-to-r from-purple-600 to-cyan-500 text-white shadow-lg shadow-purple-600/30 hover:scale-[1.02] active:scale-[0.98] transition-all"
          >
            Get Started Free
          </NavLink>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative z-10 max-w-5xl mx-auto px-6 pt-16 pb-20 text-center">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-purple-950/60 border border-purple-500/30 text-purple-300 text-xs font-semibold mb-8 shadow-inner">
          <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
          <span>AI-Powered Gamified Computer Science Education</span>
        </div>

        <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.1] mb-6 text-white">
          Learn Engineering.{' '}
          <span className="bg-gradient-to-r from-purple-400 via-pink-400 to-cyan-400 bg-clip-text text-transparent">
            Build Skills.
          </span>{' '}
          Level Up.
        </h1>

        <p className="max-w-2xl mx-auto text-base sm:text-lg text-slate-300/80 leading-relaxed mb-10">
          CodeOrbit combines bite-sized progressive learning paths, AI tutoring, smart spaced repetition,
          and career placement preparation designed specifically for engineering students.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <NavLink
            to="/register"
            className="w-full sm:w-auto px-8 py-4 rounded-2xl text-base font-bold bg-gradient-to-r from-purple-600 via-indigo-600 to-cyan-500 text-white shadow-xl shadow-purple-600/30 hover:shadow-purple-500/50 hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center gap-2"
          >
            <Rocket className="w-5 h-5 text-cyan-300" />
            <span>Start Learning Free</span>
          </NavLink>
          <NavLink
            to="/login"
            className="w-full sm:w-auto px-8 py-4 rounded-2xl text-base font-bold bg-purple-950/40 border border-purple-500/30 text-purple-200 hover:bg-purple-900/40 hover:text-white transition-all flex items-center justify-center gap-2"
          >
            <span>Explore Demo Account</span>
            <ArrowRight className="w-4 h-4 text-purple-400" />
          </NavLink>
        </div>

        {/* Floating Stat Badges */}
        <div className="mt-14 grid grid-cols-2 md:grid-cols-4 gap-4 max-w-3xl mx-auto">
          <div className="p-4 rounded-2xl bg-purple-950/30 border border-purple-500/20">
            <div className="text-2xl font-extrabold text-white">6</div>
            <div className="text-xs text-purple-300/70 font-medium">Core CS Subjects</div>
          </div>
          <div className="p-4 rounded-2xl bg-purple-950/30 border border-purple-500/20">
            <div className="text-2xl font-extrabold text-cyan-400">75+</div>
            <div className="text-xs text-purple-300/70 font-medium">Progressive Topics</div>
          </div>
          <div className="p-4 rounded-2xl bg-purple-950/30 border border-purple-500/20">
            <div className="text-2xl font-extrabold text-amber-400">14</div>
            <div className="text-xs text-purple-300/70 font-medium">Interactive Formats</div>
          </div>
          <div className="p-4 rounded-2xl bg-purple-950/30 border border-purple-500/20">
            <div className="text-2xl font-extrabold text-emerald-400">100%</div>
            <div className="text-xs text-purple-300/70 font-medium">Zero Paid APIs Needed</div>
          </div>
        </div>
      </section>

      {/* Curriculum Showcase */}
      <section className="relative z-10 max-w-6xl mx-auto px-6 py-16 border-t border-purple-500/15">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-extrabold text-white mb-3">
            Engineered For University & Placement Success
          </h2>
          <p className="text-sm text-slate-400 max-w-xl mx-auto">
            Structured step-by-step paths from foundational fundamentals to interview-grade boss challenges.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {subjects.map((s) => (
            <div
              key={s.name}
              className="p-6 rounded-2xl bg-gradient-to-br from-[#130b2e] to-[#0d0720] border border-purple-500/20 hover:border-purple-500/40 transition-all hover:-translate-y-1"
            >
              <div className="text-4xl mb-4">{s.icon}</div>
              <h3 className="text-xl font-bold text-white mb-2">{s.name}</h3>
              <p className="text-xs text-slate-300/80 leading-relaxed">{s.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How It Works Section */}
      <section className="relative z-10 max-w-5xl mx-auto px-6 py-16 border-t border-purple-500/15">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-extrabold text-white mb-3">The Learning Loop</h2>
          <p className="text-sm text-slate-400">Continuous mastery powered by adaptive deterministic feedback.</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-5 gap-4 text-center">
          {[
            { step: '1', title: 'Choose Path', desc: 'Select any of the 6 engineering subjects' },
            { step: '2', title: 'Learn Topic', desc: 'Bite-sized cards with real-world examples' },
            { step: '3', title: 'Interactive Tasks', desc: 'Solve code, SQL, and concept puzzles' },
            { step: '4', title: 'AI Analytics', desc: 'Weaknesses identified & explained' },
            { step: '5', title: 'Level Up', desc: 'Gain XP, badges, and placement readiness' },
          ].map((item) => (
            <div key={item.step} className="p-4 rounded-xl bg-purple-950/20 border border-purple-500/20">
              <div className="w-8 h-8 rounded-full bg-cyan-500/20 text-cyan-300 font-bold text-sm mx-auto flex items-center justify-center mb-3">
                {item.step}
              </div>
              <div className="font-bold text-sm text-white mb-1">{item.title}</div>
              <div className="text-[11px] text-slate-400">{item.desc}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-auto border-t border-purple-500/15 py-8 px-6 text-center text-xs text-slate-500">
        © 2026 CodeOrbit. AI Personalized Learning Platform for Engineering Students.
      </footer>
    </div>
  );
}
