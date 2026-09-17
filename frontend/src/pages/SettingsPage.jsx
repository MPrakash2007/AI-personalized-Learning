import React, { useState } from 'react';
import {
  Settings as SettingsIcon, Bell, Volume2, Shield, Lock,
  Cpu, Moon, Sparkles, Check, Save, AlertTriangle
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import api from '../services/api';

export default function SettingsPage() {
  const { user, updateUser, logout } = useAuth();
  const { showToast } = useToast();

  // Learning Preferences
  const [dailyTarget, setDailyTarget] = useState(
    user?.preferences?.daily_target_minutes || 30
  );
  const [soundEffects, setSoundEffects] = useState(
    user?.preferences?.sound_effects !== undefined ? user.preferences.sound_effects : true
  );
  const [dailyReminder, setDailyReminder] = useState(
    user?.preferences?.daily_reminder !== undefined ? user.preferences.daily_reminder : true
  );
  const [aiTone, setAiTone] = useState('concise'); // concise, socratic, deep

  // Password Change
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isChangingPassword, setIsChangingPassword] = useState(false);

  const handleSavePreferences = async (e) => {
    e.preventDefault();
    try {
      const res = await api.put('/auth/profile', {
        daily_target_minutes: dailyTarget,
        sound_effects: soundEffects,
        daily_reminder: dailyReminder
      });
      updateUser(res.data);
      showToast('Learning preferences saved!', 'success');
    } catch (err) {
      showToast('Failed to save settings', 'error');
    }
  };

  const handleChangePassword = async (e) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      showToast('New passwords do not match', 'warning');
      return;
    }
    if (newPassword.length < 6) {
      showToast('Password must be at least 6 characters', 'warning');
      return;
    }

    try {
      setIsChangingPassword(true);
      await api.post('/auth/change-password', {
        current_password: currentPassword,
        new_password: newPassword
      });
      showToast('Password successfully updated!', 'success');
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch (err) {
      const msg = err.response?.data?.detail || 'Failed to update password';
      showToast(msg, 'error');
    } finally {
      setIsChangingPassword(false);
    }
  };

  return (
    <div className="space-y-8 animate-fadeIn pb-12 max-w-4xl mx-auto">
      {/* Header Banner */}
      <div className="relative overflow-hidden rounded-3xl p-6 sm:p-8 bg-gradient-to-r from-purple-950/70 via-[#140b2b]/90 to-slate-950/60 border border-purple-500/20 shadow-2xl backdrop-blur-xl">
        <div className="flex items-center gap-3">
          <div className="p-3 rounded-2xl bg-purple-900/40 text-purple-300 border border-purple-500/30">
            <SettingsIcon className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl sm:text-3xl font-black text-white">Platform Settings</h1>
            <p className="text-xs sm:text-sm text-slate-400 mt-1">
              Customize your learning cadence, AI explanation depth, and security preferences.
            </p>
          </div>
        </div>
      </div>

      {/* Preferences Section */}
      <div className="p-6 sm:p-8 rounded-3xl bg-[#140c2b]/80 border border-purple-500/20 backdrop-blur-xl shadow-xl space-y-6">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-cyan-400" />
          <span>Study Goals & Audio</span>
        </h3>

        <form onSubmit={handleSavePreferences} className="space-y-6">
          {/* Daily Study Target */}
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Daily Target Study Time
            </label>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {[15, 30, 45, 60].map((mins) => (
                <button
                  key={mins}
                  type="button"
                  onClick={() => setDailyTarget(mins)}
                  className={`py-2.5 px-4 rounded-xl border text-xs font-bold transition-all ${
                    dailyTarget === mins
                      ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white border-purple-400 shadow-md'
                      : 'bg-purple-950/30 border-purple-500/20 text-slate-400 hover:text-white'
                  }`}
                >
                  {mins} Minutes / day
                </button>
              ))}
            </div>
          </div>

          {/* Toggles */}
          <div className="space-y-4 pt-4 border-t border-purple-500/15">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Volume2 className="w-5 h-5 text-purple-400" />
                <div>
                  <div className="text-sm font-semibold text-white">Gamification Audio Effects</div>
                  <div className="text-xs text-slate-400">Play sounds on XP gains and quiz completions</div>
                </div>
              </div>
              <input
                type="checkbox"
                checked={soundEffects}
                onChange={(e) => setSoundEffects(e.target.checked)}
                className="w-5 h-5 accent-cyan-500 rounded cursor-pointer"
              />
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Bell className="w-5 h-5 text-cyan-400" />
                <div>
                  <div className="text-sm font-semibold text-white">Daily Streak Reminders</div>
                  <div className="text-xs text-slate-400">Receive nudges before your streak resets at midnight</div>
                </div>
              </div>
              <input
                type="checkbox"
                checked={dailyReminder}
                onChange={(e) => setDailyReminder(e.target.checked)}
                className="w-5 h-5 accent-cyan-500 rounded cursor-pointer"
              />
            </div>
          </div>

          <div className="flex justify-end pt-4 border-t border-purple-500/15">
            <button
              type="submit"
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 text-white text-xs font-bold shadow-lg shadow-cyan-500/20 hover:scale-105 transition-all"
            >
              <Save className="w-3.5 h-3.5" />
              <span>Save Preferences</span>
            </button>
          </div>
        </form>
      </div>

      {/* AI Assistant Configuration */}
      <div className="p-6 sm:p-8 rounded-3xl bg-[#140c2b]/80 border border-purple-500/20 backdrop-blur-xl shadow-xl space-y-5">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <Cpu className="w-5 h-5 text-purple-400" />
          <span>AI Tutor Engine & Socratic Settings</span>
        </h3>

        <div className="p-4 rounded-2xl bg-purple-950/40 border border-purple-500/20 flex items-center justify-between">
          <div>
            <div className="text-sm font-semibold text-white">Current Intelligence Provider</div>
            <div className="text-xs text-cyan-400 mt-0.5">
              CodeOrbit RuleBasedSmartProvider (100% Offline & Instant)
            </div>
          </div>
          <span className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold">
            ACTIVE
          </span>
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
            Explanation Style
          </label>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {[
              { id: 'concise', name: 'Concise & Exam Focused', desc: 'Direct bullet points and formulas' },
              { id: 'socratic', name: 'Socratic Guiding', desc: 'Asks follow-up questions to test grasp' },
              { id: 'deep', name: 'Deep Academic', desc: 'Proofs, architecture & internal mechanics' }
            ].map((st) => (
              <div
                key={st.id}
                onClick={() => setAiTone(st.id)}
                className={`p-3.5 rounded-2xl border cursor-pointer transition-all ${
                  aiTone === st.id
                    ? 'bg-purple-950/80 border-cyan-400 shadow-md shadow-purple-950/50'
                    : 'bg-purple-950/20 border-purple-500/15 hover:border-purple-500/30'
                }`}
              >
                <div className="text-xs font-bold text-white">{st.name}</div>
                <div className="text-[11px] text-slate-400 mt-1">{st.desc}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Password & Security */}
      <div className="p-6 sm:p-8 rounded-3xl bg-[#140c2b]/80 border border-purple-500/20 backdrop-blur-xl shadow-xl space-y-6">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <Shield className="w-5 h-5 text-emerald-400" />
          <span>Security & Password</span>
        </h3>

        <form onSubmit={handleChangePassword} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
              Current Password
            </label>
            <input
              type="password"
              required
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl bg-purple-950/40 border border-purple-500/20 text-sm text-white focus:outline-none focus:border-cyan-400"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                New Password
              </label>
              <input
                type="password"
                required
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl bg-purple-950/40 border border-purple-500/20 text-sm text-white focus:outline-none focus:border-cyan-400"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                Confirm New Password
              </label>
              <input
                type="password"
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl bg-purple-950/40 border border-purple-500/20 text-sm text-white focus:outline-none focus:border-cyan-400"
              />
            </div>
          </div>

          <div className="flex justify-end pt-4 border-t border-purple-500/15">
            <button
              type="submit"
              disabled={isChangingPassword}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-purple-900/40 hover:bg-purple-800/60 border border-purple-500/30 text-purple-200 text-xs font-semibold transition-all hover:scale-105 active:scale-95 disabled:opacity-50"
            >
              <Lock className="w-3.5 h-3.5" />
              <span>{isChangingPassword ? 'Updating...' : 'Update Password'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
