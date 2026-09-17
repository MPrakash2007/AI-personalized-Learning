import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import {
  Flame, Zap, Trophy, Brain, ArrowRight, Sparkles, CheckCircle2,
  BookOpen, Clock, Target, AlertTriangle, Loader2
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import SubjectCard from '../components/Learning/SubjectCard';

export default function DashboardPage() {
  const { user } = useAuth();
  const [subjects, setSubjects] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [quests, setQuests] = useState([]);
  const [loading, setLoading] = useState(true);

  // Time-based greeting (Good morning / afternoon / evening)
  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 18) return 'Good afternoon';
    return 'Good evening';
  };

  useEffect(() => {
    const fetchDashboardData = async () => {
      setLoading(true);
      try {
        const [subRes, recRes, questRes] = await Promise.all([
          api.get('/subjects'),
          api.get('/recommendations'),
          api.get('/quests/today'),
        ]);
        setSubjects(subRes.data);
        setRecommendations(recRes.data.recommendations || []);
        setQuests(questRes.data || []);
      } catch (err) {
        console.error('Failed to load dashboard data:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboardData();
  }, []);

  // Compute overall average mastery
  const overallMastery = subjects.length
    ? Math.round(subjects.reduce((acc, s) => acc + s.overall_mastery, 0) / subjects.length)
    : 78;

  // Active recommended item
  const activeRec = recommendations[0] || {
    title: 'Practice Functional Dependencies',
    reason: 'You have answered 4 of the last 7 normalization questions incorrectly.',
    action_url: '/learn/dbms/normalization',
    estimated_minutes: 8,
  };

  if (loading) {
    return (
      <div className="py-24 flex flex-col items-center justify-center gap-4 text-purple-300">
        <Loader2 className="w-10 h-10 animate-spin text-cyan-400" />
        <p className="text-sm font-medium">Loading your personalized learning orbit...</p>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* 1. Welcome & Greeting Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center gap-2">
            {getGreeting()}, {user?.full_name?.split(' ')[0] || 'Student'} 👋
          </h1>
          <p className="text-xs sm:text-sm text-purple-300/70 mt-1">
            Ready to continue your learning journey?
          </p>
        </div>

        {/* Level Banner */}
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-purple-950/40 border border-purple-500/25 self-start md:self-auto text-xs">
          <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
          <span className="text-slate-300">Engineering Scholar</span>
          <span className="px-2 py-0.5 rounded bg-purple-500/30 text-purple-200 font-bold">
            Level {user?.level || 12}
          </span>
        </div>
      </div>

      {/* 2. Top Metric Dials (Streak, XP, Level, Overall Mastery) */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Streak */}
        <div className="card-orbit p-5 flex items-center gap-4 border-amber-500/20">
          <div className="w-12 h-12 rounded-2xl bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-amber-400">
            <Flame className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <div className="text-xs font-semibold text-amber-300/80 uppercase tracking-wider">
              Streak
            </div>
            <div className="text-xl sm:text-2xl font-black text-white">
              {user?.streak?.current_streak || 7} Days
            </div>
          </div>
        </div>

        {/* XP */}
        <div className="card-orbit p-5 flex items-center gap-4 border-cyan-500/20">
          <div className="w-12 h-12 rounded-2xl bg-cyan-500/20 border border-cyan-500/40 flex items-center justify-center text-cyan-400">
            <Zap className="w-6 h-6" />
          </div>
          <div>
            <div className="text-xs font-semibold text-cyan-300/80 uppercase tracking-wider">
              Total XP
            </div>
            <div className="text-xl sm:text-2xl font-black text-white">
              {user?.xp?.toLocaleString() || '2,450'}
            </div>
          </div>
        </div>

        {/* Level */}
        <div className="card-orbit p-5 flex items-center gap-4 border-purple-500/20">
          <div className="w-12 h-12 rounded-2xl bg-purple-500/20 border border-purple-500/40 flex items-center justify-center text-purple-400">
            <Trophy className="w-6 h-6" />
          </div>
          <div>
            <div className="text-xs font-semibold text-purple-300/80 uppercase tracking-wider">
              Level
            </div>
            <div className="text-xl sm:text-2xl font-black text-white">
              Level {user?.level || 12}
            </div>
          </div>
        </div>

        {/* Overall Mastery */}
        <div className="card-orbit p-5 flex items-center gap-4 border-emerald-500/20">
          <div className="w-12 h-12 rounded-2xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400">
            <Brain className="w-6 h-6" />
          </div>
          <div>
            <div className="text-xs font-semibold text-emerald-300/80 uppercase tracking-wider">
              Mastery
            </div>
            <div className="text-xl sm:text-2xl font-black text-emerald-300">
              {overallMastery}%
            </div>
          </div>
        </div>
      </div>

      {/* 3. Continue Learning & AI Recommendation Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Continue Learning In-Progress Card */}
        <div className="lg:col-span-1 card-orbit p-6 flex flex-col justify-between border-cyan-500/30 relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-32 h-32 bg-cyan-500/10 rounded-full blur-2xl pointer-events-none" />

          <div>
            <div className="flex items-center justify-between mb-4">
              <span className="text-xs font-bold text-cyan-400 uppercase tracking-wider">
                Continue Learning
              </span>
              <span className="text-2xl">🗄️</span>
            </div>

            <h3 className="text-xl font-bold text-white mb-1">DBMS</h3>
            <div className="text-sm font-semibold text-purple-200 mb-4">Normalization</div>

            <div className="space-y-2 mb-6">
              <div className="flex justify-between text-xs text-slate-300 font-medium">
                <span>Progress</span>
                <span className="text-cyan-300 font-bold">65%</span>
              </div>
              <div className="w-full h-2 rounded-full bg-purple-950/80 border border-purple-500/20 overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-purple-500 to-cyan-400 rounded-full"
                  style={{ width: '65%' }}
                />
              </div>
            </div>
          </div>

          <NavLink
            to="/learn/dbms/normalization"
            className="w-full py-2.5 px-4 rounded-xl text-xs font-bold bg-gradient-to-r from-purple-600 to-cyan-500 text-white shadow-lg shadow-purple-600/30 hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center gap-2"
          >
            <span>Continue Lesson</span>
            <ArrowRight className="w-4 h-4" />
          </NavLink>
        </div>

        {/* AI Recommended For You */}
        <div className="lg:col-span-2 card-orbit p-6 flex flex-col justify-between border-purple-500/30 relative overflow-hidden">
          <div className="absolute -top-10 -right-10 w-40 h-40 bg-pink-500/15 rounded-full blur-3xl pointer-events-none" />

          <div>
            <div className="flex items-center gap-2 text-xs font-bold text-pink-400 uppercase tracking-wider mb-3">
              <Sparkles className="w-4 h-4" />
              <span>AI Recommended For You</span>
            </div>

            <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4 mb-4">
              <div>
                <h3 className="text-lg sm:text-xl font-bold text-white mb-2">
                  {activeRec.title}
                </h3>
                <div className="p-3 rounded-xl bg-purple-950/40 border border-purple-500/20 text-xs text-purple-200/90 leading-relaxed mb-3">
                  <span className="font-semibold text-purple-300">Analysis Reason: </span>
                  {activeRec.reason}
                </div>
              </div>

              <div className="shrink-0 flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-purple-900/40 border border-purple-500/30 text-purple-300 text-xs font-semibold self-start">
                <Clock className="w-3.5 h-3.5 text-cyan-400" />
                <span>{activeRec.estimated_minutes || 8} min practice</span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3 pt-3 border-t border-purple-500/15">
            <NavLink
              to={activeRec.action_url || '/learn/dbms/normalization'}
              className="px-6 py-2.5 rounded-xl text-xs font-bold bg-gradient-to-r from-pink-600 to-purple-600 text-white shadow-lg shadow-purple-600/30 hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center gap-2"
            >
              <span>Start Targeted Practice</span>
              <ArrowRight className="w-4 h-4" />
            </NavLink>
            <NavLink
              to="/ai-recommendations"
              className="px-4 py-2.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white transition-colors"
            >
              View All Recommendations →
            </NavLink>
          </div>
        </div>
      </div>

      {/* 4. Today's Goals (Daily Quests checklist) */}
      <div className="card-orbit p-6 border-purple-500/20">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Target className="w-5 h-5 text-rose-400" />
            <h3 className="text-lg font-bold text-white">Today's Goals</h3>
          </div>
          <NavLink
            to="/daily-quests"
            className="text-xs font-semibold text-cyan-400 hover:underline"
          >
            View All Quests →
          </NavLink>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {quests.map((q) => (
            <div
              key={q.id}
              className="p-4 rounded-xl bg-purple-950/30 border border-purple-500/20 flex flex-col justify-between"
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-semibold text-slate-200 truncate pr-2">
                  {q.title}
                </span>
                {q.is_completed ? (
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                ) : (
                  <span className="text-[11px] font-bold text-cyan-300">
                    {q.current_count}/{q.target_count}
                  </span>
                )}
              </div>

              <div className="w-full h-1.5 rounded-full bg-purple-950 overflow-hidden mb-2">
                <div
                  className="h-full bg-gradient-to-r from-purple-500 to-cyan-400 rounded-full"
                  style={{
                    width: `${Math.min(100, (q.current_count / q.target_count) * 100)}%`,
                  }}
                />
              </div>

              <div className="text-[10px] text-amber-300 font-semibold flex items-center gap-1">
                <Zap className="w-3 h-3 text-amber-400" />
                <span>+{q.xp_reward} XP reward</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 5. Your Subjects Grid (DBMS, OOPS, OS, DS, ML, CN) */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-xl font-bold text-white">Your Subjects</h3>
            <p className="text-xs text-purple-300/60">Choose a subject to continue your path</p>
          </div>
          <NavLink to="/learn" className="text-xs font-semibold text-cyan-400 hover:underline">
            View All Curriculums →
          </NavLink>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {subjects.map((subj) => (
            <SubjectCard key={subj.id} subject={subj} />
          ))}
        </div>
      </div>
    </div>
  );
}
