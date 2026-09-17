import React, { useState, useEffect } from 'react';
import { Award, Lock, Sparkles, CheckCircle2, Zap, Loader2 } from 'lucide-react';
import api from '../services/api';

export default function AchievementsPage() {
  const [achievements, setAchievements] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get('/achievements')
      .then((res) => setAchievements(res.data))
      .catch((err) => console.error('Error fetching achievements:', err))
      .finally(() => setLoading(false));
  }, []);

  const unlockedCount = achievements.filter((a) => a.is_unlocked).length;

  if (loading) {
    return (
      <div className="py-24 flex flex-col items-center justify-center gap-3 text-purple-300">
        <Loader2 className="w-8 h-8 animate-spin text-cyan-400" />
        <span className="text-sm">Loading achievement trophy room...</span>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 text-xs font-bold text-yellow-400 uppercase tracking-wider mb-1">
          <Award className="w-4 h-4" />
          <span>Hall of Trophies</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          Badges & Achievements
        </h1>
        <p className="text-xs sm:text-sm text-purple-300/70 mt-1">
          Milestones earned across your streaks, concept mastery, boss challenges, and AI tutor inquiries.
        </p>
      </div>

      {/* Trophies Summary */}
      <div className="card-orbit p-6 border-purple-500/25 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div>
          <div className="text-xs font-bold text-cyan-400 uppercase tracking-wider mb-1">
            Unlocked Badges
          </div>
          <div className="text-2xl font-black text-white">
            {unlockedCount} of {achievements.length} Achievements
          </div>
        </div>

        <div className="w-full sm:w-64 h-3 rounded-full bg-purple-950/80 border border-purple-500/20 overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-yellow-500 to-amber-400 rounded-full transition-all duration-700"
            style={{ width: `${(unlockedCount / max(1, achievements.length)) * 100}%` }}
          />
        </div>
      </div>

      {/* Badges Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        {achievements.map((a) => {
          return (
            <div
              key={a.id}
              className={`card-orbit p-6 border transition-all flex flex-col justify-between ${
                a.is_unlocked
                  ? 'border-yellow-500/30 bg-gradient-to-br from-[#1b1236] to-[#120b29]'
                  : 'border-purple-500/10 opacity-60 bg-[#0d071e]'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div
                    className={`w-14 h-14 rounded-2xl flex items-center justify-center text-3xl border ${
                      a.is_unlocked
                        ? 'bg-amber-500/20 border-yellow-400/40 text-yellow-300 shadow-lg shadow-amber-500/20'
                        : 'bg-purple-950/40 border-purple-500/20 text-slate-500'
                    }`}
                  >
                    {a.icon || '🏆'}
                  </div>

                  <div className="flex items-center gap-1.5 text-xs text-amber-300 font-semibold">
                    <Zap className="w-3.5 h-3.5 text-amber-400" />
                    <span>+{a.xp_reward} XP</span>
                  </div>
                </div>

                <h3 className="text-base font-bold text-white mb-1 flex items-center gap-2">
                  <span>{a.title}</span>
                  {a.is_unlocked ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  ) : (
                    <Lock className="w-3.5 h-3.5 text-slate-500" />
                  )}
                </h3>
                <p className="text-xs text-slate-300/70 leading-relaxed mb-4">{a.description}</p>
              </div>

              <div className="pt-3 border-t border-purple-500/15 flex items-center justify-between text-[11px]">
                <span className="text-purple-300/50 uppercase tracking-wider font-semibold">
                  {a.category}
                </span>
                <span
                  className={
                    a.is_unlocked ? 'text-emerald-400 font-semibold' : 'text-slate-500 font-medium'
                  }
                >
                  {a.is_unlocked ? 'Unlocked ✓' : 'Locked'}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function max(a, b) {
  return a > b ? a : b;
}
