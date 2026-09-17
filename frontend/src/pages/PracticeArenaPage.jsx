import React, { useState, useEffect } from 'react';
import {
  Brain, Clock, Shuffle, Target, Briefcase, Zap, Filter, ArrowRight, Loader2
} from 'lucide-react';
import api from '../services/api';
import InteractiveTask from '../components/Learning/InteractiveTask';

export default function PracticeArenaPage() {
  const [mode, setMode] = useState('quick'); // quick, timed, weak, random, interview
  const [selectedSubject, setSelectedSubject] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState('');
  const [subjects, setSubjects] = useState([]);
  const [questions, setQuestions] = useState([]);
  const [currentQIndex, setCurrentQIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const [started, setStarted] = useState(false);

  useEffect(() => {
    api.get('/subjects').then((res) => setSubjects(res.data)).catch(console.error);
  }, []);

  const startPractice = async (selectedMode = mode) => {
    setLoading(true);
    setStarted(false);
    setCurrentQIndex(0);

    try {
      let params = {};
      if (selectedSubject) params.subject_id = selectedSubject;
      if (selectedDifficulty) params.difficulty = selectedDifficulty;

      if (selectedMode === 'quick') {
        params.limit = 10;
      } else if (selectedMode === 'timed') {
        params.limit = 20;
      } else if (selectedMode === 'weak') {
        params.only_incorrect = true;
        params.limit = 10;
      } else {
        params.limit = 15;
      }

      const res = await api.get('/questions', { params });
      let qList = res.data;

      // Fallback if weak topics filter returned empty
      if (selectedMode === 'weak' && qList.length === 0) {
        const fallbackRes = await api.get('/questions', { params: { limit: 10 } });
        qList = fallbackRes.data;
      }

      setQuestions(qList);
      setStarted(true);
    } catch (err) {
      console.error('Error starting practice arena:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleNextQuestion = () => {
    if (currentQIndex < questions.length - 1) {
      setCurrentQIndex((prev) => prev + 1);
    } else {
      setStarted(false);
    }
  };

  const modesList = [
    { id: 'quick', title: 'Quick Practice', desc: '10 Curated Questions', icon: Zap, color: 'text-cyan-400' },
    { id: 'timed', title: 'Timed Practice', desc: '20 Questions against time', icon: Clock, color: 'text-amber-400' },
    { id: 'weak', title: 'Weak Concepts', desc: 'AI-targeted practice', icon: Target, color: 'text-rose-400' },
    { id: 'random', title: 'Random Mix', desc: 'Cross-subject engineering blend', icon: Shuffle, color: 'text-purple-400' },
  ];

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 text-xs font-bold text-purple-400 uppercase tracking-wider mb-1">
          <Brain className="w-4 h-4" />
          <span>Interactive Arena</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          Practice Arena
        </h1>
        <p className="text-xs sm:text-sm text-purple-300/70 mt-1">
          Sharpen your conceptual memory and diagnostic accuracy with customized practice modes.
        </p>
      </div>

      {!started ? (
        <div className="space-y-6">
          {/* Mode Selector */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {modesList.map((m) => {
              const Icon = m.icon;
              const isSelected = mode === m.id;
              return (
                <button
                  key={m.id}
                  type="button"
                  onClick={() => setMode(m.id)}
                  className={`card-orbit p-5 text-left transition-all border flex flex-col justify-between ${
                    isSelected
                      ? 'border-cyan-400 bg-purple-600/20 ring-1 ring-cyan-400 shadow-xl'
                      : 'border-purple-500/20 hover:border-purple-500/40'
                  }`}
                >
                  <div className="flex items-center justify-between mb-4">
                    <Icon className={`w-6 h-6 ${m.color}`} />
                    {isSelected && <span className="w-2 h-2 rounded-full bg-cyan-400" />}
                  </div>
                  <div>
                    <h3 className="text-base font-bold text-white mb-1">{m.title}</h3>
                    <p className="text-xs text-purple-300/60">{m.desc}</p>
                  </div>
                </button>
              );
            })}
          </div>

          {/* Filters & Customization */}
          <div className="card-orbit p-6 border-purple-500/20 space-y-4">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Filter className="w-4 h-4 text-cyan-400" />
              Configure Filter Parameters (Optional)
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  Specific Subject
                </label>
                <select
                  value={selectedSubject}
                  onChange={(e) => setSelectedSubject(e.target.value)}
                  className="w-full p-2.5 rounded-xl bg-purple-950/40 border border-purple-500/20 text-slate-200 text-xs focus:outline-none focus:border-cyan-400"
                >
                  <option value="">All 6 Engineering Subjects</option>
                  {subjects.map((s) => (
                    <option key={s.id} value={s.id}>
                      {s.icon} {s.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  Difficulty Level
                </label>
                <select
                  value={selectedDifficulty}
                  onChange={(e) => setSelectedDifficulty(e.target.value)}
                  className="w-full p-2.5 rounded-xl bg-purple-950/40 border border-purple-500/20 text-slate-200 text-xs focus:outline-none focus:border-cyan-400"
                >
                  <option value="">Any Difficulty (Mixed)</option>
                  <option value="EASY">Easy</option>
                  <option value="MEDIUM">Medium</option>
                  <option value="HARD">Hard</option>
                </select>
              </div>
            </div>

            <div className="pt-2 flex justify-end">
              <button
                type="button"
                disabled={loading}
                onClick={() => startPractice(mode)}
                className="px-8 py-3 rounded-xl font-bold text-sm bg-gradient-to-r from-purple-600 via-indigo-600 to-cyan-500 text-white shadow-lg shadow-purple-600/30 hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center gap-2"
              >
                {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Zap className="w-4 h-4" />}
                <span>Launch Practice Session</span>
              </button>
            </div>
          </div>
        </div>
      ) : (
        /* Active Practice Session */
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <button
              onClick={() => setStarted(false)}
              className="text-xs font-semibold text-slate-400 hover:text-white transition-colors"
            >
              ← End Practice Session
            </button>
            <div className="text-xs font-bold text-cyan-400">
              Question {currentQIndex + 1} of {questions.length}
            </div>
          </div>

          {questions.length > 0 ? (
            <InteractiveTask
              question={questions[currentQIndex]}
              topicId={questions[currentQIndex]?.topic_id}
              onCompleteNext={handleNextQuestion}
            />
          ) : (
            <div className="card-orbit p-8 text-center">
              <p className="text-sm text-slate-400">No questions found matching criteria.</p>
              <button
                onClick={() => setStarted(false)}
                className="mt-4 px-4 py-2 rounded-xl text-xs font-bold bg-purple-600 text-white"
              >
                Back to Selector
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
