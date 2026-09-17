import React, { useState, useEffect } from 'react';
import {
  User as UserIcon, Mail, GraduationCap, Building2, Calendar,
  Trophy, Flame, Zap, Award, Edit3, Shield, Star, CheckCircle2,
  Bookmark, Sparkles, BookOpen
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import api from '../services/api';

export default function ProfilePage() {
  const { user, updateUser } = useAuth();
  const { showToast } = useToast();
  const [achievements, setAchievements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    full_name: user?.full_name || '',
    college: user?.college || '',
    degree: user?.degree || 'B.Tech',
    branch: user?.branch || 'Computer Science and Engineering',
    graduation_year: user?.graduation_year || 2026,
    avatar_url: user?.avatar_url || ''
  });

  useEffect(() => {
    if (user) {
      setFormData({
        full_name: user.full_name || '',
        college: user.college || '',
        degree: user.degree || 'B.Tech',
        branch: user.branch || 'Computer Science and Engineering',
        graduation_year: user.graduation_year || 2026,
        avatar_url: user.avatar_url || ''
      });
    }
  }, [user]);

  useEffect(() => {
    const fetchAchievements = async () => {
      try {
        setLoading(true);
        const res = await api.get('/achievements');
        setAchievements(res.data);
      } catch (err) {
        console.error('Failed to load achievements:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchAchievements();
  }, []);

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    try {
      const res = await api.put('/auth/profile', formData);
      updateUser(res.data);
      setIsEditing(false);
      showToast('Profile updated successfully!', 'success');
    } catch (err) {
      showToast('Failed to update profile', 'error');
    }
  };

  const unlockedAchievements = achievements.filter((a) => a.is_unlocked);

  return (
    <div className="space-y-8 animate-fadeIn pb-12">
      {/* Student Profile Card Header */}
      <div className="relative overflow-hidden rounded-3xl p-6 sm:p-8 bg-gradient-to-r from-purple-950/70 via-[#140b2b]/90 to-indigo-950/60 border border-purple-500/20 shadow-2xl backdrop-blur-xl">
        <div className="absolute -right-10 -top-10 w-64 h-64 bg-purple-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="flex flex-col sm:flex-row items-center sm:items-start gap-6 relative z-10">
          {/* Avatar with Glow Ring */}
          <div className="relative">
            <div className="w-24 h-24 sm:w-28 sm:h-28 rounded-3xl bg-gradient-to-tr from-purple-600 via-cyan-500 to-indigo-500 p-[2.5px] shadow-2xl shadow-purple-600/40">
              <img
                src={
                  user?.avatar_url ||
                  `https://api.dicebear.com/7.x/bottts/svg?seed=${user?.full_name || 'CodeOrbit'}`
                }
                alt="Avatar"
                className="w-full h-full rounded-[22px] bg-[#0d081f] object-cover"
              />
            </div>
            <div className="absolute -bottom-2 -right-2 px-2.5 py-0.5 rounded-full bg-cyan-500 text-black text-xs font-black shadow-lg">
              LVL {user?.level || 12}
            </div>
          </div>

          {/* User Details */}
          <div className="flex-1 text-center sm:text-left">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <h1 className="text-2xl sm:text-3xl font-black text-white">
                  {user?.full_name || 'Engineering Student'}
                </h1>
                <div className="flex items-center justify-center sm:justify-start gap-2 text-xs text-slate-400 mt-1">
                  <Mail className="w-3.5 h-3.5 text-cyan-400" />
                  <span>{user?.email}</span>
                </div>
              </div>

              <button
                onClick={() => setIsEditing(!isEditing)}
                className="flex items-center justify-center gap-2 px-4 py-2 rounded-xl bg-purple-900/40 hover:bg-purple-800/60 border border-purple-500/30 text-purple-200 text-xs font-semibold transition-all"
              >
                <Edit3 className="w-3.5 h-3.5" />
                <span>{isEditing ? 'Cancel Editing' : 'Edit Profile'}</span>
              </button>
            </div>

            {/* Academic Info Chips */}
            <div className="flex items-center justify-center sm:justify-start gap-2.5 flex-wrap mt-4">
              <div className="flex items-center gap-1.5 px-3 py-1 rounded-xl bg-purple-950/60 border border-purple-500/20 text-xs text-purple-300">
                <GraduationCap className="w-3.5 h-3.5 text-cyan-400" />
                <span>{user?.degree || 'B.Tech'} in {user?.branch || 'CSE'}</span>
              </div>
              <div className="flex items-center gap-1.5 px-3 py-1 rounded-xl bg-purple-950/60 border border-purple-500/20 text-xs text-slate-300">
                <Building2 className="w-3.5 h-3.5 text-indigo-400" />
                <span>{user?.college || 'Engineering Institute'}</span>
              </div>
              <div className="flex items-center gap-1.5 px-3 py-1 rounded-xl bg-purple-950/60 border border-purple-500/20 text-xs text-slate-300">
                <Calendar className="w-3.5 h-3.5 text-purple-400" />
                <span>Class of {user?.graduation_year || 2026}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Highlight Stats Row */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-8 pt-6 border-t border-purple-500/15">
          <div className="p-3.5 rounded-2xl bg-purple-950/40 border border-purple-500/20 flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-amber-500/20 text-amber-300 border border-amber-500/30">
              <Flame className="w-5 h-5 text-amber-400" />
            </div>
            <div>
              <div className="text-xs text-slate-400 font-medium">Daily Streak</div>
              <div className="text-lg font-bold text-white">{user?.streak?.current_streak || 7} Days</div>
            </div>
          </div>

          <div className="p-3.5 rounded-2xl bg-purple-950/40 border border-purple-500/20 flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
              <Zap className="w-5 h-5 text-cyan-400" />
            </div>
            <div>
              <div className="text-xs text-slate-400 font-medium">Total Orbit XP</div>
              <div className="text-lg font-bold text-white">{user?.xp?.toLocaleString()}</div>
            </div>
          </div>

          <div className="p-3.5 rounded-2xl bg-purple-950/40 border border-purple-500/20 flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-yellow-500/20 text-yellow-300 border border-yellow-500/30">
              <Trophy className="w-5 h-5 text-yellow-400" />
            </div>
            <div>
              <div className="text-xs text-slate-400 font-medium">Unlocked Badges</div>
              <div className="text-lg font-bold text-white">{unlockedAchievements.length} / {achievements.length}</div>
            </div>
          </div>

          <div className="p-3.5 rounded-2xl bg-purple-950/40 border border-purple-500/20 flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-purple-500/20 text-purple-300 border border-purple-500/30">
              <Star className="w-5 h-5 text-purple-400" />
            </div>
            <div>
              <div className="text-xs text-slate-400 font-medium">Longest Streak</div>
              <div className="text-lg font-bold text-white">{user?.streak?.longest_streak || 14} Days</div>
            </div>
          </div>
        </div>
      </div>

      {/* Edit Profile Form (Shown conditionally) */}
      {isEditing && (
        <div className="p-6 sm:p-8 rounded-3xl bg-[#140b2b]/90 border border-purple-500/30 backdrop-blur-xl shadow-2xl animate-fadeIn">
          <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <Edit3 className="w-4 h-4 text-cyan-400" />
            <span>Update Academic Details</span>
          </h3>

          <form onSubmit={handleUpdateProfile} className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                  Full Name
                </label>
                <input
                  type="text"
                  value={formData.full_name}
                  onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                  className="w-full px-4 py-2.5 rounded-xl bg-purple-950/40 border border-purple-500/20 text-sm text-white focus:outline-none focus:border-cyan-400"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                  College / University
                </label>
                <input
                  type="text"
                  value={formData.college}
                  onChange={(e) => setFormData({ ...formData, college: e.target.value })}
                  className="w-full px-4 py-2.5 rounded-xl bg-purple-950/40 border border-purple-500/20 text-sm text-white focus:outline-none focus:border-cyan-400"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                  Degree
                </label>
                <input
                  type="text"
                  value={formData.degree}
                  onChange={(e) => setFormData({ ...formData, degree: e.target.value })}
                  className="w-full px-4 py-2.5 rounded-xl bg-purple-950/40 border border-purple-500/20 text-sm text-white focus:outline-none focus:border-cyan-400"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                  Engineering Branch
                </label>
                <input
                  type="text"
                  value={formData.branch}
                  onChange={(e) => setFormData({ ...formData, branch: e.target.value })}
                  className="w-full px-4 py-2.5 rounded-xl bg-purple-950/40 border border-purple-500/20 text-sm text-white focus:outline-none focus:border-cyan-400"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                  Graduation Year
                </label>
                <input
                  type="number"
                  value={formData.graduation_year}
                  onChange={(e) => setFormData({ ...formData, graduation_year: parseInt(e.target.value) || 2026 })}
                  className="w-full px-4 py-2.5 rounded-xl bg-purple-950/40 border border-purple-500/20 text-sm text-white focus:outline-none focus:border-cyan-400"
                />
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-4 border-t border-purple-500/20">
              <button
                type="button"
                onClick={() => setIsEditing(false)}
                className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 text-white text-xs font-bold shadow-lg shadow-cyan-500/20 transition-all hover:scale-105"
              >
                Save Changes
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Badges & Achievements Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-xl font-bold text-white flex items-center gap-2">
              <Trophy className="w-5 h-5 text-amber-400" />
              <span>Earned Achievements & Badges</span>
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Milestones unlocked through continuous revision, quizzes, and streak consistency.
            </p>
          </div>
          <span className="text-xs font-bold text-cyan-400 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30">
            {unlockedAchievements.length} Unlocked
          </span>
        </div>

        {loading ? (
          <div className="p-12 text-center text-slate-400">Loading your accomplishments...</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {achievements.map((ach) => (
              <div
                key={ach.id}
                className={`p-5 rounded-2xl border transition-all flex items-start gap-4 backdrop-blur-xl ${
                  ach.is_unlocked
                    ? 'bg-[#140c2b]/80 border-purple-500/30 hover:border-purple-500/50 shadow-lg'
                    : 'bg-[#0d071d]/40 border-purple-500/10 opacity-60'
                }`}
              >
                <div
                  className={`w-12 h-12 rounded-2xl flex items-center justify-center text-2xl flex-shrink-0 ${
                    ach.is_unlocked
                      ? 'bg-gradient-to-tr from-amber-500/20 to-purple-500/20 border border-amber-500/30'
                      : 'bg-slate-900 border border-slate-800 grayscale'
                  }`}
                >
                  {ach.icon}
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-1">
                    <h4 className="text-sm font-bold text-white truncate">{ach.title}</h4>
                    {ach.is_unlocked ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                    ) : (
                      <span className="text-[10px] text-slate-400 flex-shrink-0 font-semibold">
                        LOCKED
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-slate-400 mt-1 line-clamp-2 leading-relaxed">
                    {ach.description}
                  </p>
                  <div className="mt-2 text-[11px] font-bold text-amber-400">
                    +{ach.xp_reward} XP
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
