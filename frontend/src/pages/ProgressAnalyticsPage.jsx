import React, { useState, useEffect } from 'react';
import {
  TrendingUp, Brain, Award, Zap, Flame, CheckCircle2, Target,
  AlertTriangle, ArrowRight, Loader2
} from 'lucide-react';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  BarChart, Bar
} from 'recharts';
import api from '../services/api';
import { NavLink } from 'react-router-dom';

export default function ProgressAnalyticsPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get('/progress/overview')
      .then((res) => setData(res.data))
      .catch((err) => console.error('Error fetching progress overview:', err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="py-24 flex flex-col items-center justify-center gap-3 text-purple-300">
        <Loader2 className="w-8 h-8 animate-spin text-cyan-400" />
        <span className="text-sm">Compiling performance analytics...</span>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="text-center py-20 text-slate-400">
        Unable to load performance metrics at this time.
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 text-xs font-bold text-emerald-400 uppercase tracking-wider mb-1">
          <TrendingUp className="w-4 h-4" />
          <span>Cognitive Telemetry</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          Performance Analytics
        </h1>
        <p className="text-xs sm:text-sm text-purple-300/70 mt-1">
          Real-time metrics tracking your mastery, diagnostic accuracy, and weekly practice velocity.
        </p>
      </div>

      {/* Top Level Metric Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="card-orbit p-5 border-emerald-500/25">
          <div className="text-xs font-bold text-emerald-400 uppercase tracking-wider mb-1">
            Overall Mastery
          </div>
          <div className="text-2xl sm:text-3xl font-black text-emerald-300">
            {data.overall_mastery}%
          </div>
          <div className="text-[11px] text-slate-400 mt-1">
            {data.topics_mastered} topics mastered
          </div>
        </div>

        <div className="card-orbit p-5 border-cyan-500/25">
          <div className="text-xs font-bold text-cyan-400 uppercase tracking-wider mb-1">
            Overall Accuracy
          </div>
          <div className="text-2xl sm:text-3xl font-black text-cyan-300">
            {data.overall_accuracy}%
          </div>
          <div className="text-[11px] text-slate-400 mt-1">
            {data.total_correct_answers} / {data.total_questions_attempted} correct
          </div>
        </div>

        <div className="card-orbit p-5 border-amber-500/25">
          <div className="text-xs font-bold text-amber-400 uppercase tracking-wider mb-1">
            Learning Streak
          </div>
          <div className="text-2xl sm:text-3xl font-black text-amber-300">
            {data.current_streak} Days
          </div>
          <div className="text-[11px] text-slate-400 mt-1">
            Longest: {data.longest_streak} days
          </div>
        </div>

        <div className="card-orbit p-5 border-purple-500/25">
          <div className="text-xs font-bold text-purple-400 uppercase tracking-wider mb-1">
            Total XP & Level
          </div>
          <div className="text-2xl sm:text-3xl font-black text-white">
            {data.total_xp.toLocaleString()} XP
          </div>
          <div className="text-[11px] text-slate-400 mt-1">
            Level {data.current_level} Scholar
          </div>
        </div>
      </div>

      {/* Recharts: XP & Accuracy over Time */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* XP Over Time Area Chart */}
        <div className="card-orbit p-6 border-purple-500/20">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Zap className="w-4 h-4 text-cyan-400" />
                XP Velocity (Past 7 Days)
              </h3>
              <p className="text-xs text-purple-300/60">Daily experience points accumulated</p>
            </div>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data.xp_history}>
                <defs>
                  <linearGradient id="xpGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.6} />
                    <stop offset="95%" stopColor="#06b6d4" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#26174a" />
                <XAxis dataKey="day" stroke="#94a3b8" fontSize={11} />
                <YAxis stroke="#94a3b8" fontSize={11} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#120b29',
                    borderColor: '#8b5cf6',
                    borderRadius: '0.75rem',
                    fontSize: '12px',
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="xp"
                  stroke="#8b5cf6"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#xpGradient)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Accuracy Trend Bar Chart */}
        <div className="card-orbit p-6 border-purple-500/20">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Brain className="w-4 h-4 text-emerald-400" />
                Diagnostic Accuracy Trend
              </h3>
              <p className="text-xs text-purple-300/60">Percentage of first-attempt correct answers</p>
            </div>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.accuracy_history}>
                <CartesianGrid strokeDasharray="3 3" stroke="#26174a" />
                <XAxis dataKey="day" stroke="#94a3b8" fontSize={11} />
                <YAxis stroke="#94a3b8" fontSize={11} domain={[0, 100]} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#120b29',
                    borderColor: '#10b981',
                    borderRadius: '0.75rem',
                    fontSize: '12px',
                  }}
                />
                <Bar dataKey="accuracy" fill="#10b981" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Subject-Wise Mastery Breakdown */}
      <div className="card-orbit p-6 border-purple-500/20">
        <h3 className="text-lg font-bold text-white mb-1">Subject-Wise Mastery Breakdown</h3>
        <p className="text-xs text-purple-300/60 mb-6">
          Aggregate curriculum mastery across all 6 core disciplines.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {data.subject_mastery.map((s) => (
            <div key={s.subject_id} className="p-4 rounded-xl bg-purple-950/30 border border-purple-500/15">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2.5">
                  <span className="text-2xl">{s.icon}</span>
                  <div>
                    <h4 className="text-sm font-bold text-white">{s.name}</h4>
                    <span className="text-[11px] text-slate-400">
                      {s.completed_topics} / {s.total_topics} topics completed
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-base font-extrabold text-white">{s.mastery}%</span>
                  <span className="text-[10px] text-purple-300 block">Mastery</span>
                </div>
              </div>

              <div className="w-full h-2 rounded-full bg-purple-950 overflow-hidden mt-3">
                <div
                  className="h-full rounded-full transition-all duration-700"
                  style={{
                    width: `${Math.max(5, s.mastery)}%`,
                    backgroundColor: s.color || '#8b5cf6',
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Weak Topics / Areas for Improvement */}
      {data.weak_topics && data.weak_topics.length > 0 && (
        <div className="card-orbit p-6 border-rose-500/30 bg-rose-950/10">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-rose-400" />
              <h3 className="text-lg font-bold text-white">Focus Areas & Weak Concepts</h3>
            </div>
            <span className="text-xs font-semibold text-rose-300">
              {data.weak_topics.length} topics flagged
            </span>
          </div>

          <div className="space-y-3">
            {data.weak_topics.map((wt) => (
              <div
                key={wt.topic_id}
                className="p-3.5 rounded-xl bg-[#0f0a24] border border-rose-500/20 flex flex-col sm:flex-row sm:items-center justify-between gap-3"
              >
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 text-[10px] font-bold">
                      {wt.subject_name}
                    </span>
                    <span className="text-sm font-bold text-white">{wt.topic_title}</span>
                  </div>
                  <p className="text-xs text-slate-300">{wt.recommendation}</p>
                </div>

                <div className="flex items-center gap-3 self-end sm:self-center">
                  <div className="text-right">
                    <span className="text-xs font-bold text-rose-400">{wt.accuracy}%</span>
                    <span className="text-[10px] text-slate-500 block">accuracy</span>
                  </div>
                  <NavLink
                    to="/practice"
                    className="px-3 py-1.5 rounded-lg bg-rose-500/20 hover:bg-rose-500/30 text-rose-200 border border-rose-500/30 text-xs font-semibold transition-colors"
                  >
                    Target Practice
                  </NavLink>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
