import React, { useState, useEffect } from 'react';
import { Target, Zap, CheckCircle2, Award, Flame, Loader2 } from 'lucide-react';
import api from '../services/api';
import { useToast } from '../context/ToastContext';
import { useAuth } from '../context/AuthContext';

export default function DailyQuestsPage() {
  const [quests, setQuests] = useState([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();
  const toast = useToast();

  useEffect(() => {
    api
      .get('/quests/today')
      .then((res) => setQuests(res.data))
      .catch((err) => console.error('Failed to load quests:', err))
      .finally(() => setLoading(false));
  }, []);

  const totalRewards = quests.reduce((acc, q) => acc + q.xp_reward, 0);
  const completedCount = quests.filter((q) => q.is_completed).length;

  if (loading) {
    return (
      <div className="py-24 flex flex-col items-center justify-center gap-3 text-purple-300">
        <Loader2 className="w-8 h-8 animate-spin text-cyan-400" />
        <span className="text-sm">Loading daily quest missions...</span>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-200 max-w-4xl mx-auto">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 text-xs font-bold text-rose-400 uppercase tracking-wider mb-1">
          <Target className="w-4 h-4" />
          <span>Daily Training Regimen</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          Daily Quests
        </h1>
        <p className="text-xs sm:text-sm text-purple-300/70 mt-1">
          Complete daily engineering objectives to maintain your streak, level up faster, and claim bonus XP.
        </p>
      </div>

      {/* Quest Summary Banner */}
      <div className="card-orbit p-6 border-purple-500/25 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div>
          <div className="text-xs font-bold text-cyan-400 uppercase tracking-wider mb-1">
            Today's Progress
          </div>
          <div className="text-2xl font-black text-white">
            {completedCount} of {quests.length} Quests Completed
          </div>
        </div>

        <div className="flex items-center gap-4 text-xs font-semibold">
          <div className="flex items-center gap-1.5 text-amber-300">
            <Zap className="w-4 h-4 text-amber-400" />
            <span>Up to +{totalRewards} Bonus XP</span>
          </div>
          <div className="flex items-center gap-1.5 text-rose-300">
            <Flame className="w-4 h-4 text-rose-400" />
            <span>Streak Safe</span>
          </div>
        </div>
      </div>

      {/* Quests List */}
      <div className="space-y-4">
        {quests.map((q) => {
          const pct = Math.min(100, Math.round((q.current_count / q.target_count) * 100));

          return (
            <div
              key={q.id}
              className={`card-orbit p-6 border transition-all ${
                q.is_completed
                  ? 'border-emerald-500/40 bg-emerald-950/20'
                  : 'border-purple-500/20 hover:border-purple-500/40'
              }`}
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
                <div className="flex items-center gap-3">
                  <div
                    className={`w-10 h-10 rounded-xl flex items-center justify-center text-lg ${
                      q.is_completed
                        ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40'
                        : 'bg-purple-950/60 text-purple-300 border border-purple-500/25'
                    }`}
                  >
                    {q.is_completed ? <CheckCircle2 className="w-5 h-5" /> : <Target className="w-5 h-5" />}
                  </div>

                  <div>
                    <h3 className="text-base font-bold text-white">{q.title}</h3>
                    <p className="text-xs text-purple-300/60 capitalize">Type: {q.quest_type}</p>
                  </div>
                </div>

                <div className="flex items-center gap-3 self-end sm:self-center">
                  <span className="px-3 py-1 rounded-lg bg-amber-500/20 text-amber-300 font-bold text-xs flex items-center gap-1">
                    <Zap className="w-3.5 h-3.5" />
                    <span>+{q.xp_reward} XP</span>
                  </span>
                  {q.is_completed && (
                    <span className="px-2.5 py-1 rounded-lg bg-emerald-500/20 text-emerald-300 font-bold text-xs">
                      Claimed ✓
                    </span>
                  )}
                </div>
              </div>

              {/* Progress Bar */}
              <div className="space-y-1.5">
                <div className="flex justify-between text-xs text-slate-300 font-medium">
                  <span>Progress</span>
                  <span className="text-cyan-300 font-bold">
                    {q.current_count} / {q.target_count} ({pct}%)
                  </span>
                </div>
                <div className="w-full h-2 rounded-full bg-purple-950/80 border border-purple-500/20 overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${
                      q.is_completed ? 'bg-emerald-400' : 'bg-gradient-to-r from-purple-500 to-cyan-400'
                    }`}
                    style={{ width: `${pct}%` }}
                  />
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
