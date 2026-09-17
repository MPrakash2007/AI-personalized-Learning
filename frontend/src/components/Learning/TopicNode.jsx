import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Check, Lock, Sparkles, Star, Crown, Play } from 'lucide-react';

export default function TopicNode({ topic, subjectSlug, isBoss, index, isAlternate }) {
  const [hovered, setHovered] = useState(false);
  const navigate = useNavigate();

  const status = topic.progress?.status || (index === 0 ? 'AVAILABLE' : 'LOCKED');
  const mastery = topic.progress?.mastery_score || 0;
  const isLocked = status === 'LOCKED';

  const handleClick = () => {
    if (!isLocked) {
      navigate(`/learn/${subjectSlug}/${topic.slug}`);
    }
  };

  // Node visual attributes by status
  let nodeBg = 'bg-[#150e2e] border-purple-500/30 text-purple-300';
  let NodeIcon = Play;
  let glowClass = '';

  if (isBoss) {
    nodeBg = 'bg-gradient-to-tr from-amber-600 to-yellow-400 border-yellow-300 text-slate-950 font-bold shadow-xl shadow-amber-500/40';
    NodeIcon = Crown;
    glowClass = 'ring-4 ring-amber-400/30 animate-pulse';
  } else if (status === 'MASTERED' || mastery >= 85) {
    nodeBg = 'bg-gradient-to-tr from-yellow-500 to-amber-400 border-amber-300 text-slate-950 shadow-lg shadow-amber-500/30';
    NodeIcon = Star;
    glowClass = 'ring-2 ring-yellow-400/50';
  } else if (status === 'COMPLETED') {
    nodeBg = 'bg-gradient-to-tr from-emerald-600 to-teal-400 border-emerald-300 text-white shadow-lg shadow-emerald-500/30';
    NodeIcon = Check;
  } else if (status === 'IN_PROGRESS') {
    nodeBg = 'bg-gradient-to-tr from-purple-600 to-cyan-500 border-cyan-300 text-white shadow-xl shadow-cyan-500/40';
    NodeIcon = Sparkles;
    glowClass = 'ring-4 ring-cyan-400/40 animate-pulse';
  } else if (status === 'AVAILABLE') {
    nodeBg = 'bg-[#1e1342] border-cyan-400/60 text-cyan-300 hover:border-cyan-300 shadow-md shadow-purple-900/40';
    NodeIcon = Play;
  } else {
    // LOCKED
    nodeBg = 'bg-[#100a24]/80 border-purple-500/10 text-slate-500 cursor-not-allowed';
    NodeIcon = Lock;
  }

  return (
    <div className="relative flex flex-col items-center group my-3 sm:my-5">
      {/* Node Interactive Button */}
      <button
        type="button"
        onClick={handleClick}
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
        disabled={isLocked}
        className={`w-14 h-14 sm:w-16 sm:h-16 rounded-full border-2 flex items-center justify-center transition-all duration-300 transform group-hover:scale-110 active:scale-95 ${nodeBg} ${glowClass}`}
        aria-label={`Topic: ${topic.title} (${status})`}
      >
        <NodeIcon className={`w-6 h-6 sm:w-7 sm:h-7 ${status === 'IN_PROGRESS' ? 'animate-spin' : ''}`} />
      </button>

      {/* Topic Title Label */}
      <div className="mt-2 text-center max-w-[140px] sm:max-w-[170px]">
        <span
          className={`text-xs sm:text-sm font-semibold block truncate ${
            isLocked ? 'text-slate-500' : 'text-slate-200 group-hover:text-cyan-300'
          }`}
        >
          {topic.title}
        </span>
        <span className="text-[10px] text-purple-300/50 block font-medium uppercase tracking-wider">
          {isBoss ? '👑 Boss Challenge' : `${mastery}% Mastery`}
        </span>
      </div>

      {/* Interactive Tooltip Card */}
      {hovered && (
        <div className="absolute bottom-full mb-3 z-30 w-56 p-3 rounded-xl bg-[#130b2c] border border-purple-500/40 shadow-2xl shadow-purple-950/90 text-left pointer-events-none animate-in fade-in zoom-in-95 duration-200">
          <div className="text-xs font-bold text-white mb-1">{topic.title}</div>
          <div className="text-[11px] text-slate-300/80 mb-2.5 line-clamp-2">
            {topic.description || 'Interactive engineering lesson module.'}
          </div>
          <div className="space-y-1.5 text-[10px]">
            <div className="flex justify-between text-slate-400">
              <span>Status:</span>
              <span className="font-semibold text-cyan-300 capitalize">{status.toLowerCase().replace('_', ' ')}</span>
            </div>
            <div className="flex justify-between text-slate-400">
              <span>Mastery:</span>
              <span className="font-semibold text-emerald-400">{mastery}%</span>
            </div>
            <div className="flex justify-between text-slate-400">
              <span>Questions:</span>
              <span className="font-semibold text-slate-200">{topic.questions_count || 6} Questions</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
