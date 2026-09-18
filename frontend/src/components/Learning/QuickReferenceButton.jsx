import React, { useState } from 'react';
import { BookOpen, Sparkles } from 'lucide-react';
import QuickReferenceModal from './QuickReferenceModal';

export default function QuickReferenceButton({
  topicSlug,
  variant = 'outline',
  className = '',
  label = 'Quick Reference',
  onStartQuiz
}) {
  const [isOpen, setIsOpen] = useState(false);

  let variantStyles = '';
  if (variant === 'primary') {
    variantStyles = 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white border-purple-400/40 shadow-lg shadow-purple-600/30 hover:scale-105';
  } else if (variant === 'pill') {
    variantStyles = 'bg-purple-950/60 border-purple-500/30 text-cyan-300 hover:border-cyan-400 hover:text-white';
  } else if (variant === 'compact') {
    variantStyles = 'p-2 bg-purple-950/40 border-purple-500/20 text-purple-300 hover:text-cyan-300 hover:border-cyan-400/50';
  } else {
    // outline
    variantStyles = 'bg-[#12082b] border-cyan-500/30 text-cyan-300 hover:border-cyan-400 hover:text-white hover:bg-cyan-500/10 shadow-md shadow-purple-950/40';
  }

  return (
    <>
      <button
        type="button"
        onClick={(e) => {
          e.stopPropagation();
          setIsOpen(true);
        }}
        className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border text-xs font-bold transition-all active:scale-95 cursor-pointer ${variantStyles} ${className}`}
        title="View University Quick Reference Sheet"
        aria-label="Open Exam Quick Reference"
      >
        <BookOpen className="w-3.5 h-3.5" />
        <span>{label}</span>
      </button>

      <QuickReferenceModal
        topicSlug={topicSlug}
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
        onStartQuiz={onStartQuiz}
      />
    </>
  );
}
