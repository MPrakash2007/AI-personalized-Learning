import React, { useState } from 'react';
import confetti from 'canvas-confetti';
import {
  CheckCircle2, XCircle, Bot, ArrowRight, Zap, Code, Sparkles, HelpCircle
} from 'lucide-react';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { useToast } from '../../context/ToastContext';
import MistakeExplainerModal from './MistakeExplainerModal';

export default function InteractiveTask({ question, topicId, onCompleteNext }) {
  const [selectedAnswer, setSelectedAnswer] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showMistakeModal, setShowMistakeModal] = useState(false);
  const [similarQuestion, setSimilarQuestion] = useState(null);

  const { updateUser } = useAuth();
  const toast = useToast();

  const currentQ = similarQuestion || question;

  const handleSubmit = async () => {
    if (!selectedAnswer || submitted || loading) return;

    setLoading(true);
    try {
      const res = await api.post('/attempts/submit', {
        question_id: currentQ.id,
        topic_id: topicId,
        selected_answer: selectedAnswer,
        time_taken_seconds: 12,
      });

      setResult(res.data);
      setSubmitted(true);

      // Update user state live in Auth context
      updateUser({
        xp: res.data.new_xp,
        level: res.data.new_level,
        streak: { current_streak: res.data.current_streak },
      });

      if (res.data.is_correct) {
        toast.xp(`+${res.data.xp_earned} XP earned! Topic Mastery: ${res.data.topic_mastery}%`);
        // Trigger celebratory confetti
        confetti({
          particleCount: 50,
          spread: 60,
          origin: { y: 0.8 },
          colors: ['#8b5cf6', '#06b6d4', '#10b981', '#ec4899'],
        });
      } else {
        toast.error('Not quite! Check the explanation below.');
      }
    } catch (err) {
      console.error('Failed to submit question attempt:', err);
      toast.error('Failed to evaluate answer. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleNext = () => {
    setSelectedAnswer('');
    setSubmitted(false);
    setResult(null);
    setSimilarQuestion(null);
    if (onCompleteNext) onCompleteNext(result?.is_correct || false, result?.xp_earned || 0);
  };

  const handleTrySimilar = (similarData) => {
    if (!similarData) return;
    setSimilarQuestion({
      id: currentQ.id,
      prompt: similarData.prompt,
      question_type: 'mcq',
      difficulty: 'MEDIUM',
      explanation: similarData.explanation,
      options: similarData.options.map((opt, i) => ({
        id: i + 100,
        text: opt.text,
        is_correct: opt.is_correct,
        order: i + 1,
      })),
    });
    setSelectedAnswer('');
    setSubmitted(false);
    setResult(null);
  };

  return (
    <div className="card-orbit p-6 max-w-2xl mx-auto space-y-6">
      {/* Question Header & Difficulty */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="px-2.5 py-1 rounded-lg bg-purple-500/20 text-purple-300 font-bold text-[11px] uppercase tracking-wider">
            {currentQ.question_type.replace('_', ' ')}
          </span>
          <span
            className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
              currentQ.difficulty === 'HARD'
                ? 'bg-rose-500/20 text-rose-300'
                : currentQ.difficulty === 'EASY'
                ? 'bg-emerald-500/20 text-emerald-300'
                : 'bg-amber-500/20 text-amber-300'
            }`}
          >
            {currentQ.difficulty}
          </span>
        </div>

        <div className="flex items-center gap-1.5 text-xs text-cyan-300 font-semibold">
          <Zap className="w-3.5 h-3.5 text-cyan-400" />
          <span>+{currentQ.xp_reward || 10} XP</span>
        </div>
      </div>

      {/* Prompt */}
      <div className="text-base sm:text-lg font-semibold text-slate-100 leading-relaxed">
        {currentQ.prompt}
      </div>

      {/* Optional Code Snippet */}
      {currentQ.code_snippet && (
        <div className="p-4 rounded-xl bg-[#090514] border border-purple-500/25 font-mono text-xs text-purple-200 overflow-x-auto">
          <pre>{currentQ.code_snippet}</pre>
        </div>
      )}

      {/* Options List */}
      <div className="space-y-2.5">
        {currentQ.options &&
          currentQ.options.map((option, idx) => {
            const isSelected = selectedAnswer === option.text;
            let optionStyles =
              'bg-purple-950/30 border-purple-500/20 text-slate-200 hover:border-purple-400/50 hover:bg-purple-900/30';

            if (submitted) {
              if (option.text === result?.correct_answer) {
                optionStyles = 'bg-emerald-950/60 border-emerald-500 text-emerald-100';
              } else if (isSelected && !result?.is_correct) {
                optionStyles = 'bg-rose-950/60 border-rose-500 text-rose-100';
              } else {
                optionStyles = 'bg-purple-950/20 border-purple-500/10 text-slate-500 opacity-60';
              }
            } else if (isSelected) {
              optionStyles =
                'bg-purple-600/30 border-cyan-400 text-white shadow-lg shadow-purple-950/50 ring-1 ring-cyan-400';
            }

            return (
              <button
                key={option.id || idx}
                type="button"
                disabled={submitted || loading}
                onClick={() => setSelectedAnswer(option.text)}
                className={`w-full p-4 rounded-xl border text-left text-sm font-medium transition-all flex items-center justify-between ${optionStyles}`}
              >
                <div className="flex items-center gap-3">
                  <span className="w-6 h-6 rounded-lg bg-purple-900/40 text-purple-300 flex items-center justify-center text-xs font-bold border border-purple-500/20">
                    {String.fromCharCode(65 + idx)}
                  </span>
                  <span>{option.text}</span>
                </div>

                {submitted && option.text === result?.correct_answer && (
                  <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
                )}
                {submitted && isSelected && !result?.is_correct && (
                  <XCircle className="w-5 h-5 text-rose-400 shrink-0" />
                )}
              </button>
            );
          })}
      </div>

      {/* Post-Submission Feedback Box */}
      {submitted && result && (
        <div
          className={`p-4 rounded-xl border animate-in fade-in slide-in-from-bottom-2 duration-300 ${
            result.is_correct
              ? 'bg-emerald-950/40 border-emerald-500/40 text-emerald-200'
              : 'bg-rose-950/40 border-rose-500/40 text-rose-200'
          }`}
        >
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2 font-bold text-sm">
              {result.is_correct ? (
                <>
                  <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                  <span>✓ Correct! +{result.xp_earned} XP</span>
                </>
              ) : (
                <>
                  <XCircle className="w-5 h-5 text-rose-400" />
                  <span>✕ Not quite.</span>
                </>
              )}
            </div>

            {!result.is_correct && (
              <button
                onClick={() => setShowMistakeModal(true)}
                className="px-3 py-1 rounded-lg bg-purple-600/40 hover:bg-purple-600/60 border border-purple-400/40 text-xs font-semibold text-purple-200 flex items-center gap-1.5 transition-colors"
              >
                <Bot className="w-3.5 h-3.5 text-pink-400" />
                <span>Explain My Mistake</span>
              </button>
            )}
          </div>

          <p className="text-xs leading-relaxed text-slate-300 mb-3">{result.explanation}</p>

          <div className="text-[11px] text-purple-300/80 font-semibold">
            Topic Mastery: {result.topic_mastery}%{' '}
            {result.mastery_change > 0 && `(+${result.mastery_change}%)`}
          </div>
        </div>
      )}

      {/* Primary Action Button */}
      <div className="pt-2 flex justify-end">
        {!submitted ? (
          <button
            type="button"
            disabled={!selectedAnswer || loading}
            onClick={handleSubmit}
            className="px-6 py-2.5 rounded-xl font-bold text-sm bg-gradient-to-r from-purple-600 via-indigo-600 to-cyan-500 text-white shadow-lg shadow-purple-600/30 hover:shadow-purple-500/50 hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-40 disabled:pointer-events-none"
          >
            {loading ? 'Evaluating...' : 'Check Answer'}
          </button>
        ) : (
          <button
            type="button"
            onClick={handleNext}
            className="px-6 py-2.5 rounded-xl font-bold text-sm bg-gradient-to-r from-emerald-600 to-teal-500 text-white shadow-lg shadow-emerald-600/30 hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center gap-2"
          >
            <span>Continue</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        )}
      </div>

      {/* Mistake Explainer AI Modal */}
      <MistakeExplainerModal
        isOpen={showMistakeModal}
        onClose={() => setShowMistakeModal(false)}
        questionId={currentQ.id}
        userAnswer={selectedAnswer}
        correctAnswer={result?.correct_answer}
        onTrySimilar={handleTrySimilar}
      />
    </div>
  );
}
