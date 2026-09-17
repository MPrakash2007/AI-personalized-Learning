import React, { useState, useEffect } from 'react';
import { Bot, Sparkles, X, CheckCircle2, AlertTriangle, ArrowRight, Loader2 } from 'lucide-react';
import api from '../../services/api';

export default function MistakeExplainerModal({
  isOpen,
  onClose,
  questionId,
  userAnswer,
  correctAnswer,
  onTrySimilar,
}) {
  const [loading, setLoading] = useState(true);
  const [explanation, setExplanation] = useState(null);

  useEffect(() => {
    if (isOpen && questionId) {
      setLoading(true);
      api
        .post('/ai/explain-mistake', {
          question_id: questionId,
          user_answer: userAnswer || 'Option',
        })
        .then((res) => setExplanation(res.data))
        .catch((err) => {
          console.error('Explain mistake error:', err);
          setExplanation({
            why_wrong: `You selected "${userAnswer}". This choice is often confused with this concept because it deals with adjacent system states.`,
            core_concept: `The correct answer is "${correctAnswer}". Review the underlying invariant and dependencies.`,
            real_world_example: 'In distributed systems or relational engines, operations must be strictly ordered to prevent dirty reads or undefined states.',
            similar_question: null,
          });
        })
        .finally(() => setLoading(false));
    }
  }, [isOpen, questionId, userAnswer, correctAnswer]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-md">
      <div className="w-full max-w-xl bg-[#120b29] border border-purple-500/30 rounded-2xl shadow-2xl p-6 relative max-h-[90vh] overflow-y-auto">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-white p-1 rounded-lg transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Header */}
        <div className="flex items-center gap-3 mb-5">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-pink-500 to-purple-600 flex items-center justify-center text-white shadow-lg shadow-purple-500/30">
            <Bot className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              CodeOrbit AI Explanation
              <Sparkles className="w-4 h-4 text-pink-400" />
            </h3>
            <p className="text-xs text-purple-300/60">Deconstructing your concept misconception</p>
          </div>
        </div>

        {loading ? (
          <div className="py-12 flex flex-col items-center justify-center gap-3 text-purple-300">
            <Loader2 className="w-8 h-8 animate-spin text-cyan-400" />
            <span className="text-xs font-medium">Analyzing mistake & formulating breakdown...</span>
          </div>
        ) : (
          <div className="space-y-4 text-sm">
            {/* Why Wrong Box */}
            <div className="p-3.5 rounded-xl bg-rose-950/40 border border-rose-500/30 text-rose-200">
              <div className="flex items-center gap-2 font-semibold text-rose-300 mb-1">
                <AlertTriangle className="w-4 h-4" />
                <span>Why your choice didn't work</span>
              </div>
              <p className="text-xs leading-relaxed">{explanation?.why_wrong}</p>
            </div>

            {/* Core Concept */}
            <div className="p-3.5 rounded-xl bg-emerald-950/40 border border-emerald-500/30 text-emerald-200">
              <div className="flex items-center gap-2 font-semibold text-emerald-300 mb-1">
                <CheckCircle2 className="w-4 h-4" />
                <span>The Correct Principle</span>
              </div>
              <p className="text-xs leading-relaxed">{explanation?.core_concept}</p>
            </div>

            {/* Real World Example */}
            {explanation?.real_world_example && (
              <div className="p-3.5 rounded-xl bg-purple-950/40 border border-purple-500/20 text-purple-200">
                <div className="font-semibold text-purple-300 text-xs mb-1 uppercase tracking-wider">
                  💡 Engineering Analogy
                </div>
                <p className="text-xs leading-relaxed text-slate-300">
                  {explanation.real_world_example}
                </p>
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex items-center justify-end gap-3 pt-3 border-t border-purple-500/15">
              <button
                onClick={onClose}
                className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-300 hover:text-white hover:bg-purple-950/40 transition-colors"
              >
                Got It
              </button>
              {explanation?.similar_question && onTrySimilar && (
                <button
                  onClick={() => {
                    onClose();
                    onTrySimilar(explanation.similar_question);
                  }}
                  className="px-4 py-2 rounded-xl text-xs font-semibold bg-gradient-to-r from-purple-600 to-indigo-600 text-white flex items-center gap-1.5 shadow-lg shadow-purple-600/30 hover:opacity-90 transition-opacity"
                >
                  <span>Try Similar Question</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
