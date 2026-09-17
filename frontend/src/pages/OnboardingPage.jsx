import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Sparkles, Check, ArrowRight, ArrowLeft, Brain, Target, Clock, BookOpen
} from 'lucide-react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';

export default function OnboardingPage() {
  const [step, setStep] = useState(1);
  const [selectedSubjects, setSelectedSubjects] = useState(['DBMS', 'DS']);
  const [level, setLevel] = useState('Intermediate');
  const [dailyTime, setDailyTime] = useState(30);
  const [goal, setGoal] = useState('Placement preparation');
  const [loading, setLoading] = useState(false);

  const { updateUser } = useAuth();
  const toast = useToast();
  const navigate = useNavigate();

  const subjectsList = [
    { name: 'DBMS', icon: '🗄️', desc: 'Databases & Query Tuning' },
    { name: 'OOPS', icon: '🧩', desc: 'Object-Oriented Architecture' },
    { name: 'OS', icon: '⚙️', desc: 'Operating Systems & Concurrency' },
    { name: 'DS', icon: '🌳', desc: 'Data Structures & Algorithms' },
    { name: 'ML', icon: '🧠', desc: 'Machine Learning & Models' },
    { name: 'CN', icon: '🌐', desc: 'Computer Networks & TCP/IP' },
  ];

  const levels = [
    { id: 'Beginner', title: 'Beginner', desc: 'Starting from fundamental first principles' },
    { id: 'Intermediate', title: 'Intermediate', desc: 'Have basic syntax, need deeper concepts' },
    { id: 'Advanced', title: 'Advanced', desc: 'Aiming for top product company interviews' },
  ];

  const timeOptions = [
    { min: 15, label: '15 min / day', desc: 'Quick daily dose' },
    { min: 30, label: '30 min / day', desc: 'Steady learning (Recommended)' },
    { min: 45, label: '45 min / day', desc: 'Focused study pace' },
    { min: 60, label: '60+ min / day', desc: 'Intensive sprint' },
  ];

  const goals = [
    'Placement preparation',
    'Semester examination prep',
    'Skill development & mastery',
    'Competitive programming',
    'System design & interviews',
  ];

  const toggleSubject = (sName) => {
    if (selectedSubjects.includes(sName)) {
      if (selectedSubjects.length > 1) {
        setSelectedSubjects(selectedSubjects.filter((s) => s !== sName));
      }
    } else {
      setSelectedSubjects([...selectedSubjects, sName]);
    }
  };

  const handleFinish = async () => {
    setLoading(true);
    try {
      const res = await api.post('/auth/onboarding', {
        programming_level: level,
        preferred_subjects: selectedSubjects,
        daily_target_minutes: dailyTime,
        career_goal: goal,
      });

      updateUser(res.data);
      toast.success('🎉 Personalization complete! +50 XP bonus awarded.');
      navigate('/dashboard');
    } catch (err) {
      console.error('Onboarding submission error:', err);
      toast.error('Failed to save preferences, proceeding to dashboard.');
      navigate('/dashboard');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#090514] text-slate-100 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background ambient lighting */}
      <div className="fixed top-1/3 left-1/3 w-96 h-96 rounded-full bg-purple-600/20 blur-[130px] pointer-events-none" />
      <div className="fixed bottom-1/3 right-1/3 w-96 h-96 rounded-full bg-cyan-600/20 blur-[130px] pointer-events-none" />

      <div className="w-full max-w-xl card-orbit p-8 relative z-10 border border-purple-500/30 shadow-2xl">
        {/* Step Indicator */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-2">
            {[1, 2, 3, 4].map((i) => (
              <div
                key={i}
                className={`h-2 rounded-full transition-all ${
                  i === step
                    ? 'w-8 bg-cyan-400 shadow-sm shadow-cyan-400'
                    : i < step
                    ? 'w-4 bg-purple-500'
                    : 'w-4 bg-purple-950/60'
                }`}
              />
            ))}
          </div>
          <span className="text-xs font-bold text-purple-300/70 uppercase tracking-wider">
            Step {step} of 4
          </span>
        </div>

        {/* Step 1: Subjects */}
        {step === 1 && (
          <div className="space-y-5 animate-in fade-in duration-200">
            <div>
              <h2 className="text-2xl font-bold text-white mb-1.5 flex items-center gap-2">
                What do you want to learn?
                <Sparkles className="w-5 h-5 text-cyan-400" />
              </h2>
              <p className="text-xs text-purple-300/70">
                Choose the core computer science disciplines you want to focus on.
              </p>
            </div>

            <div className="grid grid-cols-2 gap-3">
              {subjectsList.map((s) => {
                const isSelected = selectedSubjects.includes(s.name);
                return (
                  <button
                    key={s.name}
                    type="button"
                    onClick={() => toggleSubject(s.name)}
                    className={`p-4 rounded-xl border text-left transition-all flex flex-col justify-between ${
                      isSelected
                        ? 'bg-purple-600/30 border-cyan-400 ring-1 ring-cyan-400 shadow-lg shadow-purple-950/60'
                        : 'bg-purple-950/30 border-purple-500/20 hover:border-purple-400/40 text-slate-300'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-2xl">{s.icon}</span>
                      {isSelected && <Check className="w-4 h-4 text-cyan-400" />}
                    </div>
                    <div>
                      <div className="text-sm font-bold text-white">{s.name}</div>
                      <div className="text-[11px] text-purple-200/60">{s.desc}</div>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {/* Step 2: Current Level */}
        {step === 2 && (
          <div className="space-y-5 animate-in fade-in duration-200">
            <div>
              <h2 className="text-2xl font-bold text-white mb-1.5 flex items-center gap-2">
                What's your current level?
                <Brain className="w-5 h-5 text-purple-400" />
              </h2>
              <p className="text-xs text-purple-300/70">
                This helps us calibrate question difficulty and recommendation pacing.
              </p>
            </div>

            <div className="space-y-3">
              {levels.map((lvl) => {
                const isSelected = level === lvl.id;
                return (
                  <button
                    key={lvl.id}
                    type="button"
                    onClick={() => setLevel(lvl.id)}
                    className={`w-full p-4 rounded-xl border text-left transition-all flex items-center justify-between ${
                      isSelected
                        ? 'bg-purple-600/30 border-cyan-400 ring-1 ring-cyan-400 shadow-lg'
                        : 'bg-purple-950/30 border-purple-500/20 hover:border-purple-400/40'
                    }`}
                  >
                    <div>
                      <div className="text-sm font-bold text-white">{lvl.title}</div>
                      <div className="text-xs text-purple-200/60">{lvl.desc}</div>
                    </div>
                    {isSelected && <Check className="w-5 h-5 text-cyan-400 shrink-0" />}
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {/* Step 3: Daily Target */}
        {step === 3 && (
          <div className="space-y-5 animate-in fade-in duration-200">
            <div>
              <h2 className="text-2xl font-bold text-white mb-1.5 flex items-center gap-2">
                How much time can you study daily?
                <Clock className="w-5 h-5 text-amber-400" />
              </h2>
              <p className="text-xs text-purple-300/70">
                We'll tailor your daily quests and streak targets based on your commitment.
              </p>
            </div>

            <div className="grid grid-cols-2 gap-3">
              {timeOptions.map((t) => {
                const isSelected = dailyTime === t.min;
                return (
                  <button
                    key={t.min}
                    type="button"
                    onClick={() => setDailyTime(t.min)}
                    className={`p-4 rounded-xl border text-left transition-all ${
                      isSelected
                        ? 'bg-purple-600/30 border-cyan-400 ring-1 ring-cyan-400 shadow-lg'
                        : 'bg-purple-950/30 border-purple-500/20 hover:border-purple-400/40'
                    }`}
                  >
                    <div className="text-sm font-bold text-white mb-1">{t.label}</div>
                    <div className="text-[11px] text-purple-200/60">{t.desc}</div>
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {/* Step 4: Primary Goal */}
        {step === 4 && (
          <div className="space-y-5 animate-in fade-in duration-200">
            <div>
              <h2 className="text-2xl font-bold text-white mb-1.5 flex items-center gap-2">
                What is your primary goal?
                <Target className="w-5 h-5 text-emerald-400" />
              </h2>
              <p className="text-xs text-purple-300/70">
                We'll prioritize recommendations to match your target outcome.
              </p>
            </div>

            <div className="space-y-2.5">
              {goals.map((g) => {
                const isSelected = goal === g;
                return (
                  <button
                    key={g}
                    type="button"
                    onClick={() => setGoal(g)}
                    className={`w-full p-3.5 rounded-xl border text-left text-sm font-medium transition-all flex items-center justify-between ${
                      isSelected
                        ? 'bg-purple-600/30 border-cyan-400 text-white ring-1 ring-cyan-400'
                        : 'bg-purple-950/30 border-purple-500/20 text-slate-300 hover:border-purple-400/40'
                    }`}
                  >
                    <span>{g}</span>
                    {isSelected && <Check className="w-4 h-4 text-cyan-400" />}
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {/* Navigation Buttons */}
        <div className="flex items-center justify-between pt-8 border-t border-purple-500/15 mt-8">
          {step > 1 ? (
            <button
              type="button"
              onClick={() => setStep(step - 1)}
              className="px-4 py-2.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white flex items-center gap-1.5 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back</span>
            </button>
          ) : (
            <div />
          )}

          {step < 4 ? (
            <button
              type="button"
              onClick={() => setStep(step + 1)}
              className="px-6 py-2.5 rounded-xl text-xs font-bold bg-gradient-to-r from-purple-600 to-cyan-500 text-white shadow-lg shadow-purple-600/30 hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center gap-1.5"
            >
              <span>Next</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          ) : (
            <button
              type="button"
              disabled={loading}
              onClick={handleFinish}
              className="px-6 py-2.5 rounded-xl text-xs font-bold bg-gradient-to-r from-emerald-600 to-teal-500 text-white shadow-lg shadow-emerald-600/30 hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center gap-1.5 disabled:opacity-50"
            >
              <span>{loading ? 'Finalizing...' : 'Launch Dashboard 🚀'}</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
