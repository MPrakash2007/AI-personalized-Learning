import React, { useState, useEffect } from 'react';
import { useParams, NavLink, useNavigate } from 'react-router-dom';
import confetti from 'canvas-confetti';
import {
  ArrowLeft, ArrowRight, CheckCircle2, Trophy, Crown, Sparkles,
  BookOpen, Code, Brain, Zap, HelpCircle, Loader2
} from 'lucide-react';
import api from '../services/api';
import { useToast } from '../context/ToastContext';
import { useAuth } from '../context/AuthContext';
import InteractiveTask from '../components/Learning/InteractiveTask';

export default function LessonPlayerPage() {
  const { subjectSlug, topicSlug } = useParams();
  const [topic, setTopic] = useState(null);
  const [currentStep, setCurrentStep] = useState(1);
  const [activeQuestionIndex, setActiveQuestionIndex] = useState(0);
  const [completedLesson, setCompletedLesson] = useState(false);
  const [loading, setLoading] = useState(true);

  const toast = useToast();
  const { refreshMe } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    setLoading(true);
    api
      .get(`/topics/${topicSlug}`)
      .then((res) => {
        setTopic(res.data);
      })
      .catch((err) => {
        console.error('Failed to load topic lesson:', err);
      })
      .finally(() => setLoading(false));
  }, [topicSlug]);

  if (loading) {
    return (
      <div className="py-24 flex flex-col items-center justify-center gap-3 text-purple-300">
        <Loader2 className="w-8 h-8 animate-spin text-cyan-400" />
        <span className="text-sm">Preparing interactive lesson player...</span>
      </div>
    );
  }

  if (!topic) {
    return (
      <div className="text-center py-20">
        <h2 className="text-xl font-bold text-white mb-2">Topic not found</h2>
        <NavLink to={`/learn/${subjectSlug}`} className="text-sm text-cyan-400 hover:underline">
          ← Back to Curriculum
        </NavLink>
      </div>
    );
  }

  const lesson = topic.lessons?.[0];
  const steps = lesson?.steps || [];
  const questions = topic.questions || [];

  const handleStepComplete = async () => {
    if (currentStep < 6) {
      setCurrentStep((prev) => prev + 1);
    } else {
      // Completed all 6 steps
      try {
        if (lesson) {
          const res = await api.post(`/lessons/${lesson.id}/complete`);
          toast.xp(`+${res.data.xp_earned} XP! Topic completed.`);
        }
        await refreshMe();
        confetti({
          particleCount: 80,
          spread: 80,
          origin: { y: 0.6 },
          colors: ['#8b5cf6', '#06b6d4', '#10b981', '#f59e0b'],
        });
        setCompletedLesson(true);
      } catch (err) {
        console.error('Error completing lesson:', err);
        setCompletedLesson(true);
      }
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-in fade-in duration-200">
      {/* Top Breadcrumb & Subject Info */}
      <div className="flex items-center justify-between">
        <NavLink
          to={`/learn/${subjectSlug}`}
          className="inline-flex items-center gap-2 text-xs font-semibold text-slate-400 hover:text-white transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to {topic.subject_name || 'Curriculum'}</span>
        </NavLink>

        <div className="flex items-center gap-2 text-xs font-semibold text-purple-300">
          <span>{topic.subject_icon}</span>
          <span>{topic.subject_name}</span>
          <span className="text-slate-500">•</span>
          <span className="text-cyan-400">Step {currentStep} of 6</span>
        </div>
      </div>

      {/* Boss Challenge Special Header */}
      {topic.is_boss && (
        <div className="p-4 rounded-2xl bg-gradient-to-r from-amber-600/30 via-purple-600/20 to-amber-600/30 border border-amber-500/40 flex items-center justify-between shadow-xl">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-amber-500/20 border border-amber-400 flex items-center justify-center text-xl">
              👑
            </div>
            <div>
              <div className="text-sm font-black text-amber-300 uppercase tracking-wider">
                {topic.boss_title || 'Major Milestone Boss Challenge'}
              </div>
              <div className="text-xs text-slate-300">
                Conquer this milestone to achieve comprehensive mastery!
              </div>
            </div>
          </div>
          <div className="px-3 py-1 rounded-xl bg-amber-500/20 text-amber-300 font-bold text-xs">
            +100 XP
          </div>
        </div>
      )}

      {/* Progress Step Bar */}
      <div className="card-orbit p-4 border-purple-500/15">
        <div className="flex items-center justify-between text-xs font-semibold text-slate-300 mb-2">
          <span>{topic.title}</span>
          <span className="text-cyan-400">{Math.round((currentStep / 6) * 100)}%</span>
        </div>
        <div className="grid grid-cols-6 gap-1.5 sm:gap-2">
          {['Understand', 'Example', 'Practice', 'Apply', 'Challenge', 'Quiz'].map(
            (label, idx) => {
              const stepNum = idx + 1;
              const isDone = stepNum < currentStep;
              const isCurrent = stepNum === currentStep;

              return (
                <div key={label} className="space-y-1">
                  <div
                    className={`h-2 rounded-full transition-all ${
                      isDone
                        ? 'bg-emerald-400'
                        : isCurrent
                        ? 'bg-cyan-400 shadow-sm shadow-cyan-400 animate-pulse'
                        : 'bg-purple-950/80 border border-purple-500/20'
                    }`}
                  />
                  <div className="hidden sm:block text-[10px] text-center text-purple-300/60 truncate font-medium">
                    {label}
                  </div>
                </div>
              );
            }
          )}
        </div>
      </div>

      {/* Main Lesson Content Card or Quiz Player */}
      {!completedLesson ? (
        currentStep < 6 ? (
          <div className="card-orbit p-6 sm:p-8 space-y-6">
            <div>
              <span className="text-[11px] font-bold text-cyan-400 uppercase tracking-wider">
                Step {currentStep}: {steps[currentStep - 1]?.step_type}
              </span>
              <h2 className="text-2xl font-bold text-white mt-1">
                {steps[currentStep - 1]?.title || `${topic.title} Principle`}
              </h2>
            </div>

            <div className="prose prose-invert max-w-none text-slate-200 text-sm leading-relaxed space-y-4">
              <p>{steps[currentStep - 1]?.content}</p>

              {steps[currentStep - 1]?.code_snippet && (
                <div className="p-4 rounded-xl bg-[#090514] border border-purple-500/25 font-mono text-xs text-purple-200 overflow-x-auto my-4">
                  <pre>{steps[currentStep - 1].code_snippet}</pre>
                </div>
              )}
            </div>

            {/* Quick Checkpoint within Step */}
            <div className="p-4 rounded-xl bg-purple-950/30 border border-purple-500/20 flex items-center justify-between">
              <div className="flex items-center gap-2 text-xs font-semibold text-purple-300">
                <Sparkles className="w-4 h-4 text-cyan-400" />
                <span>Concept Checkpoint Ready</span>
              </div>
              <button
                type="button"
                onClick={handleStepComplete}
                className="px-5 py-2 rounded-xl text-xs font-bold bg-gradient-to-r from-purple-600 to-cyan-500 text-white shadow-lg shadow-purple-600/30 hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center gap-1.5"
              >
                <span>Continue to Step {currentStep + 1}</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        ) : (
          /* Step 6: Interactive Topic Quiz Assessment */
          <div className="space-y-4">
            <div className="text-center py-2">
              <h2 className="text-xl font-bold text-white">⭐ Topic Challenge Assessment</h2>
              <p className="text-xs text-slate-400">
                Solve the interactive problem below to verify mastery and earn topic XP.
              </p>
            </div>

            {questions.length > 0 ? (
              <InteractiveTask
                question={questions[activeQuestionIndex % questions.length]}
                topicId={topic.id}
                onCompleteNext={handleStepComplete}
              />
            ) : (
              <div className="card-orbit p-8 text-center space-y-4">
                <p className="text-sm text-slate-300">
                  Ready to submit your topic completion!
                </p>
                <button
                  type="button"
                  onClick={handleStepComplete}
                  className="px-6 py-2.5 rounded-xl font-bold text-xs bg-gradient-to-r from-emerald-600 to-teal-500 text-white"
                >
                  Complete Topic Lesson
                </button>
              </div>
            )}
          </div>
        )
      ) : (
        /* Final Completion Result Card */
        <div className="card-orbit p-8 sm:p-12 text-center max-w-xl mx-auto space-y-6 border-emerald-500/40 shadow-2xl">
          <div className="w-20 h-20 rounded-3xl bg-gradient-to-tr from-emerald-500 to-cyan-400 flex items-center justify-center text-4xl mx-auto shadow-xl shadow-emerald-500/40 animate-bounce">
            🏆
          </div>

          <div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white">
              Topic Masterclass Complete!
            </h2>
            <p className="text-xs sm:text-sm text-purple-300/80 mt-1">
              You've successfully advanced your knowledge in {topic.title}.
            </p>
          </div>

          <div className="grid grid-cols-3 gap-3 p-4 rounded-xl bg-purple-950/40 border border-purple-500/20">
            <div>
              <div className="text-xs text-slate-400 font-medium">XP Earned</div>
              <div className="text-lg font-bold text-amber-300">+{topic.is_boss ? 100 : 50} XP</div>
            </div>
            <div>
              <div className="text-xs text-slate-400 font-medium">Mastery</div>
              <div className="text-lg font-bold text-emerald-400">
                {Math.max(75, topic.progress?.mastery_score || 78)}%
              </div>
            </div>
            <div>
              <div className="text-xs text-slate-400 font-medium">Status</div>
              <div className="text-lg font-bold text-cyan-400">Unlocked</div>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-4">
            <NavLink
              to={`/learn/${subjectSlug}`}
              className="w-full sm:w-auto px-6 py-2.5 rounded-xl text-xs font-bold bg-gradient-to-r from-purple-600 to-cyan-500 text-white shadow-lg shadow-purple-600/30 hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center gap-2"
            >
              <span>Continue Learning Path</span>
              <ArrowRight className="w-4 h-4" />
            </NavLink>
            <NavLink
              to="/practice"
              className="w-full sm:w-auto px-6 py-2.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white bg-purple-950/40 border border-purple-500/20 transition-colors"
            >
              Practice Arena
            </NavLink>
          </div>
        </div>
      )}
    </div>
  );
}
