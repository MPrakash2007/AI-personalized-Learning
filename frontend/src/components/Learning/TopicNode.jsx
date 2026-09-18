import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Check, Lock, Sparkles, Star, Crown, Play, BookOpen } from 'lucide-react';
import QuickReferenceModal from './QuickReferenceModal';

export default function TopicNode({ topic, subjectSlug, isBoss, index, isAlternate }) {
  const [hovered, setHovered] = useState(false);
  const [showQuickRef, setShowQuickRef] = useState(false);
  const [shake, setShake] = useState(false);
  const navigate = useNavigate();

  const status = topic.progress?.status || (topic.is_accessible === false ? 'UPCOMING' : 'AVAILABLE');
  const mastery = topic.progress?.mastery_score || 0;
  const isCompleted = status === 'COMPLETED' || status === 'MASTERED';
  const isUpcoming = status === 'UPCOMING' || (!isCompleted && topic.is_accessible === false);
  const isAvailable = !isUpcoming;

  const handleClick = (e) => {
    e.preventDefault();
    if (isUpcoming) {
      setShake(true);
      setTimeout(() => setShake(false), 500);
      return;
    }
    navigate(`/learn/${subjectSlug}/${topic.slug}`);
  };

  // Node visual attributes by status
  let nodeBg = '';
  let NodeIcon = Play;
  let glowClass = '';

  if (isBoss) {
    if (isCompleted) {
      nodeBg = 'bg-gradient-to-tr from-amber-600 to-yellow-400 border-yellow-300 text-slate-950 font-bold shadow-xl shadow-amber-500/40';
      NodeIcon = Crown;
      glowClass = 'ring-4 ring-amber-400/50 animate-pulse';
    } else if (isUpcoming) {
      nodeBg = 'bg-[#140b28] border-amber-500/20 text-amber-500/40 opacity-60 shadow-inner';
      NodeIcon = Lock;
    } else {
      nodeBg = 'bg-gradient-to-tr from-purple-800 to-amber-700 border-amber-400 text-amber-200 shadow-xl shadow-amber-500/30';
      NodeIcon = Crown;
      glowClass = 'ring-2 ring-amber-400/40';
    }
  } else if (status === 'MASTERED' || mastery >= 85) {
    nodeBg = 'bg-gradient-to-tr from-yellow-500 to-amber-400 border-amber-300 text-slate-950 shadow-lg shadow-amber-500/30';
    NodeIcon = Star;
    glowClass = 'ring-2 ring-yellow-400/50';
  } else if (isCompleted) {
    // Completed != Locked: Always accessible with emerald check
    nodeBg = 'bg-gradient-to-tr from-emerald-600 to-teal-400 border-emerald-300 text-white shadow-lg shadow-emerald-500/30';
    NodeIcon = Check;
  } else if (status === 'IN_PROGRESS') {
    nodeBg = 'bg-gradient-to-tr from-purple-600 to-cyan-500 border-cyan-300 text-white shadow-xl shadow-cyan-500/40';
    NodeIcon = Sparkles;
    glowClass = 'ring-4 ring-cyan-400/40 animate-pulse';
  } else if (isUpcoming) {
    // UPCOMING: Muted purple/gray, lock icon, disabled appearance
    nodeBg = 'bg-[#100924] border-purple-900/30 text-purple-400/40 shadow-inner opacity-65 cursor-not-allowed';
    NodeIcon = Lock;
  } else {
    // AVAILABLE: Cyan glow, play icon, bright interactive button
    nodeBg = 'bg-[#180f33] border-cyan-400/80 text-cyan-300 hover:border-cyan-300 hover:text-white shadow-lg shadow-cyan-500/20';
    NodeIcon = Play;
    glowClass = 'ring-2 ring-cyan-400/30 hover:ring-cyan-400/60';
  }

  return (
    <>
      <div className="relative flex flex-col items-center group my-3 sm:my-5">
        {/* Node Interactive Button */}
        <button
          type="button"
          onClick={handleClick}
          onMouseEnter={() => setHovered(true)}
          onMouseLeave={() => setHovered(false)}
          className={`w-14 h-14 sm:w-16 sm:h-16 rounded-full border-2 flex items-center justify-center transition-all duration-300 transform ${
            isUpcoming
              ? 'cursor-not-allowed group-hover:scale-100'
              : 'group-hover:scale-110 active:scale-95 cursor-pointer'
          } ${nodeBg} ${glowClass} ${shake ? 'animate-bounce' : ''}`}
          aria-label={`Topic: ${topic.title} (${status})`}
          disabled={false}
        >
          <NodeIcon className="w-6 h-6 sm:w-7 sm:h-7" />
        </button>

        {/* Topic Title Label */}
        <div className="mt-2 text-center max-w-[140px] sm:max-w-[170px]">
          <span
            className={`text-xs sm:text-sm font-semibold block truncate ${
              isUpcoming
                ? 'text-slate-500'
                : 'text-slate-200 group-hover:text-cyan-300'
            }`}
          >
            {topic.title}
          </span>
          <span className="text-[10px] block font-medium uppercase tracking-wider">
            {isUpcoming ? (
              <span className="text-purple-400/50 flex items-center justify-center gap-1">
                <Lock className="w-2.5 h-2.5" /> Upcoming
              </span>
            ) : isBoss ? (
              <span className="text-amber-300">👑 Boss Challenge</span>
            ) : isCompleted ? (
              <span className="text-emerald-400">✓ Completed ({mastery}%)</span>
            ) : (
              <span className="text-cyan-400">Available</span>
            )}
          </span>
        </div>

        {/* Interactive Tooltip Card */}
        {hovered && (
          <div className="absolute bottom-full mb-3 z-30 w-64 p-3.5 rounded-2xl bg-[#130b2c] border border-purple-500/40 shadow-2xl shadow-purple-950/90 text-left pointer-events-auto animate-in fade-in zoom-in-95 duration-200">
            <div className="flex items-center justify-between gap-1 mb-1">
              <span className="text-xs font-bold text-white truncate">{topic.title}</span>
              {isUpcoming ? (
                <span className="px-1.5 py-0.5 rounded bg-purple-950/80 border border-purple-500/20 text-[9px] font-bold text-purple-300 uppercase">
                  Locked
                </span>
              ) : isCompleted ? (
                <span className="px-1.5 py-0.5 rounded bg-emerald-950/80 border border-emerald-500/30 text-[9px] font-bold text-emerald-300 uppercase">
                  Unlocked
                </span>
              ) : (
                <span className="px-1.5 py-0.5 rounded bg-cyan-950/80 border border-cyan-500/30 text-[9px] font-bold text-cyan-300 uppercase">
                  Ready
                </span>
              )}
            </div>

            <div className="text-[11px] text-slate-300/80 mb-3 line-clamp-2">
              {topic.description || 'Interactive engineering curriculum module.'}
            </div>

            {isUpcoming ? (
              <div className="p-2 rounded-xl bg-purple-950/40 border border-purple-500/20 text-[10px] text-purple-300/90 flex items-center gap-1.5">
                <Lock className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                <span>Complete previous topic to continue.</span>
              </div>
            ) : (
              <div className="space-y-1.5 text-[10px]">
                <div className="flex justify-between text-slate-400">
                  <span>Status:</span>
                  <span className="font-semibold text-cyan-300 capitalize">
                    {status.toLowerCase().replace('_', ' ')}
                  </span>
                </div>
                <div className="flex justify-between text-slate-400">
                  <span>Mastery:</span>
                  <span className="font-semibold text-emerald-400">{mastery}%</span>
                </div>
              </div>
            )}

            {/* Quick Reference Button inside Tooltip */}
            <div className="mt-3 pt-2.5 border-t border-purple-500/20 flex items-center justify-between gap-2">
              <button
                type="button"
                onClick={(e) => {
                  e.stopPropagation();
                  setShowQuickRef(true);
                }}
                className="w-full py-1.5 px-2.5 rounded-lg bg-purple-950/60 border border-purple-500/30 text-[10px] font-bold text-cyan-300 hover:text-white hover:border-cyan-400 transition-colors flex items-center justify-center gap-1"
              >
                <BookOpen className="w-3 h-3" />
                <span>Quick Reference</span>
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Quick Reference Sheet Modal */}
      <QuickReferenceModal
        topicSlug={topic.slug}
        isOpen={showQuickRef}
        onClose={() => setShowQuickRef(false)}
        onStartQuiz={isAvailable ? () => navigate(`/learn/${subjectSlug}/${topic.slug}`) : null}
      />
    </>
  );
}
