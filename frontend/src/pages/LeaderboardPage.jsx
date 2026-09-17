import React, { useState, useEffect } from 'react';
import {
  Users, Trophy, Medal, Flame, Zap, Brain, School, Globe, Loader2
} from 'lucide-react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function LeaderboardPage() {
  const { user } = useAuth();
  const [timeframe, setTimeframe] = useState('weekly');
  const [category, setCategory] = useState('global');
  const [leaderboardUsers, setLeaderboardUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLeaderboard();
  }, [timeframe, category]);

  const fetchLeaderboard = () => {
    setLoading(true);
    api
      .get(`/leaderboard?timeframe=${timeframe}&category=${category}`)
      .then((res) => setLeaderboardUsers(res.data.users || []))
      .catch((err) => console.error('Error fetching leaderboard:', err))
      .finally(() => setLoading(false));
  };

  const getRankBadge = (rank) => {
    if (rank === 1) return <span className="text-xl">🥇</span>;
    if (rank === 2) return <span className="text-xl">🥈</span>;
    if (rank === 3) return <span className="text-xl">🥉</span>;
    return (
      <span className="w-7 h-7 rounded-lg bg-purple-950/60 border border-purple-500/20 text-purple-300 flex items-center justify-center text-xs font-bold">
        {rank}
      </span>
    );
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-200 max-w-5xl mx-auto">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 text-xs font-bold text-cyan-400 uppercase tracking-wider mb-1">
          <Trophy className="w-4 h-4" />
          <span>Community Standings</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          Orbit Leaderboard
        </h1>
        <p className="text-xs sm:text-sm text-purple-300/70 mt-1">
          Compete against peer engineers across your campus and worldwide as you solve lessons and earn XP.
        </p>
      </div>

      {/* Filter Tabs */}
      <div className="card-orbit p-3 border-purple-500/20 flex flex-col sm:flex-row items-center justify-between gap-3">
        {/* Timeframe Tabs */}
        <div className="flex items-center gap-1.5 p-1 rounded-xl bg-[#0e0824] border border-purple-500/20 w-full sm:w-auto">
          {[
            { id: 'weekly', label: 'Weekly' },
            { id: 'monthly', label: 'Monthly' },
            { id: 'all_time', label: 'All Time' },
          ].map((t) => (
            <button
              key={t.id}
              type="button"
              onClick={() => setTimeframe(t.id)}
              className={`flex-1 sm:flex-none px-4 py-1.5 rounded-lg text-xs font-bold transition-all ${
                timeframe === t.id
                  ? 'bg-purple-600 text-white shadow-md'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>

        {/* Scope Tabs */}
        <div className="flex items-center gap-1.5 p-1 rounded-xl bg-[#0e0824] border border-purple-500/20 w-full sm:w-auto">
          {[
            { id: 'global', label: 'Global', icon: Globe },
            { id: 'college', label: 'My College', icon: School },
          ].map((c) => {
            const Icon = c.icon;
            return (
              <button
                key={c.id}
                type="button"
                onClick={() => setCategory(c.id)}
                className={`flex-1 sm:flex-none px-3.5 py-1.5 rounded-lg text-xs font-bold flex items-center justify-center gap-1.5 transition-all ${
                  category === c.id
                    ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/30'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{c.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Leaderboard Table Card */}
      <div className="card-orbit border-purple-500/20 overflow-hidden">
        {loading ? (
          <div className="py-24 flex flex-col items-center justify-center gap-3 text-purple-300">
            <Loader2 className="w-8 h-8 animate-spin text-cyan-400" />
            <span className="text-sm">Calculating rankings...</span>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-purple-500/20 bg-purple-950/40 text-[11px] font-bold text-purple-300/70 uppercase tracking-wider">
                  <th className="py-3.5 px-4 text-center w-16">Rank</th>
                  <th className="py-3.5 px-4">Student</th>
                  <th className="py-3.5 px-4 text-center">Level</th>
                  <th className="py-3.5 px-4 text-center">Streak</th>
                  <th className="py-3.5 px-4 text-center">Mastery</th>
                  <th className="py-3.5 px-4 text-right">Total XP</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-purple-500/10 text-xs">
                {leaderboardUsers.map((u) => {
                  const isCurrentUser = user?.id === u.user_id;

                  return (
                    <tr
                      key={u.user_id}
                      className={`transition-colors ${
                        isCurrentUser
                          ? 'bg-purple-600/15 border-l-2 border-cyan-400 font-semibold'
                          : 'hover:bg-purple-950/30'
                      }`}
                    >
                      <td className="py-3.5 px-4 text-center flex items-center justify-center">
                        {getRankBadge(u.rank)}
                      </td>
                      <td className="py-3.5 px-4">
                        <div className="flex items-center gap-3">
                          <img
                            src={u.avatar_url || 'https://api.dicebear.com/7.x/bottts/svg?seed=Peer'}
                            alt="Avatar"
                            className="w-8 h-8 rounded-full bg-purple-950/60 ring-1 ring-purple-500/30"
                          />
                          <div>
                            <div className="font-bold text-slate-100 flex items-center gap-1.5">
                              <span>{u.full_name}</span>
                              {isCurrentUser && (
                                <span className="px-1.5 py-0.5 rounded bg-cyan-500/20 text-cyan-300 text-[10px] font-bold">
                                  You
                                </span>
                              )}
                            </div>
                            <div className="text-[11px] text-slate-400">{u.college}</div>
                          </div>
                        </div>
                      </td>
                      <td className="py-3.5 px-4 text-center">
                        <span className="px-2 py-0.5 rounded bg-purple-500/20 text-purple-200 font-bold">
                          Lvl {u.level}
                        </span>
                      </td>
                      <td className="py-3.5 px-4 text-center">
                        <span className="inline-flex items-center gap-1 text-amber-300 font-bold">
                          <Flame className="w-3.5 h-3.5 text-amber-400" />
                          <span>{u.streak}d</span>
                        </span>
                      </td>
                      <td className="py-3.5 px-4 text-center">
                        <span className="text-emerald-400 font-bold">{u.mastery_score}%</span>
                      </td>
                      <td className="py-3.5 px-4 text-right">
                        <span className="text-cyan-300 font-extrabold text-sm">
                          {u.xp.toLocaleString()} XP
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
