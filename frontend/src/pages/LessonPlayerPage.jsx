import React, { useState, useEffect, useRef } from 'react';
import { useParams, NavLink, useNavigate } from 'react-router-dom';
import confetti from 'canvas-confetti';
import {
  ArrowLeft, ArrowRight, CheckCircle2, Trophy, Crown, Sparkles,
  BookOpen, Code, Brain, Zap, HelpCircle, Loader2, ExternalLink,
  Target, RotateCcw, Award, CheckCircle, BarChart3, ChevronRight,
  BookMarked, Lightbulb, Bookmark, AlertTriangle, Table, Lock
} from 'lucide-react';
import api from '../services/api';
import { useToast } from '../context/ToastContext';
import { useAuth } from '../context/AuthContext';
import InteractiveTask from '../components/Learning/InteractiveTask';
import QuickReferenceButton from '../components/Learning/QuickReferenceButton';

export default function LessonPlayerPage() {
  const { subjectSlug, topicSlug } = useParams();
  const [topic, setTopic] = useState(null);
  const [viewMode, setViewMode] = useState('study'); // 'study' | 'quiz' | 'summary'
  const [activeSectionIdx, setActiveSectionIdx] = useState(0);
  const [learnQuestions, setLearnQuestions] = useState([]);
  const [activeQuestionIdx, setActiveQuestionIdx] = useState(0);
  const [quizStats, setQuizStats] = useState({ correct: 0, totalAnswered: 0, xpEarned: 0 });
  const [userAnswers, setUserAnswers] = useState([]);
  const [completionResult, setCompletionResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [loadingQuiz, setLoadingQuiz] = useState(false);
  const [lockedError, setLockedError] = useState(null);

  const quizStartTimeRef = useRef(Date.now());

  const toast = useToast();
  const { refreshMe } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    setLoading(true);
    setLockedError(null);
    api
      .get(`/topics/${topicSlug}`)
      .then((res) => {
        setTopic(res.data);
      })
      .catch((err) => {
        console.error('Failed to load topic lesson:', err);
        if (err.response?.status === 403) {
          setLockedError(err.response?.data?.detail || 'This topic is locked. Complete the previous topic to continue.');
        }
      })
      .finally(() => setLoading(false));
  }, [topicSlug]);

  const loadLearnQuestions = async () => {
    if (learnQuestions.length > 0) {
      setViewMode('quiz');
      quizStartTimeRef.current = Date.now();
      return;
    }
    setLoadingQuiz(true);
    try {
      const res = await api.get(`/topics/${topicSlug}/learn-questions`);
      const qList = res.data.questions || [];
      setLearnQuestions(qList);
      setActiveQuestionIdx(0);
      setQuizStats({ correct: 0, totalAnswered: 0, xpEarned: 0 });
      setUserAnswers([]);
      quizStartTimeRef.current = Date.now();
      setViewMode('quiz');
    } catch (err) {
      console.error('Failed to load learn questions:', err);
      if (err.response?.status === 403) {
        toast.error('This topic quiz is locked. Complete previous topics first.');
      } else {
        toast.error('Failed to load topic questions. Please try again.');
      }
    } finally {
      setLoadingQuiz(false);
    }
  };

  const handleQuestionComplete = async (isCorrect, xp) => {
    const currentQ = learnQuestions[activeQuestionIdx];
    const newCorrect = quizStats.correct + (isCorrect ? 1 : 0);
    const newAnswered = quizStats.totalAnswered + 1;
    const newXp = quizStats.xpEarned + (xp || (isCorrect ? 10 : 0));

    const updatedAnswers = [
      ...userAnswers,
      {
        question_id: currentQ?.id,
        is_correct: isCorrect,
        time_taken_seconds: 15
      }
    ];
    setUserAnswers(updatedAnswers);

    setQuizStats({
      correct: newCorrect,
      totalAnswered: newAnswered,
      xpEarned: newXp
    });

    if (activeQuestionIdx + 1 < learnQuestions.length) {
      setActiveQuestionIdx((prev) => prev + 1);
    } else {
      // Completed all questions in the quiz!
      const totalElapsed = Math.round((Date.now() - quizStartTimeRef.current) / 1000);
      try {
        const completeRes = await api.post(`/topics/${topicSlug}/complete-quiz`, {
          score: newCorrect,
          total: newAnswered,
          answers: updatedAnswers,
          time_taken_seconds: totalElapsed
        });
        setCompletionResult(completeRes.data);
        await refreshMe();
      } catch (err) {
        console.error('Quiz completion API error:', err);
        // Fallback local calculation if offline
        const accuracyPct = Math.round((newCorrect / Math.max(1, newAnswered)) * 100);
        setCompletionResult({
          status: accuracyPct >= 85 ? 'MASTERED' : 'COMPLETED',
          mastery_score: accuracyPct,
          accuracy: accuracyPct,
          xp_awarded: newXp,
          next_topic_slug: null
        });
      }

      confetti({
        particleCount: 120,
        spread: 90,
        origin: { y: 0.6 },
        colors: ['#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ec4899'],
      });
      setViewMode('summary');
    }
  };

  if (loading) {
    return (
      <div className="py-24 flex flex-col items-center justify-center gap-3 text-purple-300">
        <Loader2 className="w-8 h-8 animate-spin text-cyan-400" />
        <span className="text-sm">Loading comprehensive topic masterclass...</span>
      </div>
    );
  }

  if (lockedError) {
    return (
      <div className="card-orbit p-8 sm:p-12 text-center max-w-lg mx-auto my-16 space-y-6 border-amber-500/30 shadow-2xl">
        <div className="w-16 h-16 rounded-3xl bg-amber-500/20 border border-amber-400/40 flex items-center justify-center text-amber-300 mx-auto">
          <Lock className="w-8 h-8" />
        </div>
        <div>
          <h2 className="text-xl sm:text-2xl font-black text-white">Topic Locked</h2>
          <p className="text-xs sm:text-sm text-purple-300/80 mt-2 leading-relaxed">
            {lockedError}
          </p>
        </div>
        <NavLink
          to={`/learn/${subjectSlug}`}
          className="inline-flex items-center gap-2 px-6 py-3 rounded-xl text-xs font-bold bg-gradient-to-r from-purple-600 to-cyan-500 text-white shadow-lg shadow-purple-600/30 hover:scale-105 transition-all"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Curriculum Roadmap</span>
        </NavLink>
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

  const sections = topic.sections && topic.sections.length > 0
    ? topic.sections
    : (topic.lessons?.[0]?.steps || []);

  const sources = topic.source_references || [];
  const currentSection = sections[activeSectionIdx] || sections[0];

  return (
    <div className="max-w-5xl mx-auto space-y-6 animate-in fade-in duration-200">
      {/* Top Header & Breadcrumb */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <NavLink
            to={`/learn/${subjectSlug}`}
            className="inline-flex items-center gap-2 text-xs font-semibold text-slate-400 hover:text-white transition-colors mb-2"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to {topic.subject_name || 'Curriculum'}</span>
          </NavLink>
          <div className="flex items-center gap-3">
            <span className="text-3xl">{topic.subject_icon || '📚'}</span>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-xl sm:text-2xl font-black text-white">{topic.title}</h1>
                {topic.is_boss && (
                  <span className="px-2.5 py-0.5 rounded-full bg-amber-500/20 border border-amber-400/50 text-amber-300 text-[10px] font-bold uppercase tracking-wider">
                    👑 Boss Milestone
                  </span>
                )}
              </div>
              <p className="text-xs text-purple-300/80">{topic.description}</p>
            </div>
          </div>
        </div>

        {/* Action Buttons: Quick Reference + Quiz */}
        <div className="flex items-center gap-2.5 flex-wrap">
          <QuickReferenceButton topicSlug={topicSlug} onStartQuiz={loadLearnQuestions} />

          <div className="flex items-center gap-1.5 bg-[#120a2b] p-1.5 rounded-2xl border border-purple-500/30">
            <button
              type="button"
              onClick={() => setViewMode('study')}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 ${
                viewMode === 'study'
                  ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg shadow-purple-600/30'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <BookOpen className="w-3.5 h-3.5 text-cyan-400" />
              <span>Study</span>
            </button>
            <button
              type="button"
              onClick={loadLearnQuestions}
              disabled={loadingQuiz}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 ${
                viewMode === 'quiz'
                  ? 'bg-gradient-to-r from-cyan-500 to-teal-500 text-slate-950 shadow-lg shadow-cyan-500/30'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {loadingQuiz ? (
                <Loader2 className="w-3.5 h-3.5 animate-spin text-cyan-300" />
              ) : (
                <Target className="w-3.5 h-3.5 text-amber-300" />
              )}
              <span>Topic Quiz</span>
            </button>
          </div>
        </div>
      </div>

      {/* =========================================================================
          VIEW MODE: STUDY MATERIAL (12 Deep Educational Sections)
      ========================================================================= */}
      {viewMode === 'study' && (
        <div className="space-y-6">
          {/* Section Tabs Navigator */}
          <div className="card-orbit p-3 border-purple-500/20 overflow-x-auto">
            <div className="flex items-center gap-2 min-w-max">
              {sections.map((sec, idx) => {
                const isActive = idx === activeSectionIdx;
                return (
                  <button
                    key={sec.id || idx}
                    type="button"
                    onClick={() => setActiveSectionIdx(idx)}
                    className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 ${
                      isActive
                        ? 'bg-purple-600/40 border border-cyan-400 text-cyan-200 shadow-md shadow-purple-950/60'
                        : 'bg-purple-950/20 border border-purple-500/10 text-slate-400 hover:text-slate-200 hover:bg-purple-900/20'
                    }`}
                  >
                    <span className="w-4 h-4 rounded-full bg-purple-800/60 flex items-center justify-center text-[10px]">
                      {idx + 1}
                    </span>
                    <span className="capitalize truncate max-w-[130px] sm:max-w-[170px]">
                      {sec.title || `Section ${idx + 1}`}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Active Section Content Card */}
          {currentSection && (
            <div className="card-orbit p-6 sm:p-8 space-y-6 border-purple-500/30 shadow-2xl">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-purple-500/20 pb-4">
                <div>
                  <span className="text-[11px] font-bold text-cyan-400 uppercase tracking-wider">
                    Section {activeSectionIdx + 1} of {sections.length} • {currentSection.section_type?.replace('_', ' ') || 'Core Concept'}
                  </span>
                  <h2 className="text-xl sm:text-2xl font-black text-white mt-1">
                    {currentSection.title}
                  </h2>
                </div>
                <div className="flex items-center gap-2">
                  <span className="px-3 py-1 rounded-full bg-purple-900/40 border border-purple-500/30 text-purple-300 text-xs font-semibold">
                    12-Part Exam Masterclass
                  </span>
                </div>
              </div>

              {/* Main Educational Text */}
              <div className="prose prose-invert max-w-none text-slate-200 text-sm sm:text-base leading-relaxed whitespace-pre-line space-y-4">
                {currentSection.content}
              </div>

              {/* Example Data / Matrix / Comparison Table */}
              {currentSection.example_data && (
                <div className="p-4 rounded-2xl bg-indigo-950/30 border border-indigo-500/30 space-y-2">
                  <div className="flex items-center gap-2 text-xs font-bold text-indigo-300 uppercase tracking-wider">
                    <Table className="w-4 h-4 text-cyan-400" />
                    <span>Technical Reference & Data Matrix</span>
                  </div>
                  <div className="text-xs text-slate-300 whitespace-pre-line font-mono bg-[#090514] p-3 rounded-xl border border-indigo-500/20 overflow-x-auto">
                    {currentSection.example_data}
                  </div>
                </div>
              )}

              {/* Code Snippet */}
              {currentSection.code_snippet && (
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-xs text-purple-300 font-mono px-1">
                    <span className="flex items-center gap-1.5 font-bold">
                      <Code className="w-3.5 h-3.5 text-cyan-400" />
                      <span>Code Implementation / Demonstration</span>
                    </span>
                  </div>
                  <div className="p-4 rounded-2xl bg-[#080414] border border-purple-500/30 font-mono text-xs text-purple-200 overflow-x-auto shadow-inner">
                    <pre>{currentSection.code_snippet}</pre>
                  </div>
                </div>
              )}

              {/* Diagram / ASCII Schematics */}
              {currentSection.diagram_data && (
                <div className="space-y-2">
                  <div className="text-xs font-bold text-cyan-300 flex items-center gap-1.5 uppercase tracking-wider">
                    <Brain className="w-4 h-4 text-cyan-400" />
                    <span>System Architecture / Visual Data Flow</span>
                  </div>
                  <div className="p-4 rounded-2xl bg-[#090514] border border-cyan-500/30 font-mono text-xs text-cyan-200 overflow-x-auto">
                    <pre className="leading-tight">{currentSection.diagram_data}</pre>
                  </div>
                </div>
              )}

              {/* Section Navigation Buttons */}
              <div className="flex items-center justify-between pt-6 border-t border-purple-500/20">
                <button
                  type="button"
                  disabled={activeSectionIdx === 0}
                  onClick={() => setActiveSectionIdx((prev) => Math.max(0, prev - 1))}
                  className="px-4 py-2 rounded-xl text-xs font-bold bg-purple-950/50 border border-purple-500/30 text-slate-300 hover:text-white disabled:opacity-30 disabled:pointer-events-none transition-all flex items-center gap-1.5"
                >
                  <ArrowLeft className="w-3.5 h-3.5" />
                  <span>Previous</span>
                </button>

                {activeSectionIdx + 1 < sections.length ? (
                  <button
                    type="button"
                    onClick={() => setActiveSectionIdx((prev) => prev + 1)}
                    className="px-5 py-2.5 rounded-xl text-xs font-bold bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg shadow-purple-600/30 hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center gap-1.5"
                  >
                    <span>Next: {sections[activeSectionIdx + 1]?.title}</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                ) : (
                  <div className="flex items-center gap-3">
                    <QuickReferenceButton topicSlug={topicSlug} />
                    <button
                      type="button"
                      onClick={loadLearnQuestions}
                      className="px-6 py-2.5 rounded-xl text-xs font-extrabold bg-gradient-to-r from-cyan-400 to-emerald-400 text-slate-950 shadow-xl shadow-cyan-400/30 hover:scale-[1.03] active:scale-[0.98] transition-all flex items-center gap-2"
                    >
                      <span>Start Topic Quiz →</span>
                      <ArrowRight className="w-4 h-4" />
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Bottom Prominent CTA to Start Quiz */}
          <div className="p-6 sm:p-8 rounded-3xl bg-gradient-to-r from-purple-900/40 via-[#150d33] to-cyan-900/40 border border-cyan-500/30 flex flex-col sm:flex-row items-center justify-between gap-6 shadow-2xl">
            <div className="space-y-2 text-center sm:text-left">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/20 text-cyan-300 text-xs font-bold">
                <Target className="w-3.5 h-3.5" />
                <span>Topic Mastery Quiz (15–20 Questions)</span>
              </div>
              <h3 className="text-xl sm:text-2xl font-black text-white">
                Ready to Validate Your Knowledge?
              </h3>
              <p className="text-xs sm:text-sm text-purple-200/80 max-w-xl">
                Completing this quiz evaluates conceptual accuracy, unlocks the next topic in sequence, and awards XP.
              </p>
            </div>
            <div className="flex items-center gap-3 shrink-0">
              <QuickReferenceButton topicSlug={topicSlug} variant="outline" label="Open Quick Reference" />
              <button
                type="button"
                onClick={loadLearnQuestions}
                disabled={loadingQuiz}
                className="px-6 py-3 rounded-2xl font-black text-xs bg-gradient-to-r from-cyan-400 to-teal-400 text-slate-950 shadow-xl shadow-cyan-400/40 hover:scale-105 active:scale-95 transition-all flex items-center gap-2"
              >
                {loadingQuiz ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin text-slate-950" />
                    <span>Loading...</span>
                  </>
                ) : (
                  <>
                    <span>Start Quiz Now</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Verified Reference Sources Card */}
          {sources.length > 0 && (
            <div className="card-orbit p-5 border-purple-500/20 space-y-3">
              <div className="flex items-center gap-2 text-xs font-bold text-purple-300 uppercase tracking-wider">
                <BookMarked className="w-4 h-4 text-cyan-400" />
                <span>Verified Reference Portals</span>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {sources.map((src, idx) => (
                  <a
                    key={idx}
                    href={src.source_url || src.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="p-3 rounded-xl bg-purple-950/30 border border-purple-500/20 hover:border-cyan-400/50 hover:bg-purple-900/30 transition-all flex items-center justify-between group"
                  >
                    <div>
                      <div className="text-xs font-bold text-slate-200 group-hover:text-cyan-300">
                        {src.title || src.source_name || src.name}
                      </div>
                      <div className="text-[10px] text-purple-400 font-mono">
                        {src.source_name || 'Academic Reference'}
                      </div>
                    </div>
                    <ExternalLink className="w-4 h-4 text-slate-400 group-hover:text-cyan-300" />
                  </a>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* =========================================================================
          VIEW MODE: TOPIC QUIZ (15–20 Questions)
      ========================================================================= */}
      {viewMode === 'quiz' && (
        <div className="space-y-6">
          {/* Quiz Status & Progress Header */}
          <div className="card-orbit p-4 border-purple-500/30 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="space-y-1">
              <div className="flex items-center gap-3 flex-wrap">
                <span className="text-xs font-bold text-cyan-400 uppercase tracking-wider">
                  Question {activeQuestionIdx + 1} of {learnQuestions.length}
                </span>
                <span className="text-slate-500">•</span>
                <span className="text-xs font-semibold text-emerald-400">
                  Score: {quizStats.correct} / {quizStats.totalAnswered} Correct
                </span>
                <span className="text-slate-500">•</span>
                <span className="text-xs font-semibold text-amber-300">
                  +{quizStats.xpEarned} XP
                </span>
              </div>
              <div className="w-full sm:w-80 h-2 rounded-full bg-purple-950 overflow-hidden mt-1">
                <div
                  className="h-full bg-gradient-to-r from-purple-500 to-cyan-400 rounded-full transition-all duration-300"
                  style={{
                    width: `${((activeQuestionIdx + 1) / Math.max(1, learnQuestions.length)) * 100}%`
                  }}
                />
              </div>
            </div>

            <div className="flex items-center gap-2">
              <QuickReferenceButton topicSlug={topicSlug} variant="pill" />
              <button
                type="button"
                onClick={() => setViewMode('study')}
                className="px-3 py-1.5 rounded-xl bg-purple-950/40 border border-purple-500/20 text-xs font-semibold text-slate-300 hover:text-white transition-colors flex items-center gap-1.5"
              >
                <BookOpen className="w-3.5 h-3.5 text-cyan-400" />
                <span>Review Notes</span>
              </button>
            </div>
          </div>

          {/* Interactive Question Component */}
          {learnQuestions.length > 0 && learnQuestions[activeQuestionIdx] ? (
            <InteractiveTask
              question={learnQuestions[activeQuestionIdx]}
              topicId={topic.id}
              onCompleteNext={(isCorrect, xp) => handleQuestionComplete(isCorrect, xp)}
            />
          ) : (
            <div className="card-orbit p-12 text-center space-y-4">
              <p className="text-slate-300 text-sm">No questions found for this topic.</p>
              <button
                type="button"
                onClick={() => setViewMode('study')}
                className="px-6 py-2.5 rounded-xl text-xs font-bold bg-purple-600 text-white"
              >
                Back to Study Material
              </button>
            </div>
          )}
        </div>
      )}

      {/* =========================================================================
          VIEW MODE: TOPIC COMPLETION SUMMARY (Unlocks Next Topic)
      ========================================================================= */}
      {viewMode === 'summary' && (
        <div className="card-orbit p-8 sm:p-12 text-center max-w-2xl mx-auto space-y-8 border-emerald-500/40 shadow-2xl">
          <div className="w-20 h-20 rounded-3xl bg-gradient-to-tr from-emerald-500 to-cyan-400 flex items-center justify-center text-4xl mx-auto shadow-xl shadow-emerald-500/40 animate-bounce">
            🏆
          </div>

          <div>
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/20 border border-emerald-400/40 text-emerald-300 text-xs font-bold uppercase tracking-wider mb-2">
              <CheckCircle className="w-3.5 h-3.5" />
              <span>{completionResult?.status || 'Topic Completed'}</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-black text-white">
              {topic.title} Mastered!
            </h2>
            <p className="text-xs sm:text-sm text-purple-300/80 mt-1 max-w-md mx-auto">
              {completionResult?.message || "You've successfully completed the exam requirements for this module."}
            </p>
          </div>

          {/* Score Metrics Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 p-4 rounded-2xl bg-purple-950/40 border border-purple-500/20">
            <div>
              <div className="text-[11px] text-slate-400 font-medium">Questions Solved</div>
              <div className="text-xl font-black text-white mt-0.5">
                {quizStats.correct} / {learnQuestions.length || 20}
              </div>
            </div>
            <div>
              <div className="text-[11px] text-slate-400 font-medium">Accuracy</div>
              <div className="text-xl font-black text-cyan-400 mt-0.5">
                {completionResult?.accuracy || Math.round((quizStats.correct / Math.max(1, quizStats.totalAnswered)) * 100)}%
              </div>
            </div>
            <div>
              <div className="text-[11px] text-slate-400 font-medium">XP Earned</div>
              <div className="text-xl font-black text-amber-300 mt-0.5">
                +{completionResult?.xp_awarded || quizStats.xpEarned} XP
              </div>
            </div>
            <div>
              <div className="text-[11px] text-slate-400 font-medium">Mastery Status</div>
              <div className="text-base font-black text-emerald-400 mt-1 uppercase">
                {completionResult?.status || 'COMPLETED'}
              </div>
            </div>
          </div>

          {/* Progression Actions */}
          <div className="space-y-3 pt-2">
            {completionResult?.next_topic_slug ? (
              <button
                type="button"
                onClick={() => navigate(`/learn/${subjectSlug}/${completionResult.next_topic_slug}`)}
                className="w-full px-8 py-4 rounded-2xl text-sm font-black bg-gradient-to-r from-emerald-400 via-teal-400 to-cyan-400 text-slate-950 shadow-xl shadow-emerald-400/40 hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center gap-2 cursor-pointer"
              >
                <span>Continue to Next Topic: {completionResult.next_topic_title || 'Next Lesson'}</span>
                <ArrowRight className="w-5 h-5" />
              </button>
            ) : null}

            <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
              <QuickReferenceButton topicSlug={topicSlug} variant="outline" label="Quick Reference Sheet" />
              <NavLink
                to={`/learn/${subjectSlug}`}
                className="w-full sm:w-auto px-6 py-2.5 rounded-xl text-xs font-bold bg-purple-950/60 border border-purple-500/30 text-slate-200 hover:text-white transition-all flex items-center justify-center gap-2"
              >
                <span>Curriculum Roadmap</span>
              </NavLink>
              <button
                type="button"
                onClick={() => {
                  setViewMode('study');
                  setActiveSectionIdx(0);
                }}
                className="w-full sm:w-auto px-5 py-2.5 rounded-xl text-xs font-semibold text-slate-400 hover:text-slate-200 transition-colors"
              >
                Review Material
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
