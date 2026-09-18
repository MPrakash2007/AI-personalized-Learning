import React, { useState, useEffect } from 'react';
import {
  X, BookOpen, AlertTriangle, Lightbulb, HelpCircle, ExternalLink,
  Zap, Brain, Code, Table, CheckCircle2, ChevronRight, Loader2, Sparkles, Target
} from 'lucide-react';
import api from '../../services/api';

export default function QuickReferenceModal({ topicSlug, isOpen, onClose, onStartQuiz }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('all');

  useEffect(() => {
    if (isOpen && topicSlug) {
      setLoading(true);
      setError(null);
      api
        .get(`/topics/${topicSlug}/quick-reference`)
        .then((res) => {
          setData(res.data);
        })
        .catch((err) => {
          console.error('Failed to load quick reference:', err);
          setError('Could not load quick reference sheet. Please try again.');
        })
        .finally(() => {
          setLoading(false);
        });
    }
  }, [isOpen, topicSlug]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 overflow-y-auto bg-black/80 backdrop-blur-md animate-in fade-in duration-200">
      <div
        className="relative w-full max-w-4xl bg-[#0e0722] border border-purple-500/30 rounded-3xl shadow-2xl shadow-purple-950/90 overflow-hidden flex flex-col max-h-[90vh] my-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal Header */}
        <div className="px-6 py-4 border-b border-purple-500/20 bg-gradient-to-r from-purple-950/60 via-[#150a33] to-cyan-950/60 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-cyan-500/20 border border-cyan-400/40 flex items-center justify-center text-cyan-300">
              <BookOpen className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-lg sm:text-xl font-black text-white">
                  {data?.title || 'Exam Quick Reference Sheet'}
                </h2>
                {data?.subject && (
                  <span className="px-2.5 py-0.5 rounded-full bg-purple-900/60 border border-purple-400/40 text-[10px] font-bold text-purple-200 uppercase">
                    {data.subject}
                  </span>
                )}
              </div>
              <p className="text-xs text-purple-300/70">
                High-yield summary, formulas, exam tips & university FAQs
              </p>
            </div>
          </div>

          <button
            type="button"
            onClick={onClose}
            className="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-purple-900/40 transition-colors"
            aria-label="Close modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto space-y-6 text-slate-200 text-sm leading-relaxed custom-scrollbar">
          {loading && (
            <div className="py-20 flex flex-col items-center justify-center gap-3 text-cyan-300">
              <Loader2 className="w-8 h-8 animate-spin" />
              <span className="text-xs font-semibold">Generating verified exam sheet...</span>
            </div>
          )}

          {error && (
            <div className="p-4 rounded-2xl bg-rose-950/40 border border-rose-500/30 text-rose-300 text-center">
              {error}
            </div>
          )}

          {!loading && !error && data && (
            <>
              {/* 1. Exam Definition & Remember Block */}
              <div className="p-5 rounded-2xl bg-gradient-to-br from-purple-950/40 to-[#12082b] border border-purple-500/30 space-y-3">
                <div className="flex items-center gap-2 text-xs font-bold text-cyan-400 uppercase tracking-wider">
                  <Brain className="w-4 h-4 text-cyan-400" />
                  <span>1. Formal Exam Definition</span>
                </div>
                <p className="text-sm font-medium text-slate-100 leading-relaxed">
                  {data.exam_definition}
                </p>

                {data.remember && (
                  <div className="p-3.5 rounded-xl bg-amber-950/30 border border-amber-500/40 text-amber-200 text-xs flex items-start gap-2.5">
                    <Sparkles className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                    <div>
                      <span className="font-bold text-amber-300">What to write in University Exam: </span>
                      {data.remember}
                    </div>
                  </div>
                )}
              </div>

              {/* 2. Key High-Scoring Points */}
              {data.key_points && data.key_points.length > 0 && (
                <div className="p-5 rounded-2xl bg-[#12082b] border border-purple-500/20 space-y-3">
                  <div className="flex items-center gap-2 text-xs font-bold text-purple-300 uppercase tracking-wider">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    <span>2. High-Yield Key Points</span>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {data.key_points.map((pt, idx) => (
                      <div
                        key={idx}
                        className="p-3 rounded-xl bg-purple-950/30 border border-purple-500/10 text-xs text-slate-300 flex items-start gap-2"
                      >
                        <span className="w-4 h-4 rounded-full bg-cyan-500/20 text-cyan-300 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">
                          {idx + 1}
                        </span>
                        <span>{pt}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* 3. Comparison Table */}
              {data.comparison && data.comparison.headers && (
                <div className="p-5 rounded-2xl bg-[#12082b] border border-purple-500/20 space-y-3">
                  <div className="flex items-center gap-2 text-xs font-bold text-indigo-300 uppercase tracking-wider">
                    <Table className="w-4 h-4 text-indigo-400" />
                    <span>3. Comparison Table ({data.comparison.title || 'Exam Comparison'})</span>
                  </div>
                  <div className="overflow-x-auto rounded-xl border border-purple-500/20">
                    <table className="w-full text-xs text-left border-collapse">
                      <thead>
                        <tr className="bg-purple-950/60 text-cyan-300 font-bold border-b border-purple-500/30">
                          {data.comparison.headers.map((h, hIdx) => (
                            <th key={hIdx} className="p-2.5">
                              {h}
                            </th>
                          ))}
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-purple-900/20 text-slate-300">
                        {data.comparison.rows?.map((row, rIdx) => (
                          <tr key={rIdx} className={rIdx % 2 === 0 ? 'bg-purple-950/20' : 'bg-transparent'}>
                            {row.map((cell, cIdx) => (
                              <td key={cIdx} className="p-2.5">
                                {cell}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* 4. Formulas / Rules */}
              {data.formulas && data.formulas.length > 0 && (
                <div className="p-5 rounded-2xl bg-[#12082b] border border-purple-500/20 space-y-3">
                  <div className="flex items-center gap-2 text-xs font-bold text-amber-300 uppercase tracking-wider">
                    <Zap className="w-4 h-4 text-amber-400" />
                    <span>4. Core Formulas & Mathematical Invariants</span>
                  </div>
                  <div className="space-y-2">
                    {data.formulas.map((form, idx) => (
                      <div
                        key={idx}
                        className="p-3 rounded-xl bg-[#090514] border border-amber-500/20 font-mono text-xs text-amber-200"
                      >
                        {form}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* 5. Exam Tip & Common Confusion */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {data.exam_tip && (
                  <div className="p-4 rounded-2xl bg-emerald-950/20 border border-emerald-500/30 space-y-2">
                    <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-400 uppercase tracking-wider">
                      <Lightbulb className="w-4 h-4 text-emerald-400" />
                      <span>🎯 Exam Scoring Tip</span>
                    </div>
                    <p className="text-xs text-slate-300 leading-relaxed">
                      {data.exam_tip}
                    </p>
                  </div>
                )}

                {data.common_confusion && (
                  <div className="p-4 rounded-2xl bg-rose-950/20 border border-rose-500/30 space-y-2">
                    <div className="flex items-center gap-1.5 text-xs font-bold text-rose-400 uppercase tracking-wider">
                      <AlertTriangle className="w-4 h-4 text-rose-400" />
                      <span>⚠️ Common Exam Confusion</span>
                    </div>
                    <div className="text-xs space-y-1 text-slate-300">
                      <div><strong className="text-rose-300">Mistake: </strong>{data.common_confusion.wrong}</div>
                      <div><strong className="text-emerald-300">Correction: </strong>{data.common_confusion.correct}</div>
                    </div>
                  </div>
                )}
              </div>

              {/* 6. University Exam FAQs */}
              {data.faqs && data.faqs.length > 0 && (
                <div className="p-5 rounded-2xl bg-[#12082b] border border-purple-500/20 space-y-3">
                  <div className="flex items-center gap-2 text-xs font-bold text-cyan-300 uppercase tracking-wider">
                    <HelpCircle className="w-4 h-4 text-cyan-400" />
                    <span>6. Frequently Asked Exam Questions (2, 5 & 10 Marks)</span>
                  </div>
                  <div className="space-y-3">
                    {data.faqs.map((faq, idx) => (
                      <div
                        key={idx}
                        className="p-3.5 rounded-xl bg-purple-950/30 border border-purple-500/20 space-y-1.5"
                      >
                        <div className="flex items-center justify-between text-xs">
                          <span className="font-bold text-white">Q: {faq.q}</span>
                          <span className="px-2 py-0.5 rounded-full bg-cyan-950 border border-cyan-500/30 text-[10px] font-bold text-cyan-300">
                            {faq.marks}
                          </span>
                        </div>
                        <p className="text-xs text-slate-300/90 leading-relaxed">
                          <strong>Answer: </strong>{faq.a}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* 7. 60-Second Last-Minute Revision */}
              {data.revision_60s && data.revision_60s.length > 0 && (
                <div className="p-5 rounded-2xl bg-gradient-to-r from-purple-950/50 to-indigo-950/50 border border-cyan-500/30 space-y-3">
                  <div className="flex items-center gap-2 text-xs font-bold text-cyan-300 uppercase tracking-wider">
                    <Zap className="w-4 h-4 text-amber-400" />
                    <span>7. ⚡ 60-Second Last-Minute Revision</span>
                  </div>
                  <ul className="space-y-2 text-xs text-slate-200">
                    {data.revision_60s.map((rev, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="text-cyan-400 font-bold">•</span>
                        <span>{rev}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* 8. Verified External References */}
              {data.references && data.references.length > 0 && (
                <div className="p-4 rounded-2xl bg-[#090514] border border-purple-500/20 space-y-2">
                  <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                    📚 Verified Academic Portals
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {data.references.map((ref, idx) => (
                      <a
                        key={idx}
                        href={ref.source_url}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-purple-950/40 border border-purple-500/30 text-xs font-medium text-cyan-300 hover:text-white hover:border-cyan-400 transition-all"
                      >
                        <span>{ref.title || ref.source_name}</span>
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </div>

        {/* Modal Footer */}
        <div className="px-6 py-4 border-t border-purple-500/20 bg-[#0c061d] flex items-center justify-between shrink-0">
          <span className="text-xs text-slate-400">
            Press <kbd className="px-1.5 py-0.5 bg-purple-950 border border-purple-500/30 rounded text-[10px] text-purple-300">Esc</kbd> to close
          </span>
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-xl text-xs font-bold bg-purple-950/60 border border-purple-500/30 text-slate-300 hover:text-white transition-all"
            >
              Close
            </button>
            {onStartQuiz && (
              <button
                type="button"
                onClick={() => {
                  onClose();
                  onStartQuiz();
                }}
                className="px-5 py-2 rounded-xl text-xs font-extrabold bg-gradient-to-r from-cyan-400 to-teal-400 text-slate-950 shadow-lg shadow-cyan-400/30 hover:scale-105 active:scale-95 transition-all flex items-center gap-1.5"
              >
                <Target className="w-3.5 h-3.5" />
                <span>Start Topic Quiz →</span>
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
