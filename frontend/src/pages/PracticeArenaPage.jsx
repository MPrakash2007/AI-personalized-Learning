import React, { useState, useEffect } from 'react';
import { useSearchParams, NavLink, useNavigate } from 'react-router-dom';
import confetti from 'canvas-confetti';
import {
  Brain, Clock, Shuffle, Target, Briefcase, Zap, Filter, ArrowRight,
  Loader2, AlertCircle, BookOpen, CheckCircle2, RotateCcw, Trophy,
  ChevronRight, Award, Sparkles
} from 'lucide-react';
import api from '../services/api';
import InteractiveTask from '../components/Learning/InteractiveTask';

export default function PracticeArenaPage() {
  const [searchParams] = useSearchParams();
  const initialSubject = searchParams.get('subject') || '';

  const [mode, setMode] = useState('quick'); // quick, timed, weak, random
  const [selectedSubject, setSelectedSubject] = useState(initialSubject);
  const [selectedDifficulty, setSelectedDifficulty] = useState('');
  const [subjects, setSubjects] = useState([]);
  const [questions, setQuestions] = useState([]);
  const [currentQIndex, setCurrentQIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const [started, setStarted] = useState(false);
  const [cantPracticeInfo, setCantPracticeInfo] = useState(null);
  const [sessionCompleted, setSessionCompleted] = useState(false);
  const [sessionStats, setSessionStats] = useState({ correct: 0, totalAnswered: 0, xpEarned: 0 });

  const navigate = useNavigate();

  useEffect(() => {
    api.get('/subjects').then((res) => {
      setSubjects(res.data);
      // If initialSubject param is slug, check if matched
      if (initialSubject) {
        const found = res.data.find(s => s.slug === initialSubject || String(s.id) === initialSubject);
        if (found) {
          setSelectedSubject(String(found.id));
        }
      }
    }).catch(console.error);
  }, [initialSubject]);

  const startPractice = async (selectedMode = mode) => {
    setLoading(true);
    setStarted(false);
    setCantPracticeInfo(null);
    setSessionCompleted(false);
    setCurrentQIndex(0);
    setSessionStats({ correct: 0, totalAnswered: 0, xpEarned: 0 });

    try {
      const params = { mode: selectedMode };
      if (selectedSubject) params.subject_id = selectedSubject;
      if (selectedDifficulty) params.difficulty = selectedDifficulty;

      if (selectedMode === 'quick') params.limit = 10;
      else if (selectedMode === 'timed') params.limit = 20;
      else if (selectedMode === 'weak') params.limit = 10;
      else params.limit = 15;

      const res = await api.get('/practice/questions', { params });
      const data = res.data;

      if (!data.can_practice) {
        setCantPracticeInfo({
          message: data.message,
          subject_name: data.subject_name,
          subject_id: selectedSubject
        });
        setLoading(false);
        return;
      }

      setQuestions(data.questions || []);
      setStarted(true);
    } catch (err) {
      console.error('Error starting practice arena:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleNextQuestion = (isCorrect, xp) => {
    const newCorrect = sessionStats.correct + (isCorrect ? 1 : 0);
    const newAnswered = sessionStats.totalAnswered + 1;
    const newXp = sessionStats.xpEarned + (xp || (isCorrect ? 10 : 0));

    setSessionStats({
      correct: newCorrect,
      totalAnswered: newAnswered,
      xpEarned: newXp
    });

    if (currentQIndex < questions.length - 1) {
      setCurrentQIndex((prev) => prev + 1);
    } else {
      // Session finished!
      confetti({
        particleCount: 80,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#8b5cf6', '#06b6d4', '#10b981', '#f59e0b'],
      });
      setSessionCompleted(true);
      setStarted(false);
    }
  };

  const modesList = [
    { id: 'quick', title: 'Quick Practice', desc: '10 Curated Questions', icon: Zap, color: 'text-cyan-400' },
    { id: 'timed', title: 'Timed Practice', desc: '20 Questions Challenge', icon: Clock, color: 'text-amber-400' },
    { id: 'weak', title: 'Weak Concepts', desc: 'Targeted Review Drill', icon: Target, color: 'text-rose-400' },
    { id: 'random', title: 'Random Mix', desc: 'Cross-Topic Drill', icon: Shuffle, color: 'text-purple-400' },
  ];

  // Selected subject object
  const currentSubjObj = subjects.find(s => String(s.id) === String(selectedSubject));

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 text-xs font-bold text-purple-400 uppercase tracking-wider mb-1">
          <Brain className="w-4 h-4 text-cyan-400" />
          <span>Interactive Practice Arena</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight">
          Practice Arena
        </h1>
        <p className="text-xs sm:text-sm text-purple-300/70 mt-1 max-w-2xl">
          Drill separate practice questions exclusively from your completed curriculum topics to lock in long-term mastery.
        </p>
      </div>

      {/* Empty State Banner when user has not completed prerequisite topics */}
      {cantPracticeInfo && (
        <div className="p-6 rounded-3xl bg-gradient-to-r from-purple-950/60 via-[#180e38] to-indigo-950/60 border border-purple-500/30 shadow-2xl space-y-4 animate-in fade-in duration-300">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 rounded-2xl bg-amber-500/20 border border-amber-400/40 flex items-center justify-center shrink-0 text-amber-300">
              <BookOpen className="w-6 h-6" />
            </div>
            <div className="space-y-1">
              <h3 className="text-base sm:text-lg font-bold text-white">
                Prerequisite Lesson Required
              </h3>
              <p className="text-xs sm:text-sm text-purple-200/80 leading-relaxed">
                {cantPracticeInfo.message}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3 pt-2">
            {currentSubjObj ? (
              <NavLink
                to={`/learn/${currentSubjObj.slug}`}
                className="px-6 py-2.5 rounded-xl text-xs font-bold bg-gradient-to-r from-purple-600 to-cyan-500 text-white shadow-lg shadow-purple-600/30 hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center gap-2"
              >
                <span>Go to {currentSubjObj.name} Curriculum</span>
                <ArrowRight className="w-4 h-4" />
              </NavLink>
            ) : (
              <NavLink
                to="/learn"
                className="px-6 py-2.5 rounded-xl text-xs font-bold bg-gradient-to-r from-purple-600 to-cyan-500 text-white shadow-lg shadow-purple-600/30 hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center gap-2"
              >
                <span>Browse All Curriculums</span>
                <ArrowRight className="w-4 h-4" />
              </NavLink>
            )}
            <button
              type="button"
              onClick={() => {
                setSelectedSubject('');
                setCantPracticeInfo(null);
              }}
              className="px-4 py-2.5 rounded-xl text-xs font-semibold text-slate-400 hover:text-white transition-colors"
            >
              Clear Filter
            </button>
          </div>
        </div>
      )}

      {/* Session Completed Summary Card */}
      {sessionCompleted && (
        <div className="card-orbit p-8 sm:p-12 text-center max-w-xl mx-auto space-y-6 border-emerald-500/40 shadow-2xl animate-in zoom-in-95 duration-200">
          <div className="w-20 h-20 rounded-3xl bg-gradient-to-tr from-emerald-500 to-cyan-400 flex items-center justify-center text-4xl mx-auto shadow-xl shadow-emerald-500/40 animate-bounce">
            🎯
          </div>

          <div>
            <h2 className="text-2xl sm:text-3xl font-black text-white">
              Practice Drill Concluded!
            </h2>
            <p className="text-xs sm:text-sm text-purple-300/80 mt-1">
              Outstanding work sharpening your core problem-solving instincts.
            </p>
          </div>

          <div className="grid grid-cols-3 gap-3 p-4 rounded-2xl bg-purple-950/40 border border-purple-500/20">
            <div>
              <div className="text-[11px] text-slate-400 font-medium">Solved</div>
              <div className="text-xl font-black text-white mt-0.5">
                {sessionStats.correct} / {sessionStats.totalAnswered}
              </div>
            </div>
            <div>
              <div className="text-[11px] text-slate-400 font-medium">Accuracy</div>
              <div className="text-xl font-black text-cyan-400 mt-0.5">
                {Math.round((sessionStats.correct / Math.max(1, sessionStats.totalAnswered)) * 100)}%
              </div>
            </div>
            <div>
              <div className="text-[11px] text-slate-400 font-medium">XP Earned</div>
              <div className="text-xl font-black text-amber-300 mt-0.5">
                +{sessionStats.xpEarned} XP
              </div>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
            <button
              type="button"
              onClick={() => startPractice(mode)}
              className="w-full sm:w-auto px-6 py-2.5 rounded-xl text-xs font-bold bg-gradient-to-r from-purple-600 to-cyan-500 text-white shadow-lg shadow-purple-600/30 hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center gap-2"
            >
              <RotateCcw className="w-4 h-4" />
              <span>Practice Again</span>
            </button>
            <button
              type="button"
              onClick={() => {
                setSessionCompleted(false);
                setStarted(false);
              }}
              className="w-full sm:w-auto px-5 py-2.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white bg-purple-950/40 border border-purple-500/20 transition-colors"
            >
              Configure Arena
            </button>
          </div>
        </div>
      )}

      {!started && !sessionCompleted && (
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
              <span>Configure Target Scope</span>
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  Target Subject
                </label>
                <select
                  value={selectedSubject}
                  onChange={(e) => setSelectedSubject(e.target.value)}
                  className="w-full p-2.5 rounded-xl bg-purple-950/40 border border-purple-500/20 text-slate-200 text-xs focus:outline-none focus:border-cyan-400"
                >
                  <option value="">All Completed Subjects</option>
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
                  <option value="">Any Difficulty (Adaptive)</option>
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
      )}

      {/* Active Practice Session */}
      {started && !sessionCompleted && (
        <div className="space-y-6">
          <div className="flex items-center justify-between card-orbit p-4 border-purple-500/20">
            <button
              onClick={() => setStarted(false)}
              className="text-xs font-semibold text-slate-400 hover:text-white transition-colors"
            >
              ← End Practice Session
            </button>
            <div className="flex items-center gap-4 text-xs font-bold">
              <span className="text-cyan-400">
                Question {currentQIndex + 1} of {questions.length}
              </span>
              <span className="text-slate-600">|</span>
              <span className="text-emerald-400">
                Score: {sessionStats.correct} Correct
              </span>
            </div>
          </div>

          {questions.length > 0 && questions[currentQIndex] ? (
            <InteractiveTask
              question={questions[currentQIndex]}
              topicId={questions[currentQIndex]?.topic_id}
              onCompleteNext={(isCorrect, xp) => handleNextQuestion(isCorrect, xp)}
            />
          ) : (
            <div className="card-orbit p-8 text-center space-y-4">
              <p className="text-sm text-slate-400">No practice questions found matching your completed topics.</p>
              <button
                onClick={() => setStarted(false)}
                className="px-4 py-2 rounded-xl text-xs font-bold bg-purple-600 text-white"
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
